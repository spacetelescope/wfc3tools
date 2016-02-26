"""
wf3ccd  calls the wf3ccd executable and contains the initial processing steps for all the WFC3 UVIS channel data.
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
    
__taskname__ = "wf3ccd"
__vdate__ = "03-Jan-2013"

def wf3ccd(input, output="", dqicorr="PERFORM", atodcorr="PERFORM",blevcorr="PERFORM",
        biascorr="PERFORM", flashcorr="PERFORM", verbose=False, quiet=True ):
    
    """Run the ``wf3ccd.e`` executable as from the shell."""

    call_list = ['wf3ccd.e']
    
    if verbose:
        call_list += ['-v','-t']
        
    if (dqicorr == "PERFORM"):
        call_list.append('-dqi')
    
    if (atodcorr == "PERFORM"):
        call_list.append('-atod')
        
    if (blevcorr == "PERFORM"):
        call_list.append('-blev')
        
    if (biascorr == "PERFORM"):
        call_list.append('-bias')
        
    if (flashcorr == "PERFORM"):
        call_list.append('-flash')

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
    TEAL interface for the ``wf3ccd`` function.

    """
    wf3ccd(configobj['input'],
           output=configobj['output'],
           dqicorr=configobj['dqicorr'],
           atodcorr=configobj['atodcorr'],
           blevcorr=configobj['blevcorr'],
           biascorr=configobj['biascorr'],
           flashcorr=configobj['flashcorr'],
           quiet=configobj['quiet'],
           verbose=configobj['verbose'],)
           
wf3ccd.__doc__ = getHelpAsString(docstring=True)
          
          
