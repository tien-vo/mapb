#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="mapb",
    version="0.0.1",
    description="Python code for mapping the magnetic field to the Sun.",
    url="https://github.com/tien-vo/mapb.git",
    packages=find_packages(),
    python_requires=">=3.7,<3.10",
    install_requires=[
        "sunpy[all]",
        "astropy",
        "matplotlib",
        "plasmapy",
        "numpy",
        "pyspedas",
        "mpl_extras @ https://github.com/tien-vo/mpl_extras/archive/main.zip"
    ],
)

