"""
The wfc3tools module contains a function ``wf3ir`` that calls the wf3ir executable.
Use this function to facilitate batch runs or for the TEAL interface.

This routine contains all the instrumental calibration steps for WFC3 IR channel images. The steps are:

    * dqicorr - initialize the data quality array
    * zsigcorr - estimate the amount of signal in the zeroth-read
    * blevcorr - subtact the bias level from the reference pixels
    * zoffcorr - subtract the zeroth read image
    * nlincorr - correct for detector non-linear response
    * darkcorr - subtract the dark current image
    * photcorr - compute the photometric keyword values
    * unitcorr - convert to units of count rate
    * crcorr - fit accumulating signal and identify the cr hits
    * flatcorr - divide by the flatfield images and apply gain coversion
    
The output images include the calibrated image ramp (ima file) and the accumulated ramp image (flt file)
  
Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Example


    In Python without TEAL:

    >>> from wfc3tools import wf3ir
    >>> wf3ir.wf3ir(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3ir
    >>> teal.teal('wf3ir')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3ir

"""
#get the auto update version for the call to teal help
from .version import *

# STDLIB
import os.path
import subprocess

#STSCI
from stsci.tools import parseinput
try:
    from stsci.tools import teal
except:
    teal = None
    
__taskname__ = "wf3ir"
__vdate__ = "03-Jan-2013"

def wf3ir(input, output="", verbose=False, quiet=True ):    
    """Run the ``wf3ir.e`` executable as from the shell."""

    call_list = ['wf3ir.e']

    if verbose:
        call_list += ['-v','-t']

    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    if output:
        outfiles, dummpy_out= parseinput.parseinput(output)
        call_list.append(','.join(outfiles))
    subprocess.call(call_list)


def help(file=None):
    helpstr = getHelpAsString(docstring=True)
    if file is None:
        print helpstr
    else:
        if os.path.exists(file): os.remove(file)
        f = open(file,mode='w')
        f.write(helpstr)
        f.close()
    

def getHelpAsString(docstring=False):
    """
    Returns documentation on the 'wf3ir' function. Required by TEAL.

    return useful help from a file in the script directory called
    __taskname__.help

    """

    install_dir = os.path.dirname(__file__)
    htmlfile = os.path.join(install_dir, 'htmlhelp', __taskname__ + '.html')
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    if docstring or (not docstring and not os.path.exists(htmlfile)):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __vdate__]) + '\n\n'
        if os.path.exists(helpfile):
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
    else:
        helpString = 'file://' + htmlfile

    return helpString


wf3ir.__doc__ = getHelpAsString(docstring=True)

def run(configobj=None):
    """
    TEAL interface for the ``wf3ir`` function.

    """
    wf3ir(configobj['input'],
           output=configobj['output'],
           quiet=configobj['quiet'],
           verbose=configobj['verbose'],)
           
           
