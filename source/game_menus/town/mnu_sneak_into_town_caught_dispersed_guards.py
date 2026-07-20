# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

sneak_into_town_caught_dispersed_guards_menu = [
(
    "sneak_into_town_caught_dispersed_guards",0,
    "You drive off the guards and cover your trail before running off, easily losing your pursuers in the maze of streets.",
    "none",
    [],
    [
      ("continue",[],"Continue...",
       [
           (try_begin),
               (eq, "$sneaked_into_town", 0),
               (assign, "$sneaked_into_town",1),
           (try_end),

           (assign, "$town_entered", 1),
           #(assign, "$g_mt_mode", tcm_disguised),
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  )
]
