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

process_kingdom_parties_ai_scripts = [
# script_get_relation_between_parties
# This is called more frequently than decide_kingdom_parties_ai
# Input: none
# Output: none
#called from triggers
("process_kingdom_parties_ai",
    [
		##diplomacy start+ add support for promoted kingdom ladies
       (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	   ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (gt, ":party_no", 0),
         (call_script, "script_process_hero_ai", ":troop_no"),
       (try_end),
  ])
]
