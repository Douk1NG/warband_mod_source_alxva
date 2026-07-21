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

game_check_prisoner_can_be_sold_scripts = [
# script_game_check_prisoner_can_be_sold
# This script is called from the game engine for checking if a given troop can be sold.
# Input:
# param1: troop_id,
# Output: reg0: 1= can be sold; 0= cannot be sold.
("game_check_prisoner_can_be_sold",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (try_begin),
          (check_quest_active, "qst_hunt_down_fugitive"),
          (eq, ":troop_id", "trp_fugitive"), #SB : can't sell quest troops
          (assign, reg0, 0),
        (else_try),
          (check_quest_active, "qst_hunt_down_fugitive"),
          (this_or_next|eq, ":troop_id", "trp_spy"),
          (eq, ":troop_id", "trp_spy_partner"),
          (assign, reg0, 0),
        (else_try),
          (assign, reg0, 1),
        (try_end),
      (try_end),

      #sell women only
      # (try_begin),
          # (eq, "$g_talk_troop", "trp_brothel_madam"),
          # (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_id", 65),
          # (assign, ":is_female", reg65),
          # (neq, ":is_female", 1),
          # (assign, reg0, 0),
      # (try_end),

      (set_trigger_result, reg0),
  ])
]
