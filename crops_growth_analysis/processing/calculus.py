"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import numpy
import xarray
from logger import log
from processing import images
from pystac import Item


def get_scl(sentinel_data: Item) -> xarray.DataArray:
    """Filter out clouds from SCL"""
    log.info("Loading SCL")
    scl = images.load_band(sentinel_data, "SCL")
    log.info("Filtering SCL")
    scl = scl.where(scl < 7 & scl > 1)
    log.info("Upscaling SCL")
    return upscale_array(scl)


def get_nir(sentinel_data: Item) -> xarray.DataArray:
    """Get NIR band from Sentinel data"""
    log.info("Loading NIR")
    return images.load_band(sentinel_data, "B08")


def get_ndvi(
    sentinel_data: Item, scl: xarray.DataArray, nir: xarray.DataArray
) -> xarray.DataArray:
    """Get NDVI from Sentinel data"""
    log.info("Calculating NDVI")
    log.info("Filtering NIR")
    nir = nir.where(scl)
    log.info("Loading RED")
    red = images.load_band(sentinel_data, "B04")
    log.info("Filtering RED")
    red = red.where(scl)
    log.info("Calculate NDVI")
    return (nir - red) / (nir + red)


def get_ndmi(
    sentinel_data: Item, scl: xarray.DataArray, nir: xarray.DataArray
) -> xarray.DataArray:
    """Get NDMI from Sentinel data"""
    log.info("Calculating NDMI")
    log.info("Filtering NIR")
    nir = nir.where(scl)
    log.info("Loading SWIR")
    swir = images.load_band(sentinel_data, "B11")
    log.info("Filtering SWIR")
    swir = swir.where(scl)
    log.info("Upscaling SWIR")
    swir = upscale_array(swir)
    log.info("Calculate NDMI")
    return (nir - swir) / (nir + swir)


def upscale_array(da: xarray.DataArray) -> xarray.DataArray:
    """Double size of the array, using linear interpolation"""
    # return upscale_using_interpolation(da)
    return upscale_using_reindex(da)


def upscale_using_interpolation(da: xarray.DataArray) -> xarray.DataArray:
    """Double size of the array, using linear interpolation"""
    return da.interp(
        coords={
            k: numpy.linspace(0, v - 1, v * 2) for k, v in da.sizes.items()
        }
    ).assign_coords(
        coords={k: numpy.arange(v * 2) for k, v in da.sizes.items()}
    )


def upscale_using_reindex(da: xarray.DataArray) -> xarray.DataArray:
    """Double size of the array, using reindex"""
    return da.assign_coords(
        coords={k: numpy.arange(v * 2, step=2) for k, v in da.sizes.items()}
    ).reindex(
        coords={k: numpy.arange(v * 2) for k, v in da.sizes.items()},
        method="ffill",
    )
