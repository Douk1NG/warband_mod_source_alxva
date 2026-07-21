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

center_get_food_store_limit_scripts = [
# script_center_get_food_store_limit
# Input: arg1 = center_no
# Output: reg0: food consumption (1 food item counts as 100 units)
("center_get_food_store_limit",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", 50000),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", 1500),
      (try_end),
      (assign, reg0, ":food_store_limit"),
  ])
]
