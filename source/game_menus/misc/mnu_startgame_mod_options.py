# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

startgame_mod_options_menu = [
(
    "startgame_mod_options",0,
    "Now decide how the world will behave.^Nearly everything may be changed later through the camp menu, but the content option will make some irreversable changes to the game world.",
    "none",
    [],
    [
	  # XGM Mod Menu, contains most basic settings
      ("camp_mod_opition",[],"Change Settings", [(start_presentation, "prsnt_mod_option"),(assign, "$f_temp_var", 1),]),
      ("options_back",[],"Continue",
       [
			(try_begin),
				(eq, "$f_temp_var", 0),
				(display_message, "@You haven't checked the options yet. Are you sure?"),
				(assign, "$f_temp_var", 2),
			(else_try),
				(eq, "$f_temp_var", 2),
				(display_message, "@Absolutely sure?"),
				(assign, "$f_temp_var", 3),
			(else_try),
				(eq, "$f_temp_var", 3),
				(assign, "$f_temp_var", 0),
				(display_message, "@Ok, fine."),
				(jump_to_menu, "mnu_c3_finalize"),
			(else_try),
				(assign, "$f_temp_var", 0),
				(jump_to_menu, "mnu_c3_finalize"),
			(try_end),
        ]),
     ]
  )
]
