"""
The wfc3tools module contains a function ``wf3rej`` that calls the wf3rej executable.
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

    >>> from wfc3tools import wf3rej
    >>> calwf3.wf3rej(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3rej
    >>> teal.teal('wf3rej')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3rej

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
    
__taskname__ = "wf3rej"
__vdate__ = "12-Jul-2013"

def wf3rej(input, output="", crrejtab="", scalense="", initgues="",
    skysub="", crsigmas="", crradius=-1, crthresh=-1, 
    badinpdq=-1, crmask=False, shadcorr=False, verbose=False):
    """
    
    Run the ``wf3rej.e`` executable as from the shell. For more information on CALWF3
    see the WFC3 Data Handbook at http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/


    Parameters:
    
        * input : str, Name of input files

                - a single filename (``iaa012wdq_raw.fits``)
                - a Python list of filenames
                - a partial filename with wildcards (``\*raw.fits``)
                - filename of an ASN table (``\*asn.fits``)
                - an at-file (``@input``) 

        * output: str, Name of the output FITS file.

        * crrejtab: string, reference file name

        * scalense:   string, scale factor applied to noise

        * initgues:   string, intial value estimate scheme (min|med)

        * skysub:     string, how to compute the sky (none|mode|mean)

        * crsigmas:   string, rejection levels in each iteration

        * crradius:   float, cosmic ray expansion radius in pixels

        * crthresh:   float, rejection propagation threshold

        * badinpdq:   int, data quality flag bits to reject

        * crmask:     bool, flag CR in input DQ imageS?

        * shadcorr:   bool, perform shading shutter correction?

        * verbose: bool, optional,  Print verbose time stamps?

        
  
    """
    call_list = ["wf3rej.e"]

    infiles, dummpy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    
    if verbose:
        call_list.append("-v -t")
    
    if (shadcorr):
        call_list.append("-shadcorr")
    
    if (crmask):
        call_list.append("-crmask")
        
    if (crrejtab != ""):
        call_list.append(("-table %s")%(crrejtab))
        
    if (scalense != ""):
        call_list.append(("-scale %s")%(scalense))
    
    if (initgues != ""):
        options=["min","med"]
        for item in options:
            if item not in initgues:
                print "Invalid option for intigues"
                return ValueError
            else:
                call_list.append(("-init %s")%(initgues))
    
    if (skysub != ""):
        options=["none","mode","median"]
        for item in options:
            if item not in skysub:
                printf(("Invalid skysub option: %s")%(skysub))
                printf(options)
                return ValueError
            else:
                call_list.append(("-sky %s")%(skysub))
    
    if (crsigmas != ""):
        call_list.append(("-sigmas %s")%(crsigmas))
        
    if (crradius >= 0.):
        call_list.append(("-radius %f")%(crradius))
    else:
        printf("Invalid crradius specified")
        return ValueError
    
    if (crthresh >= 0.):
        call_list.append(("-thresh %f")%(crthresh))
    else:
        printf("Invalid crthresh specified")
        return ValueError
        
    if (badindq >= 0):
        call_list.append(("-pdq %d")%(badindq))
        
    else:
        printf("Invalid DQ value specified")
        return ValueError
 

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
    Returns documentation on the 'wf3rej' function. Required by TEAL.

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


wf3rej.__doc__ = getHelpAsString(docstring=True)

def run(configobj=None):
    """
    
    TEAL interface for the ``wf3rej`` function.

    """
    wf3rej(configobj['input'],
           output=configobj['output'],
           crrejtab=configobj['crrejtab'],
           scalense=configobj['scalense'],
           initgues=configobj['initgues'],
           skysub=configobj['skysub'],
           crsigmas=configobj['crsigmas'],
           crradois=configobj['crradois'],
           crthresh=configobj['crthresh'],
           badinpdq=configobj['badinpdq'],
           crmask=configobj['crmask'],
           shadcorr=configobj['shadcorr'],
           verbose=configobj['verbose'],)
           
           
