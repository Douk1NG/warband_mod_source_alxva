# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_messenger_menu = [
(
    "dplmc_messenger",0,
##nested diplomacy start+ "His" to "{reg4?Her:His}"
    "Sire, I found {s10} and delivered your message. {reg4?Her:His} answer was {s11}.",
##nested diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (str_store_troop_name, s10, "$g_notification_menu_var1"),
        (try_begin),
          (eq, "$g_notification_menu_var2", 1),
          (str_store_string, s11, "@positive"),
        (else_try),
          (str_store_string, s11, "@negative"),
        (try_end),
        ##nested diplomacy start+
        (try_begin),
           (call_script, "script_cf_dplmc_troop_is_female", "$g_notification_menu_var1"),
           (assign, reg4, 1),
        (else_try),
           (assign, reg4, 0),
        (try_end),
        ##nested diplomacy end+
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  )
]
