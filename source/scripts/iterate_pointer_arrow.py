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

iterate_pointer_arrow_scripts = [
("iterate_pointer_arrow",
    [
      (store_mission_timer_a_msec, ":cur_time"),
      (try_begin),
        (assign, ":up_down", ":cur_time"),
        (assign, ":turn_around", ":cur_time"),
        (val_mod, ":up_down", 1080),
        (val_div, ":up_down", 3),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (position_move_z, pos0, "$g_pointer_arrow_height_adder", 1),
        (set_fixed_point_multiplier, 100),
        (val_mul, ":up_down", 100),
        (store_sin, ":up_down_sin", ":up_down"),
        (position_move_z, pos0, ":up_down_sin", 1),
        (position_move_z, pos0, 100, 1),
        (val_mod, ":turn_around", 2880),
        (val_div, ":turn_around", 8),
        (init_position, pos1),
        (position_rotate_z, pos1, ":turn_around"),
        (position_copy_rotation, pos0, pos1),
        (prop_instance_set_position, ":prop_instance", pos0),
      (try_end),
     ])
]
