# get the auto update version for the call to teal help
from .version import __version_date__, __version__

# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code

try:
    from stsci.tools import teal
    has_teal = True
except ImportError:
    has_teal = None
    print("Teal not available")

__taskname__ = "wf3ccd"


def wf3ccd(input, output=None, dqicorr="PERFORM", atodcorr="PERFORM",
           blevcorr="PERFORM", biascorr="PERFORM", flashcorr="PERFORM",
           verbose=False, quiet=True, log_func=print):

    """Run the ``wf3ccd.e`` executable as from the shell."""

    call_list = ['wf3ccd.e']
    return_code = None

    if verbose:
        call_list += ['-v', '-t']

    if (dqicorr == "PERFORM"):
        call_list.append('-dqi')

    if (atodcorr == "PERFORM"):
        call_list.append('-atod')

    if (blevcorr == "PERFORM"):
        call_list.append('-blev')

    if (biascorr == "PERFORM"):
        call_list.append('-bias')

    if (flashcorr == "PERFORM"):
        call_list.append('-flash')

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ccd does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ccd can only accept 1 file for"
                      "input at a time: {0}".format(infiles))

    for image in infiles:
        if not os.path.exists(image):
            raise IOError("Input file not found: {0}".format(image))

    call_list.append(input)

    if output:
        call_list.append(str(output))

    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    ec = error_code(return_code)
    if return_code:
        if ec is None:
            print("Unknown return code found!")
            ec = return_code
        raise RuntimeError("wf3ccd.e exited with code {}".format(ec))


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


def run(configobj=None):
    """
    TEAL interface for the ``wf3ccd`` function.

    """
    wf3ccd(configobj['input'],
           output=configobj['output'],
           dqicorr=configobj['dqicorr'],
           atodcorr=configobj['atodcorr'],
           blevcorr=configobj['blevcorr'],
           biascorr=configobj['biascorr'],
           flashcorr=configobj['flashcorr'],
           quiet=configobj['quiet'],
           verbose=configobj['verbose'],)

wf3ccd.__doc__ = getHelpAsString(docstring=True)
