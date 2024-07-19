"""Module to import parcels from csv files (and display them on a map)"""

import csv
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import pyproj
import shapely
import xarray
from pystac import ItemCollection
from shapely.geometry import Polygon
from shapely.ops import transform


@dataclass
class Parcel:
    """Parcel dataclass, to be used throughout the application"""

    id: str
    polygon: Polygon
    wgs64_polygon: Polygon
    sentinel_data: ItemCollection = ItemCollection([])
    ndvi: list[xarray.Dataset] = field(default_factory=list)


def read_csv(file_path: str) -> list[Parcel]:
    """
    Read a parcel csv file and keep only the id and geometry columns
    Return a list of parcels with an ID and a polygon
    """
    parcels: list[Parcel] = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip header
        next(reader, None)
        for row in reader:
            parcel_id = row[0]
            geometry = shapely.from_wkt(row[7])
            if isinstance(geometry, Polygon):
                polygon = geometry
                wgs64_polygon = transform(
                    pyproj.Transformer.from_crs(
                        pyproj.CRS("EPSG:2154"), pyproj.CRS("EPSG:4326")
                    ).transform,
                    polygon,
                )
                parcels.append(Parcel(parcel_id, polygon, wgs64_polygon))
            else:
                raise ValueError(f"{parcel_id} is not a polygon")
    return parcels


def read_maize():
    """
    Read maize parcels from csv file
    Result is a list of parcels with an ID and a polygon
    """
    return read_csv("data/maize.csv")


def read_tournesol():
    """
    Read tournesol data from csv file
    Result is a list of parcels with an ID and a polygon
    """
    return read_csv("data/tournesol.csv")


def display_parcels(title: str, parcels: list[Parcel]):
    """Plot the data on a map"""
    plt.figure()
    for parcel in parcels:
        x, y = parcel.polygon.exterior.xy

        # Draw polygon and label it
        plt.plot(x, y, color="blue", linewidth=2)
        plt.fill(x, y, color="skyblue", alpha=0.5)

    plt.title(f"{title} fields")
    plt.grid(True)
    plt.show()
