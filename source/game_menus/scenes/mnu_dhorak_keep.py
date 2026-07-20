# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dhorak_keep_menu = [
(
    "dhorak_keep",0,
#    "Dhorak Keep, the stronghold of the bandits stands overlooking the barren wilderness.",
    "You enter the Dhorak Keep",
    "none",
    [],
    [
      ("enter",[],"Enter.",[(set_jump_mission,"mt_town_center"),(jump_to_scene,"scn_dhorak_keep"),(change_screen_mission)]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  )
]
