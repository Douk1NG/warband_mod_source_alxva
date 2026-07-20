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

get_random_tournament_participant_scripts = [
# script_get_random_tournament_participant
# Input: none
# Output: reg0 = troop_no
("get_random_tournament_participant",
    [(call_script, "script_get_num_tournament_participants"),
     (assign, ":num_participants", reg0),
     (store_random_in_range, ":random_troop", 0, ":num_participants"),
     (assign, ":continue", 1),
     (try_for_range, ":cur_slot", 0, 64),
       (eq, ":continue", 1),
       (troop_slot_ge, "trp_tournament_participants", ":cur_slot", 0),
       (val_sub, ":random_troop", 1),
       (lt, ":random_troop", 0),
       (assign, ":continue", 0),
       (troop_get_slot, ":troop_no", "trp_tournament_participants", ":cur_slot"),
       (troop_set_slot, "trp_tournament_participants", ":cur_slot", -1),
     (try_end),
     (assign, reg0, ":troop_no"),
     ])
]
