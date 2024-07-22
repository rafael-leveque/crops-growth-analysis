"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import xarray

from crops_growth_analysis.extract import csv
from crops_growth_analysis.logger import log
from crops_growth_analysis.process.images import ItemImages


def process_parcel(parcel: csv.Parcel) -> xarray.DataArray:
    """Process a parcel"""
    data_arrays: list[xarray.DataArray] = []
    for item in parcel.sentinel_items:
        images = ItemImages(item, parcel.polygon)
        log.debug("Loading SCL and NIR")
        scl = images.load("SCL")
        nir = images.load("B08").where(scl < 7).where(scl > 1)
        del scl
        log.debug("Calculating NDVI")
        red = images.load("B04")
        log.debug("Calculate NDVI")
        ndvi = (nir - red) / (nir + red)
        del red
        log.debug("Calculating NDMI")
        swir = images.load("B11")
        ndmi = (nir - swir) / (nir + swir)
        del swir
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
    log.debug("Concatenating results")
    return xarray.concat(data_arrays, dim="time").assign_coords(
        coords={"time": [item.datetime for item in parcel.sentinel_items]}
    )
