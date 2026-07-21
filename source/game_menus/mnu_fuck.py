# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

fuck_menu = [
(
    "fuck",0,
    "Select a scene.",
    "none",
    [
	],
    [
      ("snow",[],"snow",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_snow"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Snow."),
      ("desert",[],"desert",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_desert"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Desert."),
      ("steppe",[],"steppe",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_steppe"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Steppe."),
      ("plain",[],"plain",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_camp_scene_plain"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Plain."),
      ("manor",[],"Manor",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_manor"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Manor."),
      ("tavern",[],"Tavern",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_tavern"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Tavern."),
      ("dungeon",[],"Dungeon",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_dungeon"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Dungeon."),
      ("ship_a",[],"Ship a",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_1"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship a."),
      ("ship_b",[],"Ship b",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_2"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship b."),
      ("ship_c",[],"Ship c",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_3"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship c."),
      ("ship_d",[],"Ship d",[
		  (assign, "$g_training_ground_melee_training_scene", "scn_sea_4"),
		  (jump_to_menu,"mnu_fuck_2"),
	  ],"Ship d."),
      # ("aa",[],"a a",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_a"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a a."),
      # ("ab",[],"a b",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_b"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a b."),
      # ("ac",[],"a c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a c."),
      # ("ad",[],"a d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_a_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"a d."),
      # ("bb",[],"b b",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_b"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b b."),
      # ("bc",[],"b c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b c."),
      # ("bd",[],"b d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_b_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"b d."),
      # ("cc",[],"c c",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_c_c"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"c c."),
      # ("cd",[],"c d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_c_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"c d."),
      # ("dd",[],"d d",[
		  # (assign, "$g_training_ground_melee_training_scene", "scn_sea_boarding_d_d"),
		  # (jump_to_menu,"mnu_fuck_2"),
	  # ],"d d."),
      ("leave",[],"back",[(jump_to_menu, "mnu_camp")]),
    ]
  )
]
