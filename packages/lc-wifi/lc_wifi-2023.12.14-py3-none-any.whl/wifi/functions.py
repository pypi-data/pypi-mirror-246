"""Generating the WiFiFunctions Product Class Tree From All The Components"""

from wifi.connections import connections  # noqa defines the connections.

from wifi.core.enforce import forced_actions, lookup
from wifi.api import api2
from wifi.core import WiFiFunctions
from wifi.usp import usp  # patches api2
from wifi.usp.tools import tools
from wifi.usp.provisioning import USPProvisioning as provisioning


WiFiFunctions.lookup = lookup
WiFiFunctions.forced_actions = forced_actions
WiFiFunctions.api2 = api2
WiFiFunctions.usp = usp
WiFiFunctions.usp.tools = tools
WiFiFunctions.provisioning = provisioning
