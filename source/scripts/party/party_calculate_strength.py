# ======================================================================
# SHARED DEPENDENCY
# Entity: party_calculate_strength (script)
# Called by menus in 2 domains: battle, siege
# ======================================================================

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

party_calculate_strength_scripts = [
("party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id

      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 4), #new was 12 (patch 1.125)
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_mul, ":stack_strength", 2), #new (patch 1.125)
        (val_div, ":stack_strength", 100),
        (val_max, ":stack_strength", 1), #new (patch 1.125)
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero & wounded
          (assign, ":stack_strength", 0),
        (try_end),
        (val_add, reg0, ":stack_strength"),
      (try_end),
      (party_set_slot, ":party", slot_party_cached_strength, reg0),
  ])
]
