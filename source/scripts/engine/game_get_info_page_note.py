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

game_get_info_page_note_scripts = [
#script_game_get_info_page_note
# This script is called from the game engine when the notes of a info_page is needed.
# INPUT: arg1 = info_page_no, arg2 = note_index
# OUTPUT: s0 = note
("game_get_info_page_note",
    [
##      (store_script_param_1, ":info_page_no"),
##      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0), # set it to 1 if this script is wanted to be used rather than static notes
      #SB: TODO use actual settings for camera, ai_changes etc
     ])
]
