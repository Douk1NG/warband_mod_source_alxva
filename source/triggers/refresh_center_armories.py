# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *



# Refresh Armor sellers
  

refresh_center_armories_triggers = [
(0.0, 0, 168.0, [],
  [
    (call_script, "script_refresh_center_armories"),
                     ]),
]
