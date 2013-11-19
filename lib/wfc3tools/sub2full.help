========
sub2full
========

Given an image specified by the user which contains a subarray readout, return the location of the corner of the subarray in a full frame reference image.


USAGE 
-----

    >>> python
    >>> from wfc3tools import sub2full
    >>> coords=sub2full.sub2full(filename,x=None, y=None,fullExtent=False)


PARAMETERS
----------
    
    filename [file]
        Input image name or list of image names. The rootname will be used to find the _RAW and _SPT
	files in the same directory
    
    x = None [integer] Optional
        Specify an x coordinate in the subarray to translate
	If an x and y are specified, the fullExtent option is turned off and only the translated x,y coords are returned

    y = None [integer] Optional
        Specify a y coordinate in the subarray to translate
        If an x and y are specified, the fullExtent option is turned off and only the translated x,y coords are returned

    fullExtent = False [bool] Optional
    	If set, the returned values will include the full extent of the subarray in the reference image
	For example: (x0,x1,y0,y1)


RETURNS
-------

A list of tuples which specify the translated coordinates, either (x0,y0) for each image or the full extent sections

Example Output
--------------

Default output:

::


    > sub2full('ibbso1fdq_flt.fits')
    > [(3584.0, 1539)]


Optional output:

::


    Specify a list of images:
    
    >im = ['ic5p02e0q_spt.fits',
           'ic5p02e1q_spt.fits',
           'ic5p02e2q_spt.fits',
           'ic5p02e3q_spt.fits',
           'ic5p02e4q_spt.fits']
    >
    > sub2full(im)
    >[(1062.0, 1363),
    > (1062.0, 1363),
    > (1410.0, 1243),
    > (1410.0, 1243),
    > (1402.0, 1539)]


    Return the full extent of the subarray:
    
    > sub2full('ibbso1fdq_flt.fits',fullExtent=True)
    >[(3584.0, 4096, 1539, 2050)]
