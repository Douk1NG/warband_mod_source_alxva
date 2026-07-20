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

find_high_ground_around_pos1_scripts = [
("find_high_ground_around_pos1",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      (team_get_leader, ":ai_leader", ":team_no"),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      #do not find positions close to borders (20 m)
      (val_add, ":scene_min_x", 2000),
      (val_sub, ":scene_max_x", 2000),
      (val_add, ":scene_min_y", 2000),
      (val_sub, ":scene_max_y", 2000),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),

      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),

      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
  ])
]
