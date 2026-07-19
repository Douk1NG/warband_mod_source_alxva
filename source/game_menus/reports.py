# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

reports_menus = [
  ("reports",mnf_scale_picture|mnf_enable_hot_keys,
   "Character Renown: {reg5}^Honor Rating: {reg6}^Party Morale: {reg8}^Party Size Limit: {reg7}^",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (assign, reg5, ":renown"),
    (assign, reg6, "$player_honor"),
    (assign, reg7, ":party_size_limit"),
    #(call_script, "script_get_player_party_morale_values"),
    #(party_set_morale, "p_main_party", reg0),
    (party_get_morale, reg8, "p_main_party"),

    ##diplomacy begin
    (str_clear, s1),
    (try_begin),
	    (gt, "$g_next_pay_time", 0),
      (str_store_date, s1, "$g_next_pay_time"),
      (str_store_string, s1, "@ Next pay day: {s1}"),
    (try_end),

    (try_begin),
      (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
      (str_store_troop_name, s5, "$g_player_affiliated_troop"),
      (str_store_string, s1, "@{s1}^^Affiliated to {s5}"),
    (try_end),
    ##diplomacy end
   ],
    [
      ("reports_cheat",[(ge,"$cheat_mode",1)],"{!}Cheat Reports.",
       [(jump_to_menu, "mnu_cheat_reports"),
        ]
       ),

      ("action_view_world_map",[],"View the world map.",
       [
           (start_presentation, "prsnt_world_map"),
        ]
       ),

      ###(((reports_character
      ("reports_character",[],"View character/party reports.",
       [(jump_to_menu, "mnu_reports_character"),
        ]
       ),
      ###)))

      ###(((reports_faction
      ("reports_faction",[],"View faction/relations reports.",
       [(jump_to_menu, "mnu_reports_faction"),
        ]
       ),
      ###)))

      ###(((reports_economy
      ("reports_economy",[],"View economic reports.",
       [(jump_to_menu, "mnu_reports_economy"),
        ]
       ),
      ###)))

      ###(((all_items
      ("all_items",[],"View all items.",
        [
          (assign, "$temp", 0),
          (start_presentation, "prsnt_all_items"),
        ]),
      ###)))

      ("resume_travelling",[],"Resume travelling.",
       [(change_screen_return),
        ]
       ),
      ]
  ),
  ###(((reports_character,
  ("reports_character",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("view_character_report",[],"View character report.",
       [(jump_to_menu, "mnu_character_report"),
        ]
       ),
      ("view_party_size_report",[],"View party size report.",
       [(jump_to_menu, "mnu_party_size_report"),
        ]
       ),
      ("view_npc_mission_report",[],"View companion mission report.",
       [(jump_to_menu, "mnu_companion_report"),
        (assign, "$g_player_troop", "trp_player"),
        ]
       ),
      ("view_morale_report",[],"View party morale report.",
       [(jump_to_menu, "mnu_morale_report"),
        ]
       ),
      ("rtr_reports_character",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ###)))
  ###(((reports_faction,
  ("reports_faction",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("lord_relations",[],"View list of known lords by relation.",
       [
        (assign, "$g_jrider_pres_called_from_menu", 1),
        (assign, "$g_character_presentation_type", 1),
        (start_presentation, "prsnt_jrider_character_relation_report"),
        ]
       ),
      ("courtship_relations",[],"View courtship relations.",
       [
        (jump_to_menu, "mnu_courtship_relations"),
        ]
       ),
      ("view_affiliated_family_report",[
        (this_or_next|ge,"$cheat_mode",1),
        (is_between, "$g_player_affiliated_troop", kingdoms_begin, kingdoms_end),
        ], "View affiliated family member / spouse report.",
       [
        (jump_to_menu, "mnu_dplmc_affiliated_family_report"),
        ]
       ),
      ("view_faction_relations_report",[],"View faction relations report.",
       [
        (start_presentation, "prsnt_jrider_faction_relations_report"),
        ]
       ),
      ("rtr_reports_faction",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ###)))
  ###(((reports_economy,
  ("reports_economy",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("view_weekly_budget_report",[],"View weekly budget report.",
       [
        (assign, "$g_apply_budget_report_to_gold", 0),
        (start_presentation, "prsnt_budget_report"),
        ]
       ),
      ("view_bank_report",[],"View Financial Report",
       [(start_presentation, "prsnt_bank_quickview"),]),
      ("dplmc_show_economic_report",[],"View prosperity report.",
        [
         (jump_to_menu, "mnu_dplmc_economic_report"),
         ]
        ),
      ("view_spawn_diagnostics",[],"View bandit/pirate population & respawn diagnostics.",
        [
          (start_presentation, "prsnt_spawn_diagnostics"),
        ]
        ),
      ("rtr_reports_economy",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ###)))
  ###(((cheat_reports,
  ("cheat_reports",mnf_enable_hot_keys,
   "Select a cheat report:",
   "none",
   [],
    [
      ("cheat_faction_orders",[],"{!}Cheat: Faction orders.",
       [(jump_to_menu, "mnu_faction_orders"),
        ]
       ),

      ("status_check",[],"{!}NPC status check.",
       [
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, 4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),
            (display_message, "@{!}{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        ]
       ),

      ("rtr_cheat_reports",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ###))),
  ("morale_report",0,
   "{s1}",
   "none",
   [
     (call_script, "script_get_player_party_morale_values"),

     (assign, ":target_morale", reg0),
     (assign, reg1, "$g_player_party_morale_modifier_party_size"),
     (try_begin),
       (gt, reg1, 0),
       (str_store_string, s2, "@{!} -"),
     (else_try),
       (str_store_string, s2, "str_space"),
     (try_end),

     (assign, reg2, "$g_player_party_morale_modifier_leadership"),
     (try_begin),
       (gt, reg2, 0),
       (str_store_string, s3, "@{!} +"),
     (else_try),
       (str_store_string, s3, "str_space"),
     (try_end),

     (try_begin),
       (gt, "$g_player_party_morale_modifier_no_food", 0),
       (assign, reg7, "$g_player_party_morale_modifier_no_food"),
       (str_store_string, s5, "@^No food:  -{reg7}"),
     (else_try),
       (str_store_string, s5, "str_space"),
     (try_end),
     (assign, reg3, "$g_player_party_morale_modifier_food"),
     (try_begin),
       (gt, reg3, 0),
       (str_store_string, s4, "@{!} +"),
     (else_try),
       (str_store_string, s4, "str_space"),
     (try_end),

     (try_begin),
       (gt, "$g_player_party_morale_modifier_debt", 0),
       (assign, reg6, "$g_player_party_morale_modifier_debt"),
       (str_store_string, s6, "@^Wage debt:  -{reg6}"),
     (else_try),
       (str_store_string, s6, "str_space"),
     (try_end),

     (party_get_morale, reg5, "p_main_party"),
     (store_sub, reg4, reg5, ":target_morale"),
     (try_begin),
       (gt, reg4, 0),
       (str_store_string, s7, "@{!} +"),
     (else_try),
       (str_store_string, s7, "str_space"),
     (try_end),

     (assign, reg6, 50),

     (str_store_string, s1, "str_current_party_morale_is_reg5_current_party_morale_modifiers_are__base_morale__50_party_size_s2reg1_leadership_s3reg2_food_variety_s4reg3s5s6_recent_events_s7reg4_total__reg5___"),

     (try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
       (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
       (val_div, ":faction_morale", 100),
       (neq, ":faction_morale", 0),
       (assign, reg6, ":faction_morale"),
       (str_store_faction_name, s9, ":kingdom_no"),
       (str_store_string, s1, "str_s1extra_morale_for_s9_troops__reg6_"),
     (try_end),
    ],
    [
      ("continue",[],"Continue...",
      [
        (jump_to_menu, "mnu_reports"),
      ]),
    ]
  ),
  ("courtship_relations",0,
   "{s1}",
   "none",
   [(str_store_string, s1, "str_courtships_in_progress_"),
    (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
		(gt, reg0, 0),
		(assign, reg3, reg0),

		(str_store_troop_name, s2, ":lady"),

		(store_current_hours, ":hours_since_last_visit"),
		(troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
		(val_sub, ":hours_since_last_visit", ":last_visit_hour"),
		(store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
		(assign, reg4, ":days_since_last_visit"),

		(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
	(try_end),

	(str_store_string, s1, "str_s1__poems_known"),
	(try_begin),
		 (gt, "$allegoric_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
	(try_end),
	(try_begin),
		 (gt, "$tragic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
	(try_end),
	(try_begin),
		 (gt, "$comic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
	(try_end),
	(try_begin),
		 (gt, "$heroic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
	(try_end),
	(try_begin),
		 (gt, "$mystic_poem_recitations", 0),
		 (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
	(try_end),

    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ("lord_relations",0,
   "{s1}",
   "none",
   [
    ##diplomacy start+
	 #Avoid unnecessary iterations, since below we only use slto_kingdom_hero troops.
    (assign, ":met_lord_count", 0),
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
    (try_for_range, ":active_npc", heroes_begin, heroes_end),
      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
      (troop_slot_ge, ":active_npc", slot_troop_met, 1),
      (val_add, ":met_lord_count", 1),
    ##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
	(try_end),

	(str_clear, s1),
    ##diplomacy start+
    #Add support for promoted kingdom ladies.
    #(try_for_range, ":unused", active_npcs_begin, active_npcs_end),#<- changed
    #We counted the number of heroes, so we can cut down on the number of
    #iterations (since expanding this from active_npcs to heroes means that
    #a lot of them will not be lords).
    (try_for_range, ":unused", 0, ":met_lord_count"),#<- added
		(assign, ":score_to_beat", -100),
		(assign, ":best_relation_remaining_npc", -1),
		#Add support for promoted kingdom ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),#<-changed
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<-added
	##diplomacy end+
			(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_ge, ":active_npc", slot_troop_met, 1),

			(call_script, "script_troop_get_player_relation", ":active_npc"),
			(assign, ":relation_with_player", reg0),
			(ge, ":relation_with_player", ":score_to_beat"),

			(assign, ":score_to_beat", ":relation_with_player"),
			(assign, ":best_relation_remaining_npc", ":active_npc"),
		(try_end),
		(gt, ":best_relation_remaining_npc", -1),

		(str_store_troop_name_link, s4, ":best_relation_remaining_npc"),
		(assign, reg4, ":score_to_beat"),
		(str_store_string, s1, "@{!}{s1}^{s4}: {reg4}"),
		(troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),
	(try_end),


    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
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
  ),
  ("character_report",0,
   "{s9}",
   "none",
   [(try_begin),
      (gt, "$g_player_reading_book", 0),
      (player_has_item, "$g_player_reading_book"),
      (str_store_item_name, s8, "$g_player_reading_book"),
      (str_store_string, s9, "@You are currently reading {s8}."),
    (else_try),
      (assign, "$g_player_reading_book", 0),
      (str_store_string, s9, "@You are not reading any books."),
    (try_end),
    (assign, ":num_friends", 0),
    (assign, ":num_enemies", 0),
    (str_store_string, s6, "str_dplmc_none"),
    (str_store_string, s8, "str_dplmc_none"),
    (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
	  (call_script, "script_troop_get_player_relation", ":troop_no"),
      (assign, ":player_relation", reg0),
      #(troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
      (try_begin),
        (gt, ":player_relation", 20),
        (try_begin),
          (eq, ":num_friends", 0),
          (str_store_troop_name, s8, ":troop_no"),
        (else_try),
          (eq, ":num_friends", 1),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
        (val_add, ":num_friends", 1),
      (else_try),
        (lt, ":player_relation", -20),
        (try_begin),
          (eq, ":num_enemies", 0),
          (str_store_troop_name, s6, ":troop_no"),
        (else_try),
          (eq, ":num_enemies", 1),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{s5} and {s6}"),
        (else_try),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{!}{s5}, {s6}"),
        (try_end),
        (val_add, ":num_enemies", 1),
      (try_end),
    (try_end),

	#lord recruitment changes begin
	(str_clear, s12),
	(try_begin),
		(gt, "$player_right_to_rule", 0),
		(assign, reg12, "$player_right_to_rule"),
		(str_store_string, s12, "str__right_to_rule_reg12"),
	(try_end),

	#Sexual Stats
	#(troop_get_slot, reg21, "trp_player", slot_troop_encounters),
	#(troop_get_slot, reg22, "trp_player", slot_troop_assaults),
	#(str_store_string, s9, "@Encounters: {reg21}"),
	#(str_store_string, s9, "@Assaults: {reg22}"),

	(str_clear, s15),
	(try_begin),
		(this_or_next|gt, "$claim_arguments_made", 0),
		(this_or_next|gt, "$ruler_arguments_made", 0),
		(this_or_next|gt, "$victory_arguments_made", 0),
		(this_or_next|gt, "$lords_arguments_made", 0),
		(eq, 1, 0),

		(assign, reg3, "$claim_arguments_made"),
		(assign, reg4, "$ruler_arguments_made"),
		(assign, reg5, "$victory_arguments_made"),
		(assign, reg6, "$lords_arguments_made"),
		(assign, reg7, "$benefit_arguments_made"),

		(str_store_string, s15, "str_political_arguments_made_legality_reg3_rights_of_lords_reg4_unificationpeace_reg5_rights_of_commons_reg6_fief_pledges_reg7"),
	(try_end),

	#lord recruitment changes begin

    (assign, reg3, "$player_honor"),
    (troop_get_slot, reg2, "trp_player", slot_troop_renown),

    (str_store_string, s9, "str_renown_reg2_honour_rating_reg3s12_friends_s8_enemies_s6_s9"),

    (call_script, "script_get_number_of_hero_centers", "trp_player"),
    (assign, ":no_centers", reg0),
    (try_begin),
      (gt, ":no_centers", 0),
      (try_for_range, ":i_center", 0, ":no_centers"),
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),
        (try_begin),
          (eq, ":i_center", 0),
          (str_store_party_name, s8, ":cur_center"),
        (else_try),
          (eq, ":i_center", 1),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
      (try_end),
      (str_store_string, s9, "@Your estates are: {s8}.^{s9}"),
    (try_end),
    (try_begin),
      (gt, "$players_kingdom", 0),

      (str_store_faction_name, s8, "$players_kingdom"),
      (try_begin),
	  ##diplomacy start+ Handle player is co-ruler of NPC faction
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),
	  (else_try),
	  ##diplomacy end+
        (this_or_next|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        #(str_store_string, s9, "@You are a lord of {s8}.^{s9}"),
        (str_store_string, s9, "str_you_are_a_lord_lady_of_s8_s9"),
      (else_try),
        (str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),
      (try_end),

    (try_end),
    ],
    [

	#lord recruitment changes begin

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase Right to Rule",
       [
	   (val_add, "$player_right_to_rule", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),


	("continue",[(eq,"$cheat_mode",1),
		(str_store_troop_name, s14, "$g_talk_troop"),
	],"{!}CHEAT! - increase your relation with {s14}",
       [
	   (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("cheat_slots",[(eq,"$cheat_mode",1),
        (str_store_troop_name, s14, "$g_talk_troop"),
	],"{!}CHEAT! - Access {s14} troop slots",
       [
	   # (assign, "$g_talk_troop", "trp_player"),
	   (jump_to_menu, "mnu_display_troop_slots"),
       ]
       ),



	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase honor",
       [
	   (val_add, "$player_honor", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase renown",
       [
	   (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
	   (val_add, ":renown", 50),
	   (troop_set_slot, "trp_player", slot_troop_renown, ":renown"),

	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase persuasion",
       [
	   (troop_raise_skill, "trp_player", "skl_persuasion", 1),

	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),

	#lord recruitment changes end

	   ]
  ),
  ("party_size_report",0,
   "{s1}",
   "none",
   [(call_script, "script_game_get_party_companion_limit"),
    (assign, ":party_size_limit", reg0),

    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (val_mul, ":leadership", 5),
    (store_attribute_level, ":charisma", "trp_player", ca_charisma),

    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":renown", 25),
    (try_begin),
      (gt, ":leadership", 0),
      (str_store_string, s2, "@{!} +"),
    (else_try),
      (str_store_string, s2, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":charisma", 0),
      (str_store_string, s3, "@{!} +"),
    (else_try),
      (str_store_string, s3, "str_space"),
    (try_end),
    (try_begin),
      (gt, ":renown", 0),
      (str_store_string, s4, "@{!} +"),
    (else_try),
      (str_store_string, s4, "str_space"),
    (try_end),


    #SB : other modifiers from party_get_ideal_size, listed in order of precedence
    (try_for_range, ":sreg", s6, s10),
      (str_clear, ":sreg"),
    (try_end),

    (try_begin),
      (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
      # (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
      # the above script doesn't exactly work for pretender
      (try_begin),
        # (ge, reg0, DPLMC_FACTION_STANDING_LEADER), #exclude spouse
        (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
        (store_mul, ":king_bonus", 5, "$player_right_to_rule"), #20 is "legit" ruler
        (val_clamp, ":king_bonus", dplmc_marshal_party_bonus, dplmc_monarch_party_bonus + 1),
        (assign, reg6, ":king_bonus"),
        (str_store_string, s8, "@Monarch: +{reg6}^"),
      (else_try),
        (assign, ":king_bonus", 0),
      (try_end),

      (try_begin),
        (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
        (assign, ":marshal_bonus", dplmc_marshal_party_bonus),
        (assign, reg6, ":marshal_bonus"),
        (str_store_string, s7, "@Marshal: +{reg6}^"),
      (else_try),
        (assign, ":marshal_bonus", 0),
      (try_end),
      #percentage calculation follows
      (assign, ":faction_id", "$players_kingdom"),
      (assign, ":percent", 100),
      #Limit effects of policies for nascent kingdoms.
      (assign, ":policy_min", -3),
      (assign, ":policy_max", 4),#one greater than the maximum
      (try_begin),
          (this_or_next|eq, ":faction_id", "fac_player_supporters_faction"),
          (faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
          (faction_get_slot, ":policy_max", ":faction_id", slot_faction_num_towns),
          (faction_get_slot, reg0, ":faction_id", slot_faction_num_castles),
          (val_add, ":policy_max", reg0),
          (val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
          (store_mul, ":policy_min", ":policy_max", -1),
          (val_add, ":policy_max", 1),#one greater than the maximum
      (try_end),
      (try_begin), #we detecting rulership using king_bonus to determine which percent to apply
        (gt, ":king_bonus", 0),
        (try_begin),
          (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
          (val_clamp, ":centralization", ":policy_min", ":policy_max"),
          (val_mul, ":centralization", 10),
          (val_add, ":percent", ":centralization"),
        (try_end),
      (else_try), #player is a regular vassal
        (try_begin),
          (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
          (val_clamp, ":centralization", ":policy_min", ":policy_max"),
          (val_mul, ":centralization", -3),
          (val_add, ":percent", ":centralization"),
        (try_end),
        (try_begin),
          (faction_get_slot, ":aristocracy", ":faction_id", dplmc_slot_faction_aristocracy),
          (val_clamp, ":aristocracy", ":policy_min", ":policy_max"),
          (val_mul, ":aristocracy", 3),
          (val_add, ":percent", ":aristocracy"),
        (try_end),
        (try_begin),
          (faction_get_slot, ":quality", ":faction_id", dplmc_slot_faction_quality),
          (val_clamp, ":quality", ":policy_min", ":policy_max"),
          (val_mul, ":quality", -4),
          (val_add, ":percent", ":quality"),
        (try_end),
        ##diplomacy end
      (try_end),
      (try_begin),
        (faction_get_slot, ":serfdom", ":faction_id", dplmc_slot_faction_serfdom),
        (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
        (val_mul, ":serfdom", 2), #SB : no multiplier as per description
        (val_add, ":percent", ":serfdom"),
      (try_end),
      #if no change from default, do not display
      (try_begin),
        (eq, ":percent", 100),
        (assign, ":percent", 0),
      (else_try), #last new string
        (assign, reg6, ":percent"),
        (str_store_string, s9, "@Policy: {reg6}%^"),
      (try_end),
    (else_try), #not affiliated, do not show position-based bonus
      (assign, ":king_bonus", 0),
      (assign, ":marshal_bonus", 0),
      (assign, ":percent", 0),
    (try_end),
    ## CC
    (assign, ":center_bonus", 0),
    (try_for_range, ":cur_center", castles_begin, castles_end),
      (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
      (val_add, ":center_bonus", dplmc_castle_party_bonus),
    (try_end),
    (try_begin),
      (gt, ":center_bonus", 0),
      (assign, reg6, ":center_bonus"),
      (str_store_string, s6, "@Castellan: +{reg6}^"),
    (try_end),
    ## CC

    # (assign, reg9, ":percent"),
    # (assign, reg8, ":king_bonus"),
    # (assign, reg7, ":marshal_bonus"),
    # (assign, reg6, ":center_bonus"),
    (assign, reg5, ":party_size_limit"),
    (assign, reg1, ":leadership"),
    (assign, reg2, ":charisma"),
    (assign, reg3, ":renown"),
    #SB : might as well show player party size
    (party_get_num_companions, reg10, "p_main_party"),
    (str_store_string, s1, "@Current party size is {reg10}/{reg5}.^\
Current party size modifiers are:^^\
Base size:  +30^\
Leadership: {s2}{reg1}^\
Charisma: {s3}{reg2}^\
Renown: {s4}{reg3}^^\
{s8}{s7}{s6}{s9}\
TOTAL:  {reg5}"),
    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  ("faction_relations_report",0,
   "{s1}",
   "none",
   [(str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      (try_begin),
        (ge, ":cur_relation", 90),
        (str_store_string, s3, "@Loyal"),
      (else_try),
        (ge, ":cur_relation", 80),
        (str_store_string, s3, "@Devoted"),
      (else_try),
        (ge, ":cur_relation", 70),
        (str_store_string, s3, "@Fond"),
      (else_try),
        (ge, ":cur_relation", 60),
        (str_store_string, s3, "@Gracious"),
      (else_try),
        (ge, ":cur_relation", 50),
        (str_store_string, s3, "@Friendly"),
      (else_try),
        (ge, ":cur_relation", 40),
        (str_store_string, s3, "@Supportive"),
      (else_try),
        (ge, ":cur_relation", 30),
        (str_store_string, s3, "@Favorable"),
      (else_try),
        (ge, ":cur_relation", 20),
        (str_store_string, s3, "@Cooperative"),
      (else_try),
        (ge, ":cur_relation", 10),
        (str_store_string, s3, "@Accepting"),
      (else_try),
        (ge, ":cur_relation", 0),
        (str_store_string, s3, "@Indifferent"),
      (else_try),
        (ge, ":cur_relation", -10),
        (str_store_string, s3, "@Suspicious"),
      (else_try),
        (ge, ":cur_relation", -20),
        (str_store_string, s3, "@Grumbling"),
      (else_try),
        (ge, ":cur_relation", -30),
        (str_store_string, s3, "@Hostile"),
      (else_try),
        (ge, ":cur_relation", -40),
        (str_store_string, s3, "@Resentful"),
      (else_try),
        (ge, ":cur_relation", -50),
        (str_store_string, s3, "@Angry"),
      (else_try),
        (ge, ":cur_relation", -60),
        (str_store_string, s3, "@Hateful"),
      (else_try),
        (ge, ":cur_relation", -70),
        (str_store_string, s3, "@Revengeful"),
      (else_try),
        (str_store_string, s3, "@Vengeful"),
      (try_end),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (assign, reg1, ":cur_relation"),
      (str_store_string, s2, "@{!}{s2}^{s4}: {reg1} ({s3})"),
    (try_end),
    (str_store_string, s1, "@Your relation with the factions are:^{s2}"),



    ],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
  (
    "center_reports",0,
    "Town Name: {s1}^Rent Income: {reg1} denars^Tariff Income: {reg2} denars^Food Stock: for {reg3} days",
    "none",
    [(party_get_slot, ":town_food_store", "$g_encountered_party", slot_party_food_store),
     (call_script, "script_center_get_food_consumption", "$g_encountered_party"),
     (assign, ":food_consumption", reg0),
     (try_begin),
       (gt, ":food_consumption", 0),
       (store_div, reg3, ":town_food_store", ":food_consumption"),
     (else_try),
       (assign, reg3, 9999),
     (try_end),
     (str_store_party_name, s1, "$g_encountered_party"),
     (party_get_slot, reg1, "$g_encountered_party", slot_center_accumulated_rents),
     (party_get_slot, reg2, "$g_encountered_party", slot_center_accumulated_tariffs),
     ],
    [
      ("to_price_and_productions", [], "Show prices and productions.",
       [(jump_to_menu, "mnu_price_and_production"),
        ]),

      ("go_back_dot",[],"Go back.",
       [(try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (jump_to_menu, "mnu_village"),
        (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
  ),
  (
    "price_and_production",0,
    "Productions are:^(Note: base/modified by raw materials/modified by materials plus prosperity)^{s1}^^Price factors are:^{s2}",
    "none",
    [

	 (assign, ":calradian_average_urban_hardship", 0),
	 (assign, ":calradian_average_rural_hardship", 0),

	 (try_for_range, ":center", towns_begin, towns_end),
		(call_script, "script_center_get_goods_availability", ":center"),
		(val_add, ":calradian_average_urban_hardship", reg0),
	 (try_end),

	 (try_for_range, ":center", villages_begin, villages_end),
		(call_script, "script_center_get_goods_availability", ":center"),
		(val_add, ":calradian_average_rural_hardship", reg0),
	 (try_end),

	 (val_div, ":calradian_average_rural_hardship", 110),
	 (val_div, ":calradian_average_urban_hardship", 22),



	 (call_script, "script_center_get_goods_availability", "$g_encountered_party"),

	 (assign, reg1, ":calradian_average_urban_hardship"),
	 (assign, reg2, ":calradian_average_rural_hardship"),

	 (try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_string, s1, "str___hardship_index_reg0_avg_towns_reg1_avg_villages_reg2__"),
		(display_message, "@{!}DEBUG - {s1}"),
	 (try_end),


     (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	   (neq, ":cur_good", "itm_pork"), #tied to price of grain
	   (neq, ":cur_good", "itm_chicken"), #tied to price of grain
	   (neq, ":cur_good", "itm_butter"), #tied to price of cheese
	   (neq, ":cur_good", "itm_cattle_meat"),
	   (neq, ":cur_good", "itm_cabbages"), #possibly include later

	   (call_script, "script_center_get_production", "$g_encountered_party", ":cur_good"),
	   (assign, ":production", reg0),
	   (assign, ":base_production", reg2),
	   (assign, ":base_production_modded_by_raw_materials", reg1),

	   (call_script, "script_center_get_consumption", "$g_encountered_party", ":cur_good"),
	   (assign, ":consumer_consumption", reg2),
	   (assign, ":raw_material_consumption", reg1),
	   (assign, ":consumption", reg0),

       (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
       (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
       (party_get_slot, ":price", "$g_encountered_party", ":cur_good_price_slot"),

	   (assign, ":total_centers", 0),
	   (assign, ":calradian_average_price", 0),
	   (assign, ":calradian_average_production", 0),
	   (assign, ":calradian_average_consumption", 0),

	   (try_for_range, ":center", centers_begin, centers_end),
		(neg|is_between, ":center", castles_begin, castles_end),
	    (val_add, ":total_centers", 1),
        (call_script, "script_center_get_production", ":center", ":cur_good"),
		(assign, ":center_production", reg2),
        (call_script, "script_center_get_consumption", ":center", ":cur_good"),
		(store_add, ":center_consumption", reg1, reg2),

        (party_get_slot, ":center_price", ":center", ":cur_good_price_slot"),
	    (val_add, ":calradian_average_price", ":center_price"),
	    (val_add, ":calradian_average_production", ":center_production"),
	    (val_add, ":calradian_average_consumption", ":center_consumption"),
	   (try_end),

	   (assign, ":calradian_total_production", ":calradian_average_production"),
	   (assign, ":calradian_total_consumption", ":calradian_average_consumption"),

	   (val_div, ":calradian_average_price", ":total_centers"),
	   (val_div, ":calradian_average_production", ":total_centers"),
	   (val_div, ":calradian_average_consumption", ":total_centers"),


       (str_store_item_name, s3, ":cur_good"),

       (assign, reg1, ":base_production"),
       (assign, reg2, ":base_production_modded_by_raw_materials"),
       (assign, reg3, ":production"),
       (assign, reg4, ":price"),

	   (assign, reg5, ":calradian_average_production"),
	   (assign, reg6, ":calradian_average_price"),

	   (assign, reg7, ":consumer_consumption"),
	   (assign, reg8, ":raw_material_consumption"),
	   (assign, reg9, ":consumption"),

	   (assign, reg10, ":calradian_average_consumption"),

	   (item_get_slot, ":production_slot", ":cur_good", slot_item_production_slot),
	   (party_get_slot, ":production_number", "$g_encountered_party", ":production_slot"),
	   (assign, reg11, ":production_number"),
	   (assign, reg12, ":calradian_total_production"),
	   (assign, reg13, ":calradian_total_consumption"),

	   (item_get_slot, ":production_string", ":cur_good", slot_item_production_string),
	   (str_store_string, s4, ":production_string"),

       (str_store_string, s1, "str___s3_price_=_reg4_calradian_average_reg6_capital_reg11_s4_base_reg1modified_by_raw_material_reg2modified_by_prosperity_reg3_calradian_average_production_base_reg5_total_reg12_consumed_reg7used_as_raw_material_reg8modified_total_reg9_calradian_consumption_base_reg10_total_reg13s1_"),
     (try_end),


     ],
    [
      ("go_back_dot",[],"Go back.",
       [(try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (jump_to_menu, "mnu_village"),
        (else_try),
          (jump_to_menu, "mnu_town"),
        (try_end),
        ]),
    ]
  ),
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
  ),
  ("dplmc_economic_report",0,
   "{s0}",
   "none",
   [
    (str_clear, s0),
    (str_clear, s1),
    (assign, reg0, 0),
    (str_store_string, s0, "@Prosperity Report^"),

    #Show average prosperity for each faction
    (try_for_range, ":faction", 0, kingdoms_end),
       (this_or_next|eq, ":faction", 0),
       (is_between, ":faction", kingdoms_begin, kingdoms_end),

       (this_or_next|eq, ":faction", 0),
       (faction_slot_eq, ":faction", slot_faction_state, sfs_active),

       (try_begin),
          (eq, ":faction", 0),
          (str_store_string, s1, "@Total"),
       (else_try),
          (faction_get_slot, reg0, ":faction", slot_faction_adjective),
          (gt, reg0, 0),
          (str_store_string, s1, reg0),
       (else_try),
          (str_store_faction_name, s1, ":faction"),
       (try_end),

       ##(1) Faction Prosperity, towns
       (assign, ":sum", 0),
       (assign, ":q_5", 0),
       (assign, ":q_4", 0),
       (assign, ":q_3", 0),
       (assign, ":q_2", 0),
       (assign, ":q_1", 0),
       (assign, ":num", 0),

       (try_for_range, ":center_no", towns_begin, towns_end),
          (store_faction_of_party, reg0, ":center_no"),
          (this_or_next|eq, ":faction", 0),
          (eq, reg0, ":faction"),
          (val_add, ":num", 1),
          (party_get_slot, reg0, ":center_no", slot_town_prosperity),
          (val_add, ":sum", reg0),
          (try_begin),
             (lt, reg0, 20),
             (val_add, ":q_1", 1),
          (else_try),
             (lt, reg0, 40),
             (val_add, ":q_2", 1),
          (else_try),
             (lt, reg0, 60),
             (val_add, ":q_3", 1),
          (else_try),
             (lt, reg0, 80),
             (val_add, ":q_4", 1),
          (else_try),
             (val_add, ":q_5", 1),
          (try_end),
       (try_end),

       (assign, reg0, ":num"),
       (val_max, reg0, 1),
       (store_div, reg0, ":sum", reg0),
       (str_store_string, s0, "@{s0}^{s1} Average Town Prosperity: {reg0}"),
       (assign, reg0, ":q_5"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 80-100: {reg0}"),
       (try_end),
       (assign, reg0, ":q_4"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 60-79: {reg0}"),
       (try_end),
       (assign, reg0, ":q_3"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 40-59: {reg0}"),
       (try_end),
       (assign, reg0, ":q_2"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 20-39: {reg0}"),
       (try_end),
       (assign, reg0, ":q_1"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, reg0, 0),
          (str_store_string, s0, "@{s0}^{s1} towns with prosperity 0-19: {reg0}"),
       (try_end),

       (str_store_string, s0, "@{!}{s0}^"),

       ##(2) Faction Prosperity, villages
       (assign, ":sum", 0),
       (assign, ":q_5", 0),
       (assign, ":q_4", 0),
       (assign, ":q_3", 0),
       (assign, ":q_2", 0),
       (assign, ":q_1", 0),
       (assign, ":num", 0),

       (try_for_range, ":center_no", villages_begin, villages_end),
          (store_faction_of_party, reg0, ":center_no"),
          (this_or_next|eq, ":faction", 0),
          (eq, reg0, ":faction"),
          (val_add, ":num", 1),
          (party_get_slot, reg0, ":center_no", slot_town_prosperity),
          (val_add, ":sum", reg0),
          (try_begin),
             (lt, reg0, 20),
             (val_add, ":q_1", 1),
          (else_try),
             (lt, reg0, 40),
             (val_add, ":q_2", 1),
          (else_try),
             (lt, reg0, 60),
             (val_add, ":q_3", 1),
          (else_try),
             (lt, reg0, 80),
             (val_add, ":q_4", 1),
          (else_try),
             (val_add, ":q_5", 1),
          (try_end),
       (try_end),

       (assign, reg0, ":num"),
       (val_max, reg0, 1),
       (store_div, reg0, ":sum", reg0),
       (str_store_string, s0, "@{s0}^{s1} Average Village Prosperity: {reg0}"),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_5", 0),
          (assign, reg0, ":q_5"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 80-100: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_4", 0),
          (assign, reg0, ":q_4"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 60-79: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_3", 0),
          (assign, reg0, ":q_3"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 40-59: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_2", 0),
          (assign, reg0, ":q_2"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 20-39: {reg0}"),
       (try_end),
       (try_begin),
          (this_or_next|eq, ":faction", 0),
          (gt, ":q_1", 0),
          (assign, reg0, ":q_1"),
          (str_store_string, s0, "@{s0}^{s1} villages with prosperity 0-19: {reg0}"),
       (try_end),
       (str_store_string, s0, "@{!}{s0}^"),
    (try_end),
    ],
    [
      ("dplmc_back",[],"Continue...",
       [
           (jump_to_menu, "mnu_reports"),
        ]),
      ]
  ),

  # Debug helper kept for fallen ruler / pretender recruitment investigations.
  # ("dplmc_fallen_ruler_debug_report",0,
  #  "{s0}",
  #  "none",
  #  [
  #   (str_store_string, s0, "@Fallen Ruler Debug Report^recruitable=1 means the fallen-ruler recruitment rule currently passes.^^"),
  #   (assign, ":found_any", 0),
  #   (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
  #     (this_or_next|is_between, ":troop_no", kings_begin, kings_end),
  #       (is_between, ":troop_no", pretenders_begin, pretenders_end),
  #     (troop_get_slot, ":original_faction", ":troop_no", slot_troop_original_faction),
  #     (is_between, ":original_faction", npc_kingdoms_begin, npc_kingdoms_end),
  #     (assign, ":found_any", 1),
  #
  #     (str_store_troop_name, s11, ":troop_no"),
  #     (store_faction_of_troop, ":current_faction", ":troop_no"),
  #     (str_store_faction_name, s12, ":current_faction"),
  #     (str_store_faction_name, s13, ":original_faction"),
  #     (faction_get_slot, reg10, ":original_faction", slot_faction_state),
  #     (faction_get_slot, ":original_faction_leader", ":original_faction", slot_faction_leader),
  #     (str_store_troop_name, s14, ":original_faction_leader"),
  #     (troop_get_slot, reg12, ":troop_no", slot_troop_occupation),
  #     (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
  #     (try_begin),
  #       (ge, ":prisoner_party", 0),
  #       (str_store_party_name, s15, ":prisoner_party"),
  #     (else_try),
  #       (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
  #       (is_between, ":cur_center", centers_begin, centers_end),
  #       (str_store_party_name, s15, ":cur_center"),
  #     (else_try),
  #       (str_store_string, s15, "@nowhere recorded"),
  #     (try_end),
  #
  #     (assign, reg14, 0),
  #     (assign, ":valid_fallen_faction", 0),
  #     (try_begin),
  #       (eq, ":current_faction", "fac_commoners"),
  #       (assign, ":valid_fallen_faction", 1),
  #     (else_try),
  #       (eq, ":current_faction", ":original_faction"),
  #       (faction_slot_eq, ":original_faction", slot_faction_state, sfs_defeated),
  #       (assign, ":valid_fallen_faction", 1),
  #     (try_end),
  #     (try_begin),
  #       (eq, ":valid_fallen_faction", 1),
  #       (this_or_next|neq, ":original_faction_leader", ":troop_no"),
  #         (faction_slot_eq, ":original_faction", slot_faction_state, sfs_defeated),
  #       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
  #       (assign, reg14, 1),
  #     (try_end),
  #
  #     (str_store_string, s1, "@{s11}: current={s12}; original={s13}; original_state={reg10}; original_leader={s14}; occupation={reg12}; location_or_prison={s15}; recruitable={reg14}."),
  #     (str_store_string, s0, "@{s0}^{s1}"),
  #   (try_end),
  #   (try_begin),
  #     (eq, ":found_any", 0),
  #     (str_store_string, s0, "@{s0}No kings or pretenders with an NPC original faction were found."),
  #   (try_end),
  #   ],
  #   [
  #     ("dplmc_back",[],"Continue...",
  #      [
  #          (jump_to_menu, "mnu_reports"),
  #       ]),
  #     ]
  # ),
##diplomacy end+

#SB : secondary cheat menu,
]
