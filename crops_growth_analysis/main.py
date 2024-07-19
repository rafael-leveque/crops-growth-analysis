import logging

from extraction import parcels, sentinel
from processing import calculus, images

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

PARCEL_LIMIT = 1


def main():
    # Read csv parcels
    logging.info("--- Prepare Data ---")

    logging.info(f"Reading CSV (Limited to {PARCEL_LIMIT} parcels)")
    maize_parcels = parcels.read_maize()[:PARCEL_LIMIT]

    # logging.info("Reading tournesol parcels")
    # tournesol_parcels = parcels.read_tournesol()
    # logging.info(f"Tournesol parcels: {len(tournesol_parcels)}")

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    # Search planetarium data
    logging.info("Searching planetarium data")
    client = sentinel.SentinelClient()
    for parcel in maize_parcels:
        parcel.sentinel_data = client.search_polygon(parcel.wgs64_polygon)

    # Get SCL image
    logging.info("Getting SCL image")
    for parcel in maize_parcels:
        parcel.ndvi = []
        for sentinel_data in parcel.sentinel_data:
            dataset = images.get_bands_datasets(sentinel_data)
            ndvi = calculus.ndvi(dataset)
            parcel.ndvi.append(ndvi)


if __name__ == "__main__":
    main()
