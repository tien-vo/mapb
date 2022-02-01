# mapb

## Introduction
This is a package for mapping the interplanetary magnetic field (IMF) from a
spacecraft to the solar surface through the Parker spiral geometry.

Supported spacecrafts: STEREO

## Installation

Dependencies: `numpy, matplotlib, datetime, spacepy, cdasws`. It's best to
install through an Anaconda environment, with recommended python version 3.9.
Example to create a conda environment:
```
conda create -n mapb python=3.9
```
Then run
```
python setup.py install
```

## Usage

A demonstrative example is given in `tests/demo.py`. First, import the package
and create an instance of `SpacecraftData` using a time range `trange` and
specifying the spacecrafts from which to load data (`"A"` for STEREO A, `"B"` 
for STEREO B, or both).
```
import mapb

trange = ["2010-01-01", "2011-01-01"]
data = mapb.SpacecraftData(trange, spacecraft=["A", "B"])
```

Then, we can plot the time series loaded from CDAWeb for each spacecraft.
Specify `save=True` if you wish to save figure into png files.
```
data.plot_time_series("A", save=True)
```
![Alt text](tests/sta_time_series.png?raw=true "Time series loaded from STA.")

(a) The first panel shows 3 components of the spacecraft position in
Cartesian Heliocentric coordinates. (b) The second panel shows the proton bulk
speed. (c) The third panel shows the magnetic field in RTN coordinates. (d) The
fourth panel shows the radial direction cosine of the velocity. (e) The last
panel shows the coordinates of the calculated spiral footprints on the solar
surface (traced back to 10 R_sun). (a) and (b) are necessary for the computation
of (e). (c) is to check that the magnetic field follows the spiral geometry at
the location of the spacecraft (not shown). (d) is to check the validity of the
spiral calculations (the assumption is that the velocity is mostly radial).

Similarly, for STEREO B,
```
data.plot_time_series("B", save=True)
```
![Alt text](tests/stb_time_series.png?raw=true "Time series loaded from STB.")

We can also plot the footprints on an inertial longitude vs. latitude (HEEQ) 
coordinates. Potentially, this can be combined with EUVI images (will be
implemented).
```
data.plot_footprints(save=True)
```
![Alt text](tests/footprints.png?raw=true "Parker spiral footprints.")

Also, we can plot the spiral at a given time in the xy plane (default to the
starting point in the time range if not specified).
```
data.plot_spirals(save=True)
```
![Alt text]('tests/spirals_2010-01-01 05:00:00.png'?raw=true "Spirals1.")

Or, if specified, the string has to be in %Y-%m-%dT%H:%M:%S format.
```
data.plot_spirals(time="2010-02-01T01:00:00", save=True)
```
![Alt text]('tests/spirals_2010-01-31 23:35:00.png'?raw=true "Spirals2.")

Finally, the function
```
data.show()
```
shows the created plots if using the package interactively.
