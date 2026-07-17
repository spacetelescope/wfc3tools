.. _wf32d:

wf32d
=====

.. automodapi:: wfc3tools.wf32d

Command Line Options for the ``wf32d`` C Executable
---------------------------------------------------

The wf32d function can also be called directly from the OS command line:

.. code-block:: shell

    wf32d.e input output [-options]

Input may be a single filename, and the options include:

* -v: verbose
* -t: print time stamps
* -d: debug
* -dark: perform dark subtraction
* -dqi: update the DQ array
* -flat: perform flat correction
* -shad: perform shading correction
* -phot: perform phot correction
