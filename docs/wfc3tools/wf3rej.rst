.. _wf3rej:

******
wf3rej
******

wf3rej, the cosmic-ray rejection and image combination task in calwf3,
combines CR-SPLIT or REPEAT-OBS exposures into a single image, first
detecting and then replacing flagged pixels. The task uses the same
statistical detection algorithm developed for ACS (acsrej), STIS (ocrrej),
and WFPC2 data (crrej), providing a well-tested and robust procedure.

First, wf3rej temporarily removes the sky background from each input image
(if requested via the SKYSUB parameter in the CRREJTAB), usually computed
using the mode of each image. Sky subtraction is performed before any
statistical checks are made for cosmic rays. Next, wf3rej constructs an
initial comparison image from each sky-subtracted exposure. This comparison
image can either be a median- or minimum-value sky-subtracted image
constructed from all the input images, and it represents the ‘initial
guess’ of a cosmic-ray free image. The comparison image serves as the basis
for determining the statistical deviation of each pixel within the input
images.

A detection threshold is then calculated for each pixel based on the
comparison image. The actual detection criterion for a cosmic ray is
also calculated. If the etection criterion is greater than the detection
threshold, the pixel is flagged as a cosmic ray in the input image’s DQ
array and is ignored when images are summed together. Surrounding pixels
within some expansion radius (CRRADIUS) are marked as ‘SPILL’ pixels and
are given less stringent detection thresholds.

In summary, the cosmic ray rejection task sums all non-rejected pixel
values, computes the true exposure time for that pixel, and scales the sum
to correspond to the total exposure time. The final scaled, cleaned pixel
is written to the comparison image to be used for the next iteration. This
process is then repeated with increasingly stringent detection thresholds,
as specified by CRSIGMAS. See `Section 3.4.5 of the WFC3 Data Handbook <https://hst-docs.stsci.edu/wfc3dhb>`_ for more information.


Displaying output from wf3rej in a Jupyter Notebook
===================================================

When calling `wf3rej` from a Jupyter notebook, informational text output from the underlying `wf3rej.e` program will be passed through `print` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the `log_func` keyword argument to `wf3rej`. As output is read from the underlying program, the `wf3rej` Python wrapper will call `log_func` with the contents of each line. (`print` is an obvious choice for a log function, but this also provides a way to connect `wf3rej` to the Python logging system by passing the logging.debug function or similar.)

If `log_func=None` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.


Parameters
==========

    input : str or list
        Name of input files, such as

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``)

    output : str, default=""
        Name of the output FITS file.

    crrejtab : str, default=""
        Reference file name.

    scalense : str, default="" (IS THIS A FLOAT)
        Scale factor applied to noise.

    initgues : str, default=""
        Initial value estimate scheme (min|med).

    skysub : str, default=""
        How to compute the sky (none|mode|mean).

    crsigmas : str, default="" (IS THIS A FLOAT)
        Rejection levels in each iteration.

    crradius : float, default=0
        Cosmic ray expansion radius in pixels.

    crthresh : float, default=0
        Rejection propagation threshold.

    badinpdq : int, default=0
        Data quality flag bits to reject.

    crmask : bool, default=False
        If True, flag CR in input DQ images.

    shadcorr : bool, default=False
        If True, perform shading shutter correction.

    verbose : bool, optional, default=False
        If True, Print verbose time stamps.

    log_func : func(), default=print()
        If not specified, the print function is used for logging to facilitate
        use in the Jupyter notebook.


Returns
=======

    None


Usage
=====

.. code-block:: python

    from wfc3tools import wf3rej
    wf3rej(filename)


Command Line Options for the wf3rej executable
==============================================

.. code-block:: shell

    wf3rej.e input output [-options]

Input may be a single filename, and the options include:

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
