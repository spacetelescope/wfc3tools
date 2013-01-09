"""
The wfc3tools module contains a function ``calwf3`` that calls the CALWF3 executable.
Use this function to facilitate batch runs or for the TEAL interface.

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
The current WFC3 Data Handbook can be found at  http://www.stsci.edu/hst/wfc3/documents/handbookd/currentDHB/ .  
In the meantime, if you have questions not answered in this documentation, please contact STScI Help Desk (help[at]stsci.edu). 


Running calwf3
--------------

``calwf3`` can be run on a single input raw file or an asn table listing the members of an associtaion. 
When processing an association, it retrieves calibration switch and reference file keyword settings from 
the first image listed in the asn table. ``calwf3`` does not accept a user-defined list of input images on the 
command line (e.g. ``*raw.fits`` to process all raw files in the current directory).

The ``wf3ccd``, ``wf32d``, and ``wf3ir`` tasks on the other hand, will accept such user-defined input file lists, 
but they will not accept an association table( asn ) as input.


Where to Find calwf3
--------------------

``calwf3`` is now part of HSTCAL package, which can be downloaded from
http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas


Usage
-----

From the command line::

   calwf3.e iaa001kaq_raw.fits [command line options]


Command Line Options
--------------------

``calwf3`` supports several command line options:

* -t

  * Print verbose time stamps.
  
* -s

  * Save temporary files.
  
* -v

  * Turn on verbose output.
  
* -d

  * Turn on debug output.
  
* -q

  * Turn on quiet output.
  
* -r
   
  * Print the current software version number (revision)

* --version

  * Print the current software version



Batch calwf3
------------

The recommended method for running ``calwf3`` in batch mode is to use Python and
the ``wfc3tools`` package in the "STSDAS distribution
<http://www.stsci.edu/institute/software_hardware/stsdas/download-stsdas>."

For example::

    from wfc3tools import calwf3
    import glob

    for fits in glob.iglob('j*_raw.fits'):
        calwf3.calwf3(fits)
   



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


calwf3 Output
-------------

Using RAW as input:

    * flt.fits: output calibrated exposure.
    * ima.fits: output ramp calibration IR exposure.
    
Using ASN as input with WF3REJ:

    * crj.fits: cosmic ray rejected image
"""

# STDLIB
import os.path
import subprocess

#STSCI
from stsci.tools import parseinput
try:
    from stsci.tools import teal
except:
    teal = None
    
__taskname__ = "calwf3"
__version__ = "1.0"
__vdate__ = "03-Jan-2013"


def calwf3(input, printtime=False, save_tmp=False,
           verbose=False, debug=False ):
    """

    Run the 'calwf3.e' executable as from the shell. For more information on CALWF3
    see the WFC3 Data Handbook at http://www.stsci.edu/hst/wfc3/documents/handbooks/currentDHB/


    Parameters:
    
        input : str
            Name of input file.

        printtime : bool, optional
            Set to True to turn on the printing of time stamps.

        save_tmp: bool, optional
            Set to True to have CALWF3 save temporary files.

        verbose : bool, optional
            Set to True for verbose output.

        debug : bool, optional
            Set to True to turn on debugging output.


    """
    call_list = ['calwf3.e']

    if printtime:
        call_list.append('-t')

    if save_tmp:
        call_list.append('-s')

    if verbose:
        call_list.append('-v')

    if debug:
        call_list.append('-d')


    if not os.path.exists(input):
        raise IOError('Input file not found: ' + input)

    call_list.append(input)

    subprocess.call(call_list)


def getHelpAsString():
    """
    Returns documentation on the 'calwf3' function. Required by TEAL.

    """
    return calwf3.__doc__


def run(configobj=None):
    """
    TEAL interface for the 'calwf3' function.

    """
    calwf3(configobj['input'],
           printtime=configobj['printtime'],
           save_tmp=configobj['save_tmp'],
           verbose=configobj['verbose'],
           debug=configobj['debug'])


