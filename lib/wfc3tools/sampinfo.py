""" 

sampinfo


Sampinfo prints information about a  WFC3/IR  MultiAccum image,  including  exposure  time  information  for  the  individual samples (readouts).  
The global information listed  (and  the  names of  the  header  keywords  from  which it is retrieved) includes:
    - the total number of image extensions in the file (NEXTEND)
    - the name  of the  MultiAccum  exposure  sample  sequence  (SAMP_SEQ)
    - the  total number of samples, including the  "zeroth"  read  (NSAMP)
    - the total  exposure  time of the observation (EXPTIME). 
    
Information that is listed for each sample is the IMSET number (EXTVER),  the  sample number  (SAMPNUM),  the  sample time, which is the total accumulated exposure time for a sample (SAMPTIME), 
and the delta time, which  is the  additional  exposure time accumulated since the previous sample (DELTATIM).

Note that the samples of a MultiAccum exposure  are  stored  in  the FITS  file  in  reverse  time  order. The initial, or "zeroth" read, appears  last  in  the  FITS  file,  
with  IMSET=NSAMP,   SAMPNUM=0, SAMPTIME=0,  and  DELTATIM=0. The final read of the exposure appears first in the file  and  has  IMSET=1,  SAMPNUM=NSAMP-1  (SAMPNUM  is zero-indexed), and SAMPTIME=EXPTIME.


Options:


This version will accept a single image name or a python list of images. The list of images should be a python style list, such as:
    >>> ["image1.fits","image2.fits"]

add_keys=list(): You can also supply a supplimental list of keywords to print for each sample, if the key isn't found in the sample the global header will be checked.If a key is not found the "NA" string will be printed. 
Additionally you can ask for the median or mean of the datavalues for each sample  using the appropriate switch.

median=False: Set to True in order to report the median pixel value for each sample

mean=False: Set to True in order to report the average pixel value for each sample (as measured with np.min and np.max)


USAGE: 


Typical:

    >>> python
    >>> from wfc3tools import sampinfo
    >>> sampinfo.sampinfo(imagename)

Where imagename can be a single filename or a python list() of names

To get the median value for each sample:

    >>> sampinfo.sampinfo(imagename, median=True)

To print additional keys for information:

    >>> sampinfo.sampinfo(imagename,add_keys=["DETECTOR"])

To get the average value for each sample:

    >>> sampinfo.sampinfo(imagename, mean=True)
    
"""
from __future__ import absolute_import, print_function, division

#get the auto update version for the call to  help
from .version import *

# STDLIB
from astropy.io import fits
import os,sys
import numpy as np

#STSCI
from stsci.tools import parseinput
from stsci.tools import teal
        
__taskname__ = "sampinfo"
__vdate__="Sep-16-2013"

def sampinfo(imagelist,add_keys=None,mean=False,median=False):
    """ The input can be a single image or list of images, add_keys should be a list() of additional keys"""

    datamin=False
    datamax=False
    imlist=parseinput.parseinput(imagelist)
    
    #the default list of keys to print, regardless of detector type
    
    ir_list=["SAMPTIME","DELTATIM"]
    if add_keys :
        ir_list+=add_keys
        
    #measure the min and max data
    if (mean):
        if (add_keys):
            if ("DATAMIN" not in add_keys):
                ir_list +=["DATAMIN"]    
            if ("DATAMAX" not in add_keys):
                ir_list +=["DATAMAX"]
        else:
            ir_list+=["DATAMIN","DATAMAX"]
               
    for image in imlist[0]:
        current=fits.open(image)
        header0=current[0].header
        nextend=header0["NEXTEND"]
        try:
            nsamp=header0["NSAMP"]
        except KeyError as e:
            print(str(e))
            print("Task good for IR data only")
            break
        exptime=header0["EXPTIME"]
        samp_seq=header0["SAMP_SEQ"]
        
        print("IMAGE\t\t\tNEXTEND\tSAMP_SEQ\tNSAMP\tEXPTIME")
        print("%s\t%d\t%s\t\t%d\t%f\n"%(image,nextend,samp_seq,nsamp,exptime))
        printline="IMSET\tSAMPNUM"
        
        for key in ir_list:
                printline+=("\t"+key)
        print(printline)
        
        #loop through all the samples for the image and print stuff as we go
        for samp in range(1,nsamp+1,1):
            printline=""
            printline+=str(samp)
            printline+=("\t"+str(nsamp-samp))
            for key in ir_list:
                if "DATAMIN" in key: 
                    datamin=True
                    dataminval=np.min(current["SCI",samp].data)
                if "DATAMAX" in key: 
                    datamax=True
                    datamaxval=np.min(current["SCI",samp].data)
                try:
                    printline+=("\t"+str(current["SCI",samp].header[key]))
                except KeyError:
                    try:
                        printline+=("\t"+str(current[0].header[key]))
                    except KeyError as e:
                        printline+=("\tNA")
            if (datamin and datamax):
                printline+=("\tAvgPixel: "+str((dataminval+datamaxval)/2.))     
            if (median):
                printline +=("\tMedPixel: "+str(np.median(current["SCI",samp].data)))        
            print(printline)
        current.close()

def getHelpAsString(docstring=False):
    """
    Returns documentation on the 'sampinfo' function.

    return useful help from a file in the script directory called
    __taskname__.help

    """

    install_dir = os.path.dirname(__file__)   
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    
    if docstring or (not docstring):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __vdate__]) + '\n\n'
    if os.path.exists(helpfile):
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
        
    return helpString
        
def help():
    print(getHelpAsString(docstring=True))


    

__doc__ = getHelpAsString(docstring=True)

