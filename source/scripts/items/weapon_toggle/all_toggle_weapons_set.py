# ======================================================================
# SHARED DEPENDENCY
# Entity: all_toggle_weapons_set (script)
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

all_toggle_weapons_set_scripts = [
("all_toggle_weapons_set",
    [
      (store_script_param, ":strict_mode", 1),
    
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":cur_hero", "p_main_party", ":i_stack"),
        (troop_is_hero, ":cur_hero"),
        (troop_get_slot, ":troop_weapons_set_no", ":cur_hero", slot_troop_weapons_set_no),
        (call_script, "script_get_num_equiped_weapons_of_troop", ":cur_hero"),
        (assign, ":num_weapons", reg0),
        (call_script, "script_get_num_backup_weapons_of_troop", ":cur_hero"),
        (assign, ":num_backup_weapons", reg0),
        (try_begin),
          (neq, ":troop_weapons_set_no", "$g_weapons_set_no"),
          (try_begin),
            (this_or_next|gt, ":num_backup_weapons", 0),
            (this_or_next|eq, ":num_weapons", 0),
            (eq, ":strict_mode", 1),
            (call_script, "script_hero_toggle_weapons_set", ":cur_hero"),
          (try_end),
        (else_try),
            (gt, ":num_backup_weapons", 0),
            (eq, ":num_weapons", 0),
            (eq, ":strict_mode", 0),
            (call_script, "script_hero_toggle_weapons_set", ":cur_hero"),
        (try_end),
      (try_end),
    ])
]
