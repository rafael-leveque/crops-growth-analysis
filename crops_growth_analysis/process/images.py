"""
Module to load images from Sentinel-2 data
"""

import numpy
import rasterio
import rasterio.mask
import shapely.ops
import xarray
from PIL import Image
from pyproj import CRS, Transformer
from pystac import Item
from shapely.geometry import Point, Polygon

from crops_growth_analysis.logger import log

Image.MAX_IMAGE_PIXELS = None


class ItemImages:
    """Class to load images from a Sentinel-2 item"""

    def __init__(self, item: Item, parcel: Polygon):
        self.item: Item = item
        self.parcel: Polygon = self.get_proj_polygon(parcel)

    def get_proj_polygon(self, parcel: Polygon) -> Polygon:
        """Take coordinates bounds and turn it into xy bounds"""
        # Put the bounds (EPSG:2154) in the item coordinate system
        log.debug("Getting bounds")
        item_epsg = f"EPSG:{self.item.properties['proj:epsg']}"
        return shapely.ops.transform(
            Transformer.from_crs(
                CRS("EPSG:2154"), CRS(item_epsg), always_xy=True
            ).transform,
            parcel,
        )

    def load(self, band: str) -> xarray.DataArray:
        """Get image from sentinel data"""
        url = self.item.assets[band].href
        log.debug("Loading and Reading image")
        src: rasterio.DatasetReader
        with rasterio.open(url) as src:
            # log.debug("Reading image")
            window = (
                src.window(*self.parcel.bounds).round_lengths().round_offsets()
            )
            image_array = src.read(
                1,
                window=window,
                out_shape=(
                    int(window.height * src.res[0] / 10),
                    int(window.width * src.res[1] / 10),
                ),
            )
            bounds = src.window_bounds(window)
            new_coords = {
                "x": numpy.arange(
                    bounds[0], bounds[0] + 10 * image_array.shape[1], 10
                ),
                "y": numpy.arange(
                    bounds[3], bounds[3] - 10 * image_array.shape[0], -10
                ),
            }
            data_array = xarray.DataArray(
                image_array,
                dims=["y", "x"],
                coords=new_coords,
                name=band,
            )
            data_array = self.mask(data_array)
        return data_array

    def mask(self, bands: xarray.DataArray) -> xarray.DataArray:
        """Mask bands with parcel"""
        mask = xarray.apply_ufunc(
            numpy.vectorize(lambda x, y: self.parcel.contains(Point(x, y))),
            bands["x"],
            bands["y"],
            vectorize=True,
        )
        return bands.where(mask)
