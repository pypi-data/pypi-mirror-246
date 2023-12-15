# OSEF library

Library containing utilities to read and parse a stream, live or recorded, retrieved from an
**ALB** (**A**ugmented **L**iDAR **B**ox).

The stream is in the **OSEF** format (**O**pen **SE**rialization **F**ormat):
it's an Outsight-defined serialisation binary format used to encode data streaming out of the ALB. 
It is based on *TLV-encoding*.

For the full documentation, contact us @ https://support.outsight.ai

## Installation
Install from PyPi using pip:
```bash
pip install osef
``` 
## Usage
Open and parse an osef file or stream: 

```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

for frame_dict in osef.parse(osef_path):
    tracked_objects = osef.osef_frame.TrackedObjects(frame_dict)
```

By default, the parser processes the recorded data as quickly as your computer allows it,
so potentially faster than in real conditions. 
To process recorded data at the same pace as real time OSEF stream coming from an ALB,
set the parameter real_frequency = True
```python
frame_iterator = osef.parse(osef_path, True)
```

or
```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

with osef.parser.OsefStream(osef_path) as osef_stream:
    tlv_iterator = osef.parser.get_tlv_iterator(osef_stream)
    for index, tlv in tlv_iterator:
        tree = osef.parser.build_tree(tlv)
        frame_dict = osef.parser.parse_to_dict(tree)
        tracked_objects = osef.osef_frame.TrackedObjects(frame_dict)
```

To find more code samples, see Outsight Code Samples repository:
https://gitlab.com/outsight-public/outsight-code-samples/-/tree/master

### Frame helper
In order to simplify data access in a scan frame, helper classes have been added to the library:

```python
import osef
from osef import osef_frame

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

for frame_dict in osef.parse(osef_path):
    # Frame data
    frame = osef_frame.OsefFrame(frame_dict)
    timestamp = frame.timestamp
    
    # Cloud data
    augmented_cloud = osef_frame.AugmentedCloud(frame_dict)
    coordinates = augmented_cloud.cartesian_coordinates
    reflectivities = augmented_cloud.reflectivities
    
    # Tracking data
    tracking_objects = osef_frame.TrackedObjects(frame_dict)
    poses = tracking_objects.poses
    bounding_boxes = tracking_objects.bounding_boxes
```

> 📝 All public types have a helper property

For types that do not have a property, it is possible to access them like this:
```python
import osef
from osef import osef_frame, osef_types

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

for frame_dict in osef.parse(osef_path):
    
    # Tracking data
    tracking_objects = osef_frame.TrackedObjects(frame_dict)
    class_id_array = tracking_objects[osef_types.OsefKeys.CLASS_ID_ARRAY.value]
```
