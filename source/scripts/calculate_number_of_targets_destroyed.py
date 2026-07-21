# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

calculate_number_of_targets_destroyed_scripts = [
("calculate_number_of_targets_destroyed",
   [
     (assign, "$g_number_of_targets_destroyed", 0),
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),
     ])
]
