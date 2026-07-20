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

troop_describes_troop_to_s15_scripts = [
("troop_describes_troop_to_s15",
  [
	(store_script_param, ":troop_1", 1),
	(store_script_param, ":troop_2", 2),


	(str_store_troop_name, s15, ":troop_2"),

	(try_begin),
		(eq, ":troop_2", "trp_player"),
		(str_store_string, s15, "str_you"),
	(else_try),
		(eq, ":troop_2", ":troop_1"),
		(str_store_string, s15, "str_myself"),
	(else_try),
		(call_script, "script_troop_get_family_relation_to_troop", ":troop_2", ":troop_1"),
		(gt, reg0, 0),
		(str_store_string, s15, "str_my_s11_s15"),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop_2", ":troop_1"),
		(ge, reg0, 20),
		(str_store_string, s15, "str_my_friend_s15"),
	(try_end),

	])
]
