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

cf_get_random_enemy_center_within_range_scripts = [
#script_get_random_melee_training_weapon
# Input: arg1 = party_no, arg2 = range (in kms)
# Output: reg0 = center_no
("cf_get_random_enemy_center_within_range",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":range", 2),

      (assign, ":num_centers", 0),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_add, ":num_centers", 1),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":cur_center", centers_begin, ":end_cond"),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
        (assign, ":end_cond", 0),#break
      (try_end),
      (assign, reg0, ":result"),
  ])
]
