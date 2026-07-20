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

dplmc_get_prisoners_value_between_factions_scripts = [
#Not currently used (ie, it always fails)
("dplmc_get_prisoners_value_between_factions",
   [
       (store_script_param, ":faction_no_1", 1),
       (store_script_param, ":faction_no_2", 2),

       (assign, ":faction_no_1_value", 0),
       (assign, ":faction_no_2_value", 0),

       (try_for_parties, ":party_no"),
         (store_faction_of_party, ":party_faction", ":party_no"),
         (try_begin),
           (eq, ":party_faction", ":faction_no_1"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
           (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
             (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),

             (eq, ":cur_faction", ":faction_no_2"),
             (try_begin),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_calculate_ransom_amount_for_troop", ":cur_troop_id"),
               (val_add, ":faction_no_1_value", reg0),

               (try_begin),#debug
                 (eq, "$cheat_mode", 1),
                 (assign, reg0, ":faction_no_1_value"),
                 (display_message, "@{!}DEBUG : faction_no_1_value: {reg0}"),
               (try_end),

             (try_end),
           (try_end),
         (else_try),
           (eq, ":party_faction", ":faction_no_2"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
           (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
             (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),

             (eq, ":cur_faction", ":faction_no_1"),
             (try_begin),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_calculate_ransom_amount_for_troop", ":cur_troop_id"),
               (val_add, ":faction_no_2_value", reg0),

               (try_begin), #debug
                 (eq, "$cheat_mode", 1),
                 (assign, reg0, ":faction_no_2_value"),
                 (display_message, "@{!}DEBUG : faction_no_2_value: {reg0}"),
               (try_end),

             (try_end),
           (try_end),
         (try_end),
       (try_end),
       (store_sub, reg0, ":faction_no_1_value", ":faction_no_2_value"),
    ])
]
