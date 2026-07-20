# ======================================================================
# SHARED DEPENDENCY
# Entity: game_get_upgrade_xp (script)
# Called by menus in 2 domains: cheats, town
# ======================================================================

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

game_get_upgrade_xp_scripts = [
# script_game_get_upgrade_xp
# This script is called from game engine for calculating needed troop upgrade exp
# Input:
# param1: troop_id,
# Output: reg0 = needed exp for upgrade
("game_get_upgrade_xp",
    [
      (store_script_param_1, ":troop_id"),

      (assign, ":needed_upgrade_xp", 0),
      #formula : int needed_upgrade_xp = 2 * (30 + 0.006f * level_boundaries[troops[troop_id].level + 3]);
      (store_character_level, ":troop_level", ":troop_id"),
      (store_add, ":needed_upgrade_xp", ":troop_level", 3),
      (get_level_boundary, reg0, ":needed_upgrade_xp"),
      (val_mul, reg0, 6),
      (val_div, reg0, 1000),
      (val_add, reg0, 30),

      (try_begin), #SB : merge range
        (is_between, ":troop_id", bandits_begin, bandits_end),
        (val_mul, reg0, 2),
      (try_end),

      (set_trigger_result, reg0),
  ])
]
