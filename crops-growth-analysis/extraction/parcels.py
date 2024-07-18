
# Read data csv without panda

import csv
from dataclasses import dataclass
import shapely
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

@dataclass
class Parcel:
    id: str
    polygon: Polygon
    planetarium_data = None

def read_csv(file_path: str) -> list[Parcel]:
    """
    Read a parcel csv file and keep only the id and geometry columns
    Return a list of parcels with an ID and a polygon
    """
    parcels: list[Parcel] = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader, None)
        for row in reader:
            id = row[0]
            polygon = shapely.from_wkt(row[7])
            parcels.append(Parcel(id, polygon))
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
    """
    Plot the data on a map
    """
    plt.figure()
    for id, polygon in parcels:
        x, y = polygon.exterior.xy
        center = polygon.centroid

        # Draw polygon and label it
        plt.plot(x, y, color='blue', linewidth=2)
        plt.fill(x, y, color='skyblue', alpha=0.5)
        plt.text(center.x, center.y, id, fontsize=12, ha='center', va='center', color='black')

    plt.title(f'{title} fields')
    plt.grid(True)
    plt.show()
