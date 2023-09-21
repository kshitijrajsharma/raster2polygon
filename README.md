## Raster 2 Polyon

Extracting vector polygons from raster images 

### Installation 
```
pip install raster2polygon
```

### Example : 
 
```python
from raster2polygon import polygonize

polygonize("data/masks_v2/4", "labels.geojson")
```

### Args : 

```
input_path: Path of the directory where the image files are stored.
output_path: Path of the output file.
remove_inputs: Clears the input image after geojson is produced
simplify_tolerance : the simplification accuracy as max. percentage of the arc length, in [0, 1] , Percentage Tolerance= ( Tolerance in Meters​ / Arc Length in Meters)×100
merging_distance_threshold : Minimum distance to define adjacent polygons, in meters , default 0.5 m
area_threshold (float, optional): Threshold for filtering polygon areas. Defaults to 1 sqm.
```