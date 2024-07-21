"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import stackstac
import xarray
from pystac import ItemCollection

from crops_growth_analysis.logger import log


def process_parcel(items: ItemCollection) -> xarray.DataArray:
    """Process a parcel using stackstac"""
    bands = stackstac.stack(items, assets=["B04", "B08", "B11", "SCL"])
    log.info("Calculating NDVI")
    ndvi = (bands.sel(band="B08") - bands.sel(band="B04")) / (
        bands.sel(band="B08") + bands.sel(band="B04")
    )
    log.info("Calculating NDMI")
    ndmi = (bands.sel(band="B08") - bands.sel(band="B11")) / (
        bands.sel(band="B08") + bands.sel(band="B11")
    )
    return xarray.concat([ndvi, ndmi], dim="band").assign_coords(
        coords={"band": ["ndvi", "ndmi"]}
    )
