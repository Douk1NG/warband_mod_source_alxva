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

dplmc_auto_loot_all_scripts = [
################################
# Copy this troop's upgrade options to everyone
# ("dplmc_copy_upgrade_to_all_heroes", [
# (store_script_param_1, ":troop"),
# (troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
# (troop_get_slot,":upg_horse",":troop",dplmc_slot_upgrade_horse),
# (troop_get_slot,":upg_wpn0",":troop",dplmc_slot_upgrade_wpn_0),
# (troop_get_slot,":upg_wpn1",":troop",dplmc_slot_upgrade_wpn_1),
# (troop_get_slot,":upg_wpn2",":troop",dplmc_slot_upgrade_wpn_2),
# (troop_get_slot,":upg_wpn3",":troop",dplmc_slot_upgrade_wpn_3),
# (try_for_range, ":hero", companions_begin, companions_end),
# (troop_set_slot,":hero",dplmc_slot_upgrade_armor,":upg_armor"),
# (troop_set_slot,":hero",dplmc_slot_upgrade_horse,":upg_horse"),
# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_0,":upg_wpn0"),
# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_1,":upg_wpn1"),
# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_2,":upg_wpn2"),
# (troop_set_slot,":hero",dplmc_slot_upgrade_wpn_3,":upg_wpn3"),
# (try_end),
# ]),
####################################
# Let each hero loot from the pool
("dplmc_auto_loot_all", [
    (store_script_param_1, ":pool_troop"),
    (store_script_param_2, ":sreg"),
    # for all the NPCs, in order of party listing

    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":this_hero","p_main_party",":i_stack"),
        #Allow your spouse(s) to auto loot if they are in your party
        (assign, ":is_spouse", 0),
        (try_begin),
          #Next line returns true for regular troops so need to make sure this is a hero
          (is_between, ":this_hero", heroes_begin, heroes_end),
          (troop_slot_eq, ":this_hero", slot_troop_spouse, "trp_player"),
          (assign, ":is_spouse", 1),
        (try_end),
        (this_or_next|eq, ":is_spouse", 1),
        #Letting claimants loot may be undesirable as they eventually leave, but players can always disable auto loot for them
        (this_or_next|is_between, ":this_hero", pretenders_begin, pretenders_end),
        (is_between, ":this_hero", companions_begin, companions_end),

        #SB : show strings for first iteration
        (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", ":sreg"),
        (val_add, ":sreg", 1),
    (try_end),

    #SB : get starting index once again
    (store_script_param_2, ":sreg"),
    # pick up any discards and format string
    (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":this_hero","p_main_party",":i_stack"),
        (assign, ":is_spouse", 0),
        (try_begin),
          (is_between, ":this_hero", heroes_begin, heroes_end),
          (troop_slot_eq, ":this_hero", slot_troop_spouse, "trp_player"),
          (assign, ":is_spouse", 1),
        (try_end),
        (this_or_next|eq, ":is_spouse", 1),
        (this_or_next|is_between, ":this_hero", pretenders_begin, pretenders_end),
        (is_between, ":this_hero", companions_begin, companions_end),
        (try_begin), #if first iteration picked up nothing
          (str_is_empty, ":sreg"),
          (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", ":sreg"),
        (else_try), #do not overwrite string from first iteration
          (call_script, "script_dplmc_auto_loot_troop", ":this_hero", ":pool_troop", -1),
        (try_end),
        (try_begin), #skip the first one
          (gt, ":sreg", dplmc_loot_string),
          (neg|str_is_empty, ":sreg"), # in case second hasn't picked up changes either
          (str_store_string_reg, s1, ":sreg"),
          (str_store_string_reg, s0, dplmc_loot_string),
          (str_store_string, dplmc_loot_string, "str_dplmc_s0_newline_s1"),
        (try_end),
        (val_add, ":sreg", 1), #go to next string register
    (try_end),

    #Done. Now sort the remainder
    (troop_sort_inventory, ":pool_troop"),

])
]
