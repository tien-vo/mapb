__all__ = ["ParkerSpiral"]


import astropy.constants as c
import astropy.units as u
import numpy as np


T_sun = 27.2752612 * u.day
w_sun = ((2 * np.pi * u.rad) / T_sun).to(u.Unit("rad/s"))


class ParkerSpiral:

    def __init__(self, r0, theta0, phi0, Vr, b=10 * c.R_sun):

        self.b = b
        self.theta0 = theta0
        # Calculate footprint
        rb = (r0 / b).decompose()
        self.C = (Vr / (w_sun * b * np.sin(theta0))).decompose()
        self.phib = phi0 + (1 / self.C) * (rb - 1 - np.log(rb))

    def calculate_p(self, r):
        # Unpack & normalize
        C = self.C
        r_ = (r / self.b).decompose()
        return self.phib - (1 / C) * (r_ - 1 - np.log(r_))

    def get_footprint(self):
        return self.theta0.to(u.deg), self.phib.to(u.deg)

