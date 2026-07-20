# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_affiliated_family_report_menu = [
("dplmc_affiliated_family_report",0,
   "{s0}",
   "none",
   [
    (str_clear, s0),
	(str_clear, s1),
	(try_for_range, ":troop_no", active_npcs_including_player_begin, heroes_end),
		(try_begin),
			(eq, ":troop_no", active_npcs_including_player_begin),
			(assign, ":troop_no", "trp_player"),
		(try_end),
		(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":troop_no"),
		(this_or_next|eq, ":troop_no", "trp_player"),
           (ge, reg0, 1),

		(str_clear, s1),
		(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add blank line to start

		#show name; (non-player) also show location
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(str_store_string, s1, "@{playername}"),
		(else_try),
			(call_script, "script_get_information_about_troops_position", ":troop_no", 0),#s1 = String, reg0 = knows-or-not
		(try_end),
		(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line

		#(non-player) show relation
		(try_begin),
			(neq, "trp_player", ":troop_no"),
			(call_script, "script_troop_get_player_relation", ":troop_no"),
			(assign, reg1, reg0) ,
			(str_store_string, s1, "str_relation_reg1"),
			(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line
		(try_end),

		#(non-prisoner) show party size
		(try_begin),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
            (this_or_next|eq, ":led_party", 0),
			   (ge, ":led_party", spawn_points_end),
			(this_or_next|eq, ":troop_no", "trp_player"),
			   (neq, ":led_party", "p_main_party"),
			(party_is_active, ":led_party"),
			(assign, reg0, 0),
			(party_get_num_companions, reg1, ":led_party"),#number of troops
            (str_store_string, s1, "@Troops: {reg1}"),
			(str_store_string, s0, "str_dplmc_s0_newline_s1"),#add line
		(try_end),

	(try_end),
    ],
    [
	  ("lord_relations",[],"View list of all known lords by relation.",
       [
		(jump_to_menu, "mnu_lord_relations"),
        ]
       ),
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
