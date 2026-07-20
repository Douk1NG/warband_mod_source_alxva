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

dplmc_get_troop_morality_value_scripts = [
# script_dplmc_time_sorted_heroes_for_center_aux
# INPUT: arg1 = troop_id, arg2 = morality type
# OUTPUT: reg0 has morality value, or 0 if inapplicable
("dplmc_get_troop_morality_value",
	[
		(store_script_param, ":troop_id", 1),
		(store_script_param, ":morality_type", 2),

		(assign, reg0, 0),
		(try_begin),
			(neg|is_between, ":troop_id", companions_begin, companions_end),#<-- result is 0 for non-companions
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_morality_type, ":morality_type"),
			(troop_get_slot, reg0, ":troop_id", slot_troop_morality_value),
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_2ary_morality_type, ":morality_type"),
			(troop_get_slot, reg0, ":troop_id", slot_troop_2ary_morality_value),
		(try_end),

	])
]
