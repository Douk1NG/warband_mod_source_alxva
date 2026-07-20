# ======================================================================
# SHARED DEPENDENCY
# Entity: sneak_into_town_suceeded (menu)
# Called by menus in 2 domains: castle, diplomacy
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

sneak_into_town_suceeded_menu = [
(
    "sneak_into_town_suceeded",0,
    "Disguised in the garments of a poor {reg1?cheater:{s1}}, you fool the guards and make your way into the town.",
    "none",
    [(assign, reg1, "$cheat_mode"),
     (call_script, "script_get_disguise_string", "$sneaked_into_town", 1),

     # (try_begin),
       # (eq, "$sneaked_into_town", disguise_pilgrim),
       # (assign, ":string", "str_pilgrim_disguise"),
     # (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [
           # (assign, "$sneaked_into_town",1),
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  )
]
