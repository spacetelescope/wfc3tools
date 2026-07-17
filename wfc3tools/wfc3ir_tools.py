import glob
import os

import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats

from wfc3tools import calwf3

__all__ = ["make_flattened_ramp_flt"]


def _reprocess_raw_crcorr(raw_file):
    """Utilize calwf3 to make IMA from RAW, turning CRCORR switch off.

    Output FLT, FLC, and TRA are deleted after calwf3 completes.
    The IMA file is the "flattened" version but it is not renamed.

    Parameters
    ----------
    raw_file : str
        RAW file to process.

    Returns
    -------
    ima_file : str
        IMA file created.
    """
    rootname = os.path.basename(raw_file)[0:9]

    with fits.open(raw_file, mode="update") as raw_hdu:
        orig_crcorr = raw_hdu[0].header["CRCORR"]
        raw_hdu[0].header["CRCORR"] = "OMIT"
        asn_tab = raw_hdu[0].header["ASN_TAB"]

        # TODO: Remove this block to make dummy ASN when calwf3 is patched.
        if asn_tab == "NONE":
            asn_tab = "dummy_asn.fits"
            new_asn_tab = np.rec.array(
                [(rootname, "EXP-DTH", 1)], formats="S14,S14,i1", names="MEMNAME,MEMTYPE,MEMPRSNT"
            )
            hdu_1 = fits.BinTableHDU(new_asn_tab)
            none_hdu_list = fits.HDUList([raw_hdu[0], hdu_1])
            none_hdu_list.writeto(asn_tab, overwrite=True)

    # If part of an association, assert ASN is in same directory as RAW
    # so we can catch error now because IMA cannot run though the pipeline without the ASN.
    if not os.path.isfile(asn_tab):
        raise OSError(f"{asn_tab} must be in same directory as RAW file.")

    # Remove any outputs from previous run so calwf3 does not crash.
    for ext in ("flt", "flc", "ima"):
        f = f"{rootname}_{ext}.fits"
        if os.path.isfile(f):
            os.remove(f)

    # Run calwf3
    calwf3(raw_file)

    # Removing resulting FL? and TRA, we just want IMA generated with CRCORR off
    for ext in ("flt", "flc"):
        f = f"{rootname}_{ext}.fits"
        if os.path.isfile(f):
            os.remove(f)
    f = f"{rootname}.tra"
    if os.path.isfile(f):
        os.remove(f)

    # Restore original CRCORR
    with fits.open(raw_file, mode="update") as raw_hdu:
        raw_hdu[0].header["CRCORR"] = orig_crcorr

    return f"{rootname}_ima.fits"


def _calc_avg(data, stats_method, sigma_clip, sigma, sigma_upper, sigma_lower, iters):
    """Returns a mean or median from an array, with optional sigma clipping."""
    if not sigma_clip:
        if stats_method == "median":
            return np.median(data)
        return np.mean(data)
    else:
        mean, med, s = sigma_clipped_stats(data, sigma=sigma, sigma_lower=sigma_lower, sigma_upper=sigma_upper, iters=iters)
        if stats_method == "median":
            return med
        return mean


def make_flattened_ramp_flt(
    raw_file,
    stats_subregion=None,
    stats_method="median",
    sigma_clip=False,
    sigma=None,
    sigma_upper=None,
    sigma_lower=None,
    iters=None,
):
    """
    Corrects for non-variable background and produce a 'flattened' FLT and IMA.

    This function must run in the working directory with data files.
    CRCORR value in RAW will be temporarily changed; if you are worried about the
    integrity of RAW contents, please keep a pristine copy elsewhere.

    Users supply a RAW file, which is used to create an IMA file with calwf3 with the CRCORR
    switch set to OMIT. Then, the average background level from each read of the IMA is
    subtracted from the read, and later added back to the full exposure to preserve pixel
    statistics. Finally, calwf3 is run again on the flattened IMA to produce an FLT.

    Note that if the RAW file is part of an association, the ASN file must be in the
    same directory as the RAW file. If ASN_TAB is NONE, a dummy ASN file will be created
    in the working directory.

    Users may provide a region for the median to be computed, otherwise this
    will default to the median over the whole image excluding the 5 pixel overscan
    region on the border.

    The following output files will be created:

    * ``dummy_asn.fits`` (if dummy ASN is needed for processing)
    * ``<rootname>_ima.fits`` (flattened IMA as described above)
    * ``<rootname>_flt.fits`` (FLT from flattened IMA)
    * ``<rootname>_flc.fits`` (if PCTECORR is done)
    * ``<rootname>.tra`` (trailer file from calwf3 run on flattened IMA)

    Parameters
    -----------
    raw_file : str
        RAW filename.
    stats_subregion : tuple or None
        Tuple of ``((xmin, xmax), (ymin, ymax))`` to specify region for average calculation.
        Defaults to whole image, excluding the 5-pixel overscan region.
    stats_method : str
        Method of stats computation on each read when subtracting the average to flatten.
        Must be 'mean' or 'median'. Defaults to 'median'.
    sigma_clip : bool
        If `True`, data will be sigma-clipped when computing stats. Defaults to `False`.
    sigma : int or None
        The number of standard deviations to use as the lower
        and upper clipping limit. This is ignored when ``sigma_clip=False`` and
        must be set to a number if ``sigma_clip=True``. Defaults to `None`.
    sigma_upper : int or None
        The number of standard deviations to use as the upper bound for the clipping
        limit. This is ignored when ``sigma_clip=False``. If `None` when
        ``sigma_clip=True``, then the value of ``sigma`` is used. Defaults to `None`.
    sigma_lower : int or None
        The number of standard deviations to use as the lower bound for the clipping
        limit. This is ignored when ``sigma_clip=False``. If `None` when
        ``sigma_clip=True``, then the value of ``sigma`` is used. Defaults to `None`.
    iters : int or None
        The number of iterations to perform sigma clipping. This is ignored when
        ``sigma_clip=False`` and must be set to a number if ``sigma_clip=True``.
        Defaults to `None`.
    """
    if stats_method not in ("median", "mean"):
        raise ValueError("stats_method must be mean or median")

    if sigma_clip and not sigma and (not sigma_upper or not sigma_lower):
        raise ValueError("Must set sigma, or both sigma_upper and sigma_lower.")

    # Run calwf3 without CRCORR to make IMA
    ima_file = _reprocess_raw_crcorr(raw_file)

    # Update the new flattened IMA
    with fits.open(ima_file, mode="update") as ima_hdu:
        sci_1_header = ima_hdu["SCI", 1].header
        naxis1 = sci_1_header["NAXIS1"]
        naxis2 = sci_1_header["NAXIS2"]

        # Default to whole image minus the 5 overscan pixels
        if stats_subregion is None:
            xmin = ymin = 5
            xmax = naxis1
            ymax = naxis2
        else:  # ((xmin, xmax), (ymin, ymax))
            xmin = stats_subregion[0][0]
            xmax = stats_subregion[0][1]
            ymin = stats_subregion[1][0]
            ymax = stats_subregion[1][1]
        slx = slice(xmin, xmax)
        sly = slice(ymin, ymax)

        # Subtract per-read median countrate scalar and add back in full exposure countrate
        # to preserve pixel statistics
        total_countrate = _calc_avg(
            ima_hdu["SCI", 1].data[sly, slx], stats_method, sigma_clip, sigma, sigma_upper, sigma_lower, iters
        )

        for i in range(2, ima_hdu[0].header["NSAMP"] + 1):
            ext = ("SCI, i)
            avg = _calc_avg(ima_hdu[ext].data[sly, slx], stats_method, sigma_clip, sigma, sigma_upper, sigma_lower, iters)
            ima_hdu[ext].data += total_countrate - avg

        # Turn on ramp fitting
        ima_hdu[0].header["CRCORR"] = "PERFORM"

    # Run calwf3 on modified IMA
    calwf3(ima_file)
