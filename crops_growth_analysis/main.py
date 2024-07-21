"""
Main script to run the crops growth analysis.
"""

from crops_growth_analysis.extract import parcels, sentinel
from crops_growth_analysis.logger import log
from crops_growth_analysis.process import tasks

PARCEL_LIMIT = 1
ASSETS_LIMIT = 2


def main():
    """
    Main function to run the crops growth analysis.
    """
    # Read csv parcels
    log.info("--- Prepare Data ---")

    log.info("Reading CSV (Limited to %s parcels)", PARCEL_LIMIT)
    maize_parcels = parcels.read_maize()[:PARCEL_LIMIT]

    # log.info("Reading tournesol parcels")
    # tournesol_parcels = parcels.read_tournesol()
    # log.info(f"Tournesol parcels: {len(tournesol_parcels)}")

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    # Search planetarium data
    log.info("Searching planetarium data")
    for parcel in maize_parcels:
        parcel.sentinel_data = sentinel.search_polygon(parcel.wgs64_polygon)[
            :ASSETS_LIMIT
        ]

    # Get SCL image
    log.info("Calculating NDVI and NDMI")
    for parcel in maize_parcels:
        log.info("Processing parcel %s", parcel.id)
        parcel.ndvi = []
        for sentinel_data in parcel.sentinel_data:
            log.info("Loading SCL")
            scl = tasks.get_scl(sentinel_data)
            log.info("Loading NIR")
            nir = tasks.get_nir(sentinel_data, scl)
            del scl
            log.info("Calculating NDVI")
            ndvi = tasks.get_ndvi(sentinel_data, nir)
            log.info("Calculating NDMI")
            ndmi = tasks.get_ndmi(sentinel_data, nir)
            del nir
            log.info("Saving NDVI and NDMI")
            parcel.ndvi.append(ndvi)
            parcel.ndmi.append(ndmi)
            del ndvi, ndmi
    log.info("Done")


if __name__ == "__main__":
    main()
