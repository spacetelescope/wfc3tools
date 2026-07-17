"""Run wf3rej step in calwf3."""

import os.path
import subprocess

from stsci.tools import parseinput

from .util import error_code

__all__ = ["wf3rej"]


def wf3rej(
    input,
    output,
    crrejtab="",
    scalense=0.0,
    initgues="",
    skysub="",
    crsigmas="",
    crradius=0.0,
    crthresh=0.0,
    badinpdq=0,
    crmask=False,
    shadcorr=False,
    verbose=False,
    log_func=print,
):
    """
    Combines CR-SPLIT or REPEAT-OBS exposures into a single image, first
    detecting and then replacing flagged pixels.

    In summary, the cosmic ray rejection task sums all non-rejected pixel
    values, computes the true exposure time for that pixel, and scales the sum
    to correspond to the total exposure time. The final scaled, cleaned pixel
    is written to the comparison image to be used for the next iteration. This
    process is then repeated with increasingly stringent detection thresholds,
    as specified by CRSIGMAS.

    Parameters
    ----------
    input : str or list
        Name of input files, such as:

        - comma-separated (no spaces) filenames (``iaao01k8q_flc.fits,iaao01k9q_flc.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``*flt.fits``)
        - an at-file (``@input``)

    output : str
        Name of the output FITS file.

    crrejtab : str, optional
        Reference file name. Default is empty string.

    scalense : float, optional
        Scale factor applied to noise. Default is 0.

    initgues : str, optional
        Initial value estimate scheme (min|med).
        Default is empty string.

    skysub : str, optional
        How to compute the sky (none|mode|mean).
        Default is empty string.

    crsigmas : str, optional
        Rejection levels (float) in each iteration.
        Default is empty string.

    crradius : float, optional
        Cosmic ray expansion radius in pixels.
        Default is 0.

    crthresh : float, optional
        Rejection propagation threshold. Default is 0.

    badinpdq : int, optional
        Data quality flag bits to reject. Default is 0.

    crmask : bool, optional
        If `True`, flag CR in DQ extension of the input images.
        If `False`, the value of crmask is read from the CRREJTAB
        file and used as the specification. Default is `False`.

    shadcorr : bool, optional
        If `True`, perform shading shutter correction.
        Default is `False` (read from SHADCORR keyword value
        in primary header of first image to process).

    verbose : bool, optional
        If `True`, print verbose time stamps. Default is `False`.

    log_func : func
        By default, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Examples
    --------
    >>> from wfc3tools import wf3rej
    >>> from glob import glob
    >>> infiles = glob("*flt.fits")
    >>> wf3rej(infiles, "output.fits", verbose=True)
    >>> wf3rej([filename1, filename2], "output.fits", verbose=True)
    >>> wf3rej("*flt.fits", "output.fits", verbose=True)
    >>> wf3rej("@input.lst", "output.fits", verbose=True)
    """

    call_list = ["wf3rej.e"]
    return_code = None

    infiles, dummy = parseinput.parseinput(input)

    for image in infiles:
        if not os.path.exists(image):
            raise IOError("Input file not found: {0}".format(image))

    # Generate a comma-separated string of the input filenames
    input = ",".join(infiles)

    call_list.append(input)

    if output:
        call_list.append(str(output))

    if verbose:
        call_list.append("-v")
        call_list.append("-t")

    if shadcorr:
        call_list.append("-shadcorr")

    if crmask:
        call_list.append("-crmask")

    if crrejtab != "":
        call_list += ["-table", crrejtab]

    if scalense != "":
        call_list += ["-scale", str(scalense)]

    if initgues != "":
        options = ["min", "med"]
        if initgues not in options:
            raise ValueError("Invalid option for initgues")
        else:
            call_list += ["-init", str(initgues)]

    if skysub != "":
        options = ["none", "mode", "median"]
        if skysub not in options:
            raise ValueError(f"Invalid skysub option {options}: {skysub}")
        else:
            call_list += ["-sky", str(skysub)]

    if crsigmas != "":
        call_list += ["-sigmas", str(crsigmas)]

    if crradius >= 0.0:
        call_list += ["-radius", str(crradius)]
    else:
        raise ValueError("Invalid crradius specified")

    if crthresh >= 0.0:
        call_list += ["-thresh", str(crthresh)]
    else:
        raise ValueError("Invalid crthresh specified")

    if badinpdq >= 0:
        call_list += ["-pdq", str(badinpdq)]

    else:
        raise ValueError("Invalid DQ value specified")

    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode("utf8"))

    return_code = proc.wait()
    ec = error_code(return_code)
    if return_code:
        if ec is None:
            raise RuntimeError(f"wf3rej.e exited with unknown return code {return_code}.")
        raise RuntimeError(f"wf3rej.e exited with return code {ec}.")
