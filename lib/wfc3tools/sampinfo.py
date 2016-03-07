from __future__ import absolute_import, print_function, division

#get the auto update version for the call to  help
from .version import __version__,__vdate__

# STDLIB
from astropy.io import fits
import os,sys
import numpy as np

#STSCI
from stsci.tools import parseinput
from stsci.tools import teal
        
__taskname__ = "sampinfo"

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


    

sampinfo.__doc__ = getHelpAsString(docstring=True)

