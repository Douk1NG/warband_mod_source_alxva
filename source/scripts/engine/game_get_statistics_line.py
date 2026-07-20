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

game_get_statistics_line_scripts = [
#script_game_get_statistics_line:
# This script is called from the game engine when statistics page is opened.
# INPUT:
# param1: line_no
("game_get_statistics_line",
    [
      (store_script_param_1, ":line_no"),
      (try_begin),
        (eq, ":line_no", 0),
        (get_player_agent_kill_count, reg1),
        (str_store_string, s1, "str_number_of_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 1),
        (get_player_agent_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_troops_wounded_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 2),
        (get_player_agent_own_troop_kill_count, reg1),
        (str_store_string, s1, "str_number_of_own_troops_killed_reg1"),
        (set_result_string, s1),
      (else_try),
        (eq, ":line_no", 3),
        (get_player_agent_own_troop_kill_count, reg1, 1),
        (str_store_string, s1, "str_number_of_own_troops_wounded_reg1"),
        (set_result_string, s1),
      (try_end),
  ])
]
