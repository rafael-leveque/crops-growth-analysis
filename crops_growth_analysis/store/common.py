"""Abstract class for storing parcels."""

from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO

from xarray import DataArray

from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log


class AbstractParcelStorage(ABC):
    """
    An abstract class to interact with database to store parcels timeseries.
    """

    def store_parcel(self, parcel: Parcel):
        """
        Store the parcel.
        """
        # Store parcel information
        log.debug("Storing parcel information")
        self.store_parcel_info(parcel)
        # Store timeseries
        log.debug("Storing timeseries")
        timeserie: DataArray
        ds: DataArray
        for timeserie in parcel.timeseries:
            for ds in timeserie:
                index_type: str = ds["index_type"].item()
                time: datetime = ds["time"].item()
                log.debug(
                    "Storing index type %s and time %s",
                    index_type,
                    time,
                )
                netcdf_buffer = BytesIO()
                ds.to_netcdf(netcdf_buffer)
                self.store_ds(
                    parcel.id,
                    index_type,
                    time,
                    netcdf_buffer.getvalue(),
                )
        log.debug("Parcel stored")

    @abstractmethod
    def store_parcel_info(self, parcel: Parcel):
        """
        Store the parcel information.
        """
        raise NotImplementedError

    @abstractmethod
    def store_ds(
        self,
        parcel_id: str,
        index_type: str,
        time: datetime,
        data: bytes = None,
        url: str = None,
    ):
        """
        Store a single timeserie dataset.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Close the connection.
        """
        raise NotImplementedError
