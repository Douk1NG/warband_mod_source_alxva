# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_notification_appoint_chancellor_menu = [
(
    "dplmc_notification_appoint_chancellor",0,
    "As a lord of a fief you can now appoint a chancellor who resides at you court for a weekly salary of 20 denars. He will be the keeper of your seal and conduct the correspondence between you and other important persons.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent nobleman from the area.",
       [
        (call_script, "script_dplmc_appoint_chancellor"),
        (jump_to_menu, "mnu_dplmc_chancellor_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without chancellor.",
       [
         (assign, "$g_player_chancellor", -1), #denied
         (change_screen_return),
        ]),
     ]
  )
]
