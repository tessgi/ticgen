# ticgen

A tool for calculating a TESS magnitude, and an expected noise level for stars to be observed by TESS.


[![Build Status](https://travis-ci.org/tessgi/ticgen.svg?branch=master)](https://travis-ci.org/tessgi/ticgen)
[![PyPI](http://img.shields.io/pypi/v/tvguide.svg)](https://pypi.python.org/pypi/ticgen/)
<!-- [![DOI](https://zenodo.org/badge/94136696.svg)](https://zenodo.org/badge/latestdoi/94136696) -->

## Installation
You can install using pip
``` bash
$ pip install ticgen --upgrade
```

or via the github repository
``` bash
$ git clone https://github.com/tessgi/ticgen.git
$ cd tvguide
$ python setup.py install
```

The code has been tested in Python 2.7, 3.5, and 3.6.


## Usage
Provide some magnitudes and we'll calculate a TESS magnitude and a noise level
```
$ ticgen -V 7.5 -J 12.0 -Ks 11.5

TESS mag = 10.09, calculated using V/J/Ks.
1-sigma scatter in 60 min = 212 ppm.
```
