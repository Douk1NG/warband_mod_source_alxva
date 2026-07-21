# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

companion_report_menu = [
("companion_report",0,
   "{s7}{s2}",
   "none",
   [
   (str_clear, s1),
   (str_clear, s2),
   (str_store_string, s7, "str_no_companions_in_service"),

   (try_begin),
	(troop_get_slot, ":spouse_or_betrothed", "trp_player", slot_troop_spouse),
	(try_begin),
		##diplomacy start+ Test gender with script
		#(troop_get_type, ":is_female", "trp_player"),#<- replaced
		(call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
		#(eq, ":is_female", 1),#<- replaced
		##diplomacy end+
		(str_store_string, s8, "str_husband"),
	(else_try),
		(str_store_string, s8, "str_wife"),
	(try_end),

	(try_begin),
		(le, ":spouse_or_betrothed", 0),
		(troop_get_slot, ":spouse_or_betrothed", "trp_player", slot_troop_betrothed),
		(str_store_string, s8, "str_betrothed"),
	(try_end),
	(gt, ":spouse_or_betrothed", 0),

	(str_store_troop_name, s4, ":spouse_or_betrothed"),
	(troop_get_slot, ":cur_center", ":spouse_or_betrothed", slot_troop_cur_center),
	(try_begin),
		(is_between, ":cur_center", centers_begin, centers_end),
		(str_store_party_name, s5, ":cur_center"),
	(else_try),
		(troop_slot_eq, ":spouse_or_betrothed", slot_troop_occupation, slto_kingdom_hero),
		(str_store_string, s5, "str_leading_party"),
	(else_try),
		(str_store_string, s5, "str_whereabouts_unknown"),
    (try_end),
	(str_store_string, s3, "str_s4_s8_s5"),
	# (str_store_string, s2, s1),
	(str_store_string, s2, "str_s2_s3"),

   (try_end),


   (try_begin),
    (ge, "$cheat_mode", 1),
	(ge, "$npc_to_rejoin_party", 0),
    (str_store_troop_name, s5, "$npc_to_rejoin_party"),
    (str_store_string, s1, s2),
	(str_store_string, s2, "@{!}DEBUG -- {s1}^NPC in rejoin queue: {s5}^"),
   (try_end),


   (try_for_range, ":companion", companions_begin, companions_end),
		# (str_clear, s2),
		(str_clear, s3),

		(try_begin),
			# (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),

			(troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
            #SB : replace the call
            (call_script, "script_companion_get_mission_string", ":companion"),


			# (str_store_troop_name, s4, ":companion"),

			# (try_begin),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
				# (str_store_string, s8, "str_gathering_support"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
				# (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
				# (str_store_party_name, s11, ":town_with_contacts"),

				# (str_store_string, s8, "str_gathering_intelligence"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),	#This covers most diplomatic missions

				# (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				# ##diplomacy begin
				# (neg|troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible), #SB : replace hard constant 8
        		# ##diplomacy end

				# (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
				# (str_store_faction_name, s9, ":faction"),
				# (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
				# (try_begin),
					# (eq, ":days_left", 1),
					# (str_store_string, s5, "str_expected_back_imminently"),
				# (else_try),
					# (assign, reg3, ":days_left"),
					# (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
				# (try_end),
			# (else_try),
				# (eq, ":companion", "$g_player_minister"),
				# (str_store_string, s8, "str_serving_as_minister"),
				# (try_begin),
					# (is_between, "$g_player_court", centers_begin, centers_end),
					# (str_store_party_name, s9, "$g_player_court"),
					# (str_store_string, s5, "str_in_your_court_at_s9"),
				# (else_try),
					# (str_store_string, s5, "str_whereabouts_unknown"),
				# (try_end),
			# (else_try),
				# (main_party_has_troop, ":companion"),
				# (str_store_string, s8, "str_under_arms"),
				# (str_store_string, s5, "str_in_your_party"),
			# (else_try),
				# (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
				# (str_store_string, s8, "str_attempting_to_rejoin_party"),
				# (str_store_string, s5, "str_whereabouts_unknown"),
			# (else_try),	#Companions who are in a center
				# (troop_slot_ge, ":companion", slot_troop_cur_center, 1),

				# (str_store_string, s8, "str_separated_from_party"),
				# (str_store_string, s5, "str_whereabouts_unknown"),
			# (else_try), #Excludes companions who have occupation = retirement
				# (try_begin),
					# (check_quest_active, "qst_lend_companion"),
					# (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
					# (str_store_string, s8, "@On loan,"),
				# (else_try),
					# (check_quest_active, "qst_lend_surgeon"),
					# (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
					# (str_store_string, s8, "@On loan,"),
				# (else_try),
					# (troop_set_slot, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
					# (str_store_string, s8, "str_attempting_to_rejoin_party"),
				# (try_end),
				# (str_store_string, s5, "str_whereabouts_unknown"),

				(try_begin),
					(ge, "$cheat_mode", 1),
					(troop_get_slot, reg2, ":companion", slot_troop_current_mission),
					(troop_get_slot, reg3, ":companion", slot_troop_days_on_mission),
					(troop_get_slot, reg4, ":companion", slot_troop_prisoner_of_party),
					(troop_get_slot, reg4, ":companion", slot_troop_playerparty_history),

					(display_message, "@{!}DEBUG: {s4} current mission: {reg2}, days on mission: {reg3}, prisoner: {reg4}, pphistory: {reg5}"),
				(try_end),
			# (try_end),

			# (str_store_string, s3, "str_s4_s8_s5"),

			# (str_store_string, s2, s1),
            (str_store_string_reg, s3, s0),
			(str_store_string, s2, "str_s2_s3"),

			(str_clear, s7), #"no companions in service"
		# (else_try),
			# (neg|troop_slot_eq, ":companion", slot_troop_occupation, slto_kingdom_hero),
			# (troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),

			# (str_store_troop_name, s4, ":companion"),
			# (str_store_string, s8, "str_missing_after_battle"),
			# (str_store_string, s5, "str_whereabouts_unknown"),

			# (str_store_string, s3, "str_s4_s8_s5"),
			# (str_store_string, s2, s1),
			# (str_store_string, s1, "str_s2_s3"),
			# (str_clear, s7), #"no companions in service"

		(try_end),

   (try_end),


    ],
    [

    #SB : start commander presentation
      ("start",[],"Companion Overview...",
       [
        # (assign, "$g_player_troop", "trp_player"),
        #clear troop's temp slots for presentation
        (try_for_range, ":stack_troop", active_npcs_including_player_begin, companions_end),
          (troop_set_slot, ":stack_troop", dplmc_slot_troop_temp_slot, 0),
        (try_end),
        (troop_set_slot, "trp_player", dplmc_slot_troop_temp_slot, 0),
        #assign first companion to be selected
        # (party_get_num_companion_stacks, ":end", "p_main_party"),
        # (try_for_range, ":stack_no", 1, ":end"),
          # (party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
          # (is_between, ":troop_no", companions_begin, companions_end),
          # (assign, "$g_player_troop", ":troop_no"),
          # (assign, ":end", -1),
        # (try_end),
        # (set_player_troop, "$g_player_troop"),

        #To do : add $supported_pretender and/or spouse in two placeholder troops before active_npcs
        (start_presentation, "prsnt_companion_overview"),
        ]
       ),

      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        #SB : fix globals
        (assign, "$g_player_troop", "trp_player"),
        (set_player_troop, "$g_player_troop"),
        ]
       ),
    ]
  )
]
