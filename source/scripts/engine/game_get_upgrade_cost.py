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

game_get_upgrade_cost_scripts = [
# script_game_get_upgrade_cost
# This script is called from game engine for calculating needed troop upgrade exp
# Input:
# param1: troop_id,
# Output: reg0 = needed cost for upgrade
("game_get_upgrade_cost",
    [
      (store_script_param_1, ":troop_id"),

      (store_character_level, ":troop_level", ":troop_id"),

      (try_begin),
        (is_between, ":troop_level", 0, 6),
        (assign, reg0, 10),
      (else_try),
        (is_between, ":troop_level", 6, 11),
        (assign, reg0, 20),
      (else_try),
        (is_between, ":troop_level", 11, 16),
        (assign, reg0, 40),
      (else_try),
        (is_between, ":troop_level", 16, 21),
        (assign, reg0, 80),
      (else_try),
        (is_between, ":troop_level", 21, 26),
        (assign, reg0, 120),
      (else_try),
        (is_between, ":troop_level", 26, 31),
        (assign, reg0, 160),
      (else_try),
        (assign, reg0, 200),
      (try_end),

      (set_trigger_result, reg0),
  ])
]
