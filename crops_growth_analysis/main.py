"""
Main script to run the crops growth analysis.
"""

from extraction import parcels, sentinel
from logger import log
from processing import calculus, images

PARCEL_LIMIT = 1


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
        parcel.sentinel_data = sentinel.search_polygon(parcel.wgs64_polygon)

    # Get SCL image
    log.info("Calculating NDVI and NDMI")
    for parcel in maize_parcels:
        log.info(f"Processing parcel {parcel.id}")
        parcel.ndvi = []
        for sentinel_data in parcel.sentinel_data:
            log.info("Loading images")
            bands_da = images.get_bands(sentinel_data)
            log.info("Formatting as dataset")
            bands_ds = calculus.format_as_dataset(bands_da)
            log.info("Calculating NDVI and NDMI")
            result = calculus.ndvi_and_ndmi(bands_ds)
            parcel.ndvi.append(result)


if __name__ == "__main__":
    main()
