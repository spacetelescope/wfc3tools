import pytest

from wfc3tools import calwf3


def test_no_valid_input(_jail):
    """Run a very simple aliveness test."""
    with pytest.raises(IOError, match="No valid image specified"):
        calwf3()


def test_version_print(_jail):
    """Make sure no error results from version print."""
    calwf3(version=True)
