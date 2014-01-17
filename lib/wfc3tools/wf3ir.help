=====
wf3ir
=====

Use this function to facilitate batch runs or for the TEAL interface.

This routine contains all the instrumental calibration steps for WFC3 IR channel images. The steps are:

    * dqicorr - initialize the data quality array
    * zsigcorr - estimate the amount of signal in the zeroth-read
    * blevcorr - subtact the bias level from the reference pixels
    * zoffcorr - subtract the zeroth read image
    * nlincorr - correct for detector non-linear response
    * darkcorr - subtract the dark current image
    * photcorr - compute the photometric keyword values
    * unitcorr - convert to units of count rate
    * crcorr - fit accumulating signal and identify the cr hits
    * flatcorr - divide by the flatfield images and apply gain coversion
    
The output images include the calibrated image ramp (ima file) and the accumulated ramp image (flt file)
  
Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Examples
--------
    In Python without TEAL:

    >>> from wfc3tools import wf3ir
    >>> calwf3.wf3ir(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3ir
    >>> teal.teal('wf3ir')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3ir

Parameters
----------

    input : str
        Name of input files

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``) 

    output: str
        Name of the output FITS file.

    verbose: bool, optional
        Print verbose time stamps?

    quiet: bool, optional
        Print messages only to trailer file?


**The wf3ir function can also be called directly from the OS command line:**

>>> wf32ir.e input output [-options]

Where the OS options include:

* -v: verbose
* -f: print time stamps

