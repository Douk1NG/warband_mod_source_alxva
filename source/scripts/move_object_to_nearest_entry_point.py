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

move_object_to_nearest_entry_point_scripts = [
("move_object_to_nearest_entry_point",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (prop_instance_get_position, pos0, ":instance_id"),

       (assign, ":smallest_dist", -1),
       (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
         (entry_point_get_position, pos1, ":entry_point_no"),
         (get_sq_distance_between_positions, ":dist", pos0, pos1),
         (this_or_next|eq, ":smallest_dist", -1),
         (lt, ":dist", ":smallest_dist"),
         (assign, ":smallest_dist", ":dist"),
         (assign, ":nearest_entry_point", ":entry_point_no"),
       (try_end),

       (try_begin),
         (ge, ":smallest_dist", 0),
         (lt, ":smallest_dist", 22500), #max 15m distance
         (entry_point_get_position, pos1, ":nearest_entry_point"),
         (position_rotate_x, pos1, -90),
         (prop_instance_animate_to_position, ":instance_id", pos1, 1),
       (try_end),
     (try_end),
   ])
]
