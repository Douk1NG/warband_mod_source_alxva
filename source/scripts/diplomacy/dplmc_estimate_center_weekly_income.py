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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_estimate_center_weekly_income_scripts = [
##"script_dplmc_helper_get_troop1_troop2_family_slot_aux"
#
#  INPUT:  arg1   :center_no
# OUTPUT:  reg0   estimated value of weekly income
#
#TODO: Add a better explanation for why this function does not include tarrifs.
("dplmc_estimate_center_weekly_income", [
		(store_script_param_1, ":center_no"),
		(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
		(try_begin),
		  #If there is some sort of aberration, assign to 50 instead of
		  #clamping, on the assumption that the value bears no relation
		  #to the true prosperity at all.
		  (neg|is_between, ":prosperity", 0, 101),
		  (assign, ":prosperity", 50),
		(try_end),
		(store_add, reg0, 20, ":prosperity"),
		(val_mul, reg0, 1200),
		(val_div, reg0, 120),
		(try_begin),
		  (party_slot_eq, ":center_no", slot_party_type, spt_town),
		  #Towns have higher base rent than castles and villages
		  (val_mul, reg0, 2),
		  #Include town garrison allowance
		  (val_mul, ":prosperity", 15),
		  (val_add, ":prosperity", 700),
		  (val_mul, ":prosperity", 3),
		  (val_div, ":prosperity", 2),
		  (val_add, reg0, ":prosperity"),
		(else_try),
		  (party_slot_eq, ":center_no", slot_party_type, spt_castle),
		  #Include castle garrison allowance
		  (val_mul, ":prosperity", 15),
		  (val_add, ":prosperity", 700),
		  (val_add, reg0, ":prosperity"),
		(try_end),
		#At this point, the final result is in reg0.
	])
]
