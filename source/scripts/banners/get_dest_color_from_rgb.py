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

get_dest_color_from_rgb_scripts = [
# script_cf_check_color_visibility
("get_dest_color_from_rgb",
    [
      (store_script_param, ":red", 1),
      (store_script_param, ":green", 2),
      (store_script_param, ":blue", 3),

      (assign, ":cur_color", 0xFF000000),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
    ])
]
