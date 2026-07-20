# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

retirement_verify_menu = [
("retirement_verify",0,
   "You are at day {reg0}. Your current luck is {reg1}. Are you sure you want to retire?",
   "none",
   [
     (store_current_day, reg0),
     (assign, reg1, "$g_player_luck"),
     ],
    [
      ("retire_yes",[],"Yes.",
       [
         (start_presentation, "prsnt_retirement"),
        ]
       ),
      ("retire_no",[],"No.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
