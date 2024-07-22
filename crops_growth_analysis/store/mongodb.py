"""Module to store parcels and their NDVI and NDMI values in files"""

import pymongo

from crops_growth_analysis.extract.csv import Parcel


def store_parcel(parcel: Parcel):
    """
    Store the parcel in Mongo DB
    One document for parcel information and one document for each band
    """
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["crops_growth_analysis"]
    parcels = db["parcels"]
    ndvi = db["ndvi"]
    ndmi = db["ndmi"]

    # Store parcel information
    parcel_dict = {
        "_id": parcel.id,
        "polygon": parcel.polygon.wkt,
        "processed_datetimes": [
            item.datetime for item in parcel.sentinel_items
        ],
    }
    parcels.update_one({"_id": parcel.id}, {"$set": parcel_dict}, upsert=True)
    # Store bands information
    for band in parcel.bands:
        ndvi_dict = {
            "parcel_id": parcel.id,
            "datetime": band.datetime,
            "ndvi": band.ndvi,
        }
        ndvi.replace_one(
            {"parcel_id": parcel.id, "datetime": band.datetime},
            ndvi_dict,
            upsert=True,
        )
        ndmi_dict = {
            "parcel_id": parcel.id,
            "datetime": band.datetime,
            "ndmi": band.ndmi,
        }
        ndmi.replace_one(
            {"parcel_id": parcel.id, "datetime": band.datetime},
            ndmi_dict,
            upsert=True,
        )
