from astropy.io import fits
import glob
import os 
import shutil 
import numpy as np
from wfc3tools import calwf3
import glob
import pyregion

def _reprocess_raw_crcorr(raw_file):

	raw_hdu = fits.open(raw_file, mode = 'update')
	### if raw file is part of an asn, assert that .asn is in same directory as .raw
	asn_tab = raw_hdu[0].header['ASN_TAB']
	if asn_tab != '':
		if not os.path.isfile(asn_tab):
			raise OSError("{} must be in same directory as raw file.".format(asn_tab))
	### generate ima file with CRCORR set to OMIT 
	orig_setting = raw_hdu[0].header['CRCORR']
	raw_hdu[0].header['CRCORR'] = 'OMIT'	
	raw_hdu.close()
	if verbose == True:
		print('Removing existing calwf3 outputs for {}'.format(raw_file))
	### remove existing files with same name
	for ext in ['flt','ima']:
		if os.path.isfile(raw_file.replace('raw',ext)):
			os.remove(raw_file.replace('raw',ext))
	if os.path.isfile(raw_file.replace('_raw.fits','.tra')):
		os.remove(raw_file.replace('_raw.fits','.tra'))
	### run calwf3
	if verbose == True:
		print('Generating initial IMA')
	calwf3(raw_file, verbose = verbose)
def make_flattened_ramp_flt(raw_file, 
							stats_subregion = None, outfile = None, verbose = False):

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
	raw_file : string
		Full path to raw file.
	stats_subregion : tuple
		Tuple of ((xmin, xmax), (ymin, ymax)) to specify region for average calculation.
		Defaults to whole image, excluding the 5-pixel overscan region.
	outfile : str
		output file name. Defaults to original file rootnames with 'flt'
	verbose : bool
		*** This flag requires a not yet implemented fix in calwf3. 
		
	Outputs
	--------
	An FLT and IMA file created after flattening the reads (flattened_{}_flt.fits, 
	flattened_{}_ima.fits, and flattened_{}.tra)
	
	"""
	basename_raw = os.path.basename(raw_file)
	os.rename(raw_file, raw_file.replace(basename_raw,'flattened_'+basename_raw))
	raw_file_temp = raw_file.replace(basename_raw,'flattened_'+basename_raw)
	raw_hdu = fits.open(raw_file_temp, mode = 'update')
	
	### generate ima file with CRCORR set to OMIT 
	asn_tab = raw_hdu[0].header['ASN_TAB']
	orig_setting = raw_hdu[0].header['CRCORR']
	raw_hdu[0].header['CRCORR'] = 'OMIT'	
	raw_hdu.flush()
	raw_hdu.close()
	### if raw file is part of an asn, assert that .asn is in same directory as .raw
	if asn_tab != '':
		if not os.path.isfile(asn_tab):
			raise OSError("{} must be in same directory as raw file.".format(asn_tab))

	### remove existing calwf3 output with same name
	for ext in ['flt','ima']:
		if os.path.isfile(raw_file.replace('raw',ext)):
			os.remove(raw_file.replace('raw',ext))
	if os.path.isfile(raw_file.replace('_raw.fits','.tra')):
		os.remove(raw_file.replace('_raw.fits','.tra'))
		
	### run calwf3
	calwf3(raw_file, verbose = verbose)
	
	###remove intermediate flt/tra 
	if os.path.isfile(raw_file.replace('raw','flt')):
		os.remove(raw_file.replace('raw','flt'))
	if os.path.isfile(raw_file.replace('_raw.fits','.tra')):
		os.remove(raw_file.replace('_raw.fits','.tra'))
	## change switch back to what it was originally so input file is not modified
	raw_hdu = fits.open(raw_file, mode = 'update')
	raw_hdu[0].header['CRCORR'] = orig_setting
	raw_hdu.flush()
	raw_hdu.close()
	os.rename(raw_file, orig_raw_path)
	
 	#work on new ima
	ima_file = raw_file.replace('raw','ima')
	ima_hdu = fits.open(ima_file, mode='update')
	naxis1, naxis2 = ima_hdu['SCI',1].header['naxis1'], ima_hdu['SCI',1].header['naxis2']
	
	#default to whole image minus the 5 overscan pixels 
	if stats_subregion is None:
		xmin, xmax = 5, naxis1
		ymin, ymax = 5, naxis2
	stats_region =[[xmin,xmax], [ymin,ymax]]
	slx = slice(stats_region[0][0], stats_region[0][1])
	sly = slice(stats_region[1][0], stats_region[1][1])
	
	#Subtract per - read median count - rate scalar and add back in
	#full exposure count rate to preserve pixel statistics
	total_countrate = np.median(ima_hdu['SCI',1].data[sly, slx])
	
	for i in range(ima_hdu[0].header['NSAMP']-1):
		med = np.median(ima_hdu['SCI',i+1].data[sly, slx])
		ima_hdu['SCI',i+1].data += total_countrate - med
		if verbose == True:
			print('%s, [SCI,%d], median_bkg: %.2f' %(raw_file, i+1, med))  
		
	#Turn back on the ramp fitting for running calwf3 in the next step
	ima_hdu[0].header['CRCORR'] ='PERFORM'
	ima_hdu.close()
	
	calwf3(ima_file)
	
	#remove intermediate ima & rename new one
	os.remove(ima_file)
	
	base_dir = orig_raw_path.replace(basename_raw,'')
	for f in glob.glob(base_dir+'flattened_'+basename_raw.replace('_raw.fits','') + '*'):
		if '_ima' in f:
			print(f,f.replace('_ima','',1))
			os.rename(f,f.replace('_ima','',1))
	
# def ir_satmask(raw_file, region_filename, imset):
#     """
#     Mask satellite trails in the DQ array of individual IMA read.
# 
#     Note that if the raw file is part of an association, the .asn file must be
#     in the same directory as the raw file.
# 
#     Parameters
#     ----------
#     raw_input : str
#         Input raw file to be sattelite corrected
# 
#     region_filename: str
#         Input region file name. Expecting DS9 style region file
# 
#     imset: int
#         Imset (Read number) that needs to be satellite corrected.
# 
#     """
#     
# 	orig_raw_path = raw_file
# 	basename_raw = os.path.basename(orig_raw_path)
# 	os.rename(raw_file, raw_file.replace(basename_raw,'flattened_'+basename_raw))
# 	raw_file = raw_file.replace(basename_raw,'flattened_'+basename_raw)
# 	raw_hdu = fits.open(raw_file, mode = 'update')
# 	### if raw file is part of an asn, assert that .asn is in same directory as .raw
# 	asn_tab = raw_hdu[0].header['ASN_TAB']
# 	if asn_tab != '':
# 		if not os.path.isfile(asn_tab):
# 			raise OSError("{} must be in same directory as raw file.".format(asn_tab))
# 	### generate ima file with CRCORR set to OMIT 
# 	orig_setting = raw_hdu[0].header['CRCORR']
# 	raw_hdu[0].header['CRCORR'] = 'OMIT'	
# 	raw_hdu.close()
# 	if verbose == True:
# 		print('Removing existing calwf3 outputs for {}'.format(raw_file))
# 	### remove existing files with same name
# 	for ext in ['flt','ima']:
# 		if os.path.isfile(raw_file.replace('raw',ext)):
# 			os.remove(raw_file.replace('raw',ext))
# 	if os.path.isfile(raw_file.replace('_raw.fits','.tra')):
# 		os.remove(raw_file.replace('_raw.fits','.tra'))
# 	### run calwf3
# 	if verbose == True:
# 		print('Generating initial IMA')
# 	calwf3(raw_file, verbose = verbose)
# 	
	
	
	
	