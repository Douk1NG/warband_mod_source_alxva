# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from module_constants import *

bandit_overhaul_adjust_party_size_scripts = [
  ("bandit_overhaul_adjust_party_size", [
    (store_script_param, ":party_no", 1),
    (store_script_param, ":base_max_size", 2),
    (party_is_active, ":party_no"),
    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
    (gt, ":num_stacks", 0),

    # The setting is in tenths of a percent per player level. For example,
    # setting 5 gives level 40 a 20% increase. Keep per-mille precision until
    # troop counts are rounded so half-percent steps are not lost.
    (store_character_level, ":player_level", "trp_player"),
    (store_mul, ":growth_per_mille", ":player_level", "$g_bo_party_growth_per_level_tenths"),
    (store_add, ":scale_per_mille", 1000, ":growth_per_mille"),
    (store_mul, ":scaled_cap", ":base_max_size", ":scale_per_mille"),
    (val_add, ":scaled_cap", 500),
    (val_div, ":scaled_cap", 1000),
    (val_max, ":scaled_cap", 1),

    (assign, ":scaled_total", 0),
    (try_for_range, ":stack_no", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
      (party_stack_get_size, ":old_size", ":party_no", ":stack_no"),
      (store_mul, ":new_size", ":old_size", ":scale_per_mille"),
      (val_add, ":new_size", 500),
      (val_div, ":new_size", 1000),
      (val_max, ":new_size", 1),
      (try_begin),
        (gt, ":new_size", ":old_size"),
        (store_sub, ":difference", ":new_size", ":old_size"),
        (party_add_members, ":party_no", ":troop_no", ":difference"),
      (else_try),
        (lt, ":new_size", ":old_size"),
        (store_sub, ":difference", ":old_size", ":new_size"),
        (party_remove_members, ":party_no", ":troop_no", ":difference"),
      (try_end),
      (val_add, ":scaled_total", ":new_size"),
    (try_end),

    # The configured scaled maximum is a hard cap, including for multi-stack
    # parties such as manhunters. Remove excess from non-leader stacks first.
    (try_begin),
      (gt, ":scaled_total", ":scaled_cap"),
      (store_sub, ":excess", ":scaled_total", ":scaled_cap"),
      (try_for_range_backwards, ":stack_no", 1, ":num_stacks"),
        (gt, ":excess", 0),
        (party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
        (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
        (val_min, ":stack_size", ":excess"),
        (gt, ":stack_size", 0),
        (party_remove_members, ":party_no", ":troop_no", ":stack_size"),
        (val_sub, ":excess", ":stack_size"),
      (try_end),
      (try_begin),
        (gt, ":excess", 0),
        (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
        (party_stack_get_size, ":stack_size", ":party_no", 0),
        (val_sub, ":stack_size", 1),
        (val_min, ":stack_size", ":excess"),
        (gt, ":stack_size", 0),
        (party_remove_members, ":party_no", ":troop_no", ":stack_size"),
      (try_end),
    (try_end),
  ]),
]
