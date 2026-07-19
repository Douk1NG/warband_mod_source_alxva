# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_chancellor_confirm_menu = [
(
    "dplmc_chancellor_confirm",0,
    "Your chancellor can be found at your court. You should consult him if you want to send messages or gifts.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  )
]
