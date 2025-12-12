import numpy as np
from astroquery.mast import Observations

from wfc3tools import pstack


def test_pstack(_jail):
    filename = "ibh719grq_ima.fits"
    Observations.download_file(f"mast:HST/product/{filename}", cache=True)

    x_data, y_data = pstack("ibh719grq_ima.fits", column=100, row=25, extname="sci", plot=False)

    x_truth = np.array(
        [
            100.651947,
            93.470573,
            86.2892,
            79.107826,
            71.926453,
            64.745079,
            57.563702,
            50.382328,
            43.200954,
            36.019581,
            28.838205,
            21.65683,
            14.475455,
            7.29408,
            0.112705,
            0.0,
        ]
    )
    y_truth = np.array(
        [
            136.75660802,
            151.46077054,
            133.8688648,
            108.50410805,
            109.17918583,
            81.5139582,
            90.26712192,
            61.68512157,
            59.11241987,
            39.01870227,
            32.63157047,
            16.07532735,
            33.69198196,
            16.90631634,
            13.54113704,
            0.0,
        ]
    )

    # MAST data can change over time, 1% agreement is good enough.
    np.testing.assert_allclose(x_data, x_truth, rtol=0.01)
    np.testing.assert_allclose(y_data, y_truth, rtol=0.01)
