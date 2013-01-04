"""
The calwfc3 module contains a function `calwf3` that calls the CALWF3 executable.
Use this function to facilitate batch runs of CALWF3, or for the TEAL interface.

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

"""

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
__version__ = "1.0"
__vdate__ = "03-Jan-2013"


def calwf3(input, printtime=False, save_tmp=False,
           verbose=False, debug=False ):
    """
    Run the calwf3.e executable as from the shell. For information on CALWF3
    see http://stsdas.stsci.edu/calwf3/.

    By default this will run the calwf3 given by 'calwf3.e'.

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


def getHelpAsString():
    """
    Returns documentation on the `calwf3` function. Required by TEAL.

    """
    return calwf3.__doc__


def run(configobj=None):
    """
    TEAL interface for the `calwf3` function.

    """
    calwf3(configobj['input'],
           printtime=configobj['printtime'],
           save_tmp=configobj['save_tmp'],
           verbose=configobj['verbose'],
           debug=configobj['debug'])


