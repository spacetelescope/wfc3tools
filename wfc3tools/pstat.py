"""
pstat:

    Plot statistics for a specified image section up the stack of an IR
    MultiAccum image.  Sections from any of the SCI, ERR, DQ, image extensions
    can be plotted.  A choice of  mean, midpt (median), mode, standard deviation,
    minimum, and maximum statistics is available. The total number of samples is
    determined from the primary header keyword NSAMP and all samples (excluding
    the zeroth-read) are plotted. The SCI, ERR, DQ statistics are plotted as a
    function of sample time. The sample times are read from the SAMPTIME
    keyword in the SCI header for each readout.

    SAMP and TIME are not generally populated until the FLT image stage. To plot
    the samptime vs sample, use wfc3tools.pstat and the "time" extension.

    When specifying an image section, note the Python slicing rules are in play
    which means the valid data within the bounds of the start:stop values will be
    used for any computation.

Usage:

    >>> from wfc3tools import pstat
    >>> time, counts = pstat('ibh719grq_ima.fits', col_slice=(100, 104), row_slice=(20, 25), units="counts")
    >>> time
    array([ 100.651947,   93.470573,   86.2892  ,   79.107826,   71.926453,
             64.745079,   57.563702,   50.382328,   43.200954,   36.019581,
             28.838205,   21.65683 ,   14.475455,    7.29408 ,    0.112705,
              0.      ])
    >>> counts
    array([210.93391217,   210.3575491 ,   187.08969378,   181.75601219,
           151.43222828,   138.52899031,   116.67495111,   109.19263377,
            86.42073624,    80.97576756,    70.44724733,    53.37688116,
            33.1249918 ,    12.25499919,    -4.88105808,     0.        ])

.. Warning::

    Note that the arrays are structured in SCI order, so the final exposure is the first element in the array.

.. Warning::
    The interface to this utility has been updated from previous versions and 
    is **not backwards compatible.**  Here is an example to illustrate the "original"
    syntax, the "original syntax corrected for row/column order", and finally the
    "new" syntax which requires column and row sections to be specified as tuples.

    | Example: To plot the left edge of the detector

    | Original syntax: [y1:y2, x1:x2]
    | time, counts = pstat('ibohbfb9q_ima.fits[1:1014,100:300]')

    | Original syntax, but correcting the row/column order: [x1:x2, y1:y2]
    | time, counts = pstat('ibohbfb9q_ima.fits[100:300,1:1014]')

    | New syntax using tuples for col_slice and row_slice to specify the section:
    | time, counts = pstat('ibohbfb9q_ima.fits', col_slice=(100,300), row_slice=(1,1014))

"""

# STDLIB
import os
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import mode as mode

plt.ion()


def pstat(filename, col_slice=None, row_slice=None, extname="sci", units="counts",
          stat="midpt", title=None, xlabel=None, ylabel=None, plot=True, overplot=False):
    """
    A function to plot the statistics of one or more pixels up an IR ramp.

    Parameters
    ----------
    filename : str
       Input MultiAccum image filename.  This should be either a _raw or _ima file,
       containing all the data from multiple readouts.  Only the filename should be
       be specified (i.e., no image section or extension name).

    col_slice : tuple of ints, default = None
       A tuple representing the columns to be included as part of the analysis.
       The default value of None indicates use of all columns.

    row_slice : tuple of ints, default = None
       A tuple representing the rows to be included as part of the analysis.
       The default value of None indicates use of all rows.

    extname :  str, default="sci"
       Extension name (EXTNAME keyword value) of data to plot. Allowed values
       are "sci", "err", and "dq".

    units : str, default="counts"
       Plot "sci" or "err" data in units of counts or countrate
       ("rate").  Input data can be in either unit; conversion will be
       performed automatically.  Ignored when plotting "dq", "samp", or
       "time" data. Allowed values are "counts" and "rate".

    stat : str, default="midpt"
       Type of statistic to compute. Allowed values are "mean", "midpt",
       "mode", "stddev", "min", and "max".

    title : str, default=None
       Title for the plot.  If left blank, the name of the input image,
       appended with the extname and image section, is used.

    xlabel : str, default=None
       Label for the X-axis of the plot.  If left blank, a suitable default
       is generated.

    ylabel : str, default=None
       Label for the Y-axis of the plot. If left blank, a suitable default
       based on the plot units and the extname of the data is generated.

    plot : bool, default=True
       If False, return data and do not plot.

    overplot : bool, default=False
       If True, the results will be overplotted on the previous plot.

    Returns
    -------
    xaxis : numpy.ndarray
       Array of x-axis values that will be plotted.

    yaxis : numpy.ndarray
       Array of y-axis values that will be plotted as specified by 'units'.

    Notes
    -----
    Pixel values here are 0 based, not 1 based.


    Examples
    --------

    | Using an image section to generate output in counts
    | >>> from wfc3tools import pstat
    | >>> time, counts = pstat('ibh719grq_ima.fits', col_slice=(100, 104), row_slice=(20, 25), units="counts")

    | Using the entire image to generate output in countrate
    | >>> time, counts = pstat('ibh719grq_ima.fits', col_slice=None, row_slice=None, units="rate")

    """

    # ignore any image extension or section specified on the filename string
    # now that the extension and image section are specified via parameters
    bracket_loc = filename.find("[")

    # get the base filename and strip off any extra information as necessary
    if (bracket_loc < 0):
        imagename = filename
    elif (bracket_loc > 0):
        imagename = filename[:bracket_loc]
        print("Any extension name or image section must be specified via parameters.")
        print("Input filename has been stripped of data in brackets, %s" % (imagename))

    # check for a valid stat value
    valid_stats = ["midpt", "mean", "mode", "stddev", "min", "max"]
    if stat not in valid_stats:
        print("Invalid value given for stat: %s" % (valid_stats))
        return 0, 0

    valid_ext = ["sci", "err", "dq"]
    if extname.lower() not in valid_ext:
        print("Invalid value given for extname: %s" % (valid_ext))
        return 0, 0

    # check on image section specification
    all_cols = False
    if not col_slice:
        all_cols = True
    elif not(isinstance(col_slice, tuple) and len(col_slice) == 2 and all(isinstance(val, int) for val in col_slice)):
        print("Invalid specification for col_slice which must be a tuple of two integer values.")
        return 0, 0

    all_rows = False
    if not row_slice:
        all_rows = True
    elif not(isinstance(row_slice, tuple) and len(row_slice) == 2 and all(isinstance(val, int) for val in row_slice)):
        print("Invalid specification for row_slice which must be a tuple of two integer values.")
        return 0, 0

    # open the file and get the data
    with fits.open(imagename) as myfile:
        nsamp = myfile[0].header["NSAMP"]
        bunit = myfile[1].header["BUNIT"]  # must look at header for units
        yaxis = np.zeros(nsamp)
        xaxis = np.zeros(nsamp)

        xsize = myfile[1].header["NAXIS1"]  # full x size
        ysize = myfile[1].header["NAXIS2"]  # full y size

        # set the start and end of the image section -- Python slicing rules apply
        if all_cols:
            xstart = 0
            xend = xsize
        else:
            xstart = col_slice[0]
            xend = col_slice[1]

        if all_rows:
            ystart = 0
            yend = ysize
        else:
            ystart = row_slice[0]
            yend = row_slice[1]

        for i in range(1, nsamp, 1):
            if "midpt" in stat:
                yaxis[i-1] = np.median(myfile[extname.upper(), i].data[ystart:yend, xstart:xend])

            if "mean" in stat:
                yaxis[i-1] = np.mean(myfile[extname.upper(), i].data[ystart:yend, xstart:xend])

            if "mode" in stat:
                yaxis[i-1] = mode(myfile[extname.upper(), i].data[ystart:yend, xstart:xend],
                                  axis=None)[0]

            if "min" in stat:
                yaxis[i-1] = np.min(myfile[extname.upper(), i].data[ystart:yend, xstart:xend])

            if "max" in stat:
                yaxis[i-1] = np.max(myfile[extname.upper(), i].data[ystart:yend, xstart:xend])

            if "stddev" in stat:
                yaxis[i-1] = np.std(myfile[extname.upper(), i].data[ystart:yend, xstart:xend])

            exptime = myfile["SCI", i].header['SAMPTIME']
            xaxis[i-1] = exptime

            # convert to countrate
            if "rate" in units.lower() and "/" not in bunit.lower():
                yaxis[i-1] /= exptime
            # convert to counts
            if "counts" in units.lower() and "/" in bunit.lower():
                yaxis[i-1] *= exptime

    if plot:
        if not overplot:
            plt.clf()  # clear out any current plot
        if not ylabel:
            if "rate" in units.lower():
                if "/" in bunit.lower():
                    ylabel = bunit
                else:
                    ylabel = bunit + " per second"
            else:
                if "/" in bunit:
                    stop_index = bunit.find("/")
                    ylabel = bunit[:stop_index]
                else:
                    ylabel = bunit

        ylabel += ("   %s" % (stat))
        plt.ylabel(ylabel)

        if not xlabel:
            plt.xlabel("Sample time (s)")

        if not title:
            title = "%s   Pixel stats for [%d:%d,%d:%d]" % (imagename, xstart,
                                                            xend, ystart, yend)
        plt.title(title)
        plt.plot(xaxis, yaxis, "+")
        plt.draw()

    return xaxis, yaxis
