# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_preferences_menu = [
(
    "dplmc_preferences",0,
    "All Options",## Hijacked this to be the consolidated options menu.
    "none",
    [],
    [
	  # XGM Mod Menu, contains most basic settings
      ("camp_mod_opition",[],"Main Settings", [(start_presentation, "prsnt_mod_option")]),
	  # Formations Mod Settings
      ("formation_mod_option",[],"Formations Mod Settings", [(start_presentation, "prsnt_formation_mod_option")]),
	  # Camera Hotkeys
      ("dplmc_deathcam_keys",[ (eq, "$g_dplmc_battle_continuation", 0),],"Camera Keys Settings",[(assign, "$g_presentation_next_presentation", "prsnt_redefine_keys"),(start_presentation, "prsnt_redefine_keys"),]),
      ("dplmc_back",[],"Return",
       [
           (jump_to_menu, "mnu_camp"),
        ]),
     ]
  )
]
