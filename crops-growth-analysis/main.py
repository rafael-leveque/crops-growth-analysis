from extraction import parcels
from extraction.planetarium import Planetarium

def main():
    # Read csv parcels
    maize_parcels = parcels.read_maize()
    tournesol_parcels = parcels.read_tournesol()

    # Display parcels
    # extraction.parcels.display_parcels("Maize", maize_parcels)
    # extraction.parcels.display_parcels("Tournesol", tournesol_parcels)
    # extraction.parcels.display_parcels("All", maize_data + tournesol_parcels)

    # Search planetarium data
    sample = maize_parcels[0]
    planetarium = Planetarium()
    i_s = planetarium.search_polygon(sample.polygon)
    # Print result length
    print(len(i_s.get_all_items()))
    # planetarium_sample = planetarium.search_polygon(sample.polygon).get_all_items()
    # p_item = planetarium_sample[0]
    # print(p_item)


if __name__ == "__main__":
    main()
