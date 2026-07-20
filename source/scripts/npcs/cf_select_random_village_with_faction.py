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

cf_select_random_village_with_faction_scripts = [
#script_cf_select_random_village_with_faction:
# This script selects a random village in range [villages_begin, villages_end)
# such that faction of the village is equal to given_faction
# INPUT:
# arg1 = faction_no
#OUTPUT:
# This script may return false if there is no matching village.
# reg0 = village_no
("cf_select_random_village_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
      (try_end),
      (gt, ":no_villages", 0), #Fail if there are no villages
      (store_random_in_range, ":random_village", 0, ":no_villages"),
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
        (gt, ":no_villages", ":random_village"),
        (assign, ":result", ":cur_village"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
