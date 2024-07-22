"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import stackstac
import xarray

from crops_growth_analysis.extract import parcels
from crops_growth_analysis.logger import log


def process_parcel(parcel: parcels.Parcel) -> xarray.DataArray:
    """Process a parcel using stackstac"""
    # log.debug("Loading All Bands")
    bands = stackstac.stack(
        parcel.sentinel_items,
        assets=["B04", "B08", "B11", "SCL"],
        bounds=parcel.polygon.bounds,
        epsg=2154,
    )
    bands = bands.where(bands.sel(band="SCL") < 7).where(
        bands.sel(band="SCL") > 1
    )
    # log.debug("Calculating NDVI")
    ndvi = (bands.sel(band="B08") - bands.sel(band="B04")) / (
        bands.sel(band="B08") + bands.sel(band="B04")
    )
    # log.debug("Calculating NDMI")
    ndmi = (bands.sel(band="B08") - bands.sel(band="B11")) / (
        bands.sel(band="B08") + bands.sel(band="B11")
    )
    # log.debug("Concatenating results")
    return xarray.concat([ndvi, ndmi], dim="band").assign_coords(
        coords={"band": ["ndvi", "ndmi"]}
    )
