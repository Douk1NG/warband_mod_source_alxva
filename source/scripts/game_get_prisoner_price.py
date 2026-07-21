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

game_get_prisoner_price_scripts = [
# script_game_get_prisoner_price
# This script is called from the game engine for calculating prisoner price
# Input:
# param1: troop_id,
# Output: reg0
("game_get_prisoner_price",
    [
      (store_script_param_1, ":troop_id"),

      (try_begin), #SB : regular prices for constable selling
        (this_or_next|eq, "$g_talk_troop", "$g_player_constable"),
        (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
        (store_character_level, ":troop_level", ":troop_id"),
        (store_add, ":ransom_amount", ":troop_level", 10),
        # (val_add, ":ransom_amount", 10),
        (val_mul, ":ransom_amount", ":ransom_amount"),
        (val_div, ":ransom_amount", 6),
      (else_try),
        # (eq, "$g_talk_troop", "trp_brothel_madam"),
        # (assign, ":ransom_amount", 0),
      # (else_try),
        (assign, ":ransom_amount", 100),
      (try_end),

      (assign, reg0, ":ransom_amount"),

      (set_trigger_result, reg0),
  ])
]
