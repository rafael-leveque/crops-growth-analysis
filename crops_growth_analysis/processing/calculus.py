"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import numpy
import xarray

from logger import log


def format_as_dataset(data: dict[str, xarray.DataArray]) -> xarray.Dataset:
    """
    Make the required changes to the data so that it can be used as a dataset
    """
    # B11 and SCL are half the definition of B04 and B08
    # We need to upscale them
    log.info("Upscaling B11 and SCL")
    data["B11"] = upscale_array(data["B11"])
    data["SCL"] = upscale_array(data["SCL"])
    return xarray.Dataset(data)


def upscale_array(da: xarray.DataArray) -> xarray.DataArray:
    """Double size of the array, using linear interpolation"""
    return da.interp(
        coords={
            k: numpy.linspace(0, v - 1, v * 2) for k, v in da.sizes.items()
        }
    ).assign_coords(
        coords={k: numpy.arange(v * 2) for k, v in da.sizes.items()}
    )


def ndvi_and_ndmi(ds: xarray.Dataset) -> xarray.Dataset:
    """Filter on SCL and calculate NDVI and NDMI"""
    log.info("Filtering on SCL")
    ds_clean = ds.where(ds["SCL"] < 7 & ds["SCL"] > 1)
    nir = ds_clean["B08"]
    red = ds_clean["B04"]
    swir = ds_clean["B11"]
    log.info("Calculating NDVI and NDMI")
    ndvi = (nir - red) / (nir + red)
    ndmi = (nir - swir) / (nir + swir)
    return xarray.Dataset({"NDVI": ndvi, "NDMI": ndmi})
