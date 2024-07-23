"""Module to store parcels and their NDVI and NDMI values in MongoDB"""

import pymongo
import io

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
        self.db = self.client["mongo-netcarbon"]
        self.parcels = self.db["parcels"]
        self.ndvi = self.db["ndvi"]
        self.ndmi = self.db["ndmi"]

    def store_parcel(self, parcel: Parcel):
        """
        Store the parcel in Mongo DB
        """
        # Store parcel information
        log.debug("Storing parcel information")
        self.store_parcel_info(parcel)
        # Store bands information
        log.debug("Storing bands information")
        for band_ds in parcel.bands:
            for time_ds in band_ds:
                current_band = time_ds["band"].item()
                current_time = time_ds["time"].item()
                log.debug(
                    "Storing band %s and time %s",
                    current_band,
                    current_time,
                )
                netcdf_buffer = io.BytesIO()
                time_ds.to_netcdf(netcdf_buffer)
                self.store_band(
                    parcel.id,
                    current_band,
                    current_time,
                    netcdf_buffer.getvalue(),
                )
        log.debug("Parcel stored")

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

    def store_band(
        self,
        parcel_id: str,
        band: str,
        time: str,
        data: bytes = None,
        url: str = None,
    ):
        """
        Store band information in Mongo DB
        Either with binary data or with a URL
        """
        document = {
            "parcel_id": parcel_id,
            "datetime": time,
        }
        collection = self.ndvi if band == "ndvi" else self.ndmi
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
