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

point_y_toward_position_scripts = [
("point_y_toward_position", [
      (store_script_param, ":from_position", 1),
      (store_script_param, ":to_position", 2),
      (assign, ":save_fpm", 1),
      (convert_to_fixed_point, ":save_fpm"),
      (set_fixed_point_multiplier, 100),  #to match cm returned by get_distance_between_positions

      #remove current rotation
      (position_get_x, ":from_x", ":from_position"),
      (position_get_y, ":from_y", ":from_position"),
      (position_get_z, ":from_z", ":from_position"),
      (init_position, ":from_position"),
      (position_set_x, ":from_position", ":from_x"),
      (position_set_y, ":from_position", ":from_y"),
      (position_set_z, ":from_position", ":from_z"),

      #horizontal rotation
      (position_get_x, ":change_in_x", ":to_position"),
      (val_sub, ":change_in_x", ":from_x"),
      (position_get_y, ":change_in_y", ":to_position"),
      (val_sub, ":change_in_y", ":from_y"),

      (try_begin),
        (this_or_next | neq, ":change_in_y", 0),
        (neq, ":change_in_x", 0),
        (store_atan2, ":theta", ":change_in_y", ":change_in_x"),
        (assign, ":ninety", 90),
        (convert_to_fixed_point, ":ninety"),
        (val_sub, ":theta", ":ninety"),	#point Y axis at to position
        (position_rotate_z_floating, ":from_position", ":theta"),
      (try_end),

      #vertical rotation
      (get_distance_between_positions, ":distance_between", ":from_position", ":to_position"),
      (try_begin),
        (gt, ":distance_between", 0),
        (position_get_z, ":dist_z_to_sine", ":to_position"),
        (val_sub, ":dist_z_to_sine", ":from_z"),
        (val_div, ":dist_z_to_sine", ":distance_between"),
        (store_asin, ":theta", ":dist_z_to_sine"),
        (position_rotate_x_floating, ":from_position", ":theta"),
      (try_end),

      (assign, reg0, ":distance_between"),
      (set_fixed_point_multiplier, ":save_fpm"),])
]
