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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

cf_check_color_visibility_scripts = [
("cf_check_color_visibility",
    [
      (store_script_param, ":color_1", 1),
      (store_script_param, ":color_2", 2),
      (store_mod, ":blue_1", ":color_1", 256),
      (store_div, ":green_1", ":color_1", 256),
      (val_mod, ":green_1", 256),
      (store_div, ":red_1", ":color_1", 256 * 256),
      (val_mod, ":red_1", 256),
      (store_mod, ":blue_2", ":color_2", 256),
      (store_div, ":green_2", ":color_2", 256),
      (val_mod, ":green_2", 256),
      (store_div, ":red_2", ":color_2", 256 * 256),
      (val_mod, ":red_2", 256),
      (store_sub, ":red_dif", ":red_1", ":red_2"),
      (val_abs, ":red_dif"),
      (store_sub, ":green_dif", ":green_1", ":green_2"),
      (val_abs, ":green_dif"),
      (store_sub, ":blue_dif", ":blue_1", ":blue_2"),
      (val_abs, ":blue_dif"),
      (assign, ":max_dif", 0),
      (val_max, ":max_dif", ":red_dif"),
      (val_max, ":max_dif", ":green_dif"),
      (val_max, ":max_dif", ":blue_dif"),
      (ge, ":max_dif", 64),
     ])
]
