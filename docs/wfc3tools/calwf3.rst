
******
calwf3
******


``calwf3`` is the name of the  main executable which processes data from the WFC3 instrument onboard Hubble taken with either the UVIS or IR detectors. The code automatically calls the appropriate tasks, but users may also run the tasks independently if they desire special processing for their datasets. :ref:`wf3cte`, :ref:`wf3ccd` and :ref:`wf32d` are used for processing UVIS images, while IR image processing is done with :ref:`wf3ir`. The :ref:`wf3rej` program is used for both UVIS and IR images to combine multiple exposures contained in a CR-SPLIT or REPEAT-OBS set. :num:`Figure#calflow` is the flow diagram for the UVIS pipeline as a whole, while :num:`Figure#irflow` contains the flow for the IR pipeline.


During automatic pipeline processing by the STScI archive, ``Astrodrizzle`` follows ``calwf3``. All calibrated images are corrected for geometric distortion correction and associated sets of dithered images are combined into a single product. See the WFC3 Data Handbook for more information, or `Astrodrizzle <http://www.stsci.edu/hst/HST_overview/drizzlepac/>`_ .


Where to Find calwf3
====================

``calwf3`` is part of HSTCAL package, which can be downloaded from
http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas
and is installed along with the STScI distributed package Ureka.


A detailed description of the improved ``calwf3``, Version 3.3, which is more generally referred to as the UVIS2.0 update, will be available in a future publication of WFC3 Data Handbook and several ISRs which will accompany the update.

The current WFC3 Data Handbook can be found at  http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/ .
In the meantime, if you have questions not answered in this documentation, please contact STScI Help Desk (help[at]stsci.edu).


Running calwf3
==============

``calwf3`` can be run on a single input raw file or an asn table listing the members of an associtaion.
When processing an association, it retrieves calibration switch and reference file keyword settings from
the first image listed in the asn table. ``calwf3`` does not accept a user-defined list of input images on the
command line (e.g. ``*raw.fits`` to process all raw files in the current directory).

The :ref:`wf3ccd`, :ref:`wf32d`, :ref:`wf3cte` and :ref:`wf3ir` tasks on the other hand, will accept such user-defined input file lists, but they will not accept an association table( asn ) as input.


Running ``calwf3`` from a python terminal
-----------------------------------------

    In Python without TEAL:

    >>> from wfc3tools import calwf3
    >>> calwf3(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import calwf3
    >>> teal.teal('calwf3')

    In Pyraf:

    >>> import wfc3tools
    >>> epar calwf3


Running many files at the same time
-----------------------------------

The recommended method for running ``calwf3`` in batch mode is to use Python and
the ``wfc3tools`` package in the `STSDAS distribution
<http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas>`_ .

For example::

    from wfc3tools import calwf3
    from glob import glob

    for fits in glob('j*_raw.fits'):
        calwf3(fits)

.. note::

   When running in the notebook or from the python wrappers ``calwf3()`` may raise a RuntimeError if the underlying ``calwf3.e`` program fails with a non-zero exit code. Review the text output during the calibration call for hints as to what went wrong. Full runtime and error messages are printed to the terminal window and saved in the trailer file (.tra) for every run to help you diagnose the issue. 


Displaying output from calwf3 in a Jupyter Notebook
---------------------------------------------------

When calling ``calwf3`` from a Jupyter notebook or from the python wrappers, informational text output from the underlying ``calwf3.e`` program will be passed through ``print`` as the calibration runs by default, and show up in the user's cell. This behavior can be customized by passing your own function as the ``log_func`` keyword argument to ``calwf3``. As output is read from the underlying program, the ``calwf3`` Python wrapper will call ``log_func`` with the contents of each line. (``print`` is an obvious choice for a log function, but this also provides a way to connect ``calwf3`` to the Python logging system by passing the ``logging.debug`` function or similar.)

If ``log_func=None`` is passed, informational text output from the underlying program will be ignored, but the program's exit code will still be checked for successful completion.


Command Line Options
--------------------

`calwf3`  can also be called directly from the OS command line:

>>> calwf3.e iaa001kaq_raw.fits [command line options]


The command line executable only accepts one file at a time, but you can use os tools like `awk` to process everything in a directory:

>>> ls *raw.fits | awk '{print "calwf3.e",$1}' | csh


The following options are available

* t: Print verbose time stamps.

* s: Save temporary files.

* v: Turn on verbose output.

* d: Turn on debug output.

* q: Turn on quiet output.

* r: Print the current software version number (with full revision information)

* --version: Print the current software version number only


Types of files used as input to calwf3
--------------------------------------

* _asn file: name of an association table
* _raw file: name of an individual, uncalibrated exposure
* _crj file: name of any sub-product from an association table

While both CR-SPLIT and REPEAT-OBS exposures from an association get combined using `calwf3`, dithered observations from an association do not.

.. _uvis_data_format:

.. figure:: ../_static/uvis_data_format.png
    :align: center
    :alt:  UVIS data raw file format

    UVIS data raw file format



.. _ir_data_format:

.. figure:: ../_static/ir_data_format.png
    :align: center
    :alt:  IR data raw file format

    IR data raw file format


* The science image contains the data from the focal plane array detectors.
* The error array contains an estimate of the statistical uncertainty associated with each corresponding science image pixel
* The data quality array contains independent flags indicating various status and problem conditions associated with each corresponding pixel in the science image
* The sample array (IR ONLY) contains the number of samples used to derive the corresponding pixel values in the science image.
* The time array (IR ONLY) contains the effective integration time associated with each corresponding science image pixel value.

Parameters
==========

    input : str
        Name of input files

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``)

    output: str
        Name of the output FITS file.

    printtime: bool
        print a detailed time stamp

    save_tmp: bool
        save temporary files

    debug: bool
        print optionsl debugging statements

    parallel: bool
        run the code with OpemMP parallel processing turned on for the UVIS CTE correction

    log_func: func()
        if not specified, the print function is used for logging to facilitate use in the jupyter notebook

    verbose: bool, optional
        Print verbose time stamps?

    quiet: bool, optional
        Print messages only to trailer file?



Types of output file from calwf3
--------------------------------

The suffixes used for WFC3 raw and calibrated data products closely mimic those used by ACS and NICMOS:

========   =================================================    ====================
SUFFIX     DESCRIPTION                                          UNITS
========   =================================================    ====================
_raw       raw data                                             DN
_rac       UVIS CTE corrected raw data, no other calibration    DN
_asn       association file for observation set
_spt       telescope and WFC3 telemetry and engineering data
_blv_tmp   overscan-trimmed UVIS exposure                       DN
_blc_tmp   overscan0trimmed UVIS, CTE corrected exposure        DN
_crj_tmp   uncalibrated, cosmic-ray rejected combined           DN
_crc_tmp   uncalibrated, cosmic-rat rejected, CTE cleaned       DN
_ima       calibrated intermediate IR multiaccum image          :math:`e^{-}/s`
_flt       UVIS calibrated exposure                             :math:`e^{-}`
_flc       UVIS calibrated exposure including CTE correction    :math:`e^{-}`
_flt       IR calibrated exposure                               :math:`e^{-}/s`
_crj       UVIS calibrated, cosmic ray rejected image           :math:`e^{-}`
_crj       IR calibrated, cosmic ray rejected image             :math:`e^{-}/s`
_crc       UVIS calibrated, cr rejected, cte cleaned image      :math:`e^{-}`
.tra       trailer file, contains processing messages
========   =================================================    ====================


** DRZ and DRC products are produced with Astrodrizzle, see `Astrodrizzle <http://www.stsci.edu/hst/HST_overview/drizzlepac/>`_ **


Keyword Usage
-------------

`calwf3` processing is controlled by the values of keywords in the input image headers. Certain keywords, referred to as calibration switches, are used to control which calibration steps are performed. Reference file keywords indicate which reference files to use in the various calibration steps. Users who which to perform custom reprocessing of their data may change the values of these keywords in the _raw FITS file headers and then rerun the modified file through  `calwf3`. See the `WFC3 Data Handbook <http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/wfc3_Ch25.html>`_ for a more complete description of these keywords and their values.


.. include:: uvis_pipeline.inc

.. include:: ir_pipeline.inc
