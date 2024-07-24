"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import numpy
import stackstac
import xarray
from shapely.geometry import Point

from crops_growth_analysis.extract import csv
from crops_growth_analysis.logger import log


def process_parcel(parcel: csv.Parcel) -> xarray.DataArray:
    """Process a parcel using stackstac"""
    log.debug("Loading All Bands")
    bands = stackstac.stack(
        parcel.sentinel_items,
        assets=["B04", "B08", "B11", "SCL"],
        bounds=parcel.polygon.bounds,
        epsg=2154,
    )
    bands = mask_parcel(parcel, bands)
    scl = bands.sel(band="SCL")
    bands = bands.where(scl < 7).where(scl > 1)
    log.debug("Calculating NDVI")
    red = bands.sel(band="B04")
    nir = bands.sel(band="B08")
    ndvi = (nir - red) / (nir + red)
    log.debug("Calculating NDMI")
    swir = bands.sel(band="B11")
    ndmi = (nir - swir) / (nir + swir)
    log.debug("Concatenating results")
    return xarray.concat([ndvi, ndmi], dim="index_type").assign_coords(
        index_type=["ndvi", "ndmi"]
    )


def mask_parcel(
    parcel: csv.Parcel, bands: xarray.DataArray
) -> xarray.DataArray:
    """Mask bands with parcel"""
    mask = xarray.apply_ufunc(
        numpy.vectorize(lambda x, y: parcel.polygon.contains(Point(x, y))),
        bands["x"],
        bands["y"],
        vectorize=True,
    )
    return bands.where(mask)
