"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import math

import numpy
import shapely.ops
import xarray
from pyproj import CRS, Transformer
from pystac import Item

from crops_growth_analysis.extract import parcels
from crops_growth_analysis.logger import log
from crops_growth_analysis.process import images


def process_parcel(parcel: parcels.Parcel) -> xarray.DataArray:
    """Process a parcel"""
    data_arrays: list[xarray.DataArray] = []
    bounds = get_xy_bounds(parcel)
    for item in parcel.sentinel_items:
        log.info("Loading SCL and NIR")
        scl = get_scl(item).sel(bounds)
        nir = get_nir(item, scl, bounds)
        del scl
        log.info("Calculating NDVI")
        ndvi = get_ndvi(item, nir, bounds)
        log.info("Calculating NDMI")
        ndmi = get_ndmi(item, nir, bounds)
        del nir
        data_arrays.append(
            xarray.DataArray(
                data=[ndvi, ndmi],
                dims=["band", "y", "x"],
                coords={
                    "band": ["ndvi", "ndmi"],
                    "y": ndvi.y,
                    "x": ndvi.x,
                },
            )
        )
        del ndvi, ndmi
    log.info("Concatenating results")
    return xarray.concat(data_arrays, dim="time").assign_coords(
        coords={"time": [item.datetime for item in parcel.sentinel_items]}
    )


def get_xy_bounds(parcel: parcels.Parcel) -> dict[str, slice]:
    """Take coordinates bounds and turn it into xy bounds"""
    # Put the bounds (EPSG:2154) in the same coordinate system
    # as the transform (EPSG:32631)
    log.info("Getting bounds")
    proj_bounds = shapely.ops.transform(
        Transformer.from_crs(
            CRS("EPSG:2154"), CRS("EPSG:32631"), always_xy=True
        ).transform,
        parcel.polygon,
    ).bounds
    # Get the transform
    transform = images.load_transformation(parcel.sentinel_items[0])
    # Invert transform
    inv_transform = ~transform

    # Careful : raster y coordinates are actually inverted
    x_min, y_max = inv_transform * (proj_bounds[0], proj_bounds[1])
    x_max, y_min = inv_transform * (proj_bounds[2], proj_bounds[3])

    return {
        "x": slice(math.floor(x_min), math.ceil(x_max)),
        "y": slice(math.floor(y_min), math.ceil(y_max)),
    }


def get_scl(sentinel_data: Item) -> xarray.DataArray:
    """Filter out clouds from SCL"""
    scl = images.load_band(sentinel_data, "SCL")
    scl = scl.where(scl < 7).where(scl > 1)
    return upscale_array(scl)


def get_nir(
    sentinel_data: Item, scl: xarray.DataArray, bounds: dict[str, slice]
) -> xarray.DataArray:
    """Get NIR band from Sentinel data and filter out clouds"""
    return images.load_band(sentinel_data, "B08").sel(bounds).where(scl)


def get_ndvi(
    sentinel_data: Item, nir: xarray.DataArray, bounds: dict[str, slice]
) -> xarray.DataArray:
    """Get NDVI from Sentinel data"""
    log.info("Loading RED")
    red = images.load_band(sentinel_data, "B04").sel(bounds)
    log.info("Calculate NDVI")
    return (nir - red) / (nir + red)


def get_ndmi(
    sentinel_data: Item, nir: xarray.DataArray, bounds: dict[str, slice]
) -> xarray.DataArray:
    """Get NDMI from Sentinel data"""
    log.info("Loading SWIR")
    swir = images.load_band(sentinel_data, "B11")
    log.info("Upscaling SWIR")
    swir = upscale_array(swir).sel(bounds)
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
