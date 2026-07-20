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

dplmc_player_troops_leave_scripts = [
("dplmc_player_troops_leave",
   [
    (store_script_param_1, ":percent"),

    (try_begin),#debug
     (eq, "$cheat_mode", 1),
     (assign, reg0, ":percent"),
     (display_message, "@{!}DEBUG : removing player troops: {reg0}%"),
    (try_end),

    (assign, ":deserters", 0),
    (try_for_parties, ":party_no"),
      (assign, ":remove_troops", 0),
      (try_begin),
        (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
        (party_slot_eq, ":party_no", slot_party_type, spt_castle),
        (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
        (assign, ":remove_troops", 1),
      (else_try),
         (eq, "p_main_party", ":party_no"),
         (assign, ":remove_troops", 1),
      (try_end),

      (eq, ":remove_troops", 1),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
        (val_mul, ":stack_size", ":percent"),
        (val_div, ":stack_size", 100),
        (party_stack_get_troop_id, ":troop_id", ":party_no", ":i_stack"),
        (party_remove_members, ":party_no", ":troop_id", ":stack_size"),
        (val_add, ":deserters", ":stack_size"),
      (try_end),
    (try_end),
    (assign, reg0, ":deserters"),
   ]
  )
]
