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

get_troop_holdings_scripts = [
("get_troop_holdings",
     [
         (store_script_param, ":troop_no", 1),

         (assign, ":owned_centers", 0),
         (assign, ":num_centers", 0),
         (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
             (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
             (try_begin),
               (eq, ":num_centers", 0),
               (str_store_party_name, s50, ":cur_center"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (eq, ":num_centers", 1),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{s57} and {s50}"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{!}{s57}, {s50}"),
               (val_add, ":owned_centers", 1),
             (try_end),
             (val_add, ":num_centers", 1),
         (try_end),
         (assign, reg50, ":owned_centers"),
     ])
]
