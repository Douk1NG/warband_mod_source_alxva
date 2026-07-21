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

get_troop_priority_point_for_tournament_scripts = [
# script_get_troop_priority_point_for_tournament
# Input: arg1 = troop_no
# Output: reg0 = troop_point
("get_troop_priority_point_for_tournament",
    [(store_script_param, ":troop_no", 1),
     (assign, ":troop_point", 0),
     (try_begin),
       (ge, ":troop_no", 0),
       (val_add, ":troop_point", 40000),
       (try_begin),
         (eq, ":troop_no", "trp_player"),
         (val_add, ":troop_point", 80000),
       (try_end),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (val_add, ":troop_point", 20000),
       (try_end),
       (try_begin),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
         (val_add, ":troop_point", 10000),
       (else_try),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
         (val_add, ":troop_point", ":renown"),
         (val_add, ":troop_point", 1000), #in order to make it more prior than tournament heroes with higher levels
       (else_try),
         (store_character_level, ":level", ":troop_no"),
         (val_add, ":troop_point", ":level"),
       (try_end),
     (try_end),
     (assign, reg0, ":troop_point"),
     ])
]
