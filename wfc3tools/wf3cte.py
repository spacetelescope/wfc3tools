"""Run wf3cte step in calwf3."""

import subprocess

from stsci.tools import parseinput

__all__ = ["wf3cte"]


def wf3cte(input, parallel=True, verbose=False, log_func=print):
    """
    Run the ``wf3cte.e`` executable as from the shell.

    This routine performs the CTE correction on raw data files. The calibration
    step keyword is PCTECORR; if this is set to PERFORM, then the CTE correction
    will be applied to the dataset.

    Parameters
    ----------
    input : str or list
        Name of input files, such as:

        - a single filename (``iaa012wdq_raw.fits``)
        - a Python list of filenames
        - a partial filename with wildcards (``*raw.fits``)
        - an at-file (``@input``)

    parallel : bool, optional
        If `True`, run the code with OpemMP parallel processing turned on for the
        UVIS CTE correction. Default is `True`.

    verbose: bool, optional
        If True, print verbose time stamps. Default is `False`.

    log_func : func
        By default, the print function is used for logging to facilitate
        use in the Jupyter notebook.

    Examples
    --------
    >>> from wfc3tools import wf3cte
    >>> filename = '/path/to/some/wfc3/image.fits'
    >>> wf3cte(filename)

    """

    call_list = ["wf3cte.e"]

    if verbose:
        call_list.append("-v")

    if not parallel:
        call_list.append("-1")

    infiles, dummy_out = parseinput.parseinput(input)
    call_list.append(",".join(infiles))

    print(call_list)

    proc = subprocess.Popen(
        call_list,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if log_func is not None:
        for line in proc.stdout:
            log_func(line.decode("utf8"))

    return_code = proc.wait()
    if return_code != 0:
        raise RuntimeError("wf3cte.e exited with code {}".format(return_code))
