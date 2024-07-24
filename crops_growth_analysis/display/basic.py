"""Basic matplotlib display functions for parcels"""

import datetime

import matplotlib.pyplot as plt
import numpy
import stackstac
import xarray
from matplotlib.axes import Axes

from crops_growth_analysis.extract.csv import Parcel

# Limit the number of parcels
PARCEL_LIMIT = 3

# Limit the number of time to display
TIME_LIMIT = 5


def display_parcels(parcels: list[Parcel]):
    """
    Display parcels
    For now, we just display the first parcel
    """
    # Process limits
    parcel_nb = min(PARCEL_LIMIT, len(parcels))
    time_nb = min(TIME_LIMIT, len(parcels[0].sentinel_items))

    # Init plot
    _, ax = plt.subplots(
        parcel_nb, time_nb, sharex="row", sharey="row", squeeze=False
    )

    # Display parcels
    for i in range(parcel_nb):
        display_parcel(parcels[i], ax[i, :])

    plt.show()


def display_parcel(parcel: Parcel, ax: list[Axes]):
    """
    Display parcel timeseries
    For now, we just display the first time
    """
    # Process limits
    time_nb = min(TIME_LIMIT, len(parcel.sentinel_items))

    # Display timeseries
    for i in range(time_nb):
        display_parcel_at_time(
            parcel, parcel.sentinel_items[i].datetime, ax[i]
        )


def display_parcel_at_time(parcel: Parcel, time: datetime.datetime, ax: Axes):
    """
    Display parcel indexes at provided time.
    For now, we just display NDVI.
    Ideally we would read from databases.
    For now, we just take the previously computed values.
    """
    # Get images arrays
    visual = get_visual(parcel, time)
    ndvi: xarray.DataArray = parcel.timeseries.sel(index_type="ndvi").sel(
        time=time.replace(tzinfo=None), method="nearest"
    )

    # Apply color function to every pixel
    ndvi_color_overlay = apply_color_function(ndvi)
    extent = [
        ndvi.coords["x"].min(),
        ndvi.coords["x"].max(),
        ndvi.coords["y"].min(),
        ndvi.coords["y"].max(),
    ]

    # Polygon
    x, y = parcel.polygon.exterior.xy

    # Plot
    ax.imshow(visual, interpolation="none", extent=extent)
    ax.imshow(ndvi_color_overlay, interpolation="none", extent=extent)
    ax.plot(x, y, color="blue", linewidth=2)


def get_visual(parcel: Parcel, time: datetime.datetime) -> numpy.array:
    """
    Get visual image for parcel at provided time
    Again, we use previously computed values for now.
    """

    # Loads bands
    visual_ds: xarray.DataArray = stackstac.stack(
        next(item for item in parcel.sentinel_items if item.datetime == time),
        assets=["B04", "B03", "B02"],
        bounds=parcel.polygon.bounds,
        epsg=2154,
    ).isel(time=0)

    # Create RGB image from xarray DataArray
    ratio = 0.0001
    return numpy.stack(
        [
            visual_ds.sel(band="B04").values * ratio,
            visual_ds.sel(band="B03").values * ratio,
            visual_ds.sel(band="B02").values * ratio,
            numpy.ones(visual_ds.sel(band="B02").shape),
        ],
        axis=-1,
    )


def apply_color_function(ndvi: xarray.DataArray) -> numpy.array:
    """
    Apply color function to NDVI
    This is basically a fancy way of applying a color map to the NDVI values
    """
    return numpy.stack(numpy.vectorize(ndvi_to_color)(ndvi.values), axis=-1)


def ndvi_to_color(ndvi_value: float) -> tuple[float, float, float, float]:
    """
    Convert NDVI value to color
    May use a gradiant for better display.
    We'll keep it like that for now.
    """
    opacity = 0.15
    if ndvi_value < 0.33:
        return (1, 0, 0, opacity)  # Red with 50% opacity
    elif ndvi_value < 0.66:
        return (1, 1, 0, opacity)  # Yellow with 50% opacity
    else:
        return (0, 1, 0, opacity)  # Green with 50% opacity
