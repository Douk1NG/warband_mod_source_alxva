# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_sortie_possible_menu = [
(
    "notification_sortie_possible",0,
    "Enemy Sighted: Enemies have been sighted outside the walls of {s4}, and {s5} and others are preparing for a sortie. You may join them if you wish.",
    "none",
    [
	(str_store_party_name, s4, "$g_notification_menu_var1"),
	(party_stack_get_troop_id, ":leader", "$g_notification_menu_var2", 0),
	(str_store_troop_name, s5, ":leader"),
      ],
    [
      ("continue",[],"Continue",
       [
	   #stop auto-clock

	   (change_screen_return),
        ]),
     ]
  )
]
