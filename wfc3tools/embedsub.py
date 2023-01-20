from .sub2full import sub2full

# STDLIB
from astropy.io import fits
import os
import numpy

# STSCI
from stsci.tools import parseinput

__taskname__ = "embedsub"


def embedsub(files):
    """Return the full-frame location of the subarray.

    Parameters
    ----------
    filename : string
       The name of the image file containing the subarray. This can be a
       single filename or a list of files. The ippsoot will be used to
       construct the output filename. You should input an FLT image

    The output file will contain the subarray image placed inside the full
    frame extent of a regular image

    """
    uvis = False
    uvis_full_x = 2051
    uvis_full_y = 4096
    ir_full = 1014

    infiles, dummy_out = parseinput.parseinput(files)
    if len(infiles) < 1:
        return ValueError("Please input a valid HST filename")

    # process all the input subarrays
    for filename in infiles:

        # Make sure the input name conforms to normal style
        if '_flt' not in filename:
            print("Warning: Can't properly parse '%s'; Skipping" % files)

        # Extract the root name and build SPT and output file names
        root = filename[0:filename.find('_flt')]
        full = root[0:len(root)-1] + 'f_flt.fits'

        try:
            flt = fits.open(filename)
        except EnvironmentError:
            print("Problem opening fits file %s" % (filename))

        detector = flt[0].header['DETECTOR']
        if 'UVIS' in detector:
            uvis = True

        # compute subarray corners assuming the raw image location
        x1, x2, y1, y2 = sub2full(filename, fullExtent=True)[0]
        print("Subarray image section [x1,x2,y1,y2] = [%d:%d,%d:%d]" % (x1, x2,
                                                                        y1, y2))

        if uvis:
            xaxis = uvis_full_x
            yaxis = uvis_full_y
        else:
            xaxis = ir_full
            yaxis = ir_full

        # Now copy the subarray image data into full-chip data arrays;
        # The regions outside the subarray will be set to zero in the
        # SCI, ERR, SAMP, and TIME extensions, and to DQ=4.
        sci = numpy.zeros([xaxis, yaxis], dtype=numpy.float32)
        err = numpy.zeros([xaxis, yaxis], dtype=numpy.float32)
        dq = numpy.zeros([xaxis, yaxis], dtype=numpy.int16) + 4

        sci[y1-1:y2, x1-1:x2] = flt[1].data
        err[y1-1:y2, x1-1:x2] = flt[2].data
        dq[y1-1:y2, x1-1:x2] = flt[3].data

        if not uvis:
            samp = numpy.zeros([xaxis, yaxis], dtype=numpy.int16)
            time = numpy.zeros([xaxis, yaxis], dtype=numpy.float32)
            samp[y1-1:y2, x1-1:x2] = flt[4].data
            time[y1-1:y2, x1-1:x2] = flt[5].data

        # Reset a few WCS values to make them appropriate for a
        # full-chip image
        crpix1 = flt[1].header['CRPIX1']
        crpix2 = flt[1].header['CRPIX2']

        flt[1].header['sizaxis1'] = yaxis
        flt[1].header['sizaxis2'] = xaxis

        # loop through each possible fits extension and modify keywords if they exist
        for i in range(1, len(flt)):
            try:
                _ = flt[i].header['crpix1'] # if crpix1 doesn't exist this will cause a KeyError
                flt[i].header['crpix1'] = crpix1 + x1 - 1
                flt[i].header['crpix2'] = crpix2 + y1 - 1
                _ = flt[i].header['ltv1'] # if ltv1 doesn't exist this will cause a KeyError
                flt[i].header['ltv1'] = 0.0
                flt[i].header['ltv2'] = 0.0
            except KeyError:
                # if crpix1 doesn't exist pass to the next extension
                pass
                # Note: it's ok to keep this all under one try because there will 
                # never be a scenario where crpix1 doesn't exist but ltv1 does.
                # However, there are some extensions where crpix1 exists but ltv1 doesn't.

        # set the header value of SUBARRAY to False since it's now
        # regular size image
        flt[0].header['SUBARRAY'] = False
        
        # Now write out the SCI, ERR, DQ extensions to the full-chip file
        hdu_list = fits.open(filename)
        hdu_list[0].header = flt[0].header
        hdu_list[1].data = sci
        hdu_list[1].header = flt[1].header
        hdu_list[2].data = err
        hdu_list[2].header = flt[2].header
        hdu_list[3].data = dq
        hdu_list[3].header = flt[3].header
        if not uvis:
            hdu_list[4].data = samp
            hdu_list[4].header = flt[4].header
            hdu_list[5].data = time
            hdu_list[5].header = flt[5].header

        hdu_list.writeto(full, overwrite=False)
        hdu_list.close() 

        # close the input files
        flt.close()
        print("Image saved to: %s" % (full))
