# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_should_consult_menu = [
(
    "notification_player_should_consult",0,
##diplomacy start+ Replace "Your minister" with "{reg0?Your minister:{s11}}" and "him" with "{reg4?her:him}".
#Also "sends words" to "sends word"
    "{reg0?Your minister:{s11}} send word that there are problems brewing in the realm which, if left untreated, could sap your authority. You should consult with {reg4?her:him} at your earliest convenience",
	##diplomacy end+
    "none",
    [
      ],
    [
      ("continue",[],"Continue...",
       [
	    (setup_quest_text, "qst_consult_with_minister"),

        (str_store_troop_name, s11, "$g_player_minister"),
        (str_store_party_name, s12, "$g_player_court"),

		(str_store_string, s2, "str_consult_with_s11_at_your_court_in_s12"),
	    (call_script, "script_start_quest", "qst_consult_with_minister", -1),
		##diplomacy start+ Set minister gender and reg0 for generic vs specific
		(assign, reg4, 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", "$g_player_minister"),
			(assign, reg4, 1),
		(try_end),
		(assign, reg0, 1),
		(try_begin),
			(is_between, "$g_player_minister", heroes_begin, heroes_end),
			(assign, reg0, 0),
		(try_end),
		##diplomacy end+

		(quest_set_slot, "qst_consult_with_minister", slot_quest_expiration_days, 30),
		(quest_set_slot, "qst_consult_with_minister", slot_quest_giver_troop, "$g_player_minister"),


	    (change_screen_return),
        ]),
     ]
  )
]
