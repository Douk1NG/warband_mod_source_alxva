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

faction_get_adjective_to_s10_scripts = [
("faction_get_adjective_to_s10",
	[
	(store_script_param, ":faction_no", 1),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),


	(try_begin),
		(eq, ":faction_no", "fac_player_supporters_faction"),
		(str_store_string, s10, "str_rebel"),
	(else_try),
		(this_or_next|eq, ":faction_no", "fac_outlaws"),
		(this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
		(this_or_next|eq, ":faction_no", "fac_forest_bandits"),
			(eq, ":faction_no", "fac_deserters"),
		(str_store_string, s10, "str_bandit"),
	(else_try),
		(faction_get_slot, ":adjective_string", ":faction_no", slot_faction_adjective),
		(str_store_string, s10, ":adjective_string"),
	(try_end),
	])
]
