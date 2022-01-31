import matplotlib.pyplot as plt
import astropy.units as u
import numpy as np
import mapb


trange = ["2010-01-01", "2011-01-01"]

data = mapb.SpacecraftData(trange, spacecraft=["A", "B"])

data.plot_time_series("A")
data.plot_time_series("B")
data.plot_footprints()
data.plot_spirals()
data.plot_spirals(time="2010-02-01T01:00:00")
data.show()

