.. _wf3rej:

********
`wf3rej`
********

`wf3rej`, the cosmic-ray rejection and image combination task in `calwf3`,
combines CR-SPLIT or REPEAT-OBS exposures into a single image, first
detecting and then replacing flagged pixels. The task uses the same
statistical detection algorithm developed for ACS (`acsrej`), STIS (`ocrrej`),
and WFPC2 data (`crrej`), providing a well-tested and robust procedure.

First, `wf3rej` temporarily removes the sky background from each input image
(if specified via the SKYSUB parameter in the CRREJTAB, or by a parameter passed
to the Python script or C executable), usually computed using the mathematical
mode of each image. Sky subtraction is performed before any
statistical checks are made for cosmic rays. Next, `wf3rej` constructs an
initial comparison image from each sky-subtracted exposure. This comparison
image can either be a median- or minimum-value sky-subtracted image
constructed from all the input images, and it represents the ‘initial
guess’ of a cosmic-ray free image. The comparison image serves as the basis
for determining the statistical deviation of each pixel within the input
images.

A detection threshold is then calculated for each pixel based on the
comparison image. The actual detection criterion for a cosmic ray is
also calculated. If the detection criterion is greater than the detection
threshold, the pixel is flagged as a cosmic ray in the input image’s DQ
array and is ignored when images are summed together. Surrounding pixels
within some expansion radius (CRRADIUS) are marked as ‘SPILL’ pixels and
are given less stringent detection thresholds.

In summary, the cosmic ray rejection task sums all non-rejected pixel
values, computes the true exposure time for that pixel, and scales the sum
to correspond to the total exposure time. The final scaled, cleaned pixel
is written to the comparison image to be used for the next iteration. This
process is then repeated with increasingly stringent detection thresholds,
as specified by CRSIGMAS. See `Section 3.4.5 of the WFC3 Data Handbook 
<https://hst-docs.stsci.edu/wfc3dhb/chapter-3-wfc3-data-calibration/3-4-pipeline-tasks>`_
for more information.


Running `wf3rej` from a Python Terminal
=======================================

.. code-block:: shell

    from wfc3tools import wf3rej
    wf3rej([filename1, filename2])


Displaying Output from `wf3rej` in a Jupyter Notebook
-----------------------------------------------------

When calling `wf3rej` from a Jupyter notebook, informational text output from the underlying `wf3rej.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3rej`. As output is read from the underlying program, the `wf3rej` Python wrapper will call `log_func` with the contents of each line. Note that `print` is an obvious choice for a log function, but this also provides a way to connect `wf3rej` to the Python logging system by passing the `logging.debug` function or similar.

If `log_func=None` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.

Input Parameters for the Python Interface 
-----------------------------------------

Parameters
~~~~~~~~~~

    input : str or list
        Name of input files, such as
            * comma-separated (no spaces) filenames (``iaao01k8q_flc.fits,iaao01k9q_flc.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``*flt.fits``)
            * an at-file (``@input``)

    output : str
        Name of the output FITS file.

    crrejtab : str, default=""
        Reference filename.

    scalense : float, default=0.
        Scale factor applied to noise.

    initgues : str, default=""
        Initial value estimate scheme (min|med).

    skysub : str, default=""
        How to compute the sky (none|mode|mean).

    crsigmas : str, default=""
        Rejection levels in each iteration.

    crradius : float, default=0.
        Cosmic ray expansion radius in pixels.

    crthresh : float, default=0.
        Rejection propagation threshold.

    badinpdq : int, default=0
        Data quality flag bits to reject.

    crmask : bool, default=Setting to be read from CRREJTAB.
        If argument is present, write the CR flag value to the input DQ images.

    shadcorr : bool, default=Setting to be read from SHADCORR keyword value in primary header of first image to process.
        If argument is present, perform shading shutter correction.

    verbose : bool, optional, default=False
        If True, print timestamps and other output.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.


Returns
~~~~~~~

    None


Usage
~~~~~

.. code-block:: python

    from wfc3tools import wf3rej
    from glob import glob
    infiles = glob("*flt.fits")
    wf3rej(infiles, "output.fits", verbose=True)

    wf3rej("*flt.fits", "output.fits", verbose=True)

    wf3rej("@input.lst", "output.fits", verbose=True)

Please see the highlighted Note regarding the parameter settings for `wf3rej.e` for more details as to the action taken when the parameters use their default values. 

Command Line Options for the `wf3rej` C Executable
==================================================

.. code-block:: shell

    wf3rej.e input output [-r] [-v] [-t] [-shadcorr] [-crmask] [-table <filename>] 
        [-scale <float>] [-init <med|min>] [-sky <none|mode|mean>] [-sigmas <string>] 
        [-radius <float>] [-thresh <float>] [-pdq <short>]


    Example - Process data with timestamps and a custom cosmic ray rejection table:
    wf3rej.e iaao01k8q_flc.fits,iaao01k9q_flc.fits output.fits -t

    Example - Print the code version and exit:
    wf3rej.e -r

    input : comma-separated list of strings
        Input filenames as a list of comma-separated input names
        ipppssoot_raw.fits,ipppssoot_raw.fits (Note: Do not include any blank spaces.)

    output : str
        Name of output filename

    options
           -r : print version number/date of software and exit (no other options selected)
           -v : verbose mode
           -t : print the timestamps
    -shadcorr : perform shading shutter correction
      -crmask : set CR flags in input DQ images

    -table <filename>: string, the crrejtab filename
      -scale <number>: float, scale factor for noise
      -init <med|min>: string, initial value estimate scheme
     -sky <none|mode|mean>: string, method to compute sky
    -sigmas <string of numbers>: string, rejection levels for each iteration (e.g., "3.5,4.5,5.5")
     -radius <number>: float, CR expansion radius
    -thresh <number> : float, rejection propagation threshold
        -pdq <number>: short, data quality flag bits to reject

.. note::

    If the ``shadcorr`` option is included on the command line **or** SHADCORR = PERFORM in the primary header of the first image to be processed, the shadcorr correction will be done.

    Including the ``crmask`` option on the command line indicates the desire to put the CR flag values into the DQ extension of the input images.  Not including this option does *not* turn off the insertion, but rather the program will follow the default setting for the ``crmask`` option as indicated in the CRREJTAB calibration file.

    If not all of the following options have been specified on the command line, the CRREJTAB will be read and default values used for the missing options.  The options are: crmask, scale, init, sky, sigmas, radius, thresh, and pdq.  The CRREJTAB read is either the filename specified by the ``table`` parameter **or** the one specified in primary header of the first image to be processed.   In verbose mode, all of the option values are printed to the output logfile.

