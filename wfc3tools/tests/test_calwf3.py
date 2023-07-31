"""Licensed under a 3-clause BSD style license - see LICENSE.rst."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pytest
from wfc3tools import calwf3

import glob
import os
import shutil


def test_no_valid_input():
    """Run a very simple aliveness test."""
    with pytest.raises(IOError) as e:
        def cal():
            calwf3()
        cal()
    assert 'No valid image specified' in str(e.value)


def test_version_print():
    """Make sure no error results from version print."""
    def cal():
        calwf3(version=True)
    cal()

class TestCALWF3:
    # Test that the wrapper for calwf3 runs, and that input
    # parameters to the function are appropriatley passed
    # to calwf3.e

    # test data (and reference files) should be on disk
    # (figure out best way to do this, for now just have test data in repo)
    # tried making dummy files that are generated and written out then deleted, 
    # but calwf3 crashes. there should be a way to do this but giving up for now.

    def __init__(self):
        self.data_dir = os.path.join(os.getcwd(), 'wfc3_data')
        self.tmp_dir = os.path.join(os.getcwd(), 'tmp_dir')
        if not os.path.isdir(self.tmp_dir):
            os.mkdir(self.tmp_dir)

        # cleanup just to be safe before running any tests
        self.cleanup_dir()

    def cleanup_dir(self):
        # remove all files in temporary directory

        for f in glob.glob(self.tmp_dir + '/*'):
            os.remove(f)

    def test_calwf3_input_single_raw(self):

        # copy over a single raw file to temp directory
        shutil.copy(glob.glob(os.path.join(self.data_dir, 'IR/SA/iev519qzq_raw.fits'))[0], self.tmp_dir)

        # single filename
        input_raw = os.path.join(self.tmp_dir, 'iev519qzq_raw.fits')
        ret = calwf3(input_raw)
        self.cleanup_dir()
        assert ret == 1

    def test_calwf3_input_list_raws(self):

        # xfail this test! even though the documentation says this input type is
        # possible it's not. 

        # copy over all raw files in asn to temp directory
        for f in glob.glob(os.path.join(self.data_dir, 'IR/SA/*raw.fits')):
            shutil.copy(f, self.tmp_dir)

        input_raws = glob.glob(self.tmp_dir + '/*raw.fits')

        ret = calwf3(input_raws)
        self.cleanup_dir()
    
        assert ret == 1

    def test_calwf3_input_wildcard(self):

        # also xfail this for now until its fixed, documentation advertises
        # this as an option but it fails in calwf3.e

        # copy over all raw files in asn to temp directory
        for f in glob.glob(os.path.join(self.data_dir, 'IR/SA/*raw.fits')):
            shutil.copy(f, self.tmp_dir)

        ret = calwf3(self.tmp_dir + '/*raw.fits')
        self.cleanup_dir()
    
        assert ret == 1

    def test_calwf3_input_asn(self):

        # this test is failing in python, but i can run it on command line.
        # is this a character limit issue? 

        # copy over all raw files in asn to temp directory
        for f in glob.glob(os.path.join(self.data_dir, 'UVIS/SA/*raw.fits')):
            shutil.copy(f, self.tmp_dir)

        # and asn
        shutil.copy(glob.glob(os.path.join(self.data_dir, 'UVIS/SA/*asn*'))[0], self.tmp_dir)

        input_asn = os.path.join(self.tmp_dir, 'iev510050_asn.fits')
        ret = calwf3(input_asn)
        #self.cleanup_dir()
    
        assert ret == 1

    def test_calwf3_output_filename(self):
        # this also needs to be fixed, skip/xfail for now.
        
        # copy over a single raw file to temp directory
        shutil.copy(glob.glob(os.path.join(self.data_dir, 'IR/SA/iev519qzq_raw.fits'))[0], self.tmp_dir)

        # single filename
        input_raw = os.path.join(self.tmp_dir, 'iev519qzq_raw.fits')

        calwf3(input_raw, output='test_output')
        self.cleanup_dir()
    
        assert os.path.isfile(os.path.join(self.tmp_dir, 'test_output.fits'))


    def test_calwf3_save_tmp(self):
        # test that all the intermediate files are saved to disk
        # when ``save_tmp=True``. for some reason, this is only working
        # for UVIS.

        # run on single IR raw
        shutil.copy(glob.glob(os.path.join(self.data_dir, 'UVIS/FF/id5e01pfq_raw.fits'))[0], self.tmp_dir)
        input_raw = os.path.join(self.tmp_dir, 'id5e01pfq_raw.fits')
        ret = calwf3(input_raw, save_tmp=True)

        # make sure expected temporary outputs were produced
        expected_tmp_outputs = ['rac_tmp', 'blc_tmp', 'blv_tmp']
        for f in expected_tmp_outputs:
            assert(os.path.isfile(os.path.join(self.tmp_dir, f'id5e01pfq_{f}.fits')))
