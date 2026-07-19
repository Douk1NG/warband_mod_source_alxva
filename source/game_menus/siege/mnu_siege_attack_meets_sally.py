# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

siege_attack_meets_sally_menu = [
(
    "siege_attack_meets_sally",mnf_scale_picture,
    "The defenders sally out to meet your assault.",
    "none",
    [
        (set_background_mesh, "mesh_pic_sally_out"),
    ],
    [
      ("continue",[],
       "Continue...",
       [
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
       ]),
    ]
  )
]
