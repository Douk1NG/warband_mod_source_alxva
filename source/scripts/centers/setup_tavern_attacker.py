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

setup_tavern_attacker_scripts = [
("setup_tavern_attacker",
	[
	  (store_script_param, ":cur_entry", 1),

	  (try_begin),
	    (neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_belligerent_drunk"),
	  (try_end),

	  (try_begin),
	    (troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_hired_assassin"),
	  (try_end),
	])
]
