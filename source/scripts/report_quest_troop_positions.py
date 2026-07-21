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

report_quest_troop_positions_scripts = [
#script_report_quest_troop_positions
# INPUT: arg1 = quest_no, arg2 = troop_no, arg3 = note_index
# OUTPUT: none
("report_quest_troop_positions",
    [
      (store_script_param, ":quest_no", 1),
      (store_script_param, ":troop_no", 2),
      (store_script_param, ":note_index", 3),
      (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
      (str_store_string, s5, "@At the time quest was given:^{s1}"),
      (add_quest_note_from_sreg, ":quest_no", ":note_index", s5, 1),
      (call_script, "script_update_troop_location_notes", ":troop_no", 1),
    ])
]
