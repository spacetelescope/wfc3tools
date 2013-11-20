from __future__ import division, print_function # confidence high

#get the auto update version 
from .version import *

# STDLIB
import pyfits
import os
from glob import glob
from stsci.tools import parseinput
from stsci.tools import teal

__taskname__ = "sub2full"
__vdate__ = "19-Nov-2013"


def sub2full(filename,x=None,y=None, fullExtent=False):
    """Return the full-frame location of the subarray coordinates using a  file specified by the user. 
    
    Parameters
    ----------
    filename : string
       The name of the image file containing the subarray. This can be a single filename or a list of files.
       The ippsoot will be used to reference the files RAW and SPT file headers

     x : int, optional
       input x position to translate, will return x0 otherwise
       if x and y are specified the fullExtent option is turned off

     y : int, optional
       input y position to translate, will return y0 otherwise
       if x and y are specified the fullExtent option is turned off
     
     fullExtent: bool, optional
      return the full extent of the subarray in the raw frame (x0,x1, y0,y1)
      This option will only work with the default specification of the corner, x0,y0
    """
    
    infiles, dummy_out= parseinput.parseinput(filename)
    coords=list()
    
    for f in infiles:
    
        root = f[0:f.find('_')]

        raw = root + '_raw.fits'
        spt = root + '_spt.fits'

        uvis_x_size = 2051
        serial_over = 25.0
        ir_overscan = 5.0

        #open up our image files
        try:
            fd1=pyfits.open(raw)
            fd2=pyfits.open(spt)
        except (ValueError,IOError) as e:
            raise ValueError('%s '%(e))
 
        #check for required keywords and close the images
        try:
            detector=fd1[0].header['DETECTOR']
            subarray=fd1[0].header['SUBARRAY']
            xcorner=int(fd2[1].header['XCORNER'])
            ycorner=int(fd2[1].header['YCORNER'])
            numrows=int(fd2[1].header['NUMROWS'])
            numcols=int(fd2[1].header['NUMCOLS'])
            fd1.close()
            fd2.close()
        except KeyError, e:
            raise KeyError("Required header keyword missing; %s"%(e))
            

        sizaxis1 = numcols
        sizaxis2 = numrows

        if (xcorner==0 and ycorner==0):
           cornera1 = 0
           cornera2 = 0
           cornera1a = cornera1 + 1
           cornera1b = cornera1a + sizaxis1 - 1
           cornera2a = cornera2 + 1
           cornera2b = cornera2a + sizaxis2 - 1
        else:
           if detector == 'UVIS':
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
              cornera1b =cornera1a + sizaxis1 - 11
              cornera2a =cornera2 + 1
              cornera2b =cornera2a + sizaxis2 - 11
              
        if (x or y):
            if ( (type(x) != type(1))  or (type(y) != type(1))):
                raise ValueError("Must input integer value for x and y ")
            else:
                cornera1a=cornera1a+x
                cornera2a=cornera2a+y
                fullExtent=False

        if (fullExtent):
            coords.append((int(cornera1a),int(cornera1b),int(cornera2a),int(cornera2b)))         
        else:
            coords.append((int(cornera1a),int(cornera2a)))         

    #return the tuple list of coordinates
    return coords

def _getHelpAsString(docstring=False):
    """
    Returns documentation on the 'sub2full' function.

    return useful help from a file in the script directory called
    __taskname__.help

    """

    install_dir = os.path.dirname(__file__)   
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    
    if docstring or (not docstring):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __vdate__]) + '\n\n'
    if os.path.exists(helpfile):
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
        
    return helpString
        
    
def help():
    print(_getHelpAsString(docstring=True))

__doc__ = _getHelpAsString(docstring=True)

if __name__ == "main":
    """called as a function from the terminal just return the default corner locations """
    import sys
    sub2full(sys.argv[1])
