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

cancel_quest_scripts = [
#script_cancel_quest
# INPUT: arg1 = quest_no
# OUTPUT: none
("cancel_quest",
    [(store_script_param, ":quest_no", 1),
     (str_clear, s1),
     (add_quest_note_from_sreg, ":quest_no", 0, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 1, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 2, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
     (add_quest_note_from_sreg, ":quest_no", 7, s1, 0),
     (cancel_quest, ":quest_no"),
     (try_begin),
       (is_between, ":quest_no", mayor_quests_begin, mayor_quests_end),
       (assign, "$merchant_quest_last_offerer", -1),
       (assign, "$merchant_offered_quest", -1),
     (try_end),
     ])
]
