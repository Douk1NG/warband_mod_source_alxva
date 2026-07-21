# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_withdraw_from_treasury (script)
# Called by menus in 2 domains: center_management, diplomacy
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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_withdraw_from_treasury_scripts = [
("dplmc_withdraw_from_treasury",
    [
      (store_script_param_1, ":amount"),
      (troop_remove_gold, "trp_household_possessions", ":amount"),
      (assign, reg0, ":amount"),
      (play_sound, "snd_money_paid"),
      (display_message, "@{reg0} denars removed from treasury."),
  ])
]
