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

calculate_improvement_limit_scripts = [
("calculate_improvement_limit", [
        (store_script_param_1, ":troop_no"),
        (assign, ":limit", dplmc_improvement_limit),
        (troop_get_slot, ":personality", ":troop_no", slot_lord_reputation_type),
        (try_begin), #bad personality, unlikely to ever build property
            (is_between, ":personality", lrep_selfrighteous, lrep_goodnatured),
            (val_mul, ":limit", ":personality"),
            (val_div, ":limit", 2),
        (else_try), #include companion personality types
            (is_between, ":personality", lrep_goodnatured, lrep_custodian),
            (try_begin), #exception
              (neq, ":personality", lrep_roguish),
              (store_mul, ":level", ":personality", 250),
              (val_sub, ":limit", ":level"),
            (try_end),
        (try_end),
        (assign, reg0, ":limit"),
    ])
]
