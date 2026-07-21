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

get_item_value_with_imod_scripts = [
("get_item_value_with_imod",
    [
      (store_script_param, ":item", 1),
      (store_script_param, ":imod", 2),
      (try_begin),
        (gt, ":item", -1),
        (store_item_value, ":score", ":item"),
        (item_get_slot, ":imod_mult", ":imod", slot_item_modifier_multiplier),
        (val_mul, ":score", ":imod_mult"),
        (val_div, ":score", 100),
      (else_try),
        (assign, ":score", 0),
      (try_end),
      (assign, reg0, ":score"),
    ])
]
