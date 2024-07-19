"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import xarray


def ndvi_and_ndmi(ds: xarray.Dataset) -> xarray.Dataset:
    """Filter on SCL and calculate NDVI and NDMI"""
    ds_clean = ds.where(ds["SCL"] < 7 & ds["SCL"] > 1)
    nir = ds_clean["B08"]
    red = ds_clean["B04"]
    swir = ds_clean["B11"]
    ndvi = (nir - red) / (nir + red)
    ndmi = (nir - swir) / (nir + swir)
    return xarray.Dataset({"NDVI": ndvi, "NDMI": ndmi})
