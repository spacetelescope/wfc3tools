# STDLIB
from astropy.io import fits
import os
from stsci.tools import parseinput

__taskname__ = "sub2full"


def sub2full(filename, x=None, y=None, fullExtent=False):

    infiles, dummy_out = parseinput.parseinput(filename)
    if len(infiles) < 1:
        return ValueError("Please input a valid HST filename")

    coords = list()

    for f in infiles:
        spt = f[0:9] + '_spt.fits'
        uvis_x_size = 2051
        serial_over = 25.0
        ir_overscan = 5.0

        # open up our image files
        try:
            fd2 = fits.open(spt)
        except (ValueError, IOError) as e:
            raise ValueError('%s ' % (e))

        # check for required keywords and close the images
        try:
            detector = fd2[0].header['SS_DTCTR']
            subarray = fd2[0].header['SS_SUBAR']
            xcorner = int(fd2[1].header['XCORNER'])
            ycorner = int(fd2[1].header['YCORNER'])
            numrows = int(fd2[1].header['NUMROWS'])
            numcols = int(fd2[1].header['NUMCOLS'])
            fd2.close()
        except KeyError as e:
            raise KeyError("Required header keyword missing; %s" % (e))

        if "NO" in subarray:
            raise ValueError("Image is not a subarray: %s" % (f))

        sizaxis1 = numcols
        sizaxis2 = numrows

        if (xcorner == 0 and ycorner == 0):
            cornera1 = 0
            cornera2 = 0
            cornera1a = cornera1 + 1
            cornera1b = cornera1a + sizaxis1 - 1
            cornera2a = cornera2 + 1
            cornera2b = cornera2a + sizaxis2 - 1
        else:
            if 'UVIS' in detector:
                cornera1 = ycorner
                cornera2 = uvis_x_size - xcorner - sizaxis2
                if xcorner >= uvis_x_size:
                    cornera2 = cornera2 + uvis_x_size

                cornera1a = cornera1 + 1 - serial_over
                cornera1b = cornera1a + sizaxis1 - 1
                cornera2a = cornera2 + 1
                cornera2b = cornera2a + sizaxis2 - 1

                if cornera1a < 1:
                    cornera1a = 1
                if cornera1b > 4096:
                    cornera1b = 4096

            else:
                cornera1 = ycorner - ir_overscan
                cornera2 = xcorner - ir_overscan
                cornera1a = cornera1 + 1
                cornera1b = cornera1a + sizaxis1 - 11
                cornera2a = cornera2 + 1
                cornera2b = cornera2a + sizaxis2 - 11

        if (x or y):
            if ((not isinstance(x, int) or (not isinstance(y, int)))):
                raise ValueError("Must input integer value for x and y ")
            else:
                cornera1a = cornera1a + x
                cornera2a = cornera2a + y
                fullExtent = False

        if (fullExtent):
            coords.append((int(cornera1a), int(cornera1b), int(cornera2a),
                           int(cornera2b)))
        else:
            coords.append((int(cornera1a), int(cornera2a)))

    # return the tuple list of coordinates
    return coords
