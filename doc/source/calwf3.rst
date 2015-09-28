======
calwf3
======

Examples
--------

    In Python without TEAL:

    >>> from wfc3tools import calwf3
    >>> calwf3.calwf3(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import calwf3
    >>> teal.teal('calwf3')

    In Pyraf:

    >>> import wfc3tools
    >>> epar calwf3


A detailed description of this new and improved ``calwf3`` will be available in a future publication of WFC3 Data Handbook. 
The current WFC3 Data Handbook can be found at  http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/ .  
In the meantime, if you have questions not answered in this documentation, please contact STScI Help Desk (help[at]stsci.edu). 


Running calwf3
--------------

``calwf3`` can be run on a single input raw file or an asn table listing the members of an associtaion. 
When processing an association, it retrieves calibration switch and reference file keyword settings from 
the first image listed in the asn table. ``calwf3`` does not accept a user-defined list of input images on the 
command line (e.g. ``*raw.fits`` to process all raw files in the current directory).

The ``wf3ccd``, ``wf32d``, and ``wf3ir`` tasks on the other hand, will accept such user-defined input file lists, 
but they will not accept an association table( asn ) as input.

Batch calwf3
------------

The recommended method for running ``calwf3`` in batch mode is to use Python and
the ``wfc3tools`` package in the "STSDAS distribution
<http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas>."

For example::

    from wfc3tools import calwf3
    import glob

    for fits in glob.glob('j*_raw.fits'):
        calwf3.calwf3(fits)


Where to Find calwf3
--------------------

``calwf3`` is now part of HSTCAL package, which can be downloaded from
http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas


Usage
-----

**The calwf3 executable can also be called directly from the command line:**

>>> calwf3.e iaa001kaq_raw.fits [command line options]


Command Line Options
--------------------

``calwf3`` supports several command line options:

* -t: Print verbose time stamps.
  
* -s: Save temporary files.
  
* -v: Turn on verbose output.
  
* -d: Turn on debug output.
  
* -q: Turn on quiet output.
  
* -r: Print the current software version number (revision)

* --version: Print the current software version


CTE correction (PCTECORR)
-------------------------
The charge transfer efficiency (CTE) of the UVIS detector has inevitably been declining over time as on-orbit radiation damage creates charge traps in the CCDs. Faint sources in particular can suffer large flux losses or even be lost entirely if observations are not planned and analyzed carefully. The CTE loss will depend on the morphology of the source, the distribution of electrons in the field of view (from sources, background, cosmic rays, and hot pixels) and the population of charge traps in the detector column between the source and the transfer register. And the magnitude of the CTE loss increases continuously with time as new charge traps form. 

CTE is typically measured as a pixel-transfer efficiency, and would be unity for a perfect CCD. One indicator of CTE is the Extended Pixel Edge Response (EPER). Inefficient transfer of electrons in a flat-field exposure produces an exponential tail of charge in the overscan region. Analysis of monitoring observations through January 2013 shows that CTE continues to decline linearly over time (WFC3 ISR 2013-03). For further updates, see the CTE section of the WFC3 Performance Monitoring webpage.


Unit Conversion to Electrons
----------------------------

The UVIS image is multiplied by gain right after BIASCORR, converting it to
ELECTRONS. This step is no longer embedded within FLATCORR.


Dark Current Subtraction (DARKCORR)
-----------------------------------

It uses DARKFILE for the reference dark image.

The UVIS Dark image is now scaled by EXPTIME and FLASHDUR.


Post-Flash Correction (FLSHCORR)
--------------------------------

Post-flash correction is now performed after DARKCORR in the WF32D step.
When FLSHCORR=PERFORM, it uses FLSHFILE (the post-flash reference file).


FLATCORR
--------

Conversion from DN to ELECTRONS no longer depends on FLATCORR=PERFORM. Unit
conversion is done for all exposures after BIASCORR.


Photometry Keywords (PHOTCORR)
------------------------------

The PHOTCORR step is now performed using tables of precomputed values instead
of calls  to SYNPHOT. The correct table for a given image must be specified
in the IMPHTTAB header keyword in order for calwf3 to perform the PHOTCORR step.
By default, it should be in the ``iref`` directory and have the suffix
``_imp.fits``. Each DETECTOR uses a different table.

If you do not wish to use this feature, set PHOTCORR to OMIT.
If you intend to use FLUXCORR, then PHOTCORR must be set to PERFORM as well.


Flux normalization for UVIS1 and UVIS2 (FLUXCORR)
-------------------------------------------------
The FLUXCORR step was added in calwf3 v3.2.1 as a way to scale the UVIS chips 
so that they will produce the same flux when converted to electrons. This requires new keywords 
which specify new PHOTFLAM values to use for each chip as well as a keyword to specify the scaling factor 
for the chips. New flatfields must be used and will replace the old flatfields in CDBS but the change will
not be noticable to users. Users should be aware that flatfield images used in conjunction with v3.2.1
of the software should not be used with older versions as the data will be scaled incorrectly. 

The new keywords include:

PHTFLAM1: The FLAM for UVIS 1 
PHTFLAM2: The FLAM for UVIS 2
PHTRATIO: The ratio: PHTFLAM2 / PHTFLAM1, which is calculated by calwf3 and is multiplied with UVIS2 (SCI,1 in the data file)

In order for FLUXCORR to work the value of PHOTCORR must also be set to perform since this populates
the header of the data with the keywords FLUXCORR requires to compute the PHTRATIO.


calwf3 Output
-------------

Using RAW as input:

    * flt.fits: output calibrated exposure.
    * ima.fits: output ramp calibration IR exposure.
    
Using ASN as input with WF3REJ:

    * crj.fits: cosmic ray rejected image


