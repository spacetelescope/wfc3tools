# STDLIB
from astropy.io import fits
import os
import numpy as np

# STSCI
from stsci.tools import parseinput

__taskname__ = "sampinfo"


def sampinfo(imagelist, add_keys=None, mean=False, median=False):
    """ Print information for each sample in the image.

    Parameters
    ----------
    imagelist: list
        The input can be a single image or list of images
    add_keys: list
        A list of of additional keys for printing
    mean: bool
        print the mean statistic
    median: bool
        print the median statistic

    """

    datamin = False
    datamax = False
    imlist = parseinput.parseinput(imagelist)

    # the default list of keys to print, regardless of detector type
    ir_list = ["SAMPTIME", "DELTATIM"]
    if add_keys:
        ir_list += add_keys

    # measure the min and max data
    if (mean):
        if (add_keys):
            if ("DATAMIN" not in add_keys):
                ir_list += ["DATAMIN"]
            if ("DATAMAX" not in add_keys):
                ir_list += ["DATAMAX"]
        else:
            ir_list += ["DATAMIN", "DATAMAX"]

    for image in imlist[0]:
        current = fits.open(image)
        header0 = current[0].header
        nextend = header0["NEXTEND"]
        try:
            nsamp = header0["NSAMP"]
        except KeyError as e:
            print(str(e))
            print("Task good for IR data only")
            break
        exptime = header0["EXPTIME"]
        samp_seq = header0["SAMP_SEQ"]

        print("IMAGE\t\t\tNEXTEND\tSAMP_SEQ\tNSAMP\tEXPTIME")
        print("%s\t%d\t%s\t\t%d\t%f\n" % (image, nextend, samp_seq,
                                          nsamp, exptime))
        printline = "IMSET\tSAMPNUM"

        for key in ir_list:
                printline += ("\t"+key)
        print(printline)

        # loop through all the samples for the image and print stuff as we go
        for samp in range(1, nsamp+1, 1):
            printline = ""
            printline += str(samp)
            printline += ("\t"+str(nsamp-samp))
            for key in ir_list:
                if "DATAMIN" in key:
                    datamin = True
                    dataminval = np.min(current["SCI", samp].data)
                if "DATAMAX" in key:
                    datamax = True
                    datamaxval = np.min(current["SCI", samp].data)
                try:
                    printline += ("\t"+str(current["SCI", samp].header[key]))
                except KeyError:
                    try:
                        printline += ("\t"+str(current[0].header[key]))
                    except KeyError as e:
                        printline += ("\tNA")
            if (datamin and datamax):
                printline += ("\tAvgPixel: "+str((dataminval+datamaxval)/2.))
            if (median):
                printline += ("\tMedPixel: "+str(np.median(current["SCI",
                                                           samp].data)))
            print(printline)
        current.close()
