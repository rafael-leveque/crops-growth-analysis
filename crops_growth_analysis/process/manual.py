"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import numpy
import xarray

from crops_growth_analysis.extract import csv
from crops_growth_analysis.logger import log
from crops_growth_analysis.process.images import ItemImages


def process_parcel(parcel: csv.Parcel) -> xarray.DataArray:
    """
    Process a parcel. Calculate NDVI and NDMI from each time of the parcel.
    """
    data_arrays: list[xarray.DataArray] = []
    for item in parcel.sentinel_items:
        images = ItemImages(item, parcel.polygon)
        log.debug("Loading SCL and NIR")
        nir = images.load("B08")
        scl = images.load("SCL", interp_like=nir, mask=True)
        nir = nir.where(scl < 7).where(scl > 1)
        del scl
        log.debug("Calculating NDVI")
        red = images.load("B04")
        ndvi = (nir - red) / (nir + red)
        del red
        log.debug("Calculating NDMI")
        swir = images.load("B11", interp_like=nir)
        ndmi = (nir - swir) / (nir + swir)
        del swir
        del nir
        data_arrays.append(
            xarray.DataArray(
                data=[ndvi, ndmi],
                dims=["index_type", "y", "x"],
                coords={
                    "index_type": ["ndvi", "ndmi"],
                    "y": ndvi.y,
                    "x": ndvi.x,
                },
            )
        )
        del ndvi, ndmi
    log.debug("Concatenating results")
    return xarray.concat(data_arrays, dim="time").assign_coords(
        time=[
            numpy.datetime64(item.datetime) for item in parcel.sentinel_items
        ]
    )
