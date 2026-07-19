# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_notification_appoint_chamberlain_menu = [
(
    "dplmc_notification_appoint_chamberlain",0,
    "As a lord of a fief you can now appoint a chamberlain who resides at you court for a weekly salary of 15 denars. He will handle all financial affairs like collecting and determining taxes, paying wages and managing your estate. In addition he supervises money transfers between kingdoms giving you more diplomatic options.",
    "none",
    [],
    [

      ("dplmc_appoint_default",[],"Appoint a prominent nobleman from the area.",
       [
        (call_script, "script_dplmc_appoint_chamberlain"),
        (jump_to_menu, "mnu_dplmc_chamberlain_confirm"),
        ]),
      ("dplmc_continue",[],"Proceed without chamberlain.",
       [
         (assign, "$g_player_chamberlain", -1), #denied
         (change_screen_return),
        ]),
     ]
  )
]
