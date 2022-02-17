# STDLIB
import os
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt

__taskname__ = "pstack"

plt.ion()

def pstack(filename, column=0, row=0, extname="sci", units="counts",
           title=None, xlabel=None, ylabel=None, plot=True):
    """A function  to plot the statistics of one pixels up the IR ramp  image
    Original implementation in the iraf nicmos package. Pixel values here are
    0 based, not 1 based """

    time = False
    valid_ext = ["sci", "err", "dq", "time"]
    if extname.lower() not in valid_ext:
        print("Invalid value given for extname")
        return 0, 0

    with fits.open(filename) as myfile:
        nsamp = myfile[0].header["NSAMP"]
        bunit = myfile[1].header["BUNIT"]  # must use data header for units
        yaxis = np.zeros(nsamp)

        # plots versus sample for TIME extension
        if "time" in extname.lower():
            xaxis = np.arange(nsamp) + 1
            time = True
        else:
            xaxis = np.zeros(nsamp)

        for i in range(1, nsamp, 1):
            if time:
                yaxis[i-1] = myfile["SCI", i].header['SAMPTIME']
            else:
                yaxis[i-1] = myfile[extname.upper(), i].data[column, row]
                xaxis[i-1] = myfile["SCI", i].header['SAMPTIME']

                # convert to countrate
                if "rate" in units.lower() and "/" not in bunit.lower():
                    exptime = myfile["SCI", i].header['SAMPTIME']
                    yaxis[i-1] /= exptime
                # convert to counts
                if "counts" in units.lower() and "/" in bunit.lower():
                    exptime = myfile["SCI", i].header['SAMPTIME']
                    yaxis[i-1] *= exptime

    if not ylabel:
        if "rate" in units.lower():
            if "/" in bunit.lower():
                ylabel = bunit
            else:
                ylabel = bunit+" per second"
        else:
            if "/" in bunit:
                stop_index = bunit.find("/")
                ylabel = bunit[:stop_index]
            else:
                ylabel = bunit
    if plot:
        plt.clf()
        plt.ylabel(ylabel)

        if not xlabel and time:
            plt.xlabel("Sample Number")
        if not xlabel and not time:
            plt.xlabel("Sample time")

        if not title:
            title = "%s   Pixel stack for col=%d, row=%d" % (filename, column,
                                                             row)
        plt.title(title)

        if time:
            plt.xlim(np.max(xaxis), np.min(xaxis))
            plt.ylabel("Seconds")

        plt.plot(xaxis, yaxis, "+")
        plt.draw()

    return xaxis, yaxis
