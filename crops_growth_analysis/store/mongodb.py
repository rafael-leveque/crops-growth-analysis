"""Module to store parcels and their NDVI and NDMI values in MongoDB"""

import pymongo

from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log


class ParcelStorage:
    """
    Parcel storage class
    Init client and create collections
    Provides methods to store parcels and bands
    """

    def __init__(self):
        """
        Init client and create collections
        """
        # Connect to MongoDB
        log.debug("Connecting to MongoDB")
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["crops_growth_analysis"]
        self.parcels = self.db["parcels"]
        self.ndvi = self.db["ndvi"]
        self.ndmi = self.db["ndmi"]

    def store_parcel(self, parcel: Parcel):
        """
        Store the parcel in Mongo DB
        """
        # Store parcel information
        log.debug("Storing parcel information")
        parcel_dict = {
            "_id": parcel.id,
            "polygon": parcel.polygon.wkt,
            "processed_datetimes": [
                item.datetime for item in parcel.sentinel_items
            ],
        }
        self.parcels.update_one(
            {"_id": parcel.id}, {"$set": parcel_dict}, upsert=True
        )
        # Store bands information
        log.debug("Storing bands information")
        for band in parcel.bands:
            log.debug("Storing nvdi %s", band.datetime)
            ndvi_dict = {
                "parcel_id": parcel.id,
                "datetime": band.datetime,
                "ndvi": band.ndvi,
            }
            self.ndvi.replace_one(
                {"parcel_id": parcel.id, "datetime": band.datetime},
                ndvi_dict,
                upsert=True,
            )
            log.debug("Storing ndmi %s", band.datetime)
            ndmi_dict = {
                "parcel_id": parcel.id,
                "datetime": band.datetime,
                "ndmi": band.ndmi,
            }
            self.ndmi.replace_one(
                {"parcel_id": parcel.id, "datetime": band.datetime},
                ndmi_dict,
                upsert=True,
            )
        log.debug("Parcel stored")

    def close(self):
        """
        Close the client
        """
        self.client.close()
        log.debug("MongoDB client closed")
