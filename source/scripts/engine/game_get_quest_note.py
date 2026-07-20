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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_quest_note_scripts = [
#script_game_get_center_note
# This script is called from the game engine when the notes of a quest is needed.
# INPUT: arg1 = quest_no, arg2 = note_index
# OUTPUT: s0 = note
("game_get_quest_note",
    [
##      (store_script_param_1, ":quest_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
      #SB: TODO set up progress for pretender quests and other long-winding series
     ])
]
