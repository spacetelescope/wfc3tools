"""The wfc3tools package holds Python tasks useful for analyzing WFC3 data."""

# HSTCAL
from .calwf3 import calwf3
from .wf32d import wf32d
from .wf3ccd import wf3ccd
from .wf3cte import wf3cte
from .wf3ir import wf3ir
from .wf3rej import wf3rej

# Python tools
from .embedsub import embedsub
from .pstack import pstack
from .pstat import pstat
from .sampinfo import sampinfo
from .sub2full import sub2full
from .util import display_help
from .wfc3ir_tools import make_flattened_ramp_flt

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''
