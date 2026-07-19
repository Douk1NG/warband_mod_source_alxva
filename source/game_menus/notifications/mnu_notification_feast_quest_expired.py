# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_feast_quest_expired_menu = [
(
    "notification_feast_quest_expired",0,
    "{s10}",
    "none",
    [
    (str_store_string, s10, "str_feast_quest_expired"),
    ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  )
]
