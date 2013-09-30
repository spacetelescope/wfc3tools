============
pstack
============

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
----------    
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

    plot = True [bool]  set plot to false if you only want the data returned

Usage: 
------

    python
    from wfc3tools import pstack
    xdata,ydata=pstack.pstack(inputFilename,column=x,row=y,extname="sci",units="counts|rate",title="",ylabel="",xlabel="")


