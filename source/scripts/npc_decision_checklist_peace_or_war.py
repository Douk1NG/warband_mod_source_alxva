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

npc_decision_checklist_peace_or_war_scripts = [
#script_encounter_agent_draw_weapon
(
	"npc_decision_checklist_peace_or_war",
	#this script is used to add a bit more color to diplomacy, particularly with regards to the player

	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	(store_script_param, ":envoy", 3),

	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a synonym for "the faction led by the player"
	#in many places, correct this here.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(assign, ":actor_strength", 0),
	(assign, ":target_strength", 0),
	(assign, ":actor_centers_held_by_target", 0),

#	(assign, ":two_factions_share_border", 0),
	(assign, ":third_party_war", 0),
	(assign, ":num_third_party_wars", 0),

	(assign, ":active_mutual_enemy", 0), #an active enemy with which the target is at war
	(assign, "$g_concession_demanded", 0),
	##diplomacy start+
	(assign, ":last_center_lost", 0),#  last center lost to the target faction
	(assign, ":last_center_lost_time", 0),# time the last center was lost to the target faction

	#"Third party" after taking into account alliances
	#(assign, ":actual_third_party_war", 0),
	(assign, ":num_actual_third_party_wars", 0),
	##diplomacy end+

	(store_relation, ":current_faction_relation", ":actor_faction", ":target_faction"),

	(try_begin),
		(eq, ":target_faction", "fac_player_supporters_faction"),
		(assign, ":modified_honor_and_relation", "$player_honor"), #this can be affected by the emissary's skill

		(val_add, ":target_strength", 2), #for player party
	(else_try),
		(assign, ":modified_honor_and_relation", 0), #this can be affected by the emissary's skill
	(try_end),

	(faction_get_slot, ":actor_leader", ":actor_faction", slot_faction_leader),
	(faction_get_slot, ":target_leader", ":target_faction", slot_faction_leader),

	(call_script, "script_troop_get_relation_with_troop", ":actor_leader", ":target_leader"),

	(assign, ":relation_bonus", reg0),
	(val_min, ":relation_bonus", 10),
	(val_add, ":modified_honor_and_relation", ":relation_bonus"),

	(str_store_troop_name, s15, ":actor_leader"),
	(str_store_troop_name, s16, ":target_leader"),


	(assign, ":war_damage_suffered", 0),
	(assign, ":war_damage_inflicted", 0),

	(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":actor_faction", ":target_faction"),
	(assign, ":war_peace_truce_status", reg0),
	(str_clear, s12),
	(try_begin),
		(eq, ":war_peace_truce_status", -2),
		(str_store_string, s12, "str_s15_is_at_war_with_s16_"),

		(store_add, ":war_damage_inflicted_slot", ":target_faction", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":war_damage_inflicted_slot", kingdoms_begin),
		(faction_get_slot, ":war_damage_inflicted", ":actor_faction", ":war_damage_inflicted_slot"),

		(store_add, ":war_damage_suffered_slot", ":actor_faction", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":war_damage_suffered_slot", kingdoms_begin),
		(faction_get_slot, ":war_damage_suffered", ":target_faction", ":war_damage_suffered_slot"),


	(else_try),
		#truce in effect
		(eq, ":war_peace_truce_status", 1),
		(str_store_string, s12, "str_in_the_short_term_s15_has_a_truce_with_s16_as_a_matter_of_general_policy_"),
	(else_try),
		#provocation noted
		(eq, ":war_peace_truce_status", -1),
		(str_store_string, s12, "str_in_the_short_term_s15_was_recently_provoked_by_s16_and_is_under_pressure_to_declare_war_as_a_matter_of_general_policy_"),
	(try_end),

	#clear for dialog with lords
	(try_begin),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(str_clear, s12),
	(try_end),

	(try_begin),
		(gt, ":envoy", -1),
		(store_skill_level, ":persuasion_x_2", "skl_persuasion", ":envoy"),
		(val_mul, ":persuasion_x_2", 2),
		(val_add, ":modified_honor_and_relation", ":persuasion_x_2"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":modified_honor_and_relation"),
			(display_message, "str_envoymodified_diplomacy_score_honor_plus_relation_plus_envoy_persuasion_=_reg4"),
		(try_end),

	(try_end),


	(try_for_range, ":kingdom_to_reset", kingdoms_begin, kingdoms_end),
		(faction_set_slot, ":kingdom_to_reset", slot_faction_temp_slot, 0),
	(try_end),

	(try_for_parties, ":party_no"),
		(assign, ":party_value", 0),
		(try_begin),
			(is_between, ":party_no", towns_begin, towns_end),
			(assign, ":party_value", 3),
		(else_try),
			(is_between, ":party_no", castles_begin, castles_end),
			(assign, ":party_value", 2),
		(else_try),
			(is_between, ":party_no", villages_begin, villages_end),
			(assign, ":party_value", 1),
		(else_try),
			(party_get_template_id, ":template", ":party_no"),
			(eq, ":template", "pt_kingdom_hero_party"),
			(assign, ":party_value", 2),
		(try_end),


		(store_faction_of_party, ":party_current_faction", ":party_no"),
		(party_get_slot, ":party_original_faction", ":party_no", slot_center_original_faction),
		(party_get_slot, ":party_ex_faction", ":party_no", slot_center_ex_faction),


		#total strengths
		(try_begin),
			(is_between, ":party_current_faction", kingdoms_begin, kingdoms_end),
			(faction_get_slot, ":faction_strength", ":party_current_faction", slot_faction_temp_slot),
			(val_add, ":faction_strength", ":party_value"),
			(faction_set_slot, ":party_current_faction", slot_faction_temp_slot, ":faction_strength"),
		(try_end),


		(try_begin),
			(eq, ":party_current_faction", ":target_faction"),
			(val_add, ":target_strength", ":party_value"),

			(try_begin),
				(this_or_next|eq, ":party_original_faction", ":actor_faction"),
					(eq, ":party_ex_faction", ":actor_faction"),
				(val_add, ":actor_centers_held_by_target", 1),
				(try_begin),
					(is_between, ":party_no", walled_centers_begin, walled_centers_end),
					(assign, "$g_concession_demanded", ":party_no"),
					(str_store_party_name, s18, "$g_concession_demanded"),
					##diplomacy start+ Also track the most recently taken walled center
					(eq, ":party_ex_faction", ":actor_faction"),
					(this_or_next|lt, ":last_center_lost", 1),
						(party_slot_ge, ":party_no", dplmc_slot_center_last_transfer_time, ":last_center_lost_time"),
					(assign, ":last_center_lost", ":party_no"),
					(party_get_slot, ":last_center_lost_time", ":party_no", dplmc_slot_center_last_transfer_time),
					##diplomacy end+
				(try_end),
			(try_end),

# Could include two factions share border, but war is unlikely to break out in the first place unless there is a common border

#			(try_begin),
#				(is_between, ":party_no", walled_centers_begin, walled_centers_end),
#				(try_for_range, ":other_center", walled_centers_begin, walled_centers_end),
#					(assign, ":two_factions_share_border", 0),
#					(store_faction_of_party, ":other_faction", ":other_center"),
#					(eq, ":other_faction", ":actor_faction"),
#					(store_distance_to_party_from_party, ":distance", ":party_no", ":other_center"),
#					(le, ":distance", 15),
#					(assign, ":two_factions_share_border", 1),
#				(try_end),
#			(try_end),
		(else_try),
			(eq, ":party_current_faction", ":actor_faction"),
			(val_add, ":actor_strength", ":party_value"),
		(try_end),
	(try_end),

	#Total Calradia strength = 110 x 1 (villages,), 48? x 2 castles, 22 x 3 towns, 88 x 2 lord parties = 272 + 176 = 448
	(assign, ":strongest_kingdom", -1),
	(assign, ":score_to_beat", 60), #Maybe raise once it works
	##diplomacy start+
	#Take into account alliances
	(assign, ":strongest_kingdom_offensive", -1),
	(assign, ":strongest_kingdom_offensive_score", -1),

	(assign, ":strongest_kingdom_defensive", -1),
	(assign, ":strongest_kingdom_defensive_score", -1),

	(faction_get_slot, ":actor_offensive_score", ":actor_faction", slot_faction_temp_slot),
	(faction_get_slot, ":actor_defensive_score", ":actor_faction", slot_faction_temp_slot),

	#(faction_get_slot, ":target_offensive_score", ":target_faction", slot_faction_temp_slot),
	(faction_get_slot, ":target_defensive_score", ":target_faction", slot_faction_temp_slot),

	#Use these instead of just counting the number of factions
    (assign, ":strength_against_actor", 0),
	(assign, ":strength_against_target", 0),

	##diplomacy end+
	(try_for_range, ":strongest_kingdom_candidate", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":candidate_strength", ":strongest_kingdom_candidate", slot_faction_temp_slot),
		##diplomacy start+
		#Take into account allies
		(assign, ":candidate_offensive_score", ":candidate_strength"),
		(assign, ":candidate_defensive_score", ":candidate_strength"),
		(try_for_range, ":other_kingdom", kingdoms_begin, kingdoms_end),
		   (neq, ":other_kingdom", ":strongest_kingdom_candidate"),
			(faction_get_slot, ":other_kingdom_strength", ":other_kingdom", slot_faction_temp_slot),
			(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":strongest_kingdom_candidate", ":other_kingdom"),
			#Add 90% rather than 100%, because otherwise, if several kingdoms are
			#allied all of them will have the same strength by this measurement.
			(try_begin),
					 #Full alliance
					 (gt, reg0, dplmc_treaty_alliance_days_expire),
					 (store_mul, reg0, ":other_kingdom_strength", 9),
					 (val_div, reg0, 10),
					 (val_add, ":candidate_offensive_score", reg0),
					 (val_add, ":candidate_defensive_score", reg0),
			(else_try),
					 #Defensive alliance
					 (gt, reg0, dplmc_treaty_defense_days_expire),
					 (store_mul, reg0, ":other_kingdom_strength", 9),
					 (val_div, reg0, 10),
					 (val_add, ":candidate_defensive_score", reg0),
			(try_end),
		(try_end),
		#Update actor/target strengths with alliances, and "strength against"
		(try_begin),
			(eq, ":strongest_kingdom_candidate", ":actor_faction"),
			(assign, ":actor_offensive_score", ":candidate_offensive_score"),
			(assign, ":actor_defensive_score", ":candidate_defensive_score"),
		(else_try),
			(store_relation, ":relation", ":strongest_kingdom_candidate", ":actor_faction"),
			(lt, ":relation", 0),
			(val_add, ":strength_against_actor", ":other_kingdom_strength"),
		(try_end),
		(try_begin),
			(eq, ":strongest_kingdom_candidate", ":target_faction"),
			#(assign, ":target_offensive_score", ":candidate_offensive_score"),
			(assign, ":target_defensive_score", ":candidate_defensive_score"),
		(else_try),
			(store_relation, ":relation", ":strongest_kingdom_candidate", ":target_faction"),
			(lt, ":relation", 0),
			(val_add, ":strength_against_target", ":other_kingdom_strength"),
		(try_end),
		#Update global max/min
		(try_begin),
			(gt, ":candidate_offensive_score", ":strongest_kingdom_offensive_score"),
			(assign, ":strongest_kingdom_offensive", ":strongest_kingdom_candidate"),
			(assign, ":strongest_kingdom_offensive_score", ":candidate_offensive_score"),
		(try_end),
		(try_begin),
			(gt, ":candidate_defensive_score", ":strongest_kingdom_defensive_score"),
			(assign, ":strongest_kingdom_defensive", ":strongest_kingdom_candidate"),
			(assign, ":strongest_kingdom_defensive_score", ":candidate_defensive_score"),
		(try_end),
		##diplomacy end+
		(gt, ":candidate_strength", ":score_to_beat"),
		(assign, ":strongest_kingdom", ":strongest_kingdom_candidate"),
		(assign, ":score_to_beat", ":candidate_strength"),
	(try_end),


	(try_begin),
		(eq, "$cheat_mode", 2),
		(gt, ":strongest_kingdom", 1),
		(str_store_faction_name, s4, ":strongest_kingdom"),
		(assign, reg3, ":score_to_beat"),
		(display_message, "@{!}DEBUG - {s4} strongest kingdom with {reg3} strength"),
		##diplomacy start+ Show strongest counting alliances if it's different
		(try_begin),
			(gt, ":strongest_kingdom_offensive", 0),
			(neq, ":strongest_kingdom_offensive", ":strongest_kingdom"),
			(str_store_faction_name, s4, ":strongest_kingdom_offensive"),
			(assign, reg3, ":strongest_kingdom_offensive_score"),
			(display_message, "@{!}DEBUG - including offensive and defensive alliances {s4} strongest kingdom with {reg3} strength"),
		(try_end),
		(try_begin),
			(gt, ":strongest_kingdom_defensive", 0),
			(neq, ":strongest_kingdom_defensive", ":strongest_kingdom"),
			(neq, ":strongest_kingdom_defensive", ":strongest_kingdom_offensive"),
			(str_store_faction_name, s4, ":strongest_kingdom_defensive"),
			(assign, reg3, ":strongest_kingdom_defensive_score"),
			(display_message, "@{!}DEBUG - including only defensive alliances {s4} strongest kingdom with {reg3} strength"),
		(try_end),
		#Revert values
		(assign, reg3, ":score_to_beat"),
		(str_store_faction_name, s4, ":strongest_kingdom"),
		##diplomacy end+
	(try_end),


	(assign, ":strength_ratio", 1),
	(try_begin),
		(gt, ":actor_strength", 0),
		(store_mul, ":strength_ratio", ":target_strength", 100),
		(val_div, ":strength_ratio", ":actor_strength"),
	(try_end),
	##diplomacy start+
	#Other strength ratios using strengths counting alliances
	(assign, ":strength_ratio_new_attack", 1),
	(try_begin),
		(gt, ":actor_offensive_score", 0),
		(store_mul, ":strength_ratio_new_attack", ":target_defensive_score", 100),
		(val_div, ":strength_ratio_new_attack", ":actor_offensive_score"),
	(try_end),
	(assign, ":strength_ratio_current_war", 1),
	(try_begin),
		(gt, ":actor_defensive_score", 0),
		(store_mul, ":strength_ratio_current_war", ":target_defensive_score", 100),
		(val_div, ":strength_ratio_current_war", ":actor_defensive_score"),
	(try_end),
	#Calculate the total magnitude of the forces hostile to the faction versus its allies
	(assign, ":strength_ratio_all_enemies_actor", 1),
	(try_begin),
		(gt, ":actor_defensive_score", 0),
		(store_mul, ":strength_ratio_all_enemies_actor", ":strength_against_actor", 100),
		(val_div, ":strength_ratio_all_enemies_actor", ":actor_defensive_score"),
	(try_end),
	##diplomacy end+

	(try_for_range, ":possible_mutual_enemy", kingdoms_begin, kingdoms_end),
		(neq, ":possible_mutual_enemy", ":target_faction"),
		(neq, ":possible_mutual_enemy", ":actor_faction"),
		(faction_slot_eq, ":possible_mutual_enemy", slot_faction_state, sfs_active),

		(store_relation, ":relation", ":possible_mutual_enemy", ":actor_faction"),
		(lt, ":relation", 0),
		(assign, ":third_party_war", ":possible_mutual_enemy"),
		(val_add, ":num_third_party_wars", 1),

		##diplomacy start+
		##ACTUAL third-party wars (i.e. not allied to the target faction)
		(call_script, "script_dplmc_get_faction_truce_length_with_faction", ":target_faction", ":possible_mutual_enemy"),
		(try_begin),
			(neg|gt, reg0, dplmc_treaty_defense_days_expire),
			#(assign, ":actual_third_party_war", ":possible_mutual_enemy"),
			(val_add, ":num_actual_third_party_wars", 1),
		(try_end),
		##diplomacy end+

		(store_relation, ":relation", ":possible_mutual_enemy", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":active_mutual_enemy", ":possible_mutual_enemy"),
	(try_end),

	(store_current_hours, ":cur_hours"),
    (faction_get_slot, ":faction_ai_last_decisive_event", ":actor_faction", slot_faction_ai_last_decisive_event),
    (store_sub, ":hours_since_last_decisive_event", ":cur_hours", ":faction_ai_last_decisive_event"),

	##diplomacy start+ use gender script
	(call_script, "script_dplmc_store_troop_is_female_reg", ":actor_leader", 4),
	##diplomacy end+

	(try_begin),
		(gt, "$supported_pretender", 0),
		(this_or_next|eq, "$supported_pretender", ":actor_leader"),
			(eq, "$supported_pretender", ":target_leader"),
		(this_or_next|eq, ":actor_faction", "$supported_pretender_old_faction"),
            (eq, ":target_faction", "$supported_pretender_old_faction"),

		(assign, ":result", -3),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_cannot_negotiate_with_s16_as_to_do_so_would_undermine_reg4herhis_own_claim_to_the_throne_this_civil_war_must_almost_certainly_end_with_the_defeat_of_one_side_or_another"),
	(else_try),
		(lt, ":modified_honor_and_relation", -20),
		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|lt, ":strength_ratio_current_war", 125),
		##diplomacy end+
		(lt, ":strength_ratio", 125),
		(lt, ":war_damage_suffered", 400),
		(this_or_next|neq, ":war_peace_truce_status", -2),
			(lt, ":hours_since_last_decisive_event", 720),
		##diplomacy start+ Examine strength of enemies versus allies
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 125),
		##diplomacy end+
		(eq, ":num_third_party_wars", 0),

		(assign, ":result", -3),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
	(else_try),
		(gt, ":actor_centers_held_by_target", 0),
		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (display_message, "@{!}Actor centers held by target noted"),
		(try_end),

		(lt, ":war_damage_suffered", 200),
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}War damage under minimum"),
		(try_end),

		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|lt, ":strength_ratio_current_war", 125),
		##diplomacy end+
		(lt, ":strength_ratio", 125),
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}Strength ratio correct"),
		(try_end),
		##diplomacy start+ Examine strength of enemies versus allies
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 125),
		##diplomacy end+
		(eq, ":num_third_party_wars", 0),
		(try_begin),
		  (eq, "$cheat_mode", 1),
          (display_message, "@{!}Third party wars"),
		(try_end),

		(assign, ":result", -2),
		(assign, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
	(else_try),
		(eq, ":war_peace_truce_status", -2),
		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|lt, ":strength_ratio_current_war", 125),
		##diplomacy end+
		(lt, ":strength_ratio", 125),
		(le, ":num_third_party_wars", 1),
		(ge, ":war_damage_inflicted", 5),
		(this_or_next|neq, ":war_peace_truce_status", -2),
			(lt, ":hours_since_last_decisive_event", 720),

		(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
		(gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),

		(assign, ":result", -2),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_feels_that_reg4shehe_is_winning_the_war_against_s16_and_sees_no_reason_not_to_continue"),
	(else_try),
		(le, ":war_peace_truce_status", -1),

		(this_or_next|eq, ":war_peace_truce_status", -1), #either a war is just beginning, or there is a provocation
			(le, ":war_damage_inflicted", 1),
		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|lt, ":strength_ratio_new_attack", 150),
		##diplomacy end+
		(lt, ":strength_ratio", 150),
		##diplomacy start+ Examine strength of enemies versus allies
		(this_or_next|lt, ":strength_ratio_all_enemies_actor", 150),
		##diplomacy end+
		(eq, ":num_third_party_wars", 0),

		(faction_slot_ge, ":actor_faction", slot_faction_instability, 60),

		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
	(else_try),
		(eq, ":war_peace_truce_status", -2),
		(lt, ":war_damage_inflicted", 100),
		(eq, ":num_third_party_wars", 1),

		(assign, ":result", -1),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12even_though_reg4shehe_is_fighting_on_two_fronts_s15_is_inclined_to_continue_the_war_against_s16_for_a_little_while_longer_for_the_sake_of_honor"),

	(else_try),
		(eq, ":war_peace_truce_status", -2),
		(lt, ":war_damage_inflicted", 100),
		(eq, ":num_third_party_wars", 0),

		(assign, ":result", -1),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_feels_that_reg4shehe_must_pursue_the_war_against_s16_for_a_little_while_longer_for_the_sake_of_honor"),
	(else_try),
		(this_or_next|faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_attacking_center),
		(this_or_next|faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_raiding_village),
			(faction_slot_eq, ":actor_faction", slot_faction_ai_state, sfai_attacking_enemy_army),
		(faction_get_slot, ":offensive_object", ":actor_faction", slot_faction_ai_object),
		(party_is_active, ":offensive_object"),
		(store_faction_of_party, ":offensive_object_faction", ":offensive_object"),
		(eq, ":offensive_object_faction", ":target_faction"),
		(str_store_party_name, s17, ":offensive_object"),

		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_is_currently_on_the_offensive_against_s17_now_held_by_s16_and_reluctant_to_negotiate"),


	(else_try),
		#Attack strongest kingdom, if it is also at war
		##diplomacy start+ Take into account strengths including alliances
		(this_or_next|eq, ":strongest_kingdom_offensive", ":target_faction"),
		##diplomacy end+
		(eq, ":strongest_kingdom", ":target_faction"),
		(eq, ":num_third_party_wars", 0),

		#Either not at war, or at war for two months
		(this_or_next|ge, ":war_peace_truce_status", -1),
			(lt, ":hours_since_last_decisive_event", 1440),

#		(eq, ":two_factions_share_border", 0),

		(assign, ":at_least_one_other_faction_at_war_with_strongest", 0),
		(try_for_range, ":kingdom_to_check", kingdoms_begin, kingdoms_end),
			(neq, ":kingdom_to_check", ":actor_faction"),
			(neq, ":kingdom_to_check", ":target_faction"),
			(faction_slot_eq, ":kingdom_to_check", slot_faction_state, sfs_active),
			(store_relation, ":relation_of_factions", ":kingdom_to_check", ":target_faction"),
			(lt, ":relation_of_factions", 0),
			(assign, ":at_least_one_other_faction_at_war_with_strongest", 1),
		(try_end),
		(eq, ":at_least_one_other_faction_at_war_with_strongest", 1),


		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),

	#bid to conquer all Calradia
	(else_try),
		(eq, ":num_third_party_wars", 0),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- No third party wars for {s15}"),
		(try_end),
		(eq, ":actor_faction", ":strongest_kingdom"),
		#peace with no truce or provocation

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} is strongest kingdom"),
		(try_end),


		(faction_get_slot, ":actor_strength", ":actor_faction", slot_faction_temp_slot),
		(faction_get_slot, ":target_strength", ":target_faction", slot_faction_temp_slot),
		(store_sub, ":strength_difference", ":actor_strength", ":target_strength"),
		##diplomacy start+ Include bonus from alliance
		(store_sub, reg0, ":actor_offensive_score", ":target_defensive_score"),
		(this_or_next|ge, reg0, 30),
		##diplomacy end+
		(ge, ":strength_difference", 30),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} has 30 point advantage over {s16}"),
		(try_end),


		(assign, ":nearby_center_found", 0),
		(try_for_range, ":actor_faction_walled_center", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":walled_center_faction_1", ":actor_faction_walled_center"),
			(eq, ":walled_center_faction_1", ":actor_faction"),
			(try_for_range, ":target_faction_walled_center", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":walled_center_faction_2", ":target_faction_walled_center"),
				(eq, ":walled_center_faction_2", ":target_faction"),
				(store_distance_to_party_from_party, ":distance", ":target_faction_walled_center", ":actor_faction_walled_center"),
				(lt, ":distance", 25),
				(assign, ":nearby_center_found", 1),
			(try_end),
		(try_end),
		(eq, ":nearby_center_found", 1),


		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- {s15} has proximity to {s16}"),
		(try_end),

		(assign, ":result", -1),
		(assign, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),

	(else_try),
		(lt, ":modified_honor_and_relation", -20),

		(assign, ":result", 0),
		(assign, ":explainer_string", "str_s12s15_distrusts_s16_and_fears_that_any_deals_struck_between_the_two_realms_will_not_be_kept"),


	#wishes to deal
	(else_try),
		(lt, ":current_faction_relation", 0),
		(ge, ":num_third_party_wars", 2),
		(assign, ":result", 3),

		(assign, ":explainer_string", "str_s12s15_is_at_war_on_too_many_fronts_and_eager_to_make_peace_with_s16"),
	(else_try),
		(gt, ":active_mutual_enemy", 0),
		(eq, ":actor_centers_held_by_target", 0),
		(this_or_next|ge, ":current_faction_relation", 0),
#			(eq, ":two_factions_share_border", 0),
			(eq, 1, 1),

		(assign, ":result", 3),
		(str_store_faction_name, s17, ":active_mutual_enemy"),
		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+
		(assign, ":explainer_string", "str_s12s15_seems_to_think_that_s16_and_reg4shehe_have_a_common_enemy_in_the_s17"),

	(else_try),
		(eq, ":war_peace_truce_status", -2),
		(ge, ":hours_since_last_decisive_event", 720),

		##diplomacy start+
		#(troop_get_type, reg4, ":actor_leader"),#<- commented out
		##diplomacy end+

		(assign, ":result", 2),
		(assign, ":explainer_string", "str_s12s15_feels_frustrated_by_reg4herhis_inability_to_strike_a_decisive_blow_against_s16"),


	(else_try),
		(lt, ":current_faction_relation", 0),
		(gt, ":war_damage_suffered", 100),

		(val_mul, ":war_damage_suffered_x_2", 2),
		(lt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),

		(assign, ":result", 2),
		(assign, ":explainer_string", "str_s12s15_has_suffered_enough_in_the_war_with_s16_for_too_little_gain_and_is_ready_to_pursue_a_peace"),

	(else_try),
		(gt, ":third_party_war", 0),
		(ge, ":modified_honor_and_relation", 0),
		(lt, ":current_faction_relation", 0),

		(assign, ":result", 1),
		(str_store_faction_name, s17, ":third_party_war"),
		(assign, ":explainer_string", "str_s12s15_would_like_to_firm_up_a_truce_with_s16_to_respond_to_the_threat_from_the_s17"),
	(else_try),
		(gt, ":third_party_war", 0),
		(ge, ":modified_honor_and_relation", 0),

		(assign, ":result", 1),
		(str_store_faction_name, s17, ":third_party_war"),
		(assign, ":explainer_string", "str_s12s15_wishes_to_be_at_peace_with_s16_so_as_to_pursue_the_war_against_the_s17"),
	(else_try),
		(gt, ":strength_ratio", 175),
#		(eq, ":two_factions_share_border", 1),

		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_seems_to_be_intimidated_by_s16_and_would_like_to_avoid_hostilities"),
	(else_try),
		(lt, ":current_faction_relation", 0),

		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_has_no_particular_reason_to_continue_the_war_with_s16_and_would_probably_make_peace_if_given_the_opportunity"),
	(else_try),
		(assign, ":result", 1),
		(assign, ":explainer_string", "str_s12s15_seems_to_be_willing_to_improve_relations_with_s16"),
	(try_end),
	##diplomacy start+
	#Possibly change the concession demanded
	(try_begin),
		(gt, "$g_concession_demanded", 0),
		(gt, ":last_center_lost", 0),
		(neq, "$g_concession_demanded", ":last_center_lost"),
		(try_begin),
			#This logically can't happen due to the order centers appear in
			(is_between, "$g_concession_demanded", towns_begin, towns_end),
			(neg|is_between, ":last_center_lost", towns_begin, towns_end),#Do not replace
		(else_try),
			(is_between, ":last_center_lost", towns_begin, towns_end),
			(neg|is_between, "$g_concession_demanded", towns_begin, towns_end),
			(assign, "$g_concession_demanded", ":last_center_lost"),
		(else_try),
			(party_slot_eq, ":last_center_lost", slot_center_original_faction, ":actor_faction"),
			(neg|party_slot_eq, "$g_concession_demanded", slot_center_original_faction, ":actor_faction"),
			(assign, "$g_concession_demanded", ":last_center_lost"),
		(try_end),
		(eq, "$g_concession_demanded", ":last_center_lost"),
		(str_store_party_name, s18, "$g_concession_demanded"),#change s18 to match
	(try_end),
	##diplomacy end+
	(str_store_string, s14, ":explainer_string"),
	(assign, reg0, ":result"),
	(assign, reg1, ":explainer_string"),

	])
]
