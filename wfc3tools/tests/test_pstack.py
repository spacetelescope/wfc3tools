from wfc3tools.pstack import pstack
from astropy.io import fits
import numpy as np


class TestPSTACK:

    def __init__(self):
    self.data_dir = os.path.join(os.getcwd(), 'wfc3_data')
    self.tmp_dir = os.path.join(os.getcwd(), 'tmp_dir')
    if not os.path.isdir(self.tmp_dir):
        os.mkdir(self.tmp_dir)

    # cleanup just to be safe before running any tests
    self.cleanup_dir()

    # copy test file once, no outputs created, clean up after all tests
    shutil.copy(glob.glob(os.path.join(data_dir, 'IR/SA/iev519qyq_ima.fits'))[0], tmp_dir)
    self.input_ima = os.path.join(tmp_dir, 'iev519qyq_ima.fits')

    def cleanup_dir(self):
        # remove all files in temporary directory

        for f in glob.glob(self.tmp_dir + '/*'):
            os.remove(f)


    def test_pstack_basic():
        # test basic functionality of pstack

        with fits.open(self.input_ima, mode='update') as hdu:
            for i in range(1, 17):
                hdu["SCI", i].header['SAMPTIME'] = 1.0  # make all extimes 1s
                hdu['SCI', i].data[0, 0] = 1. # and data values

        xaxis, yaxis = pstack(self.input_ima, column=0, row=0, extname="sci")
        assert(np.all(xaxis[:-1]) == 1.)
        assert(np.all(yaxis[:-1]) == 1.)


    def test_pstack_ext(self):
        # test using 'ERR' or 'DQ' instead of 'SCI'

        exts = ['ERR', 'DQ']

        for ext in exts:
            # set slice of image to 1 so stats are all just 1. 
            with fits.open(self.input_ima, mode='update') as hdu:
                for i in range(1, 17):
                    hdu[ext, i].header['SAMPTIME'] = 1.0  # make all exptimes 1s
                    hdu[ext, i].data[:, :] = 1. # and all data values

            xaxis, yaxis = pstack(self.input_ima, column=0, row=0, extname=ext)
            assert(np.all(xaxis[:-1]) == 1.)
            assert(np.all(yaxis[:-1]) == 1.)
