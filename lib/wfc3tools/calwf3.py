""" Call the calwf3.e executable """

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
    
__taskname__ = "calwf3"
__vdate__ = "03-Jan-2013"


def calwf3(input, printtime=False, save_tmp=False,
           verbose=False, debug=False ):

    """
    CALWF3 calibrates UVIS and IR images for WFC3

    Parameters
    ----------

    input : str
        Name of input file.

    printtime : bool, optional
        Set to True to turn on the printing of time stamps.

    save_tmp: bool, optional
        Set to True to have CALWF3 save temporary files.

    verbose : bool, optional
        Set to True for verbose output.

    debug : bool, optional
        Set to True to turn on debugging output.


    If you have questions not answered in this documentation, please contact STScI Help Desk (help[at]stsci.edu). 

    Examples
    --------

    In Python without TEAL:

        >>> from wfc3tools import calwf3
        >>> calwf3.calwf3(filename)

        In Python with TEAL:

        >>> from stsci.tools import teal
        >>> from wfc3tools import calwf3
        >>> teal.teal('calwf3')

        In Pyraf:

        >>> import wfc3tools
        >>> epar calwf3


    Notes
    ------

    ``calwf3`` can be run on a single input raw file or an asn table listing the members of an associtaion. 
    When processing an association, it retrieves calibration switch and reference file keyword settings from 
    the first image listed in the asn table. ``calwf3`` does not accept a user-defined list of input images on the 
    command line (e.g. ``*raw.fits`` to process all raw files in the current directory).

    The ``wf3ccd``, ``wf32d``, and ``wf3ir`` tasks on the other hand, will accept such user-defined input file lists, 
    but they will not accept an association table( asn ) as input.



    Where to Find calwf3:

    ``calwf3`` is now part of HSTCAL package, which can be downloaded from
    http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas


    """
    
    call_list = ['calwf3.e']

    if printtime:
        call_list.append('-t')

    if save_tmp:
        call_list.append('-s')

    if verbose:
        call_list.append('-v')

    if debug:
        call_list.append('-d')


    if not os.path.exists(input):
        raise IOError('Input file not found: ' + input)

    call_list.append(input)

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
    Returns documentation on the 'calwf3' function. Required by TEAL.

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


calwf3.__doc__ = getHelpAsString(docstring=True)
        

def run(configobj=None):
    """
    TEAL interface for the 'calwf3' function.

    """
    calwf3(configobj['input'],
           printtime=configobj['printtime'],
           save_tmp=configobj['save_tmp'],
           verbose=configobj['verbose'],
           debug=configobj['debug'])


