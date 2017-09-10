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
You can provide any combination of these mangitudes
*  -T TMAG, --Tmag TMAG  TESS magnitude of the source
*  -J JMAG, --Jmag JMAG  J magnitude of the source
*  -K KSMAG, --Ksmag KSMAG Ks magnitude of the source
*  -V VMAG, --Vmag VMAG  V magnitude of the source
*  -G GMAG, --Gmag GMAG  Gaia magnitude of the source
*  -H HMAG, --Hmag HMAG  H magnitude of the source
*  -B BMAG, --Bmag BMAG  B magnitude of the source
*  --Bphmag BPHMAG       B photgraphic magnitude of the source

You can also specify the integration time in minutes. This will be used to calculate the noise. This assumes noise scales with the inverse square-root of the integration time. (default: 60)
*  -i INTEGRATION, --integration INTEGRATION

```
ticgen --Tmag 18.0 --integration 1440

TESS mag = 18.00, calculated using Tmag was provided.
1-sigma scatter in 1440 min = 51045 ppm.
```

You can also run on a csvfile with magnitudes.
The header of the file must contain one or more of 
Tmag, Vmag, Jmag, Bmag, Bphmag, Ksmag, Hmag, and Gmag. Not all the magnitues need to be included in the file and the columns can be in any order.

A new csv file will be created with two columns: TESS mag and 1-sigma noise level in parts-per-million.

Here is an example of an acceptable file
```
Tmag,Vmag,Jmag,Bmag,Bphmag,Ksmag,Hmag,Gmag
12.0,,,,,,,
,11.5,8.1,,,6.7,,
,,,,,,16.0,
,,12.0,12.0,,8.6,,
```

and this would output
```
# Tmag, 1-sigma noise (ppm)
    12.000,    595.007
     9.850,    188.867
    16.700,  32331.695
    12.872,   1030.614
```




                 


