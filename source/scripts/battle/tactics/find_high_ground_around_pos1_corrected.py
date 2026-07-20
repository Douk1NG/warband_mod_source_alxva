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

find_high_ground_around_pos1_corrected_scripts = [
("find_high_ground_around_pos1_corrected", [
      (store_script_param, ":destination_pos", 1),
      (store_script_param, ":search_radius", 2),
      (assign, ":fixed_point_multiplier", 1),
      (convert_to_fixed_point, ":fixed_point_multiplier"),
      (set_fixed_point_multiplier, 1),

      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),

      (get_scene_boundaries, ":destination_pos", pos0),
      (position_get_x, ":scene_min_x", ":destination_pos"),
      (position_get_x, ":scene_max_x", pos0),
      (position_get_y, ":scene_min_y", ":destination_pos"),
      (position_get_y, ":scene_max_y", pos0),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (assign, ":highest_pos_z", -100),
      (copy_position, ":destination_pos", pos1),
      (init_position, pos0),

      (try_for_range, ":i_x", ":min_x", ":max_x"),
        (try_for_range, ":i_y", ":min_y", ":max_y"),
          (position_set_x, pos0, ":i_x"),
          (position_set_y, pos0, ":i_y"),
          (position_set_z_to_ground_level, pos0),
          (position_get_z, ":cur_pos_z", pos0),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, ":destination_pos", pos0),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),

      (set_fixed_point_multiplier, ":fixed_point_multiplier"),])
]
