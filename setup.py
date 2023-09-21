import io

from setuptools import find_packages, setup

with io.open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="raster2polygon",
    version="0.0.1",
    url="https://github.com/kshitijrajsharma/raster2polygon",
    author="Kshitij Raj Sharma",
    author_email="skshitizraj@gmail.com",
    description="A package for extracting vector prints from raster image",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "gdal",
        "rtree",
        "tqdm<=4.62.3",
        "pandas==1.5.3",
        "Pillow<=9.0.1",
        "geopandas<=0.10.2",
        "opencv-python==4.5.5.64",
        "opencv-python-headless<=4.7.0.68",
        "mercantile==1.2.1",
        "shapely",
        "rasterio",
    ],
)
