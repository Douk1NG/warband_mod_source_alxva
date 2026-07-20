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

game_get_party_prisoner_limit_scripts = [
# script_cf_multiplayer_evaluate_poll
# This script is called from the game engine when the prisoner limit is needed for a party.
# INPUT: arg1 = party_no
# OUTPUT: reg0 = prisoner_limit
("game_get_party_prisoner_limit",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":troop_no", "trp_player"),

      (assign, ":limit", 0),
      (store_skill_level, ":skill", "skl_prisoner_management", ":troop_no"),
      (store_mul, ":limit", ":skill", 5),
      (try_begin), #SB : override with diplomacy_var2
        (eq, "$diplomacy_var", DPLMC_CURRENT_VERSION_CODE),
        (assign, ":limit", "$diplomacy_var2"),
      (try_end),
      (try_begin),
        (eq, ":party_no", "p_main_party"),
        (troop_get_slot, ":renown_prisoner_capacity_bonus", "trp_player", slot_troop_renown),
        (val_div, ":renown_prisoner_capacity_bonus", 20),
        (val_add, ":limit", ":renown_prisoner_capacity_bonus"),
      (try_end),
      (assign, reg0, ":limit"),
      (set_trigger_result, reg0),
  ])
]
