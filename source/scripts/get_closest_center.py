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

get_closest_center_scripts = [
##  ("cf_select_faction_spawn_point",
# Input: arg1 = party_no
# Output: reg0 = center_no (closest)
("get_closest_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ])
]
