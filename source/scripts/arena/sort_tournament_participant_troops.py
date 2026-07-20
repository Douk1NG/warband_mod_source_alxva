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

sort_tournament_participant_troops_scripts = [
# script_sort_tournament_participant_troops
# Input: none
# Output: none (sorts trp_tournament_participants)
("sort_tournament_participant_troops",
    [(try_for_range, ":cur_slot", 0, 63),
       (store_add, ":cur_slot_2_begin", ":cur_slot", 1),
       (try_for_range, ":cur_slot_2", ":cur_slot_2_begin", 64),
         (troop_get_slot, ":troop_1", "trp_tournament_participants", ":cur_slot"),
         (troop_get_slot, ":troop_2", "trp_tournament_participants", ":cur_slot_2"),
         (call_script, "script_get_troop_priority_point_for_tournament", ":troop_1"),
         (assign, ":troop_1_point", reg0),
         (call_script, "script_get_troop_priority_point_for_tournament", ":troop_2"),
         (assign, ":troop_2_point", reg0),
         (gt, ":troop_2_point", ":troop_1_point"),
         (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_2"),
         (troop_set_slot, "trp_tournament_participants", ":cur_slot_2", ":troop_1"),
       (try_end),
     (try_end),
     ])
]
