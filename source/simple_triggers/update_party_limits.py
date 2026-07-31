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



  # Make parties larger as game progresses.
  

update_party_limits_simple_triggers = [
(24,
   [
       (call_script, "script_update_party_creation_random_limits"),
    ]),
]
