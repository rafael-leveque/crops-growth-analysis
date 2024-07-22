"""Module to store parcels and their NDVI and NDMI values in PostgreSQL"""

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
                ndvi DOUBLE PRECISION,
                PRIMARY KEY (parcel_id, datetime)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ndmi (
                parcel_id TEXT,
                datetime TIMESTAMP,
                ndmi DOUBLE PRECISION,
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
        parcel_dict = {
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
            parcel_dict,
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
            self.cursor.execute(
                """
                INSERT INTO ndvi (parcel_id, datetime, ndvi)
                VALUES (%(parcel_id)s, %(datetime)s, %(ndvi)s)
                ON CONFLICT (parcel_id, datetime) DO UPDATE
                SET ndvi = excluded.ndvi
                """,
                ndvi_dict,
            )
            log.debug("Storing ndmi %s", band.datetime)
            ndmi_dict = {
                "parcel_id": parcel.id,
                "datetime": band.datetime,
                "ndmi": band.ndmi,
            }
            self.cursor.execute(
                """
                INSERT INTO ndmi (parcel_id, datetime, ndmi)
                VALUES (%(parcel_id)s, %(datetime)s, %(ndmi)s)
                ON CONFLICT (parcel_id, datetime) DO UPDATE
                SET ndmi = excluded.ndmi
                """,
                ndmi_dict,
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
