# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_game_1_menu = [
("start_game_1",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "Select your character's gender.",
    "none",
##diplomacy start+ Reset prejudice preferences
    [
        (assign, "$g_disable_condescending_comments", 0),
    ],
##diplomacy end+
    [
      ("start_male",[],"Male",
       [
         (troop_set_type,"trp_player", 0),
         (assign,"$character_gender", tf_male),
         (jump_to_menu,"mnu_start_character_1"),
        ]
       ),
      ("start_female",[],"Female",
       [
         (troop_set_type, "trp_player", 1),
         (assign, "$character_gender", tf_female),
##diplomacy start+
#Jump to the prejudice-level menu instead
#         (jump_to_menu, "mnu_start_character_1"),
         (jump_to_menu, "mnu_dplmc_start_select_prejudice"),
##diplomacy end+
       ]
       ),
	  ("go_back",[],"Go back",
       [
	     (jump_to_menu,"mnu_start_game_0"),
       ]),
    ]
  )
]
