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

get_custom_banner_color_from_index_scripts = [
# script_get_custom_banner_color_from_index
# Input: arg1 = color_index
# Output: reg0 = color
("get_custom_banner_color_from_index",
    [
      (store_script_param, ":color_index", 1),

      (assign, ":cur_color", 0xFF000000),
      (assign, ":red", 0x00),
      (assign, ":green", 0x00),
      (assign, ":blue", 0x00),
      (store_mod, ":mod_i_color", ":color_index", 7),
      (try_begin),
        (eq, ":mod_i_color", 0),
        (assign, ":blue", 0xFF),
      (else_try),
        (eq, ":mod_i_color", 1),
        (assign, ":red", 0xEE),
      (else_try),
        (eq, ":mod_i_color", 2),
        (assign, ":red", 0xFB),
        (assign, ":green", 0xAC),
      (else_try),
        (eq, ":mod_i_color", 3),
        (assign, ":red", 0x5F),
        (assign, ":blue", 0xFF),
      (else_try),
        (eq, ":mod_i_color", 4),
        (assign, ":red", 0x05),
        (assign, ":green", 0x44),
      (else_try),
        (eq, ":mod_i_color", 5),
        (assign, ":red", 0xEE),
        (assign, ":green", 0xEE),
        (assign, ":blue", 0xEE),
      (else_try),
        (assign, ":red", 0x22),
        (assign, ":green", 0x22),
        (assign, ":blue", 0x22),
      (try_end),
      (store_div, ":cur_tone", ":color_index", 7),
      (store_sub, ":cur_tone", 8, ":cur_tone"),
      (val_mul, ":red", ":cur_tone"),
      (val_div, ":red", 8),
      (val_mul, ":green", ":cur_tone"),
      (val_div, ":green", 8),
      (val_mul, ":blue", ":cur_tone"),
      (val_div, ":blue", 8),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
     ])
]
