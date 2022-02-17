# STDLIB
import os.path
import subprocess

# STSCI
from stsci.tools import parseinput

__taskname__ = "wf3cte"


def wf3cte(input, out=None, parallel=True, verbose=False, log_func=print):

    """Run the ``wf3cte.e`` executable as from the shell."""

    call_list = ['wf3cte.e']

    if verbose:
        call_list.append('-v')

    if not parallel:
        call_list.append('-1')

    infiles, dummy_out = parseinput.parseinput(input)
    call_list.append(','.join(infiles))
    if out:
        call_list.append(str(out))

    print(call_list)
    
    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode('utf8'))

    return_code = proc.wait()
    if return_code != 0:
        raise RuntimeError("wf3cte.e exited with code {}".format(return_code))
