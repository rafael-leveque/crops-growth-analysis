from dataclasses import dataclass
import planetary_computer
from pystac import Item
from pystac_client import Client
from shapely import Polygon
from PIL import Image


@dataclass
class SentinelData:
    item: Item
    scl: Image.Image = None


class Sentinel:

    def __init__(self):
        self.__catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

    def search_polygon(self, polygon: Polygon) -> list[SentinelData]:
        return [
            SentinelData(item)
            for item in self.__catalog.search(
                collections=["sentinel-2-l2a"],
                intersects=polygon,
                datetime="2024",
            ).item_collection()
        ]
