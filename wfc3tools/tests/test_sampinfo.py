import re

from wfc3tools import sampinfo
from wfc3tools.tests.helpers import BaseWFC3TOOLS


def normalize(r):
    """
    Strip white space and tabs from output, replace with all single spaces,
    split into a list by newlines.
    """
    return [re.sub(r"\s+", " ", s.strip()) for s in r.split("\n")]


class TestSampInfo(BaseWFC3TOOLS):
    detector = "ir"

    def test_sampinfo(self, capsys):
        filename = "ibcf02faq_raw.fits"
        self.get_input_file(filename, skip_ref=True)

        capsys.readouterr()  # clear buffer

        # expected header for all calls to sampinfo, for this dataset
        h1 = "IMAGE NEXTEND SAMP_SEQ NSAMP EXPTIME"
        h2 = "ibcf02faq_raw.fits 80 STEP50 16 499.234009"
        h3 = "IMSET SAMPNUM SAMPTIME DELTATIM"

        sampinfo(filename)
        c = normalize(capsys.readouterr().out)
        assert h2 in c
        assert h3 in c
        assert "1 15 499.234009 50.000412" in c
        capsys.readouterr()  # clear buffer

        # include median
        sampinfo(filename, median=True)
        c = normalize(capsys.readouterr().out)
        assert h1 in c
        assert h2 in c
        assert h3 in c
        assert "1 15 499.234009 50.000412 MedPixel: 11384.0" in c
        capsys.readouterr()  # clear buffer

        # include mean
        sampinfo(filename, mean=True)
        c = normalize(capsys.readouterr().out)
        assert h1 in c
        assert h2 in c
        assert "IMSET SAMPNUM SAMPTIME DELTATIM DATAMIN DATAMAX" in c
        assert "1 15 499.234009 50.000412 0.0 57019.0 AvgPixel: 28509.5" in c
        capsys.readouterr()  # clear buffer

        # test image list (same image twice)
        sampinfo([filename, filename])
        c = normalize(capsys.readouterr().out)
        assert c.count(h1) == 2
        assert c.count(h2) == 2
        assert c.count(h3) == 2
        assert c.count("1 15 499.234009 50.000412") == 2
