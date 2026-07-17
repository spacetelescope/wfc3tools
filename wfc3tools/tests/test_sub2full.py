import pytest
from astropy.io import fits

from wfc3tools import sub2full
from wfc3tools.tests.helpers import BaseWFC3TOOLS


class TestSub2full(BaseWFC3TOOLS):
    detector = "uvis"

    def test_sub2full(self):
        rootname = "ibbso1fdq"
        flt = f"{rootname}_flt.fits"
        spt = f"{rootname}_spt.fits"
        self.get_input_file(flt, skip_ref=True)
        self.get_input_file(spt, skip_ref=True)

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
        rootname2 = "ic5p02e2q"
        flt2 = f"{rootname2}_flt.fits"
        spt2 = f"{rootname2}_spt.fits"
        self.get_input_file(flt2, skip_ref=True)
        self.get_input_file(spt2, skip_ref=True)

        coords = sub2full([flt, flt2])
        assert coords == [(3584, 1539), (1410, 1243)]

        # multiple coordinates should raise error
        with pytest.raises(ValueError, match="Must input integer value for x and y"):
            sub2full(flt, x=(1, 2), y=(1, 2))

        # missing header keyword should raise an error
        with fits.open(spt, mode="update") as f:
            del f[0].header["SS_DTCTR"]
        with pytest.raises(KeyError, match="Required header keyword missing"):
            sub2full(flt)


def test_sub2full_bad_file():
    """Bad filename should raise error."""
    with pytest.raises(ValueError, match="Please input a valid HST filename"):
        sub2full("test", x=(1, 2), y=(1, 2))
