"""
wf3rej contains the Cosmic Ray rejection and shading correction processing steps for  the WFC3 UVIS and IR data. These steps are:

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
    helpstr = _getHelpAsString(docstring=True)
    if file is None:
        print helpstr
    else:
        if os.path.exists(file): os.remove(file)
        f = open(file,mode='w')
        f.write(helpstr)
        f.close()
    

def _getHelpAsString(docstring=False):
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
           
           
#This replaces the help for the function which is also printed in the HTML and TEAL
wf3rej.__doc__ = _getHelpAsString(docstring=True)
