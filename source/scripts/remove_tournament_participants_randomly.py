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

remove_tournament_participants_randomly_scripts = [
# script_remove_tournament_participants_randomly
# Input: arg1 = number_to_be_removed
# Output: none
("remove_tournament_participants_randomly",
    [(store_script_param, ":number_to_be_removed", 1),
     #SB : TODO simulate tournament fighting relationship changes
     (try_for_range, ":unused", 0, ":number_to_be_removed"),
       (assign, ":total_weight", 0),
       (try_for_range, ":cur_slot", 0, 64),
         (troop_get_slot, ":troop_no", "trp_tournament_participants", ":cur_slot"),
         (ge, ":troop_no", 0),
         (store_character_level, ":level", ":troop_no"),
         (val_min, ":level", 38),
         (store_sub, ":weight", 40, ":level"),
         (val_add, ":total_weight", ":weight"),
       (try_end),
       (store_random_in_range, ":random_weight", 0, ":total_weight"),
       (assign, ":continue", 1),
       (try_for_range, ":cur_slot", 0, 64),
         (eq, ":continue", 1),
         (troop_get_slot, ":troop_no", "trp_tournament_participants", ":cur_slot"),
         (ge, ":troop_no", 0),
         (store_character_level, ":level", ":troop_no"),
         (val_min, ":level", 38),
         (store_sub, ":weight", 40, ":level"),
         (val_sub, ":random_weight", ":weight"),
         (lt, ":random_weight", 0),
         (troop_set_slot, "trp_tournament_participants", ":cur_slot", -1),
         (assign, ":continue", 0),
       (try_end),
     (try_end),
     ])
]
