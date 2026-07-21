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

troop_get_leaded_center_with_index_scripts = [
# script_troop_count_number_of_enemy_troops
# Input: arg1 = troop_no, arg2 = center index within range between zero and the number of centers that troop owns
# Output: reg0 = center_no
("troop_get_leaded_center_with_index",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
