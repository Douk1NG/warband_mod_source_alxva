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

find_travel_location_scripts = [
# script_get_closest_walled_center_of_faction
##  # Input: arg1 = party_no
##  # Output: reg0 = center_no
##  ("get_random_enemy_town",
##    [
##      (store_script_param_1, ":party_no"),
##
##      (assign, ":result", -1),
##      (assign, ":total_enemy_centers", 0),
##      (store_faction_of_party, ":party_faction", ":party_no"),
##
##      (try_for_range, ":center_no", towns_begin, towns_end),
##        (store_faction_of_party, ":center_faction", ":center_no"),
##        (neq, ":center_faction", ":party_faction"),
##        (val_add, ":total_enemy_centers", 1),
##      (try_end),
##
##      (try_begin),
##        (eq, ":total_enemy_centers", 0),
##      (else_try),
##        (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
##        (assign, ":total_enemy_centers", 0),
##        (try_for_range, ":center_no", towns_begin, towns_end),
##          (eq, ":result", -1),
##          (store_faction_of_party, ":center_faction", ":center_no"),
##          (neq, ":center_faction", ":party_faction"),
##          (store_relation, ":party_relation", ":center_faction", ":party_faction"),
##          (le, ":party_relation", -10),
##          (val_add, ":total_enemy_centers", 1),
##          (lt, ":random_center", ":total_enemy_centers"),
##          (assign, ":result", ":center_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":result"),
##  ]),
# script_find_travel_location
# Input: arg1 = center_no
# Output: reg0 = new_center_no (to travel within the same faction)
("find_travel_location",
    [
      (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),

        (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (val_add, ":cur_distance", 1),

        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),

      (assign, reg0, -1),

      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),

          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (val_add, ":cur_distance", 1),

          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
  ])
]
