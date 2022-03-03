# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code

__taskname__ = "wf3ir"


def wf3ir(input, output=None, verbose=False, quiet=True, log_func=print):
    """Call the wf3ir.e executable """

    call_list = ['wf3ir.e']
    return_code = None

    if verbose:
        call_list += ['-v', '-t']

    infiles, dummy = parseinput.parseinput(input)
    if "_asn" in input:
        raise IOError("wf3ir does not accept association tables")
    if len(parseinput.irafglob(input)) == 0:
        raise IOError("No valid image specified")
    if len(parseinput.irafglob(input)) > 1:
        raise IOError("wf3ir can only accept 1 file for"
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
        raise RuntimeError("wf3ir.e exited with code {}".format(ec))
