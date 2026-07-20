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

lady_evaluate_troop_as_suitor_scripts = [
("lady_evaluate_troop_as_suitor",
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":lady", ":suitor"),
	(assign, ":romantic_chemistry", reg0),

	(try_begin),
      (call_script, "script_cf_test_lord_incompatibility_to_s17", ":lady", ":suitor"),
    (try_end),

	(store_sub, ":personality_modifier", 0, reg0),
	(assign, reg2, ":personality_modifier"),

	(try_begin),
		(troop_get_slot, ":renown_modifier", ":suitor", slot_troop_renown),
		(val_div, ":renown_modifier", 20),
		(try_begin),
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			(val_mul, ":renown_modifier", 2),
			(val_sub, ":renown_modifier", 15),
		(try_end),
	(try_end),

	(store_add, ":final_score", ":renown_modifier", ":personality_modifier"),
	(val_add, ":final_score", ":romantic_chemistry"),
	(assign, reg0, ":final_score"),
	])
]
