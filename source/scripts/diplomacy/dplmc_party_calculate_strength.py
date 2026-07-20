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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_party_calculate_strength_scripts = [
("dplmc_party_calculate_strength",
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

      (assign, ":sum", 0),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),

        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (try_end),
        (val_add, ":sum", ":stack_size"),
      (try_end),
      (assign, reg0, ":sum"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (display_message, "@{!}DEBUG : sum: {reg0}"),
      (try_end),
  ])
]
