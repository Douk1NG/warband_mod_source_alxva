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

get_army_size_from_slider_value_scripts = [
("get_army_size_from_slider_value",
    [
     (store_script_param, ":slider_value", 1),
     (assign, ":army_size", ":slider_value"),
     (try_begin),
       (gt, ":slider_value", 25),
       (store_sub, ":adder_value", ":slider_value", 25),
       (val_add, ":army_size", ":adder_value"),
       (try_begin),
         (gt, ":slider_value", 50),
         (store_sub, ":adder_value", ":slider_value", 50),
         (val_mul, ":adder_value", 3),
         (val_add, ":army_size", ":adder_value"),
       (try_end),
     (try_end),
     (assign, reg0, ":army_size"),
  ])
]
