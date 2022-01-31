from ..get_data import load_data
from ..spiral import ParkerSpiral
from astropy.coordinates import SkyCoord, PhysicsSphericalRepresentation
from sunpy.coordinates import HeliographicStonyhurst as HEEQ
import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np


def test():

    trange = ["2010-01-01", "2010-02-01"]

    STA = load_data(trange, sc="STA", Nt=1000)
    coord_STA = SkyCoord(
        *STA["HEEQ"].T, obstime=STA["Epoch"], frame=HEEQ,
        representation_type="cartesian",
    )
    coord_STA.representation_type = "physicsspherical"
    ps_A = ParkerSpiral(
        coord_STA.r, coord_STA.theta, coord_STA.phi, STA["Vp"]
    )
    xA, yA = ps_A.get_footprint()

    STB = load_data(trange, sc="STB", Nt=1000)
    coord_STB = SkyCoord(
        *STB["HEEQ"].T, obstime=STB["Epoch"], frame=HEEQ,
        representation_type="cartesian",
    )
    coord_STB.representation_type = "physicsspherical"
    ps_B = ParkerSpiral(
        coord_STB.r, coord_STB.theta, coord_STB.phi, STB["Vp"]
    )
    xB, yB = ps_B.get_footprint()

    fig, ax = plt.subplots(1, 1)

    ax.plot(yA.value, xA.value, "-k")
    ax.plot(yB.value, xB.value, "-r")

    ax.set_aspect("equal")
    ax.set_ylim(80, 100)

    plt.show()

    #ps = ParkerSpiral(
    #    1 * u.au, np.pi / 2 * u.rad, np.pi / 4 * u.rad, 750 * u.km / u.s
    #)

    #r = np.linspace(ps.b, 1.1 * u.au, 1000)
    #p = ps.calculate_p(r)

    #x = r * np.cos(p)
    #y = r * np.sin(p)

    #fig, ax = plt.subplots(1, 1)
    #ax.plot(x, y, "-k")
    #ax.set_aspect("equal")
    #ax.set_xlim(-1.2, 1.2)
    #ax.set_ylim(-1.2, 1.2)
    #plt.show()

