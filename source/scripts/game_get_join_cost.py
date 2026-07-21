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

game_get_join_cost_scripts = [
# script_game_get_join_cost
# This script is called from the game engine for calculating troop join cost.
# Input:
# param1: troop_id,
# Output: reg0: weekly wage
("game_get_join_cost",
    [
      (store_script_param_1, ":troop_id"),

      (assign,":join_cost", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":troop_level", ":troop_id"),
        (store_add, ":join_cost", ":troop_level", 5),
        (val_mul, ":join_cost", ":join_cost"),
        (val_add, ":join_cost", 40),
        (val_div, ":join_cost", 5),
        (try_begin), #mounted troops cost %100 more than the normal cost
          (troop_is_mounted, ":troop_id"),
          (val_mul, ":join_cost", 2),
        (try_end),
      (try_end),
      (assign, reg0, ":join_cost"),
      (set_trigger_result, reg0),
  ])
]
