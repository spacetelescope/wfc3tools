import numpy as np

from wfc3tools import pstack, pstat
from wfc3tools.tests.helpers import BaseWFC3TOOLS


class TestPstack(BaseWFC3TOOLS):
    detector = "ir"

    def test_pstack_pstat(self):
        filename = "ibh719grq_ima.fits"
        self.get_input_file(filename, skip_ref=True)

        # MAST data can change over time, 1% agreement is good enough.
        rtol = 0.01

        # pstack
        x_data, y_data = pstack(filename, column=100, row=25, extname="sci", plot=False)

        # fmt: off
        x_truth = np.array([
            100.651947, 93.470573, 86.2892, 79.107826,
            71.926453, 64.745079, 57.563702, 50.382328,
            43.200954, 36.019581, 28.838205, 21.65683,
            14.475455, 7.29408, 0.112705, 0])
        pstack_y_truth = np.array([
            136.75660802, 151.46077054, 133.8688648, 108.50410805,
            109.17918583, 81.5139582, 90.26712192, 61.68512157,
            59.11241987, 39.01870227, 32.63157047, 16.07532735,
            33.69198196, 16.90631634, 13.54113704, 0])
        # fmt: on

        np.testing.assert_allclose(x_data, x_truth, rtol=rtol)
        np.testing.assert_allclose(y_data, pstack_y_truth, rtol=rtol)

        # pstat
        stat_ct = pstat(filename, col_slice=(100, 104), row_slice=(20, 25), units="counts", plot=False)

        # fmt: off
        pstat_y_truth = np.array([
            210.93391217, 210.3575491, 187.08969378, 181.75601219,
            151.43222828, 138.52899031, 116.67495111, 109.19263377,
            86.42073624, 80.97576756, 70.44724733, 53.37688116,
            33.1249918, 12.25499919, -4.88105808, 0.0])
        # fmt: on

        np.testing.assert_allclose(stat_ct[0], x_truth, rtol=rtol)
        np.testing.assert_allclose(stat_ct[1], pstat_y_truth, rtol=rtol)

        stat_rate = pstat(filename, col_slice=(100, 104), row_slice=(20, 25), units="rate", plot=False)

        # fmt: off
        rate = np.array([
            2.09567642, 2.25052166, 2.16817045, 2.29757309,
            2.10537601, 2.13960648, 2.02688408, 2.16728044,
            2.00043583, 2.2481041, 2.44284439, 2.46466732,
            2.28835583, 1.68012953, -43.30826569, 0.0])
        # fmt: on

        np.testing.assert_allclose(stat_rate[0], x_truth, rtol=rtol)
        np.testing.assert_allclose(stat_rate[1], rate, rtol=rtol)
