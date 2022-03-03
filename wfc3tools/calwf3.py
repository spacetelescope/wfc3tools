# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput
from .util import error_code

__taskname__ = "calwf3"


def calwf3(input=None, output=None, printtime=False, save_tmp=False,
           verbose=False, debug=False, parallel=True, version=False,
           log_func=print):

    call_list = ['calwf3.e']
    return_code = None

    if version and input is None:
        call_list.append('-r')
    else:
        if printtime:
            call_list.append('-t')

        if save_tmp:
            call_list.append('-s')

        if verbose:
            call_list.append('-v')

        if debug:
            call_list.append('-d')

        if not parallel:
            call_list.append('-1')

        infiles, dummy = parseinput.parseinput(input)
        if len(parseinput.irafglob(input)) == 0:
            raise IOError("No valid image specified")
        if len(parseinput.irafglob(input)) > 1:
            raise IOError("calwf3 can only accept 1 file for"
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
    if ec:
        if ec is None:
            print("Unknown return code found!")
            ec = return_code
        raise RuntimeError("calwf3.e exited with code {}".format(ec))
