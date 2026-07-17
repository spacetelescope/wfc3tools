"""Run wf3ir step in calwf3.

This routine contains all the instrumental calibration steps for
WFC3 IR channel images. The steps are:

- DQICORR: initialize the data quality array
- ZSIGCORR: estimate the amount of signal in the zeroth-read
- BLEVCORR: subtract the bias level from the reference pixels
- ZOFFCORR: subtract the zeroth read image
- NLINCORR: correct for detector non-linear response
- DARKCORR: subtract the dark current image
- PHOTCORR: compute the photometric keyword values
- UNITCORR: convert to units of count rate
- CRCORR: fit accumulating signal and identify the cr hits
- FLATCORR: divide by the flatfield images and apply gain conversion

The output images include the calibrated image ramp (IMA file) and the
accumulated ramp image (FLT file).

Only those steps with a switch value of PERFORM in the input files
will be executed, after which the switch will be set to COMPLETE in the
corresponding output files. See the WFC3 Data Handbook for
more information.

"""

import os.path
import subprocess

from stsci.tools import parseinput

from .util import error_code

__all__ = ["wf3ir"]


def wf3ir(input, output=None, verbose=False, quiet=True, log_func=print):
    """
    Call the wf3ir.e executable.

    Use this function to facilitate batch runs.

    Parameters
    ----------
    input : str
        Name of input files, such as:

        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``*raw.fits``)
        - filename of an ASN table (``*asn.fits``)
        - an at-file (``@input``)

    output : str, optional
        Name of the output FITS file. Default is `None`.

    verbose : bool, optional
        If `True`, print verbose time stamps.
        Default is `False`.

    quiet : bool, optional
        If `True`, print messages only to trailer file.
        Default is `True`.

    log_func : func
        By default, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Examples
    --------
    >>> from wfc3tools import wf3ir
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3ir(filename)

    """

    call_list = ["wf3ir.e"]
    return_code = None

    if verbose:
        call_list += ["-v", "-t"]

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ir does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ir can only accept 1 file forinput at a time: {0}".format(infiles))

    for image in infiles:
        if not os.path.exists(image):
            raise IOError("Input file not found: {0}".format(image))

    call_list.append(input)

    if output:
        call_list.append(str(output))

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
            print("Unknown return code found!")
            ec = return_code
        raise RuntimeError("wf3ir.e exited with code {}".format(ec))
