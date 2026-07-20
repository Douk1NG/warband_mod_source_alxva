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

town_init_doors_scripts = [
# script_town_init_doors
# Input: door_state (-1 = closed, 1 = open, 0 = use $town_nighttime)
# Output: none (required for siege mission templates)
("town_init_doors",
   [(store_script_param, ":door_state", 1),
    (try_begin),
      (assign, ":continue", 0),
      (try_begin),
        (eq, ":door_state", 1),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":door_state", 0),
        (eq, "$town_nighttime", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),# open doors
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
    (try_end),
  ])
]
