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
data.plot_time_series("A")
```
![Alt text](tests/sta_time_series.png?raw=true "Time series loaded from STA.")
