__all__ = ["spiral_footprint", "reconstruct_footprint"]


from astropy.coordinates import cartesian_to_spherical
import astropy.constants as c
import astropy.units as u
import numpy as np


T_sun = 27.2752612 * u.day
w_sun = ((2 * np.pi * u.rad) / T_sun).to(u.Unit("rad/s"))


def spiral_footprint(cartesian_HEEQ, Vr, b=10 * c.R_sun):
    # Convert to spherical coordinates (math sph not physics sph)
    r, theta, phi = cartesian_to_spherical(*cartesian_HEEQ.T)
    # Normalize
    rb = (r / b).decompose()
    C = (Vr / (w_sun * b * np.cos(theta))).decompose()
    # Calculate azimuthal angle at footprint
    phib = phi + (1 / C) * (rb - 1 - np.log(rb))
    # Save into data structures
    footprint = dict(
        data=np.array([theta.to(u.deg), phib.to(u.deg)]).T * u.deg,
        attrs=dict(FIELDNAM="Spiral footprint", UNITS="deg",
                   legends=["lat(HEEQ)", "lon(HEEQ)"]))
    return footprint


def reconstruct_footprint(r, footprint, Vr, b=10 * c.R_sun):
    # Unpack
    thetab, phib = footprint
    # Normalize
    rb = (r / b).decompose()
    C = (Vr / (w_sun * b * np.cos(thetab))).decompose()
    # Calculate azimuthal angle at footprint
    phi = phib - (1 / C) * (rb - 1 - np.log(rb))
    return phi
