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

round_value_scripts = [
("round_value",
    [
      (store_script_param_1, ":value"),
      (try_begin),
        (lt, ":value", 100),
        (neq, ":value", 0),
        (val_add, ":value", 5),
        (val_div, ":value", 10),
        (val_mul, ":value", 10),
        (try_begin),
          (eq, ":value", 0),
          (assign, ":value", 5),
        (try_end),
      (else_try),
        (lt, ":value", 300),
        (val_add, ":value", 25),
        (val_div, ":value", 50),
        (val_mul, ":value", 50),
      (else_try),
        (val_add, ":value", 50),
        (val_div, ":value", 100),
        (val_mul, ":value", 100),
      (try_end),
      (assign, reg0, ":value"),
  ])
]
