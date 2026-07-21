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

cf_select_random_town_at_peace_with_faction_in_trade_route_scripts = [
#script_cf_select_random_town_at_peace_with_faction_in_trade_route
# INPUT:
# arg1 = town_no
# arg2 = faction_no
#OUTPUT:
# This script may return false if there is no matching town.
# reg0 = town_no
("cf_select_random_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
      (assign, ":result", -1),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (eq, ":result", -1),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_sub, ":random_town", 1),
        (lt, ":random_town", 0),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
