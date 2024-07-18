import planetary_computer
from pystac import ItemCollection
from pystac_client import Client
from shapely import Polygon


class SentinelClient:

    def __init__(self):
        self.__catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

    def search_polygon(self, polygon: Polygon) -> ItemCollection:
        return self.__catalog.search(
            collections=["sentinel-2-l2a"],
            intersects=polygon,
            datetime="2024",
        ).item_collection()
