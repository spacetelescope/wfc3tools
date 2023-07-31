from wfc3tools.pstat import pstat
from astropy.io import fits
import numpy as np

import glob
import os
import shutil


class TestPSTAT:

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


    def test_pstat_basic(self):
    	# test basic functionality of pstat

	    # set slice of image to 1 so stats are all just 1. 
	    with fits.open(self.input_ima, mode='update') as hdu:
	        for i in range(1, 17):
	            hdu["SCI", i].header['SAMPTIME'] = 1.0  # make all exptimes 1s
	            hdu['SCI', i].data[:, :] = 1. # and all data values

	    xdata, ydata = pstat(self.input_ima)
	    assert(np.all(xaxis[:-1]) == 1.)
        assert(np.all(yaxis[:-1]) == 1.)


   def test_pstat_stat_modes(self):

   	    # set slice of image to 1 so stats are all just 1. 
    	with fits.open(self.input_ima, mode='update') as hdu:
        	for i in range(1, 17):
            	hdu["SCI", i].header['SAMPTIME'] = 1.0  # make all exptimes 1s
            	hdu['SCI', i].data[:, :] = 1. # and all data values

        # test every stat
    	stats = ["mean", "midpt", "mode", "stddev", "min", "max"]
    	for stat in stats:
        	xaxis, yaxis = pstat(input_ima)
        	assert(np.all(xaxis[:-1]) == 1.)
        	assert(np.all(yaxis[:-1]) == 1.)


    def test_pstat_slice(self):
    	# test using slices of data rather than whole array

	   	slicee = (0, 5)

	    # set slice of image to 1 so stats are all just 1. 
	    with fits.open(self.input_ima, mode='update') as hdu:
	        for i in range(1, 17):
	            hdu["SCI", i].header['SAMPTIME'] = 1.0  # make all exptimes 1s
	            hdu['SCI', i].data[0:5, 0:5] = 99. # and all data values
	    xaxis, yaxis = pstat(self.input_ima, row_slice=slicee, col_slice=slicee)
	    assert(np.all(xaxis[:-1]) == 99.)
	    assert(np.all(yaxis[:-1]) == 99.)


	def test_pstat_ext(self):
		# test using err/dq instead of sci

		exts = ['ERR', 'DQ']

		for ext in exts:
			# set slice of image to 1 so stats are all just 1. 
    		with fits.open(self.input_ima, mode='update') as hdu:
        		for i in range(1, 17):
            		hdu[ext, i].header['SAMPTIME'] = 1.0  # make all exptimes 1s
            		hdu[ext, i].data[:, :] = 1. # and all data values

           	xdata, ydata = pstat(self.input_ima, extname=ext)
           	assert(np.all(xaxis[:-1]) == 1.)
	    	assert(np.all(yaxis[:-1]) == 1.)
