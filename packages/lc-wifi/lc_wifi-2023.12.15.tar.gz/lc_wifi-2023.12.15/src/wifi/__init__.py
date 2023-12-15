import sys
import os

# FIXME: the brutal way to get the libs from AXSerbia 1:1 in:
sys.path.insert(0, os.path.dirname(__file__) + '/wifi_libs')

from .functions import WiFiFunctions  # noqa
