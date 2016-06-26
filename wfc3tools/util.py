# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import print_function, division
import warnings
from .version import __version__

__all__ = ["display_help"]

try:
    from stsci.tools import teal
except:
    teal = None


def display_help():
    """ display local html help in a browser window"""
    url = "http://wfc3tools.readthedocs.io/"
    print(url)
    try:
        import webbrowser
        # grab the version that's installed
        if "dev" not in __version__:
            url += "en/{0:s}/".format(__version__)
        webbrowser.open(url)
    except ImportError:
        warnings.warn("webbrowser module not installed, see {0:s} help \
                       pages".format(url))
