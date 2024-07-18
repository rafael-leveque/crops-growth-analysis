import numpy
from pystac import Item
from PIL import Image
import requests
import xarray


def get_bands_datasets(sentinel_item: Item) -> xarray.Dataset:
    """Get bands datasets
    """
    red = get_image(sentinel_item, "B04")
    nir = get_image(sentinel_item, "B08")
    swir = get_image(sentinel_item, "B11")
    return xarray.Dataset([red, nir, swir])


def get_image(sentinel_item: Item, band: str) -> Image.Image:
    """Get image from sentinel data
    """
    url = sentinel_item.item.assets[band].href
    raw_image = requests.get(url, stream=True).raw
    image = Image.open(raw_image)
    image_array = numpy.array(image)
    data_array = xarray.DataArray(image_array, dims=["y", "x"], name=band)
    return data_array
