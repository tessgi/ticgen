from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import logging, os, __main__
logging.basicConfig()  # Avoid "No handlers could be found for logger" warning
logger = logging.getLogger(__name__)

from .version import __version__

class Highlight:
    # if os.path.basename(__main__.__file__).strip(".py").startswith("wtg"):
    #     RED=GREEN=YELLOW=BLUE=PURPLE=CYAN=END=""
    # else:
        """Defines colors for highlighting words in the terminal."""
        RED = "\033[0;31m"
        GREEN = "\033[0;32m"
        YELLOW = "\033[0;33m"
        BLUE = "\033[0;34m"
        PURPLE = "\033[0;35m"
        CYAN = "\033[0;36m"
        END = '\033[0m'

# this needs to come after the Highlight import
from .ticgen import ticgen, calc_star, Star, ticgen_csv
PACKAGEDIR = os.path.dirname(os.path.abspath(__file__))
