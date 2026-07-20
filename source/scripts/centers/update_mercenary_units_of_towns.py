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

update_mercenary_units_of_towns_scripts = [
#script_update_mercenary_units_of_towns
# INPUT: none
# OUTPUT: none
("update_mercenary_units_of_towns",
    [(try_for_range, ":town_no", towns_begin, towns_end),
      (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
      (party_set_slot, ":town_no", slot_center_mercenary_troop_type, ":troop_no"),
      (store_random_in_range, ":amount", 3, 8),
	  ##diplomacy start+
	  #OPTIONAL CHANGE: The same way that lord party sizes increase as the player
	  #progresses, also increase mercenary party sizes to maintain their relevance.
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
		 (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
		 (store_add, ":level_factor", 80, ":level"),
         (val_mul, ":amount", ":level_factor"),
         (val_div, ":amount", 80),
	  (try_end),
	  ##diplomacy end+
      (party_set_slot, ":town_no", slot_center_mercenary_troop_amount, ":amount"),
    (try_end),
     ])
]
