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

cf_troop_get_random_leaded_walled_center_with_less_strength_priority_scripts = [
# script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority
# Input: arg1 = troop_no, arg2 = preferred_center_no
# Output: reg0 = center_no (Can fail)
("cf_troop_get_random_leaded_walled_center_with_less_strength_priority",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":preferred_center_no", 2),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_add, ":num_centers", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_add, ":num_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":center_no"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":num_centers", ":strength"),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":center_no"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
