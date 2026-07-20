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

get_num_tournament_participants_scripts = [
# script_get_num_tournament_participants
# Input: none
# Output: reg0 = num_participants
("get_num_tournament_participants",
    [(assign, ":num_participants", 0),
     (try_for_range, ":cur_slot", 0, 64),
       (troop_slot_ge, "trp_tournament_participants", ":cur_slot", 0),
       (val_add, ":num_participants", 1),
     (try_end),
     (assign, reg0, ":num_participants"),
     ])
]
