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




  # Decide vassal ai
   

decide_vassal_ai_simple_triggers = [
(7,
    [
      (call_script, "script_init_ai_calculation"),
      #(call_script, "script_decide_kingdom_party_ais"),
	  ##diplomacy start+
	  #Also call script_calculate_troop_ai for kingdom ladies who have become slto_kingdom_heroes
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	  ##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),
      ]),
]
