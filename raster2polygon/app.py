# Standard library imports
import os
from pathlib import Path

from .get_polygons import get_polygons
from .merge_polygons import merge_polygons


def polygonize(
    input_path: str,
    output_path: str,
    remove_inputs: False,
    simplify_tolerance=0.01,
    merging_distance_threshold=0.5,
    area_threshold=1,
) -> None:
    """Polygonize raster tiles from the input path using AutoBFE's algorithm.

    There are two steps:
    1. It polygonizes each of the individual tiles first.
    2. Using GDAL buffering, it merges all the nearby polygons
    so that the split polygons get merged into one.

    Whether the images are georeferenced or not doesn't really matter.
    Even PNG images will do.

    CRS of the resulting GeoJSON file will be EPSG:4326.

    Args:
        input_path: Path of the directory where the image files are stored.
        output_path: Path of the output file.
        remove_inputs: Clears the input image after geojson is produced
        simplify_tolerance : the simplification accuracy as max. percentage of the arc length, in [0, 1] , Percentage Tolerance= ( Tolerance in Meters​ / Arc Length in Meters)×100
        merging_distance_threshold : Minimum distance to define adjacent polygons, in meters , default 0.5 m
        area_threshold (float, optional): Threshold for filtering polygon areas. Defaults to 1 sqm.

    Example::

        polygonize("data/masks_v2/4", "labels.geojson")
    """
    if os.path.exists(output_path):
        os.remove(output_path)
    base_path = Path(output_path).parents[0]
    base_path.mkdir(exist_ok=True, parents=True)

    get_polygons(
        input_path,
        "temp-labels.geojson",
        kernel_opening=1,
        simplify_threshold=simplify_tolerance,
    )
    merge_polygons(
        "temp-labels.geojson",
        output_path,
        distance_threshold=merging_distance_threshold,
        area_threshold=area_threshold,
    )
    os.remove("temp-labels.geojson")

    if remove_inputs:
        # Get a list of all .tif files in the directory
        tif_files = [f for f in os.listdir(input_path) if f.endswith(".tif")]

        # Loop through the list of .tif files and delete each one
        for file in tif_files:
            file_path = os.path.join(input_path, file)
            os.remove(file_path)
