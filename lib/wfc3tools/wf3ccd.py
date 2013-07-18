"""
The wfc3tools module contains a function ``wf3ccd`` that calls the wf3ccd executable.
Use this function to facilitate batch runs or for the TEAL interface.

This routine contains the initial processing steps for all the WFC3 UVIS channel data. These steps are:

    * dqicorr - initializing the data quality array
    * atodcorr - perform the a to d conversion correction
    * blevcorr - subtract the bias level from the overscan region
    * biascorr - subtract the bias image
    * flshcorr - subtract the post-flash image
    
If blevcorr is performed the output contains the overcan-trimmed region.
  
Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Example
-------

    In Python without TEAL:

    >>> from wfc3tools import wf3ccd
    >>> wf3ccd.wf3ccd(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3ccd
    >>> teal.teal('wf3ccd')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3ccd

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
    
__taskname__ = "wf3ccd"
__vdate__ = "03-Jan-2013"

def wf3ccd(input, output="", dqicorr="PERFORM", atodcorr="PERFORM",blevcorr="PERFORM",
        biascorr="PERFORM", flashcorr="PERFORM", verbose=False, quiet=True ):
    
    """Run the ``wf3ccd.e`` executable as from the shell. For more information on CALWF3 """

    call_list = ['wf3ccd.e']

    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    call_list += ["output",output]
    
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
    Returns documentation on the 'wf3ccd' function. Required by TEAL.

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


wf3ccd.__doc__ = getHelpAsString(docstring=True)


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
           
           
          
