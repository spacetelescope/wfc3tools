============
pstat
============

Plot statistics for a specified image section  up  the  stack  of  a
an IR MultiAccum image.  Sections from any of the SCI,
ERR, DQ,  image extensions can be  plotted.   A  choice
of  mean,  median,  mode,  standard  deviation,  minimum and maximum
statistics is available.  The total number of samples is  determined
from  the  primary  header  keyword NSAMP and all samples (excluding
the zeroth-read) are plotted.  The SCI, ERR, DQ  statistics
are  plotted as a function of sample time. The sample times  are  read
from  the  SAMPTIME  keyword in the SCI header for each readout.  

SAMP and TIME aren't generally populated until the FLT image stage
To plot the samptime vs sample, use wfc3tools.pstat and the "time" extension

The plotting data is returned as two arrays


Parameters
----------
    
    filename [file]
        Input   MultiAccum   image  name  with  optional  image  section 
        specification.  If no image section  is  specified,  the  entire
        image  is  used.   This  should  be  either a _raw or _ima file,
        containing all  the  data  from  multiple  readouts.   You  must
        specify  just  the  file name and image section, with no extname
        designation.
    

    extname = "sci" [string, allowed values: sci | err | dq ]
        Extension name (EXTNAME keyword value) of data to plot.
    
    units = "counts" [string, allowed values: counts | rate]
        Plot "sci" or  "err"  data  in  units  of  counts  or  countrate
        ("rate").   Input data can be in either unit; conversion will be
        performed automatically.  Ignored when  plotting  "dq",  "samp",
        or "time" data.
    
    stat = "midpt" [string, allowed values: mean|midpt|mode|stddev|min|max]
       Type of statistic to compute.
        
    title = "" [string]
       Title  for  the  plot.   If  left  blank,  the name of the input
       image, appended with the extname and image section, is used.
    
    xlabel = "" [string]
       Label for the X-axis of the plot.  If  left  blank,  a  suitable
       default is generated.
    
    ylabel = "" [string]
       Label  for  the  Y-axis  of  the plot. If left blank, a suitable
       default based on the plot units and the extname of the  data  is
       generated.
    

Usage
-----

    pstat.py  inputFilename [pixel range]


    >>> python
    >>> from wfc3tools import pstat
    >>> pstat.pstat(inputFilename, pixel=None)


