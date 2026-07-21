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

cf_get_random_lord_in_a_center_with_faction_scripts = [
# script_cf_faction_get_random_enemy_faction
##  # Input: arg1 = troop_no
##  # Output: reg0 = enemy_troop_no (Can fail)
##  ("cf_troop_get_random_enemy_troop_as_a_town_lord",
##    [
##      (store_script_param_1, ":troop_no"),
##
##      (assign, ":result", -1),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##      (try_end),
##      (store_random_in_range,":random_enemy",0,":count_enemies"),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (eq, ":result", -1),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##        (gt, ":count_enemies", ":random_enemy"),
##        (assign, ":result", ":cur_enemy"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
##  # script_cf_get_random_enemy_with_valid_slot
##  # Input: arg1 = faction_no, arg2 = slot_no
##  # Output: reg0 = faction_no (Can fail)
##  ("cf_get_random_enemy_with_valid_slot",
##    [
##      (store_script_param_1, ":faction_no"),
##      (store_script_param_2, ":slot_no"),
##
##      (assign, ":result", -1),
##      (assign, ":count_factions", 0),
##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
##        (le, ":cur_relation", -10),
##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
##        (gt, ":cur_value", 0),#Checking validity
##        (val_add, ":count_factions", 1),
##      (try_end),
##      (store_random_in_range,":random_faction",0,":count_factions"),
##      (assign, ":count_factions", 0),
##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
##        (eq, ":result", -1),
##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
##        (le, ":cur_relation", -10),
##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
##        (gt, ":cur_value", 0),#Checking validity
##        (val_add, ":count_factions", 1),
##        (gt, ":count_factions", ":random_faction"),
##        (assign, ":result", ":cur_faction"),
##      (try_end),
##
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
##  # script_cf_get_random_kingdom_hero
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no (Can fail)
##  ("cf_get_random_kingdom_hero",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##      (try_end),
##      (store_random_in_range, ":random_hero", 0, ":count_heroes"),
##      (assign, ":result", -1),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (eq, ":result", -1),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##        (lt, ":random_hero", ":count_heroes"),
##        (assign, ":result", ":cur_lord"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
# script_cf_get_random_kingdom_hero_as_lover - removed
##  # script_cf_get_random_siege_location_with_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
##  # script_cf_get_random_siege_location_with_attacker_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_attacker_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
##  # script_cf_get_number_of_random_troops_from_party
##  # Input: arg1 = party_no, arg2 = number of troops to remove
##  # Output: reg0 = troop_no, Can fail if there are no slots having the required number of units!
##  ("cf_get_number_of_random_troops_from_party",
##    [
##      (store_script_param_1, ":party_no"),
##      (store_script_param_2, ":no_to_remove"),
##
##      (assign, ":result", -1),
##      (assign, ":count_stacks", 0),
##
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##      (try_end),
##      (store_random_in_range,":random_stack",0,":count_stacks"),
##      (assign, ":count_stacks", 0),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (eq, ":result", -1),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##        (gt, ":count_stacks", ":random_stack"),
##        (assign, ":result", ":stack_troop"),
##      (try_end),
##
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),
# script_cf_get_random_lord_in_a_center_with_faction
# Input: arg1 = faction_no
# Output: reg0 = troop_no, Can Fail!
("cf_get_random_lord_in_a_center_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ])
]
