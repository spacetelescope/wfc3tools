.. _wf3rej:

wf3rej
======

``wf3rej`` is the cosmic-ray rejection and image combination task in ``calwf3``.
It combines CR-SPLIT or REPEAT-OBS exposures into a single image, first
detecting and then replacing flagged pixels. The task uses the same
statistical detection algorithm developed for ACS (``acsrej``), STIS (``ocrrej``),
and WFPC2 data (``crrej``), providing a well-tested and robust procedure.
It takes input FLT/FLC images and will produce an output CRJ/CRC image.

First, it temporarily removes the sky background from each input image
(if specified via the SKYSUB parameter in the CRREJTAB, or by a parameter passed
to the Python script or C executable), usually computed using the mathematical
mode of each image. Sky subtraction is performed before any
statistical checks are made for cosmic rays. Next, it constructs an
initial comparison image from each sky-subtracted exposure. This comparison
image can either be a median- or minimum-value sky-subtracted image
constructed from all the input images, and it represents the "initial
guess" of a cosmic-ray free image. The comparison image serves as the basis
for determining the statistical deviation of each pixel within the input
images.

A detection threshold is then calculated for each pixel based on the
comparison image. The actual detection criterion for a cosmic ray is
also calculated. If the detection criterion is greater than the detection
threshold, the pixel is flagged as a cosmic ray in the input image's DQ
array and is ignored when images are summed together. Surrounding pixels
within some expansion radius (CRRADIUS) are marked as SPILL pixels and
are given less stringent detection thresholds.

In summary, the cosmic ray rejection task sums all non-rejected pixel
values, computes the true exposure time for that pixel, and scales the sum
to correspond to the total exposure time. The final scaled, cleaned pixel
is written to the comparison image to be used for the next iteration. This
process is then repeated with increasingly stringent detection thresholds,
as specified by CRSIGMAS. See
`the WFC3 Data Handbook
<https://hst-docs.stsci.edu/wfc3dhb/chapter-3-wfc3-data-calibration/3-4-pipeline-tasks>`_
for more information.

.. automodapi:: wfc3tools.wf3rej

Command Line Options for the ``wf3rej`` C Executable
----------------------------------------------------

The wf3rej function can also be called directly from the OS command line:

.. code-block:: shell

    wf3rej.e input output [-r] [-v] [-t] [-shadcorr] [-crmask] [-table <filename>]
        [-scale <float>] [-init <med|min>] [-sky <none|mode|mean>] [-sigmas <string>]
        [-radius <float>] [-thresh <float>] [-pdq <short>]

Print the code version and exit::

    wf3rej.e -r

Process data with timestamps and a custom cosmic ray rejection table::

    wf3rej.e iaao01k8q_flc.fits,iaao01k9q_flc.fits output.fits -t

Input can be a comma-delimited list of files (no spaces) and
an output file must be specified, and the options include:

* -r: report version of code and exit (no other options selected)
* -v: verbose mode
* -t: print the timestamps
* -shadcorr: perform shading shutter correction
* -crmask: flag CR in input DQ images
* -table <filename>: the crrejtab filename
* -scale <number>: scale factor for noise
* -init <med|min>: initial value estimate scheme
* -sky <none|median|mode>: how to compute sky
* -sigmas <string of numbers>: rejection levels for each iteration
  (e.g., "3.5,4.5,5.5")
* -radius <number>: CR expansion radius
* -thresh <number> : rejection propagation threshold
* -pdq <number>: data quality flag bits to reject

If the ``shadcorr`` option is included on the command line **or**
``SHADCORR=PERFORM`` in the primary header of the first image
to be processed, the shading shutter correction will be done.

Including the ``crmask`` option on the command line indicates
the desire to put the CR flag values into the DQ extension
of the input images.  Not including this option does
*not* turn off the insertion, but rather the program will
follow the default setting for the ``crmask`` option as
indicated in the CRREJTAB calibration file.

If not all of the following options have been specified on
the command line, the CRREJTAB will be read and default values
used for the missing options.  The options are:
crmask, scale, init, sky, sigmas, radius, thresh, and pdq.
The CRREJTAB read is either the filename specified by the
``table`` parameter **or** the one specified in primary header
of the first image to be processed.
In verbose mode, all of the option values are printed to
the output logfile.
