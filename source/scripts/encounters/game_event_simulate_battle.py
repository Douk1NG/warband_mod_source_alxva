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

game_event_simulate_battle_scripts = [
#script_game_event_simulate_battle:
# This script is called whenever the game simulates the battle between two parties on the map.
# INPUT:
# param1: Defender Party
# param2: Attacker Party
("game_event_simulate_battle",
    [
      (store_script_param_1, ":root_defender_party"),
      (store_script_param_2, ":root_attacker_party"),

      (assign, "$marshall_defeated_in_battle", -1),

      (store_current_hours, ":hours"),

      ##diplomacy start+ Get campaign AI, used below
      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      ##diplomacy end+

      (try_for_parties, ":party"),
        (party_get_battle_opponent, ":opponent", ":party"),
        (gt, ":opponent", 0),
        (party_set_slot, ":party", slot_party_last_in_combat, ":hours"),
      (try_end),

      (assign, ":trigger_result", 1),
      (try_begin),
        (ge, ":root_defender_party", 0),
        (ge, ":root_attacker_party", 0),
        (party_is_active, ":root_defender_party"),
        (party_is_active, ":root_attacker_party"),
        (store_faction_of_party, ":defender_faction", ":root_defender_party"),
        (store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
        #(neq, ":defender_faction", "fac_player_faction"),
        #(neq, ":attacker_faction", "fac_player_faction"),
        (store_relation, ":reln", ":defender_faction", ":attacker_faction"),
        (lt, ":reln", 0),
        (assign, ":trigger_result", 0),

        (try_begin),
          (this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
          (eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
          (assign, "$g_battle_simulation_cancel_for_party", -1),
          (assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),
          (assign, ":trigger_result", 1),
        (else_try),
          (try_begin),
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
            (party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
            (assign, ":trigger_result", 1), #End battle!
          (try_end),
          (party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),

          #(assign, ":cancel_attack", 0),

          (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),

	      ##diplomacy start+
 		  (assign, ":terrain_code", dplmc_terrain_code_none),#defined in header_terrain.py
          (try_begin),
              (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			  (call_script, "script_dplmc_get_terrain_code_for_battle", ":root_attacker_party", ":root_defender_party"),
			  (assign, ":terrain_code", reg0),
			  #
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_ally", ":terrain_code", 0, 1),
              (assign, ":defender_strength", reg0),
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code", 0, 1),
              (assign, ":attacker_strength", reg0),
          (else_try),
              (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
              (assign, ":defender_strength", reg0),
          #(call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
              (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
              (assign, ":attacker_strength", reg0),
          (try_end),
          ##diplomacy end+

          (store_div, ":defender_strength", ":defender_strength", 20),
          (val_min, ":defender_strength", 50),
          (val_max, ":defender_strength", 1),
          (store_div, ":attacker_strength", ":attacker_strength", 20),
          (val_min, ":attacker_strength", 50),
          (val_add, ":attacker_strength", 1),
          (try_begin),
            #For sieges increase attacker casualties and reduce defender casualties.
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
            (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
            (val_mul, ":defender_strength", 123), #it was 1.5 in old version, now it is only 1.23
            (val_div, ":defender_strength", 100),

            (val_mul, ":attacker_strength", 100), #it was 0.5 in old version, now it is only 1 / 1.23
            (val_div, ":attacker_strength", 123),
          (try_end),

          ##diplomacy begin
          (assign, ":defender_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":defender_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":defender_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":defender_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":defender_percent", ":quality"),
          (try_end),
          (val_mul, ":defender_strength", ":defender_percent"),
          (val_div, ":defender_strength", 100),

          (assign, ":attacker_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":attacker_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":attacker_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":attacker_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":attacker_percent", ":quality"),
          (try_end),
          (val_mul, ":attacker_strength", ":attacker_percent"),
          (val_div, ":attacker_strength", 100),
          ##diplomacy end

          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":old_defender_strength", reg0),

          (try_begin),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
          (assign, ":new_attacker_strength", reg0),

          (try_begin),
            (gt, ":new_attacker_strength", 0),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":new_defender_strength", reg0),

          (try_begin),
            (this_or_next|eq, ":new_attacker_strength", 0),
            (eq, ":new_defender_strength", 0),
            # Battle concluded! determine winner

            (assign, ":do_not_end_battle", 0),
            (try_begin),
              (neg|troop_is_wounded, "trp_player"),
              (eq, ":new_defender_strength", 0),
              (eq, "$auto_enter_town", "$g_encountered_party"),
              (eq, ":old_defender_strength", ":new_defender_strength"),
              (assign, ":do_not_end_battle", 1),
            (try_end),
            (eq, ":do_not_end_battle", 0),

            (try_begin),
              (eq, ":new_attacker_strength", 0),
              (eq, ":new_defender_strength", 0),
              (assign, ":root_winner_party", -1),
              (assign, ":root_defeated_party", -1),
              (assign, ":collective_casualties", -1),
            (else_try),
              (eq, ":new_attacker_strength", 0),
              (assign, ":root_winner_party", ":root_defender_party"),
              (assign, ":root_defeated_party", ":root_attacker_party"),
              (assign, ":collective_casualties", "p_collective_enemy"),
            (else_try),
              (assign, ":root_winner_party", ":root_attacker_party"),
              (assign, ":root_defeated_party", ":root_defender_party"),
              (assign, ":collective_casualties", "p_collective_ally"),
            (try_end),
##diplomacy begin
        (try_begin),
          (gt, ":root_defeated_party", -1),
# Recruiter kit begin
 # This little fella just shows a message when a recruiter is defeated.

         (assign, ":minimum_distance", 1000000),
         (try_for_range, ":center", centers_begin, centers_end),
           (store_distance_to_party_from_party, ":dist", ":root_defeated_party", ":center"),
           (try_begin),
             (lt, ":dist", ":minimum_distance"),
             (assign, ":minimum_distance", ":dist"),
             (assign, ":nearest_center", ":center"),
           (try_end),
         (try_end),

        (str_clear, s10),
        (try_begin),
          (gt, ":nearest_center", 0),
          (str_store_party_name, s10, ":nearest_center"),
          (str_store_string, s10, "@ near {s10}"),
        (try_end),

        #SB : reformat loop
        (party_get_slot, ":type", ":root_defeated_party", slot_party_type),
        (try_begin),
          (eq, ":type", dplmc_spt_recruiter),
          (party_get_slot, reg10, ":root_defeated_party", dplmc_slot_party_recruiter_needed_recruits),
          (party_get_slot, ":party_origin", ":root_defeated_party", dplmc_slot_party_recruiter_origin),
          (str_store_party_name_link, s13, ":party_origin"),
          (display_log_message, "@Your recruiter who was commissioned to recruit {reg10} recruits to {s13} has been defeated{s10}!", message_defeated),
        (else_try),
          (eq,":type", dplmc_spt_gift_caravan),
          (party_get_slot, ":target_troop", ":root_defeated_party", slot_party_orders_object),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (try_begin),
            (gt, ":target_troop", 0),
            (str_store_troop_name, s13, ":target_troop"),
          (else_try),
            (str_store_party_name, s13, ":target_party"),
          (end_try),
          (party_get_slot, ":gift", ":root_defeated_party", dplmc_slot_party_mission_diplomacy),
          (str_store_item_name, s12, ":gift"),
          #SB : defeated -> looted
          (display_log_message, "@Your caravan sending {s12} to {s13} has been looted{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_messenger),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),
          #SB : defeated -> intercepted
          (display_log_message, "@Your messenger on the way to {s13} has been ambushed{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_patrol),
          (party_slot_eq, ":root_defeated_party", dplmc_slot_party_mission_diplomacy, "trp_player"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@Your soldiers patrolling {s13} have been defeated{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_scout),
          (store_faction_of_party, ":party_faction", ":root_defeated_party"),
          (eq, ":party_faction", "$players_kingdom"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@A scout trying to gather information about {s13} has been slain{s10}!", message_defeated),
        (else_try), #SB : reinforcements
          (eq, ":type", spt_reinforcement),
          (store_faction_of_party, ":party_faction", ":root_defeated_party"),
          (eq, ":party_faction", "$players_kingdom"), #show only if relevant
          (party_get_slot, ":home_village", ":root_defeated_party", slot_party_home_center),
          (party_get_slot, ":target_party", ":home_village", slot_village_bound_center),
          (str_store_party_name_link, s12, ":home_village"),
          (str_store_party_name_link, s13, ":target_party"),
          (display_log_message, "@Reinforcements from {s12} intended for {s13} have been intercepted{s10}!", message_defeated),
        (try_end),
      (try_end),
##diplomacy end

            (try_begin),
              (ge, ":root_winner_party", 0),
              (call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
              (assign, ":nonempty_winner_party", reg0),
              (store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
              (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
            (else_try),
              (assign, ":nonempty_winner_party", -1),
            (try_end),

            (try_begin),
              (ge, ":collective_casualties", 0),
              (party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
            (else_try),
              (assign, ":num_stacks", 0),
            (try_end),

            #SB : set up primary color here
            (faction_get_color, ":faction_color", ":faction_receiving_prisoners"),
            #depending on war status we can enforce either message_positive or message_negative
            (try_for_range, ":troop_iterator", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
              (troop_is_hero, ":cur_troop_id"),

              (try_begin),
                #abort quest if troop loses a battle during rest time
                (check_quest_active, "qst_lend_surgeon"),
                (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, ":cur_troop_id"),
                (call_script, "script_abort_quest", "qst_lend_surgeon", 0),
              (try_end),

              (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),

              (troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),

              (store_random_in_range, ":rand", 0, 100),
              (str_store_troop_name_link, s1, ":cur_troop_id"),
              (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
              (store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
              (str_store_faction_name_link, s3, ":defeated_troop_faction"),
              #SB : colorize
              (faction_get_color, ":color", ":defeated_troop_faction"),
              (try_begin),
                (this_or_next|eq, ":nonempty_winner_party", "p_main_party"),
                (ge, ":rand", hero_escape_after_defeat_chance),

                #dckplmc
                (party_get_template_id, ":party_template", ":root_defeated_party"),
                (try_begin),
                    (eq, ":party_template", "pt_hero_party"),
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                    # (assign, ":continue", 1),
                    # (assign, ":minimum_distance", 99999),
                    # (assign, ":prison_center", -1),
                     # (try_for_range, ":center", walled_centers_begin, walled_centers_end),
                        # (store_distance_to_party_from_party, ":dist", ":center", ":root_defeated_party"),
                        # (lt, ":dist", ":minimum_distance"),
                        # (assign, ":minimum_distance", ":dist"),
                        # (assign, ":prison_center", ":center"),
                     # (try_end),
                      # (assign, reg1, ":prison_center"),
                      # #(display_message, "@{!}DEBUG : prison center is {reg1}"),
                      # (try_begin),
                        # (ge, ":prison_center", 0),
                        # (party_add_prisoners, ":prison_center", ":cur_troop_id", 1),
                        # (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":prison_center"),
                      # (else_try),
                        # (store_random_in_range, ":town_no", towns_begin, towns_end),
                        # (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                      # (try_end),
                (try_end),
                #(neq, ":party_template", "pt_hero_party"), #end




                (party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
                ##diplomacy start+ kingdom ladies might lead kingdom parties
                (this_or_next|is_between,":leader_troop_id", kingdom_ladies_begin, kingdom_ladies_end),
                   (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end),

                (this_or_next|troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
                ##diplomacy end+
                (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end), #disable non-kingdom parties capturing enemy lords
                (party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1),
                (gt, reg0, 0),
                #(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
                (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),

                (display_log_message, "str_hero_taken_prisoner", ":color"),

                (try_begin),
                  (call_script, "script_cf_prisoner_offered_parole", ":cur_troop_id"),

                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner granted parole"),
                  (try_end),

                  (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", 3),
				  (val_add, "$total_battle_enemy_changes", 3),
                (else_try),
                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner not offered parole"),
		          (try_end),

		          (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", -5),
				  (val_add, "$total_battle_enemy_changes", -5),
		        (try_end),

				(store_faction_of_party, ":capturer_faction", ":nonempty_winner_party"),
                (call_script, "script_update_troop_location_notes_prisoned", ":cur_troop_id", ":capturer_faction"),
              (else_try),

                #dckplmc
                (try_begin),
                    (party_get_template_id, ":party_template", ":root_defeated_party"),
                    (eq, ":party_template", "pt_hero_party"),
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (store_random_in_range, ":town_no", towns_begin, towns_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                (try_end),

                (display_message,"@{s1} of {s3} was defeated in battle but managed to escape.", ":color"),
              (try_end),

              (try_begin),
                (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (assign, "$marshall_defeated_in_battle", ":cur_troop_id"),
                #Marshall is defeated, refresh ai.
                (assign, "$g_recalculate_ais", 1),
              (try_end),

              ##diplomacy begin
              (try_begin),
                (call_script, "script_dplmc_is_affiliated_family_member", ":cur_troop_id"),
                (eq, reg0, 1),
                ##diplomacy start+ skip relationship decay for defeat when the player himself is imprisoned or wounded
					 (eq, "$g_player_is_captive", 0),
                (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
                (neg|troop_is_wounded, "trp_player"),
                ##diplomacy end+
					 (assign, ":mitigating_factors", 0),
					 (try_begin),
					    #Being at war with the troop's faction is a mitigating factor, unless the player leads his faction.
						 (store_relation, reg0, "$players_kingdom", ":cur_troop_faction"),
						 (lt, reg0, 0),
						 (neq, "$players_kingdom", "fac_player_supporters_faction"),
						 (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
						 (assign, ":mitigating_factors", 1),
					 (try_end),

                (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
					   ##diplomacy start+
						#The dead, exiled, and retired don't participate in this
						(neg|troop_slot_ge, ":family_member", slot_troop_occupation, slto_retirement),
						#Members of factions at war with the defeated affiliate's faction don't have
						#any relation loss either: it would be nonsensical for them to be willing to
						#battle him themselves, but become enraged at his defeat.
						(store_troop_faction, ":family_member_faction", ":family_member"),
						(store_relation, reg0, ":family_member_faction", ":cur_troop_faction"),
						(this_or_next|eq, ":family_member_faction", ":cur_troop_faction"),
							(ge, reg0, 0),
                  ##(call_script, "script_troop_get_family_relation_to_troop", ":family_member", "$g_player_affiliated_troop"),
                  (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
                  (gt, reg0, 0),
                  (assign, reg0, -2),
                  (try_begin),
                    (eq, ":reduce_campaign_ai", 0),#hard: -1
                    (assign, reg0, -1),
                  (else_try),
                    (eq, ":reduce_campaign_ai", 1),#medium: -1 or 0
                    (store_random_in_range, reg0, -1, 1),
                  (else_try),
                    (eq, ":reduce_campaign_ai", 2),#easy: 0
                    (assign, reg0, 0),
                  (try_end),
                  (val_add, reg0, ":mitigating_factors"),
                  (lt, reg0, 0),
                  (call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
                  ##diplomacy end+
                (try_end),
              (try_end),
              ##diplomacy end
            (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
             (else_try),
               (assign, ":num_stacks", 0),
             (try_end),
             (try_for_range, ":troop_iterator", 0, ":num_stacks"),
               (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
               (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
               (str_store_troop_name_link, s1, ":cur_troop_id"),
               (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
               (str_store_faction_name_link, s3, ":cur_troop_faction"),
               #SB : colorize, use previously set up primary color
               (display_log_message, "str_hero_freed", ":faction_color"),

                (try_begin), #dckplmc
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),
                    (store_random_in_range, ":town_no", towns_begin, towns_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                (try_end),
             (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_clear, "p_temp_party"),
               (assign, "$g_move_heroes", 0), #heroes are already processed above. Skip them here.
               (call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
               (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
               (distribute_party_among_party_group, "p_temp_party", ":root_winner_party"),

               (call_script, "script_battle_political_consequences", ":root_defeated_party", ":root_winner_party"),

               (call_script, "script_clear_party_group", ":root_defeated_party"),
             (try_end),
             (assign, ":trigger_result", 1), #End battle!

             #Center captured
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
               (this_or_next|eq, ":cur_party_type", spt_town),
               (eq, ":cur_party_type", spt_castle),

               #free all captive ladies
               (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                   (troop_get_slot, ":center", ":lady", slot_troop_prisoner_of_party),
                   (neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
                   (eq, ":root_defeated_party", ":center"),
                   (call_script, "script_remove_troop_from_prison", ":lady"),
                   (store_faction_of_troop, ":lady_faction", ":lady"),
                   (store_faction_of_party, ":rescue_faction", ":root_winner_party"),
                   (faction_get_color, ":lady_faction_color", ":lady_faction"),
                   (str_store_troop_name_link, s1, ":lady"),
                   (str_store_faction_name_link, s2, ":rescue_faction"),
                   (str_store_faction_name_link, s3, ":lady_faction"),
                   (display_log_message, "str_hero_freed", ":lady_faction_color"),
               (try_end),

               (assign, "$g_recalculate_ais", 1),

               (store_faction_of_party, ":winner_faction", ":root_winner_party"),
               (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),

               (str_store_party_name, s1, ":root_defeated_party"),
               (str_store_faction_name, s2, ":winner_faction"),
               (str_store_faction_name, s3, ":defeated_faction"),
               ## CC
               (faction_get_color, ":faction_color", ":winner_faction"),
               (display_log_message, "str_center_captured", ":faction_color"),
               ## CC

			   (store_current_hours, ":hours"),
			   (faction_set_slot, ":winner_faction", slot_faction_ai_last_decisive_event, ":hours"),

               (try_begin),
                 (eq, "$g_encountered_party", ":root_defeated_party"),
                 (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
                 (call_script, "script_change_player_relation_with_lords_after_battle"),
               (try_end),

               (try_begin),
                 (party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
                 (gt, ":num_stacks", 0),
                 (party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
		##diplomacy start+ support for promoted kingdom ladies
                 (is_between, ":leader_troop_no", heroes_begin, heroes_end),#<- dplmc+ added
                 (this_or_next|troop_slot_eq, ":leader_troop_no", slot_troop_occupation, slto_kingdom_hero),#<- dplmc+ addded
                     (is_between, ":leader_troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy end+
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
               (else_try),
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
               (try_end),

               (call_script, "script_lift_siege", ":root_defeated_party", 0),
               (call_script, "script_spawn_looters", ":root_defeated_party", 5), #SB : spawn some looters
               (store_faction_of_party, ":fortress_faction", ":root_defeated_party"),
			   (try_begin),
			     (is_between, ":root_defeated_party", towns_begin, towns_end),
			     (assign, ":damage", 40),
			   (else_try),
			     (assign, ":damage", 20),
			   (try_end),
			   (call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":fortress_faction", ":damage"),

               (call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"),
               (try_begin),
			     ##diplomacy start+ Handle player is co-ruler of faction
			     (assign, ":is_defeated_faction_coruler", 0),
            	 (try_begin),
            		##zerilius changes begin
            		(eq, ":defeated_faction", "$players_kingdom"),
            		# (eq, ":is_defeated_faction_coruler", "$players_kingdom"),
            		##zerilius changes end
            		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
            		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            		(assign, ":is_defeated_faction_coruler", 1),
            	 (try_end),
				 (this_or_next|eq, ":is_defeated_faction_coruler", 1),
	  		     ##diplomacy end+
                 (eq, ":defeated_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_center_lost", ":root_defeated_party", ":winner_faction"),
               (try_end),

               (party_get_num_attached_parties, ":num_attached_parties",  ":root_attacker_party"),
                 (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
                 (party_get_attached_party_with_rank, ":attached_party", ":root_attacker_party", ":attached_party_rank"),

                 (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
                 (assign, ":total_size", 0),
                 (try_for_range, ":i_stack", 0, ":num_stacks"),
                   (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
                   (val_add, ":total_size", ":stack_size"),
                 (try_end),

                 (try_begin),
                   (ge, ":total_size", 10),

                   (assign, ":stacks_added", 0),
                   (assign, ":last_random_stack", -1),

                   (assign, ":end_condition", 10),
                   (try_for_range, ":unused", 0, ":end_condition"),
                     (store_random_in_range, ":random_stack", 1, ":num_stacks"),
                     (party_stack_get_troop_id, ":random_stack_troop", ":attached_party", ":random_stack"),
                     (party_stack_get_size, ":stack_size", ":attached_party", ":random_stack"),
                     (ge, ":stack_size", 4),
                     (neq, ":random_stack", ":last_random_stack"),

                     (store_mul, ":total_size_mul_2", ":total_size", 2),
                     (assign, ":percentage", ":total_size_mul_2"),
                     (val_min, ":percentage", 100),

                     (val_mul, ":stack_size", ":percentage"),
                     (val_div, ":stack_size", 100),

                     (party_stack_get_troop_id, ":party_leader", ":attached_party", 0),

                     (try_begin),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_conventional),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_otherworldly),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_adventurous),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
                       (assign, reg2, 0),
                       (store_random_in_range, ":random_percentage", 40, 50), #average 45%
                     (else_try),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_ambitious),
                       ##diplmoacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
                       (assign, reg2, 1),
                       (store_random_in_range, ":random_percentage", 30, 40), #average 35%
                     (else_try),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_roguish),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
                       (assign, reg2, 2),
                       (store_random_in_range, ":random_percentage", 20, 30), #average 25%
                     (else_try),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_benefactor),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_custodian),
                       (assign, reg2, 3),
                       (store_random_in_range, ":random_percentage", 50, 60), #average 55%
                     (try_end),

                     (val_min, ":random_percentage", 100),
                     (val_mul, ":stack_size", ":random_percentage"),
                     (val_div, ":stack_size", 100),

                     (party_add_members, ":root_defender_party", ":random_stack_troop", ":stack_size"),
                     (party_remove_members, ":attached_party", ":random_stack_troop", ":stack_size"),

                     (val_add, ":stacks_added", 1),
                     (assign, ":last_random_stack", ":random_stack"),

                     (try_begin),
                       #if troops from three different stack is already added then break
                       (eq, ":stacks_added", 3),
                       (assign, ":end_condition", 0),
                     (try_end),
                   (try_end),
                 (try_end),
               (try_end),

               #Reduce prosperity of the center by 5
			   (try_begin),
			     (neg|is_between, ":root_defeated_party", castles_begin, castles_end),
			     (call_script, "script_change_center_prosperity", ":root_defeated_party", -5),
			     (val_add, "$newglob_total_prosperity_from_townloot", -5),
			   (try_end),
               (call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
             (try_end),
           (try_end),

           #ADD XP
           (try_begin),
             (party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),

             (assign, ":xp_gained_attacker", 200),
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (store_faction_of_party, ":root_attacker_party_faction", ":root_attacker_party"),
             (try_begin),
               (this_or_next|eq, ":root_attacker_party", "p_main_party"),
               (this_or_next|eq, ":root_attacker_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_attacker_party_faction", "$players_kingdom"),
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_attacker", 3),
               (val_div, ":xp_gained_attacker", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_attacker", 2),
             (try_end),

             (gt, ":new_attacker_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_attacker_party", ":xp_gained_attacker"),
           (try_end),
           (try_begin),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),

             (assign, ":xp_gained_defender", 200),
             (store_faction_of_party, ":root_defender_party_faction", ":root_defender_party"),
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (try_begin),
               (this_or_next|eq, ":root_defender_party", "p_main_party"),
               (this_or_next|eq, ":root_defender_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_defender_party_faction", "$players_kingdom"),
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_defender", 3),
               (val_div, ":xp_gained_defender", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_defender", 2),
             (try_end),

             (gt, ":new_defender_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_defender_party", ":xp_gained_defender"),
           (try_end),

           (try_begin),
             #ozan - do not randomly end battles aganist towns or castles.
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle), #added by ozan
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_town),   #added by ozan
             #end ozan

             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_attacker_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_attacker_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_defender_followers", ":root_defender_party", slot_party_follower_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_defender_followers"),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),

             (try_begin),
               (lt, ":random_num", 10),
               (assign, ":trigger_result", 1), #End battle!
             (try_end),
           (else_try),
             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),

             (val_mul, ":total_defender_strength", 13), #multiply defender strength with 1.3
             (val_div, ":total_defender_strength", 10),

             (gt, ":total_defender_strength", ":total_attacker_strength"),
             (gt, ":total_defender_strength", 3),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),

             (try_begin),
               (lt, ":random_num", 15), #15% is a bit higher than 10% (which is open area escape probability)
               (assign, ":trigger_result", 1), #End battle!

               (assign, "$g_recalculate_ais", 1), #added new

               (try_begin),
                 (eq, "$cheat_mode", 1),
                 (display_message, "@{!}DEBUG : Siege attackers are running away"),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
       (try_end),
       (set_trigger_result, ":trigger_result"),
  ])
]
