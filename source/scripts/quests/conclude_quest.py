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

conclude_quest_scripts = [
#script_conclude_quest
# INPUT: arg1 = quest_no
# OUTPUT: none
("conclude_quest",
    [
      (store_script_param, ":quest_no", 1),
      (conclude_quest, ":quest_no"),
      (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
      (str_store_troop_name, s59, ":quest_giver_troop"),
      (add_quest_note_from_sreg, ":quest_no", 7, "@This quest has been concluded. Talk to {s59} to finish it.", 0),
    ])
]
