import logging

from PIL import Image
import requests
from extraction import parcels
from extraction.planetarium import Planetarium

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    # Read csv parcels
    logging.info("Reading parcels")
    maize_parcels = parcels.read_maize()[:5]
    logging.info(f"Maize parcels: {len(maize_parcels)}")

    # logging.info("Reading tournesol parcels")
    # tournesol_parcels = parcels.read_tournesol()
    # logging.info(f"Tournesol parcels: {len(tournesol_parcels)}")

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    # Search planetarium data
    logging.info("Init planetarium search")
    planetarium = Planetarium()
    logging.info("Searching planetarium data")
    for parcel in maize_parcels:
        parcel.sentinel_data = planetarium.search_polygon(
            parcel.wgs64_polygon
        ).item_collection()
    logging.info("Planetarium data search done")

    maize_s_data_cnt = [len(parcel.sentinel_data) for parcel in maize_parcels]
    logging.info(
        f"Maize parcels sentinel data max is {max(maize_s_data_cnt)} and min is {min(maize_s_data_cnt)}"
    )

    first_asset = maize_parcels[0].sentinel_data[0].assets["SCL"]
    response = requests.get(first_asset.href, stream=True)
    image = Image.open(response.raw)
    # image = Image.open(requests.get(first_asset.href).raw)
    # image.show()
    # logging.info(f"Content: {response.content}")

    # logging.info(f"Properties: {maize_parcels[0].sentinel_data[0].properties.keys()}")
    # logging.info(f"Properties: {maize_parcels[0].sentinel_data[0].assets.keys()}")


if __name__ == "__main__":
    main()
