import xarray
from PIL import Image


def ndvi(ds: xarray.Dataset) -> xarray.DataArray:
    """
    Calculate NDVI only when scl does not have clouds
    """
    ds_clean = ds.where(ds["SCL"] < 7 & ds["SCL"] > 1)
    nir = ds_clean["B08"]
    red = ds_clean["B04"]
    swir = ds_clean["B11"]
    ndvi = (nir - red) / (nir + red)
    ndmi = (nir - swir) / (nir + swir)
    return xarray.Dataset({"NDVI": ndvi, "NDMI": ndmi})


def ndmi(dataset: xarray.Dataset) -> Image.Image:
    """
    Calculate NDMI
    """
    nir = dataset["B08"]
    swir = dataset["B11"]
    return (nir - swir) / (nir + swir)
