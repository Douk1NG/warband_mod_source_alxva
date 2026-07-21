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

party_calculate_regular_strength_scripts = [
("party_calculate_regular_strength",
    [
      (store_script_param_1, ":party"), #Party_id

      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_mul, ":stack_strength", ":stack_size"),
        (val_add,reg0, ":stack_strength"),
      (try_end),
  ])
]
