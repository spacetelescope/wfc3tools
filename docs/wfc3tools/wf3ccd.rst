.. _wf3ccd:

wf3ccd
======

.. automodapi:: wfc3tools.wf3ccd

Command Line Options for the ``wf3ccd`` executable
--------------------------------------------------

The wf3ccd function can also be called directly from the OS command line:

.. code-block:: shell

    wf32ccd.e input output [-options]

Input may be a single filename, and the options include:

* -v: verbose
* -t: print time stamps
* -dqi: udpate the DQ array
* -atod: perform a-to-d gain correction
* -blev: subtract bias from overscan
* -bias: perform bias correction
* -flash: remove post-flash image
