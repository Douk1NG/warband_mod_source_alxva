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

calculate_equipment_limit_scripts = [
("calculate_equipment_limit", [
        (store_script_param_1, ":troop_no"),
        (store_script_param_2, ":center_no"),
        (assign, ":limit", dplmc_equipment_limit),
        (troop_get_slot, ":personality", ":troop_no", slot_lord_reputation_type),

        (try_begin), #focus on arms
          (is_between, ":personality", lrep_martial, lrep_selfrighteous),
          (val_div, ":limit", 2),
        (else_try), #invest in gear not fief
          (eq, ":personality", lrep_roguish),
          (val_sub, ":limit", 1000),
        (try_end),

        #aristocracy modifier as enthusiasm for shopping
        (store_faction_of_party, ":faction_no", ":center_no"),
        (faction_get_slot, ":aristocracy", ":faction_no", dplmc_slot_faction_aristocracy),
        (val_mul, ":aristocracy", -100), #high plutocracy more shopping, decreasing threshold
        (val_add, ":limit", ":aristocracy"),

        (assign, reg0, ":limit"),
    ])
]
