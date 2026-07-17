import pytest

from wfc3tools import calwf3

# Mark all tests in this module:
# Even if test does not use data, it needs HSTCAL to be installed
# and that is only available on RegressionTests workflow.
pytestmark = [pytest.mark.bigdata]


def test_no_valid_input(_jail):
    """Run a very simple aliveness test."""
    with pytest.raises(IOError, match="No valid image specified"):
        calwf3()


def test_version_print(_jail):
    """Make sure no error results from version print."""
    calwf3(version=True)
