"""
The wf3ir  processes IR images
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
    """Call the wf3ir.e executable """

    call_list = ['wf3ir.e']

    if verbose:
        call_list += ['-v','-t']

    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    call_list.append(str(output))
    
    subprocess.call(call_list)


def run(configobj=None):
    """
    TEAL interface for the ``wf3ir`` function.

    """
    wf3ir(configobj['input'],
           output=configobj['output'],
           quiet=configobj['quiet'],
           verbose=configobj['verbose'],)
           

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


def help(file=None):
    """
    Print out syntax help for running wf3ir
    
    """
        
    helpstr = getHelpAsString(docstring=True)
    if file is None:
        print helpstr
    else:
        if os.path.exists(file): os.remove(file)
        f = open(file,mode='w')
        f.write(helpstr)
        f.close()
    



wf3ir.__doc__ = getHelpAsString(docstring=True)

           
