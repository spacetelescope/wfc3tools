# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code

__taskname__ = "wf32d"


def wf32d(input, output=None, dqicorr="PERFORM", darkcorr="PERFORM",
          flatcorr="PERFORM", shadcorr="PERFORM", photcorr="PERFORM",
          verbose=False, quiet=True, debug=False, log_func=print):
    """  Call the wf32d.e executable."""

    call_list = ['wf32d.e']
    return_code = None

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

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf32d does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf32d can only accept 1 file for"
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
        raise RuntimeError("wf32d.e exited with code {}".format(ec))
