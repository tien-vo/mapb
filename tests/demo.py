import mapb

trange = ["2010-01-01", "2011-01-01"]
data = mapb.SpacecraftData(trange, spacecraft=["A", "B"])

data.plot_time_series("A", save=True)
data.plot_time_series("B", save=True)
data.plot_footprints(save=True)
data.plot_spirals(save=True)
data.plot_spirals(time="2010-02-01T01:00:00", save=True)
data.show()

