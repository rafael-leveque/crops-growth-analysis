"""Module to store parcels and their NDVI and NDMI values in MongoDB"""

from datetime import datetime

import pymongo

from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log
from crops_growth_analysis.store.common import AbstractParcelStorage


class ParcelStorage(AbstractParcelStorage):
    """
    Parcel storage class
    Init client and create collections
    Provides methods to store parcels and timeseries
    """

    def __init__(self):
        """
        Init client and create collections
        """
        # Connect to MongoDB
        log.debug("Connecting to MongoDB")
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mongo-netcarbon"]
        self.parcels = self.db["parcels"]
        self.ndvi = self.db["ndvi"]
        self.ndmi = self.db["ndmi"]

    def store_parcel_info(self, parcel: Parcel):
        """
        Store parcel information in Mongo DB
        """
        document = {
            "_id": parcel.id,
            "polygon": parcel.polygon.wkt,
            "processed_datetimes": [
                item.datetime for item in parcel.sentinel_items
            ],
        }
        self.parcels.update_one(
            {"_id": parcel.id}, {"$set": document}, upsert=True
        )

    def store_ds(
        self,
        parcel_id: str,
        index_type: str,
        time: datetime,
        data: bytes = None,
        url: str = None,
    ):
        """
        Store a single timeserie dataset in Mongo DB
        Either with binary data or with a URL
        """
        document = {
            "parcel_id": parcel_id,
            "datetime": time,
        }
        collection = self.ndvi if index_type == "ndvi" else self.ndmi
        collection.replace_one(
            document,
            {**document, "data": data, "url": url},
            upsert=True,
        )

    def close(self):
        """
        Close the client
        """
        self.client.close()
        log.debug("MongoDB client closed")
