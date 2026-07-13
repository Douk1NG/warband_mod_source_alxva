# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

####################################################################################################################
# FACTION AI & POLITICS SCRIPTS
# 
# This file governs kingdom-level decisions: declaring war, making peace, electing marshals,
# issuing faction policies, and evaluating realm stability or rebellion chances.
####################################################################################################################

faction_ai_scripts = [
  # This script is called from the game engine
  # Input:
  # param1: faction_no,
  # Output: reg0: extra morale x 100

  ("game_get_morale_of_troops_from_faction",
    [
      (store_script_param_1, ":troop_no"),

      (store_troop_faction, ":faction_no", ":troop_no"),

      (try_begin),
        (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),

        (faction_get_slot, reg0, ":faction_no",  slot_faction_morale_of_player_troops),

        #(assign, reg1, ":faction_no"),
        #(assign, reg2, ":troop_no"),
        #(assign, reg3, reg0),
        #(display_message, "@extra morale for troop {reg2} of faction {reg1} is {reg3}"),
      (else_try),
        (assign, reg0, 0),
      (try_end),
      ##diplomacy start+
      #If there is no current morale penalty, then there will be a minor morale bonus
		#if the player has his own faction and his culture matches the source kingdom.
		(try_begin),
		   (eq, reg0, 0),
			(is_between,"$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
			(eq, "$g_player_culture", ":faction_no"),
			#xxx TODO: pick a number less arbitrarily
			(assign, reg0, 100),
		(try_end),
      ##diplomacy end+
      (val_div, reg0, 100),

      (party_get_morale, reg1, "p_main_party"),

      (val_add, reg0, reg1),

      (set_trigger_result, reg0),
  ]),

  #script_game_event_detect_party:
  # This script is called from the game engine when the notes of a faction is needed.
  # INPUT: arg1 = faction_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_faction_note",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":note_index"),
      (set_trigger_result, 0),

##      (try_begin),
##        (eq, 2, 1),
##        (str_store_faction_name, s14, ":faction_no"),
##        (assign, reg4, "$temp"),
##        (display_message, "str_updating_faction_notes_for_s14_temp_=_reg4"),
##      (try_end),

      (try_begin),
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        #conditions end
        (try_begin),
            (eq, ":note_index", 0),
          (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
          (str_store_faction_name, s5, ":faction_no"),
          ##diplomacy start+
          ##OLD:
          #(str_store_troop_name_link, s6, ":faction_leader"),
          ##NEW:
          (try_begin),
             (lt, ":faction_leader", 0),
             #(le, ":faction_leader", 0),
             #(this_or_next|lt, ":faction_leader", 0),
             #   (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
             (str_store_string, s6, "str_noone"),
          (else_try),
             (eq, ":faction_leader", "trp_kingdom_heroes_including_player_begin"),
             (assign, ":faction_leader", "trp_player"),
          (str_store_troop_name_link, s6, ":faction_leader"),
          (else_try),
             (str_store_troop_name_link, s6, ":faction_leader"),
          (try_end),
			 ##diplomacy end+
          (assign, ":num_centers", 0),
          (str_store_string, s8, "@nowhere"),
          (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
            (store_faction_of_party, ":center_faction", ":cur_center"),
            (eq, ":center_faction", ":faction_no"),
            (try_begin),
              (eq, ":num_centers", 0),
              (str_store_party_name_link, s8, ":cur_center"),
            (else_try),
              (eq, ":num_centers", 1),
              (str_store_party_name_link, s7, ":cur_center"),
              (str_store_string, s8, "@{s7} and {s8}"),
            (else_try),
              (str_store_party_name_link, s7, ":cur_center"),
              (str_store_string, s8, "@{!}{s7}, {s8}"),
            (try_end),
            (val_add, ":num_centers", 1),
          (try_end),
          (assign, ":num_members", 0),
          (str_store_string, s10, "@noone"),
          ##diplomacy start+ support for promoted kingdom ladies
          (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", heroes_end),#<- changed active_npcs_end to heroes_end
          ##diplomacy end+
            (assign, ":cur_troop", ":loop_var"),
            (try_begin),
              (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
              (assign, ":cur_troop", "trp_player"),
              (assign, ":troop_faction", "$players_kingdom"),
            (else_try),
              (store_troop_faction, ":troop_faction", ":cur_troop"),
            (try_end),
            (eq, ":troop_faction", ":faction_no"),
            (neq, ":cur_troop", ":faction_leader"),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (try_begin),
              (eq, ":num_members", 0),
              (str_store_troop_name_link, s10, ":cur_troop"),
            (else_try),
              (eq, ":num_members", 1),
              (str_store_troop_name_link, s9, ":cur_troop"),
              (str_store_string, s10, "@{s9} and {s10}"),
            (else_try),
              (str_store_troop_name_link, s9, ":cur_troop"),
              (str_store_string, s10, "@{!}{s9}, {s10}"),
            (try_end),
            (val_add, ":num_members", 1),
          (try_end),

              #wars
          (str_store_string, s12, "@noone"),
   #       (assign, ":num_enemies", 0),
   #       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
   #         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
   #         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
   #         (lt, ":cur_relation", 0),
   #         (try_begin),
   #           (eq, ":num_enemies", 0),
   #           (str_store_faction_name_link, s12, ":cur_faction"),
   #         (else_try),
   #           (eq, ":num_enemies", 1),
   #           (str_store_faction_name_link, s11, ":cur_faction"),
   #           (str_store_string, s12, "@the {s11} and the {s12}"),
   #         (else_try),
   #           (str_store_faction_name_link, s11, ":cur_faction"),
   #           (str_store_string, s12, "@the {s11}, the {s12}"),
   #         (try_end),
   #         (val_add, ":num_enemies", 1),
        #       (try_end),


        ##SB : add domestic policy as overview
        (str_clear, s21),
        (str_clear, s20),
        (try_begin),
            (eq, ":faction_no", "$players_kingdom"),
            (str_store_string, s20, "@Domestic policy: ^^"),
            (call_script, "script_display_policy_string_to_reg", ":faction_no", 0, 1),
        (try_end),
        (str_store_string, s21, "str_foreign_relations__"),

              #other foreign relations
          (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
            (neq, ":faction_no", ":cur_faction"),
            (str_store_faction_name_link, s14, ":cur_faction"),
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_no", ":cur_faction"),
            (assign, ":diplomatic_status", reg0),
            (assign, ":duration_of_status", reg1),

            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":faction_no"),
            (assign, ":reverse_diplomatic_status", reg0),
            (try_begin),
              (eq, ":diplomatic_status", -2),
              (str_store_string, s21, "str_s21__the_s5_is_at_war_with_the_s14"),
              (store_add, ":slot_war_damage_inflicted", ":cur_faction", slot_faction_war_damage_inflicted_on_factions_begin),
              (val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
              (faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot_war_damage_inflicted"),
              (store_mul, ":war_damage_inflicted_x_2", ":war_damage_inflicted", 2),

              (store_add, ":slot_war_damage_suffered", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
              (val_sub, ":slot_war_damage_suffered", kingdoms_begin),
              (faction_get_slot, ":war_damage_suffered", ":cur_faction", ":slot_war_damage_suffered"),
              (store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),


			  (assign, ":war_cause", 0),
			  (assign, ":attacker", 0),
			  (try_for_range, ":log_entry", 0, "$num_log_entries"),
				(troop_get_slot, ":type", "trp_log_array_entry_type", ":log_entry"),
				(is_between, ":type", logent_faction_declares_war_out_of_personal_enmity, logent_war_declaration_types_end),
				(troop_get_slot, ":actor", "trp_log_array_actor", ":log_entry"),
				(troop_get_slot, ":object", "trp_log_array_faction_object", ":log_entry"),

				(try_begin),
					(eq, ":actor", ":cur_faction"),
					(eq, ":object", ":faction_no"),
					(assign, ":war_cause", ":type"),
					(assign, ":attacker", ":actor"),
				(else_try),
					(eq, ":actor", ":faction_no"),
					(eq, ":object", ":cur_faction"),
					(assign, ":war_cause", ":type"),
					(assign, ":attacker", ":actor"),
				(try_end),
			  (try_end),

			  #bug fix! backing up s8 to somewhere else
                          (str_store_string, s25, s8),
			  (try_begin),
			    (gt, ":war_cause", 0),
				(str_store_faction_name, s8, ":attacker"),
				(try_begin),
					(eq, ":war_cause", logent_faction_declares_war_out_of_personal_enmity),
					(str_store_string, s21, "str_s21_the_s8_declared_war_out_of_personal_enmity"),
				(else_try),
					(eq, ":war_cause", logent_faction_declares_war_to_respond_to_provocation),
					(str_store_string, s21, "str_s21_the_s8_declared_war_in_response_to_border_provocations"),
				(else_try),
					(eq, ":war_cause", logent_faction_declares_war_to_curb_power),
					(str_store_string, s21, "str_s21_the_s8_declared_war_to_curb_the_other_realms_power"),
				(else_try),
					(eq, ":war_cause", logent_faction_declares_war_to_regain_territory),
					(str_store_string, s21, "str_s21_the_s8_declared_war_to_regain_lost_territory"),
				##diplomacy begin
				(else_try),
					(eq, ":war_cause", logent_faction_declares_war_to_fulfil_pact),
					(str_store_string, s21, "str_dplmc_s21_the_s8_declared_war_to_fulfil_pact"),
				##diplomacy end
				(else_try),
					(eq, ":war_cause", logent_player_faction_declares_war),
					(neq, ":attacker", "fac_player_supporters_faction"),
					(str_store_string, s21, "str_s21_the_s8_declared_war_as_part_of_a_bid_to_conquer_all_calradia"),
				(try_end),
			  (try_end),
			  #bug fix! restoring the back up to s8
              (str_store_string, s8, s25),

              (try_begin),
                (gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),
                (str_store_string, s21, "str_s21_the_s5_has_had_the_upper_hand_in_the_fighting"),
              (else_try),
                (gt, ":war_damage_suffered", ":war_damage_inflicted_x_2"),
                (str_store_string, s21, "str_s21_the_s5_has_gotten_the_worst_of_the_fighting"),
              (else_try),
                (gt, ":war_damage_inflicted", 100),
                (gt, ":war_damage_inflicted", 100),
                (str_store_string, s21, "str_s21_the_fighting_has_gone_on_for_some_time_and_the_war_may_end_soon_with_a_truce"),
              (else_try),
                (str_store_string, s21, "str_s21_the_fighting_has_begun_relatively_recently_and_the_war_may_continue_for_some_time"),
              (try_end),
              (try_begin),
                (eq, "$cheat_mode", 1),
                (assign, reg4, ":war_damage_inflicted"),
                (assign, reg5, ":war_damage_suffered"),
                (str_store_string, s21, "str_s21_reg4reg5"),
              (try_end),
            (else_try),
              (eq, ":diplomatic_status", 1),
              (str_clear, s18),
              (try_begin),
                (neq, ":reverse_diplomatic_status", 1),
                (str_store_string, s18, "str__however_the_truce_is_no_longer_binding_on_the_s14"),
              (try_end),
			  (assign, reg1, ":duration_of_status"),
			  ##diplomacy begin
              (try_begin),
			    ##nested diplomacy start+ Use named variables for truce lengths
                #(is_between, ":duration_of_status", 1, 21),
				(is_between, ":duration_of_status", dplmc_treaty_truce_days_expire + 1, dplmc_treaty_truce_days_initial + 1),
				##nested diplomacy end+
              ##diplomacy end
              (str_store_string, s21, "str_s21__the_s5_is_bound_by_truce_not_to_attack_the_s14s18_the_truce_will_expire_in_reg1_days"),
              ##diplomacy begin
			  ##nested diplomacy start+ Use named variables for truce lengths
              (else_try),
                #(is_between, ":duration_of_status", 21, 41),
                #(val_sub, reg1, 20),
                (is_between, ":duration_of_status", dplmc_treaty_trade_days_expire + 1, dplmc_treaty_trade_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_trade_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_trade_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (else_try),
                #(is_between, ":duration_of_status", 41, 61),
                #(val_sub, reg1, 40),
                (is_between, ":duration_of_status", dplmc_treaty_defense_days_expire + 1, dplmc_treaty_defense_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_defense_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_defensive_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (else_try),
                #(is_between, ":duration_of_status", 61, 81),
                #(val_sub, reg1, 60),
                (is_between, ":duration_of_status", dplmc_treaty_alliance_days_expire + 1, dplmc_treaty_alliance_days_initial + 1),
                (val_sub, reg1, dplmc_treaty_alliance_days_expire),
                (str_store_string, s21, "str_dplmc_s21__the_s5_is_bound_by_alliance_not_to_attack_the_s14s18_it_will_expire_in_reg1_days"),
              (try_end),
			  ##nested diplomacy end+ (Use named variables for truce lengths)
               ##diplomacy end
            (else_try),
              (eq, ":diplomatic_status", -1),
              (str_store_string, s21, "str_s21__the_s5_has_recently_suffered_provocation_by_subjects_of_the_s14_and_there_is_a_risk_of_war"),
            (else_try),
              (eq, ":diplomatic_status", 0),
              (str_store_string, s21, "str_s21__the_s5_has_no_outstanding_issues_with_the_s14"),
            (try_end),
            (try_begin),
              (eq, ":reverse_diplomatic_status", -1),
              (str_store_string, s21, "str_s21_the_s14_was_recently_provoked_by_subjects_of_the_s5_and_there_is_a_risk_of_war_"),
            (try_end),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (call_script, "script_npc_decision_checklist_peace_or_war", ":faction_no", ":cur_faction", -1),
			  (str_store_string, s21, "@{!}DEBUG : {s21}.^CHEAT MODE ASSESSMENT: {s14}^"),
            (try_end),
          (try_end),
          (str_store_string, s0, "str_the_s5_is_ruled_by_s6_it_occupies_s8_its_vassals_are_s10__s21", 0),
          (set_trigger_result, 1),
        (try_end),
      (else_try),
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
        (try_begin),
          (eq, ":note_index", 0),
          (str_store_faction_name, s5, ":faction_no"),
          (str_store_string, s0, "@{s5} has been defeated!", 0),
          (set_trigger_result, 1),
        (else_try),
          (eq, ":note_index", 1),
          (str_clear, s0),
          (set_trigger_result, 1),
        (try_end),
      (else_try),
        (try_begin),
          (this_or_next|eq, ":note_index", 0),
          (eq, ":note_index", 1),
          (str_clear, s0),
          (set_trigger_result, 1),
        (try_end),
      (try_end),
     ]),

  #script_game_get_quest_note
("initialize_faction_troop_types",
    [

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_get_slot, ":culture", ":faction_no", slot_faction_culture),

        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_1_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_1_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_2_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_2_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_3_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_3_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_4_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_4_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_5_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_5_troop, ":troop"),

        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_1"),

          (faction_set_slot, ":faction_no",  slot_faction_deserter_troop, "trp_swadian_deserter"),
          (faction_set_slot, ":faction_no",  slot_faction_guard_troop, "trp_swadian_sergeant"),
          (faction_set_slot, ":faction_no",  slot_faction_messenger_troop, "trp_swadian_messenger"),
          (faction_set_slot, ":faction_no",  slot_faction_prison_guard_troop, "trp_swadian_prison_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_castle_guard_troop, "trp_swadian_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_1_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_1_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_1_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_2"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_vaegir_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_vaegir_guard"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_vaegir_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_vaegir_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_vaegir_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_2_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_2_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_2_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_3"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_khergit_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_khergit_horseman"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_khergit_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_khergit_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_khergit_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_3_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_3_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_3_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_4"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_nord_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_nord_warrior"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_nord_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_nord_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_nord_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_4_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_4_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_4_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_5"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_rhodok_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_rhodok_veteran_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_rhodok_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_rhodok_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_rhodok_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_5_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_5_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_5_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_6"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_sarranid_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_sarranid_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_sarranid_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_sarranid_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_sarranid_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_6_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_6_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_6_reinforcements_c"),
        (try_end),
      (try_end),
	]),

      # counts number of active parties with a template and faction.
  # Input: arg1 = faction_no, arg2 = party_type
  # Output: reg0 = count

  ("count_parties_of_faction_and_party_type",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),
      (assign, reg0, 0),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
        (store_faction_of_party, ":cur_faction", ":party_no"),
        (eq, ":cur_party_type", ":party_type"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, reg0, 1),
      (try_end),
  ]),

# script_faction_get_number_of_armies
# Input: arg1 = faction_no
# Output: reg0 = number_of_armies
  ("faction_get_number_of_armies",
   [
      (store_script_param_1, ":faction_no"),
      (assign, ":num_armies", 0),
      ##diplomacy start+ support for promoted kingdom ladies
      (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- changed from active_npcs to heroes
      ##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
    	(store_troop_faction, ":hero_faction_no", ":troop_no"),
        (eq, ":hero_faction_no", ":faction_no"),
        (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
        (ge, ":hero_party", 0),
        (party_is_active, ":hero_party"),
        (call_script, "script_party_count_fit_regulars", ":hero_party"),
        (assign, ":party_size", reg0),
        (call_script, "script_party_get_ideal_size", ":hero_party"),
        (assign, ":ideal_size", reg0),
        (val_mul, ":ideal_size", 60),
        (val_div, ":ideal_size", 100),
        (gt, ":party_size", ":ideal_size"),
        (val_add, ":num_armies", 1),
      (try_end),
      (assign, reg0, ":num_armies"),
    ]),


# script_faction_recalculate_strength
# Input: arg1 = faction_no
# Output: reg0 = strength
  ("faction_recalculate_strength",
   [
      (store_script_param_1, ":faction_no"),

      (call_script, "script_faction_get_number_of_armies", ":faction_no"),
      (assign, ":num_armies", reg0),
      (assign, ":num_castles", 0),
      (assign, ":num_towns", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (eq, ":center_faction", ":faction_no"),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_castle),
          (val_add, ":num_castles", 1),
        (else_try),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_add, ":num_towns", 1),
        (try_end),
      (try_end),

      (faction_set_slot, ":faction_no", slot_faction_num_armies, ":num_armies"),
      (faction_set_slot, ":faction_no", slot_faction_num_castles, ":num_castles"),
      (faction_set_slot, ":faction_no", slot_faction_num_towns, ":num_towns"),

    ]),

  #script_select_random_town:
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_enemy_faction",
    [
      (store_script_param_1, ":faction_no"),

      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (le, ":cur_relation", -1),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),

      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_cf_faction_get_random_friendly_faction
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (Can fail)
  ("cf_faction_get_random_friendly_faction",
    [
      (store_script_param_1, ":faction_no"),

      (assign, ":result", -1),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
      (try_end),
      (store_random_in_range,":random_faction",0,":count_factions"),
      (assign, ":count_factions", 0),
      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (eq, ":result", -1),
        (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        (neq, ":cur_faction", ":faction_no"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (ge, ":cur_relation", 0),
        (val_add, ":count_factions", 1),
        (gt, ":count_factions", ":random_faction"),
        (assign, ":result", ":cur_faction"),
      (try_end),

      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_cf_troop_get_random_enemy_troop_with_occupation
  # Input: arg1 = troop_no, arg2 = faction
  ("change_troop_faction",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        #Reactivating inactive or defeated faction
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_set_slot, ":faction_no", slot_faction_state, sfs_active),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),

	  #Political ramifications
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),
	  ##diplomacy start+ save these for reference
	  #(faction_get_slot, ":orig_faction_leader", ":orig_faction", slot_faction_leader),
	  (faction_get_slot, ":new_faction_leader", ":faction_no", slot_faction_leader),
	  (try_begin),
		  #Avoid letting heroes get stuck as slto_inactive if petitioners switch away from the player's faction
		  (eq, ":orig_faction", "fac_player_supporters_faction"),
	     (gt, ":troop_no", 0),
	     (troop_is_hero, ":troop_no"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
		  (this_or_next|is_between, ":troop_no", lords_begin, lords_end),
		  (this_or_next|is_between, ":troop_no", kings_begin, kings_end),
		  (this_or_next|is_between, ":troop_no", pretenders_begin, pretenders_end),
		  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
		     (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (try_end),
	  ##diplomacy end+

	  #remove if he is marshal
	  (try_begin),
		(faction_slot_eq, ":orig_faction", slot_faction_marshall, ":troop_no"),
        (call_script, "script_check_and_finish_active_army_quests_for_faction", ":orig_faction"),

		#No current issue on the agenda
		(try_begin),
			(faction_slot_eq, ":orig_faction", slot_faction_political_issue, 0),

			(faction_set_slot, ":orig_faction", slot_faction_political_issue, 1), #Appointment of marshal
			(store_current_hours, ":hours"),
			(val_max, ":hours", 0),
			(faction_set_slot, ":orig_faction", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
			##diplomacy start+ Reset political stance for kingdom ladies as well
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),##OLD
			(try_for_range, ":active_npc", heroes_begin, heroes_end),##NEW
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":orig_faction"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":orig_faction"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
		(try_end),

        (try_begin),
		  (troop_get_slot, ":old_marshall_party", ":troop_no", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshal, ":old_marshall_party", 0),
        (try_end),

		(faction_set_slot, ":orig_faction", slot_faction_marshall, -1),
	  (try_end),
	  #Removal as marshal ends

	  #Other political ramifications
	  (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
	  ##diplomacy start+ Support promoted kingdom ladies
	  #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":active_npc", heroes_begin, heroes_end),
	  ##diplomacy end+
		(troop_slot_eq, ":active_npc", slot_troop_stance_on_faction_issue, ":troop_no"),
		(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	  (try_end),
	  #Political ramifications end


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in normal faction change"),
		(try_end),

      (troop_set_faction, ":troop_no", ":faction_no"),
	  ##diplomacy start+
	  ##Don't give lords amnesia about what the player said to recruit them.
	  ##OLD:
      #(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
      #(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
      #(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  ##NEW
	  (try_begin),
		 (eq, ":troop_no", "trp_player"),
		 #Don't change of this for the player.
	  (else_try),
	    (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
			(eq, ":faction_no", "$players_kingdom"),
		 (ge, ":new_faction_leader", 0),
		 (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
		 (this_or_next|eq, ":new_faction_leader", "trp_player"),
		 (this_or_next|troop_slot_eq, ":new_faction_leader", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":new_faction_leader"),
		 #Joined faction that player is ruler or co-ruler of.  Don't forget
		 #any promises received.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
	  (else_try),
	     #Joined a new faction.  Previous promises moot.
		 (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
		 (troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
		 (troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
	  (try_end),
	  ##diplomacy end+

      #Give new title
      # (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"), moved down

      (try_begin),
        (this_or_next|eq, ":faction_no", "$players_kingdom"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_check_concilio_calradi_achievement"),
      (try_end),

	  #Takes walled centers and dependent villages with him
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_set_faction, ":center_no", ":faction_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (party_set_faction, ":village_no", ":faction_no"),
          (party_get_slot, ":farmer_party_no", ":village_no", slot_village_farmer_party),
          (try_begin),
            (gt, ":farmer_party_no", 0),
            (party_is_active, ":farmer_party_no"),
            (party_set_faction, ":farmer_party_no", ":faction_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":old_town_lord", ":village_no", slot_town_lord),
            (neq, ":old_town_lord", ":troop_no"),
            (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
            ##diplomacy start+ Invalidate old lord's cached center points
            (gt, ":old_town_lord", -1),
            (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
            ##diplomacy end+
          (try_end),
        (try_end),
      (try_end),

	  #Dependant kingdom ladies switch faction
	  (try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
		##diplomacy start+ This is required if kingdom ladies can be promoted to other roles
        (this_or_next|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, 0),#for prisoners
		   (troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(store_faction_of_troop, reg0, ":kingdom_lady"),
		(this_or_next|eq, reg0, ":orig_faction"),
		(neg|faction_slot_eq, reg0, slot_faction_state, sfs_active),
		##diplomacy end+
		(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
		(assign, ":closest_male_relative", reg0),
		(assign, ":new_center", reg1),

		(eq, ":closest_male_relative", ":troop_no"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":kingdom_lady"),
			(display_message, "@{!}DEBUG - {s4} faction changed by guardian moving"),
		(try_end),

		(troop_set_faction, ":kingdom_lady", ":faction_no"),
        (call_script, "script_troop_set_title_according_to_faction", ":kingdom_lady", ":faction_no"),
		(troop_slot_eq, ":kingdom_lady", slot_troop_prisoner_of_party, -1),
		(troop_set_slot, ":kingdom_lady", slot_troop_cur_center, ":new_center"),
	  (try_end),

      #Give new title
      (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"), #moved from top

	  #Remove his control over villages under another fortress
      (try_for_range, ":village_no", villages_begin, villages_end),
        (party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":village_faction", ":village_no"),
        (try_begin),
          (neq, ":village_faction", ":faction_no"),
          (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
          ##diplomacy start+ invalidate cached center points
          (gt, ":old_town_lord", -1),
          (troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, 0),
          ##diplomacy end+
        (try_end),
      (try_end),

	  #Free prisoners
      (try_begin),
        (troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":leaded_party", 0),
        (party_set_faction, ":leaded_party", ":faction_no"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":leaded_party"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":leaded_party", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
          (troop_is_hero, ":cur_troop_id"),
          (eq, ":cur_faction", ":faction_no"),
          (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (party_remove_prisoners, ":leaded_party", ":cur_troop_id", 1),
        (try_end),
      (try_end),

	  #Annull all quests of which the lord is giver
	  (try_for_range, ":quest", all_quests_begin, all_quests_end),
		(check_quest_active, ":quest"),
		(quest_slot_eq, ":quest", slot_quest_giver_troop, ":troop_no"),

		(str_store_troop_name, s4, ":troop_no"),
		(try_begin),
		  (eq, "$cheat_mode", 1),
  		  (display_message, "str_s4_changing_sides_aborts_quest"),
        (try_end),
		(call_script, "script_abort_quest", ":quest", 0),
	  (try_end),

	  #Boot all lords out of centers whose faction has changed
	  ##diplomacy start+ add check for promoted kingdom ladies
	  #(try_for_range, ":lord_to_move", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":lord_to_move", heroes_begin, heroes_end),
		 (troop_slot_ge, ":lord_to_move", slot_troop_leaded_party, 1),
	  ##diplomacy end+
		(troop_get_slot, ":lord_led_party", ":lord_to_move", slot_troop_leaded_party),
	    (party_is_active, ":lord_led_party"),
		(party_get_attached_to, ":led_party_attached", ":lord_led_party"),
		(is_between, ":led_party_attached", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":led_party_faction", ":lord_led_party"),
		(store_faction_of_party, ":attached_party_faction", ":led_party_attached"),
		(neq, ":led_party_faction", ":attached_party_faction"),

		(party_detach, ":lord_led_party"),
	  (try_end),

	  #Increase relation with lord in new faction by 5
	  #Or, if player kingdom, make inactive pending confirmation
	  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	  (try_begin),
		(eq, ":faction_liege", "trp_player"),
		(neq, ":troop_no", "$g_talk_troop"),
	    (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive), #POSSIBLE REASON 1
	  (else_try),
	   ##diplomacy start+ Add support for promoted ladies
		##OLD:
		#(is_between, ":faction_liege", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##NEW:
		(is_between, ":faction_liege", heroes_begin, heroes_end),
		(is_between, ":troop_no", heroes_begin, heroes_end),
		##diplomacy end+
		(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":troop_no", 5),
		(val_add, "$total_indictment_changes", 5),
	  (try_end),

	  #Break courtship relations
	  (try_begin),
	  	(troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#Already married, do nothing
	  (else_try),
		(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy start+
		#Bug fix: don't do this for pretenders.
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		##diplomacy end+
	    (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":courted_lady", ":troop_no", ":love_interest_slot"),
            ##diplomacy start+ don't call this for bad values
            (is_between, ":courted_lady", kingdom_ladies_begin, kingdom_ladies_end),
            ##diplomacy end+
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":courted_lady", ":troop_no"),
	    (try_end),
		##diplomacy start+
		# Don't call this script for married troops / rulers
		#(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_begin),
			(neg|troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
			(neg|is_between, ":troop_no", kings_begin, kings_end),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
			(call_script, "script_assign_troop_love_interests", ":troop_no"),
		(try_end),
		##diplomacy end+
	  (else_try),
		(is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
				(troop_slot_eq, ":active_npc", ":love_interest_slot", ":troop_no"),
				(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":troop_no", ":active_npc"),
			(try_end),
		(try_end),
	  (try_end),

	  #Stop raidings/sieges of new faction's fief if there is any
	  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_party_type, spt_village),
	    (party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),
	    (eq, ":raided_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_village_raided_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (else_try),
	    (party_get_slot, ":besieged_by", ":center_no", slot_center_is_besieged_by),
	    (eq, ":besieged_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_under_siege),
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (try_end),

      (call_script, "script_update_all_notes"),

      (call_script, "script_update_village_market_towns"),
      (assign, "$g_recalculate_ais", 1),
      ]),

  # script_troop_set_title_according_to_faction
  # Input: arg1 = troop_no, arg2 = faction_no
  # EDITED FROM NATIVE TO ALLOW CUSTOM PLAYER KINGDOM TITLES
  ("troop_set_title_according_to_faction",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":faction_no", 2),
      ##diplomacy start+
      # OLD CODE:
      #(try_begin),
      #  (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
      #  (str_store_troop_name_plural, s0, ":troop_no"),
      #  (troop_get_type, ":gender", ":troop_no"),
      #  (store_sub, ":title_index", ":faction_no", kingdoms_begin),
      #  (try_begin),
      #    (eq, ":gender", 0), #male
      #    (val_add, ":title_index", kingdom_titles_male_begin),
      #  (else_try),
      #    (val_add, ":title_index", kingdom_titles_female_begin),
      #  (try_end),
      #  (str_store_string, s1, ":title_index"),
      #  (troop_set_name, ":troop_no", s1),
      #  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
      #  (gt, ":troop_party", 0),
      #  (str_store_troop_name, s5, ":troop_no"),
      #  (party_set_name, ":troop_party", "str_s5_s_party"),
      #(try_end),
      #
      # NEW CODE:
      (assign, ":save_reg0", 0),
      (assign, ":custom_name", 0),
      (try_begin),
	    #Don't do anything when given a bad value.
		 #
		 #We could restrict this further, checking whether the troop is a hero,
		 #or whether it's between heroes_begin and heroes_end, but there are
		 #legitimate reasons a coder may want to run this to get a temporary value,
		 #or use this with temporary heroes, or so forth.
		 #
		 #However, some things are unambiguously errors:
		 (this_or_next|lt, ":troop_no", 0),# At best, the rename operation would fail.
		 (this_or_next|eq, ":troop_no", "trp_heroes_end"),# This is used to store custom titles, so applying a title to this will mess them up.
		 (this_or_next|eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),#This could easily end up changed due to carelessness
		 #There is also no legitimate reason to try to give the titles to generic soldiers.
		 (is_between, ":troop_no", soldiers_begin, soldiers_end),
	  ##Custom player kingdom vassal titles, credit Caba`drin start
	  #(Updated 2011-04-24, to use Caba`drin's 2011-04-20 bug-fix and update)
	  # See http://forums.taleworlds.com/index.php/topic,148259.0.html
      (else_try),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),#<- dplmc+ altered
		(assign, ":troop_is_female", reg0),
		##Additional alteration start
		#All Rhodok benefactor / custodian NPCs insist on the name "Tribune"
		#Currently this is just Bunduk, but others could be added.
		(try_begin),
			(str_store_troop_name, s1, ":troop_no"),#s1 is overwritten below
			#For dialogue reasons, this should be enabled even when the player
			#is co-ruler of an NPC kingdom.
			(this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
				(eq, ":faction_no", "$players_kingdom"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
				(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
			(troop_slot_eq, ":troop_no", slot_troop_original_faction, "fac_kingdom_5"),
			(assign, ":is_coruler", 0),
			(try_begin),
				(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
				(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
				(gt, ":faction_leader", -1),
				(this_or_next|eq, ":faction_leader", "trp_player"),
				(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
					(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(assign, ":is_coruler", 1),
			(try_end),
			(this_or_next|eq, ":is_coruler", 1),
				(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s0, "@Tribune"),
			(str_store_troop_name_plural, s1, ":troop_no"),
			(str_store_string, s1, "str_s0_s1"),
		##Additional alteration end
		(else_try),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered (use script for gender instead)
            (try_begin),
              (eq, ":troop_is_female", 0), #male #<- dplmc+ altered
              (troop_slot_eq, "trp_heroes_end", 0, 1),
              (str_store_troop_name, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (else_try),
              (eq, ":troop_is_female", 1), #slot 0 is potentially unassigned, 'Countess Alayen'
              (troop_slot_eq, "trp_heroes_end", 1, 1),

              #unmarried ladies should retain title
              (assign, ":continue", 0),
              (try_begin),
                  (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
                  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                  (troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
                  (assign, ":continue", 1),
              (else_try),
                  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                  (assign, ":continue", 1),
              (try_end),
              (eq, ":continue", 1),

              (str_store_troop_name_plural, s0, "trp_heroes_end"),
              (str_store_troop_name_plural, s1, ":troop_no"),
              (str_store_string, s1, "str_s0_s1"),
              (assign, ":custom_name", 1),
            (try_end),
            (eq, ":custom_name", 1), #So if it fails, will rename normally
        (else_try),
            (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
            (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
            ##Additional section begin: add support for player kingdom culture
            (try_begin),
                (eq, ":faction_no", "fac_player_supporters_faction"),
                (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
                (assign, ":faction_no", "$g_player_culture"),#<- Use title from culture if one is set, and not using custom titles
            (try_end),
            ##Additional section end
            (str_store_troop_name_plural, s0, ":troop_no"),
            #(troop_get_type, ":gender", ":troop_no"),#<- dplmc+ altered
            (store_sub, ":title_index", ":faction_no", kingdoms_begin),
            (try_begin),
                (this_or_next|eq, ":troop_no", ":faction_leader"),
                (troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"), #wife is now queen/khatun/sultana
                (try_begin),
                    (eq, ":troop_is_female", 0),
                    (val_add, ":title_index", "str_faction_leader_title_male_player"),
                (else_try),
                    (val_add, ":title_index", "str_faction_leader_title_female_player"),
                (try_end),
            (else_try),
                (try_begin),
                  (eq, ":troop_is_female", 0), #<- dplmc+ altered
                  (val_add, ":title_index", kingdom_titles_male_begin),
                (else_try),
                  (try_begin),
                      (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
                      (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                      (troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
                      (val_add, ":title_index", kingdom_titles_female_begin),
                  (else_try),
                      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                      (val_add, ":title_index", kingdom_titles_female_begin),
                  (else_try),
                      (assign, ":title_index", kingdom_titles_female_begin), #unmarried or unlanded ladies should just be Lady
                  (try_end),
                (try_end),
            (try_end),
            (str_store_string, s1, ":title_index"),
        (try_end),
        (troop_set_name, ":troop_no", s1),
        (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":troop_party", 0),
        (str_store_troop_name, s5, ":troop_no"),
        (party_set_name, ":troop_party", "str_s5_s_party"),
      (try_end),
      ##Custom player kingdom vassal titles, credit Caba'drin end
      (assign, reg0, ":save_reg0"),
      ##diplomacy end+
      ]),
  # script_give_center_to_lord
  # Input: arg1 = party_no
  # Output: reg0 = weekly wage
  ("calculate_player_faction_wage",
    [(assign, ":nongarrison_wages", 0),
     (assign, ":garrison_wages", 0),
     (try_for_parties, ":party_no"),
       (assign, ":garrison_troop", 0),
       (try_begin),
         (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_town),
         (party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
         (assign, ":garrison_troop", 1),
       (try_end),
       (this_or_next|eq, ":party_no", "p_main_party"),
       (eq, ":garrison_troop", 1),
       (party_get_num_companion_stacks, ":num_stacks",":party_no"),
       (try_for_range, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
         (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
         (call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
         (assign, ":cur_wage", reg0),
         (val_mul, ":cur_wage", ":stack_size"),
         (try_begin),
           (eq, ":garrison_troop", 1),
           (val_add, ":garrison_wages", ":cur_wage"),
         (else_try),
           (val_add, ":nongarrison_wages", ":cur_wage"),
         (try_end),
       (try_end),
     (try_end),
     (val_div, ":garrison_wages", 2),#Half payment for garrisons
     (store_sub, ":total_payment", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
     (val_mul, ":nongarrison_wages", ":total_payment"),
     (val_div, ":nongarrison_wages", 14),
     ##diplomacy start+ centralization affects this in the player's kingdom
###xxx TODO: This appears to be missing.
     ##diplomacy end+
     (store_add, reg0, ":nongarrison_wages", ":garrison_wages"),
    ]),

  # script_calculate_hero_weekly_net_income_and_add_to_wealth
  ("select_faction_marshall",
   [
#     (store_script_param_1, ":faction_no"),
 #    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
  #   (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),

   #  (assign, ":old_marshal_is_avaliable", 0),
    # (try_begin),
     #  (gt, ":old_faction_marshall", 0),
      # (troop_get_slot, ":old_marshal_party", ":old_faction_marshall", slot_troop_leaded_party),
     #  (party_is_active, ":old_marshal_party"),
    #   (assign, ":old_marshal_is_avaliable", 1),
   #  (try_end),

     #Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an
	 #important event like taking a castle, ext because of marshal change. When marshal changes during
	 #an important event occurs new marshal's followers become 0 and continueing siege attack seems less
	 #valuable then armies demobilize, faction ai become "do nothing", "I cannot think anything to do" ext.

   #  (assign, ":there_is_an_important_situation", 0),
   #  (faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),

   #  (try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    (party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during raiding a village (holding around village)
   #    (is_between, ":current_ai_object", centers_begin, centers_end),
   #    (neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    (party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin), #do not demobilize during besigning a siege (holding around castle)
   #    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
   #    #(str_store_party_name, s7, ":current_ai_object"),
   #    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
   #    (ge, ":besieger_party", 0),
   #    (party_is_active, ":besieger_party"),
   #    #(str_store_party_name, s7, ":besieger_party"),
   #    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
   #    (this_or_next|eq, ":besieger_faction", ":faction_no"),
   #    (eq, ":besieger_faction", "fac_player_faction"),
   #    (assign, ":there_is_an_important_situation", 1),
   #  (try_end),

   #  (try_begin),
   #    (this_or_next|eq, ":there_is_an_important_situation", 0),
   #    (eq, ":old_marshal_is_avaliable", 0),
       #end addition ozan


    #   (assign, ":total_renown", 0),
    #   (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #     (assign, ":cur_troop", ":loop_var"),
    #     (assign, ":continue", 0),
    #     (try_begin),
    #       (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #       (assign, ":cur_troop", "trp_player"),
    #       (try_begin),
    #         (eq, ":faction_no", "$players_kingdom"),
    #         (assign, ":continue", 1),
    #       (try_end),
    #     (else_try),
    #       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
    #       (store_troop_faction, ":cur_faction", ":cur_troop"),
    #       (eq, ":cur_faction", ":faction_no"),
    #       (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
    #       (gt, ":cur_party", 0),
    #       (party_is_active, ":cur_party"),
    #       (call_script, "script_party_count_fit_for_battle", ":cur_party"),
    #       (assign, ":party_fit_for_battle", reg0),
    #       (call_script, "script_party_get_ideal_size", ":cur_party"),
    #       (assign, ":ideal_size", reg0),
    #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
    #       (val_div, ":relative_strength", ":ideal_size"),
    #       (ge, ":relative_strength", 25),
    #       (assign, ":continue", 1),
    #     (try_end),

     #    (eq, ":continue", 1),

    #     (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	#     (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	#     (store_mul, ":relation_modifier", reg0, 15),
	#     (val_add, ":renown", ":relation_modifier"),
	#     (val_max, ":renown", 1),
	#
    #     (try_begin),
    #       (eq, ":cur_troop", "trp_player"),
    #       (neq, ":old_faction_marshall", "trp_player"),
    #       (assign, ":renown", 0),
   #      (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":faction_leader"),
    #       (val_mul, ":renown", 3),
    #       (val_div, ":renown", 4),
    #     (try_end),
    #     (try_begin),
    #       (eq, ":cur_troop", ":old_faction_marshall"),
    #       (val_mul, ":renown", 1000),
    #     (try_end),
    #     (val_add, ":total_renown", ":renown"),
    #   (try_end),
    #   (assign, ":result", -1),
    #   (try_begin),
    #     (gt, ":total_renown", 0),
    #     (store_random_in_range, ":random_renown", 0, ":total_renown"),
    #     (try_for_range, ":loop_var", active_npcs_including_player_begin, active_npcs_end),
    #       (eq, ":result", -1),
    #       (assign, ":cur_troop", ":loop_var"),
    #       (assign, ":continue", 0),
    #       (try_begin),
    #         (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #         (assign, ":cur_troop", "trp_player"),
   #          (try_begin),
   #            (eq, ":faction_no", "$players_kingdom"),
   #            (assign, ":continue", 1),
   #          (try_end),
   #        (else_try),
   #          (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
   #          (store_troop_faction, ":cur_faction", ":cur_troop"),
   #          (eq, ":cur_faction", ":faction_no"),
   #          (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
   #          (gt, ":cur_party", 0),
   #          (party_is_active, ":cur_party"),
   #          (call_script, "script_party_count_fit_for_battle", ":cur_party"),
   #          (assign, ":party_fit_for_battle", reg0),
      #       (call_script, "script_party_get_ideal_size", ":cur_party"),
      #       (assign, ":ideal_size", reg0),
      #       (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
      #       (val_div, ":relative_strength", ":ideal_size"),
      #       (ge, ":relative_strength", 25),
      #       (assign, ":continue", 1),
      #     (try_end),
      #     (eq, ":continue", 1),

		#   (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
	    #   (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":faction_leader"),
	    #   (store_mul, ":relation_modifier", reg0, 15),
	    #   (val_add, ":renown", ":relation_modifier"),
	    #   (val_max, ":renown", 1),
		#
        #   (try_begin),
        #     (eq, ":cur_troop", "trp_player"),
        #     (neq, ":old_faction_marshall", "trp_player"),
        #     (assign, ":renown", 0),
        #   (try_end),
        #   (try_begin),
        #     (eq, ":cur_troop", ":faction_leader"),
        #     (val_mul, ":renown", 3),
         #    (val_div, ":renown", 4),
         #  (try_end),
         #  (try_begin),
       #      (eq, ":cur_troop", ":old_faction_marshall"),
       #      (val_mul, ":renown", 1000),
       #    (try_end),
       #    (val_sub, ":random_renown", ":renown"),
       #    (lt, ":random_renown", 0),
       #    (assign, ":result", ":cur_troop"),
       #  (try_end),
      # (try_end),
      # (try_begin),
         #(eq, "$cheat_mode", 1),
        # (ge, ":result", 0),
       #  (str_store_troop_name, s1, ":result"),
      #   (str_store_faction_name, s2, ":faction_no"),
     #    (display_message, "@{!}{s1} is chosen as the marshall of {s2}."),
    #   (try_end),
   #  (else_try),
   #    (faction_get_slot, ":old_faction_marshall", ":faction_no", slot_faction_marshall),
   #    (assign, ":result", ":old_faction_marshall"),
   #  (try_end),

   #  (assign, reg0, ":result"),
     ]),




  # script_get_center_faction_relation_including_player
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),

      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),


      (str_store_faction_name_link, s1, ":faction_no"),
      #SB : colorize message, although faction color might be better
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", message_negative),
      (try_end),
      (call_script, "script_update_all_notes"),
      ]),

  # script_set_player_relation_with_faction
  # Input: arg1 = faction_no, arg2 = relation
  # Output: none
  ("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
      ]),



  # script_change_player_relation_with_faction_ex
  # changes relations with other factions also (according to their relations between each other)
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_faction_ex",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),

      (str_store_faction_name_link, s1, ":faction_no"),
      #SB : positive/negative messages
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", message_negative),
      (try_end),
      #SB : morale adjustments
      (store_mul, ":morale_change", ":difference", 50), #instead of x100
      (call_script, "script_change_faction_troop_morale", ":faction_no", ":morale_change", 0),

      (try_for_range, ":other_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":other_faction", slot_faction_state, sfs_active),
        (neq, ":faction_no", ":other_faction"),
        (store_relation, ":other_faction_relation", ":faction_no", ":other_faction"),
        (store_relation, ":player_relation", ":other_faction", "fac_player_supporters_faction"),
        (store_mul, ":relation_change", ":difference", ":other_faction_relation"),
        (val_div, ":relation_change", 100),
        (val_add, ":player_relation", ":relation_change"),
        ##diplomacy start
        (try_begin),
            (store_add, ":truce_slot", "fac_player_supporters_faction", slot_faction_truce_days_with_factions_begin),
  		    (val_sub, ":truce_slot", kingdoms_begin),
  		    (faction_get_slot, ":truce_days", ":other_faction", ":truce_slot"),
			##nested diplomacy start+ Changed "eq 0", to "le 0", since now negative truce days track war length
            (this_or_next|le, ":truce_days", 0), #other faction only affected if no truce
			##nested diplomacy end+
            (gt, ":difference", 0), #or change > 0
            (store_relation, ":cur_relation", ":other_faction", "fac_player_supporters_faction"),

            #display relation change message
            (store_sub,  ":relation_change", ":player_relation", ":cur_relation"),
            (str_store_faction_name_link, s1, ":other_faction"),
            (assign, reg1, ":cur_relation"),
            (assign, reg2, ":player_relation"),
            (try_begin),
              (gt, ":relation_change", 0),
              (display_message, "str_faction_relation_increased", message_positive),
            (else_try),
              (lt, ":relation_change", 0),
              (display_message, "str_faction_relation_detoriated", message_negative),
            (try_end),

            #display war declaration
            (try_begin),
                (ge, ":cur_relation", 0), #old relation > 0 -> peace
                (lt, ":player_relation", 0), #new relation < 0 -> war
                ##nested diplomacy start+
                #This is the source of the "fake war" bug.  I think this should get rid of it:
                (try_begin),
                    (this_or_next|eq, "$players_kingdom", "fac_player_faction"),
                       (eq, "$players_kingdom", "fac_player_supporters_faction"),
                ##nested diplomacy end+
                (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
                ##nested diplomacy start+
				(else_try),
					(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
					(store_relation, ":players_kingdom_relation", ":other_faction", "$players_kingdom"),
					(lt, ":players_kingdom_relation", 0),
					(call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
				(else_try),
					#Display some sort of message so you know something happened
				    (display_message, "@{!} There is widespread ill-will towards you in the {s1}."),
                (try_end),
                ##nested diplomacy end+
            (try_end),
        ##diplomacy end
        (set_relation, ":other_faction", "fac_player_faction", ":player_relation"),
        (set_relation, ":other_faction", "fac_player_supporters_faction", ":player_relation"),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
      (try_end),
      (try_begin),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
          (call_script, "script_update_faction_notes", ":kingdom_no"),
        (try_end),
      (try_end),
  ]),

  # script_cf_get_random_active_faction_except_player_faction_and_faction
  # Input: arg1 = except_faction_no
  # Output: reg0 = random_faction
  ("cf_get_random_active_faction_except_player_faction_and_faction",
    [
      (store_script_param_1, ":except_faction_no"),
      (assign, ":num_factions", 0),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_add, ":num_factions", 1),
      (try_end),
      (gt, ":num_factions", 0),
      (assign, ":selected_faction", -1),
      (store_random_in_range, ":random_faction", 0, ":num_factions"),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (ge, ":random_faction", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (neq, ":faction_no", ":except_faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (val_sub, ":random_faction", 1),
        (lt, ":random_faction", 0),
        (assign, ":selected_faction", ":faction_no"),
      (try_end),
      (assign, reg0, ":selected_faction"),
  ]),

  # script_make_kingdom_hostile_to_player
  # Input: arg1 = initializing_war_peace_cond (1 = true, 0 = false)
  # Output: none

  #Aims to introduce a slightly simpler system in which the AI kings' reasoning could be made more  transparent to the player. At the start of the game, this may lead to less variation in outcomes, though
  ("randomly_start_war_peace_new",
    [
    (store_script_param_1, ":initializing_war_peace_cond"),

	(assign, ":players_kingdom_at_peace", 0), #if the player kingdom is at peace, then create an enmity
	(try_begin),
		(is_between, "$players_kingdom", "fac_kingdom_1", kingdoms_end),
		(assign, ":players_kingdom_at_peace", 1),
	(try_end),

	##diplomacy start+
	#Introduce some minor variation by changing the order in which factions consider things.
	##OLD:
    #(try_for_range, ":cur_kingdom", "fac_kingdom_1", kingdoms_end),
    #    (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
	#
	#	(try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
	##NEW:
	(store_random_in_range, ":random_offset_1", "fac_kingdom_1", kingdoms_end),
	(val_sub, ":random_offset_1", "fac_kingdom_1"),
	(try_for_range, ":cur_kingdom", "fac_kingdom_1", kingdoms_end),
		(val_add, ":cur_kingdom", ":random_offset_1"),
		(try_begin),
			(ge, ":cur_kingdom", kingdoms_end),
			(val_sub, ":cur_kingdom", kingdoms_end),
			(val_add, ":cur_kingdom", "fac_kingdom_1"),
		(try_end),
		(faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
		(store_random_in_range, ":random_offset_2", kingdoms_begin, kingdoms_end),
		(val_sub, ":random_offset_2", kingdoms_begin),
		(try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
			(val_add, ":cur_kingdom_2", ":random_offset_2"),
			(try_begin),
				(ge, ":cur_kingdom_2", kingdoms_end),
				(val_sub, ":cur_kingdom_2", kingdoms_end),
				(val_add, ":cur_kingdom_2", kingdoms_begin),
			(try_end),
	##diplomacy end+
			(neq, ":cur_kingdom", ":cur_kingdom_2"),
			(faction_slot_eq, ":cur_kingdom_2", slot_faction_state, sfs_active),

			(call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),
			(assign, ":kingdom_1_to_kingdom_2", reg0),

			(store_relation, ":cur_relation", ":cur_kingdom", ":cur_kingdom_2"),
			(try_begin),
				(lt, ":cur_relation", 0), #AT WAR

				(try_begin),
					(eq, ":cur_kingdom", "$players_kingdom"),
					(assign, ":players_kingdom_at_peace", 0),
				(try_end),

				(ge, ":kingdom_1_to_kingdom_2", 1),

        ##diplomacy begin
        (try_begin),
      	  (store_current_hours, ":cur_hours"),
          (faction_get_slot, ":faction_ai_last_decisive_event", ":cur_kingdom", slot_faction_ai_last_decisive_event),
          (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),
          (ge, ":hours_since_last_decisive_event", 96), #wait 4 days until you conclude peace after war
        ##diplomacy end
          (try_begin),
            (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),

            (store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", 2),
            (store_random_in_range, ":random", 0, 20),
            (try_begin),
              (lt, ":random", ":goodwill_level"),
              (call_script, "script_add_notification_menu", "mnu_question_peace_offer", ":cur_kingdom", 0),
            (try_end),
          (else_try),
            (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom_2", ":cur_kingdom", -1),
            (assign, ":kingdom_2_to_kingdom_1", reg0),
            (ge, ":kingdom_2_to_kingdom_1", 1),

            (store_mul, ":goodwill_level", ":kingdom_1_to_kingdom_2", ":kingdom_2_to_kingdom_1"),
            (store_random_in_range, ":random", 0, 20),
            (lt, ":random", ":goodwill_level"),

            (try_begin),
              (eq, "$g_include_diplo_explanation", 0),
              (assign, "$g_include_diplo_explanation", ":cur_kingdom"),
              (str_store_string, s57, "str_s14"),
            (try_end),

            (call_script, "script_diplomacy_start_peace_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (try_end),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
			(else_try),
				(ge, ":cur_relation", 0), #AT PEACE

			    (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom", ":cur_kingdom_2", -1),

				#negative, leans towards war/positive, leans towards peace
				(le, reg0, 0), #still no chance of war unless provocation, or at start of game

			    (assign, ":hostility", reg0),

			    (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_kingdom", ":cur_kingdom_2"),
			    (le, reg0, 0), #no truce

				(val_add, ":hostility", reg0), #increase hostility if there is a provocation

				(val_sub, ":hostility", 1), #greater chance at start of game
				(val_add, ":hostility", ":initializing_war_peace_cond"), #this variable = 1 after the start

				(store_mul, ":hostility_squared", ":hostility", ":hostility"),
				(store_random_in_range, ":random", 0, 50),

        ##diplomacy begin
        #check for pact and lower probability if there is one
        (try_for_range, ":third_kingdom", kingdoms_begin, kingdoms_end),
          (neq, ":third_kingdom", ":cur_kingdom"),
          (neq, ":third_kingdom", ":cur_kingdom_2"),
		  ##nested diplomacy start+  Faction must be active
		  (faction_slot_eq, ":third_kingdom", slot_faction_state, sfs_active),
		  ##nested diplomacy end+

          (store_relation, ":cur_relation", ":cur_kingdom_2", ":third_kingdom"),
    			(ge, ":cur_relation", 0), #AT PEACE

          (store_add, ":truce_slot", ":third_kingdom", slot_faction_truce_days_with_factions_begin),
      		(val_sub, ":truce_slot", kingdoms_begin),
      		(faction_get_slot, ":truce_days", ":cur_kingdom_2", ":truce_slot"),
      		##nested diplomacy start+ replace "40" with a named constant
      		#(gt, ":truce_days", 40),
      		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
      		##nested diplomacy end+
      		(store_div, ":hostility_change", ":truce_days", 20),
      		(val_sub, ":hostility_squared", ":hostility_change"),
        (try_end),
        ##diplomacy end

			    (lt, ":random", ":hostility_squared"),

				(try_begin),
					(eq, "$g_include_diplo_explanation", 0),
					(assign, "$g_include_diplo_explanation", ":cur_kingdom"),
					(str_store_string, s57, "str_s14"),
				(try_end),
                (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),

				(try_begin), #do some war damage for
					(eq, ":initializing_war_peace_cond", 0),
					(store_random_in_range, ":war_damage_inflicted", 10, 120),
					(store_add, ":slot_war_damage_inflicted", ":cur_kingdom", slot_faction_war_damage_inflicted_on_factions_begin),
					(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					(faction_set_slot, ":cur_kingdom_2",  ":slot_war_damage_inflicted", ":war_damage_inflicted"),

					(store_add, ":slot_war_damage_inflicted", ":cur_kingdom_2", slot_faction_war_damage_inflicted_on_factions_begin),
					(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
					(faction_set_slot, ":cur_kingdom", ":slot_war_damage_inflicted", ":war_damage_inflicted"),
				(try_end),
      ##diplomacy begin
      (else_try),
        (ge, ":cur_relation", 0), #AT PEACE
        (ge, ":kingdom_1_to_kingdom_2", 1),

        #(assign, ":barrier", 2),
        (store_add, ":faction1_to_faction2_slot", ":cur_kingdom_2", dplmc_slot_faction_attitude_begin),
        (party_get_slot, ":barrier",":cur_kingdom", ":faction1_to_faction2_slot"),

        (try_for_range, ":third_kingdom", kingdoms_begin, kingdoms_end),
          (neq, ":third_kingdom", ":cur_kingdom"),
          (neq, ":third_kingdom", ":cur_kingdom_2"),

          (store_add, ":slot_truce_days", ":cur_kingdom", slot_faction_truce_days_with_factions_begin),
          (val_sub, ":slot_truce_days", kingdoms_begin),
          (faction_get_slot, ":truce_days", ":third_kingdom", ":slot_truce_days"),
          ##nested diplomacy start+ change to use constants
          #(gt, ":truce_days", 10),
          (gt, ":truce_days", dplmc_treaty_truce_days_half_done),
          ##nested diplomacy end+
          (val_sub, ":barrier", 1),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (str_store_faction_name, s5, ":cur_kingdom"),
            (str_store_faction_name, s6, ":third_kingdom"),
            (str_store_faction_name, s7, ":cur_kingdom_2"),
            (display_message, "@{!}DEBUG: {s5} has truce with {s6}. Pact with {s7} is harder!"),
          (try_end),

        (try_end),

        (val_max, ":barrier", 0),
        (store_random_in_range, ":random", 0, 130),
        (le, ":random", ":barrier"),

        (store_add, ":slot_truce_days", ":cur_kingdom", slot_faction_truce_days_with_factions_begin),
        (val_sub, ":slot_truce_days", kingdoms_begin),
        (faction_get_slot, ":truce_days", ":cur_kingdom_2", ":slot_truce_days"),

        (store_random_in_range, ":random", 0, 3),
        (assign, ":continue", 0),
        (try_begin),
          ##nested diplomacy start+ change to use constants
          #(is_between, ":truce_days", 0, 50),
          (is_between, ":truce_days", 0, dplmc_treaty_defense_days_half_done),#50 = halfway from a defensive alliance to a trade treaty
          ##nested diplomacy end+
          (ge, ":cur_relation", 20),
          (try_begin),
            (le, ":random", 0), #1/3 for alliance, defensive
            (assign, ":continue", 1),
          (try_end),
        (else_try),
          ##nested diplomacy start+ change to use constants
          #(is_between, ":truce_days", 0, 10),
          (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),#10 = halfway done with a truce
          ##nested diplomacy end+
          (ge, ":cur_relation", 10),
          (try_begin),
            (le, ":random", 1), #2/3 # for trade
            (assign, ":continue", 1),
          (try_end),
        (else_try),
          (assign, ":continue", 1),  # for non-aggression
        (try_end),
        (eq, ":continue", 1),

        (try_begin),
		  ##nested diplomacy start+
		  (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":cur_kingdom_2"),
		  (this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		  ##nested diplomacy end+
          (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
          (ge, ":kingdom_1_to_kingdom_2", 1),

          (try_begin),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 20, 50),
            (is_between, ":truce_days", dplmc_treaty_trade_days_expire, dplmc_treaty_defense_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 30),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_alliance_offer", ":cur_kingdom", 0),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 30), #you need a non-aggression or trade aggreement for an defensive pact
            (is_between, ":truce_days", 0, dplmc_treaty_trade_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 20),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_defensive_offer", ":cur_kingdom", 0),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 10),
            (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),
            ##diplomacy end+
            (ge, ":cur_relation", 10),
            (faction_slot_eq, ":cur_kingdom", slot_faction_recognized_player, 1), #recognized us
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_trade_offer", ":cur_kingdom", 0),
          (else_try),
            (eq, ":truce_days", 0),
            (ge, ":cur_relation", 5),
            (call_script, "script_add_notification_menu", "mnu_dplmc_question_nonaggression_offer", ":cur_kingdom", 0),
          (try_end),
        (else_try),
          (ge, ":kingdom_1_to_kingdom_2", 1),

          (call_script, "script_npc_decision_checklist_peace_or_war", ":cur_kingdom_2", ":cur_kingdom", -1),
          (assign, ":kingdom_2_to_kingdom_1", reg0),
          (ge, ":kingdom_2_to_kingdom_1", 1),

          (try_begin),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 20, 50),
            (is_between, ":truce_days", dplmc_treaty_trade_days_expire, dplmc_treaty_defense_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 30),
            (call_script, "script_dplmc_start_alliance_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 30), #you need a non-aggression or trade aggreement for an defensive pact
            (is_between, ":truce_days", 0, dplmc_treaty_trade_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 20),
            (call_script, "script_dplmc_start_defensive_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            ##nested diplomacy start+ change to use constants
            #(is_between, ":truce_days", 0, 10),
            (is_between, ":truce_days", 0, dplmc_treaty_truce_days_half_done),
            ##nested diplomacy end+
            (ge, ":cur_relation", 10),
            (call_script, "script_dplmc_start_trade_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (else_try),
            (eq, ":truce_days", 0),
            (call_script, "script_dplmc_start_nonaggression_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
          (try_end),
        (try_end),
      ##diplomacy end
      (try_end),
		(try_end),
	(try_end),

	(try_begin),
		(eq, ":players_kingdom_at_peace", 1),
		(val_add, "$players_kingdom_days_at_peace", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg3, "$players_kingdom_days_at_peace"),
			(display_message, "@{!}DEBUG -- Player's kingdom has had {reg3} days of peace"),
		(try_end),
	(else_try),
		(assign, "$players_kingdom_days_at_peace", 0),
	(try_end),

     ]),


  # script_randomly_start_war_peace
  # Input: arg1 = initializing_war_peace_cond (1 = true, 0 = false)
  # Output: none
#  ("randomly_start_war_peace",
#    [
#      (store_script_param_1, ":initializing_war_peace_cond"),
#      (assign, ":total_resources", 0),
#      (assign, ":total_active_kingdoms", 0),
#      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
#        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
#        (val_add, ":total_active_kingdoms", 1),
#        (faction_get_slot, ":num_towns", ":cur_kingdom", slot_faction_num_towns),
#        (store_mul, ":kingdom_resources_value", ":num_towns", 2),
#        (faction_get_slot, ":num_castles", ":cur_kingdom", slot_faction_num_castles),
#        (val_add, ":kingdom_resources_value", ":num_castles"),
#        (val_mul, ":kingdom_resources_value", 10),
#        (val_max, ":kingdom_resources_value", 1),
#        (val_mul, ":kingdom_resources_value", 1000),
#        (faction_get_slot, ":num_armies", ":cur_kingdom", slot_faction_num_armies),
#        (val_max, ":num_armies", 1),
#        (val_div, ":kingdom_resources_value", ":num_armies"),
#        (val_add, ":total_resources", ":kingdom_resources_value"),
#      (try_end),
#      (val_max, ":total_active_kingdoms", 1),
#      (store_div, ":average_resources", ":total_resources", ":total_active_kingdoms"),

#      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
 ##       (neq, ":cur_kingdom", "fac_player_supporters_faction"),
#        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
#        (assign, ":num_ongoing_wars", 0),
#        (try_for_range, ":other_kingdom", kingdoms_begin, kingdoms_end),
#          (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
#          (store_relation, ":other_relation", ":cur_kingdom", ":other_kingdom"),
#          (lt, ":other_relation", 0),
#          (val_add, ":num_ongoing_wars", 1),
#        (try_end),

#        (faction_get_slot, ":num_towns", ":cur_kingdom", slot_faction_num_towns),
#        (store_mul, ":kingdom_1_resources_value", ":num_towns", 2),
#        (faction_get_slot, ":num_castles", ":cur_kingdom", slot_faction_num_castles),
#        (val_add, ":kingdom_1_resources_value", ":num_castles"),
#        (val_mul, ":kingdom_1_resources_value", 10),
#        (val_max, ":kingdom_1_resources_value", 1),
#        (val_mul, ":kingdom_1_resources_value", 1000),
#        (faction_get_slot, ":num_armies", ":cur_kingdom", slot_faction_num_armies),
#        (val_max, ":num_armies", 1),
#        (val_div, ":kingdom_1_resources_value", ":num_armies"),

#        (store_add, ":start_cond", ":cur_kingdom", 1),
#        (try_for_range, ":cur_kingdom_2", ":start_cond", kingdoms_end),
 ##         (neq, ":cur_kingdom", "fac_player_supporters_faction"),
#          (faction_slot_eq, ":cur_kingdom_2", slot_faction_state, sfs_active),

#          (assign, ":num_ongoing_wars_2", 0),
#          (try_for_range, ":other_kingdom", kingdoms_begin, kingdoms_end),
#            (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
#            (store_relation, ":other_relation", ":cur_kingdom_2", ":other_kingdom"),
#            (lt, ":other_relation", 0),
#            (val_add, ":num_ongoing_wars_2", 1),
#          (try_end),

#          (store_add, ":total_ongoing_wars", ":num_ongoing_wars", ":num_ongoing_wars_2"),

#          (faction_get_slot, ":num_towns", ":cur_kingdom_2", slot_faction_num_towns),
#          (store_mul, ":kingdom_2_resources_value", ":num_towns", 2),
#          (faction_get_slot, ":num_castles", ":cur_kingdom_2", slot_faction_num_castles),
#          (val_add, ":kingdom_2_resources_value", ":num_castles"),
#          (val_mul, ":kingdom_2_resources_value", 10),
#          (val_max, ":kingdom_2_resources_value", 1),
#          (val_mul, ":kingdom_2_resources_value", 1000),
#          (faction_get_slot, ":num_armies", ":cur_kingdom_2", slot_faction_num_armies),
#          (val_max, ":num_armies", 1),
#          (val_div, ":kingdom_2_resources_value", ":num_armies"),

#          (assign, ":max_resources_value", ":kingdom_1_resources_value"),
#          (val_max, ":max_resources_value", ":kingdom_2_resources_value"),
#          (val_mul, ":max_resources_value", 100),
#          (val_div, ":max_resources_value", ":average_resources"),

#          (assign, ":cur_king", -1),
#          (try_begin),
#            (eq, ":cur_kingdom", "fac_player_supporters_faction"),
#            (faction_get_slot, ":cur_king", ":cur_kingdom_2", slot_faction_leader),
#            (assign, ":cur_relation", reg0),
#            (store_sub, ":relation_effect", 200, ":cur_relation"),
#            (val_mul, ":kingdom_1_resources_value", ":relation_effect"),
#            (val_div, ":kingdom_1_resources_value", 200),
#          (else_try),
#            (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
#            (faction_get_slot, ":cur_king", ":cur_kingdom", slot_faction_leader),
#          (try_end),

#          (try_begin),
#            (ge, ":cur_king", 0),
#            (call_script, "script_troop_get_player_relation", ":cur_king"),
#            (assign, ":cur_relation", reg0),
#            (store_sub, ":relation_effect", 200, ":cur_relation"),
#            (val_mul, ":max_resources_value", ":relation_effect"),
#            (val_div, ":max_resources_value", 200),
#          (try_end),

          #max_resources_value is the obtained value that gives us how tempting the kingdom's values are
          #average is 100
 #         (val_clamp, ":max_resources_value", 20, 500),
          #not letting more than 5 times higher chance of declaring war or peace

  #        (store_random_in_range, ":random_no", 0, 10000),
 #         (store_relation, ":cur_relation", ":cur_kingdom", ":cur_kingdom_2"),
 #         (try_begin),
 #           (lt, ":cur_relation", 0), #AT WAR
 #           (store_mul, ":chance_to_make_peace", ":total_ongoing_wars", 50),
 #           (val_mul, ":chance_to_make_peace", 100),
 #           (val_div, ":chance_to_make_peace", ":max_resources_value"),
 #           (try_begin),
              #disable random peace for special conditions
 #             (this_or_next|eq, ":cur_kingdom", "fac_player_supporters_faction"),
 #             (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
 #             (assign, ":continue", 0),
          #    (try_begin),
           #     (gt, "$supported_pretender", 0),
            #    (this_or_next|eq, ":cur_kingdom", "$supported_pretender_old_faction"),
           #     (eq, ":cur_kingdom_2", "$supported_pretender_old_faction"),
          #      (assign, ":continue", 1),
         #     (else_try),
       #         (is_between, "$players_oath_renounced_against_kingdom", kingdoms_begin, kingdoms_end),
      #          (this_or_next|eq, ":cur_kingdom", "$players_oath_renounced_against_kingdom"),
     #           (eq, ":cur_kingdom_2", "$players_oath_renounced_against_kingdom"),
    #            (assign, ":continue", 1),
   #           (try_end),
         #     (eq, ":continue", 1),
        #      (assign, ":chance_to_make_peace", 0),
       #     (try_end),
      #      (try_begin),
     #         (lt, ":random_no", ":chance_to_make_peace"),
    #          (assign, ":continue", 1),
   #           (try_begin),
  #              (check_quest_active, "qst_persuade_lords_to_make_peace"),
              #  (quest_get_slot, ":quest_target_faction", "qst_persuade_lords_to_make_peace", slot_quest_target_faction),
             #   (quest_get_slot, ":quest_object_faction", "qst_persuade_lords_to_make_peace", slot_quest_object_faction),
            #    (this_or_next|eq, ":cur_kingdom", ":quest_target_faction"),
           #     (eq, ":cur_kingdom", ":quest_object_faction"),
          #      (this_or_next|eq, ":cur_kingdom_2", ":quest_target_faction"),
         #       (eq, ":cur_kingdom_2", ":quest_object_faction"),
        #        (assign, ":continue", 0), #Do not declare war if the quest is active for the specific kingdoms
       #       (try_end),
      #        (eq, ":continue", 1),
     #         (try_begin),
    #            (eq, ":cur_kingdom", "fac_player_supporters_faction"),
   #             (call_script, "script_add_notification_menu", "mnu_question_peace_offer", ":cur_kingdom_2", 0),
  #            (else_try),
            #    (eq, ":cur_kingdom_2", "fac_player_supporters_faction"),
           #     (call_script, "script_add_notification_menu", "mnu_question_peace_offer", ":cur_kingdom", 0),
          #    (else_try),
         #       (call_script, "script_diplomacy_start_peace_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
        #      (try_end),
       #     (try_end),
      #    (else_try), # AT PEACE
     #       (assign, ":chance_to_declare_war", 6),
    #        (val_sub, ":chance_to_declare_war", ":total_ongoing_wars"),
   #         (val_mul, ":chance_to_declare_war", 50),
          #  (val_mul, ":chance_to_declare_war", ":max_resources_value"),
         #   (val_div, ":chance_to_declare_war", 100),
        #    (try_begin),
       #       (lt, ":random_no", ":chance_to_declare_war"),
      #        (assign, ":continue", 1),
     #         (try_begin),
    #            (check_quest_active, "qst_raid_caravan_to_start_war"),
               # (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
              #  (quest_get_slot, ":quest_object_faction", "qst_raid_caravan_to_start_war", slot_quest_object_faction),
             #   (this_or_next|eq, ":cur_kingdom", ":quest_target_faction"),
            #    (eq, ":cur_kingdom", ":quest_object_faction"),
           #     (this_or_next|eq, ":cur_kingdom_2", ":quest_target_faction"),
          #      (eq, ":cur_kingdom_2", ":quest_object_faction"),
         #       (assign, ":continue", 0), #Do not declare war if the quest is active for the specific kingdoms
        #      (try_end),
       #       (eq, ":continue", 1),
      #        (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":cur_kingdom_2", ":initializing_war_peace_cond"),
     #       (try_end),
    #      (try_end),
   #     (try_end),
  #    (try_end),
 #    ]),



# script_exchange_prisoners_between_factions
# Input: arg1 = faction_no_1, arg2 = faction_no_2
  ("exchange_prisoners_between_factions",
   [
       (store_script_param_1, ":faction_no_1"),
       (store_script_param_2, ":faction_no_2"),
       (assign, ":faction_no_3", -1),
       (assign, ":faction_no_4", -1),
       (assign, ":free_companions_too", 0),
       (try_begin),
         (this_or_next|eq, "$players_kingdom", ":faction_no_1"),
         (eq, "$players_kingdom", ":faction_no_2"),
         (assign, ":faction_no_3", "fac_player_faction"),
         (assign, ":faction_no_4", "fac_player_supporters_faction"),
         (assign, ":free_companions_too", 1),
       (try_end),

       (try_for_parties, ":party_no"),
         (store_faction_of_party, ":party_faction", ":party_no"),
         (this_or_next|eq, ":party_faction", ":faction_no_1"),
         (this_or_next|eq, ":party_faction", ":faction_no_2"),
         (this_or_next|eq, ":party_faction", ":faction_no_3"),
         (eq, ":party_faction", ":faction_no_4"),
         (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
         (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
           (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),

           (assign, ":continue", 0),
           (try_begin),
             (is_between, ":cur_troop_id", companions_begin, companions_end),
             (eq, ":free_companions_too", 1),
             (assign, ":continue", 1),
           (else_try),
             (neg|is_between, ":cur_troop_id", companions_begin, companions_end),
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),
             (this_or_next|eq, ":cur_faction", ":faction_no_1"),
             (this_or_next|eq, ":cur_faction", ":faction_no_2"),
             (this_or_next|eq, ":cur_faction", ":faction_no_3"),
             (eq, ":cur_faction", ":faction_no_4"),
             (assign, ":continue", 1),
           (try_end),
           (eq, ":continue", 1),

           (try_begin),
             (troop_is_hero, ":cur_troop_id"),
             (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
           (try_end),
           (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
           (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),
         (try_end),
       (try_end),

    ]),

  # script_add_notification_menu
  # INPUT: arg1 = faction_no
  # OUTPUT: none
  ("player_join_faction",
    [
      (store_script_param, ":faction_no", 1),
      (assign,"$players_kingdom",":faction_no"),
      (faction_set_slot, "fac_player_supporters_faction", slot_faction_ai_state, sfai_default),
      (assign, "$players_oath_renounced_against_kingdom", 0),
      (assign, "$players_oath_renounced_given_center", 0),
      (assign, "$players_oath_renounced_begin_time", 0),

      (try_for_range,":other_kingdom",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":other_kingdom", slot_faction_state, sfs_active),
        (neq, ":other_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (neq, ":other_kingdom", ":faction_no"),
          (store_relation, ":other_kingdom_reln", ":other_kingdom", ":faction_no"),
        (else_try),
          (store_relation, ":other_kingdom_reln", "fac_player_supporters_faction", ":other_kingdom"),
          (val_max, ":other_kingdom_reln", 12),
        (try_end),
        (call_script, "script_set_player_relation_with_faction", ":other_kingdom", ":other_kingdom_reln"),
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        #Give center to kingdom if player is the owner
        (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
	  (else_try),
        #Give center to kingdom if part of player faction
     	(store_faction_of_party, ":cur_center_faction", ":cur_center"),
		(eq, ":cur_center_faction", "fac_player_supporters_faction"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":cur_center", ":faction_no"),
      (try_end),

      (try_for_range, ":quest_no", lord_quests_begin, lord_quests_end),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_for_range, ":quest_no", lord_quests_begin_2, lord_quests_end_2),
        (check_quest_active, ":quest_no"),
        (quest_get_slot, ":quest_giver_troop", ":quest_no", slot_quest_giver_troop),
        (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
        (store_relation, ":quest_giver_faction_relation", "fac_player_supporters_faction", ":quest_giver_faction"),
        (lt, ":quest_giver_faction_relation", 0),
        (call_script, "script_abort_quest", ":quest_no", 0),
      (try_end),
      (try_begin),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
        (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      (try_end),

	  (try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 1"),
		(try_end),

	    (troop_set_faction, ":spouse", "$players_kingdom"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "$players_kingdom"),
	  (try_end),
	  ##diplomacy start+
	  #Make other vassals follow the player.
	  ##(There are other possibilities that we might want to explore, but
	  ##what happens now is that they remain members of the defunct faction.)
	  (try_begin),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		  (try_for_range, ":troop_no", heroes_begin, heroes_end),
			 (store_troop_faction, ":other_troop_faction", ":troop_no"),
			 (eq, ":other_troop_faction", "fac_player_supporters_faction"),

			 (this_or_next|neg|is_between, ":troop_no", companions_begin, companions_end),
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
				(troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
			 (this_or_next|neq, ":troop_no", ":spouse"),
				(neg|is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":troop_no"),
				(display_message, "@{!} DEBUG - {s4} changed by player's defection"),
			(try_end),
			(troop_set_faction, ":troop_no", "$players_kingdom"),
			#Clear troop slots
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
			(troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
			(troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),
			#Give new title
			(try_begin),
				(this_or_next|neg|is_between,":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"),
			(try_end),
			#Change led party
			(try_begin),
				(troop_get_slot, ":troop_leaded_party", ":troop_no", slot_troop_leaded_party),
				(gt, ":troop_leaded_party", 0),
				(party_is_active, ":troop_leaded_party"),
				(party_set_faction, ":troop_leaded_party", ":faction_no"),
			(try_end),
		  (try_end),
	  (try_end),
	  ##diplomacy end+

	  # (try_for_range, ":center", centers_begin, centers_end),
	    # (store_faction_of_party, ":center_faction", ":faction_no"),
		# (neq, ":center_faction", "$players_kingdom"),
		# (party_slot_eq, ":center", slot_town_lord, stl_reserved_for_player),
# #		(party_set_slot, ":center", slot_town_lord, stl_unassigned),
	  # (try_end),

	  (troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),

	  #remove prisoners of player's faction if he was member of his own faction. And free companions which is prisoned in that faction.
      (try_for_parties, ":party_no"),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":faction_no"),

        (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),

          (this_or_next|eq, ":cur_faction", "fac_player_supporters_faction"),
          (this_or_next|eq, ":cur_faction", ":faction_no"),
          (is_between, ":cur_troop_id", companions_begin, companions_end),

          (try_begin),
            (troop_is_hero, ":cur_troop_id"),
            (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (try_end),

          (party_prisoner_stack_get_size, ":stack_size", ":party_no", ":troop_iterator"),
          (party_remove_prisoners, ":party_no", ":cur_troop_id", ":stack_size"),

          (try_begin),
            (is_between, ":cur_troop_id", companions_begin, companions_end),

            (try_begin),
              (is_between, ":party_no", towns_begin, towns_end),
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":party_no"),
            (else_try),
              (store_random_in_range, ":random_town_no", towns_begin, towns_end),
              (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":random_town_no"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      #remove prisoners end.

      #(call_script, "script_store_average_center_value_per_faction"),
      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),
      ]),

  #script_player_leave_faction
  # INPUT: arg1 = give_back_fiefs
  # OUTPUT: none
  ("player_leave_faction",
    [
      (store_script_param, ":give_back_fiefs", 1),

      (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
      (assign, ":old_kingdom", "$players_kingdom"),
      (assign, ":old_has_homage", "$player_has_homage"),
      (assign, "$players_kingdom", 0),
      (assign, "$player_has_homage", 0),

      (try_begin),
        (neq, ":give_back_fiefs", 0), #ie, give back fiefs = 1, thereby do it
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          ##diplomacy begin
          #native bug fix when giving back fiefs
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_neutral"),
          ##diplomacy end
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),

          #The following line also occurs when a lord is stripped of his fiefs by an indictment
          (party_set_slot, ":cur_center", slot_town_lord, stl_unassigned),
        (try_end),
      (else_try),
        #If you retain the fiefs
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_player_supporters_faction"),
          (party_set_slot, ":cur_center", slot_town_lord, "trp_player"),
          (troop_get_slot, ":cur_banner", "trp_player", slot_troop_banner_scene_prop),
          #custom_banner_begin
          (try_begin),
              (gt, ":cur_banner", 0),
              (val_sub, ":cur_banner", banner_scene_props_begin),
              (val_add, ":cur_banner", banner_map_icons_begin),
              (party_set_banner_icon, ":cur_center", ":cur_banner"),
          (else_try),
            (eq, ":cur_banner", -1),
            (troop_get_slot, ":flag_icon", "trp_player", slot_troop_custom_banner_map_flag_type),
            (try_begin),
               (ge, ":flag_icon", 0),
               (val_add, ":flag_icon", custom_banner_map_icons_begin),
               (party_set_banner_icon, ":cur_center", ":flag_icon"),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":cur_center", villages_begin, villages_end),
          (party_get_slot, ":cur_bound_center", ":cur_center", slot_village_bound_center),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (neg|party_slot_eq, ":cur_bound_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
        (try_end),

        (is_between, ":old_kingdom", kingdoms_begin, kingdoms_end),
        (neq, ":old_kingdom", "fac_player_supporters_faction"),
        (store_relation, ":reln", "fac_player_supporters_faction", ":old_kingdom"),
        (store_sub, ":req_dif", -40, ":reln"),
        (call_script, "script_change_player_relation_with_faction", ":old_kingdom", ":req_dif"),
      (try_end),

      (try_begin),
        (eq, ":old_has_homage", 1),
        (faction_get_slot, ":faction_leader", ":old_kingdom", slot_faction_leader),
        (call_script, "script_change_player_relation_with_troop", ":faction_leader", -20),
      (try_end),

      (try_begin),
        (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
        (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),

        (try_begin),
            (ge, "$cheat_mode", 1),
            (str_store_troop_name, s4, ":spouse"),
            (display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 3"),
        (try_end),


        (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "fac_player_supporters_faction"),
      (try_end),

      #Change relations with players_kingdom when player changes factions
      (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
        (neq, ":kingdom", "fac_player_supporters_faction"),
        (store_relation, ":relation_with_old_faction", ":old_kingdom", ":kingdom"),
        (store_relation, ":relation_with_player_faction", "fac_player_faction", ":kingdom"),

        (try_begin),
          (eq, ":old_kingdom", ":kingdom"),
          (val_min, ":relation_with_player_faction", 0),
        (else_try),
          (lt, ":relation_with_old_faction", 0),
          (val_max, ":relation_with_player_faction", 0),
       ##diplomacy start+ do not retain allies of former kingdom
       (else_try),
         (gt, ":relation_with_old_faction", 0),
         (val_min, ":relation_with_player_faction", 0),
       ##diplomacy end+
        (try_end),
        (set_relation, "fac_player_faction", ":kingdom", ":relation_with_player_faction"),
        (set_relation, "fac_player_supporters_faction", ":kingdom", ":relation_with_player_faction"),
      (try_end),

      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),

        ##diplomacy begin
        ##disband player patrols
      #SB : build one string instead of one for each party
      (try_begin),
        (str_clear, s6),
        (assign, ":num_parties", 0),
        # (ge, ":give_back_fiefs", 1),
        (try_for_parties, ":party_no"),
          (party_is_active, ":party_no"),
          (party_slot_eq,":party_no", slot_party_type, spt_patrol),
          #SB : add other checks such as faction and home center ownership
          (store_faction_of_party, ":party_faction", ":party_no"),
          (eq, ":party_faction", ":old_kingdom"),
          (party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
          # (party_slot_eq, ":home_center", slot_town_lord, "trp_player"), #this may no longer be true

          #build string
          (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
          (str_store_party_name, s50, ":target_party"),
          (try_begin),
            (eq, ":num_parties", 0),
            (str_store_string_reg, s51, s50),
          (else_try),
            (eq, ":num_parties", 1),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
          # (display_log_message, "@Your soldiers patrolling {s6} disbanded because you left the faction!", message_defeated),
          (try_begin), #do not give back fiefs, keep the patrols
            (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
            # (eq, ":give_back_fiefs", 0),
            (party_get_slot, ":town_lord", ":home_center", slot_town_lord),
            (eq, ":town_lord", "trp_player"),
            (party_set_faction, ":party_no", "fac_player_supporters_faction"),
            # (remove_party, ":party_no"),
          (else_try), #we assume ":give_back_fiefs" also returns patrols
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":town_lord"),
            (party_set_faction, ":party_no", ":old_kingdom"),
            (party_set_flags, ":party_no", pf_default_behavior,1),
          (try_end),
        (try_end),
        (try_begin),
          (gt, ":num_parties", 0),
          (faction_get_color, ":color", ":old_kingdom"),
          (assign, reg6, ":give_back_fiefs"),
          (display_log_message, "@Your soldiers patrolling {s51} {reg6?returned:disbanded} because you left the faction!", ":color"),
        (try_end),
      (try_end),
        ##diplomacy end
    ]),


    ("deactivate_player_faction",
    [
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
    (assign, "$players_kingdom", 0),
    (assign, "$players_oath_renounced_against_kingdom", 0),
    (assign, "$players_oath_renounced_given_center", 0),
    (assign, "$players_oath_renounced_begin_time", 0),
    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),

    (try_begin),
        (is_between, "$g_player_minister", companions_begin, companions_end),
        (assign, "$npc_to_rejoin_party", "$g_player_minister"),
    (try_end),
    (assign, "$g_player_minister", -1),

    (call_script, "script_add_notification_menu", "mnu_notification_player_faction_deactive", 0, 0),
    ]),


  #script_activate_player_faction
  # INPUT: arg1 = last_interaction_with_faction
  # OUTPUT: none

  #When a player convinces her husband to rebel
  #When a player proclaims herself queen
  #When a player seizes control of a center
  #When a player recruits a lord through intrigue
  #When a player
    ("activate_player_faction",
    [
    (store_script_param, ":liege", 1),

	#This moved to top, so that mnu_notification does not occur twice
	(try_begin),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(neg|is_between, ":liege", pretenders_begin, pretenders_end),
		(call_script, "script_add_notification_menu", "mnu_notification_player_faction_active", 0, 0),
		##diplomacy begin
		(call_script, "script_add_notification_menu", "mnu_dplmc_domestic_policy", 0, 0),
		##diplomacy end
	(try_end),


    (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_active),
    (faction_set_slot, "fac_player_supporters_faction", slot_faction_leader, ":liege"),

	(assign, ":original_kingdom", "$players_kingdom"),

	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_player_leave_faction", 0), #Ends quests, transfers control of centers
	(try_end),

	#Name faction
	(try_begin),
		(is_between, ":liege", active_npcs_begin, active_npcs_end),
		(store_faction_of_troop, ":liege_faction"),
		(is_between, ":liege_faction", npc_kingdoms_begin, npc_kingdoms_end),
		(faction_get_slot, ":adjective_string", ":liege_faction", slot_faction_adjective),
		(str_store_string, s1, ":adjective_string"),
		(faction_set_name, "fac_player_supporters_faction", "@{s1} Rebels"),
        #SB : opposite faction color
        (faction_get_color, ":color", ":liege_faction"),
        (store_sub, ":color", 0xFFFFFF, ":color"),#we get the opposite color
        (faction_set_color, "fac_player_supporters_faction", ":color"),
	(else_try),
		(str_store_troop_name, s2, ":liege"),
        (str_store_string, s1, "str_s2s_rebellion"),
	(try_end),


    (assign, "$players_kingdom", "fac_player_supporters_faction"),
    (assign, "$g_player_banner_granted", 1),



	#Any oaths renounced?
	(try_begin),
		(is_between, ":original_kingdom", npc_kingdoms_begin, npc_kingdoms_end),

        (faction_get_slot, ":old_leader", ":original_kingdom", slot_faction_leader),
        (call_script, "script_add_log_entry", logent_renounced_allegiance,   "trp_player",  -1, ":old_leader", "$players_kingdom"),

        #Initializing renounce war variables
        (assign, "$players_oath_renounced_against_kingdom", ":original_kingdom"),
        (assign, "$players_oath_renounced_given_center", 0),
        (store_current_hours, "$players_oath_renounced_begin_time"),

        (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":cur_center_faction", ":cur_center"),
          (party_set_slot, ":cur_center", slot_center_faction_when_oath_renounced, ":cur_center_faction"),
        (try_end),
        (party_set_slot, "$g_center_to_give_to_player", slot_center_faction_when_oath_renounced, "$players_oath_renounced_against_kingdom"),

		(store_relation, ":relation", ":original_kingdom", "fac_player_supporters_faction"),
		(ge, ":relation", 0),
		(call_script, "script_diplomacy_start_war_between_kingdoms", ":original_kingdom", "fac_player_supporters_faction", 1),
	(try_end),


	(try_begin),
		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
	    (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":spouse"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 2"),
		(try_end),

	    (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "fac_player_supporters_faction"),
	(try_end),


    #(call_script, "script_store_average_center_value_per_faction"),
    (call_script, "script_update_all_notes"),
	(assign, "$g_recalculate_ais", 1),

    ]),



  #script_agent_reassign_team
  # INPUT: faction_no
  # OUTPUT: none
  ("update_faction_notes",
    [
      (store_script_param, ":faction_no", 1),

      (try_begin),
        (this_or_next|faction_slot_eq, ":faction_no", slot_faction_state, sfs_inactive),
        (eq, ":faction_no", "fac_player_faction"),
        (faction_set_note_available, ":faction_no", 0),
      (else_try),
        (faction_set_note_available, ":faction_no", 1),
      (try_end),
##
##	(try_begin),
##		(eq, 2, 1),
##		(str_store_faction_name, s14, ":faction_no"),
##		(assign, reg4, "$temp"),
##		(display_message, "str_updating_faction_notes_for_s14_temp_=_reg4"),
##	(try_end),
##
##    (try_begin),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
##       (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
##       (str_store_faction_name, s5, ":faction_no"),
##       (str_store_troop_name_link, s6, ":faction_leader"),
##       (assign, ":num_centers", 0),
##       (str_store_string, s8, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (store_faction_of_party, ":center_faction", ":cur_center"),
##         (eq, ":center_faction", ":faction_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s8, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (assign, ":num_members", 0),
##       (str_store_string, s10, "@noone"),
##       (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
##         (assign, ":cur_troop", ":loop_var"),
##         (try_begin),
##           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
##           (assign, ":cur_troop", "trp_player"),
##           (assign, ":troop_faction", "$players_kingdom"),
##         (else_try),
##           (store_troop_faction, ":troop_faction", ":cur_troop"),
##         (try_end),
##         (eq, ":troop_faction", ":faction_no"),
##         (neq, ":cur_troop", ":faction_leader"),
##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##         (try_begin),
##           (eq, ":num_members", 0),
##           (str_store_troop_name_link, s10, ":cur_troop"),
##         (else_try),
##           (eq, ":num_members", 1),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{s9} and {s10}"),
##         (else_try),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{!}{s9}, {s10}"),
##         (try_end),
##         (val_add, ":num_members", 1),
##       (try_end),
##
##	   #wars
##       (str_store_string, s12, "@noone"),
###       (assign, ":num_enemies", 0),
###       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
###         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
###         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
###         (lt, ":cur_relation", 0),
###         (try_begin),
###           (eq, ":num_enemies", 0),
###           (str_store_faction_name_link, s12, ":cur_faction"),
###         (else_try),
###           (eq, ":num_enemies", 1),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11} and the {s12}"),
###         (else_try),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11}, the {s12}"),
###         (try_end),
###         (val_add, ":num_enemies", 1),
###       (try_end),
##
##       (str_store_string, s21, "str_foreign_relations__"),
##
##	   #other foreign relations
##       (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
##         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
##		 (neq, ":faction_no", ":cur_faction"),
##		 (str_store_faction_name_link, s14, ":cur_faction"),
##         (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_no", ":cur_faction"),
##		 (assign, ":diplomatic_status", reg0),
##		 (assign, reg2, reg1), #length of events
##		 (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":faction_no"),
##		 (assign, ":reverse_diplomatic_status", reg0),
##
##
##		 (try_begin),
##			(eq, ":diplomatic_status", -2),
##			(str_store_string, s21, "str_s21__the_s5_is_at_war_with_the_s14"),
##
##			(store_add, ":slot_war_damage_inflicted", ":cur_faction", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
##			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot_war_damage_inflicted"),
##			(store_mul, ":war_damage_inflicted_x_2", ":war_damage_inflicted", 2),
##
##			(store_add, ":slot_war_damage_suffered", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_suffered", kingdoms_begin),
##			(faction_get_slot, ":war_damage_suffered", ":cur_faction", ":slot_war_damage_suffered"),
##			(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
##
##			(try_begin),
##				(gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),
##				(str_store_string, s21, "str_s21_the_s5_has_had_the_upper_hand_in_the_fighting"),
##			(else_try),
##				(gt, ":war_damage_suffered", ":war_damage_inflicted_x_2"),
##				(str_store_string, s21, "@{s21}. The {s14} has gotten the worst of the fighting."),
##			(else_try),
##				(gt, ":war_damage_inflicted", 100),
##				(gt, ":war_damage_inflicted", 100),
##				(str_store_string, s21, "str_s21_the_fighting_has_gone_on_for_some_time_and_the_war_may_end_soon_with_a_truce"),
##			(else_try),
##				(str_store_string, s21, "str_s21_the_fighting_has_begun_relatively_recently_and_the_war_may_continue_for_some_time"),
##			(try_end),
##
##			(try_begin),
##				(eq, "$cheat_mode", 1),
##				(assign, reg4, ":war_damage_inflicted"),
##				(assign, reg5, ":war_damage_suffered"),
##				(str_store_string, s21, "str_s21_reg4reg5"),
##			(try_end),
##		 (else_try),
##			(eq, ":diplomatic_status", 1),
##			(str_clear, s18),
##
##			(try_begin),
##				(neq, reg0, 1),
##				(str_store_string, s18, "str__however_the_truce_is_no_longer_binding_on_the_s14"),
##			(try_end),
##			(str_store_string, s21, "str_s21__the_s5_is_bound_by_truce_not_to_attack_the_s14s18_the_truce_will_expire_in_reg1_days"),
##
##		 (else_try),
##			(eq, ":diplomatic_status", -1),
##			(str_store_string, s21, "str_s21__the_s5_has_recently_suffered_provocation_by_subjects_of_the_s14_and_there_is_a_risk_of_war"),
##		 (else_try),
##			(eq, ":diplomatic_status", 0),
##			(str_store_string, s21, "str_s21__the_s5_has_no_outstanding_issues_with_the_s14"),
##		 (try_end),
##
##
##		 (try_begin),
##			(eq, ":reverse_diplomatic_status", -1),
##			(str_store_string, s21, "str_s21_the_s14_was_recently_provoked_by_subjects_of_the_s5_and_there_is_a_risk_of_war_"),
##		 (try_end),
##
##		 (try_begin),
##			(eq, "$cheat_mode", 1),
##			(call_script, "script_diplomacy_faction_assess_faction_to_s14", ":faction_no", ":cur_faction", -1),
##			(str_store_string, s21, "str_s21_cheat_mode_assessment_s14_"),
##	     (try_end),
##	  (try_end),
##
##
##	  (add_faction_note_from_sreg, ":faction_no", 0, "str_the_s5_is_ruled_by_s6_it_occupies_s8_its_vassals_are_s10__s21", 0),
##
##
##
##    (else_try),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
##       (str_store_faction_name, s5, ":faction_no"),
##       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} has been defeated!", 0),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (else_try),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 0, s1, 0),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (try_end),
##
##    (try_begin),
##       (is_between, ":faction_no", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
##    (else_try),
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
##    (try_end),
     ]),

  ("update_faction_political_notes",
    [(store_script_param, ":faction_no", 1),

	(call_script, "script_evaluate_realm_stability", ":faction_no"),
    (add_faction_note_from_sreg, ":faction_no", 2, "str_instability_reg0_of_lords_are_disgruntled_reg1_are_restless", 0),
	]),



  #script_update_faction_traveler_notes
  # INPUT: faction_no
  # OUTPUT: none
  ("update_faction_traveler_notes",
    [(store_script_param, ":faction_no", 1),
     (assign, ":total_men", 0),
     (try_for_parties, ":cur_party"),
       (store_faction_of_party, ":center_faction", ":cur_party"),
       (eq, ":center_faction", ":faction_no"),
       (party_get_num_companions, ":num_men", ":cur_party"),
       (val_add, ":total_men", ":num_men"),
     (try_end),
     (str_store_faction_name, s5, ":faction_no"),
     (assign, reg1, ":total_men"),
     (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
     ]),


  #script_update_troop_notes
("update_troop_political_notes",
      [
		(store_script_param, ":troop_no", 1),
		(try_begin),
		    (str_clear, s47),

			(store_faction_of_troop, ":troop_faction", ":troop_no"),

		    (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),

		    (str_clear, s40),
		    (assign, ":logged_a_rivalry", 0),
		    (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
				(lt, reg0, -10),

		   		(str_store_troop_name_link, s39, ":kingdom_hero"),
				(try_begin),
					(eq, ":logged_a_rivalry", 0),
					(str_store_string, s40, "str_s39_rival"),
					(assign, ":logged_a_rivalry", 1),
				(else_try),
					(str_store_string, s41, "str_s40"),
					(str_store_string, s40, "str_s41_s39_rival"),
				(try_end),

		    (try_end),

		    (str_clear, s46),
		    (try_begin),
				(ge, "$cheat_mode", 1),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(str_store_string, s46, "str_reputation_cheat_mode_only_martial_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
					(str_store_string, s46, "str_reputation_cheat_mode_only_debauched_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_pitiless_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
					(str_store_string, s46, "str_reputation_cheat_mode_only_calculating_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
					(str_store_string, s46, "str_reputation_cheat_mode_only_quarrelsome_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(str_store_string, s46, "str_reputation_cheat_mode_only_goodnatured_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(str_store_string, s46, "str_reputation_cheat_mode_only_upstanding_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(str_store_string, s46, "str_reputation_cheat_mode_only_conventional_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_adventurous),
					(str_store_string, s46, "str_reputation_cheat_mode_only_adventurous_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_otherworldly),
					(str_store_string, s46, "str_reputation_cheat_mode_only_romantic_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(str_store_string, s46, "str_reputation_cheat_mode_only_moralist_"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_ambitious),
					(str_store_string, s46, "str_reputation_cheat_mode_only_ambitious_"),
				(else_try),
					(troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
					(str_store_string, s46, "str_reputation_cheat_mode_only_reg11_"),
				(try_end),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
						(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
						(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
						(str_store_troop_name_link, s39, ":love_interest"),
						(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
						(str_store_string, s2, "str_love_interest"),
						(try_begin),
							(troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
							(str_store_string, s2, "str_betrothed"),
						(try_end),
						(str_store_string, s40, "str_s40_s39_s2_reg0"),
					(try_end),
				(try_end),

		    (try_end),

		    (str_store_string, s45, "str_other_relations_s40_"),

		    (str_clear, s44),
		    (try_begin),
				(neq, ":troop_no", ":faction_leader"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
				(str_store_string, s44, "str_relation_with_liege_reg0_"),
		    (try_end),

			(str_clear, s48),

		    (try_begin),
				(eq, "$cheat_mode", 1),
				(store_current_hours, ":hours"),
				(gt, ":hours", 0),
#				(display_message, "@{!}Updating political factors"),
				(call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
				(str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
			(try_end),
			(str_store_string, s47, "str_s46s45s44s48"),

			(add_troop_note_from_sreg, ":troop_no", 3, "str_political_details_s47_", 1),

		(try_end),
    ]),

  #script_update_center_notes

  # script_get_culture_with_party_faction_for_music
  # Input: arg1 = party_no
  # Output: reg0 = culture
  ("get_culture_with_party_faction_for_music",
    [
      (store_script_param, ":party_no", 1),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":faction_no", "fac_player_faction"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":faction_no", "$players_kingdom"),
      (try_end),
      (try_begin),
        (is_between, ":party_no", centers_begin, centers_end),
        (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
        (neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (party_get_slot, ":faction_no", ":party_no", slot_center_original_faction),
      (try_end),
      (call_script, "script_get_culture_with_faction_for_music", ":faction_no"),
     ]),

  # script_get_culture_with_faction_for_music
  # Input: arg1 = party_no
  # Output: reg0 = culture
  ("get_culture_with_faction_for_music",
    [
      (store_script_param, ":faction_no", 1),
      (try_begin),
        (eq, ":faction_no", "fac_kingdom_1"),
        (assign, ":result", mtf_culture_1),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_2"),
        (assign, ":result", mtf_culture_2),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_3"),
        (assign, ":result", mtf_culture_3),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_4"),
        (assign, ":result", mtf_culture_4),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_5"),
        (assign, ":result", mtf_culture_5),
      (else_try),
        (eq, ":faction_no", "fac_kingdom_6"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (this_or_next|eq, ":faction_no", "fac_outlaws"),
        (this_or_next|eq, ":faction_no", "fac_peasant_rebels"),
        (this_or_next|eq, ":faction_no", "fac_deserters"),
        (this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
        (eq, ":faction_no", "fac_forest_bandits"),
        (assign, ":result", mtf_culture_6),
      (else_try),
        (assign, ":result", 0), #no culture, including player with no bindings to another kingdom
      (try_end),
      (assign, reg0, ":result"),
     ]),

  # script_music_set_situation_with_culture
#fairly expensive in terms of CPU
  ("evaluate_realm_stability",

    [
	(store_script_param, ":realm", 1),

	(assign, ":total_lords", 0),
	(assign, ":total_restless_lords", 0),
	(assign, ":total_disgruntled_lords", 0),

	(faction_get_slot, ":liege", ":realm", slot_faction_leader),

	(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_troop_faction, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":realm"),
		(val_add, ":total_lords", 1),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord", ":liege"),
		(try_begin),
			(le, reg3, -10),
			(val_add, ":total_disgruntled_lords", 1),
		(else_try),
			(le, reg3, 10),
			(val_add, ":total_restless_lords", 1),
		(try_end),
	(try_end),

	(try_begin),
		(gt, ":total_lords", 0),
		(store_mul, ":instability_quotient", ":total_disgruntled_lords", 100),
		(val_div, ":instability_quotient", ":total_lords"),

		(store_mul, ":restless_quotient", ":total_restless_lords", 100),
		(val_div, ":restless_quotient", ":total_lords"),

		(store_mul, ":combined_quotient", ":instability_quotient", 2),
		(val_add, ":combined_quotient", ":restless_quotient"),
		(faction_set_slot, ":realm", slot_faction_instability, ":combined_quotient"),

		(assign, reg0, ":instability_quotient"),
		# (assign, reg1, ":restless_quotient"),
		(assign, reg1, ":restless_quotient"),
	(else_try),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s1, ":realm"),
			(display_message, "str_s1_has_no_lords"),
		(try_end),
		(assign, reg0, 0),
		(assign, reg1, 0),
	(try_end),

	]),



#lord recruitment scripts end

#called from game_event_simulate_battle
#Includes a number of consequences that follow on battles, mostly affecting relations between different NPCs
#This only fires from complete victories
  ("battle_political_consequences",
    [
	(store_script_param, ":defeated_party", 1),
	(store_script_param, ":winner_party", 2),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(str_store_party_name, s4, ":winner_party"),
		(str_store_party_name, s5, ":defeated_party"),
		(display_message, "str_do_political_consequences_for_s4_victory_over_s5"),
	(try_end),

	(store_faction_of_party, ":winner_faction", ":winner_party"),
	(try_begin),
		(eq, ":winner_party", "p_main_party"),
		(assign, ":winner_faction", "$players_kingdom"),
	(try_end),

	(party_get_template_id, ":defeated_party_template", ":defeated_party"),

	#did the battle involve travellers?
	(try_begin),
		(this_or_next|eq, ":defeated_party_template", "pt_village_farmers"),
			(eq, ":defeated_party_template", "pt_kingdom_caravan_party"),


		(party_get_slot, ":destination", ":defeated_party", slot_party_ai_object),
		(party_get_slot, ":origin", ":defeated_party", slot_party_last_traded_center),

        (call_script, "script_add_log_entry", logent_traveller_attacked, ":winner_party",  ":origin", ":destination", ":winner_faction"),

		(try_begin),
			(eq, "$cheat_mode", 2),
			(neg|is_between, ":winner_faction", kingdoms_begin, kingdoms_end),
			(str_store_string, s65, "str_bandits_attacked_a_party_on_the_roads_so_a_bounty_is_probably_available"),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),

			(str_store_party_name, s15, ":origin"),
			(str_store_party_name, s16, ":destination"),
			(display_message, "str_travellers_attacked_on_road_from_s15_to_s16"),
		(try_end),


		#by logging the faction and the party, we can verify that the party number is unlikely to have been reassigned - or at any rate, that the factions have not changed
	(try_end),

	#winner consequences:
	#1)   leader improves relations with other leaders
	#2)  Player given credit for victory if the victorious party is following the player's advice
	(try_begin),
		(party_get_template_id, ":winner_party_template", ":winner_party"),
		(eq, ":winner_party_template", "pt_kingdom_hero_party"),
		(neq, ":winner_party", "p_main_party"),
		#Do not do for player party, as is included in post-battle dialogs

		(party_stack_get_troop_id, ":winner_leader", ":winner_party", 0),
		##diplomacy start+ Support additional types
		(troop_is_hero, ":winner_leader"),
		(this_or_next|troop_slot_eq, ":winner_leader", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":winner_leader", active_npcs_begin, active_npcs_end),

		(store_faction_of_party, ":winner_faction", ":winner_party"),

		(party_collect_attachments_to_party, ":winner_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
	    ##diplomacy start+ support promoted kingdom ladies
	    (is_between, ":cur_troop_id", heroes_begin, heroes_end),
	    (this_or_next|troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),
	    ##diplomacy end+
            (is_between, ":cur_troop_id", active_npcs_begin, active_npcs_end),

			(try_begin),
				(troop_get_slot, ":winner_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":winner_lord_party"),
				(call_script, "script_cf_party_under_player_suggestion", ":winner_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_succeeded, "trp_player", -1, ":cur_troop_id", -1),
			(try_end),


			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),
			(eq, ":troop_faction", ":winner_faction"),
			(neq, ":cur_troop_id", ":winner_leader"),

			(try_begin),
				(eq, "$cheat_mode", 4),
				(str_store_troop_name, s15, ":cur_troop_id"),
				(str_store_troop_name, s16, ":winner_leader"),
				(display_message, "str_s15_shares_joy_of_victory_with_s16"),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", 3),
			(val_add, "$total_battle_ally_changes", 3),

		(try_end),
		(party_clear, "p_temp_party_2"),
	(try_end),

	#consequences of defeat,
	#1) -1 relation with lord per lord, plus -15 if there is an incompatible marshal
	#2)  losers under player suggestion blame the player
	#3) Some losers resent the victor lord
	#4) Possible quarrels over defeat
	(try_begin),
		(party_collect_attachments_to_party, ":defeated_party", "p_temp_party_2"),
        (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),

		(try_begin),
			(gt, "$marshall_defeated_in_battle", 0),
			(str_store_troop_name, s15, "$marshall_defeated_in_battle"),
			(store_faction_of_troop, ":defeated_marshall_faction", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_faction_marshall_s15_involved_in_defeat"),
            (try_end),
		(else_try),
			(eq, "$marshall_defeated_in_battle", "trp_player"),
			(eq, ":defeated_party", "p_main_party"),
			(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_player_faction_marshall_involved_in_defeat"),
            (try_end),
		(else_try),
			(assign, "$marshall_defeated_in_battle", -1),
		(try_end),

		(try_for_range, ":troop_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop_id", "p_temp_party_2", ":troop_iterator"),
            (troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),

			(try_begin), #is party under suggestion?
				(troop_get_slot, ":defeated_lord_party", ":cur_troop_id", slot_troop_leaded_party),
				(party_is_active, ":defeated_lord_party"),

				#is party under suggestion?
				(call_script, "script_cf_party_under_player_suggestion", ":defeated_lord_party"),
				(call_script, "script_add_log_entry", logent_player_suggestion_failed, "trp_player", -1, ":cur_troop_id", -1),
			(try_end),


			(store_faction_of_troop, ":troop_faction", ":cur_troop_id"),

			(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
			(neq, ":cur_troop_id", ":faction_leader"),

			#Lose one point relation with liege
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s14, ":cur_troop_id"),
				(str_store_faction_name, s15, ":troop_faction"),

				(display_message, "str_s14_of_s15_defeated_in_battle_loses_one_point_relation_with_liege"),
			(try_end),

			(try_begin),
				(this_or_next|neq, ":faction_leader", "trp_player"), #if leader is zero at beginning of game. I'm not entirely sure how this could happen...
					(eq, "$players_kingdom", ":troop_faction"),

				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -1),
				(val_add, "$total_battle_ally_changes", -1),
			(try_end),


			(call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":troop_faction", 10),


			(try_begin),
				(this_or_next|is_between, ":winner_leader", active_npcs_begin, active_npcs_end),
					(eq, ":winner_leader", "trp_player"),

				(this_or_next|neq, ":winner_leader", "trp_player"), #prevents winner leader being zero, for whatever reason
					(eq, ":winner_party", "p_main_party"),

				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_quarrelsome),
				(this_or_next|troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_selfrighteous),
					(troop_slot_eq, ":cur_troop_id", slot_lord_reputation_type, lrep_debauched),

				(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":winner_leader", -1),
				(val_add, "$total_battle_enemy_changes", -1),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s14, ":cur_troop_id"),
					(str_store_troop_name, s15, ":winner_leader"),

					(display_message, "str_s14_defeated_in_battle_by_s15_loses_one_point_relation"),
				(try_end),


			(try_end),

			(gt, "$marshall_defeated_in_battle", -1),
			(eq, ":troop_faction", ":defeated_marshall_faction"),
			(str_store_troop_name, s14, ":cur_troop_id"),

			(call_script, "script_cf_test_lord_incompatibility_to_s17", ":cur_troop_id", "$marshall_defeated_in_battle"),
            (try_begin),
                (eq, "$cheat_mode", 1),
			    (display_message, "str_s14_blames_s15_for_defeat"),
            (try_end),

			(call_script, "script_add_log_entry", logent_lord_blames_defeat, ":cur_troop_id", "$marshall_defeated_in_battle", ":faction_leader", ":winner_faction"),

			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", ":faction_leader", -15),
			(val_add, "$total_battle_ally_changes", -15),

			(neq, "$marshall_defeated_in_battle", ":faction_leader"),
			(call_script, "script_troop_change_relation_with_troop", ":cur_troop_id", "$marshall_defeated_in_battle", -15),
			(val_add, "$total_battle_ally_changes", -15),

		(try_end),

		(party_clear, "p_temp_party_2"),
	(try_end),
	]),

    #SB : possibly lower controversy of attacker npc?
    ("faction_inflict_war_damage_on_faction",
    [
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	(store_script_param, ":amount", 3),


	(store_add, ":slot_war_damage", ":target_faction", slot_faction_war_damage_inflicted_on_factions_begin),
	(val_sub, ":slot_war_damage", kingdoms_begin),
	##diplomacy start+ Due to aberrant behavior, non-standard kingdoms
	##like fac_commoners can end up with parties on the map, and possibly
	##could end up inflicting or receiving war damage.  Guard against this.
	(try_begin),
	(is_between, ":slot_war_damage", slot_faction_war_damage_inflicted_on_factions_begin, slot_faction_war_damage_inflicted_on_factions_end),
	(gt, ":actor_faction", 0),
	##diplomacy end+
	(faction_get_slot, ":cur_war_damage", ":actor_faction", ":slot_war_damage"),

	(val_add, ":cur_war_damage", ":amount"),
	(faction_set_slot, ":actor_faction", ":slot_war_damage", ":cur_war_damage"),
	##diplomacy start+ Close added if-statement
	(else_try),
	   #For use in cheat-mode below
	   (assign, ":cur_war_damage", 0),
	(try_end),
	##diplomacy end+


	(try_begin),
	  (ge, "$cheat_mode", 1),
	  (str_store_faction_name, s4, ":actor_faction"),
	  (str_store_faction_name, s5, ":target_faction"),
	  (assign, reg3, ":cur_war_damage"),
	  (assign, reg4, ":amount"),
	  (display_message, "@{!}{s4} inflicts {reg4} damage on {s5}, raising total inflicted to {reg3}"),
	(try_end),


	(faction_get_slot, ":faction_marshal", ":target_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(gt, ":amount", 0),

		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_add, ":controversy", ":amount"),
		(val_min, ":controversy", 100),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage raises {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),

	(faction_get_slot, ":faction_marshal", ":actor_faction", slot_faction_marshall),
	(try_begin),
		(ge, ":faction_marshal", 0),
		(val_div, ":amount", 3),
		(gt, ":amount", 0),


		(troop_get_slot, ":controversy", ":faction_marshal", slot_troop_controversy),
		(val_sub, ":controversy", ":amount"),
		(val_max, ":controversy", 0),
		(troop_set_slot, ":faction_marshal", slot_troop_controversy, ":controversy"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":faction_marshal"),
			(assign, reg4, ":amount"),
			(assign, reg5, ":controversy"),
			(display_message, "@{!}War damage lowers {s4}'s controversy by {reg4} to {reg5}"),
		(try_end),
	(try_end),



	]),

    ("calculate_troop_political_factors_for_liege",
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":liege", 2),

	(troop_get_slot, ":lord_reputation", ":troop", slot_lord_reputation_type),

	##diplomacy start+ Work correctly in certain situations where this can be called w/o a liege.
	##OLD:
	#(store_faction_of_troop, ":faction", ":liege"),
	##NEW:
	(try_begin),
	   (eq, ":liege", "trp_player"),
	   (assign, ":faction", "fac_player_supporters_faction"),
	   (try_begin),
	     #Handle "player is co-ruler of NPC faction"
	     (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	     (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	     (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	     (assign, ":faction", "$players_kingdom"),
	     (faction_get_slot, reg0, ":faction", slot_faction_leader),
	     (gt, reg0, 0),
	     (assign, ":liege", reg0),
	   (try_end),
	(else_try),
	   #Ordinary case
	   (ge, ":liege", 0),
	   (store_faction_of_troop, ":faction", ":liege"),
	(else_try),
	   (store_faction_of_troop, reg0, ":troop"),
	   (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	   (assign, ":faction", reg0),
	(else_try),
	   (assign, ":faction", kingdoms_end),
	   (try_for_range, reg0, kingdoms_begin, ":faction"),
	      (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	      (assign, ":faction", reg0),
	   (try_end),
	   (neg|is_between, ":faction", kingdoms_begin, kingdoms_end),
	   (assign, ":faction", "fac_no_faction"),
	(try_end),
	##diplomacy end+


	(try_begin),
		(eq, ":faction", "fac_player_faction"),
		(assign, ":faction", "fac_player_supporters_faction"),
	(try_end),

	(assign, ":liege_is_undeclared_rebel", 0),
	(try_begin),
		(neg|faction_slot_eq, ":faction", slot_faction_leader, ":liege"),
		#the liege is a rebel
		(assign, ":liege_is_undeclared_rebel", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
                        ##diplomacy start+ Guard against bad liege
                        (ge, ":liege", 0),
                        ##diplomacy end+
			(str_store_troop_name, s32, ":liege"),
			(display_message, "str_s32_is_undeclared_rebel"),
		(try_end),
	(try_end),

	(assign, ":result_for_material", 0),
	(assign, ":penalty_for_changing_sides", 0),



	#FACTOR 1 - MILITARY SECURITY
	(assign, ":result_for_security", 0),

	#find the lord's home
	(assign, ":base_center", -1),
	(try_begin),
		##diplomacy start+ add support for promoted kingdom ladies
		(is_between, ":troop", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":troop", active_npcs_begin, active_npcs_end),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":base_center", -1),
			(party_slot_eq, ":center", slot_town_lord, ":troop"),
			(assign, ":base_center", ":center"),
		(try_end),
	(try_end),

	(assign, ":faction_has_base", 0),

	#add up all other centers for the security value
	(try_for_range, ":center", centers_begin, centers_end),
		(neq, ":center", ":base_center"),
		(gt, ":base_center", 0),

		(try_begin),
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":weight", 9000),
		(else_try),
			(is_between, ":center", castles_begin, castles_end),
			(assign, ":weight", 6000),
		(else_try),
			(assign, ":weight", 1000),
		(try_end),

		(store_distance_to_party_from_party, ":distance", ":base_center", ":center"),
		(val_add, ":distance", 10),
		(val_div, ":weight", ":distance"),
		(val_div, ":weight", ":distance"),

		(store_faction_of_party, ":center_faction", ":center"),

		(try_begin),
			(eq, ":center_faction", ":faction"),

			(assign, ":faction_has_base", 1),
			(val_add, ":result_for_security", ":weight"),
		(else_try),
			(neq, ":center_faction", ":faction"),
			(store_relation, ":center_relation", ":center_faction", ":faction"),

			(try_begin), #potentially hostile center
				(this_or_next|eq, ":liege_is_undeclared_rebel", 1),
					(lt, ":center_relation", 0),
				(val_div, ":weight", 2),
			(else_try), #neutral center
				(val_div, ":weight", 4),
			(try_end),

			(val_sub, ":result_for_security", ":weight"),
		(try_end),
	(try_end),


	#if a faction controls no other centers, then there is a small bonus
	(try_begin),
		(eq, ":faction_has_base", 0),
		(val_add, ":result_for_security", 20),
		(try_begin),
			(eq, "$cheat_mode", 2),
			(display_message, "str_small_bonus_for_no_base"),
		(try_end),
	(try_end),
	(val_clamp, ":result_for_security", -100, 100),


	(assign, ":result_for_security_weighted", ":result_for_security"),
	##diplomacy start+
   #ADDED TO THIS, SEE BELOW
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_cunning),
	#	(val_mul, ":result_for_security_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_martial),
	#	(val_div, ":result_for_security_weighted", 2),
	#(try_end),
	#
    ##Use companion morality type "tmt_aristocratic" as a synonym/antonym for bold
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_aristocratic),
	(assign, ":lord_tmt_aristocratic", reg0),
	(try_begin),
		(lt, ":lord_tmt_aristocratic", 1),
		(this_or_next|lt, ":lord_tmt_aristocratic", 0),
		(eq, ":lord_reputation", lrep_cunning),
		(val_mul, ":result_for_security_weighted", 2),
	(else_try),
		(ge, ":lord_tmt_aristocratic", 0),
		(this_or_next|ge, ":lord_tmt_aristocratic", 1),
		(eq, ":lord_reputation", lrep_martial),
		(val_div, ":result_for_security_weighted", 2),
	(try_end),
	##diplomacy end+

	#FACTOR 2 - INTERNAL FACTION POLITICS
	#this is a calculation of how much influence the lord believes he will have in each faction
	(assign, ":result_for_political", 0),

    (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
        (assign, ":kingdom_hero", ":loop_var"),
	##diplomacy start+ Skip what follows when there is no liege
	(ge, ":liege", 0),
	##diplomacy end+

		(this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|eq, ":kingdom_hero", "trp_kingdom_heroes_including_player_begin"),
			(is_between, ":kingdom_hero", pretenders_begin, pretenders_end),

		(store_faction_of_troop, ":kingdom_hero_faction", ":kingdom_hero"),

        (try_begin),
            (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
            (assign, ":kingdom_hero", "trp_player"),
			(assign, ":kingdom_hero_faction", "$players_kingdom"),
			(try_begin), #do not count player relation if the player is trying to suborn the character. this has the slight potential for a miscalculation, if the script is called from outside dialogs and $g_talk_troop has not been reset
				(eq, "$g_talk_troop", ":troop"),
				(store_faction_of_troop, ":cur_faction", ":troop"),
				(eq, ":cur_faction", ":faction"),
				(assign, ":kingdom_hero_faction", 0),
			(try_end),
		(try_end),

		(eq, ":kingdom_hero_faction", ":faction"),
		(neg|faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
		(neq, ":liege_is_undeclared_rebel", 1),
		(neg|is_between, ":kingdom_hero", pretenders_begin, pretenders_end),


		(call_script, "script_troop_get_relation_with_troop", ":troop", ":kingdom_hero"),
		(assign, ":troop_rel_w_hero", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":kingdom_hero", ":liege"),
		(assign, ":hero_rel_w_liege", reg0),

		(store_mul, ":lord_political_weight", ":troop_rel_w_hero", ":hero_rel_w_liege"),
		(val_div, ":lord_political_weight", 100),

		(try_begin),
			(eq, "$cheat_mode", 2), #disabled
			(eq, "$g_talk_troop", ":troop"),
			(str_store_faction_name, s20, ":kingdom_hero_faction"),
			(str_store_troop_name, s15, ":kingdom_hero"),
			(assign, reg15, ":lord_political_weight"),
			(display_message, "str_s15_considered_member_of_faction_s20_weight_of_reg15"),
		(try_end),

		(val_add, ":result_for_political", ":lord_political_weight"),
	(try_end),

	(val_clamp, ":result_for_political", -100, 101), #lords portion represents half

	(try_begin),
		##diplomacy start+ When there isn't a liege, use 0
		(assign, ":liege_relation", 0),
		(ge, ":liege", 0),
		##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":troop", ":liege"),
		(assign, ":liege_relation", reg0),
		(val_add, ":result_for_political", ":liege_relation"),
	(try_end),

	(val_div, ":result_for_political", 2),

	(val_clamp, ":result_for_political", -100, 101), #liege portion represents half

	(assign, ":result_for_political_weighted", ":result_for_political"),

	(try_begin),
		(this_or_next|eq, ":lord_reputation", lrep_goodnatured),
			(eq, ":lord_reputation", lrep_quarrelsome),
		(val_mul, ":result_for_political_weighted", 2),
	(try_end),

	#FACTOR 3 - PROMISES AND OTHER ANTICIPATED GAINS
	#lord's calculation of anticipated gains
	(assign, ":result_for_material", 0),
	(assign, ":result_for_material_weighted", ":result_for_material"),


	#FACTOR 4 - IDEOLOGY
	#lord's calculation of ideological comfort
	(try_begin),
		#Originally, the argument section was not used for a non-player liege. Actually, it can be used
		(eq, 1, 0),
		(neq, ":liege", "trp_player"),
		(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
		(assign, ":argument_strength", 0),
		(assign, ":argument_appeal", 0),
		(assign, ":result_for_argument", 0),
	(else_try),	#only if the recruitment candidate is either the player, or a supported pretender
		(troop_get_slot, ":recruitment_argument", ":troop", slot_lord_recruitment_argument),

		(call_script, "script_rebellion_arguments", ":troop", ":recruitment_argument", ":liege"),
		(assign, ":argument_appeal", reg0),
		(assign, ":argument_strength", reg1),

		(store_add, ":result_for_argument", ":argument_appeal", ":argument_strength"),

		(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
		(try_begin),
			(gt, ":result_for_argument", 0),
			#make sure player is the one making the overture

			#if player has 0 persuasion, ":result_for_argument" will be multiplied by 3/10.
			(store_add, ":player_persuasion_skill_plus_5_mul_066", ":player_persuasion_skill", 5),
			(val_mul, ":player_persuasion_skill_plus_5_mul_066", 2),
			(val_div, ":player_persuasion_skill_plus_5_mul_066", 3),

			(val_mul, ":result_for_argument", ":player_persuasion_skill_plus_5_mul_066"),
			(val_div, ":result_for_argument", 10),
		(else_try),
			(lt, ":result_for_argument", 0),
			(store_sub, ":ten_minus_player_persuasion_skill", 10, ":player_persuasion_skill"),
			(val_mul, ":result_for_argument", ":ten_minus_player_persuasion_skill"),
			(val_div, ":result_for_argument", 10),
		(try_end),

		(try_begin),
			(neq, ":liege", "trp_player"),
			(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(val_div, ":argument_strength", 2),
			(val_div, ":argument_appeal", 2),
			(val_div, ":result_for_argument", 2),
		(try_end),

	(try_end),

#	(try_begin),
#		(eq, ":lord_reputation", lrep_cunning),
#		(val_div, ":result_for_ideological_weighted", 2),
#	(else_try),
#		(eq, ":lord_reputation", lrep_upstanding),
#		(val_mul, ":result_for_ideological_weighted", 2),
#	(try_end),


	#FACTOR 5 - PENALTY FOR CHANGING SIDES
	(try_begin), #no penalty for the incumbent
		(store_faction_of_troop, ":cur_faction", ":troop"),
		(eq, ":cur_faction", ":faction"),
		(assign, ":penalty_for_changing_sides", 0),
	(else_try), #penalty for the player
		(eq, ":liege", "trp_player"),
		(store_sub, ":penalty_for_changing_sides", 60, "$player_right_to_rule"),
	(else_try), #same culture, such as a pretender
		##diplomacy start+ skip when there is no liege
		(ge, ":liege", 0),
		##diplomacy end+
		(troop_get_slot, ":orig_faction_of_lord", ":troop", slot_troop_original_faction),
		(troop_get_slot, ":orig_faction_of_liege", ":liege", slot_troop_original_faction),
		(eq, ":orig_faction_of_lord", ":orig_faction_of_liege"),
		(assign, ":penalty_for_changing_sides", 10),
	##diplomacy start+
	#"same culture, such as a pretender" pt. 2
	(else_try),
		(troop_slot_eq, ":troop", slot_troop_original_faction, ":faction"),
		(assign, ":penalty_for_changing_sides", 10),
	##diplomacy end+
	(else_try), #a liege from a different culture
		(assign, ":penalty_for_changing_sides", 50),
	(try_end),
	(val_clamp, ":penalty_for_changing_sides", 0, 101),

	(assign, ":penalty_for_changing_sides_weighted", ":penalty_for_changing_sides"),
	##diplomacy start+
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_debauched),
	#	(val_div, ":penalty_for_changing_sides_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_upstanding),
	#	(val_mul, ":penalty_for_changing_sides_weighted", 2),
	#(try_end),
	#
	##Use companion morality type "tmt_honest" as a synonym/antonym for deal-keeping
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_honest),
	(assign, ":lord_tmt_honest", reg0),
	(try_begin),
		(this_or_next|lt, ":lord_tmt_honest", 0),
		(eq, ":lord_reputation", lrep_debauched),
		(val_div, ":penalty_for_changing_sides_weighted", 2),
	(else_try),
		(this_or_next|ge, ":lord_tmt_honest", 1),
		(eq, ":lord_reputation", lrep_upstanding),
		(val_mul, ":penalty_for_changing_sides_weighted", 2),
	(try_end),
	##diplomacy end+



	(assign, reg1, ":result_for_security"),
	(assign, reg2, ":result_for_security_weighted"),
	(assign, reg3, ":result_for_political"),
	(assign, reg4, ":result_for_political_weighted"),
	(assign, reg5, ":result_for_material"),
	(assign, reg6, ":result_for_material_weighted"),
	(assign, reg7, ":argument_strength"),
	(assign, reg17, ":argument_appeal"),

	(assign, reg8, ":result_for_argument"),
	(assign, reg9, ":penalty_for_changing_sides"),
	(assign, reg10, ":penalty_for_changing_sides_weighted"),


	(try_begin),
		(eq, "$cheat_mode", 1),
		(eq, "$g_talk_troop", ":troop"),
		(str_store_troop_name, s20, ":troop"),
		(str_store_faction_name, s21, ":faction"),
		##diplomacy start+
		##OLD:
		#(str_store_troop_name, s22, ":liege"),
		##NEW:
		(try_begin),
		  (gt, ":liege", -1),
		  (str_store_troop_name, s22, ":liege"),
		(else_try),
		  (str_store_string, s22, "str_noone"),
		(try_end),
		##diplomacy end+

		(display_message, "@{!}G_talk_troop {s20} evaluates being vassal to {s22} of {s21}"),

		(display_message, "str_base_result_for_security_reg1"),
		(display_message, "str_result_for_security_weighted_by_personality_reg2"),
		(display_message, "str_base_result_for_political_connections_reg3"),
		(display_message, "str_result_for_political_connections_weighted_by_personality_reg4"),
#		(display_message, "@{!}Result for anticipated_gains: {reg5}"),
#		(display_message, "@{!}Result for anticipated_gains weighted by personality: {reg6}"),

		(try_begin),
			(this_or_next|eq, ":liege", "trp_player"),
				(eq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(display_message, "str_result_for_argument_strength_reg7"),
			(display_message, "str_result_for_argument_appeal_reg17"),
			(display_message, "str_combined_result_for_argument_modified_by_persuasion_reg8"),
		(try_end),
		(display_message, "str_base_changing_sides_penalty_reg9"),
		(display_message, "str_changing_sides_penalty_weighted_by_personality_reg10"),
	(try_end),

	(store_add, ":total", ":result_for_security_weighted", ":result_for_political_weighted"),
	(val_add, ":total", ":result_for_material_weighted"),
	(val_add, ":total", ":result_for_argument"),
	(val_sub, ":total", ":penalty_for_changing_sides_weighted"),


	(assign, reg0, ":total"),

	(try_begin),
		(eq, "$cheat_mode", 2),
		(display_message, "@{!}DEBUG -- Analyzing lord allegiances, combined bonuses and penalties = {reg0}"),
		#(display_message, "str_combined_bonuses_and_penalties_=_reg0"),
	(try_end),
	]),



    ("appoint_faction_marshall",
    [
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":faction_marshall", 2),


    (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
    (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),

    (faction_set_slot, ":faction_no", slot_faction_marshall, ":faction_marshall"),

    (try_begin),
		(ge, ":old_marshall", 0),
		(troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
        (party_is_active, ":old_marshall_party"),
        (party_set_marshal, ":old_marshall_party", 0),
    (try_end),


    (try_begin),
      (ge, ":faction_marshall", 0),
	  (troop_get_slot, ":new_marshall_party", ":faction_marshall", slot_troop_leaded_party),
      (party_is_active, ":new_marshall_party"),
      (party_set_marshal,":new_marshall_party", 1),
    (try_end),


	(try_begin),
		(neq, ":faction_marshall", ":faction_leader"),
		(neq, ":faction_marshall", ":old_marshall"),
		##diplomacy start+ Support promoted kingdom ladies
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":faction_marshall", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(this_or_next|eq, ":faction_marshall", "trp_player"),
			(is_between, ":faction_marshall", active_npcs_begin, active_npcs_end),

		(this_or_next|neq, ":faction_no", "fac_player_supporters_faction"),
			(neg|check_quest_active, "qst_rebel_against_kingdom"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s15, ":faction_no"),
			(display_message, "str_checking_lord_reactions_in_s15"),
		(try_end),


		(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":faction_leader", 5),
		(val_add, "$total_promotion_changes", 5),

		##diplomacy start+
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
		(assign, ":player_standing_in_faction", reg0),
		#(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		#Support promoted kingdom ladies
		##OLD:
		#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		##NEW:
		(try_for_range, ":lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":lord_faction", ":lord"),
			(eq, ":lord_faction", ":faction_no"),

			(neq, ":lord", ":faction_marshall"),
			(neq, ":lord", ":faction_leader"),

			(call_script, "script_troop_get_relation_with_troop", ":faction_marshall", ":lord"),
#			(try_begin),
#				(eq, "$cheat_mode", 1),
#				(str_store_troop_name, s14, ":lord"),
#				(str_store_troop_name, s17, ":faction_marshall"),
#				(display_message, "@{!}{s14}'s relation with {s17} is {reg0}"),
#			(try_end),
			(store_sub, ":adjust_relations", reg0, 10),
			(val_div, ":adjust_relations", 15),
			##diplomacy start+
			#In some situtations the player can set the marshall freely even though he isn't the faction leader.
			(try_begin),
				(eq, ":faction_marshall", "trp_player"),
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				#Still allow a relation gain below if the lord had actively supported the player
				#(which doesn't happen now if the player is the ruler, but could).
				(val_min, ":adjust_relations", 0),
			(try_end),
			##diplomacy end+
			(neq, ":adjust_relations", 0),

			#Not negatively affected if they favored the lord
			(try_begin),
				(troop_slot_eq, ":lord", slot_troop_stance_on_faction_issue, ":faction_marshall"),
				(val_add, ":adjust_relations", 1),
				(val_max, ":adjust_relations", 0),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":adjust_relations"),
			(val_add, "$total_promotion_changes", ":adjust_relations"),

			(lt, ":adjust_relations", -2),
			(store_random_in_range, ":random", 1, 10),

			(val_add, ":adjust_relations", ":random"),

			(lt, ":adjust_relations", 0),

			(str_store_troop_name, s14, ":lord"),
			(str_store_troop_name, s15, ":faction_marshall"),

			(try_begin),
			##diplomacy start+ Show protest information for your own kingdom if you have a chancellor or are the ruler
				(ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_MEMBER),
				(this_or_next|ge, ":player_standing_in_faction", DPLMC_FACTION_STANDING_LEADER_SPOUSE),#<- via the minister, or just hearing about it
					(gt, "$g_player_chancellor", 0),#<- via your chancellor
				(neg|troop_slot_eq, ":lord", slot_troop_met, 0),
				(display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
			(else_try),
				(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":lord"),
				(this_or_next|gt, reg0, 0),
			##diplomacy end+
                (eq, "$cheat_mode", 1),
                (display_message, "str_s14_protests_the_appointment_of_s15_as_marshall"),
            (try_end),

			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", -10),
			(call_script, "script_troop_change_relation_with_troop", ":faction_marshall", ":lord", -5),
			(val_add, "$total_promotion_changes", -15),

			(call_script, "script_add_log_entry", logent_lord_protests_marshall_appointment, ":lord",  ":faction_marshall", ":faction_leader", "$g_encountered_party_faction"),

		(try_end),
	(try_end),

		]),

	#it might be easier to monitor whether prices are following an intuitive pattern if we separate production from consumption
("faction_conclude_feast",
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":venue", 2),

	(str_store_faction_name, s3, ":faction_no"),
	(str_store_party_name, s4, ":venue"),

    (try_begin),
        (eq, "$cheat_mode", 1),
	    (display_message, "str_s3_feast_concludes_at_s4"),
    (try_end),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),

	(party_set_slot, ":venue", slot_town_has_tournament, 0),

	#markspot

	(assign, ":nobility_in_faction", 0),
	(assign, ":nobility_in_attendance", 0),

	(try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
		(store_faction_of_troop, ":troop_faction", ":troop_no"),
		(eq, ":faction_no", ":troop_faction"),

		(val_add, ":nobility_in_faction", 1),

		#CHECK -- is the troop there?
		(troop_slot_eq, ":troop_no", slot_troop_cur_center, ":venue"),
		(val_add, ":nobility_in_attendance", 1),

		#check for marriages
		##diplomacy start+ enable marriages for non-kingdom ladies (for example, between two companions)
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_robber_knight),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_seneschal),
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
		##diplomacy end+
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":groom", ":troop_no", slot_troop_betrothed),
		(gt, ":groom", 0),

		(troop_get_slot, ":groom_party", ":groom", slot_troop_leaded_party),
		(party_is_active, ":groom_party"),
		(party_get_attached_to, ":groom_party_attached", ":groom_party"),
		(eq, ":groom_party_attached", ":venue"),

		(store_faction_of_troop, ":lady_faction", ":troop_no"),
		(store_faction_of_troop, ":groom_faction", ":groom"),

		(eq, ":groom_faction", ":lady_faction"),
		(eq, ":lady_faction", ":faction_no"),
		(store_current_hours, ":hours_since_betrothal"),
		(troop_get_slot, ":betrothal_time", ":troop_no", slot_troop_betrothal_time),
		(val_sub, ":hours_since_betrothal", ":betrothal_time"),
		(ge, ":hours_since_betrothal", 144), #6 days, should perhaps eventually be 29 days, or 696 yours

		(call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
		(assign, ":wedding_venue", reg1),
        ##diplomacy start+ be less picky about where to hold the feast as time goes on
		#(eq, ":venue", ":wedding_venue"),
		(neq, ":troop_no", "trp_player"),
		(neq, ":groom", "trp_player"),
		(party_get_slot, ":town_lord", ":venue", slot_town_lord),
		(assign, ":hold_the_wedding", 0),
		(try_begin),
			#after 6 days, will be held if the venue is the ideal one
			(eq, ":venue", ":wedding_venue"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 6 days, will be held if the bride's father/guardian holds a feast
			(ge, ":town_lord", 0),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_father, ":town_lord"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_mother, ":town_lord"),
			   (troop_slot_eq, ":troop_no", slot_troop_guardian, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 20 days, will be held if the bride, the groom, or either of their
			#parents hold a feast
			(ge, ":hours_since_betrothal", 24 * 20),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":troop_no", ":town_lord"),
			(this_or_next|eq, ":groom", ":town_lord"),
			(this_or_next|troop_slot_eq, ":groom", slot_troop_father, ":town_lord"),
			   (troop_slot_eq, ":groom", slot_troop_mother, ":town_lord"),
			(assign, ":hold_the_wedding", 1),
		(else_try),
			#after 60 days, if against all odds the engagement hasn't been called off,
			#the faction leader qualifies, as does any relative
			(ge, ":hours_since_betrothal", 24 * 60),
			(ge, ":town_lord", 0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":troop_no"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop",  ":town_lord", ":troop_no"),
			(assign, ":bride_relation", reg0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":town_lord", ":groom"),
			(this_or_next|faction_slot_eq, ":troop_faction", slot_faction_leader, ":town_lord"),
			(this_or_next|ge, reg0, 1),
				(ge, ":bride_relation", 1),
			(assign, ":hold_the_wedding", 1),
		(try_end),
		(eq, ":hold_the_wedding", 1),
		##diplomacy end+
		(call_script, "script_courtship_event_bride_marry_groom", ":troop_no", ":groom", 0), #parameters from dialog
	(try_end),


#ssss	(assign, ":placeholder_reminder_to_calculate_effect_for_player_feast", 1),



	(party_get_slot, ":feast_host", ":venue", slot_town_lord),
	(assign, ":quality_of_feast", 0),

	(try_begin),
		(check_quest_active, "qst_organize_feast"),
		(quest_slot_eq, "qst_organize_feast", slot_quest_target_center, ":venue"),
		(assign, ":feast_host", "trp_player"),

		(assign, ":total_guests", 400),

		(call_script, "script_succeed_quest", "qst_organize_feast"),
		(call_script, "script_end_quest", "qst_organize_feast"),

		(call_script, "script_internal_politics_rate_feast_to_s9", "trp_household_possessions", ":total_guests", "$players_kingdom", 1),
		(assign, ":quality_of_feast", reg0),
	(else_try),
		(assign, ":quality_of_feast", 60),
	(try_end),


	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":feast_host"),
		(assign, reg4, ":quality_of_feast"),
		(display_message, "@{!}DEBUG - {s4}'s feast has rating of {reg4}"),
	(try_end),


	(try_begin),
	  (ge, ":feast_host", 0),
	  (store_div, ":renown_boost", ":quality_of_feast", 3),
	  (call_script, "script_change_troop_renown", ":feast_host", ":renown_boost"),

	  (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
		(party_is_active, ":leaded_party"),
		(party_get_attached_to, ":leaded_party_attached", ":leaded_party"),
		(eq, ":leaded_party_attached", ":venue"),

		(assign, ":relation_booster", ":quality_of_feast"),
		(val_div, ":relation_booster", 20),

		(try_begin),
			(eq, ":feast_host", "trp_player"),
			(val_sub, ":relation_booster", 1),
			(val_max, ":relation_booster", 0),
		(try_end),
		(call_script, "script_troop_change_relation_with_troop", ":feast_host", ":troop_no", ":relation_booster"),
		(val_add, "$total_feast_changes", ":relation_booster"),
	  (try_end),
	(try_end),


	(assign, reg3, ":nobility_in_attendance"),
	(assign, reg4, ":nobility_in_faction"),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_attendance_reg3_nobles_out_of_reg4"),
	(try_end),
	]),

	("faction_follows_controversial_policy",
	[
	(store_script_param, ":faction_no", 1),
	(store_script_param, ":policy_type", 2),

	(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_faction_name, s3, ":faction_no"),
		(display_message, "str_calculating_effect_for_policy_for_s3"),

		(val_add, "$number_of_controversial_policy_decisions", 1),
	(try_end),

	(try_begin),
		(eq, ":policy_type", logent_policy_ruler_attacks_without_provocation),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -2),
		(assign, ":honor_change", -1),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_ignores_provocation),
		(assign, ":hawk_relation_effect", -3),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_declares_war_with_justification),
		(assign, ":hawk_relation_effect", 3),
		(assign, ":honorable_relation_effect", 1),
		(assign, ":honor_change", 0),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_breaks_truce),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", -3),
		(assign, ":honor_change", -5),

	(else_try),
		(eq, ":policy_type", logent_policy_ruler_makes_peace_too_soon),
		(assign, ":hawk_relation_effect", -5),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),

	##diplomacy start+ If none of the preceeding match, don't use random memory
	(else_try),
		(assign, ":hawk_relation_effect", 0),
		(assign, ":honorable_relation_effect", 0),
		(assign, ":honor_change", 0),
	##diplomacy end+
	(try_end),

	(try_begin),
		(eq, ":faction_leader", "trp_player"),
		(call_script, "script_change_player_honor", ":honor_change"),
	(try_end),

   ##diplomacy start+ add support for promoted kingdom ladies
	#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	(try_for_range, ":lord", heroes_begin, heroes_end),
	##diplomacy end+
		(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		(store_faction_of_troop, ":lord_faction", ":lord"),
		(eq, ":lord_faction", ":faction_no"),
		(neq, ":lord", ":faction_leader"),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_adventurous),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":hawk_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":hawk_relation_effect"),
		(try_end),

		(try_begin),
		   ##diplomacy start+ Add support for lady personality type
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_moralist),
			##diplomacy end+
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_martial),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_benefactor), #new for enfiefed commoners
			(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_custodian), #new for enfiefed commoners
				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_upstanding),
			(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":lord", ":honorable_relation_effect"),
			(val_add, "$total_policy_dispute_changes", ":honorable_relation_effect"),

		(try_end),

	(try_end),

	]),


	("faction_get_adjective_to_s10",
	[
	(store_script_param, ":faction_no", 1),

	(try_begin),
		(eq, ":faction_no", "fac_player_faction"),
		(assign, ":faction_no", "$players_kingdom"),
	(try_end),


	(try_begin),
		(eq, ":faction_no", "fac_player_supporters_faction"),
		(str_store_string, s10, "str_rebel"),
	(else_try),
		(this_or_next|eq, ":faction_no", "fac_outlaws"),
		(this_or_next|eq, ":faction_no", "fac_mountain_bandits"),
		(this_or_next|eq, ":faction_no", "fac_forest_bandits"),
			(eq, ":faction_no", "fac_deserters"),
		(str_store_string, s10, "str_bandit"),
	(else_try),
		(faction_get_slot, ":adjective_string", ":faction_no", slot_faction_adjective),
		(str_store_string, s10, ":adjective_string"),
	(try_end),
	]),

		#Not currently used (ie, it always fails)
  ("dplmc_get_prisoners_value_between_factions",
   [
       (store_script_param, ":faction_no_1", 1),
       (store_script_param, ":faction_no_2", 2),

       (assign, ":faction_no_1_value", 0),
       (assign, ":faction_no_2_value", 0),

       (try_for_parties, ":party_no"),
         (store_faction_of_party, ":party_faction", ":party_no"),
         (try_begin),
           (eq, ":party_faction", ":faction_no_1"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
           (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
             (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),

             (eq, ":cur_faction", ":faction_no_2"),
             (try_begin),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_calculate_ransom_amount_for_troop", ":cur_troop_id"),
               (val_add, ":faction_no_1_value", reg0),

               (try_begin),#debug
                 (eq, "$cheat_mode", 1),
                 (assign, reg0, ":faction_no_1_value"),
                 (display_message, "@{!}DEBUG : faction_no_1_value: {reg0}"),
               (try_end),

             (try_end),
           (try_end),
         (else_try),
           (eq, ":party_faction", ":faction_no_2"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
           (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
             (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":party_no", ":troop_iterator"),
             (store_troop_faction, ":cur_faction", ":cur_troop_id"),

             (eq, ":cur_faction", ":faction_no_1"),
             (try_begin),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_calculate_ransom_amount_for_troop", ":cur_troop_id"),
               (val_add, ":faction_no_2_value", reg0),

               (try_begin), #debug
                 (eq, "$cheat_mode", 1),
                 (assign, reg0, ":faction_no_2_value"),
                 (display_message, "@{!}DEBUG : faction_no_2_value: {reg0}"),
               (try_end),

             (try_end),
           (try_end),
         (try_end),
       (try_end),
       (store_sub, reg0, ":faction_no_1_value", ":faction_no_2_value"),
    ]),

# Input: arg1 = faction_no_1, arg2 = faction_no_2
  ("dplmc_get_truce_pay_amount",
   [
       (store_script_param, ":faction_no_1", 1),
       (store_script_param, ":faction_no_2", 2),
       (store_script_param, ":check_peace_war_result", 3),
	   ##diplomacy start+
	   #Since "fac_player_supporters_faction" is used as a shorthand for the faction
	   #run by the player, intercept that here instead of the various places this is
	   #called from.
	   (call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":faction_no_1", ":faction_no_2"),
	   (assign, ":faction_no_1", reg0),
	   (assign, ":faction_no_2", reg1),
	   ##diplomacy end+

       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg0, ":check_peace_war_result"), #debug
         (display_message, "@{!}DEBUG : peace_war_result: {reg0}"),#debug
       (try_end),

       ##nested diplomacy start+
       #Improve this script; costs were too low befow.
       #faction_no_1 is player faction asking for peace
       #faction_no_2 is NPC faction that already considered peace and considers
       #      it a bad idea, so the price should not be nominal.

       #(Also, a sign error meant that the amount asked was almost always
       #zero.)

       #Because the PC wants peace and the NPC doesn't, we aren't going to
       #bother calculating relative strength or the like.  Instead, we are
       #going to assume the NPC can achieve his strategic objectives if he
       #does not make peace, and set the price accordingly.

       #Add a generic cost for check_peace_war_result
       #These are the same as in Wahiti's original script.
       (assign, ":base_cost",  4000),
       (try_begin),
          #It's dubious that this is ever currently called if the check-peace-war
          #result was >= 0, but include this for completeness.
          (ge, ":check_peace_war_result", 0),
          (assign, ":base_cost", 4000),
       (else_try),
          (ge, ":check_peace_war_result", -1),
          (assign, ":base_cost", 8000),
       (else_try),
          (ge, ":check_peace_war_result", -2),
          (assign, ":base_cost", 12000),
       (else_try),
          #It shouldn't be used with this parameter; this is for the
          #sake of completeness.
          (le, ":check_peace_war_result", -3),
          (store_mul, ":base_cost", -6000, ":check_peace_war_result"),
       (try_end),

       #Get reparations for held centers.  A truce lasts 20 days, so the
       #value "lost" in rents and tarriffs by declaring peace now cannot be
       #is not greater than 3 times the weekly average (that upper bound is
       #if the NPC is in a position to immediately recapture all of them).

       #If the NPC kingdom is currently attacking a specific village or walled
       #center, even if it isn't an ex-possession it effectively becomes one.
       #(Also, assign it or its center as a demanded fief if there wasn't one
       #already.)
       (assign, ":target_fief", -1),
       (try_begin),
          (lt, ":check_peace_war_result", 1),#This should always be true anyway, but still.
          (this_or_next|faction_slot_eq, ":faction_no_2", slot_faction_ai_state, sfai_attacking_center),
          (faction_slot_eq, ":faction_no_2", slot_faction_ai_state, sfai_raiding_village),
          (faction_get_slot, reg0, ":faction_no_2", slot_faction_ai_object),
          (is_between, reg0, centers_begin, centers_end),
          (assign, ":target_fief", reg0),
       (try_end),

       (assign, ":center_cost", 0),
       (assign, ":concession_value", 0),
       #This this old are newer are considered "recently conquered", meaning that
       #faction_no_2 thinks there's a good chance they could reclaim them if the
       #fighting continued.
       (store_current_hours, ":recently_conquered"),
       (try_begin),
          (ge, ":check_peace_war_result", 1),#ordinarily this should not be true
          (val_sub, ":recently_conquered", 24 * 2),#only the last two days
       (else_try),
          (eq, ":check_peace_war_result", 0),
          (val_sub, ":recently_conquered", 24 * 15),#last 15 days
       (else_try),
          (eq, ":check_peace_war_result", -1),
          (val_sub, ":recently_conquered", 24 * 20),#last 20 days
       (else_try),
          (eq, ":check_peace_war_result", -2),
          (val_sub, ":recently_conquered", 24 * 30),#last 30 days
       (else_try),
          (val_sub, ":recently_conquered", 24 * 60),#last 60 days
       (try_end),

       (try_for_range, ":party_no", centers_begin, centers_end),
          (store_faction_of_party, ":party_current_faction", ":party_no"),
          (eq, ":party_current_faction", ":faction_no_1"),

          #party_value is the estimated weekly income of the fief,
          #applied three times and time discounted
          (call_script, "script_dplmc_estimate_center_weekly_income", ":party_no"),
          (store_mul, ":party_value", reg0, 3),

          (try_begin),
             (ge, "$g_concession_demanded", spawn_points_begin),
             (this_or_next|eq, "$g_concession_demanded", ":party_no"),
             (party_slot_eq, ":party_no", slot_village_bound_center, "$g_concession_demanded"),
             (val_add, ":concession_value", ":party_value"),
          (try_end),

          (assign, ":continue", 0),

          (try_begin),
             #A former possession of faction 2 (must have recently changed hands, or
             #faction 2 must be enthusiastic about the war)
             (party_slot_eq, ":party_no", slot_center_original_faction, ":faction_no_2"),
             (party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":recently_conquered"),
             (assign, ":continue", 1),
          (else_try),
             #A former possession of faction 2 (must have recently changed hands, or
             #faction 2 must be enthusiastic about the war)
             (party_slot_eq, ":party_no", slot_center_ex_faction, ":faction_no_2"),
             (party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":recently_conquered"),
             (assign, ":continue", 1),
          (else_try),
             #The center is being attacked by faction 2, or is a village whose castle
             #or town is being attacked by faction 2.
             (ge, ":target_fief", centers_begin),
             (this_or_next|eq, ":party_no", ":target_fief"),
             (party_slot_eq, ":party_no", slot_village_bound_center, ":target_fief"),
             (assign, ":continue", 1),
          (else_try),
             #The center is under siege by faction 2.
             (party_get_slot, reg0, ":party_no", slot_center_is_besieged_by),
             (gt, reg0, 0),
             (party_is_active, reg0),
             (store_faction_of_party, reg0, reg0),
             (eq, reg0, ":faction_no_2"),
             (assign, ":continue", 1),
          (else_try),
             #The center is a village, and the castle or town it is bound to
             #is under siege by faction 2.
             (is_between, ":party_no", villages_begin, villages_end),
             (party_get_slot, reg0, ":party_no", slot_village_bound_center),
             (is_between, reg0, centers_begin, centers_end),
             (party_get_slot, reg0, reg0, slot_center_is_besieged_by),
             (gt, reg0, -1),
             (party_is_active, reg0),
             (store_faction_of_party, reg0, reg0),
             (eq, reg0, ":faction_no_2"),
             (assign, ":continue", 1),
          (try_end),

          (gt, ":continue", 0),

          (val_add, ":center_cost", ":party_value"),
       (try_end),

       #If no held centers were found, assume the campaign objective is to
       #conquer territory rather than recover lost territory, if the
       #NPC is sufficiently enthusiastic about the war.
       (try_begin),
          #Equivalent of a castle and a village
          (eq, ":check_peace_war_result", -1),
          (val_max, ":center_cost", (1500 + 750) * 3),
       (else_try),
          #Equivalent of two castles with two villages
          (le, ":check_peace_war_result", -2),
          (val_max, ":center_cost", (1500 + 750) * 3 * 2),
       (try_end),

	   #If the war started very recently, or a center changed hands very recently,
	   #increase the cost.  The reasoning behind this is to make the AI less prone
	   #to whipsawing.
	   #
	   #The multiplier is 2x for the first 48 hours, then decreases linearly from
       #the two-day mark until it reaches zero at the 8-day mark.
	   #
	   #As an example, here is how a cost of 10,000 would scale over this time:
	   # 1 day  - 20000
	   # 2 days - 20000
	   # 3 days - 18333
	   # 4 days - 16667
	   # 5 days - 15000
	   # 6 days - 13333
	   # 7 days - 11667
	   # 8 days - 10000
	   # 9 days - 10000
	   (store_current_hours, ":cur_hours"),
       (faction_get_slot, ":faction_ai_last_decisive_event", ":faction_no_2", slot_faction_ai_last_decisive_event),
       (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),
	   (val_max, ":hours_since_last_decisive_event", 0),
	   (try_begin),
	      #First 48 hours, the base & center costs are doubled.
	      (lt, ":hours_since_last_decisive_event", 48 + 1),
		  (val_mul, ":base_cost", 2),
		  (val_mul, ":center_cost", 2),
	   (else_try),
	      #From 2 days to 8 days, the cost multiplier goes from 2 to 1
		  (lt, ":hours_since_last_decisive_event", 24 * 8),
		  (store_sub, reg0, 24 * 2, ":hours_since_last_decisive_event"),#0 to 6 days
		  (store_sub, ":multiplier", 24 * 12, reg0),# 6 to 12 days

		  (val_mul, ":base_cost", ":multiplier"),
		  (val_add, ":base_cost", (24 * 6) // 2),
		  (val_div, ":base_cost", 24 * 6),

		  (val_mul, ":center_cost", ":multiplier"),
		  (val_add, ":center_cost", (24 * 6) // 2),
		  (val_div, ":center_cost", 24 * 6),
	   (try_end),

       #Get (value of ransoms held by faction #1) - (value of ransoms held by faction #2)
       (call_script, "script_dplmc_get_prisoners_value_between_factions", ":faction_no_1", ":faction_no_2"),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}DEBUG : prisoner_value: {reg0}"),#debug
       (try_end),
       (assign, ":prisoner_value", reg0),

       #Write result to reg0
       (store_add, reg0, ":base_cost", ":center_cost"),

	   #Scale for the player's wealth, to partially mitigate the problem
	   #of the cost becoming meaningless as the player's wealth increases.
	   #(Scale less than 1-to-1, so it is possible to become richer in real
	   #terms.)  This is also aimed at reducing the necessity of replacing
	   #the values in mods that alter gold scarcity.
	   (store_troop_gold, ":player_gold", "trp_household_possessions"),
	   (store_troop_gold, reg1, "trp_player"),
	   (val_add, ":player_gold", reg1),
	   (try_begin),
		  #Arbitrarily pick 100,000 as the target wealth, since that's when
		  #you get the Steam "gold farmer" achievement.
	      (gt, ":player_gold", 100000),
		  (store_div, reg1, ":player_gold", 1000),
		  (val_mul, reg1, reg0),
		  (val_div, reg1, 100),

		  (val_add, reg0, reg1),
		  (val_div, reg0, 2),

		  #Apply the same scaling to the concession value
		  (store_div, reg1, ":player_gold", 1000),
		  (val_mul, reg1, ":concession_value"),
		  (val_div, reg1, 100),

		  (val_add, ":concession_value", reg1),
		  (val_div, ":concession_value", 2),
	   (try_end),

       #Take into account campaign difficulty
	   (assign, ":min_cost", reg0),
       (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
       (try_begin),
           (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
           (val_mul, reg0, 3),
           (val_div, reg0, 2),
		   (val_mul, ":min_cost", 87),#set min_cost to 87% of the original base_cost + center_cost
		   (val_div, ":min_cost", 100),
       (else_try),
           (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
		   (val_mul, ":min_cost", 3),
		   (val_div, ":min_cost", 4),#set min_cost to 75% (base cost + center cost)
       (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy (0.75x)
            (val_mul, reg0, 3),
			(val_div, reg0, 4),
			(val_mul, ":min_cost", 9),
			(val_div, ":min_cost", 16),#set min_cost to (75% squared) of (base cost + center cost)
       (try_end),

       (val_sub, reg0, ":prisoner_value"),

       #Because the NPC kingdom doesn't want peace, it will not agree to peace
       #for free, as that would be a contradiction.
       (val_max, reg0, ":min_cost"),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}DEBUG : peace_war_result after prisoners: {reg0}"),#debug
       (try_end),

       #The value of the concession (if any) was already calculated above
       (assign, reg1, -1),
       (try_begin),
          (gt, "$g_concession_demanded", 0),
       	  (gt, ":concession_value", 0),
          (store_sub, reg1, reg0, ":concession_value"),
          (val_max, reg1, 0),
          #Only accept cash alone in lieu of a fief if you don't partcularly
          #want war, or if the AI is on "easy".
          (try_begin),
             (neq, ":reduce_campaign_ai", 2),#hard or medium
             (lt, ":check_peace_war_result", 0),
             (assign, reg0, -1),
          (try_end),
       (try_end),

     (try_begin), #debug
       (eq, "$cheat_mode", 1),
	     (display_message, "@{!}DEBUG : truce_pay_amount0: {reg0}"),
	     (display_message, "@{!}DEBUG : truce_pay_amount1: {reg1}"),
     (try_end),
     ##nested diplomacy end+
    ]),

  ("dplmc_troop_political_notes_to_s47",
      [
    (store_script_param, ":troop_no", 1),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),#save to revert
    (assign, ":save_reg4", reg4),#save to revert

    (try_begin),
       (eq, 0, 1),#Always disable this right now
       (is_between, "$g_talk_troop", heroes_begin, heroes_end),#i.e. not your chancellor
       (assign, ":troop_speaker", "$g_talk_troop"),
	   (call_script, "script_troop_get_player_relation", ":troop_speaker"),
	   (assign, ":speaker_player_relation", reg0),
    (else_try),
       (assign, ":troop_speaker", -1),
	   (assign, ":speaker_player_relation", 100),
    (try_end),
    ##diplomacy end+

    (try_begin),
      (str_clear, s47),

      (store_faction_of_troop, ":troop_faction", ":troop_no"),

      (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),

      (str_clear, s40),
      (assign, ":logged_a_rivalry", 0),
      ##nested diplomacy start+
      (str_clear, s41),
      #lord can be married or related to player
      #(try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
      (try_for_range, ":kingdom_hero", active_npcs_including_player_begin, active_npcs_end),
        #Also, don't include rivalries with retired (or dead) characters
        (neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),
      ##nested diplomacy end+
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
        (lt, reg0, -10),

        (str_store_troop_name_link, s39, ":kingdom_hero"),
		  ##nested diplomacy start+ use second person
        (try_begin),
           (eq, ":kingdom_hero", "trp_player"),
           (str_store_string, s39, "str_you"),
        (try_end),
		  ##nested diplomacy end+
        (try_begin),
          (eq, ":logged_a_rivalry", 0),
          ##nested diplomacy start+
          (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),#use reg4 for gender-correct pronoun
          ##nested diplomacy end+
          (str_store_string, s40, "str_dplmc_s39_rival"),
          (assign, ":logged_a_rivalry", 1),
        (else_try),
          (str_store_string, s41, "str_s40"),
          (str_store_string, s40, "str_dplmc_s41_s39_rival"),
        (try_end),

      (try_end),

      (str_clear, s46),
      ##nested diplomacy start+
      #(troop_get_type, reg4, ":troop_no"),#use for gender-correct pronoun
		(call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
      (str_store_troop_name, s46,":troop_no"),
	  (assign, ":details_available", 0),
	  (try_begin),
		#Enable details for lords you have met
		(neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
		(assign, ":details_available", 1),
          (else_try),
                #Enable details when using an "omniscient" or non-specific speaker
                (neg|is_between, ":troop_speaker", heroes_begin, heroes_end),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for NPCs that aren't standard heroes, because the following checks don't apply
                (neg|is_between, ":troop_no", heroes_begin, heroes_end),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for lords the speaker has met
                (is_between, ":troop_speaker", heroes_begin, heroes_end),
                (is_between, ":troop_no", heroes_begin, heroes_end),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":troop_speaker"),
                (neq, reg0, 0),#between NPCs, relation 0 means "have not met"
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for v. notable lords (based on renown)
                (troop_slot_ge, ":troop_no", slot_troop_renown, 500),
                (assign, ":details_available", 1),
          (else_try),
                #Enable details for v. notable lords (based on fiefs)
                (assign, reg0, 0),
                (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                   (this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
                   (this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
                     (troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
                   (val_add, reg0, 2),
                   (party_slot_eq, ":center_no", slot_party_type, spt_town),
                   (val_add, reg0, 2),
                (try_end),
                (ge, reg0, 4),#one town, or 2+ castles
                (assign, ":details_available", 1),
          (try_end),
      #xxx TODO: Make a full implementation of the above that takes into account the time of the last spy report.
      (try_begin),
		(eq, ":details_available", 0),
		(troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
        (str_store_string, s46, "str_dplmc_reputation_unknown"),
	  (else_try),
	  ##nested diplomacy end+
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        (str_store_string, s46, "str_dplmc_reputation_martial"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        (str_store_string, s46, "str_dplmc_reputation_debauched"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
        (str_store_string, s46, "str_dplmc_reputation_pitiless"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
        (str_store_string, s46, "str_dplmc_reputation_calculating"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        (str_store_string, s46, "str_dplmc_reputation_quarrelsome"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        (str_store_string, s46, "str_dplmc_reputation_goodnatured"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        (str_store_string, s46, "str_dplmc_reputation_upstanding"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
        (str_store_string, s46, "str_dplmc_reputation_conventional"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_adventurous),
        (str_store_string, s46, "str_dplmc_reputation_adventurous"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_otherworldly),
        (str_store_string, s46, "str_dplmc_reputation_romantic"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
        (str_store_string, s46, "str_dplmc_reputation_moralist"),
      (else_try),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_ambitious),
        (str_store_string, s46, "str_dplmc_reputation_ambitious"),
      (else_try),
        (troop_get_slot, reg11, ":troop_no", slot_lord_reputation_type),
        (str_store_string, s46, "str_dplmc_reputation_unknown"),
      (try_end),

      ##diplomacy start+
      (str_clear, s39),#remove annoying bug
      (str_clear, s45),#remove annoying bug

      #Special-case spouse into showing up if it doesn't get added below
      (try_begin),
         (troop_get_slot, ":spouse", ":troop_no", slot_troop_spouse),
         (ge, ":spouse", 0),

         #Because blank memory is initially zero, enforce this
         (this_or_next|is_between, ":troop_no", heroes_begin, heroes_end),
            (neq, ":spouse", "trp_player"),
         #Initialize s45
         (str_store_troop_name, s39, ":spouse"),
         (try_begin),
           (eq, ":spouse", "trp_player"),
           (str_store_string, s39, "str_you"),##<-- dplmc+ note, this was s59 before, probably an accidental bug
         (else_try), #SB : speaker
           (eq, ":spouse", ":troop_speaker"),
           (str_store_string, s39, "str_me"),
         (try_end),
         (str_store_string, s45, "str_dplmc_s40_married_s39"),
      (try_end),
      ##diplomacy end+

      (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
        (troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
        ##nested diplomacy start+ ; some lords could romance opposite-gender lords
        #(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
        (is_between, ":love_interest", active_npcs_begin, kingdom_ladies_end),
        #Also prevent a bug for companions / claimants who are lords
        (neq, ":love_interest", "trp_knight_1_1_wife"),#<- should not appear in the game
        #Also prevent bad messages for married/betrothed lords
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, ":love_interest"),
           (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
           (troop_slot_eq, ":troop_no", slot_troop_betrothed, -1),
        ##nested diplomacy end+
        (str_store_troop_name, s39, ":love_interest"),
        ##nested diplomacy start+ Use second person properly
        (try_begin),
           (eq, ":love_interest", "trp_player"),
           (str_store_string, s39, "str_you"),
         (else_try), #SB : speaker
           (eq, ":love_interest", ":troop_speaker"),
           (str_store_string, s39, "str_me"),
        (try_end),
        ##nested diplomacy start+
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
        ##nested diplomacy start+
        (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),#use reg4 for gender-correct pronoun
        ##nested diplomacy end+
        (str_store_string, s45, "str_dplmc_s40_love_interest_s39"),
        (try_begin),
        	(troop_slot_eq, ":troop_no", slot_troop_spouse, ":love_interest"),
        	(str_store_string, s45, "str_dplmc_s40_married_s39"),
        (else_try),
        	(troop_slot_eq, ":troop_no", slot_troop_betrothed, ":love_interest"),
        	(str_store_string, s45, "str_dplmc_s40_betrothed_s39"),
        (try_end),
      (try_end),

    (str_clear, s44),
    (try_begin),
      (neq, ":troop_no", ":faction_leader"),
      ##nested diplomacy start+
      (gt, ":details_available", 0),
	  #Ensure leader is valid
	  (assign, reg0, 0),#continue if 0
	  (try_begin),
	     (neq, ":troop_no", "trp_player"),
		 (neq, ":faction_leader", "trp_player"),
		 (this_or_next|neg|is_between, ":troop_no", heroes_begin, heroes_end),
			(neg|is_between, ":faction_leader", heroes_begin, heroes_end),
		 (assign, reg0, 1),
	  (try_end),
	  (eq, reg0, 0),

	  (try_begin),
	     (gt, ":troop_speaker", 0),
		 (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_no", ":troop_speaker"),
		 #(val_min, reg0, 20),
		 #(neq, ":faction_leader", "trp_player"),
		 #(val_div, reg0, 2),
	  (try_end),
	  (this_or_next|lt, reg0, 1),
		(ge, ":speaker_player_relation", 1),
      ##nested diplomacy end+
      (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),

      (assign, ":relation", reg0),
	  ##diplomacy start+ Don't mention anything for kingdom ladies at the beginning; it doesn't add information.
	  (this_or_next|lt, reg0, 0),
	  (this_or_next|gt, reg0, 1),#Remember that relation 1 is neutral (it just means "met") between NPCs
	  (this_or_next|neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
	     (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
	  ##diplomacy end+
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      ##nested diplomacy start+
      #(troop_get_type, reg4, ":troop_no"),#use for gender-correct pronoun
      (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
      #TODO: Come back and add this (take into account spying)
      #(neq, ":details_available", 0),#don't show unless more details are available
      ##nested diplomacy end+
      (store_add, ":str_id", "str_dplmc_relation_mnus_100_ns",  ":str_offset"),
      (try_begin),
        (eq, ":faction_leader", "trp_player"),
        ##nested diplomacy start+ "str_you" exists, so we might as well use it
        #(str_store_string, s59, "@you"),
        (str_store_string, s59, "str_you"),
        ##diplomacy end+
      (else_try),
        (str_store_troop_name, s59, ":faction_leader"),
      (try_end),
      (str_store_string, s59, ":str_id"),
      (str_store_string, s44, "@{!}^{s59}"),
    (try_end),

    (str_clear, s48),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (store_current_hours, ":hours"),
      (gt, ":hours", 0),
      (call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
      (str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
    (try_end),

    (str_store_string, s47, "str_s46s45s44s48"),

  (try_end),
     ##diplomacy start+
     (assign, reg1, ":save_reg1"),#revert register
     (assign, reg4, ":save_reg4"),#revert register to avoid clobbering
     ##diplomacy end+
    ]),

  ("dplmc_init_domestic_policy",
  [
    (try_for_range, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      (try_begin),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_centralization, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_aristocracy, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_quality, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_serfdom, ":random"),
      (try_end),
    (try_end),
  ]),

  #SB : add this to allow randomization of a single faction (see prsnt_dplmc_policy_management)
  ("dplmc_randomize_faction_domestic_policy",
    [
    (store_script_param, ":kingdom", 1),
    (try_for_range, ":slot", dplmc_slot_faction_centralization, dplmc_slot_faction_mercantilism + 1),
      (store_random_in_range, ":random", -3, 4),
      (faction_set_slot, ":kingdom", ":slot", ":random"),
    (try_end),
    ]),

  ("dplmc_appoint_chamberlain",
  [
    (troop_set_auto_equip, "trp_dplmc_chamberlain", 0),
    (troop_set_inventory_slot, "trp_dplmc_chamberlain", ek_body, "itm_tabard"),
    (troop_set_inventory_slot, "trp_dplmc_chamberlain", ek_foot, "itm_leather_boots"),
    (assign, "$g_player_chamberlain", "trp_dplmc_chamberlain"),
    #SB : grab all gold from chest troops (seneschals)
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
      (store_sub, ":chest_troop", ":center_no", towns_begin),
      (val_add, ":chest_troop", "trp_town_1_seneschal"),
      (store_troop_gold, ":cur_gold", ":chest_troop"),
      (troop_remove_gold, ":chest_troop", ":cur_gold"),
      (troop_add_gold, "trp_household_possessions", ":cur_gold"), #no script call
    (try_end),
  ]),

  ("dplmc_appoint_chancellor",
  [
    (troop_set_auto_equip, "trp_dplmc_chancellor", 0),
    (troop_set_inventory_slot, "trp_dplmc_chancellor", ek_body, "itm_nobleman_outfit"),
    (troop_set_inventory_slot, "trp_dplmc_chancellor", ek_foot, "itm_leather_boots"),
    (assign, "$g_player_chancellor", "trp_dplmc_chancellor"),
  ]),

  ("dplmc_appoint_constable",
  [
    (troop_set_auto_equip, "trp_dplmc_constable", 0),
    (troop_set_inventory_slot, "trp_dplmc_constable", ek_body, "itm_dplmc_coat_of_plates_red_constable"),
    (troop_set_inventory_slot, "trp_dplmc_constable", ek_foot, "itm_leather_boots"),
    (assign, "$g_player_constable", "trp_dplmc_constable"),
  ]),

##diplomacy end
  # INPUT: arg1 = troop_id, arg2 = new faction_no
  # OUTPUT: none
  ("dplmc_faction_leader_splits_gold",
    [
	(store_script_param_1, ":faction_no"),
    (store_script_param_2, ":king_gold"),
	(assign, ":push_reg0", reg0),#revert register value at end of script
	(assign, ":push_reg1", reg1),#revert register value at end of script

	(faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	(faction_get_slot, reg0, ":faction_no", dplmc_slot_faction_centralization),
	(val_clamp, reg0, -3, 4),
	(val_mul, reg0, -5),
	(try_begin),
		(troop_slot_ge, ":faction_liege", slot_troop_wealth, 20000),
		(val_add, reg0, 20),#20% if the king is at or above his starting gold
	(else_try),
		(val_add, reg0, 50),#50% otherwise
	(try_end),
	(val_add, reg0, 50),
	(store_mul, ":lord_gold", ":king_gold", reg0),#king splits other half among lords
	(val_div, ":lord_gold", 100),
	(val_sub, ":king_gold", ":lord_gold"),
	(try_begin),
		#If there's enough gold to give a meaningful amount to everyone, do so.
		#(This accomplishes two things.  It makes the distribution more even, and
		#it prevents this script from taking an unreasonably long time for very
		#large amounts of gold.)
		#
		#"Meaningful" is at least 300, because that's the minimum amount of gold a
		#lord will to to a fief to collect (it is also the AI recruitment cost on
		#hard).
		(assign, ":num_lords", 0),#<-- number of lords in faction, not including faction leader
		(try_for_range, ":lord_no", heroes_begin, heroes_end),
			(store_troop_faction, ":lord_faction_no", ":lord_no"),
			(eq, ":faction_no", ":lord_faction_no"),
			(troop_set_slot, ":lord_no", slot_troop_temp_slot, 0),
			(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
			(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
			(ge, ":lord_party", 0),
			(val_add, ":num_lords", 1),
		(try_end),
		(try_begin),
			#handle player
			(eq, "$players_kingdom", ":faction_no"),
			(neq, "trp_player", ":faction_liege"),
			(neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),
			(val_add, ":num_lords", 1),
		(try_end),
		(gt, ":num_lords", 0),#<-- can fail
		(store_div, ":gold_to_each", ":lord_gold", ":num_lords"),
		(ge, ":gold_to_each", 300),
		(val_div, ":gold_to_each", 150),#regularize (standard reinforcement costs for easy/medium/hard are 600/450/300, which are multiples of 150)
		(val_mul, ":gold_to_each", 150),

		#(try_begin),
		#	(ge, "$cheat_mode", 1),
		#	(assign, reg0, ":num_lords"),
		#	(assign, reg1, ":gold_to_each"),
		#	(str_store_faction_name, s5, ":faction_no"),
		#	(display_message, "@ {reg0} vassals of the {s5} receive {reg1} denars each (dplmc_faction_leader_splits_gold)"),
		#(try_end),

		(try_for_range, ":lord_no", heroes_begin, heroes_end),
			(ge, ":lord_gold", ":gold_to_each"),
			#verify lord is vassal of kingdom
			(store_troop_faction, ":lord_faction_no", ":lord_no"),
			(eq, ":faction_no", ":lord_faction_no"),
			(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
			(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
			(ge, ":lord_party", 0),
			#give gold to lord
			(val_sub, ":lord_gold", ":gold_to_each"),
			#(troop_get_slot, reg0, ":lord_no", slot_troop_temp_slot),
			#(val_add, reg0, ":gold_to_each"),
			#(troop_set_slot, ":lord_no", slot_troop_temp_slot, reg0),
			##(call_script, "script_troop_add_gold", ":lord_no", ":gold_to_each"),
			(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":gold_to_each", ":lord_no"),
		(try_end),
		(try_begin),
			(ge, ":lord_gold", ":gold_to_each"),
			#give gold to player if player is vassal of kingdom
			(eq, "$players_kingdom", ":faction_no"),
			(neq, "trp_player", ":faction_liege"),
			(neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),
			(val_sub, ":lord_gold", ":gold_to_each"),
			(troop_get_slot, reg0, "trp_player", slot_troop_temp_slot),
			(val_add, reg0, ":gold_to_each"),
			(troop_set_slot, "trp_player", slot_troop_temp_slot, reg0),
			##(call_script, "script_troop_add_gold", ":lord_no", ":gold_to_each"),
		(try_end),
	(try_end),
	#Now, distribute the remaining gold.  Assign gold in increments of 300,
	#because that's the minimum amount of gold a lord will go to a fief for
	#(also the AI recruitment cost on hard).
	(store_div, ":count", ":lord_gold", 300),
	(val_max, ":count", 1),
	(try_for_range, ":unused", 0, ":count"),
		(ge, ":lord_gold", 300),
		(call_script, "script_cf_get_random_lord_except_king_with_faction", ":faction_no"),
		(is_between, reg0, heroes_begin, heroes_end),
		(assign, ":troop_no", reg0),
		(val_sub, ":lord_gold", 300),
		(troop_get_slot, reg0, ":troop_no", slot_troop_temp_slot),
		(val_add, reg0, 300),
		(troop_set_slot, ":troop_no", slot_troop_temp_slot, reg0),
		#(call_script, "script_troop_add_gold", ":troop_no", 300),
	(try_end),

	#Now the distribution is set.  Give each one his allotment.
	(try_for_range, ":lord_no", heroes_begin, heroes_end),
		(ge, ":lord_gold", ":gold_to_each"),
		#verify lord is vassal of kingdom
		(store_troop_faction, ":lord_faction_no", ":lord_no"),
		(eq, ":faction_no", ":lord_faction_no"),
		(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":lord_no"),
		(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
		(neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
		(troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
		(ge, ":lord_party", 0),
		#get promised gold
		(troop_get_slot, reg0, ":lord_no", slot_troop_temp_slot),
		(neq, reg0, 0),
		#(try_begin),
		#	(ge, "$cheat_mode", 1),
		#	(str_store_troop_name, s4, ":lord_no"),
		#	(str_store_faction_name, s5, ":faction_no"),
		#	(str_store_troop_name, s6, ":faction_liege"),
		#	(display_message, "@{!}{s4} of the {s5} receives {reg0} denars (dplmc_faction_leader_splits_gold)"),
		#(try_end),
		(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", reg0, ":lord_no"),
		(troop_set_slot, ":lord_no", slot_troop_temp_slot, 0),
	(try_end),

	(val_add, ":king_gold", ":lord_gold"),#Give remaining gold to king
	(try_begin),
		(ge, "$cheat_mode", 1),
		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s5, ":faction_no"),
		(str_store_troop_name, s6, ":faction_liege"),
		(display_message, "@{!}{s6} of the {s5} retains the remaining {reg0} denars (dplmc_faction_leader_splits_gold)"),
	(try_end),

	#(call_script, "script_troop_add_gold", ":faction_liege", ":king_gold"),
	(call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":king_gold", ":faction_liege"),
	(assign, reg0, ":push_reg0"),#revert register value
	(assign, reg1, ":push_reg1"),#revert register value
	]),


  #script_dplmc_lord_return_from_exile
	# INPUT
	#   arg1:  faction_1
	#   arg2:  faction_2
	# OUTPUT
	#   reg0:  The length in days of faction_1's truce with faction_2, if any.
	#          If no truce exists, the appropriate value to return is zero.
    ("dplmc_get_faction_truce_length_with_faction",
	   [
	    (store_script_param, ":faction_1", 1),
		(store_script_param, ":faction_2", 2),

		(assign, ":truce_length", 0),

		(try_begin),
			(is_between, ":faction_1", kingdoms_begin, kingdoms_end),
			(is_between, ":faction_2", kingdoms_begin, kingdoms_end),
			(neq, ":faction_1", ":faction_2"),
			(store_add, ":truce_slot", ":faction_2", slot_faction_truce_days_with_factions_begin),
			(val_sub, ":truce_slot", kingdoms_begin),
			(faction_get_slot, ":truce_length", ":faction_1", ":truce_slot"),
        (try_end),
	    (assign, reg0, ":truce_length"),
	   ]),

  #script_dplmc_get_terrain_code_for_battle
#
#INPUT: arg1  :troop_no
#       arg2  :faction_no
#
#OUTPUT:
#       reg0  A constant with the value DPLMC_FACTION_STANDING_<something>
#
## Constants defined in module_constants.py
#DPLMC_FACTION_STANDING_LEADER = 60
#DPLMC_FACTION_STANDING_LEADER_SPOUSE = 50
#DPLMC_FACTION_STANDING_MARSHALL = 40
#DPLMC_FACTION_STANDING_LORD = 30
#DPLMC_FACTION_STANDING_DEPENDENT = 20
#DPLMC_FACTION_STANDING_MEMBER = 10#includes mercenaries
#DPLMC_FACTION_STANDING_PETITIONER = 5
#DPLMC_FACTION_STANDING_UNAFFILIATED = 0
##diplomacy end+
 ("dplmc_get_troop_standing_in_faction",
 [
    (store_script_param_1, ":troop_no"),
    (store_script_param_2, ":faction_no"),

    (assign, ":standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
    (assign, ":original_faction_no", ":faction_no"),
    (try_begin),
        #Translate fac_player_faction
        (eq, ":faction_no", "fac_player_faction"),
        (assign, ":faction_no", "fac_player_supporters_faction"),
    (try_end),

    (try_begin),
       (this_or_next|lt, ":troop_no", 0),#Do nothing, bad troop ID
          (lt, ":faction_no", 0),#Do nothing, bad faction
    (else_try),
       #Because of how this script is used, if fac_player_supporters_faction is active,
       # this always reports that the player is its leader (even though that is sometimes
       # untrue, for example in a claimant quest)
       (eq, ":troop_no", "trp_player"),#Short-circuit the remainder if these are true
       (eq, ":faction_no", "fac_player_supporters_faction"),
       (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
       # (neg|is_between, "$supported_pretender", pretenders_begin, pretenders_end), #SB : claimant exception
       (assign, ":standing", DPLMC_FACTION_STANDING_LEADER),
    (else_try),
		(try_begin),
			#Translate fac_player_supporters_faction
			(eq, ":faction_no", "fac_player_supporters_faction"),
			(gt, "$players_kingdom", 0),
			(assign, ":faction_no", "$players_kingdom"),
		(try_end),

        (store_faction_of_troop, ":troop_faction", ":troop_no"),
        (try_begin),
           #Translate fac_player_supporters_faction
           (this_or_next|eq, ":troop_no", "trp_player"),
           (this_or_next|eq, ":troop_faction", "fac_player_faction"),
           (eq, ":troop_faction", "fac_player_supporters_faction"),
           (assign, ":troop_faction", "fac_player_supporters_faction"),
           (gt, "$players_kingdom", 0),
           (assign, ":troop_faction", "$players_kingdom"),
        (try_end),
        (eq, ":troop_faction", ":faction_no"),#<- Short-circuit the remainder if this is false
        (assign, ":standing", DPLMC_FACTION_STANDING_MEMBER),

        (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
        (try_begin),
           #Faction leader
           (eq, ":faction_leader", ":troop_no"),
           (assign, ":standing", DPLMC_FACTION_STANDING_LEADER),
        (else_try),
           #Spouse of faction leader
           (gt, ":faction_leader", -1),
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
              (troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
           #Deal with possible uninitialized slot
           (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
           (this_or_next|neq, ":faction_leader", 0),
              (is_between, ":troop_no", heroes_begin, heroes_end),
           (assign, ":standing", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (else_try),
           #Faction marshall
           (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
           (assign, ":standing", DPLMC_FACTION_STANDING_MARSHALL),
        (else_try),
           #If the troop is the player, if he has homage he is a lord.
           #Otherwise he is a mercenary.
           (eq, ":troop_no", "trp_player"),
           (try_begin),
              (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
              (ge, "$player_has_homage", 1),
              (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
           (else_try),
              #If the player is married to a lord/lady in the faction, the
              #homage variable should always be set to 1+, but add a separate
              #check just in case.
              (troop_get_slot, reg0, "trp_player", slot_troop_spouse),
              (is_between, reg0, heroes_begin, heroes_end),
              (store_faction_of_troop, reg0, reg0),
              (this_or_next|eq, reg0, "fac_player_supporters_faction"),
              (eq, reg0, ":faction_no"),
              (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
           (try_end),
        (else_try),
            #None of the following conditions apply for non-heroes
            (this_or_next|lt, ":troop_no", heroes_begin),
                (neg|troop_is_hero, ":troop_no"),
        (else_try),
           #For kingdom heroes, part 1 (check lordship based on occupation)
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
        (else_try),
           #For kingdom ladies
           (this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
           (assign, ":standing", DPLMC_FACTION_STANDING_DEPENDENT),
        (else_try),
           #For petitioners
           (eq, ":original_faction_no", "fac_player_supporters_faction"),
           (is_between, ":troop_no", lords_begin, lords_end),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
           (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
           (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
           (assign, ":standing", DPLMC_FACTION_STANDING_PETITIONER),
        (else_try),
            #For kingdom heroes, part 2 (all non-companion active NPCs)
            (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
            (neg|is_between, ":troop_no", companions_begin, companions_end),
            (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
        (try_end),
    (try_end),

    (assign, reg0,  ":standing"),
 ]),

 ## "script_dplmc_store_troop_is_eligible_for_affiliate_messages"
#
#Since "fac_player_supporters_faction" is often used as a parameter when what
#is really meant is "the faction led by the player" (which is never a different
#faction in Native), there are many calls we want to change.  Another solution
#is to approach the problem from the other side, and "correct" the arguments.
#
#If exactly one argument is equal to fac_player_supporters_faction, and fac_player_supporters_faction
#is not sfs_active, and $players_kingdom is an NPC kingdom of which the player is ruler or co-ruler,
#and the other argument is not equal to $players_kingdom, then the argument equal to fac_player_supporters_faction
#will be replaced with $players_kingdom.
#
#INPUT:
# arg1 - faction_1
# arg2 - faction_2
#OUTPUT:
# reg0 - faction_1, possibly replacing fac_player_supporters_faction with $players_kingdom (see above)
# reg1 - faction_2, possibly replacing fac_player_supporters_faction with $players_kingdom (see above)
("dplmc_translate_inactive_player_supporter_faction_2",
[
    (store_script_param_1, ":faction_1"),
    (store_script_param_2, ":faction_2"),

	(try_begin),
		(this_or_next|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		(this_or_next|neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|eq, ":faction_1", "$players_kingdom"),
		(this_or_next|eq, ":faction_2", "$players_kingdom"),
			(eq, ":faction_1", ":faction_2"),
      #Do nothing
	(else_try),
		(eq, ":faction_1", "fac_player_supporters_faction"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":faction_1", "$players_kingdom"),
	(else_try),
		(eq, ":faction_2", "fac_player_supporters_faction"),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":faction_2", "$players_kingdom"),
	(try_end),

	(assign, reg0, ":faction_1"),
	(assign, reg1, ":faction_2"),
]),

##"script_cf_dplmc_player_party_meets_autoloot_conditions"
	#input - faction, change, display mode
	#output - a colored message
	("change_faction_troop_morale",
	  [(store_script_param, ":faction_no", 1),
	   (store_script_param, ":morale_change", 2),
	   (store_script_param, ":display", 3),
	   (try_begin),
		 (eq, ":display", 1),
		 (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		 (assign, ":display", 0),
	   (try_end),
	   #check if main party has troop of type before displaying
	   (try_begin),
		 (eq, ":display", 1),
		 (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		 (try_for_range, ":stack", 1, ":num_stacks"),
		   (party_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
		   (store_troop_faction, ":fac", ":troop"),
		   (eq, ":fac", ":faction_no"),
		   (assign, ":num_stacks", 1), #break
		 (try_end),
		 (neq, ":num_stacks", 1), #none found
		 (assign, ":display", 0),
	   (try_end),
	   #effects are still applied regardless - the displayed morale is divided by 100
	   (faction_get_slot, ":morale", ":faction_no", slot_faction_morale_of_player_troops),
	   (store_div, reg1, ":morale", 100),
	   (val_add, ":morale", ":morale_change"),
	   (store_div, reg2, ":morale", 100),
	   (faction_set_slot, ":faction_no", slot_faction_morale_of_player_troops, ":morale"),

	   # (try_begin),
		 # (store_sub, ":diff", reg2, reg1),
		 # (eq, ":diff", 0), #negligible
		 # (assign, ":display", 0),
	   # (try_end),

	   #actual output
	   (try_begin),
		 (eq, ":display", 1),
         (neq, reg1, reg2), #non-zero difference
		 #set up s1
		 #(faction_get_slot, ":adjective", ":faction_no", slot_faction_adjective),
         (str_store_faction_name, s1, ":faction_no"),
		 #(str_store_string, s1, ":adjective"),
		 (str_store_string, s1, "@{s1} troops"),
		 #get increase/decrease, either string will work
		 (assign, ":string", "str_troop_relation_detoriated"),
		 (try_begin),
		   (gt, ":morale_change", 0),
		   (assign, ":string", "str_troop_relation_increased"),
		 (try_end),
		 #get color
		 (faction_get_color, ":color", ":faction_no"),
		 (display_message, ":string", ":color"),
	   (try_end),
	  ]
	),

    #script_encounter_agent_draw_weapon
]
