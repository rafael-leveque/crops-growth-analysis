"""Module to interact with the Sentinel-2 dataset."""

import planetary_computer  # type: ignore
import shapely.ops
from pyproj import CRS, Transformer
from pystac import ItemCollection
from pystac_client import Client
from shapely import Polygon

catalog = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)


def search_polygon(polygon: Polygon) -> ItemCollection:
    """Search for Sentinel-2 data within a polygon."""
    # Put the polygon in the same coordinate system as the catalog
    wgs64_polygon = shapely.ops.transform(
        Transformer.from_crs(
            CRS("EPSG:2154"), CRS("EPSG:4326"), always_xy=True
        ).transform,
        polygon,
    )
    return catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=wgs64_polygon,
        datetime="2024-06-01/2024-06-30",
    ).item_collection()
