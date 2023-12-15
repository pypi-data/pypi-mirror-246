"""unpacking functions for osef types"""
from struct import Struct
from typing import List

import numpy as np

from osef import constants
from osef import osef_types


def _get_value_unpacker(pack_format: str):
    def _parse_value(value: bytes) -> object:
        return (Struct(pack_format).unpack(value))[0]

    return _parse_value


def _get_array_unpacker(dtype: np.dtype, cols: int = 0):
    def _parse_array(value: bytes) -> np.ndarray:
        array = np.frombuffer(value, dtype=dtype)
        if cols > 0:
            array = np.reshape(array, (int(array.shape[0] / cols), cols))
        return array

    return _parse_array


def _get_structured_array_unpacker(dtype: np.dtype):
    def _parse_structured_array(value: bytes) -> np.ndarray:
        array = np.frombuffer(value, dtype=dtype)
        names = array.dtype.names
        if "__todrop" in names:
            names.remove("__todrop")
            array = array[names]
        return array

    return _parse_structured_array


def _bytes_unpacker(value: bytes) -> bytes:
    return value


def _get_dict_unpacker(pack_format: str, fields_names: List[str]):
    def _parse_dict(value: bytes) -> dict:
        array = list(Struct(pack_format).iter_unpack(value))
        return dict(zip(fields_names, array[0]))

    return _parse_dict


def _get_string_unpacker():
    def _parse_string(value: bytes) -> str:
        return value.decode("ascii")[:-1]

    return _parse_string


def _processing_bitfield_unpacker(value: bytes) -> dict:
    background_deleted = 0
    bitfield = Struct("<Q").unpack(value)[0]
    return {"background_deleted": (bitfield & (1 << background_deleted) != 0)}


def _bool_bitfield_unpacker(value: bytes) -> np.ndarray:
    if len(value) == 0:
        return np.array([], dtype=bool)
    np_8bit = np.frombuffer(value, dtype=np.uint8)
    return np.unpackbits(np_8bit, bitorder="little").astype(bool)


def _percept_class_unpacker(value: bytes) -> np.ndarray:
    dtype = [
        (constants.ClassKeys.CLASS_CODE, int),
        (constants.ClassKeys.CLASS_NAME, "<U12"),
    ]
    if len(value) == 0:
        return np.array(np.array([], dtype=dtype))

    classes_iter = Struct("<H").iter_unpack(value)

    data_list = [(code[0], osef_types.PerceptId(code[0]).name) for code in classes_iter]
    return np.array(data_list, dtype=dtype)


def _class_array_unpacker(value: bytes) -> np.ndarray:
    dtype = [
        (constants.ClassKeys.CLASS_CODE, int),
        (constants.ClassKeys.CLASS_NAME, "<U12"),
    ]
    if len(value) == 0:
        return np.array([], dtype=dtype)

    classes_iter = Struct("<L").iter_unpack(value)
    data_list = [(code[0], osef_types.ClassId(code[0]).name) for code in classes_iter]
    return np.array(data_list, dtype=dtype)


def _lidar_model_unpacker(value: bytes) -> constants.LidarModel:

    if len(value) == 0:
        return constants.LidarModel(0, osef_types.LidarModelId.UNKNOWN.name)

    model_code = Struct("<B").unpack(value)[0]
    data_list = constants.LidarModel(
        model_code, osef_types.LidarModelId(model_code).name
    )
    return data_list


def _parse_timestamp(value: bytes) -> float:
    seconds, micro_seconds = Struct("<LL").unpack(value)
    return seconds + micro_seconds * 10**-6


def _pose_unpacker(value: bytes) -> dict:
    """Values to parse: tx ty tz Vxx Vyx Vzx Vxy Vyy Vzy Vxz Vyz Vzz

    Where rotation matrices should be at the end:
        | Vxx Vxy Vxz |
    R = | Vyx Vyy Vyz |
        | Vzx Vzy Vzz |
    """
    floats = np.array(Struct("<ffffffffffff").unpack(value), dtype=np.float32)

    # we have to transpose rotation matrices because values
    # are received column by column and not line by line
    return {
        constants.PoseKeys.TRANSLATION: np.array(floats[0:3]),
        constants.PoseKeys.ROTATION: np.transpose(
            np.reshape(np.array(floats[3:]), (3, 3))
        ),
    }


def _pose_array_unpacker(value: bytes) -> List:
    """Values to parse: tx ty tz Vxx Vyx Vzx Vxy Vyy Vzy Vxz Vyz Vzz

    Where rotation matrices should be at the end:
        | Vxx Vxy Vxz |
    R = | Vyx Vyy Vyz |
        | Vzx Vzy Vzz |
    """
    floats = np.array(
        list(Struct("<ffffffffffff").iter_unpack(value)), ndmin=2, dtype=np.float32
    )

    translations = floats[:, 0:3]
    rotations = np.transpose(floats[:, 3:].reshape((-1, 3, 3)), axes=[0, 2, 1])
    # we have to transpose rotation matrices because values
    # are received column by column and not line by line
    return [
        {constants.PoseKeys.TRANSLATION: t, constants.PoseKeys.ROTATION: r}
        for t, r in zip(translations, rotations)
    ]


def _object_properties_unpacker(value: bytes) -> np.ndarray:
    dtype = [
        (constants.ObjectProperties.ORIENTED, bool),
        (constants.ObjectProperties.IS_SEEN, bool),
        (constants.ObjectProperties.HAS_VALID_SLAM_POSE, bool),
        (constants.ObjectProperties.IS_STATIC, bool),
    ]
    if len(value) == 0:
        return np.array([], dtype=dtype)

    object_iter = Struct("<B").iter_unpack(value)
    property_list = [
        (bool(c[0] & 0x1), bool(c[0] & 0x2), bool(c[0] & 0x4), bool(c[0] & 0x8))
        for c in object_iter
    ]
    return np.array(property_list, dtype=dtype)


def _imu_unpacker(value: bytes) -> dict:
    value = Struct("<LLffffff").unpack(value)
    return {
        "timestamp": {"unix_s": value[0], "remaining_us": value[1]},
        "acceleration": value[2:5],
        "angular_velocity": value[5:8],
    }
