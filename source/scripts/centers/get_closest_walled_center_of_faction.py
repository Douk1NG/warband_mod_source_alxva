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

get_closest_walled_center_of_faction_scripts = [
# script_get_closest_center
# Input: arg1 = party_no, arg2 = kingdom_no
# Output: reg0 = center_no (closest)
("get_closest_walled_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
