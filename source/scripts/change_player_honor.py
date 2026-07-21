# ======================================================================
# SHARED DEPENDENCY
# Entity: change_player_honor (script)
# Called by menus in 6 domains: castle, character_creation, cheats, dickplomacy, town, village
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

change_player_honor_scripts = [
("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      ##diplomacy start+
      #Exacerbate the effect of honor losses as the player's honor increases
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- experimental settings must be enabled
         (ge, "$player_honor", 10),
         (lt, ":honor_dif", 0),
         (store_add, ":honor_multiplier", "$player_honor", 100),
         (val_mul, ":honor_dif", ":honor_multiplier"),
         (val_sub, ":honor_dif", 50),
         (val_div, ":honor_dif", 100),
      (try_end),
      ##diplomacy end+
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour.", message_positive),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour.", message_negative),
      (try_end),

##      (val_mul, ":honor_dif", 1000),
##      (assign, ":temp_honor", 0),
##      (assign, ":num_nonlinear_steps", 10),
##      (try_begin),
##        (gt, "$player_honor", 0),
##        (lt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 0),
##      (else_try),
##        (lt, "$player_honor", 0),
##        (gt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 3),
##      (try_end),
##
##      (try_begin),
##        (ge, "$player_honor", 0),
##        (assign, ":temp_honor", "$player_honor"),
##      (else_try),
##        (val_sub, ":temp_honor", "$player_honor"),
##      (try_end),
##      (try_for_range, ":unused",0,":num_nonlinear_steps"),
##        (ge, ":temp_honor", 10000),
##        (val_div, ":temp_honor", 2),
##        (val_div, ":honor_dif", 2),
##      (try_end),
##      (val_add, "$player_honor", ":honor_dif"),
  ])
]
