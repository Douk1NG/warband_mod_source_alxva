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

convert_3d_pos_to_map_bar_pos_scripts = [
("convert_3d_pos_to_map_bar_pos",
   [
    (store_script_param_1, ":y_offset"),

    (set_fixed_point_multiplier, 1000),
    (position_move_z, pos1, 170),
    (position_get_screen_projection, pos3, pos1),
    (position_get_x, ":pos_x", pos3),
    (try_begin),
      (is_between, ":pos_x", -200, 1201),
      (val_clamp, ":pos_x", 0, 1001),
    (else_try), # hide on the left
      (lt, ":pos_x", -200),
      (assign, ":pos_x", -250),
    (else_try), # hide on the right
      (gt, ":pos_x", 1200),
      (assign, ":pos_x", 1250),
    (try_end),
    (val_sub, ":pos_x", 500),
    (val_mul, ":pos_x", 20),
    (val_div, ":pos_x", 100),
    (val_add, ":pos_x", 500),
    (store_add, ":pos_y", 721, ":y_offset"),
    (position_set_x, pos0, ":pos_x"),
    (position_set_y, pos0, ":pos_y"),
  ])
]
