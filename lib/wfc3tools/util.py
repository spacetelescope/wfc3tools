# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import print_function, division

__all__ = ["display_help"]


def display_help():
    """ display local html help in a browser window"""
    try:
        import webbrowser
    except ImportError:
        warnings.warn(
            "webbrowser module not installed, see the installed doc directory for the HTML help pages")
        raise ImportError

    # get the user installed location of the html docs, better way?
    from . import htmlhelp
    location = (htmlhelp.__file__).split("/")
    location.pop()
    location.append("index.html")
    url = "file://" + "/".join(location)
    webbrowser.open(url)

