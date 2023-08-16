"""
wf3rej:

    Background discussion on the wf3rej algorithm can be found in the following locations:
    https://wfc3tools.readthedocs.io/en/latest/wfc3tools/wf3rej.html, and Section 3.4.5 of
    the WFC3 Data Handbook.

    This routine performs the cosmic ray rejection on input FLT/FLC images and will
    produce an output CRJ/CRC image.  In contrast to this module, wf3rej.py, which is
    a Python wrapper around the C executable, the wf3rej.e C executable can also be
    called directly from the OS command line prompt:

    $ wf3rej.e input output [-options]

    Input can be a comma-delimited list of files, and an output file must be specified.
    $ wf3rej.e iaao01k8q_flc.fits,iaao01k9q_flc.fits output.fits -t

    Where the C executable options include:

        * -r: report version of code and exit (no other options selected)
        * -v: verbose
        * -t: print the timestamps
        * -shadcorr: perform shading shutter correction
        * -crmask: flag CR in input DQ images
        * -table <filename>: the crrejtab filename
        * -scale <number>: scale factor for noise
        * -init <med|min>: initial value estimate scheme
        * -sky <none|median|mode>: how to compute sky
        * -sigmas: rejection levels for each iteration
        * -radius <number>: CR expansion radius
        * -thresh <number> : rejection propagation threshold
        * -pdq <number>: data quality flag bits to reject

"""

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def wf3rej(input, output, crrejtab="", scalense=0., initgues="",
           skysub="", crsigmas="", crradius=0., crthresh=0.,
           badinpdq=0, crmask=False, shadcorr=False, verbose=False,
           log_func=print):
    """
    wf3rej, the cosmic-ray rejection and image combination task in calwf3,
    combines CR-SPLIT or REPEAT-OBS exposures into a single image, first
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
        Name of input files, such as
        - comma-separated (no spaces) filenames (``iaao01k8q_flc.fits,iaao01k9q_flc.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``*flt.fits``)
        - an at-file (``@input``)

    output : str
        Name of the output FITS file.

    crrejtab : str, default=""
        Reference file name.

    scalense : float, default=0.
        Scale factor applied to noise.

    initgues : str, default=""
        Initial value estimate scheme (min|med).

    skysub : str, default=""
        How to compute the sky (none|mode|mean).

    crsigmas : str, default="" (IS THIS A FLOAT)
        Rejection levels in each iteration.

    crradius : float, default=0.
        Cosmic ray expansion radius in pixels.

    crthresh : float, default=0.
        Rejection propagation threshold.

    badinpdq : int, default=0
        Data quality flag bits to reject.

    crmask : bool, default=False
        If True, flag CR in DQ extension of the input images. If False, the wf3rej
        program will read the value of crmask from the CRREJTAB file and follow the
        specification.  If True in the file, flag CR in DQ extensions of the input
        images.  If False, do NOT flag CR in the DQ extension of input images.

    shadcorr : bool, default=False
        If True, perform shading shutter correction.

    verbose : bool, optional, default=False
        If True, Print verbose time stamps.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Returns
    -------
    None

    Examples
    --------
    >>> from wfc3tools import wf3rej
    >>> from glob import glob
    >>> infiles = glob("*flt.fits")
    >>> wf3rej(infiles, "output.fits", verbose=True)

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
    input = ','.join(infiles)

    call_list.append(input)

    if output:
        call_list.append(str(output))

    if verbose:
        call_list.append("-v")
        call_list.append("-t")

    if (shadcorr):
        call_list.append("-shadcorr")

    if (crmask):
        call_list.append("-crmask")

    if (crrejtab != ""):
        call_list += ["-table", crrejtab]

    if (scalense != ""):
        call_list += ["-scale", str(scalense)]

    if (initgues != ""):
        options = ["min", "med"]
        if initgues not in options:
            raise ValueError("Invalid option for initgues")
        else:
            call_list += ["-init", str(initgues)]

    if (skysub != ""):
        options = ["none", "mode", "median"]
        if skysub not in options:
            raise ValueError(f"Invalid skysub option {options}: {skysub}")
        else:
            call_list += ["-sky", str(skysub)]

    if (crsigmas != ""):
        call_list += ["-sigmas", str(crsigmas)]

    if (crradius >= 0.):
        call_list += ["-radius", str(crradius)]
    else:
        raise ValueError("Invalid crradius specified")

    if (crthresh >= 0.):
        call_list += ["-thresh", str(crthresh)]
    else:
        raise ValueError("Invalid crthresh specified")

    if (badinpdq >= 0):
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
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    ec = error_code(return_code)
    if return_code:
        if ec is None:
            raise RuntimeError(f"wf3rej.e exited with unknown return code {return_code}.")
        raise RuntimeError(f"wf3rej.e exited with return code {ec}.")
