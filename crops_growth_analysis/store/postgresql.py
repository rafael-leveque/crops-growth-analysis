"""Module to store parcels and their NDVI and NDMI values in PostgreSQL"""

import io

import psycopg2

from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log


class ParcelStorage:
    """
    Parcel storage class
    Init client and create tables
    Provides methods to store parcels and bands
    """

    def __init__(self):
        """
        Init client and create tables
        """
        # Connect to PostgreSQL
        log.debug("Connecting to PostgreSQL")
        self.conn = psycopg2.connect(
            dbname="crops_growth_analysis",
            user="crops_growth_analysis",
            password="crops_growth_analysis",
            host="localhost",
        )
        self.cursor = self.conn.cursor()

        # Create tables
        log.debug("Creating tables")
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS parcels (
                id TEXT PRIMARY KEY,
                polygon GEOMETRY(Polygon),
                processed_datetimes TIMESTAMP[]
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ndvi (
                parcel_id TEXT,
                datetime TIMESTAMP,
                data BYTEA,
                url TEXT,
                PRIMARY KEY (parcel_id, datetime)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ndmi (
                parcel_id TEXT,
                datetime TIMESTAMP,
                data BYTEA,
                url TEXT,
                PRIMARY KEY (parcel_id, datetime)
            )
            """
        )

    def store_parcel(self, parcel: Parcel):
        """
        Store the parcel in PostgreSQL
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
                    "Storing band %s and time %s", current_band, current_time
                )
                netcdf_buffer = io.BytesIO()
                time_ds.to_netcdf(netcdf_buffer)
                self.store_band(
                    parcel.id,
                    current_band,
                    current_time,
                    netcdf_buffer.getvalue(),
                )

    def store_parcel_info(self, parcel: Parcel):
        """
        Store parcel information in PostgreSQL
        """
        document = {
            "id": parcel.id,
            "polygon": parcel.polygon.wkt,
            "processed_datetimes": [
                item.datetime for item in parcel.sentinel_items
            ],
        }
        self.cursor.execute(
            """
            INSERT INTO parcels (id, polygon, processed_datetimes)
            VALUES (%(id)s, ST_GeomFromText(%(polygon)s), %(processed_datetimes)s)
            ON CONFLICT (id) DO UPDATE
            SET polygon = excluded.polygon,
                processed_datetimes = excluded.processed_datetimes
            """,
            document,
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
        Store band information in PostgreSQL
        Either with binary data or with a URL
        """
        document = {
            "parcel_id": parcel_id,
            "band": band,
            "datetime": time,
            "data": data,
            "url": url,
        }
        self.cursor.execute(
            """
            INSERT INTO %(band)s (parcel_id, datetime, data, url)
            VALUES (%(parcel_id)s, %(datetime)s, %(data)s, %(url)s)
            ON CONFLICT (parcel_id, datetime) DO UPDATE
            SET value = excluded.value
            """,
            document,
        )

    def close(self):
        """
        Close connection
        """
        # Commit and close connection
        log.debug("Committing and closing connection")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
