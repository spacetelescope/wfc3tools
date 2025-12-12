import os

import pytest
from astropy.io import fits
from astroquery.mast import Observations

from wfc3tools import sub2full


def download_test_data(filenames, local_path=os.curdir, cache=True):
    for f in filenames:
        Observations.download_file(f"mast:HST/product/{f}", cache=cache, local_path=local_path)


def test_sub2full(_jail):
    flt = "ibbso1fdq_flt.fits"
    spt = "ibbso1fdq_spt.fits"

    download_test_data([flt, spt])

    # default args
    coords = sub2full(flt, x=None, y=None, fullExtent=False)
    assert coords == [(3584, 1539)]

    # full extent
    coords = sub2full(flt, x=None, y=None, fullExtent=True)
    assert coords == [(3584, 4096, 1539, 2050)]

    # single coordinate
    coords = sub2full(flt, x=1, y=1)
    assert coords == [(3585, 1540)]

    # list of images
    flt2 = "ic5p02e2q_flt.fits"
    spt2 = "ic5p02e2q_spt.fits"
    download_test_data([flt2, spt2])
    coords = sub2full([flt, flt2])
    assert coords == [(3584, 1539), (1410, 1243)]

    # multiple coordinates should raise error
    with pytest.raises(ValueError, match="Must input integer value for x and y"):
        sub2full(flt, x=(1, 2), y=(1, 2))

    # bad filename should raise error
    with pytest.raises(ValueError, match="Please input a valid HST filename"):
        sub2full("test", x=(1, 2), y=(1, 2))

    # missing header keyword should raise an error
    with fits.open(spt, mode="update") as f:
        del f[0].header["SS_DTCTR"]
    with pytest.raises(KeyError, match="Required header keyword missing"):
        sub2full(flt)
