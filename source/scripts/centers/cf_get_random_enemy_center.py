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

cf_get_random_enemy_center_scripts = [
##  # script_cf_get_new_center_leader_chance_for_troop
##  # Input: arg1 = troop_no
##  # Output: reg0 = chance of the troop to rule a new center
##  ("cf_get_new_center_leader_chance_for_troop",
##    [
##      (store_script_param_1, ":troop_no"),
##      (troop_get_slot, ":troop_rank", ":troop_no", slot_troop_kingdom_rank),
##      (try_begin),
##        (eq, ":troop_rank", 4),
##        (assign, ":troop_chance", 1000),
##      (else_try),
##        (eq, ":troop_rank", 3),
##        (assign, ":troop_chance", 800),
##      (else_try),
##        (eq, ":troop_rank", 2),
##        (assign, ":troop_chance", 400),
##      (else_try),
##        (eq, ":troop_rank", 1),
##        (assign, ":troop_chance", 100),
##      (else_try),
##        (assign, ":troop_chance", 10),
##      (try_end),
##
##      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
##      (assign, ":number_of_hero_centers", reg0),
##      (try_begin),
##        (gt, ":number_of_hero_centers", 0),
##        (val_mul, ":number_of_hero_centers", 2),
##        (val_mul, ":number_of_hero_centers", ":number_of_hero_centers"),
##        (val_div, ":troop_chance", ":number_of_hero_centers"),
##      (try_end),
##      (assign, reg0, ":troop_chance"),
##      (eq, reg0, 0),
##      (assign, reg0, 1),
##  ]),
##  # script_select_kingdom_hero_for_new_center
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no as the new leader
##  ("select_kingdom_hero_for_new_center",
##    [
##      (store_script_param_1, ":kingdom"),
##
##      (assign, ":min_num_centers", -1),
##      (assign, ":min_num_centers_troop", -1),
##
##      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
##        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##        (store_troop_faction, ":troop_faction", ":troop_no"),
##        (eq, ":troop_faction", ":kingdom"),
##        (call_script, "script_get_number_of_hero_centers", ":troop_no"),
##        (assign, ":num_centers", reg0),
##        (try_begin),
##          (lt, ":num_centers", ":min_num_centers"),
##          (assign, ":min_num_centers", ":num_centers"),
##          (assign, ":min_num_centers_troop", ":troop_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":min_num_centers_troop"),
##  ]),
# script_cf_get_random_enemy_center
# Input: arg1 = party_no
# Output: reg0 = center_no
("cf_get_random_enemy_center",
    [
      (store_script_param_1, ":party_no"),

      (assign, ":result", -1),
      (assign, ":total_enemy_centers", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_add, ":total_enemy_centers", 1),
      (try_end),

      (gt, ":total_enemy_centers", 0),
      (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
      (assign, ":total_enemy_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
