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

cf_agent_can_rout_scripts = [
("cf_agent_can_rout", [
	(store_script_param, ":agent", 1),

	(try_begin),
		(agent_is_ally, ":agent"),
		#count ready allies
		(assign, ":ready", "$j_num_us_ready"),
		(val_add, ":ready", "$j_num_allies_ready"),

		#count deady allies
		(store_add, ":deady", "$j_num_us_wounded", "$j_num_us_routed"),
		(val_add, ":deady", "$j_num_us_dead"),
		(val_add, ":deady", "$j_num_allies_wounded"),
		(val_add, ":deady", "$j_num_allies_routed"),
		(val_add, ":deady", "$j_num_allies_dead"),
		(val_mul, ":deady", 10),
	(else_try),
		#count ready enemies
		(assign, ":ready", "$j_num_enemies_ready"),

		#count deady enemies
		(store_add, ":deady", "$j_num_enemies_wounded", "$j_num_enemies_routed"),
		(val_add, ":deady", "$j_num_enemies_dead"),
		(val_mul, ":deady", 10),
	(try_end),
	# (display_message, "@agents cannot rout"),
	(gt, ":deady", ":ready"),
	# (display_message, "@agents can rout"),
])
]
