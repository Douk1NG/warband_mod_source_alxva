# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_deserters_menu = [
(
    "dplmc_deserters",0,
    "Some of your men don't believe that you will pay their wages and desert. Overall you lose: {s11} men.",
    "none",
    [
      (set_background_mesh, "mesh_pic_deserters"),
      (store_random_in_range, ":random", 1,  "$g_notification_menu_var1"),
      (call_script, "script_dplmc_player_troops_leave", ":random"),
      (str_store_string, s11, "@{reg0}"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  )
]
