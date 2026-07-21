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

cf_select_random_walled_center_with_faction_scripts = [
#script_cf_select_random_walled_center_with_faction:
# This script selects a random center in range [centers_begin, centers_end)
# such that faction of the town is equal to given_faction
# INPUT:
# arg1 = faction_no
# arg2 = preferred_center_no
#OUTPUT:
# This script may return false if there is no matching town.
# reg0 = town_no (Can fail)
("cf_select_random_walled_center_with_faction",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_centers", 1),
        (eq, ":cur_center", ":preferred_center_no"),
        (val_add, ":no_centers", 99),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
