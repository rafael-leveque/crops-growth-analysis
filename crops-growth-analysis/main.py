from extraction import data
from extraction.planetarium import Planetarium

def main():
    # Read csv data
    maize_fields = data.read_maize_fields()
    tournesol_fields = data.read_tournesol_fields()

    # Display data
    # extraction.data.display_data("Maize", maize_data)
    # extraction.data.display_data("Tournesol", tournesol_data)
    # extraction.data.display_data("All", maize_data + tournesol_data)

    # Search planetarium data
    planetarium = Planetarium()
    sample = maize_fields[0]
    planetarium_sample = planetarium.search_polygon(sample.polygon).get_all_items()
    p_item = planetarium_sample[0]
    print(p_item)


if __name__ == "__main__":
    main()
