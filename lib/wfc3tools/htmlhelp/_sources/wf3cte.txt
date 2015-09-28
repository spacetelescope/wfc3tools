======
wf3cte
======

This routine perform CTE correction on raw data files. These steps are:

    * pctecorr - initializing the data quality array
    

CTE corrections can *ONLY* be performed on RAW data which has not been calibrated in any way.
Data which have already been through BLEVCORR, BIASCORR or DARKCORR will be rejected.
 
The standalone call make a *_rac.fits file by default.

Example
--------

    In Python without TEAL:

    >>> from wfc3tools import wf3cte
    >>> calwf3.wf3cte(filename)

    In Python with TEAL:

    >>> from stsci.tools import teal
    >>> from wfc3tools import wf3cte
    >>> teal.teal('wf3cte')

    In Pyraf:

    >>> import wfc3tools
    >>> epar wf3cte

Parameters
----------

    input : str
        Name of input files

            * a single filename (``iaa012wdq_raw.fits``)
            * a Python list of filenames
            * a partial filename with wildcards (``\*raw.fits``)
            * filename of an ASN table (``\*asn.fits``)
            * an at-file (``@input``) 

    -1 : value, as in minus one, this will make sure only 1 processor/thread is used during processing, otherwise all available are used.

    verbose: bool, optional
        Print verbose time stamps?


**The wf3cte function can also be called directly from the OS command line:**

>>> wf3cte.e input  [-options]

Where the OS options include:

* -v: verbose
* -1: turn off multiprocessing

