"""
Main script to run the crops growth analysis.
"""

import time

from crops_growth_analysis.extract import parcels, sentinel
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
    log.info("--- Prepare Data ---")

    log.info(
        "Reading CSV %s",
        "" if PARCEL_LIMIT > 0 else f"(Limited to {PARCEL_LIMIT})",
    )
    maize_parcels = parcels.read_maize()[:PARCEL_LIMIT]

    # log.info("Reading tournesol parcels")
    # tournesol_parcels = parcels.read_tournesol()
    # log.info(f"Tournesol parcels: {len(tournesol_parcels)}")

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    log.info("Searching planetarium data")
    for parcel in maize_parcels:
        parcel.sentinel_items = sentinel.search_polygon(parcel.polygon)[
            :ASSETS_LIMIT
        ]

    log.info("Calculating NDVI and NDMI")
    for parcel in maize_parcels:
        log.info("Processing parcel %s", parcel.id)
        # parcel.bands = manual.process_parcel(parcel)
        parcel.bands = external.process_parcel(parcel).compute()
    log.info(maize_parcels[0].bands.isel(time=0).isel(band=0))
    log.info("--- End Timer ---")
    log.info("--- Execution time: %s seconds ---", time.time() - start_time)


if __name__ == "__main__":
    main()
