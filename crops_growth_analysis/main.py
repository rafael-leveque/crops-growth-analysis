"""
Main script to run the crops growth analysis.
"""

import time

from crops_growth_analysis.extract import csv, sentinel
from crops_growth_analysis.logger import log
from crops_growth_analysis.process import external, manual

PARCEL_LIMIT = -1
ASSETS_LIMIT = -1


def main():
    """
    Main function to run the crops growth analysis.
    """
    # Start Timer
    log.info("--- Start Timer ---")
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

    log.info("Calculating NDVI and NDMI")
    for parcel in parcels:
        log.debug("Processing parcel %s", parcel.id)
        parcel.bands = manual.process_parcel(parcel)
        # parcel.bands = external.process_parcel(parcel).compute()
    log.info("--- End Timer ---")
    log.info(
        "--- DataArray Size: %s kb ---",
        round(sum([parcel.bands.nbytes for parcel in parcels]) / 1024, 2),
    )
    log.info("--- Execution time: %s seconds ---", time.time() - start_time)


if __name__ == "__main__":
    main()
