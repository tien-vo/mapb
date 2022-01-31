__all__ = ["load_data"]


from astropy.coordinates import cartesian_to_spherical
from cdasws import CdasWs
import astropy.units as u
import numpy as np


_vars_get = ["HEEQ", "Vp"]
cdas = CdasWs()


def load_data(trange, sc="STA", Nt=None):

    print(f"Loading {sc} data...", end=" ")
    name = f"{sc}_L2_MAGPLASMA_1M"
    # Load data
    data = cdas.get_data(name, _vars_get, *trange)[1]

    for var in _vars_get:
        fillval = data[var].attrs["FILLVAL"]
        data[var][data[var] == fillval] = np.nan
        data[var] *= u.Unit(data[var].attrs["UNITS"].replace("sec", "s"))

    N = len(data["Epoch"])
    if Nt is not None:
        for var in _vars_get + ["Epoch"]:
            data[var] = data[var][::N // Nt]

        data["Nt"] = Nt
    else:
        data["Nt"] = N

    # Convert HEEQ to spherical coordinates
    x = data["HEEQ"][:, 0]
    y = data["HEEQ"][:, 0]
    x = data["HEEQ"][:, 0]

    print("Done!")
    return data

