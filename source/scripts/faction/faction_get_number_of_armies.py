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

faction_get_number_of_armies_scripts = [
# script_faction_get_number_of_armies
# Input: arg1 = faction_no
# Output: reg0 = number_of_armies
("faction_get_number_of_armies",
   [
      (store_script_param_1, ":faction_no"),
      (assign, ":num_armies", 0),
      ##diplomacy start+ support for promoted kingdom ladies
      (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- changed from active_npcs to heroes
      ##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
    	(store_troop_faction, ":hero_faction_no", ":troop_no"),
        (eq, ":hero_faction_no", ":faction_no"),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
        (ge, ":hero_party", 0),
        (party_is_active, ":hero_party"),
        (call_script, "script_party_count_fit_regulars", ":hero_party"),
        (assign, ":party_size", reg0),
        (call_script, "script_party_get_ideal_size", ":hero_party"),
        (assign, ":ideal_size", reg0),
        (val_mul, ":ideal_size", 60),
        (val_div, ":ideal_size", 100),
        (gt, ":party_size", ":ideal_size"),
        (val_add, ":num_armies", 1),
      (try_end),
      (assign, reg0, ":num_armies"),
    ])
]
