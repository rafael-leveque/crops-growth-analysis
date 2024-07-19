"""
Module to load images from Sentinel-2 data
"""

import numpy
import requests
import xarray
from PIL import Image
from pystac import Item


def get_bands_datasets(sentinel_item: Item) -> xarray.Dataset:
    """Get bands datasets"""
    red = get_image(sentinel_item, "B04")
    nir = get_image(sentinel_item, "B08")
    swir = get_image(sentinel_item, "B11")
    return xarray.Dataset({"B04": red, "B08": nir, "B11": swir})


def get_image(sentinel_item: Item, band: str) -> xarray.DataArray:
    """Get image from sentinel data"""
    url = sentinel_item.assets[band].href
    raw_image = requests.get(url, stream=True, timeout=10).raw
    image = Image.open(raw_image)
    image_array = numpy.array(image)
    data_array = xarray.DataArray(image_array, dims=["y", "x"], name=band)
    return data_array
