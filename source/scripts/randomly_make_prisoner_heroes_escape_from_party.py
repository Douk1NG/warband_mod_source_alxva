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

randomly_make_prisoner_heroes_escape_from_party_scripts = [
# script_cf_party_remove_random_regular_troop
# Input: arg1 = party_no, arg2 = escape_chance_mul_1000
# Output: none
("randomly_make_prisoner_heroes_escape_from_party",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":escape_chance", 2),
     (assign, ":quest_troop_1", -1),
     (assign, ":quest_troop_2", -1),
     (try_begin),
       (check_quest_active, "qst_rescue_lord_by_replace"),
       (quest_get_slot, ":quest_troop_1", "qst_rescue_lord_by_replace", slot_quest_target_troop),
     (try_end),
     (try_begin),
       (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
       (quest_get_slot, ":quest_troop_2", "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop),
     (try_end),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neq, ":stack_troop", ":quest_troop_1"),
       (neq, ":stack_troop", ":quest_troop_2"),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_random_in_range, ":random_no", 0, 1000),
       (lt, ":random_no", ":escape_chance"),
       (party_remove_prisoners, ":party_no", ":stack_troop", 1),
       (call_script, "script_remove_troop_from_prison", ":stack_troop"),
       (str_store_troop_name_link, s1, ":stack_troop"),
       (try_begin),
         (eq, ":party_no", "p_main_party"),
         (str_store_string, s2, "@your party"),
       (else_try),
         (str_store_party_name, s2, ":party_no"),
       (try_end),
       (assign, reg0, 0),
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, reg0, 1),
       (try_end),
       (store_troop_faction, ":troop_faction", ":stack_troop"),
       (str_store_faction_name_link, s3, ":troop_faction"),
       (faction_get_color, ":color", ":troop_faction"),
       #SB : factionalize color, set to log
       (display_log_message, "@{reg0?One of your prisoners, :}{s1} of {s3} has escaped from captivity!", ":color"),
     (try_end),
     ])
]
