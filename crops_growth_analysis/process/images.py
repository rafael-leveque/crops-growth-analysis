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
        self.parcel: Polygon = parcel

    def load(
        self,
        band: str,
        interp_like: xarray.DataArray = None,
        mask: bool = False,
    ) -> xarray.DataArray:
        """
        Get image from sentinel data
        If interp_like is provided, the image will be interpolated to match the
        resolution of interp_like
        If mask is True, the image will be masked with the parcel polygon
        """
        url = self.item.assets[band].href
        log.debug("Loading and Reading image")
        src: rasterio.DatasetReader
        with rasterio.open(url) as src:
            # log.debug("Reading image")
            proj_parcel = self.project_polygon(self.parcel)
            window = (
                src.window(*proj_parcel.bounds).round_lengths().round_offsets()
            )
            image_array = src.read(1, window=window)
            bounds = self.project_bounds(src.window_bounds(window))
            new_coords = {
                "y": numpy.linspace(bounds[3], bounds[1], window.height),
                "x": numpy.linspace(bounds[0], bounds[2], window.width),
            }
            data_array = xarray.DataArray(
                image_array,
                dims=["y", "x"],
                coords=new_coords,
                name=band,
            )
            if interp_like is not None:
                data_array = data_array.interp_like(
                    interp_like, method="nearest"
                )
            if mask:
                data_array = self.mask(data_array)
        return data_array

    def project_polygon(self, parcel: Polygon) -> Polygon:
        """Project parcel to image CRS"""
        return shapely.ops.transform(
            Transformer.from_crs(
                CRS("EPSG:2154"),
                CRS(f"EPSG:{self.item.properties['proj:epsg']}"),
                always_xy=True,
            ).transform,
            parcel,
        )

    def project_bounds(
        self, bounds: tuple[float, float, float, float]
    ) -> tuple[float, float, float, float]:
        """Project image CRS bounds to parcel CRS"""
        transformer = Transformer.from_crs(
            CRS(f"EPSG:{self.item.properties['proj:epsg']}"),
            CRS("EPSG:2154"),
            always_xy=True,
        )
        return transformer.transform_bounds(*bounds)

    def mask(self, bands: xarray.DataArray) -> xarray.DataArray:
        """Mask bands with parcel"""
        mask = xarray.apply_ufunc(
            numpy.vectorize(lambda x, y: self.parcel.contains(Point(x, y))),
            bands["x"],
            bands["y"],
            vectorize=True,
        )
        return bands.where(mask)
