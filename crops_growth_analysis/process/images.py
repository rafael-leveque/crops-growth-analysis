"""
Module to load images from Sentinel-2 data
"""

import numpy
import rasterio
import rasterio.transform
import requests
import xarray
from PIL import Image
from pystac import Item

from crops_growth_analysis.logger import log

Image.MAX_IMAGE_PIXELS = None


def load_transformation(sentinel_item: Item) -> rasterio.Affine:
    """Get transformation from sentinel data"""
    url = sentinel_item.assets["SCL"].href
    with rasterio.open(url) as src:
        # Since SCL is a 20m resolution image,
        # we need to divide the resolution by 2
        return src.transform * rasterio.Affine.scale(0.5, 0.5)


def load_band(sentinel_item: Item, band: str) -> xarray.DataArray:
    """Get image from sentinel data"""
    url = sentinel_item.assets[band].href
    log.info("Loading and Reading image")
    raw_image = requests.get(url, stream=True, timeout=10).raw
    image = Image.open(raw_image)
    # log.info("Converting image to array")
    image_array = numpy.array(image)
    data_array = xarray.DataArray(
        image_array,
        dims=["y", "x"],
        coords={
            "x": range(image_array.shape[1]),
            "y": range(image_array.shape[0]),
        },
        name=band,
    )
    return data_array
