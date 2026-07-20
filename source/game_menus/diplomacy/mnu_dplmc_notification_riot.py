# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_notification_riot_menu = [
(
    "dplmc_notification_riot",0,
    "The peasants of {s1} launched a riot against you! In a surprise attack, men loyal to you have been slain. The remainder joined the angry crowd.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (try_begin),
        (party_slot_eq, "$g_notification_menu_var1", slot_party_type, spt_town),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),
      ],
    [
      ("dplmc_continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  )
]
