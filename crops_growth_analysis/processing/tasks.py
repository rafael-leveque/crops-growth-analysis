"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import numpy
import xarray
from pystac import Item

from crops_growth_analysis.logger import log
from crops_growth_analysis.processing import images


def get_scl(sentinel_data: Item) -> xarray.DataArray:
    """Filter out clouds from SCL"""
    scl = images.load_band(sentinel_data, "SCL")
    scl = scl.where(scl < 7).where(scl > 1)
    return upscale_array(scl)


def get_nir(sentinel_data: Item, scl: xarray.DataArray) -> xarray.DataArray:
    """Get NIR band from Sentinel data and filter out clouds"""
    return images.load_band(sentinel_data, "B08").where(scl)


def get_ndvi(sentinel_data: Item, nir: xarray.DataArray) -> xarray.DataArray:
    """Get NDVI from Sentinel data"""
    log.info("Loading RED")
    red = images.load_band(sentinel_data, "B04")
    log.info("Calculate NDVI")
    return (nir - red) / (nir + red)


def get_ndmi(sentinel_data: Item, nir: xarray.DataArray) -> xarray.DataArray:
    """Get NDMI from Sentinel data"""
    log.info("Loading SWIR")
    swir = images.load_band(sentinel_data, "B11")
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
        coords={k: numpy.arange(0, v * 2, 2) for k, v in da.sizes.items()}
    ).reindex(
        indexers={k: numpy.arange(v * 2) for k, v in da.sizes.items()},
        method="ffill",
    )
