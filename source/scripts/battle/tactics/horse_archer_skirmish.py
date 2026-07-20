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

horse_archer_skirmish_scripts = [
("horse_archer_skirmish",
		[
			(store_script_param, ":agent", 1), #agent
			(store_script_param, ":enemy_agent", 2), #enemy agent
			(store_script_param, ":enemy_dist", 3), #distance from enemy
			(store_script_param, ":min_dist", 4), #min distance (inner radius)
			(store_script_param, ":max_dist", 5), #max distance (outer radius)
			(store_script_param, ":script_param_6", 6), #new position adder
			(try_begin),
				(assign, ":min_dist_from_enemy", ":min_dist"),
				(gt, ":enemy_agent", 0),
				(agent_get_position, pos0, ":agent"),
				(agent_get_position, pos1, ":enemy_agent"),
				# (agent_get_slot, ":skirmish_direction", ":agent", 106), #1/2 agents go clockwise
				(agent_get_slot, ":dist_to_add", ":agent", slot_agent_make_dist_with_enemy),
				# (try_begin),
					# (eq, ":skirmish_direction", 0),
					# (store_random_in_range, ":skirmish_direction", 1, 3),
					# (agent_set_slot, ":agent", 106, ":skirmish_direction"),
				# (try_end),
				(try_begin),
					(le, ":enemy_dist", ":max_dist"),
					(val_add, ":dist_to_add", ":script_param_6"),
					(try_begin),
						(ge, ":dist_to_add", 360),
						(assign, ":dist_to_add", 0),
					(try_end),
					(agent_set_slot, ":agent", slot_agent_make_dist_with_enemy, ":dist_to_add"),
					# (try_begin),
						# (eq, ":skirmish_direction", 1),
						# (val_mul, ":dist_to_add", -1),
						# (val_sub, ":min_dist_from_enemy", 1500), #clockwise agents stay closer to enemy
					# (try_end),
					(position_get_rotation_around_z, reg1, 1),
					(store_sub, reg0, 360, reg1),
					(val_add, ":dist_to_add", reg0),
					(position_rotate_z, pos1, ":dist_to_add"),
					(position_move_x, pos1, ":min_dist_from_enemy", 0),
					(agent_set_scripted_destination, ":agent", pos1, 1), #no rethink?
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 1),
				(else_try),
					(agent_clear_scripted_mode, ":agent"),
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 0),
				(try_end),
			(try_end)
		])
]
