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

convert_slot_no_to_color_scripts = [
("convert_slot_no_to_color",
    [
      (store_script_param, ":cur_color", 1),

      (store_mod, ":blue", ":cur_color", 6),
      (val_div, ":cur_color", 6),
      (store_mod, ":green", ":cur_color", 6),
      (val_div, ":cur_color", 6),
      (store_mod, ":red", ":cur_color", 6),
      (val_mul, ":blue", 0x33),
      (val_mul, ":green", 0x33),
      (val_mul, ":red", 0x33),
      (assign, ":dest_color", 0xFF000000),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":dest_color", ":blue"),
      (val_add, ":dest_color", ":green"),
      (val_add, ":dest_color", ":red"),
      (assign, reg0, ":dest_color"),
    ])
]
