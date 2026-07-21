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

evaluate_realm_stability_scripts = [
# script_music_set_situation_with_culture
#fairly expensive in terms of CPU
("evaluate_realm_stability",

    [
	(store_script_param, ":realm", 1),

	(assign, ":total_lords", 0),
	(assign, ":total_restless_lords", 0),
	(assign, ":total_disgruntled_lords", 0),

	(faction_get_slot, ":liege", ":realm", slot_faction_leader),

	(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_troop_faction, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":realm"),
		(val_add, ":total_lords", 1),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord", ":liege"),
		(try_begin),
			(le, reg3, -10),
			(val_add, ":total_disgruntled_lords", 1),
		(else_try),
			(le, reg3, 10),
			(val_add, ":total_restless_lords", 1),
		(try_end),
	(try_end),

	(try_begin),
		(gt, ":total_lords", 0),
		(store_mul, ":instability_quotient", ":total_disgruntled_lords", 100),
		(val_div, ":instability_quotient", ":total_lords"),

		(store_mul, ":restless_quotient", ":total_restless_lords", 100),
		(val_div, ":restless_quotient", ":total_lords"),

		(store_mul, ":combined_quotient", ":instability_quotient", 2),
		(val_add, ":combined_quotient", ":restless_quotient"),
		(faction_set_slot, ":realm", slot_faction_instability, ":combined_quotient"),

		(assign, reg0, ":instability_quotient"),
		# (assign, reg1, ":restless_quotient"),
		(assign, reg1, ":restless_quotient"),
	(else_try),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s1, ":realm"),
			(display_message, "str_s1_has_no_lords"),
		(try_end),
		(assign, reg0, 0),
		(assign, reg1, 0),
	(try_end),

	])
]
