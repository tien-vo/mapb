""" Base procedures to load spacecraft data """

__all__ = ["BaseSpacecraftData"]


from .spiral import spiral_footprint
from cdasws import CdasWs
import astropy.constants as c
import astropy.units as u
import numpy as np


cdas = CdasWs()


class BaseSpacecraftData:

    def __init__(
        self, trange, spacecraft=["A"], downsample=1000, b=10 * c.R_sun
    ):
        self.trange = trange
        self.sc = spacecraft
        self.N = downsample
        self.b = b
        self.data = {}
        self.attrs = {}
        for sc in spacecraft:
            # Load spacecraft data
            data, attrs = self._load(sc)
            # Add Parker spiral footprints
            prf = f"st{sc.lower()}_"
            footprint = spiral_footprint(
                data[f"{prf}HEEQ"], data[f"{prf}Vp"], b=b
            )
            data.update({f"{prf}footprint": footprint["data"]})
            attrs.update({f"{prf}footprint": footprint["attrs"]})

            # Update into class attributes
            self.data.update(data)
            self.attrs.update(attrs)


    def _load(self, sc):

        # Unpack
        trange = self.trange
        N = self.N

        # Get cartesian HEEQ spacecraft position and proton bulk speed
        status, d = cdas.get_data(
            f"ST{sc}_L2_MAGPLASMA_1M",
            ["HEEQ", "BFIELDRTN", "Vp", "Vr_Over_V_RTN"],
            *trange,
            progressCallback=self._report,
            progressUserValue=sc
        )

        data, attrs = {}, {}
        if status["http"]["status_code"] == 200:
            # Filter & add physical units
            kw = dict(filt=True, unit=True, N=N)
            sc = sc.lower()
            # Process data
            data[f"st{sc}_epoch"] = self._process(d["Epoch"], N=N)
            data[f"st{sc}_HEEQ"] = self._process(d["HEEQ"], **kw)
            data[f"st{sc}_Vp"] = self._process(d["Vp"], **kw)
            data[f"st{sc}_B_RTN"] = self._process(d["BFIELDRTN"], **kw)
            data[f"st{sc}_rdircos"] = self._process(d["Vr_Over_V_RTN"], **kw)
            # Copy attributes
            attrs[f"st{sc}_epoch"] = d["Epoch"].attrs
            attrs[f"st{sc}_HEEQ"] = dict(
                d["HEEQ"].attrs, **dict(legends=d["metavar0"])
            )
            attrs[f"st{sc}_Vp"] = d["Vp"].attrs
            attrs[f"st{sc}_B_RTN"] = dict(
                d["BFIELDRTN"].attrs, **dict(legends=d["metavar1"])
            )
            attrs[f"st{sc}_rdircos"] = d["Vr_Over_V_RTN"].attrs
        else:
            print(f"STEREO {sc}: Failed retrieving data.")

        return data, attrs

    @staticmethod
    def _report(progress, message, sc):
        print(f"STEREO {sc} ({progress * 100:.0f}%): {message}")
        return 0

    @staticmethod
    def _process(data, filt=False, unit=False, N=None):
        """ Filter to nan values and add physical units """
        # Unpack
        attrs = data.attrs
        fillval = attrs["FILLVAL"]
        unit_ = attrs["UNITS"].replace("sec", "s")
        unit_ = "" if unit_ == "Na" else unit_
        # Filter
        if filt: data[data == fillval] = np.nan
        # Add unit
        if unit: data *= u.Unit(unit_)
        # Downsample to save memory
        if N is not None:
            Nt = max(data.shape)
            data = data[::Nt // N]
        return data

