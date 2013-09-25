"""
This routine contains the Cosmic Ray rejection and shading correction processing steps for  the WFC3 UVIS and IR data. These steps are:

* crcorr - initializing the data quality array

If blevcorr is performed the output contains the overcan-trimmed region.

Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.


Example


In Python without TEAL:

>>> from wfc3tools import wf3rej
>>> wf3rej.wf3rej(filename)

In Python with TEAL:

>>> from stsci.tools import teal
>>> from wfc3tools import wf3rej
>>> teal.teal('wf3rej')

In Pyraf:

>>> import wfc3tools
>>> epar wf3rej

Parameters


input : str, Name of input files

      - a single filename (``iaa012wdq_raw.fits``)
      - a Python list of filenames
      - a partial filename with wildcards (``\*raw.fits``)
      - filename of an ASN table (``\*asn.fits``)
      - an at-file (``@input``) 

output : str, Name of the output FITS file.

crrejtab : string, reference file name

scalense :   string, scale factor applied to noise

initgues :   string, intial value estimate scheme (min|med)

skysub :     string, how to compute the sky (none|mode|mean)

crsigmas :   string, rejection levels in each iteration

crradius :   float, cosmic ray expansion radius in pixels

crthresh :   float, rejection propagation threshold

badinpdq :   int, data quality flag bits to reject

crmask :     bool, flag CR in input DQ imageS?

shadcorr :   bool, perform shading shutter correction?

verbose : bool, optional,  Print verbose time stamps?



"""
# STDLIB
import os.path
import subprocess

#get the auto update version for the call to teal help
from .version import *

#STSCI
from stsci.tools import parseinput
try:
    from stsci.tools import teal
except:
    teal = None

__taskname__ = "wf3rej"
__vdate__ = "12-Jul-2013"

def wf3rej(input, output="", crrejtab="", scalense="", initgues="",
    skysub="", crsigmas="", crradius=0, crthresh=0, 
    badinpdq=0, crmask=False, shadcorr=False, verbose=False):
    """call the calwf3.e executable"""

    call_list = ["wf3rej.e"]

    infiles, dummy_out= parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    call_list.append(str(output))
    
    if verbose:
        call_list += ["-v","-t"]
            
    if (shadcorr):
        call_list += ["-shadcorr"]
    
    if (crmask):
        call_list += ["-crmask"]
        
    if (crrejtab != ""):
        call_list += ["-table",crrejtab]
        
    if (scalense != ""):
        call_list += ["-scale",str(scalense)]
    
    if (initgues != ""):
        options=["min","med"]
        if initgues not in options:
            print "Invalid option for intigues"
            return ValueError
        else:
            call_list += ["-init",str(initgues)]
    
    if (skysub != ""):
        options=["none","mode","median"]
        if skysub not in options:
            print(("Invalid skysub option: %s")%(skysub))
            print(options)
            return ValueError
        else:
            call_list += ["-sky",str(skysub)]
                
    
    if (crsigmas != ""):
        call_list += ["-sigmas",str(crsigmas)]
        
    if (crradius >= 0.):
        call_list += ["-radius",str(crradius)]
    else:
        print("Invalid crradius specified")
        return ValueError
    
    if (crthresh >= 0.):
        call_list += ["-thresh",str(crthresh)]
    else:
        print("Invalid crthresh specified")
        return ValueError
        
    if (badinpdq >= 0):
        call_list += ["-pdq",str(badinpdq)]
        
    else:
        print("Invalid DQ value specified")
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
    """Returns documentation on the 'wf3rej' function. Required by TEAL.

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


#This replaces the help for the function which is also printed in the HTML and TEAL
wf3rej.__doc__ = getHelpAsString(docstring=True)

def run(configobj=None):
    """TEAL interface for the ``wf3rej`` function."""

    wf3rej(configobj['input'],
           output=configobj['output'],
           crrejtab=configobj['crrejtab'],
           scalense=configobj['scalense'],
           initgues=configobj['initgues'],
           skysub=configobj['skysub'],
           crsigmas=configobj['crsigmas'],
           crradius=configobj['crradius'],
           crthresh=configobj['crthresh'],
           badinpdq=configobj['badinpdq'],
           crmask=configobj['crmask'],
           shadcorr=configobj['shadcorr'],
           verbose=configobj['verbose'],)
           
           
