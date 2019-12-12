# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os.path
import subprocess
from .version import __version_date__, __version__

from stsci.tools import parseinput
from .util import error_code


def calwf3(input=None, printtime=False, save_tmp=False, verbose=False,
           debug=False, parallel=True, log_func=print):
    """
    Runs the calwf3 calibration pipeline on a single input WFC3 UVIS or IR
    image, or asn table listing members of an association.

    calwf3 is the name of the main executable which processes data from the
    WFC3 instrument onboard Hubble taken with either the UVIS or IR detectors.
    The code is organized into subtasks - wf3cte, wf3ccd and wf32d are used for
    processing UVIS images, while IR image processing is done with wf3ir.
    wef3rej is used for both detectors to combine images contained in a
    CR-SPLIT or REPEAT-OBS set. These subtasks can be run independently for
    custom processing, but calwf3 refers to the full pipeline that runs all
    appropriate calibrations steps.

    calwf3 processing is controlled by the values of keywords in the input
    image headers. Certain keywords, referred to as calibration switches, are
    used to control which calibration steps are performed. Reference file
    keywords indicate which reference files to use in the various calibration
    steps. Users who wish to perform custom reprocessing of their data may
    change the values of these keywords in the _raw FITS file primary headers
    and then rerun the modified file through calwf3. See the WFC3 Data Handbook
    for a more complete description of these keywords and their values.

    calwf3 can be run on a single input raw* file or an asn table listing the
    members of an association. calwf3 does not accept a user-defined list of
    input images on the command line (e.g. *raw.fits to process all raw files
    in the current directory).

    Parameters
    ----------
    input : str
        Single UVIS or IR raw file, IR ima file, or an ASN table (_asn.fits).
    printtime : bool
        Print a detailed time stamp.
    save_tmp: bool
        Save temporary files.
    debug: bool
        Print optional debugging statements.
    parallel: bool
        Run the code with OpemMP parallel processing turned on for the
        UVIS CTE correction.
    log_func: func()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.
    verbose : bool, optional
        Print verbose time stamps.
    quiet : bool, optional
        Print messages only to trailer file.

    Outputs
    -------
    <filename>.tra : text file
        Trailer file, contains processing messages.
    <filename>_ima.fits : FITS file
        Calibrated intermediate IR multiaccum image (e-/s).
    <filename>_flt.fits : FITS file
        UVIS calibrated exposure (e-), or IR calibrated exposure (e-/s).
    <filename>_flc.fits : FITS file
        UVIS calibrated exposure including CTE correction (e-/s). Only produced
        if PCTECORR in image header is set to PERFORM.
    <filename>_crj.fits : FITS file
            UVIS calibrated, cosmic ray rejected image (e-), or IR calibrated
            cosmic ray rejected image (e-/s). Produced if input is an
            association with more than one member, and contains exposures in a
            CR-SPLIT or REPEAT-OBS set
    <filename>_crc.fits : FITS file
            UVIS calibrated, CR rejected, CTE cleaned image (e-). Produced if
            input is an association of UVIS raws, and PCTECORR in image header
            is set to PERFORM.
    <filename>_crj_tmp.fits : FITS file
        Uncalibrated, cosmic-ray rejected combined (DN)
    <filename>_crc_tmp.fits : FITS file
            UVIS calibrated, CR rejected, CTE cleaned image (e-). Produced if
            input is an association of UVIS raws, and PCTECORR in image header
            is set to PERFORM.
    <filename>_rac_tmp.fits : FITS file
                UVIS CTE corrected raw data, no other calibration (DN).
    <filename>_blv_tmp.fits : FITS file
                Overscan-trimmed UVIS exposure (DN).
    <filename>_blc_tmp.fits : FITS file
                Overscan-trimmed UVIS, CTE corrected exposure (DN).

    Notes
    ------
        - *If an intermediate step file (i.e _ima.fits) file is provided as
            input, the pipeline will pick up at the step following the
            production of that file. Output file names may be unexpected, so
            proceed with caution when using this option.
        - Output files depend on input (IR or UVIS, _ima.fits or _raw.fits, and
            if input is an association or single file) and the save_tmp flag.
        - If an IR association is passed in, the associated _spt.fits files
            must be downloaded along with the _raw.fits files.
        - When processing an association, calwf3 retrieves calibration switch
            and reference file keyword settings from the first image listed in
            the asn table.

    """

    call_list = ['calwf3.e']
    return_code = None

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
