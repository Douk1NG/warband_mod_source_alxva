# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

recalculate_ais_scripts = [
# script_recalculate_ais
# Input: none
# Output: none
#When a lord changes factions
#When a center changes factions
#When a center is captured
#When a marshal is defeated
#Every 23 hours
("recalculate_ais",
    [
      (call_script, "script_init_ai_calculation"),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (assign, reg8, ":faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        #(neg|faction_slot_eq, ":faction_no",  slot_faction_marshall, "trp_player"),
        (call_script, "script_decide_faction_ai", ":faction_no"),
      (try_end),

	  ##diplomacy start+ add support for promoted kingdom ladies
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	  ##diplomacy end+
        (store_troop_faction, ":faction_no", ":troop_no"),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),
    ])
]
