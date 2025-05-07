import os

from astroquery.mast import Observations
import numpy as np

from wfc3tools import pstat


def test_pstat(tmpdir):

    os.chdir(tmpdir)

    filename = 'ibh719grq_ima.fits'
    Observations.download_file(f'mast:HST/product/{filename}', cache=True)

    truth = (np.array([100.651947, 93.470573, 86.2892, 79.107826, 71.926453,
                       64.745079, 57.563702, 50.382328, 43.200954, 36.019581,
                       28.838205, 21.65683, 14.475455, 7.29408, 0.112705, 0.]),
             np.array([210.93391217, 210.3575491, 187.08969378, 181.75601219,
                       151.43222828, 138.52899031, 116.67495111, 109.19263377,
                       86.42073624, 80.97576756, 70.44724733, 53.37688116,
                       33.1249918, 12.25499919, -4.88105808, 0.]))

    stat = pstat(filename, col_slice=(100, 104), row_slice=(20, 25),
                 units="counts", plot=False)
    np.testing.assert_allclose(stat[0], truth[0])
    np.testing.assert_allclose(stat[1], truth[1])

    stat = pstat(filename, col_slice=(100, 104), row_slice=(20, 25),
                 units="rate", plot=False)
    rate = np.array([2.09567642, 2.25052166, 2.16817045, 2.29757309,
                     2.10537601, 2.13960648, 2.02688408, 2.16728044,
                     2.00043583, 2.2481041, 2.44284439, 2.46466732,
                     2.28835583, 1.68012953, -43.30826569, 0.])
    np.testing.assert_allclose(stat[0], truth[0])
    np.testing.assert_allclose(stat[1], rate)
