"""
Main script to run the crops growth analysis.
"""

import time

from crops_growth_analysis.extract import csv, sentinel
from crops_growth_analysis.logger import log
# from crops_growth_analysis.process import manual
from crops_growth_analysis.process import external
# from crops_growth_analysis.store import minio
# from crops_growth_analysis.store import mongodb
from crops_growth_analysis.store import postgresql
from crops_growth_analysis.display import basic

PARCEL_LIMIT = -1
ASSETS_LIMIT = -1


def main():
    """
    Main function to run the crops growth analysis.
    """
    # Start Timer
    overall_start_time = time.time()

    log.info("--- Start Extract ---")
    start_time = time.time()

    # Read csv parcels
    log.info(
        "Reading CSV %s",
        "" if PARCEL_LIMIT < 0 else f"(Limited to {PARCEL_LIMIT} parcels)",
    )
    parcels = (csv.read_maize() + csv.read_tournesol())[:PARCEL_LIMIT]

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    log.info(
        "Searching planetarium data %s",
        "" if ASSETS_LIMIT < 0 else f"(Limited to {ASSETS_LIMIT} assets)",
    )
    for parcel in parcels:
        parcel.sentinel_items = sentinel.search_polygon(parcel.polygon)[
            :ASSETS_LIMIT
        ]

    extract_time = time.time() - start_time
    log.info("--- Extract Time : %s ---", extract_time)
    log.info("--- Start Process ---")
    start_time = time.time()

    log.info("Calculating NDVI and NDMI")
    for parcel in parcels:
        log.debug("Processing parcel %s", parcel.id)
        # parcel.bands = manual.process_parcel(parcel)
        parcel.bands = external.process_parcel(parcel).compute()

    process_time = time.time() - start_time
    log.info("--- Process Time : %s ---", process_time)
    log.info(
        "--- DataArray Size: %s kb ---",
        round(sum([parcel.bands.nbytes for parcel in parcels]) / 1024, 2),
    )
    log.info("--- Start Store ---")
    start_time = time.time()

    log.info("Starting DB connection")
    storage = postgresql.ParcelStorage()
    # storage = minio.ParcelStorage()
    # storage = mongodb.ParcelStorage()
    log.info("Storing parcels")
    for parcel in parcels:
        log.debug("Storing parcel %s", parcel.id)
        storage.store_parcel(parcel)
    log.info("Closing DB connection")
    storage.close()

    store_time = time.time() - start_time
    log.info("--- Store Time : %s ---", store_time)

    log.info("--- Start Display ---")
    start_time = time.time()

    log.info("Displaying parcels")
    first_parcel = parcels[0]
    basic.plot_parcel(first_parcel, first_parcel.sentinel_items[0].datetime)

    display_time = time.time() - start_time
    log.info("--- Display Time : %s ---", display_time)

    overall_time = time.time() - overall_start_time
    log.info("--- Summary ---")
    log.info("--- Extract Time : %s ---", extract_time)
    log.info("--- Process Time : %s ---", process_time)
    log.info("--- Store Time : %s ---", store_time)
    log.info("--- Display Time : %s ---", display_time)
    log.info("--- Overall Time : %s ---", overall_time)


if __name__ == "__main__":
    main()
