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

add_tournament_participant_scripts = [
# script_add_tournament_participant
# Input: arg1 = troop_no
# Output: none
("add_tournament_participant",
    [(store_script_param, ":troop_no", 1),
     (assign, ":continue", 1),
     (try_for_range, ":cur_slot", 0, 64),
       (eq, ":continue", 1),
       (troop_slot_eq, "trp_tournament_participants", ":cur_slot", -1),
       (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
       (assign, ":continue", 0),
     (try_end),
     ])
]
