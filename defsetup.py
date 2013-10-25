from __future__ import division # confidence high

import sys
import distutils
import distutils.core
import distutils.sysconfig

try:
    import numpy
except:
    raise ImportError('NUMPY was not found. It may not be installed or it may not be on your PYTHONPATH')

pythoninc = distutils.sysconfig.get_python_inc()
numpyinc = numpy.get_include()

pkg =  "wfc3tools"


setupargs = {
    'version' : 		"1.2dev",
    'description' :	    "Python Tools for WFC3 Data",
    'author' : 		    "Megan Sosey",
    'author_email' : 	"help@stsci.edu",
    'license' : 		"http://www.stsci.edu/resources/software_hardware/pyraf/LICENSE",
    'data_files' :      [( pkg+"/pars", ['lib/wfc3tools/pars/*']),( pkg, ['lib/wfc3tools/*.help']),(pkg,['LICENSE.txt'])],
    'scripts' :         [ 'lib/wfc3tools/runastrodriz'] ,
    'platforms' : 	    ["Linux","Solaris","Mac OS X","Win"],
    'package_dir' :     { 'wfc3tools':'lib/wfc3tools', },

}

