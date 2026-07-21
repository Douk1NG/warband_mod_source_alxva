# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_feast_in_progress_menu = [
(
    "notification_player_feast_in_progress",0,
##diplomacy start+ make gender correct
    "Feast in Preparation^^Your {wife/husband} has started preparations for a feast in your hall in {s11}",
##diplomacy end+
    "none",
    [
    (str_store_party_name, s11, "$g_notification_menu_var1"),
    ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
