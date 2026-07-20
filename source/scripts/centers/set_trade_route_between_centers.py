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

set_trade_route_between_centers_scripts = [
#script_game_get_faction_note
# INPUT:
# param1: center_no_1
# param1: center_no_2
("set_trade_route_between_centers",
    [(store_script_param, ":center_no_1", 1),
     (store_script_param, ":center_no_2", 2),
     (assign, ":center_1_added", 0),
     (assign, ":center_2_added", 0),
     (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
       (try_begin),
         (eq, ":center_1_added", 0),
         (party_slot_eq, ":center_no_1", ":cur_slot", 0),
         (party_set_slot, ":center_no_1", ":cur_slot", ":center_no_2"),
         (assign, ":center_1_added", 1),
       (try_end),
       (try_begin),
         (eq, ":center_2_added", 0),
         (party_slot_eq, ":center_no_2", ":cur_slot", 0),
         (party_set_slot, ":center_no_2", ":cur_slot", ":center_no_1"),
         (assign, ":center_2_added", 1),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":center_1_added", 0),
       (str_store_party_name, s1, ":center_no_1"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     (try_begin),
       (eq, ":center_2_added", 0),
       (str_store_party_name, s1, ":center_no_2"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     ])
]
