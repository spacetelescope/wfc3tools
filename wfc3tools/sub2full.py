from __future__ import division, print_function  

# get the auto update version
from .version import __version_date__, __version__

# STDLIB
from astropy.io import fits
import os
from stsci.tools import parseinput, teal

__taskname__ = "sub2full"


def sub2full(filename, x=None, y=None, fullExtent=False):
    """ 
    Given an image specified by the user which contains a subarray readout,
    returns the location of the corner of the subarray in a full frame reference 
    image (including the full physical extent of the chip) in 1-indexed pixels.

    If the user supplies an X and Y coordinate, then the translated location of
    that point will be returned.

    Parameters
    -----------
    filename : str or list of str
        Input image or list of input images. This function requires that for 
        each file in ``filename``, the associated SPT file must be in the same
        directory. 
    x, y : None, int (optional)
        Specify an x/y coordinate in the subarray to translate. If an x and y 
        are specified, the ``fullExtent`` option is turned off and only the 
        translated x,y coords are returned.
    fullExtent : bool (Default = False, optional)
        If set, the returned values will include the full extent of the 
        subarray in the reference image, for example: (x0,x1,y0,y1).

    Returns
    -------
    coords : tuple or list of tuples
        A list of tuples which specify the translated coordinates, either 
        (x0,y0) for each image or the full extent sections.
    """

    infiles, dummy_out = parseinput.parseinput(filename)
    if len(infiles) < 1:
        return ValueError("Please input a valid HST filename")

    coords = list()

    for f in infiles:

        spt = os.path.join(os.path.dirname(f), os.path.basename(f)[0:9] + '_spt.fits')
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


def getHelpAsString(docstring=False):
    """
    Returns documentation on the 'sub2full' function.

    return useful help from a file in the script directory called
    __taskname__.help

    """

    install_dir = os.path.dirname(__file__)
    helpfile = os.path.join(install_dir, __taskname__ + '.help')

    if docstring or (not docstring):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __version_date__]) + '\n\n'
    if os.path.exists(helpfile):
            helpString += teal.getHelpFileAsString(__taskname__, __file__)

    return helpString


def help():
    print(getHelpAsString(docstring=True))

sub2full.__doc__ = getHelpAsString(docstring=True)

if __name__ == "main":
    """called from system shell, return the default corner locations """
    import sys
    sub2full(sys.argv[1])
