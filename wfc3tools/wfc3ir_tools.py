from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import glob
import os 
import shutil 
import numpy as np
from wfc3tools import calwf3
import glob
import pyregion

def _reprocess_raw_crcorr(raw_file):

	"""Bookkeeping + call to calwf3 to make ima from raw, turning CRCORR switch off."""
	
	### temporary rename of file
	os.rename(raw_file, 'temp_'+ raw_file)
	raw_file = 'temp_'+ raw_file

	raw_hdu = fits.open(raw_file, mode = 'update')
	
	### set CRCORR to OMIT 
	orig_setting = raw_hdu[0].header['CRCORR']
	raw_hdu[0].header['CRCORR'] = 'OMIT'	
	raw_hdu.close()
	
	### if part of an association, assert .ASN is in same directory as .RAW
	### catch error now - later the .ima won't run though the pipeline without the .asn.
	asn_tab = raw_hdu[0].header['ASN_TAB']
	if asn_tab != '':
		if not os.path.isfile(asn_tab):
			raise OSError("{} must be in same directory as raw file.".format(asn_tab))

	### remove existing 'temp' files from previous run with same name, if they exist
	exts = ['flt','flc','ima']
	existing_files = [raw_file.replace('raw', ext) for ext in exts]
	
	for f in existing_files:
		if os.path.isfile(f):
			os.remove(f)
			
	### run calwf3
	calwf3(raw_file)
	
	### removing resulting FLT and TRA, we just want IMA generated with CRCORR off
	for f in existing_files[0:2]:
		if os.path.isfile(f):
			os.remove(f)
	os.remove(raw_file.replace('_raw.fits','.tra'))

	### rename raw file to original, IMA from 'temp' to 'flattened', and tra
	os.rename(raw_file, raw_file.replace('temp_',''))
	raw_file = raw_file.replace('temp_','')
	os.rename('temp_'+raw_file.replace('raw','ima'), \
			  'flattened_' + raw_file.replace('raw','ima'))

	### reset CRCORR in raw file to original setting so file is unchanged
	raw_hdu = fits.open(raw_file, mode = 'update')
	raw_hdu[0].header['CRCORR'] = orig_setting	
	raw_hdu.close()

def _calc_avg(data, stats_method, sigma_clip, sigma, sigma_upper, sigma_lower, iters):
	""" Returns a mean or median from an array, with optional sigma clipping."""
	if not sigma_clip:
		if stats_method == 'median':
			return np.median(data)
		return np.mean(data)
	else:
		mean, med, s = sigma_clipped_stats(data, sigma = sigma, sigma_lower = sigma_lower, 
                                    	   sigma_upper = sigma_upper, iters = iters)
		if stats_method == 'median':
			return med
		return mean
	
def make_flattened_ramp_flt(raw_file, stats_subregion = None, stats_method = 'median', 
							sigma_clip = False, sigma = None, sigma_upper = None,
							sigma_lower = None, iters = None):

	""" 
	Corrects for non-variable background and produce a 'flattened' FLT and IMA. Users 
	supply a raw file, which is used to create an ima file with calwf3 with the CRCORR 
	switch set to OMIT. Then, the average background level from each read of the ima is 
	subtracted from the read, and later added back to the full exposure to preserve pixel 
	statistics. Finally, calwf3 is run again on the flattened ima to produce an flt.
	
	Note that if the raw file is part of an association, the .asn file must be in the 
	same directory as the raw file. 
	
	Users may provide a region for the median to be computed, otherwise this
	will default to the median over the whole image excluding the 5 pixel overscan
	region on the border. 
	
	Parameters
	-----------
	raw_file : str
		Full path to raw file.
	stats_subregion : tuple
		Tuple of ((xmin, xmax), (ymin, ymax)) to specify region for average calculation.
		Defaults to whole image, excluding the 5-pixel overscan region.	
	stats_method : str	
		Method of stats computation on each read when subtracting the average to flatten.
		Must be 'mean' or 'median'. Defaults to 'median'.
	sigma_clip : bool
		If True, data will be sigma-clipped when computing stats. Defaults to False.
	sigma : int
		The number of standard deviations to use as the lower 
		and upper clipping limit. Defaults to None, but must be set if sigma_clip = True.
	sigma_upper : int
		The number of standard deviations to use as the upper bound for the clipping 
		limit. If None then the value of sigma is used. Defaults to None.
	sigma_lower : int
		The number of standard deviations to use as the lower bound for the clipping 
		limit. If None then the value of sigma is used. Defaults to None.
	iters : int
		The number of iterations to perform sigma clipping. Defaults to None, but must 
		be set if sigma_clip = True.
		
	Outputs
	--------
	An FLT and IMA file created after flattening the reads (flattened_{}_flt.fits, 
	flattened_{}_ima.fits, and flattened_{}.tra)
	
	"""
	### input checking 
	if stats_method not in ['median', 'mean']:
		raise ValueError('stats_method must be mean or median')
	if not sigma_clip:
		if sigma or sigma_upper or sigma_lower or iters:
			true_params = np.array(('sigma','sigma_upper','sigma_lower'))[np.array((sigma,\
									sigma_upper,sigma_lower)).astype('bool')]
			raise ValueError('sigma_clip = False, but parameters {} were set'.\
								format(true_params))
	else:
		if not sigma:
			raise ValueError('sigma_clipping = True, parameter sigma must be provided')
					
	starting_path = os.getcwd()
	basename_raw = os.path.basename(raw_file)
	path_raw = raw_file.replace(basename_raw,'')
	raw_hdu = fits.open(raw_file, mode = 'update')

	### must work in pwd for calwf3 
	os.chdir(path_raw)
	### run calwf3 w/ CRCORR off on raw to make ima
	_reprocess_raw_crcorr(basename_raw)
	
	### work on new flattened IMA
	ima_file = raw_file.replace(basename_raw, 'flattened_' + basename_raw).replace('raw','ima')
	ima_hdu = fits.open(ima_file, mode='update')
	naxis1, naxis2 = ima_hdu['SCI',1].header['naxis1'], ima_hdu['SCI',1].header['naxis2']

	### default to whole image minus the 5 overscan pixels 
	if stats_subregion is None:
		xmin, xmax = 5, naxis1	
		ymin, ymax = 5, naxis2
	stats_region =[[xmin,xmax], [ymin,ymax]]
	slx = slice(stats_region[0][0], stats_region[0][1])
	sly = slice(stats_region[1][0], stats_region[1][1])

	### subtract per-read median countrate scalar and add back in full exposure count 
	### rate to preserve pixel statistics
	total_countrate = _calc_avg(ima_hdu['SCI',1].data[sly, slx], stats_method, \
								sigma_clip, sigma, sigma_upper, sigma_lower, iters)

	for i in range(ima_hdu[0].header['NSAMP']-1):
		avg = _calc_avg(ima_hdu['SCI',i+1].data[sly, slx], stats_method, \
								sigma_clip, sigma, sigma_upper, sigma_lower, iters)
		ima_hdu['SCI',i+1].data += total_countrate - avg 

	### turn back on the ramp fitting and run calwf3
	ima_hdu[0].header['CRCORR'] ='PERFORM'
	ima_hdu.flush()
	ima_hdu.close()
	calwf3(ima_file)
	
	### remove one copy of IMA file and rename newly processed files
	os.remove(ima_file) 
	for f in glob.glob(starting_path+'/flattened_'+basename_raw.replace('_raw.fits','') + '*'):
		if ('_ima_' in f) or ('.tra' in f):
			os.rename(f,f.replace('_ima','',1))

	os.chdir(starting_path)