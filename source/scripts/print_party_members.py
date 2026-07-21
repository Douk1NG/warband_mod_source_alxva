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

print_party_members_scripts = [
("print_party_members",
    [
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (assign, reg10, ":num_stacks"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 0),
          (str_store_troop_name, s51, ":stack_troop"),
        (try_end),
        (str_store_troop_name, s52, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 1),
          (str_store_string, s51, "str_s52_and_s51"),
        (else_try),
          (gt, ":i_stack", 1),
          (str_store_string, s51, "str_s52_comma_s51"),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":num_stacks", 0),
        (str_store_string, s51, "str_noone"),
      (try_end),
  ])
]
