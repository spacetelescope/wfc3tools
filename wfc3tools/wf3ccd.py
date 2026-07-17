"""Run wf3ccd step in calwf3.

This routine contains the initial processing steps for all the WFC3 UVIS
channel data. These steps are:

* DQICORR - initialize the data quality array with values
  from BPIXTAB, flag for A-to-D saturation, and potentially flag for
  full-well saturation using scalar value as the threshold
  (fall-back algorithm)
* ATODCORR - perform the a-to-d conversion correction
* BLEVCORR - subtract the bias level from the overscan region
* BIASCORR - subtract the bias image
* Flag for full-well saturation using a two-dimensional image
* Detect and record SINK pixels in the DQ mask
  (performed if DQICORR is set to PERFORM)
* FLSHCORR - subtract the post-flash image

This step processes everything in counts. If a calibration reference file
is in units of electrons when used during processing, the calibration data
are divided by the gain before use. The conversion to electrons happens
in :ref:`wf32d`.

``wf3ccd`` first subtracts the bias and trims the overscan regions from the
image. If an associated set of UVIS CR-SPLIT or REPEAT-OBS images is being
processed, all of the overscan-trimmed images are sent through ``wf3rej``to
be combined and receive cosmic-ray rejection. The resulting combined image
then receives final calibration with ``wf32d``, which includes dark
subtraction and flat-fielding. If there are multiple sets of CR-SPLIT or
REPEAT-OBS images in an association, each set goes through the cycle of
``wf3ccd``, ``wf3rej``, and ``wf32d`` processing.

If BLEVCORR is performed the output contains the overcan-trimmed region.

Only those steps with a switch value of PERFORM in the input files will be
executed, after which the switch will be set to COMPLETE in the
corresponding output files. See the WFC3 Data Handbook for
more information.

.. note::
    Strictly speaking, the application of the full-well saturation *image* is
    not a calibration step (i.e., there is no SATCORR), but the application
    of a 2D image to flag pixels versus using a single scalar value to flag
    saturated pixels as previously done in DQICORR will be done in ``doFullWellSat()``
    after BLEVCORR and BIASCORR.  This correction should only be done if both
    BLEVCORR and BIASCORR have been performed.  This flagging is only applicable
    for the UVIS.

"""

import os.path
import subprocess

from stsci.tools import parseinput

from .util import error_code

__all__ = ["wf3ccd"]


def wf3ccd(
    input,
    output=None,
    dqicorr="PERFORM",
    atodcorr="PERFORM",
    blevcorr="PERFORM",
    biascorr="PERFORM",
    flashcorr="PERFORM",
    verbose=False,
    quiet=True,
    log_func=print,
):
    """
    Run the ``wf3ccd.e`` executable as from the shell.

    ``wf3ccd`` first subtracts the bias and trims the overscan regions from the
    image. If an associated set of UVIS CR-SPLIT or REPEAT-OBS images is being
    processed, all of the overscan-trimmed images are sent through ``wf3rej`` to
    be combined and receive cosmic-ray rejection.

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
        Update the DQ array from bad pixel table, as well as flag the A-to-D saturation.
        If the comparatively new FITS keyword (mid-2023) SATUFILE is missing or not
        populated in the input file, the full-well saturation will also be flagged using
        a single value as the threshold. Allowed values are "PERFORM" and "OMIT".
        Default is "PERFORM".

    atodcorr : str, optional
        Analog to digital correction. Allowed values are "PERFORM" and "OMIT".
        Default is "PERFORM".

    blevcorr : str, optional
        Subtract bias from overscan regions. Allowed values are "PERFORM" and
        "OMIT". Default is "PERFORM".

    biascorr : str, optional
        Subtract bias image. Allowed values are "PERFORM" and "OMIT".
        Default is "PERFORM".

    flashcorr : str, optional
        Subtract post-flash image. Allowed values are "PERFORM" and "OMIT".
        Default is "PERFORM".

    verbose : bool, optional
        If `True`, print verbose time stamps. Default is `False`.

    quiet : bool, optional
        If `True`, print messages only to trailer file.
        Default is `True`.

    log_func : func
        By default, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Examples
    --------
    >>> from wfc3tools import wf3ccd
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3ccd(filename)

    """

    call_list = ["wf3ccd.e"]
    return_code = None

    if verbose:
        call_list += ["-v", "-t"]

    if dqicorr == "PERFORM":
        call_list.append("-dqi")

    if atodcorr == "PERFORM":
        call_list.append("-atod")

    if blevcorr == "PERFORM":
        call_list.append("-blev")

    if biascorr == "PERFORM":
        call_list.append("-bias")

    if flashcorr == "PERFORM":
        call_list.append("-flash")

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ccd does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ccd can only accept 1 file forinput at a time: {0}".format(infiles))

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
        raise RuntimeError("wf3ccd.e exited with code {}".format(ec))
