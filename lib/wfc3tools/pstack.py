""" 
pstack


Plot the stack of MultiAccum sample values for a specified pixel  in
IR multiaccum image.  Pixels from any of the SCI, ERR, DQ, or TIME image 
extensions can be plotted.  The total number  of
samples  is determined from the primary header keyword NSAMP and all
samples (excluding the zeroth read) are plotted.  The SCI, ERR,  DQ,
values are plotted as a function of sample time, while TIME
values are plotted as a  function  of  sample  number.   The  sample
times  are read from the SAMPTIME keyword in the SCI header for each
readout. If any of the ERR, DQ, SAMP, or TIME extensions have  null
data  arrays,  the value of the PIXVALUE extension header keyword is
substituted for the pixel values.  The plotted data  values  can  be
saved to an output text table or printed to the terminal.

The BUNIT keyword value is used to determine the starting units of the data.

pstack returns the x and y arrays plotted


Parameters
    
    input [file]
        Input MultiAccum image name.  This should be either  a  _ima  or
        _raw  file, containing all the data from multiple readouts.  You
        must specify just the file name, with no extension designation.
    
    col [integer]
        The column index of the pixel to be plotted.
    
    row [integer]
        The row index of the pixel to be plotted.
    
    extname = "sci" [string, allowed values: sci | err | dq | samp | time]
       Extension name (EXTNAME keyword value) of data to plot.
    
    units = "counts" [string, allowed values: counts | rate]
       Plot "sci" or  "err"  data  in  units  of  counts  or  countrate
       ("rate").   Input data can be in either unit; conversion will be
       performed automatically.  Ignored when  plotting  "dq",  "samp",
       or "time" data.
        
    title = "" [string]
       Title  for  the  plot.   If  left  blank,  the name of the input
       image, appended with  the  extname  and  column  and  row  being
       plotted, is used.
    
    xlabel = "" [string]
       Label  for  the  X-axis  of the plot.  If left blank, a suitable
       default is generated.
    
    ylabel = "" [string]
       Label for the Y-axis of the plot.  If  left  blank,  a  suitable
       default  based  on the plot units and the extname of the data is
       generated.

USAGE: 


    python
    from wfc3tools import pstack
    xdata,ydata=pstack.pstack(inputFilename,column=x,row=y,extname="sci",units="counts|rate",title="",ylabel="",xlabel="")


"""
from __future__ import division # confidence high
from __future__ import print_function #confidence high

#get the auto update version 
from .version import *

# STDLIB
import os
import pyfits
import numpy as np
import matplotlib.pyplot as plt
from stsci.tools import teal

__taskname__ = "pstack"
__vdate__ = "06-Sep-2013"


def pstack(filename,column=0,row=0,extname="sci",units="counts",title=None,xlabel=None,ylabel=None):
    """A fucntion to plot the statistics of one or more pixels up the IR ramp  image
    Original implementation in the iraf nicmos package. Pixel values here are 0 based, not 1 based """


    time=False

    valid_ext=["sci","err","dq","time"]
    if extname.lower() not in valid_ext:
        print("Invalid value given for extname")
        return 0,0
    
    
    with pyfits.open(filename) as myfile:
        nsamp=myfile[0].header["NSAMP"]
        bunit=myfile[1].header["BUNIT"] #must look in a data header for units
        yaxis=np.zeros(nsamp)

        #plots versus sample for TIME extension
        if "time" in extname.lower():
            xaxis=np.arange(nsamp) +1
            time=True
        else:
            xaxis=np.zeros(nsamp)
        
        for i in range(1,nsamp,1):
            if time:
                yaxis[i-1]=myfile["SCI",i].header['SAMPTIME']  
            else:
                yaxis[i-1]=myfile[extname.upper(),i].data[column,row]  #y is always the data value   
                xaxis[i-1]= myfile["SCI",i].header['SAMPTIME']  #plot vs time for most samps
                
                #convert to countrate     
                if "rate" in units.lower() and "/" not in bunit.lower():
                    exptime=myfile["SCI",i].header['SAMPTIME']
                    yaxis[i-1] /= exptime
                #convert to counts
                if "counts" in units.lower() and "/" in bunit.lower():
                    exptime=myfile["SCI",i].header['SAMPTIME']
                    yaxis[i-1] *= exptime
                
    if not ylabel:
        if "rate" in units.lower():
            if "/" in bunit.lower():
                ylabel=bunit
            else:
                ylabel=bunit+" per second"
        else:
            if "/" in bunit:
                stop_index=bunit.find("/")
                ylabel=bunit[:stop_index]
            else:
                ylabel=bunit
                         
    plt.clf() #clear out any current plot
    plt.ylabel(ylabel)

        
        
    if not xlabel and time:
        plt.xlabel("Sample Number")
    if not xlabel and not time:
        plt.xlabel("Sample time")

    if not title:
        title="%s   Pixel stack for col=%d, row=%d"%(filename,column,row)
    plt.title(title)

    if time:
        plt.xlim(np.max(xaxis),np.min(xaxis))
        plt.ylabel("Seconds")
        
    plt.plot(xaxis,yaxis,"+")
        
    return xaxis,yaxis




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

