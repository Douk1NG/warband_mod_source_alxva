# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_start_select_prejudice_menu = [
("dplmc_start_select_prejudice",menu_text_color(0xFF000000)|mnf_disable_all_keys,
    "In the traditional medieval society depicted in the game, war and politics are usually dominated by male members of the nobility.  Because of this, a female character can face initial prejudice, and some opportunities open to men will not be available (although a woman will also have some opportunities a man will not).  Some players might find distasteful, so if you want you can ignore that aspect of society in Calradia.^^You can later change your mind through the options in the Camp menu.",
    "none",
    [],
    [
      ("dplmc_start_prejudice_yes",[],"I do not mind encountering sexism.",
       [
         (assign, "$g_disable_condescending_comments", 0),#Default value
         (jump_to_menu,"mnu_start_character_1"),
        ]
       ),
      ("dplmc_start_prejudice_no",[],"I would prefer not to encounter as much sexism.",
       [
         (assign, "$g_disable_condescending_comments", 2),#Any value 2 or higher shuts off sexist setting elements
         (jump_to_menu, "mnu_start_character_1"),
       ]
       ),
	  ("go_back",[],"Go back",
       [
	     (jump_to_menu,"mnu_start_game_1"),
       ]),
    ]
  )
]
