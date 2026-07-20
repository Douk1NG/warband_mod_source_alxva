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

game_get_money_text_scripts = [
#script_game_get_money_text:
# This script is called from the game engine when an amount of money needs to be displayed.
# INPUT: arg1 = amount in units
# OUTPUT: result string = money in text
("game_get_money_text",
    [
      (store_script_param_1, ":amount"),
      (try_begin),
        (eq, ":amount", 1),
        (str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
        (str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
  ])
]
