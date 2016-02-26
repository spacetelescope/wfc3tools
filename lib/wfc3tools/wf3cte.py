"""
wf3cte  calls the wf3cte executable and contains the initial processing steps for all the WFC3 UVIS channel data.
"""
from __future__ import print_function #confidence high

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
    
__taskname__ = "wf3cte"
__vdate__ = "28-Sep-2015"

def wf3cte(input, parallel=True, verbose=False):
    
    """Run the ``wf3cte.e`` executable as from the shell."""

    call_list = ['wf3cte.e']
    
    if verbose:
        call_list += ['-v']
        
    if parallel:
        call_list += ['-1']
        
    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    call_list.append(str(output))
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
    """Return documentation on the 'wf3cte' function. Required by TEAL."""

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
    TEAL interface for the ``wf3cte`` function.

    """
    wf3cte(configobj['input'],
           parallel=configobj['parallel'],
           verbose=configobj['verbose'],)
           
wf3cte.__doc__ = getHelpAsString(docstring=True)
          
          
