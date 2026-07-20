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

find_nearest_enemy_position_scripts = [
("find_nearest_enemy_position",
		[
			(store_script_param, ":agent", 1),
			(store_script_param, ":agent_team", 2),
			(store_script_param, ":threshold", 3), #if under threshold then stop searching
			(assign, ":nearest_dist", 100000),
			(assign, ":nearest_agent", -1),
			(agent_get_position, pos1, ":agent"),
			(try_for_agents, ":agent2"),
				(gt, ":nearest_dist", ":threshold"),
				(agent_is_alive, ":agent2"),
				(agent_is_active, ":agent2"),
				(agent_is_human, ":agent2"),
				(agent_get_team, ":agent2_team", ":agent2"),
				(teams_are_enemies, ":agent2_team", ":agent_team"),
				(agent_get_position, pos2, ":agent2"),
				(get_distance_between_positions, ":enemy_dist", pos2, pos1),
				(lt, ":enemy_dist", ":nearest_dist"),
				(assign, ":nearest_agent", ":agent2"),
				(assign, ":nearest_dist", ":enemy_dist"),
			(try_end),
			(assign, reg1, ":nearest_dist"),
			(assign, reg4, ":nearest_agent")
		])
]
