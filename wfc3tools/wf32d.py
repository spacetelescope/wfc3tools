from __future__ import print_function

# get the auto update version for the call to teal help
from .version import __version_date__, __version__

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
try:
    from stsci.tools import teal
    has_teal = True
except ImportError:
    has_teal = False
    print("Teal not available")

__taskname__ = "wf32d"


def wf32d(input, output="", dqicorr="PERFORM", darkcorr="PERFORM",
          flatcorr="PERFORM", shadcorr="PERFORM", photcorr="PERFORM",
          verbose=False, quiet=True, debug=False):
    """  Call the wf32d.e executable."""

    if verbose:
        call_list += ['-v', '-t']

    if debug:
        call_list.append('-d')

    if (darkcorr == "PERFORM"):
        call_list.append('-dark')

    if (dqicorr == "PERFORM"):
        call_list.append('-dqi')

    if (flatcorr == "PERFORM"):
        call_list.append('-flat')

    if (shadcorr == "PERFORM"):
        call_list.append('-shad')

    if (photcorr == "PERFORM"):
        call_list.append('-phot')

    infiles, dummpy_out = parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    call_list.append(str(output))

    subprocess.call(call_list)


def help(file=None):
    helpstr = getHelpAsString(docstring=True)
    if file is None:
        print(helpstr)
    else:
        if os.path.exists(file):
            os.remove(file)
        f = open(file, mode='w')
        f.write(helpstr)
        f.close()


def getHelpAsString(docstring=False):
    """Return documentation on the 'wf3ir' function. Required by TEAL."""

    install_dir = os.path.dirname(__file__)
    htmlfile = os.path.join(install_dir, 'htmlhelp', __taskname__ + '.html')
    helpfile = os.path.join(install_dir, __taskname__ + '.help')
    if docstring or (not docstring and not os.path.exists(htmlfile)):
        helpString = ' '.join([__taskname__, 'Version', __version__,
                               ' updated on ', __version_date__]) + '\n\n'
        if os.path.exists(helpfile) and has_teal:
            helpString += teal.getHelpFileAsString(__taskname__, __file__)
    else:
        helpString = 'file://' + htmlfile

    return helpString


wf32d.__doc__ = getHelpAsString(docstring=True)


def run(configobj=None):
    """
    TEAL interface for the ``wf32d`` function.

    """
    wf32d(configobj['input'],
          output=configobj['output'],
          dqicorr=configobj['dqicorr'],
          darkcorr=configobj['darkcorr'],
          flatcorr=configobj['flatcorr'],
          shadcorr=configobj['shadcorr'],
          photcorr=configobj['photcorr'],
          quiet=configobj['quiet'],
          verbose=configobj['verbose'],
          debug=configobj['debug'])
