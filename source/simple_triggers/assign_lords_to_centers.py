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



  # Assigning lords to centers with no leaders
  

assign_lords_to_centers_simple_triggers = [
(72,
   [
   (neq, "$g_election_date", 45),
   (display_message, "@re-initializing banner info"),
   (call_script, "script_initialize_banner_info"),
   #(assign, "$g_custom_banner_new_game", 0),
   #(call_script, "script_assign_lords_to_empty_centers"),
    ]),
]
