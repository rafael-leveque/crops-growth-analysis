"""
Module to load images from Sentinel-2 data
"""

import numpy
import requests
import xarray
from PIL import Image
from pystac import Item
from logger import log


Image.MAX_IMAGE_PIXELS = None


def get_bands(sentinel_item: Item) -> dict[str, xarray.DataArray]:
    """Get bands dataarray from sentinel data"""
    return {
        band: load_band(sentinel_item, band)
        for band in ["B04", "B08", "B11", "SCL"]
    }


def load_band(sentinel_item: Item, band: str) -> xarray.DataArray:
    """Get image from sentinel data"""
    log.info(f"Loading image {band}")
    url = sentinel_item.assets[band].href
    raw_image = requests.get(url, stream=True, timeout=10).raw
    log.info("Reading image")
    image = Image.open(raw_image)
    log.info("Converting image to array")
    image_array = numpy.array(image)
    data_array = xarray.DataArray(image_array, dims=["y", "x"], name=band)
    return data_array
