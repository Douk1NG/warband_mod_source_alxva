# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_pre_hire_troops_menu = [
(
    "town_pre_hire_troops",0,
    "Upon entering a seedy tavern you note the assortment of mercenaries, cut-throuts, refugees, and adventerous warriors. With some time and a little investigation, they could give you an overview of who's available for hire..^(this takes 1 hours)",
    "none",
    [],
    [
      ("continue",[],"Ask about..",
       [
           (store_sub, ":num_hours", 1),
           (rest_for_hours, ":num_hours", 5, 0), #rest while not attackable
           (change_screen_return),
           (jump_to_menu,"mnu_town_hire_troops"),
        ]),
      ("go_back",[],"Go back..",
       [
           (jump_to_menu,"mnu_dickplo_town_manage"),
        ]),
    ]
  )
]
