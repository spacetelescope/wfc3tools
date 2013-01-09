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

Examples
--------

    In Python without TEAL:

    >>> from wfc3tools import wf3ccd
    >>> calwf3.wf3ccd(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3ccd
    >>> teal.teal('wf3ccd')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3ccd

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
    
__taskname__ = "wf3ccd"
__version__ = "1.0"
__vdate__ = "03-Jan-2013"

def wf3ccd(input, output="", dqicorr="PERFORM", atodcorr="PERFORM",blevcorr="PERFORM",
        biascorr="PERFORM", flashcorr="PERFORM", verbose=False, quiet=True ):
    """
    
    Run the ``wf3ccd.e`` executable as from the shell. For more information on CALWF3
    see the WFC3 Data Handbook at http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/


    Parameters:

        input : str
            Name of input files

                * a single filename (``iaa012wdq_raw.fits``)
                * a Python list of filenames
                * a partial filename with wildcards (``\*raw.fits``)
                * filename of an ASN table (``\*asn.fits``)
                * an at-file (``@input``) 

        output: str
            Name of the output FITS file.

        dqicorr: str, "PERFORM/OMIT", optional
            Update the dq array from bad pixel table

        atodcorr: str, "PERFORM/OMIT", optional
            Analog to digital correction

        blevcorr: str, "PERFORM/OMIT", optional
            Subtract bias from overscan regions

        biascorr: str, "PERFORM/OMIT", optional
            Subtract bias image

        flashcorr: str, "PERFORM/OMIT", optional
            Subtract post-flash image

        verbose: bool, optional
            Print verbose time stamps?

        quiet: bool, optional
            Print messages only to trailer file?
        
  
    """
    call_list = ['wf3ccd.e']

    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    
    if verbose:
        call_list.append('-v -t')

 
        
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


def getHelpAsString():
    """
    Returns documentation on the ``wf3ccd`` function. Required by TEAL.

    """
    return wf3ccd.__doc__


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
           
           
          
