"""
Main script to run the crops growth analysis.
"""

import time

from crops_growth_analysis.display import basic
from crops_growth_analysis.extract import csv, sentinel
from crops_growth_analysis.logger import log
from crops_growth_analysis.process import external, manual
from crops_growth_analysis.store import common, minio, mongodb, postgresql

# Set the limits for parcels and assets.
# Set to -1 to disable limits.
PARCEL_LIMIT = -1
ASSETS_LIMIT = -1

# Set the processing method to use.
# One of "manual" or "external"
PROCESSING_METHOD = "external"

# Set the database to use.
# One of "postgresql", "minio" or "mongodb"
DATABASE = None

# Set the log level
log.setLevel("INFO")


def main():
    """
    Main function to run the crops growth analysis.
    """
    # Start Timer
    overall_start_time = time.time()

    log.info("--- Start Extract ---")
    start_time = time.time()
    parcels = extract()
    extract_time = time.time() - start_time
    log.info("--- Extract Time : %s ---", extract_time)

    log.info("--- Start Process ---")
    start_time = time.time()
    parcels = process(parcels)
    process_time = time.time() - start_time
    log.info("--- Process Time : %s ---", process_time)

    log.info("--- Start Store ---")
    start_time = time.time()
    store(parcels)
    store_time = time.time() - start_time
    log.info("--- Store Time : %s ---", store_time)

    log.info("--- Start Display ---")
    start_time = time.time()
    display(parcels)
    display_time = time.time() - start_time
    log.info("--- Display Time : %s ---", display_time)

    overall_time = time.time() - overall_start_time
    log.info("--- Summary ---")
    log.info("--- Extract Time : %s ---", extract_time)
    log.info("--- Process Time : %s ---", process_time)
    log.info("--- Store Time : %s ---", store_time)
    log.info("--- Display Time : %s ---", display_time)
    log.info("--- Overall Time : %s ---", overall_time)


def extract() -> list[csv.Parcel]:
    """
    Extract parcels and assets from CSV and Planetarium.
    """
    # Read csv parcels
    log.info(
        "Reading CSV %s",
        "" if PARCEL_LIMIT < 0 else f"(Limited to {PARCEL_LIMIT} parcels)",
    )
    parcels = (csv.read_maize() + csv.read_tournesol())[:PARCEL_LIMIT]

    log.info(
        "Searching planetarium data %s",
        "" if ASSETS_LIMIT < 0 else f"(Limited to {ASSETS_LIMIT} assets)",
    )
    for parcel in parcels:
        parcel.sentinel_items = sentinel.search_polygon(parcel.polygon)[
            :ASSETS_LIMIT
        ]

    return parcels


def process(parcels: list[csv.Parcel]) -> list[csv.Parcel]:
    """
    Process parcels to calculate NDVI and NDMI.
    """
    log.info("Calculating NDVI and NDMI")
    for parcel in parcels:
        log.debug("Processing parcel %s", parcel.id)
        if PROCESSING_METHOD == "manual":
            parcel.timeseries = manual.process_parcel(parcel)
        else:
            parcel.timeseries = external.process_parcel(parcel).compute()

    return parcels


def store(parcels: list[csv.Parcel]):
    """
    Store parcels in the database.
    """
    storage: common.AbstractParcelStorage
    if DATABASE == "postgresql":
        storage = postgresql.ParcelStorage()
    elif DATABASE == "minio":
        storage = minio.ParcelStorage()
    elif DATABASE == "mongodb":
        storage = mongodb.ParcelStorage()
    else:
        log.warning("No database selected. Skipping storage.")
        return

    log.info("Storing parcels")
    for parcel in parcels:
        log.debug("Storing parcel %s", parcel.id)
        storage.store_parcel(parcel)
    log.info("Closing DB connection")
    storage.close()


def display(parcels: list[csv.Parcel]):
    """
    Display parcels.
    """
    log.info("Displaying parcels")
    basic.display_parcels(parcels)


if __name__ == "__main__":
    main()
