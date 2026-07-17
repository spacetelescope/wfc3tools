"""Run wf32d step in calwf3.

This routine performs the remaining series of tasks in the UVIS pipeline.
The wf32d primary functions include:

- DARKCORR: dark current subtraction
- FLATCORR: flat-fielding
- PHOTCORR: photometric keyword calculations
- FLUXCORR: photometric normalization of the UVIS1 and UVIS2 chips

Only those steps with a switch value of PERFORM in the input files will be
executed, after which the switch will be set to COMPLETE in the
corresponding output files. See the WFC3 Data Handbook for
more information.

"""

import os.path
import subprocess

from stsci.tools import parseinput

from .util import error_code

__all__ = ["wf32d"]


def wf32d(
    input,
    output=None,
    dqicorr="PERFORM",
    darkcorr="PERFORM",
    flatcorr="PERFORM",
    shadcorr="PERFORM",
    photcorr="PERFORM",
    verbose=False,
    quiet=True,
    debug=False,
    log_func=print,
):
    """
    Call the wf32d.e executable.

    Use this function to facilitate batch runs.

    Perform or omit DQ array updates, dark image subtraction, flatfield image
    multiplication, shutter shading correction, and photometry keyword updates
    for the output file.

    Parameters
    ----------
    input : str or list
        Name of input files, such as:

        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``*raw.fits``)
        - filename of an ASN table (``*asn.fits``)
        - an at-file (``@input``)

    output : str
        Name of the output FITS file. Default is `None`.

    dqicorr : str, optional
        Update the dq array from bad pixel table. Allowed values are "PERFORM"
        and "OMIT". Default is "PERFORM".

    darkcorr : str, optional
        Subtract the dark image. Allowed values are "PERFORM" and "OMIT".
        Default is "PERFORM".

    flatcorr : str, optional
        Multiply by the flatfield image. Allowed values are "PERFORM" and
        "OMIT". Default is "PERFORM".

    shadcorr : str, optional
        Correct for shutter shading (CCD). Allowed values are "PERFORM" and
        "OMIT". Default is "PERFORM".

    photcorr : str, optional
        Update photometry keywords in the header. Allowed values are "PERFORM"
        and "OMIT". Default is "PERFORM".

    verbose : bool, optional
        If `True`, print verbose time stamps. Default is `False`.

    quiet : bool, optional
        If `True`, print messages only to trailer file. Default is `True`.

    debug : bool, optional
        If `True`, print debugging statements. Default is `False`.

    log_func : func
        By default, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Examples
    --------
    >>> from wfc3tools import wf32d
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf32d(filename)

    """

    call_list = ["wf32d.e"]
    return_code = None

    if verbose:
        call_list += ["-v", "-t"]

    if debug:
        call_list.append("-d")

    if darkcorr == "PERFORM":
        call_list.append("-dark")

    if dqicorr == "PERFORM":
        call_list.append("-dqi")

    if flatcorr == "PERFORM":
        call_list.append("-flat")

    if shadcorr == "PERFORM":
        call_list.append("-shad")

    if photcorr == "PERFORM":
        call_list.append("-phot")

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf32d does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf32d can only accept 1 file forinput at a time: {0}".format(infiles))

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
        raise RuntimeError("wf32d.e exited with code {}".format(ec))
