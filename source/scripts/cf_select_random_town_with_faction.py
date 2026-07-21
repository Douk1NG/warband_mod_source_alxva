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

cf_select_random_town_with_faction_scripts = [
# This script selects a random town in range [towns_begin, towns_end)
# INPUTS:
# none
#OUTPUT:
# reg0: id of the selected random town
##  ("select_random_town",
##    [
##      (assign, ":num_towns", towns_end),
##      (val_sub,":num_towns", towns_begin),
##      (store_random, ":random_town", ":num_towns"),
##      (val_add,":random_town", towns_begin),
##      (assign, reg0, ":random_town"),
##  ]),
#  ("select_random_spawn_point",
#    [
#      (assign, reg(20), spawn_points_end),
#      (val_sub,reg(20), spawn_points_begin),
#      (store_random, reg(21), reg(20)),
#      (val_add,reg(21), spawn_points_begin),
#      (assign, "$pout_town", reg(21)),
# ]),
#script_cf_select_random_town_with_faction:
# This script selects a random town in range [towns_begin, towns_end)
# such that faction of the town is equal to given_faction
# INPUT:
# arg1 = faction_no
#OUTPUT:
# This script may return false if there is no matching town.
# reg0 = town_no
("cf_select_random_town_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
