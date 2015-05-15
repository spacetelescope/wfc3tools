"""
CALWF3 calibrates UVIS and IR images for WFC3
"""

#get the auto update version for the call to teal help
from __future__ import absolute_import, print_function
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

    """ Call the calwf3.e executable """

    
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
        print(helpstr)
    else:
        if os.path.exists(file): os.remove(file)
        f = open(file,mode='w')
        f.write(helpstr)
        f.close()
    

def getHelpAsString(docstring=False):
    """Return documentation on the 'wf3ir' function. Required by TEAL."""

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
        

def run(configobj=None):
    """
    TEAL interface for the 'calwf3' function.

    """
    calwf3(configobj['input'],
           printtime=configobj['printtime'],
           save_tmp=configobj['save_tmp'],
           verbose=configobj['verbose'],
           debug=configobj['debug'])


calwf3.__doc__ = getHelpAsString(docstring=True)
