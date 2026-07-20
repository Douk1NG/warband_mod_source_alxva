# ======================================================================
# SHARED DEPENDENCY
# Entity: party_count_members_with_full_health (script)
# Called by menus in 3 domains: battle, siege, village
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

party_count_members_with_full_health_scripts = [
("party_count_members_with_full_health",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (neq, ":stack_troop", "trp_player"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (ge, ":troop_hp", 80),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size, ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
          (val_max, ":num_fit", 0),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ])
]
