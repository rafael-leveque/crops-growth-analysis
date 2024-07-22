"""Module to calculate NDVI and NDMI from Sentinel-2 data"""

import shapely.ops
import stackstac
import xarray
from pyproj import CRS, Transformer

from crops_growth_analysis.extract import parcels
from crops_growth_analysis.logger import log


def process_parcel(parcel: parcels.Parcel) -> xarray.DataArray:
    """Process a parcel using stackstac"""
    log.info("Loading All Bands")
    bands = stackstac.stack(
        parcel.sentinel_items,
        assets=["B04", "B08", "B11", "SCL"],
        bounds=get_bounds(parcel),
    )
    log.info("Calculating NDVI")
    ndvi = (bands.sel(band="B08") - bands.sel(band="B04")) / (
        bands.sel(band="B08") + bands.sel(band="B04")
    )
    log.info("Calculating NDMI")
    ndmi = (bands.sel(band="B08") - bands.sel(band="B11")) / (
        bands.sel(band="B08") + bands.sel(band="B11")
    )
    log.info("Concatenating results")
    return xarray.concat([ndvi, ndmi], dim="band").assign_coords(
        coords={"band": ["ndvi", "ndmi"]}
    )


def get_bounds(parcel: parcels.Parcel) -> tuple[float, float, float, float]:
    """Take polygon and get bbox bounds"""
    # Put the bounds (EPSG:2154) in the same coordinate system
    # as the transform (EPSG:32631)
    log.info("Getting bounds")
    return shapely.ops.transform(
        Transformer.from_crs(
            CRS("EPSG:2154"), CRS("EPSG:32631"), always_xy=True
        ).transform,
        parcel.polygon,
    ).bounds
