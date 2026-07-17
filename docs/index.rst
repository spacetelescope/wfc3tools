.. wfc3tools documentation master file, created by
   sphinx-quickstart on Wed Dec 12 16:53:43 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################
WFC3 Python User Tools
######################

See the `WFC3 Team website  <https://www.stsci.edu/hst/wfc3/>`_ and the
`WFC3 Data Handbook <https://hst-docs.stsci.edu/wfc3dhb>`_ for more information.

*****************
Pipeline Software
*****************

A subset of the tools in the WFC3TOOLS package allows the user to employ
the same software that STScI uses in the science calibration pipelines
to calibrate WFC3 data from both the UVIS and IR detectors.  This means
the user can reprocess data with the latest software releases and/or reference
files at will.  This also means the user can customize the actual calibrations
applied to the data by modifying the settings (e.g., OMIT vs PERFORM) of
calibration steps in the primary header of the RAW FITS file.

The set of calibration tools resident in the WFC3TOOLS package are actually
thin Python wrappers around C executables.  While the C code is
performing the heavy lifting, the Python wrapper acts as a convenience
front-end function for the C code.  In order to use the Python tools
which are actually wrappers, the user must also obtain the HSTCAL package
which contains the C version of the pipeline programs.

.. note::

    While a calibration tool will be referenced generically in this discussion as,
    for example, ``calwf3``, the file actually being executed in C is ``calwf3.e`` and
    in Python is ``calwf3.py``.

.. toctree::
   :maxdepth: 2

   wfc3tools/calwf3.rst
   wfc3tools/wf3cte.rst
   wfc3tools/wf3ccd.rst
   wfc3tools/wf32d.rst
   wfc3tools/wf3ir.rst
   wfc3tools/wf3rej.rst

**************
Analysis Tools
**************

.. toctree::
   :maxdepth: 2

   wfc3tools/embedsub.rst
   wfc3tools/pstack.rst
   wfc3tools/pstat.rst
   wfc3tools/sampinfo.rst
   wfc3tools/sub2full.rst
   wfc3tools/wfc3ir_tools.rst
   wfc3tools/utils.rst

* :ref:`genindex`
* :ref:`modindex`
