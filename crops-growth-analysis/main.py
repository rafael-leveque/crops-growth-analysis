import extraction
import extraction.data

def main():
    maize_data = extraction.data.read_maize_data()
    extraction.data.display_data("Maize", maize_data)

    tournesol_data = extraction.data.read_tournesol_data()
    extraction.data.display_data("Tournesol", tournesol_data)

    extraction.data.display_data("All", maize_data + tournesol_data)

if __name__ == "__main__":
    main()
