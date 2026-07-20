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

init_troop_age_scripts = [
("init_troop_age",
	[
	(store_script_param, ":troop_no", 1),
	(store_script_param, ":age", 2), #minimum 20

	(try_begin),
		(gt, ":age", 20),
		(troop_set_slot, ":troop_no", slot_troop_age, 20),
	(else_try),
		(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(try_end),

	(store_sub, ":years_to_age", ":age", 20),
    (troop_set_age, ":troop_no", 0),

	(try_begin),
		(gt, ":years_to_age", 0),
		(try_for_range, ":unused", 0, ":years_to_age"),
			(call_script, "script_age_troop_one_year", ":troop_no"),
		(try_end),
	(try_end),

	])
]
