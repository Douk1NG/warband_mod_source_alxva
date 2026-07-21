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

npc_decision_checklist_take_stand_on_issue_scripts = [
("npc_decision_checklist_take_stand_on_issue",
	#Called from dialogs, and from simple_triggers

	#This a very inefficient checklist, and if I did it again, I would score for each troop. That way the troop could answer "why not" to an individual lord
	[
	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":troop_faction", ":troop_no"),

	(assign, ":result", -1),
	(faction_get_slot, ":faction_issue", ":troop_faction", slot_faction_political_issue),

	(assign, ":player_declines_honor", 0),
	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
	    (gt, "$g_dont_give_fief_to_player_days", 1),
		(assign, ":player_declines_honor", 1),
	(else_try),
	    (gt, "$g_dont_give_marshalship_to_player_days", 1),
		(assign, ":player_declines_honor", 1),
	(try_end),

	##diplomacy start+
	(faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":affiliated_with_player", reg0),

	(assign, ":subaltern_gender", -1),#The gender subject to sexism (as far as leadership is concerned).
	(try_begin),
		(lt, "$g_disable_condescending_comments", 2),#Prejudice not disabled
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),#Don't bother with the rest of the check
		(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),#if the lord has an unbiased outlook.
		(neg|troop_slot_ge, ":troop_no", slot_lord_reputation_type, lrep_roguish),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(store_sub, ":subaltern_gender", 1, reg0),
		(try_begin),
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", ":troop_faction", ":subaltern_gender"),
		(else_try),
			(assign, ":subaltern_gender", -1),
		(try_end),
	(try_end),

	(assign, ":faction_lord_count", 0),#Keep track of the number of lords in the faction
	##diplomacy end+

	(assign, ":total_faction_renown", 0),
	(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
	(try_begin),
		(eq, "$players_kingdom", ":troop_faction"),
		(eq, "$player_has_homage", 1),
		(troop_get_slot, ":total_faction_renown", "trp_player", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(eq, ":subaltern_gender", "$character_gender"),
			(val_mul, ":total_faction_renown", 4),
			(val_add, ":total_faction_renown", 3),
			(val_div, ":total_faction_renown", 5),
		(try_end),
		##diplomacy end+
	(try_end),

##diplomacy start+
	(try_for_range, ":active_npc", heroes_begin, heroes_end),#Changed range to include kingdom ladies
	    (troop_set_slot, ":active_npc", dplmc_slot_troop_temp_slot, 0), #this will hold distance to closest owned fief
##diplomacy end+
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0), #reset to zero

		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":active_npc_faction", ":troop_faction"),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		##diplomacy start+
		#Increment the faction lord count
		(val_add, ":faction_lord_count", 1),

		(try_begin),#If the player has set the prejudice mode to "high".
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		##diplomacy end+
		(val_add, ":total_faction_renown", ":renown"),
	(try_end),


	(assign, ":total_faction_center_value", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", ":troop_faction"),

		(assign, ":center_value", 1),
		(try_begin),
		##diplomacy start+
		#Use different scoring scheme
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			(try_begin),
			   (party_slot_eq, ":center", slot_party_type, spt_town),
  			   (assign, ":center_value", 3),
			(else_try),
			   (neg|party_slot_eq, ":center", slot_party_type, spt_village),
			   (this_or_next|party_slot_eq, ":center", slot_party_type, spt_castle),
				(is_between, ":center", walled_centers_begin, walled_centers_end),
			   (assign, ":center_value", 2),
			(try_end),
		#Otherwise fall through to old behavior
		(else_try),
		##diplomacy end+
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":center_value", 2),
		(try_end),

		(val_add, ":total_faction_center_value", ":center_value"),

		(party_get_slot, ":town_lord", ":center", slot_town_lord),
		##diplomacy start+
		#The rest of the script assumes that non-player lords are heroes,
		#so add that condition here to get the count right.
		#(gt, ":town_lord", -1),
		(this_or_next|eq, ":town_lord", "trp_player"),
			(is_between, ":town_lord", heroes_begin, heroes_end),

		#Calculate distance for alternate scoring if the issue is a center
		(try_begin),
			(is_between, ":faction_issue", centers_begin, centers_end),
			(neq, ":center", ":faction_issue"),
			(troop_get_slot, ":dplmc_temp_slot", ":town_lord", dplmc_slot_troop_temp_slot),
			(store_distance_to_party_from_party, reg0, ":center", ":faction_issue"),
			(gt, reg0, 0),
			(try_begin),
				(eq, ":dplmc_temp_slot", 0),
				(assign, ":dplmc_temp_slot", reg0),
			(else_try),
				(val_min, ":dplmc_temp_slot", reg0),
			(try_end),
			(troop_set_slot, ":town_lord", dplmc_slot_troop_temp_slot, ":dplmc_temp_slot"),
		(try_end),
		##diplomacy end+

		(troop_get_slot, ":temp_slot", ":town_lord", slot_troop_temp_slot),
		(val_add, ":temp_slot", ":center_value"),
		(troop_set_slot, ":town_lord", slot_troop_temp_slot, ":temp_slot"),
	(try_end),
	(val_max, ":total_faction_center_value", 1),

	(store_div, ":average_renown_per_center_point", ":total_faction_renown", ":total_faction_center_value"),
	##diplomacy start+
	(val_max, ":faction_lord_count", 1),

#	(store_mul, ":avg_renown_plus_500_per_cp", ":faction_lord_count", 500),
#	(val_add, ":avg_renown_plus_500_per_cp", ":total_faction_renown"),
#	(store_add, reg0, ":total_faction_center_value", ":faction_lord_count"),
#	(val_div, ":avg_renown_plus_500_per_cp", reg0),

	#Get the standard deviation of renown per center point
	(assign, ":renown_per_center_point_variance", 0),
#	(assign, ":renown_plus_500_per_center_point_variance", 0),

	(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
		(store_sub, ":active_npc_faction", ":troop_faction", 1),#guaranteed not to equal
		(try_begin),
			#handle player
			(eq, ":active_npc", active_npcs_including_player_begin),
			(assign, ":active_npc", "trp_player"),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(assign, ":active_npc_faction", ":troop_faction"),
		(else_try),
			#handle kingdom heroes
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(try_end),

		(eq, ":active_npc_faction", ":troop_faction"),

		(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
			(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
			(eq, reg0, ":subaltern_gender"),
			(val_mul, ":renown", 4),
			(val_add, ":renown", 3),
			(val_div, ":renown", 5),
		(try_end),
		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
		#Variance for renown / center points
		(val_max, ":center_points", 1),
		(store_div, reg0, ":renown", ":center_points"),
		(val_sub, reg0, ":average_renown_per_center_point"),
		(val_mul, reg0, reg0),
		(val_add, ":renown_per_center_point_variance", reg0),

#		#Variance for renown + 500 / center points + 1
#		(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
#		(val_add, ":center_points", 1),
#		(store_add, reg0, ":renown", 500),
#		(val_div, reg0, ":center_points"),
#		(val_sub, reg0, ":avg_renown_plus_500_per_cp"),
#		(val_mul, reg0, reg0),
#		(val_add, ":renown_plus_500_per_center_point_variance", reg0),
	(try_end),

	#Get renown per center point standard deviation, or 10%, whichever is greater
	(store_div, reg0, ":faction_lord_count", 2),#for rounding
	(val_add, ":renown_per_center_point_variance", reg0),
	(val_div, ":renown_per_center_point_variance", 	":faction_lord_count"),

	(assign, reg0, ":renown_per_center_point_variance"),
	(convert_to_fixed_point, reg0),
	(store_sqrt, reg0, reg0),
	(convert_from_fixed_point, reg0),
	(assign, ":renown_per_center_point_standard_deviation", reg0),
	(val_add, reg0, 5),
	(val_div, reg0, 10),
	(val_max, ":renown_per_center_point_standard_deviation", reg0),
	(store_sub, ":renown_low_target", ":average_renown_per_center_point", ":renown_per_center_point_standard_deviation"),
	(val_max, ":renown_low_target", 0),

#	#Get (renown + 500) per (center point plus one) standard deviation, or 10%, whichever is greater
#	(store_div, reg0, ":faction_lord_count", 2),#for rounding
#	(val_add, ":renown_plus_500_per_center_point_variance", reg0),
#	(val_div, ":renown_plus_500_per_center_point_variance", ":faction_lord_count"),
#
#	(assign, reg0, ":renown_plus_500_per_center_point_variance"),
#	(convert_to_fixed_point, reg0),
#	(store_sqrt, reg0, reg0),
#	(convert_from_fixed_point, reg0),
#	(assign, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(val_add, reg0, 5),
#	(val_div, reg0, 10),
#	(val_max, ":renown_plus_500_per_center_point_standard_deviation", reg0),
#	(store_sub, ":renown_500_low_target", ":avg_renown_plus_500_per_cp", ":renown_plus_500_per_center_point_standard_deviation"),
#	(val_max, ":renown_500_low_target", 0),
	##diplomacy end+

	(try_begin),
		(is_between, ":faction_issue", centers_begin, centers_end),
		#NOTE -- The algorithms here might seem a bit repetitive, but are designed that way to create internal cliques among the lords in a faction.



		(try_begin),#If the center is a village, and a lord has no fief, choose him
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),

			(is_between, ":faction_issue", villages_begin, villages_end),
			(assign, ":favorite_lord_without_center", -1),
			(assign, ":score_to_beat", -1),
			##diplomacy start+
			(try_begin),
				#With changes enabled, widen the range of scores to check for certain personality types
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_conventional),
					(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
					(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
						(is_between, ":troop_no", pretenders_begin, pretenders_end),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(else_try),
					(ge, ":faction_leader", 0),
					(this_or_next|eq, ":faction_leader", ":troop_no"),
					(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
						(troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
					(assign, ":score_to_beat", -6),#-5 or better is indifferent
				(try_end),
			(try_end),
			##diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If the player doesn't have prejudice disabled, don't automatically support for a first fief
				(try_begin),
					(this_or_next|neq, ":subaltern_gender", "$character_gender"),
					(this_or_next|is_between, ":troop_no", companions_begin, companions_end),#Former companions will support the player
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),#Spouses will support the player
						(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
				(else_try),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+

				(gt, ":relation", ":score_to_beat"),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 75),
				(assign, ":favorite_lord_without_center", "trp_player"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladise
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),  #<-- replace this
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
				(try_begin),
					(eq, ":active_npc", ":troop_no"),
					(assign, ":relation", 50),
				(else_try),
					(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
					(assign, ":relation", reg0),
				(try_end),
				##diplomacy start+ Disadvantage the subaltern gender
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(try_begin),
					(eq, reg0, ":subaltern_gender"),
					(val_sub, ":relation", 20),
				(try_end),
				##diplomacy end+
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 75),

				(gt, ":relation", ":score_to_beat"),
				(assign, ":favorite_lord_without_center", ":active_npc"),
				(assign, ":score_to_beat", ":relation"),
			(try_end),

			(gt, ":favorite_lord_without_center", -1),
			(assign, ":result", ":favorite_lord_without_center"),
			(assign, ":result_explainer", "str_political_explanation_lord_lacks_center"),
		##diplomacy start+
		##Faction leaders are more rational about whom they support.
	   (else_try),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":best_candidate", -1),
			(assign, ":best_score", -1),
			(assign, ":explanation", 0),
			(try_begin),
			   (eq,"$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", "trp_player", ":faction_issue"),#reg0 = score, reg1 = explanation
				(assign, ":best_candidate", "trp_player"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(this_or_next|eq, ":best_candidate", -1),
				   (gt, reg0, ":best_score"),
				(assign, ":best_candidate", ":active_npc"),
				(assign, ":best_score", reg0),
				(assign, ":explanation", reg1),
			(try_end),
			(gt, ":best_candidate", -1),
			(assign, ":result", ":best_candidate"),
			(assign, ":result_explainer", ":explanation"),
		##diplomacy end+
		(else_try),	#taken by troop
			(is_between, ":faction_issue", walled_centers_begin, walled_centers_end),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),

			(party_get_slot, ":last_taken_by_troop", ":faction_issue", slot_center_last_taken_by_troop),
			(try_begin),
				(try_begin),
					(neq, ":troop_faction", "$players_kingdom"),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, "$player_has_homage", 0),
					(assign, ":last_taken_by_troop", -1),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_by_player"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try),
					(eq, ":faction_issue", "$g_castle_requested_for_troop"),
					(assign, ":last_taken_by_troop", "trp_player"),
				(else_try), #ie, the fellow who took it is no longer in the faction
					(gt, ":last_taken_by_troop", -1),
					(store_faction_of_troop, ":last_take_by_troop_faction", ":last_taken_by_troop"),
					(neq, ":last_take_by_troop_faction", ":troop_faction"),
					(assign, ":last_taken_by_troop", -1),
				(try_end),
			(try_end),
			(gt, ":last_taken_by_troop", -1),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(gt, ":last_taken_by_troop", -1),
				(str_store_troop_name, s3, ":last_taken_by_troop"),
				(display_message, "@{!}Castle taken by {s3}"),
			(try_end),


			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":last_taken_by_troop"),
			##diplomacy start+
			#If behavior changes are enabled, increase the accepted range for certain personality types.
			(assign, ":relation", reg0),
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(else_try),
					(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
					(val_add, reg0, 5),#i.e. accept at -5 (indifferent) or higher
				(try_end),
			(try_end),
			##diplomacy end+
			(ge, reg0, 0),

			(neg|troop_slot_ge, ":last_taken_by_troop", slot_troop_controversy, 25),

			(troop_get_slot, ":renown", ":last_taken_by_troop", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":last_taken_by_troop"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":center_points", ":last_taken_by_troop", slot_troop_temp_slot),
			(val_max, ":center_points", 1),
			(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
			(val_mul, ":renown_divided_by_center_points", 6), #was five
			(val_div, ":renown_divided_by_center_points", 4),

			##diplomacy start+
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				#Possibly raise renown_divided_by_center_points
				(store_div, reg0, ":renown", ":center_points"),
				(val_add, reg0, ":renown_per_center_point_standard_deviation"),
				(val_max, ":renown_divided_by_center_points", reg0),
			(try_end),
			##diplomacy end+
			(ge, ":renown_divided_by_center_points", ":average_renown_per_center_point"),


			(assign, ":result", ":last_taken_by_troop"),
			(assign, ":result_explainer", "str_political_explanation_lord_took_center"),


		#Check self, immediate family
		#This is done instead of a single weighted score to create cliques -- groups of NPCs who support one another
		(else_try),
			(assign, ":most_deserving_close_friend", -1),
			(assign, ":score_to_beat", ":average_renown_per_center_point"),
			(val_div, ":score_to_beat", 3),
			(val_mul, ":score_to_beat", 2),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg3, ":score_to_beat"),
				(display_message, "@{!}Two-thirds average_renown = {reg3}"),
			(try_end),

			###diplomacy start+
			#(try_begin),
			#	(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			#	(try_begin),
			#		(eq, "$cheat_mode", 1),
			#		(assign, reg3, ":renown_low_target"),
			#		(display_message, "@{!}Average renown per center minus one standard deviation = {reg3}"),
			#	(try_end),
			#(try_end),
			###diplomacy end+

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				#If affiliated with player
				(this_or_next|gt, ":affiliated_with_player", 0),
				##diplomacy end+
				(ge, ":relation", 20),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 50),

				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),


				(assign, ":most_deserving_close_friend", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+  Support promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #<- replace
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				##diplomacy start+
				(assign, reg0, 0),
				#If affiliated with player
				(try_begin),
					(lt, ":relation", 20),
					(gt, ":affiliated_with_player", 0),
					(neq, ":active_npc", ":troop_no"),
					(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
				(try_end),
				(this_or_next|gt, reg0, 0),#<-- both affiliated
				##diplomacy end+
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 20),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 50),

				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),


				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_troop_name, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Colleague test: score for {s10} = {reg3}"),
				(try_end),


				(gt, ":renown_divided_by_center_points", ":score_to_beat"),

				(assign, ":most_deserving_close_friend", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),

			(gt, ":most_deserving_close_friend", -1),


			(assign, ":result", ":most_deserving_close_friend"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_friend"),



		(else_try),
		#Most deserving in entire faction, minus those with no relation
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
			(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),

			(assign, ":most_deserving_in_faction", -1),
			(assign, ":score_to_beat", 0),

			(try_begin),
				(eq, "$players_kingdom", ":troop_faction"),
				(eq, "$player_has_homage", 1),
				(eq, ":player_declines_honor", 0),

				(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
				(assign, ":relation", reg0),
				(ge, ":relation", 0),
				(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(eq, ":subaltern_gender", "$character_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", "trp_player", slot_troop_temp_slot),
				(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 25),

				(val_max, ":center_points", 1),
				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),

				(assign, ":most_deserving_in_faction", "trp_player"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),
			##diplomacy start+ add support for promoted kingdom ladies
			#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
			   (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":troop_faction"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

				(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
				(assign, ":relation", reg0),
				(this_or_next|eq, ":active_npc", ":troop_no"),
					(ge, ":relation", 0),
				(neg|troop_slot_ge, ":active_npc", slot_troop_controversy, 25),

				(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
				##diplomacy start+
				(try_begin),
					(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
					(call_script, "script_dplmc_store_troop_is_female", ":active_npc"),
					(eq, reg0, ":subaltern_gender"),
					(val_mul, ":renown", 4),
					(val_add, ":renown", 3),
					(val_div, ":renown", 5),
				(try_end),
				##diplomacy end+
				(troop_get_slot, ":center_points", ":active_npc", slot_troop_temp_slot),
				(val_max, ":center_points", 1),

				(store_div, ":renown_divided_by_center_points", ":renown", ":center_points"),
				(gt, ":renown_divided_by_center_points", ":score_to_beat"),

				(try_begin),
					(eq, "$cheat_mode", 1),
					(str_store_string, s10, ":active_npc"),
					(assign, reg3, ":renown_divided_by_center_points"),
					(display_message, "@{!}DEBUG -- Open test: score for {s10} = {reg3}"),
				(try_end),


				(assign, ":most_deserving_in_faction", ":active_npc"),
				(assign, ":score_to_beat", ":renown_divided_by_center_points"),
			(try_end),


			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			(assign, ":result_explainer", "str_political_explanation_most_deserving_in_faction"),
		##diplomacy start+
		(else_try),
			#The lord wasn't able to find any suitable candidates,
			#so now we perform the evaluation from another perspective.
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#DPLMC_AI_CHANGES >= LOW
			#DPLMC_AI_CHANGES >= MEDIUM   XOR   status >= DPLMC_FACTION_STANDING_LEADER_SPOUSE
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":troop_no", ":troop_faction"),
			(this_or_next|ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
				(lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
			(assign, ":save_reg1", reg1),

			(assign, ":score_to_beat", 0),
			(assign, ":most_deserving_in_faction", -1),
			#(assign, ":tmp_explanation", 0),

			(try_for_range, ":active_npc", active_npcs_including_player_begin, heroes_end),
				(store_sub, ":active_npc_faction", ":troop_faction", 1),
				(try_begin),
					(eq, ":active_npc", active_npcs_including_player_begin),
					(assign, ":active_npc", "trp_player"),
					(eq, "$players_kingdom", ":troop_faction"),
					(eq, "$player_has_homage", 1),
					(assign, ":active_npc_faction", ":troop_faction"),
				(else_try),
					(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(try_end),
				(eq, ":active_npc_faction", ":troop_faction"),

				#(call_script, "script_dplmc_aux_troop_evaluate_troop_for_center", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation
				(call_script, "script_dplmc_calculate_troop_score_for_center_aux", ":troop_no", ":active_npc", ":faction_issue"),#reg0 = score, reg1 = explanation

				(this_or_next|eq, ":most_deserving_in_faction", -1),
					(ge, reg0, ":score_to_beat"),
				(assign, ":score_to_beat", reg0),
            (assign, ":result_explainer", reg1),
				(assign, ":most_deserving_in_faction", ":active_npc"),
			(try_end),

			(gt, ":most_deserving_in_faction", -1),
			(assign, ":result", ":most_deserving_in_faction"),
			#(assign, ":result_explainer", ":result_explainer"),#unneeded
         (assign, reg1, ":save_reg1"),
		##diplomacy end+
		(else_try),
			(assign, ":result", ":troop_no"),
			(assign, ":result_explainer", "str_political_explanation_self"),
		(try_end),


	(else_try),
		(eq, ":faction_issue", 1),

		(assign, ":relationship_threshhold", 15),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
			(assign, ":relationship_threshhold", 5),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
			(assign, ":relationship_threshhold", 25),
		(try_end),

		#For marshals, score marshals according to renown divided by controversy - first for friends and family, then for everyone
		(assign, ":marshal_candidate", -1),
		(assign, ":score_to_beat", 0),
		(try_begin),
			(eq, "$players_kingdom", ":troop_faction"),
			(eq, "$player_has_homage", 1),
			(eq, "$g_player_is_captive", 0),
			(eq, ":player_declines_honor", 0),


			(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
			(ge, reg0, ":relationship_threshhold"),
			(assign, ":marshal_candidate", "trp_player"),
			(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(eq, ":subaltern_gender", "$character_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", "trp_player", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score_to_beat", ":renown", ":controversy_divisor"),
		(try_end),

      ##diplomacy start+ Support promoted ladies
		#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":active_npc", heroes_begin, heroes_end),
      ##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":troop_faction"),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":active_npc", slot_troop_prisoner_of_party, -1),

			(neg|faction_slot_eq, ":troop_faction", slot_faction_leader, ":active_npc"),

			(call_script, "script_troop_get_relation_with_troop", ":active_npc", ":troop_no"),
			(assign, ":relation", reg0),
			(this_or_next|eq, ":active_npc", ":troop_no"),
				(ge, ":relation", ":relationship_threshhold"),

			(troop_get_slot, ":renown", ":active_npc", slot_troop_renown),
			##diplomacy start+
			(try_begin),
				(lt, "$g_disable_condescending_comments", 0),#If the player has set the prejudice mode to "high"
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(eq, reg0, ":subaltern_gender"),
				(val_mul, ":renown", 4),
				(val_add, ":renown", 3),
				(val_div, ":renown", 5),
			(try_end),
			##diplomacy end+
			(troop_get_slot, ":controversy_divisor", ":active_npc", slot_troop_controversy),
			(val_add, ":controversy_divisor", 50),
			(store_div, ":score", ":renown", ":controversy_divisor"),

			(gt, ":score", ":score_to_beat"),

			(assign, ":marshal_candidate", ":active_npc"),
			(assign, ":score_to_beat", ":score"),

		(try_end),

		(assign, ":result", ":marshal_candidate"),
		(assign, ":result_explainer", "str_political_explanation_marshal"),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(gt, ":result", -1),
		(str_store_troop_name, s8, ":troop_no"),
		(str_store_troop_name, s9, ":result"),
		(str_store_string, s10, ":result_explainer"),
		(display_message, "@{!}DEBUG -- {s8} backs {s9}:{s10}"),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":result_explainer"),

	])
]
