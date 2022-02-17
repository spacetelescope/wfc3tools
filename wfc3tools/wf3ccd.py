# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code


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
