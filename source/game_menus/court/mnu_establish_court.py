# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

establish_court_menu = [
("establish_court",mnf_disable_all_keys,
    "To establish {s4} as your court will require a small refurbishment. In particular, you will need a set of tools and a bolt of velvet. it may also take a short while for some of your followers to relocate here. Do you wish to proceed?",
    "none",
    [
	(str_store_party_name, s4, "$g_encountered_party"),
	],

    [
      ("establish",[
	  (player_has_item, "itm_tools"),
	  (player_has_item, "itm_velvet"),
	  ],"Establish {s4} as your court",
       [
		(assign, "$g_player_court", "$current_town"),
	    (troop_remove_item, "trp_player", "itm_tools"),
	    (troop_remove_item, "trp_player", "itm_velvet"),
        (jump_to_menu, "mnu_center_manage"),
       ]),

    ("capital_exists",
      [
        (store_and, ":name_set", "$players_kingdom_name_set", rename_center),
        (ge, ":name_set", rename_center),
        (str_store_party_name, s1, "$g_player_court"),
        (disable_menu_option),
      ],
       "You cannot move the court as your capital is at {s1}.",
       [
     ]),


      ("continue",[],"Hold off...",
       [
         (jump_to_menu, "mnu_center_manage"),
       ]),
    ]
  )
]
