import logging

from PIL import Image
import requests
from extraction import parcels
from extraction.planetarium import Sentinel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

PARCEL_LIMIT = 3


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
    sentinel = Sentinel()
    for parcel in maize_parcels:
        parcel.sentinel_data = sentinel.search_polygon(parcel.wgs64_polygon)

    # Get SCL image
    logging.info("Getting SCL image")
    for parcel in maize_parcels:
        for sentinel_data in parcel.sentinel_data:
            scl_url = sentinel_data.item.assets["SCL"].href
            raw_image = requests.get(scl_url, stream=True).raw
            sentinel_data.scl = Image.open(raw_image).convert("RGB")

    parcels_cnt = len(maize_parcels)
    logging.info(f"Parcels count: {parcels_cnt}")

    items_cnt = len(maize_parcels[0].sentinel_data)
    logging.info(f"Sentinel Items : {items_cnt}")

    assets_cnt = len(maize_parcels[0].sentinel_data[0].item.assets)
    logging.info(
        f"Asset per item: {maize_parcels[0].sentinel_data[0].item.assets.keys()}"
    )
    logging.info(f"Asset per item: {assets_cnt}")

    total_assets = parcels_cnt * items_cnt * assets_cnt
    logging.info(f"Total assets: {total_assets}")

    # logging.info(f"Last data: {last_data}")
    # for parcel in maize_parcels:

    #     for sentinel_data in parcel.sentinel_data:
    #         parcel.scl_image =
    # first_asset = maize_parcels[0].sentinel_data[0].assets["SCL"]
    # response = requests.get(first_asset.href, stream=True)
    # _ = Image.open(response.raw)
    # image = Image.open(requests.get(first_asset.href).raw)
    # image.show()
    # logging.info(f"Content: {response.content}")


if __name__ == "__main__":
    main()
