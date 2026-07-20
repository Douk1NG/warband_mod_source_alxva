# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

fuck_2_menu = [
(
    "fuck_2",0,
    "Pick a position",
    "none",
    [(assign, "$g_sex_position", 0),
	 (assign, "$temp", 3),
	 (assign, "$temp_2", 1),
	 (call_script, "script_write_fit_party_members_to_stack_selection", "p_main_party", 1),
	],
    [
      ("op_1",[],"Riding",[
		  (assign, "$g_sex_position", 0),
		  (jump_to_menu,"mnu_fuck_3"),
	  ],"Riding"),
      ("op_2",[],"Fucking from behind",[
		  (assign, "$g_sex_position", 1),
		  (jump_to_menu,"mnu_fuck_3"),
	  ]),
      ("op_3",[],"Fucking both ends",[
		  (assign, "$g_sex_position", 2),
		  (assign, "$temp", 4),
		  (jump_to_menu,"mnu_fuck_3"),
	  ]),
      ("leave",[],"Go back.",[(jump_to_menu, "mnu_camp")]),
	]
  )
]
