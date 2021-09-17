"""
calwf3:

    The main executable which processes data taken with either the UVIS or IR
    detectors of the WFC3 instrument onboard the Hubble Space Telescope is
    called calwf3. The code is organized into subroutines that are called by
    the calwf3 executable. The subroutines may be called independently if users
    desire specialized processing for their dataset. The subroutines used for
    processing UVIS images are called w3cte, wf3ccd, and wf32d. The main
    subroutine used for processing IR images is wf3ir. The wf3rej subroutine is
    shared between the UVIS and IR pipelines and is used for combining CR-SPLIT
    or REPEAT-OBS image sets. See Section 3.1 of the WFC3 Data Handbook for
    more information.

Running calwf3:

    ``calwf3`` can be run on a single input raw file or an asn table listing the
    members of an associtaion. When processing an association, it retrieves
    calibration switch and reference file keyword settings from the first image
    listed in the asn table. ``calwf3`` does not accept a user-defined list of
    input images on the command line (e.g. ``*raw.fits`` to process all raw
    files in the current directory).

"""

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


def calwf3(input=None, output=None, printtime=False, save_tmp=False,
           verbose=False, debug=False, parallel=True, version=False,
           log_func=print):
    """
    Run the calwf3.e executable as from the shell.

    Parameters
    ----------
    input : str or list, default=None
        Name of input files, such as
        - a single filename (iaa012wdq_raw.fits)
        - a Python list of filenames
        - a partial filename with wildcards (\*raw.fits)
        - filename of an ASN table (\*asn.fits)

    output : WHAT IS TYPE, default=None
        WHAT IS OUTPUT

    printtime : bool, default=False
        If True, print a detailed time stamp.

    save_tmp : bool, default=False
        If True, save temporary files.

    verbose : bool, optional, default=False
        If True, print verbose time stamps.

    debug : bool, default=False
        If True, print optional debugging statements.

    parallel : bool, default=True
        If True, run the code with OpemMP parallel processing turned on for the
        UVIS CTE correction.

    version : bool, default=False
        If True, WHAT IS VERSION???

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    DO WE STILL NEED THIS?
    quiet: bool, optional
        Print messages only to trailer file?

    Returns
    -------
    None

    Examples
    --------
    >>> # Running one file
    >>> from wfc3tools import calwf3
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> calwf3(filename)

    >>> # Running many files at the same time:
    >>> from wfc3tools import calwf3
    >>> from glob import glob
    >>> for fits in glob('j*_raw.fits'):
    >>>     calwf3(fits)

    """

    call_list = ['calwf3.e']
    return_code = None

    if version and input is None:
        call_list.append('-r')
    else:
        if printtime:
            call_list.append('-t')

        if save_tmp:
            call_list.append('-s')

        if verbose:
            call_list.append('-v')

        if debug:
            call_list.append('-d')

        if not parallel:
            call_list.append('-1')

        infiles, dummy = parseinput.parseinput(input)
        if len(parseinput.irafglob(input)) == 0:
            raise IOError("No valid image specified")
        if len(parseinput.irafglob(input)) > 1:
            raise IOError("calwf3 can only accept 1 file for"
                          "input at a time: {0}".format(infiles))

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
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    ec = error_code(return_code)
    if ec:
        if ec is None:
            print("Unknown return code found!")
            ec = return_code
        raise RuntimeError("calwf3.e exited with code {}".format(ec))

if __name__ == "main":
    """called system prompt, return the default corner locations """
    import sys
    calwf3(sys.argv[1])
