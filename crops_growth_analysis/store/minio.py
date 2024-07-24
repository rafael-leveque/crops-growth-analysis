"""
Module to store parcels and their NDVI and NDMI values in Minio
backed by Postgresql or MongoDB metadata
"""

from datetime import datetime

import minio

import crops_growth_analysis.store.mongodb as mongodb
import crops_growth_analysis.store.postgresql as postgresql
from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log
from crops_growth_analysis.store.common import AbstractParcelStorage


class ParcelStorage(AbstractParcelStorage):
    """
    Parcel storage class
    Init client and create tables
    Provides methods to store parcels and timeseries
    """

    def __init__(
        self,
        metadata_backend: str = "mongodb",
        url: str = "localhost:9000",
        secure: bool = False,
    ):
        """Init clients and create buckets"""
        self.backend = (
            postgresql.ParcelStorage()
            if metadata_backend == "postgresql"
            else mongodb.ParcelStorage()
        )
        log.debug("Init Minio Client")
        self.minio_client = minio.Minio(
            url,
            access_key="minio",
            secret_key="netcarbon",
            secure=secure,
        )
        scheme = "https" if secure else "http"
        self.base_url = f"{scheme}://{url}"
        log.debug("Get Minio NDVI Bucket")
        if not self.minio_client.bucket_exists("ndvi"):
            self.minio_client.make_bucket("ndvi")
        log.debug("Get Minio NDMI Bucket")
        if not self.minio_client.bucket_exists("ndmi"):
            self.minio_client.make_bucket("ndmi")

    def store_parcel_info(self, parcel: Parcel):
        """
        Store parcel information in backend
        """
        self.backend.store_parcel_info(parcel)

    def store_ds(
        self,
        parcel_id: str,
        index_type: str,
        time: datetime,
        data: bytes = None,
        url: str = None,
    ):
        """
        Store a single timeserie dataset in Minio and metadata in backend
        """
        time_dir = time.strftime("%Y/%m/%d")
        object_name = (
            f"{parcel_id}/{time_dir}/{parcel_id}-{index_type}-{time}.nc"
        )
        self.minio_client.put_object(
            index_type,
            object_name,
            data,
            len(data),
            "application/octet-stream",
        )
        object_url = f"{self.base_url}/{index_type}/{object_name}"
        self.backend.store_ds(parcel_id, index_type, time, url=object_url)

    def close(self):
        """
        Close the backend
        """
        self.backend.close()
