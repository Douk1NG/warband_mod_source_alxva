# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_hire_troops_menu = [
(
    "town_hire_troops",0,
    "This is the list you've managed to scrap together:",
    "none",
    [],
    [
      ("hire_farmers",[],"Hire farmers.",
       [
           (jump_to_menu,"mnu_town_hire_farmers"),
        ]),
      ("hire_cutthroats",[],"Hire villains, cutthrroats and looters.",
       [
           (jump_to_menu,"mnu_town_hire_cutthroats"),
        ]),
      ("hire_knights",[],"Hire knights in shiny armour.",
       [
           (jump_to_menu,"mnu_town_hire_knights"),
        ]),
      ("go_back",[],"Go back..",
       [
           (jump_to_menu,"mnu_dickplo_town_manage"),
        ]),
    ]
  )
]
