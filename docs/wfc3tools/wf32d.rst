.. _wf32d:


*****
wf32d
*****

Use this function to facilitate batch runs or for the TEAL interface.

The wf32d primary functions include:
  * DARKCORR: dark current subtraction
  * FLATCORR: flat-fielding
  * PHOTCORR: photometric keyword calculations
  * FLUXCORR: photometric normalization of the UVIS1 and UVIS2 chips

Only those steps with a switch value of PERFORM in the input files will be executed, after which the switch
will be set to COMPLETE in the corresponding output files.

Examples
========

In Python without TEAL:

.. code-block:: python

    from wfc3tools import wf32d
    wf32d(filename)

In Python with TEAL:

.. code-block:: python

    from stsci.tools import teal
    from wfc3tools import wf32d
    teal.teal('wf32d')

In Pyraf:

.. code-block:: python

    import wfc3tools
    epar wf32d



Parameters
==========

    input: str
        Name of input files

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``)

    output: str
        Name of the output FITS file.

    dqicorr: str, "PERFORM/OMIT", optional
        Update the dq array from bad pixel table

    darkcorr: str, "PERFORM/OMIT", optional
        Subtract the dark image

    flatcorr: str, "PERFORM/OMIT", optional
        Multiply by the flatfield image

    shadcorr: str, "PERFORM/OMIT", optional
        Correct for shutter shading (CCD)

    photcorr: str, "PERFORM/OMIT", optional
        Update photometry keywords in the header

    fluxcorr; str, "PERFORM/OMIT", optional
        Perform chip photometry normalization

    verbose: bool, optional
        Print verbose time stamps?

    quiet: bool, optional
        Print messages only to trailer file?


Command Line Options for the wf32d executable
=============================================

.. code-block:: shell

    wf32d.e input output [-options]

input may be a single filename

Where the options include:

* -v: verbose
* -f: print time stamps
* -d: debug
* -dark: perform dark subtraction
* -dqi: update the DQ array
* -flat: perform flat correction
* -shad: perform shading correction
* -phot: perform phot correction
