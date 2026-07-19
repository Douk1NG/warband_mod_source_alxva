# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_lord_defects_menu = [
(
    "notification_lord_defects",0,
##diplomacy start+ Fix gender of pronouns
    "Defection: {s4} has abandoned the {s5} and joined the {s7}, taking {reg4?her:his} fiefs with {reg4?her:him}",
##diplomacy end+
    "none",
	[
	  (assign, ":defecting_lord", "$g_notification_menu_var1"),
	  (assign, ":old_faction", "$g_notification_menu_var2"),
	  (str_store_troop_name, s4, ":defecting_lord"),
	  (str_store_faction_name, s5, ":old_faction"),
	  (store_faction_of_troop, ":new_faction", ":defecting_lord"),
	  (str_store_faction_name, s7, ":new_faction"),
	  ##diplomacy start+ get gender with script
	  #(troop_get_type, reg4, ":defecting_lord"),#<-OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":defecting_lord", 4),
	  ##diplomacy end+

	],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
	)
]
