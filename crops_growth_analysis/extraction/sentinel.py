"""Module to interact with the Sentinel-2 dataset."""

import planetary_computer  # type: ignore
from pystac import ItemCollection
from pystac_client import Client
from shapely import Polygon

catalog = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)


def search_polygon(polygon: Polygon) -> ItemCollection:
    """Search for Sentinel-2 data within a polygon."""
    return catalog.search(
        collections=["sentinel-2-l2a"],
        intersects=polygon,
        datetime="2024",
    ).item_collection()
