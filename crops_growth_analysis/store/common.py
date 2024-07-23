"""Abstract class for storing parcels."""

from abc import ABC, abstractmethod
from io import BytesIO

from crops_growth_analysis.extract.csv import Parcel
from crops_growth_analysis.logger import log


class AbstractParcelStorage(ABC):
    """
    An abstract class for storing parcels.
    """

    def store_parcel(self, parcel):
        """
        Store the parcel.
        """
        # Store parcel information
        log.debug("Storing parcel information")
        self.store_parcel_info(parcel)
        # Store bands information
        log.debug("Storing bands information")
        for band_ds in parcel.bands:
            for time_ds in band_ds:
                current_band = time_ds["band"].item()
                current_time = time_ds["time"].item()
                log.debug(
                    "Storing band %s and time %s",
                    current_band,
                    current_time,
                )
                netcdf_buffer = BytesIO()
                time_ds.to_netcdf(netcdf_buffer)
                self.store_band(
                    parcel.id,
                    current_band,
                    current_time,
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
    def store_band(
        self,
        parcel_id: str,
        band: str,
        time: str,
        data: bytes = None,
        url: str = None,
    ):
        """
        Store the band information.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Close the connection.
        """
        raise NotImplementedError
