# ======================================================================
# SHARED DEPENDENCY
# Entity: get_num_heroes_of_party (script)
# Called by menus in 2 domains: battle, siege
# ======================================================================

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
from module_items import items

get_num_heroes_of_party_scripts = [
("get_num_heroes_of_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param_2, ":exclude_wounded"),

      (assign, ":num_of_heroes", 0),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (val_add, ":num_of_heroes", 1),
        (troop_is_wounded, ":stack_troop"),
        (val_sub, ":num_of_heroes", ":exclude_wounded"),
      (try_end),
      (assign, reg0, ":num_of_heroes"),
    ])
]
