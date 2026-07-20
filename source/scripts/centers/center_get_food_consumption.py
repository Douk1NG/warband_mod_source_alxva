# ======================================================================
# SHARED DEPENDENCY
# Entity: center_get_food_consumption (script)
# Called by menus in 3 domains: diplomacy, reports, siege
# ======================================================================

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

center_get_food_consumption_scripts = [
#script_kill_cattle_from_herd
# Input: arg1 = center_no
# Output: reg0: food consumption (1 food item counts as 100 units)
("center_get_food_consumption",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_consumption", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_consumption", 500),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_consumption", 50),
      (try_end),
      ##diplomacy start+
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 #Optional change: increase food consumption with garrison size
		 #The rationale goes like this:
		 #The average reinforcement size for a town or castle is 9.5 per round.
		 #At the start of the game:
		 #
		 #  Castles get 15 reinforcement rounds, for around 142.5 troops
		 #  Towns   get 40 reinforcement rounds, for around 380 troops
		 #
		 #Of course both the castles and the towns have other people living
		 #there as well.
		 (party_get_num_companions, ":garrison_size", ":center_no"),
		 (try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(gt, ":garrison_size", 150),
			#Assume that the garrison accounts for most of the food consumption.
			(store_div, ":food_consumption", ":garrison_size", 3),
		 (else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(gt, ":garrison_size", 380),
			#Assume that the garrison makes the same contribution to size for towns.
			(store_div, ":food_consumption", ":garrison_size", 3),#for 381, equals 127
			(val_add, ":food_consumption", 500 - 127),
		 (try_end),

		 #Optional change: increase food consumption with prosperity
		 (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (party_get_slot, reg0, ":center_no", slot_town_prosperity),
			(gt, reg0, 50),#<- increase only
         (val_add, reg0, 75),
         (val_mul, ":food_consumption", reg0),
         (val_add, ":food_consumption", 62),
         (val_div, ":food_consumption", 125),
      (try_end),
      ##diplomacy+
      (assign, reg0, ":food_consumption"),
  ])
]
