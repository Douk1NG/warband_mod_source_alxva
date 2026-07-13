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
from native.scripts.music.music_scripts import music_scripts
from native.scripts.orders.orders_scripts import orders_scripts
from native.scripts.siege.siege_scripts import siege_scripts
from native.scripts.training_ground.training_ground_scripts import training_ground_scripts
from native.scripts.multiplayer.multiplayer_scripts import multiplayer_scripts
from native.scripts.economy.economy_scripts import economy_scripts
from native.scripts.quests.quest_scripts import quest_scripts
from native.scripts.morale.morale_scripts import morale_scripts
from native.scripts.heraldry.heraldry_scripts import heraldry_scripts
from native.scripts.arena.arena_scripts import arena_scripts
from native.scripts.encounters.encounters_scripts import encounters_scripts
from native.scripts.party_ai.party_ai_scripts import party_ai_scripts
from native.scripts.centers.centers_scripts import centers_scripts
from native.scripts.npcs.npcs_scripts import npcs_scripts
from native.scripts.faction_ai.faction_ai_scripts import faction_ai_scripts
from native.scripts.core.core_scripts import core_scripts
from native.scripts.misc.misc_scripts import misc_scripts
from native.scripts.misc.misc_scripts_extra import misc_scripts_extra
from native.scripts.misc.misc_scripts_extra2 import misc_scripts_extra2
from native.scripts.diplomacy.diplomacy_scripts import diplomacy_scripts
from native.scripts.dickplomacy.dickplomacy_scripts import dickplomacy_scripts
from native.scripts.feats import feats_scripts
##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+

##diplomacy begin
##jrider reports
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *

## deprecated due to 1.165 operations
# ibf_item_type_mask = 0x000000ff

# def set_item_difficulty():
  # item_difficulty = []
  # for i_item in xrange(len(items)):
    # item_difficulty.append((item_set_slot, i_item, dplmc_slot_item_difficulty, get_difficulty(items[i_item][6])))
  # return item_difficulty[:]

# def set_item_base_score():
  # item_base_score = []
  # for i_item in xrange(len(items)):
    # if items[i_item][3] & ibf_item_type_mask == itp_type_two_handed_wpn and items[i_item][3] & itp_two_handed == 0:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_two_handed_one_handed, 1))
    # type = items[i_item][3] & ibf_item_type_mask
    # if type >= itp_type_head_armor and type <= itp_type_hand_armor:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_head_armor, get_head_armor(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_body_armor, get_body_armor(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_leg_armor, get_leg_armor(items[i_item][6])))
    # elif type >= itp_type_one_handed_wpn and type <= itp_type_thrown and type != itp_type_shield:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_thrust_damage, get_thrust_damage(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_swing_damage, get_swing_damage(items[i_item][6])))
    # elif type == itp_type_horse:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_speed, get_missile_speed(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_armor, get_body_armor(items[i_item][6])))
    # elif type == itp_type_shield:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_size, get_weapon_length(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_armor, get_body_armor(items[i_item][6])))
  # return item_base_score[:]
  # #### Autoloot improved by rubik end

##diplomacy end

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################


scripts = [


   ##diplomacy start+
   #Modified this to return additional information.
	##diplomacy end+
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

	]),

	(
	"diplomacy_faction_get_diplomatic_status_with_faction",
	#result: -1 faction_1 has a casus belli against faction_2. 1, faction_1 has a truce with faction_2, -2, the two factions are at war
	[
	(store_script_param, ":actor_faction", 1),
	(store_script_param, ":target_faction", 2),
	##diplomacy start+
	#Since "fac_player_supporters_faction" is used as a shorthand for the faction
	#run by the player, intercept that here instead of the various places this is
	#called from.
	(call_script, "script_dplmc_translate_inactive_player_supporter_faction_2", ":actor_faction", ":target_faction"),
	(assign, ":actor_faction", reg0),
	(assign, ":target_faction", reg1),
	##diplomacy end+

	(store_add, ":truce_slot", ":target_faction", slot_faction_truce_days_with_factions_begin),
	(store_add, ":provocation_slot", ":target_faction", slot_faction_provocation_days_with_factions_begin),
	(val_sub, ":truce_slot", kingdoms_begin),
	(val_sub, ":provocation_slot", kingdoms_begin),

	(assign, ":result", 0),
	(assign, ":duration", 0),

	(try_begin),
		(store_relation, ":relation", ":actor_faction", ":target_faction"),
		(lt, ":relation", 0),
		(assign, ":result", -2),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":truce_slot", 1),
		(assign, ":result", 1),

		(faction_get_slot, ":duration", ":actor_faction", ":truce_slot"),
	(else_try),
		(faction_slot_ge, ":actor_faction", ":provocation_slot", 1),
		(assign, ":result", -1),

		(faction_get_slot, ":duration", ":actor_faction", ":provocation_slot"),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":duration"),
	]),

	(
	"npc_decision_checklist_faction_ai_alt", #This is called from within decide_faction_ai, or from
	[
		(store_script_param, ":troop_no", 1),

		(store_faction_of_troop, ":faction_no", ":troop_no"),

		(str_store_troop_name, s4, ":troop_no"),
		(str_store_faction_name, s33, ":faction_no"),
		(try_begin),
			(eq, "$cheat_mode", 1),
		    (display_message, "@{!}DEBUG -- {s4} produces a faction strategy for {s33}"),
		(try_end),

		#INFORMATIONS COLLECTING STEP 0: Here we obtain general information about current faction like how much parties that faction has, which lord is the marshall, current ai state and current ai target object
		#(faction_get_slot, ":faction_strength", ":faction_no", slot_faction_number_of_parties),
		(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
		(faction_get_slot, ":current_ai_state", ":faction_no", slot_faction_ai_state),
		(faction_get_slot, ":current_ai_object", ":faction_no", slot_faction_ai_object),

		(assign, ":marshal_party", -1),
		(assign, ":marshal_party_strength", 0),

		(try_begin),
		  (gt, ":faction_marshal", 0),
		  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
		  (party_is_active, ":marshal_party"),
		  (party_get_slot, ":marshal_party_itself_strength", ":marshal_party", slot_party_cached_strength),
		  (party_get_slot, ":marshal_party_follower_strength", ":marshal_party", slot_party_follower_strength),
		  (store_add, ":marshal_party_strength", ":marshal_party_itself_strength", ":marshal_party_follower_strength"),
	    (try_end),

	    #INFORMATIONS COLLECTING STEP 1: Here we are learning how much hours past from last offensive situation/feast concluded/current state started
	    (store_current_hours, ":hours_since_last_offensive"),
	    (faction_get_slot, ":last_offensive_time", ":faction_no", slot_faction_last_offensive_concluded),
	    (val_sub, ":hours_since_last_offensive", ":last_offensive_time"),

	    (store_current_hours, ":hours_since_last_feast_start"),
	    (faction_get_slot, ":last_feast_time", ":faction_no", slot_faction_last_feast_start_time),
	    (val_sub, ":hours_since_last_feast_start", ":last_feast_time"),

	    (store_current_hours, ":hours_at_current_state"),
	    (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
	    (val_sub, ":hours_at_current_state", ":current_state_started"),

	    (store_current_hours, ":hours_since_last_faction_rest"),
	    (faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
	    (val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),

	    (try_begin), #calculating ":last_offensive_time_score", this will be used in #11 and #12
	        (ge, ":hours_since_last_offensive", 1080), #more than 45 days (100p)
	        (assign, ":last_offensive_time_score", 100),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 480), #more than 20 days (65p..99p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 480),
	        (val_div, ":last_offensive_time_score", 20),
	        (val_add, ":last_offensive_time_score", 64),
	    (else_try),
	        (ge, ":hours_since_last_offensive", 240), #more than 10 days (41p..64p)
	        (store_sub, ":last_offensive_time_score", ":hours_since_last_offensive", 240),
	        (val_div, ":last_offensive_time_score", 10),
	        (val_add, ":last_offensive_time_score", 40),
	    (else_try), #less than 10 days (0p..40p)
	        (store_div, ":last_offensive_time_score", ":hours_since_last_offensive", 6), #0..40
	    (try_end),

	    #INFORMATION COLLECTING STEP 3: Here we are finding the most threatened center
	    (call_script, "script_find_center_to_defend", ":troop_no"),
	    (assign, ":most_threatened_center", reg0),
	    (assign, ":threat_danger_level", reg1),
	    (assign, ":enemy_strength_near_most_threatened_center", reg2), #NOTE! This will be off by as much as 50%

	    #INFORMATION COLLECTING STEP 4: Here we are finding number of vassals who are already following the marshal, and the assigned vassal ratio of current faction.
	    (assign, ":vassals_already_assembled", 0),
	    (assign, ":total_vassals", 0),
		##diplomacy start+ add support for promoted kingdom ladies
	    #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":lord", heroes_begin, heroes_end),
			(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
	        (store_faction_of_troop, ":lord_faction", ":lord"),
	        (eq, ":lord_faction", ":faction_no"),
	        (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
	        (party_is_active, ":led_party"),
	        (val_add, ":total_vassals", 1),

	        (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
	        (party_slot_eq, ":led_party", slot_party_ai_object, ":marshal_party"),

	        (party_is_active, ":marshal_party"),
	        (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":marshal_party"),
	        (lt, ":distance_to_marshal", 15),
	        (val_add, ":vassals_already_assembled", 1),
	    (try_end),
	    (assign, ":ratio_of_vassals_assembled", -1),
	    (try_begin),
	        (gt, ":total_vassals", 0),
	        (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
	        (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
	    (try_end),

	    #50% of vassals means that the campaign hour limit is ten days
	    (store_mul, ":campaign_hour_limit", ":ratio_of_vassals_assembled", 3),
	    (val_add, ":campaign_hour_limit", 90),

	    #To Steve - I understand your concern about some marshals will gather army and some will not be able to find any valueable center to attack after gathering,
	    #and these marshals will be questioned by other marshals ext. This is ok but if we search for a target without adding all other vassals what if
	    #AI cannot find any target for long time because of its low power ratio if enemy cities are equal defended? Do not forget if we do not count other vassals in
	    #faction while making target search we can only add marshal army's power and vassals around him. And if there is any threat in our centers even it is smaller,
	    #its threat_danger_level will be more than target_value_level if marshal new started gathering for ofensive. Because we only assume marshal and around vassals
	    #will join attack. And in our scenarios currently there are less vassals are around him. So power ratio will be low and any small threat will be enought to stop
	    #an offensive. Then when players finds out this they periodically will take under siege to enemy's any center and they will be saved from any kind of newly started
	    #offensive they will be faced. So we have to calculate both attack levels and select highest one to compare with threat level. Please do not change this part.

		(try_begin),
		  (ge, ":faction_marshal", 0),
		  (ge, ":marshal_party", 0),
		  (party_is_active, ":marshal_party"),

		  (call_script, "script_party_count_fit_for_battle", ":marshal_party"),
		  (assign, ":number_of_fit_soldiers_in_marshal_party", reg0),
		  (ge, ":number_of_fit_soldiers_in_marshal_party", 40),

		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 0),
		  (assign, ":center_to_attack_all_vassals_included", reg0),
		  (assign, ":target_value_level_all_vassals_included", reg1),

		  (call_script, "script_find_center_to_attack_alt", ":troop_no", 1, 1),
		  (assign, ":center_to_attack_only_marshal_and_followers", reg0),
		  (assign, ":target_value_level_only_marshal_and_followers", reg1),
		(else_try),
		  (assign, ":target_value_level_all_vassals_included", 0),
		  (assign, ":target_value_level_only_marshal_and_followers", 0),
		  (assign, ":center_to_attack_all_vassals_included", -1),
		  (assign, ":center_to_attack_only_marshal_and_followers", -1),
		(try_end),

		(try_begin),
		  (ge, ":target_value_level_all_vassals_included", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":center_to_attack", ":center_to_attack_all_vassals_included"),
		  (assign, ":target_value_level", ":target_value_level_all_vassals_included"),
		(else_try),
		  (assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),
		  (assign, ":target_value_level", ":target_value_level_only_marshal_and_followers"),
		(try_end),

		(try_begin),
		  (eq, ":current_ai_state", sfai_attacking_center),
		  (val_mul, ":target_value_level", 3),
		  (val_div, ":target_value_level", 2),
		(try_end),

		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (try_begin),
		    (is_between, ":center_to_attack", centers_begin, centers_end),
		    (str_store_party_name, s4, ":center_to_attack"),
		    (display_message, "@{!}Best offensive target {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to attack"),
		  (try_end),

		  (try_begin),
		    (is_between, ":most_threatened_center", centers_begin, centers_end),
		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@{!}Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@{!}No center found to defend"),
		  (try_end),
		(try_end),

		(try_begin),
		  (eq, "$cheat_mode", 1),

		  (try_begin),
  		    (is_between, ":most_threatened_center", centers_begin, centers_end),
 		    (str_store_party_name, s4, ":most_threatened_center"),
		    (assign, reg1, ":threat_danger_level"),
		    (display_message, "@Best threat of {s4} has value level of {reg1}"),
		  (else_try),
		    (display_message, "@No center found to defend"),
		  (try_end),
		(try_end),

	    (assign, "$g_target_after_gathering", -1),

	    (store_current_hours, ":hours"),
	    (try_begin),
	      (ge, ":target_value_level", ":threat_danger_level"),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),
	    (try_end),
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (try_begin),
	      (eq, ":last_safe_hours", 0),
	      (faction_set_slot, ":faction_no", slot_faction_last_safe_hours, ":hours"),
	    (try_end),
	    (faction_get_slot, ":last_safe_hours", ":faction_no", slot_faction_last_safe_hours),
	    (store_sub, ":hours_since_days_defensive_started", ":hours", ":last_safe_hours"),
	    (str_store_faction_name, s7, ":faction_no"),

		(assign, ":at_peace_with_everyone", 1),
		(try_for_range, ":faction_at_war", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":faction_at_war"),
			(lt, ":relation", 0),
			(assign, ":at_peace_with_everyone", 0),
		(try_end),


	    #INFORMATIONS ARE COLLECTED, NOW CHECK ALL POSSIBLE ACTIONS AND DECIDE WHAT TO DO	NEXT
		#Player marshal
		(try_begin), # a special case to end long-running feasts
			(eq, ":troop_no", "trp_player"),

			(eq, ":current_ai_state", sfai_feast),
			(ge, ":hours_at_current_state", 72),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),

			#Normally you are not supposed to set permanent values in this state, but this is a special case to end player-called feasts
			(assign, "$player_marshal_ai_state", sfai_default),
			(assign, "$player_marshal_ai_object", -1),
		(else_try), #another special state, to make player-called feasts last for a while when the player is the leader of the faction, but not the marshal
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(neq, ":troop_no", "trp_player"),

			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 48),

			(party_slot_eq, ":current_ai_object", slot_town_lord, "trp_player"),
			(store_faction_of_party, ":current_ai_object_faction", ":current_ai_object"),
			(eq, ":current_ai_object_faction", "$players_kingdom"),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),


		(else_try), #this is the main player marshal state
			(eq, ":troop_no", "trp_player"),

			(str_clear, s14),
			(assign, ":action", "$player_marshal_ai_state"),
			(assign, ":object", "$player_marshal_ai_object"),

	    #1-RESTING IF NEEDED
	    #If not currently attacking a besieging a center and vassals did not rest for long time, let them rest.
	    #If we do not take this part to toppest level, tired vassals already did not accept any order, so that
	    #faction cannot do anything already. So first let vassals rest if they need. Thats why it should be toppest.
		(else_try),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),
			(party_is_active, ":marshal_party"),

			(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_retreating_to_center),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_enemy_temporarily_has_the_field"),

		(else_try),
		    (neq, ":current_ai_state", sfai_feast),

		    (assign, ":currently_besieging", 0),
		    (try_begin),
			    (eq, ":current_ai_state", sfai_attacking_center),
			    (is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
			    (party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
			    (party_is_active, ":besieger_party"),
			    (store_faction_of_party, ":besieger_faction", ":besieger_party"),
			    (eq, ":besieger_faction", ":faction_no"),
			    (assign, ":currently_besieging", 1),
		    (try_end),

		    (assign, ":currently_defending_center", 0),
	        (try_begin),
		        (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
		        (gt, ":marshal_party", 0),
		        (party_is_active, ":marshal_party"),

				(assign, ":besieged_center", -1),
				(try_begin),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
					(party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
					(ge, ":besieger_enemy", 0),
					(assign, ":besieged_center", ":marshal_object"),
				(else_try),
					(party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
					(party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
					(ge, ":marshal_object", 0), #if commander has an object
					(neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
					(party_is_active, ":marshal_object"),
					(party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
				(try_end),

				(eq, ":besieged_center", ":current_ai_object"),
				(assign, ":currently_defending_center", 1),
	        (try_end),

		    (eq, ":currently_besieging", 0),
		    (eq, ":currently_defending_center", 0),
		    (ge, ":hours_since_last_faction_rest", 1240),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_vassals_are_tired_we_let_them_rest_for_some_time"),

	  #2-DEFENSIVE ACTIONS : GATHERING ARMY FOR DEFENDING
          (else_try),
            (party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),

            (is_between, ":most_threatened_center", centers_begin, centers_end),
            (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
            (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
            (gt, ":threat_danger_level", ":target_value_level"),

            (assign, ":continue_gathering", 0),
            (assign, ":start_gathering", 0),

            (try_begin),
              (is_between, ":most_threatened_center", villages_begin, villages_end),

              (assign, ":continue_gathering", 0),
            (else_try),
              (try_begin),
                (lt, ":hours_since_days_defensive_started", 3),
                (assign, ":multiplier", 150),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 6),
                (assign, ":multiplier", 140),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 9),
                (assign, ":multiplier", 132),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 12),
                (assign, ":multiplier", 124),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 15),
                (assign, ":multiplier", 118),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 18),
                (assign, ":multiplier", 114),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 21),
                (assign, ":multiplier", 110),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 24),
                (assign, ":multiplier", 106),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 27),
                (assign, ":multiplier", 102),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 31),
                (assign, ":multiplier", 98),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 34),
                (assign, ":multiplier", 94),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 37),
                (assign, ":multiplier", 90),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 40),
                (assign, ":multiplier", 86),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 43),
                (assign, ":multiplier", 82),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 46),
                (assign, ":multiplier", 79),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 49),
                (assign, ":multiplier", 76),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 52),
                (assign, ":multiplier", 73),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 56),
                (assign, ":multiplier", 70),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 60),
                (assign, ":multiplier", 68),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 66),
                (assign, ":multiplier", 66),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 72),
                (assign, ":multiplier", 64),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 80),
                (assign, ":multiplier", 62),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 90),
                (assign, ":multiplier", 60),
              (else_try),
                (lt, ":hours_since_days_defensive_started", 100),
                (assign, ":multiplier", 58),
              (else_try),
                (assign, ":multiplier", 56),
              (try_end),

              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", ":multiplier"),
              (val_div, ":enemy_strength_multiplied", 100),

              (try_begin),
                (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),
                (assign, ":continue_gathering", 1),
              (try_end),
            (else_try),
              (eq, ":current_ai_state", sfai_attacking_enemies_around_center),
              (neq, ":most_threatened_center", ":current_ai_object"),

              (assign, ":marshal_is_already_defending_a_center", 0),
              (try_begin),
                (gt, ":marshal_party", 0),
                (party_is_active, ":marshal_party"),

                (assign, ":besieged_center", -1),
                (try_begin),
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (center they are holding)
                  (party_get_battle_opponent, ":besieger_enemy", ":marshal_object"), #get this object's battle opponent
                  (ge, ":besieger_enemy", 0),
                  (assign, ":besieged_center", ":marshal_object"),
                (else_try),
                  (party_slot_eq, ":marshal_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
                  (party_get_slot, ":marshal_object", ":marshal_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
                  (ge, ":marshal_object", 0), #if commander has an object
                  (neg|is_between, ":marshal_object", centers_begin, centers_end), #if this object is not a center, so it is a party
				  (party_is_active, ":marshal_object"),
                  (party_get_battle_opponent, ":besieged_center", ":marshal_object"), #get this object's battle opponent
                (try_end),

                (eq, ":besieged_center", ":current_ai_object"),

                (assign, ":marshal_is_already_defending_a_center", 1),
              (try_end),

              (eq, ":marshal_is_already_defending_a_center", 0),

              (store_mul, ":enemy_strength_multiplied", ":enemy_strength_near_most_threatened_center", 80),
              (val_div, ":enemy_strength_multiplied", 100),
              (lt, ":marshal_party_strength", ":enemy_strength_multiplied"),

              (this_or_next|is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
              (neq, ":faction_no", "$players_kingdom"),

              (assign, ":start_gathering", 1),
            (try_end),

            (this_or_next|eq, ":continue_gathering", 1),
            (eq, ":start_gathering", 1),

            (assign, ":action", sfai_gathering_army),
            (assign, ":object", -1),
            (str_store_party_name, s21, ":most_threatened_center"),
            (str_store_string, s14, "str_we_should_prepare_to_defend_s21_but_we_should_gather_our_forces_until_we_are_strong_enough_to_engage_them"),

            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", ":most_threatened_center"),
            (try_end),

	    #3-DEFENSIVE ACTIONS : RIDE TO BREAK ENEMY SIEGE / DEFEAT ENEMIES NEAR OUR CENTER
		(else_try),
			(party_is_active, ":marshal_party"),
			(is_between, ":most_threatened_center", walled_centers_begin, walled_centers_end),
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
			(ge, ":threat_danger_level", ":target_value_level"),
			(party_slot_ge, ":most_threatened_center", slot_center_is_besieged_by, 0),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),

			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_break_the_siege_of_s21"),

		#3b - DEFEAT ENEMIES NEAR CENTER - similar to above, but a different string
		(else_try),
			(party_is_active, ":marshal_party"),
                        (this_or_next|eq, ":current_ai_state", sfai_default),    #MOTO not going to attack anyway
                        (this_or_next|eq, ":current_ai_state", sfai_feast),    #MOTO not going to attack anyway (THIS is the emergency to stop feast)
			(ge, ":threat_danger_level", ":target_value_level"),
			(is_between, ":most_threatened_center", villages_begin, villages_end),

			(assign, ":action", sfai_attacking_enemies_around_center),
			(assign, ":object", ":most_threatened_center"),
			(str_store_party_name, s21, ":most_threatened_center"),
			(str_store_string, s14, "str_we_should_ride_to_defeat_the_enemy_gathered_near_s21"),

		#4-DEMOBILIZATION
		#Let vassals attend their own business
		(else_try),
			(this_or_next|eq, ":current_ai_state", sfai_gathering_army),
			(this_or_next|eq, ":current_ai_state", sfai_attacking_center),
			(eq, ":current_ai_state", sfai_raiding_village),

			(ge, ":hours_since_last_faction_rest", ":campaign_hour_limit"), #Effected by ratio of vassals
			(ge, ":hours_at_current_state", 24),

			#Ozan : I am adding some codes here because sometimes armies demobilize during last seconds of an important event like taking a castle, ext.
			(assign, ":there_is_an_important_situation", 0),
			(try_begin), #do not demobilize during taking a castle/town (fighting in the castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_battle_opponent, ":besieger_party", ":current_ai_object"),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during besieging a siege (holding around castle)
				(is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_get_slot, ":besieger_party", ":current_ai_object", slot_center_is_besieged_by),
				(party_is_active, ":besieger_party"),
				(store_faction_of_party, ":besieger_faction", ":besieger_party"),
				(this_or_next|eq, ":besieger_faction", ":faction_no"),
				(eq, ":besieger_faction", "fac_player_faction"),
				(assign, ":there_is_an_important_situation", 1),
			(else_try), #do not demobilize during raiding a village (holding around village)
				(is_between, ":current_ai_object", centers_begin, centers_end),
				(neg|is_between, ":current_ai_object", walled_centers_begin, walled_centers_end),
				(party_slot_eq, ":current_ai_object", slot_village_state, svs_being_raided),
				(assign, ":there_is_an_important_situation", 1),
			(try_end),

			(eq, ":there_is_an_important_situation", 0),
			#end addition ozan

			(assign, reg7, ":hours_since_last_faction_rest"),
			(assign, reg8, ":campaign_hour_limit"),

			(str_store_string, s14, "str_this_offensive_needs_to_wind_down_soon_so_the_vassals_can_attend_to_their_own_business"),
			(assign, ":action", sfai_default),
			(assign, ":object", -1),

		#6-GATHERING BECAUSE OF NO REASON
		#Start to gather the army
		(else_try),
			(party_is_active, ":marshal_party"),
			(eq, ":at_peace_with_everyone", 0),


			(eq, ":current_ai_state", sfai_default),
			(ge, ":hours_since_last_offensive", 60),
			(lt, ":hours_since_last_faction_rest", 120),

			#There should not be a center as a precondition for attack
			#Otherwise, we are unlikely to have a situation in which the army gathers, but does nothing -- which is important to have for role-playing purposes

			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),
			(str_store_string, s14, "str_it_is_time_to_go_on_the_offensive_and_we_must_first_assemble_the_army"),

            (try_begin),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, "$g_gathering_reason", -1),
            (try_end),

		#7-OFFENSIVE ACTIONS : CONTINUE GATHERING
		(else_try),
			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),
			(eq, ":at_peace_with_everyone", 0),

			(lt, ":hours_at_current_state", 54), #gather army for 54 hours

			(lt, ":ratio_of_vassals_assembled", 12),

			(str_store_string, s14, "str_we_must_continue_to_gather_the_army_before_we_ride_forth_on_an_offensive_operation"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#7-OFFENSIVE ACTIONS PART 2 : CONTINUE GATHERING
		(else_try),
		    (assign, ":minimum_possible_attackable_target_value_level", 50),
			(eq, ":at_peace_with_everyone", 0),

            (try_begin), #agressive marshal
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
			  (val_mul, ":minimum_possible_attackable_target_value_level", 9),
			  (val_div, ":minimum_possible_attackable_target_value_level", 10),
            (try_end),

			(party_is_active, ":marshal_party"),
			(eq, ":current_ai_state", sfai_gathering_army),

			(try_begin),
				(lt, ":hours_at_current_state", 6),
				(assign, ":minimum_needed_target_value_level", 1500),
			(else_try),
				(lt, ":hours_at_current_state", 10),
				(assign, ":minimum_needed_target_value_level", 1000),
			(else_try),
		        (lt, ":hours_at_current_state", 14),
		        (assign, ":minimum_needed_target_value_level", 720),
			(else_try),
				(lt, ":hours_at_current_state", 18),
				(assign, ":minimum_needed_target_value_level", 480),
			(else_try),
				(lt, ":hours_at_current_state", 22),
				(assign, ":minimum_needed_target_value_level", 360),
			(else_try),
				(lt, ":hours_at_current_state", 26),
				(assign, ":minimum_needed_target_value_level", 240),
			(else_try),
				(lt, ":hours_at_current_state", 30),
				(assign, ":minimum_needed_target_value_level", 180),
			(else_try),
				(lt, ":hours_at_current_state", 34),
				(assign, ":minimum_needed_target_value_level", 120),
			(else_try),
				(lt, ":hours_at_current_state", 38),
				(assign, ":minimum_needed_target_value_level", 100),
			(else_try),
				(lt, ":hours_at_current_state", 42),
				(assign, ":minimum_needed_target_value_level", 80),
			(else_try),
				(lt, ":hours_at_current_state", 46),
				(assign, ":minimum_needed_target_value_level", 65),
			(else_try),
				(lt, ":hours_at_current_state", 50),
				(assign, ":minimum_needed_target_value_level", 55),
			(else_try),
				(assign, ":minimum_needed_target_value_level", ":minimum_possible_attackable_target_value_level"),
			(try_end),

            (try_begin), #agressive marshal
			  ##diplomacy start+
			  ##OLD:
			  #(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			  #(this_or_next|eq, ":reputation", lrep_martial),
			  #(this_or_next|eq, ":reputation", lrep_quarrelsome),
			  #(eq, ":reputation", lrep_selfrighteous),
			  ##NEW:
			  (call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			  (lt, reg0, 0),
			  ##diplomacy end+
			  (val_mul, ":minimum_needed_target_value_level", 9),
			  (val_div, ":minimum_needed_target_value_level", 10),
            (try_end),

			(le, ":target_value_level", ":minimum_needed_target_value_level"),
			(le, ":hours_at_current_state", 54),

			(str_store_string, s14, "str_we_have_assembled_some_vassals"),
			(assign, ":action", sfai_gathering_army),
			(assign, ":object", -1),

		#8-ATTACK AN ENEMY CENTER case 1, reconnaissance against walled center
		#(else_try),
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"),
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),

		    #(assign, ":action", sfai_attacking_center),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),

		#8-ATTACK AN ENEMY CENTER case 2, reconnaissance against village
		#(else_try),
			#(party_is_active, ":marshal_party"),
			#(neq, ":current_ai_state", sfai_default),
			#(neq, ":current_ai_state", sfai_feast),
			#(is_between, ":center_to_attack", villages_begin, villages_end),

			#(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
			#(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
			#(store_current_hours, ":hours_since_last_recon"),
			#(party_get_slot, ":last_recon_time", ":center_to_attack", ":faction_recce_slot"),
			#(val_sub, ":hours_since_last_recon", ":last_recon_time"),
			#(this_or_next|eq, ":last_recon_time", 0),
			#(gt, ":hours_since_last_recon", 96),


			#(assign, ":action", sfai_raiding_village),
			#(assign, ":object", ":center_to_attack"),
			#(str_store_string, s14, "str_we_are_conducting_recce"),
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),

			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),

			(is_between, ":center_to_attack", walled_centers_begin, walled_centers_end),

			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),

		    (assign, ":action", sfai_attacking_center),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_believe_the_fortress_will_be_worth_the_effort_to_take_it"),
		(else_try),
			(party_is_active, ":marshal_party"),
			(neq, ":current_ai_state", sfai_default),
			(neq, ":current_ai_state", sfai_feast),

			(assign, ":center_to_attack", ":center_to_attack_only_marshal_and_followers"),

			(is_between, ":center_to_attack", villages_begin, villages_end),

			(ge, ":target_value_level", ":minimum_possible_attackable_target_value_level"),

			(assign, ":action", sfai_raiding_village),
			(assign, ":object", ":center_to_attack"),
			(str_store_string, s14, "str_we_shall_leave_a_fiery_trail_through_the_heart_of_the_enemys_lands_targeting_the_wealthy_settlements_if_we_can"),

		#9 -- DISBAND THE ARMY
		(else_try),
			(eq, ":current_ai_state", sfai_gathering_army),

			(str_store_string, s14, "str_the_army_will_be_disbanded_because_we_have_been_waiting_too_long_without_a_target"),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
		#OFFENSIVE OPERATIONS END

		#FEAST-RELATED OPERATIONS BEGIN
		#10-CONCLUDE CURRENT FEAST
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(gt, ":hours_at_current_state", 72),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_it_is_time_for_the_feast_to_conclude"),

		#11-CONTINE FEAST UNLESS THERE IS AN EMERGENCY
		(else_try),
			(eq, ":current_ai_state", sfai_feast),
			(le, ":hours_at_current_state", 72),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":current_ai_object"),
			(str_store_string, s14, "str_we_should_continue_the_feast_unless_there_is_an_emergency"),

		#12-HOLD A FEAST BECAUSE THE PLAYER WANTS TO ORGANIZE ONE
		(else_try),
			(check_quest_active, "qst_organize_feast"),
			(eq, "$players_kingdom", ":faction_no"),

			(quest_get_slot, ":target_center", "qst_organize_feast", slot_quest_target_center),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":target_center"),
			(str_store_string, s14, "str_you_had_wished_to_hold_a_feast"),

		#13-HOLD A FEAST BECAUSE FEMALE PLAYER SCHEDULED TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed_female"),

			(quest_get_slot, ":groom", "qst_wed_betrothed_female", slot_quest_giver_troop),
			(troop_slot_eq, ":groom", slot_troop_prisoner_of_party, -1),

			(store_faction_of_troop, ":groom_faction", ":groom"),
			(eq, ":groom_faction", ":faction_no"),

			(faction_get_slot, ":faction_leader", ":groom_faction", slot_faction_leader),

			(assign, ":location_feast", -1),
			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
			   (eq, ":location_feast", -1),
			    (party_slot_eq, ":possible_location", slot_town_lord, ":groom"),
			    (party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
			    (assign, ":location_feast", ":possible_location"),
			(try_end),

			(try_for_range, ":possible_location", walled_centers_begin, walled_centers_end),
				(eq, ":location_feast", -1),
				(party_slot_eq, ":possible_location", slot_town_lord, ":faction_leader"),
				(party_slot_ge, ":possible_location", slot_center_is_besieged_by, 0),
				(assign, ":location_feast", ":possible_location"),
			(try_end),

			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),
			(str_store_string, s14, "str_your_wedding_day_approaches_my_lady"),

		#14-HOLD A FEAST BECAUSE A MALE CHARACTER WANTS TO GET MARRIED
		(else_try),
			(check_quest_active, "qst_wed_betrothed"),
			(neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),

			(quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
			(call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
			(assign, ":feast_host", reg0),
			(store_faction_of_troop, ":feast_host_faction", ":feast_host"),
			(eq, ":feast_host_faction", ":faction_no"),

			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),
			(assign, ":wedding_venue", reg1),

			(is_between, ":wedding_venue", centers_begin, centers_end),
			(party_slot_eq, ":wedding_venue", slot_center_is_besieged_by, -1),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":wedding_venue"),
			(str_store_string, s14, "str_your_wedding_day_approaches"),

		#15-HOLD A FEAST BECAUSE AN NPC WANTS TO GET MARRIED
		(else_try),
            (ge, ":hours_since_last_feast_start", 192), #If at least eight days past last feast start time

			(assign, ":location_feast", -1),

			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(troop_get_slot, ":groom", ":kingdom_lady", slot_troop_betrothed),
				(gt, ":groom", 0), #not the player

				(store_faction_of_troop, ":lady_faction", ":kingdom_lady"),
				(store_faction_of_troop, ":groom_faction", ":groom"),

				(try_begin), #The groom checks if he wants to continue or break off relations. This causes actions, rather than just returns a value, so it probably should be moved elsewhere
					(troop_slot_ge, ":groom", slot_troop_prisoner_of_party, 0),
				(else_try),
					(neq, ":groom_faction", ":lady_faction"),
					(neq, ":groom_faction", "fac_player_faction"),
					(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":kingdom_lady", ":groom"),
				(else_try),
					(eq, ":lady_faction", ":faction_no"),
			        ##diplomacy start+
					#neither the bride nor the groom is in retirement, dead, etc.
					(neg|troop_slot_ge, ":groom", slot_troop_occupation, slto_retirement),
					(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
					##diplomacy end+
		            (store_current_hours, ":hours_since_betrothal"),
		            (troop_get_slot, ":betrothal_time", ":kingdom_lady", slot_troop_betrothal_time),
		            (val_sub, ":hours_since_betrothal", ":betrothal_time"),
		            (ge, ":hours_since_betrothal", 719), #30 days

					(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
					(assign, ":wedding_venue", reg1),

		            (assign, ":location_feast", ":wedding_venue"),
		            (assign, ":final_bride", ":kingdom_lady"),
		            (assign, ":final_groom", ":groom"),
				(try_end),
			(try_end),

			(ge, ":location_feast", centers_begin),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),

			(str_store_troop_name, s22, ":final_bride"),
			(str_store_troop_name, s23, ":final_groom"),
			(str_store_string, s14, "str_s22_and_s23_wish_to_marry"),

		#16-HOLD A FEAST ANYWAY
		(else_try),
			(eq, ":current_ai_state", sfai_default),
            (gt, ":hours_since_last_feast_start", 240), #If at least 10 days past after last feast. (added by ozan)

			(assign, ":location_high_score", 0),
			(assign, ":location_feast", -1),

			(try_for_range, ":location", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":location_faction", ":location"),
				(eq, ":location_faction", ":faction_no"),

				(try_begin),
			        (neg|party_slot_eq, ":location", slot_village_state, svs_under_siege),
		            (party_get_slot, ":location_lord", ":location", slot_town_lord),
		            (is_between, ":location_lord", active_npcs_begin, active_npcs_end),
		            (troop_get_slot, ":location_score", ":location_lord", slot_troop_renown),
		            (store_random_in_range, ":random", 0, 1000), #will probably be king or senior lord
		            (val_add, ":location_score", ":random"),
		            (gt, ":location_score", ":location_high_score"),
		            (assign, ":location_high_score", ":location_score"),
		            (assign, ":location_feast", ":location"),
				(else_try), #do not start new feasts if any place is under siege or being raided
		            (this_or_next|party_slot_eq, ":location", slot_village_state, svs_under_siege),
						(party_slot_eq, ":location", slot_village_state, svs_being_raided),
		            (assign, ":location_high_score", 9999),
		            (assign, ":location_feast", -1),
				(try_end),
			(try_end),

			(is_between, ":location_feast", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":feast_host", ":location_feast", slot_town_lord),
			(troop_slot_eq, ":feast_host", slot_troop_prisoner_of_party, -1),

			(assign, ":action", sfai_feast),
			(assign, ":object", ":location_feast"),
			(str_store_string, s14, "str_it_has_been_a_long_time_since_the_lords_of_the_realm_gathered_for_a_feast"),

		#17-DO NOTHING
		(else_try),
			(neq, ":current_ai_state", sfai_default),

			(assign, ":action", sfai_default),
			(assign, ":object", -1),
			(str_store_string, s14, "str_the_circumstances_which_led_to_this_decision_no_longer_apply_so_we_should_stop_and_reconsider_shortly"),

		#18-DO NOTHING
		(else_try),
			(eq, ":current_ai_state", sfai_default),

			(eq, ":at_peace_with_everyone", 1),

		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_we_are_currently_at_peace"),
		(else_try),
			(eq, ":current_ai_state", sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_marshall, -1),
		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_we_are_waiting_for_selection_of_marshal"),

		(else_try),
			(eq, ":current_ai_state", sfai_default),

		    (assign, ":action", sfai_default),
		    (assign, ":object", -1),
			(str_store_string, s14, "str_the_vassals_still_need_time_to_attend_to_their_own_business"),
		(try_end),

		(assign, reg0, ":action"),
		(assign, reg1, ":object"),
	]),

 	(
	"faction_last_reconnoitered_center", #This is called from within decide_faction_ai, or from
	[
		(store_script_param, ":faction_no", 1),
		(store_script_param, ":center_no", 2),

		(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
		(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
		(store_current_hours, ":hours_since_last_recon"),
		(party_get_slot, ":last_recon_time", ":center_no", ":faction_recce_slot"),

		(try_begin),
			(lt, ":last_recon_time", 1),
			(assign, ":hours_since_last_recon", 1000),
		(else_try),
			(val_sub, ":hours_since_last_recon", ":last_recon_time"),
		(try_end),

		(assign, reg0, ":hours_since_last_recon"),
		(assign, reg1, ":last_recon_time"),
	]),

 	(
	"reduce_exact_number_to_estimate",
	#This is used to simulate limited intelligence
	#It is roughly analogous to the descriptive strings which the player will receive from alarms
	#Information is presumed to be accurate for four days
	#This is obviously cheating for the AI, as the AI will have exact info for four days, and no info at all after that.
	#It would be fairly easy to log the strength at a center when it is scouted, if we want, but I have not done that at this point,
	#The AI also has a hive mind -- ie, each party knows what its allies are thinking. In this, AI factions have an advantage over the player
	#It would be a simple matter to create a set of arrays in which each party's knowledge is individually updated, but that would also take up a lot of data space

	[
		(store_script_param, ":exact_number", 1),

		(try_begin),
			(lt, ":exact_number", 500),
			(assign, ":estimate", 0),
		(else_try),
			(lt, ":exact_number", 1000),
			(assign, ":estimate", 750),
		(else_try),
			(lt, ":exact_number", 2000),
			(assign, ":estimate", 1500),
		(else_try),
			(lt, ":exact_number", 4000),
			(assign, ":estimate", 3000),
		(else_try),
			(lt, ":exact_number", 8000),
			(assign, ":estimate", 6000),
		(else_try),
			(lt, ":exact_number", 16000),
			(assign, ":estimate", 12000),
		(else_try),
			(assign, ":estimate", 24000),
		(try_end),
		##diplomacy start+
		#This currently isn't used anywhere, but modify it if we're thinking about changing that.
		#Take into account campaign AI difficulty -- assume that the difference is either a good
		#spy network or intelligent inference.
		(game_get_reduce_campaign_ai, reg0),
		(try_begin),
			(lt, reg0, 1),#Hard mode
			(assign, ":estimate", ":exact_number"),
		(else_try),
			(eq, reg0, 1),#Medium Mode
			(val_add, ":estimate", ":exact_number"),
			(val_div, ":estimate", 2),
		(try_end),
		##diplomacy end+

		(assign, reg0, ":estimate"),
	]),

   #script_calculate_castle_prosperities_by_using_its_villages
 	(
	"calculate_castle_prosperities_by_using_its_villages", #This is called from within decide_faction_ai, or from
	[
	  (try_for_range, ":cur_castle", castles_begin, castles_end),
	    (assign, ":total_prosperity", 0),
	    (assign, ":total_villages", 0),

	    (try_for_range, ":cur_village", villages_begin, villages_end),
	      (party_get_slot, ":bound_center", ":cur_village", slot_village_bound_center),
	      (eq, ":cur_castle", ":bound_center"),

	      (party_get_slot, ":village_prosperity", ":cur_village", slot_town_prosperity),

	      (val_add, ":total_prosperity", ":village_prosperity"),
	      (val_add, ":total_villages", 1),
	    (try_end),

	    (try_begin),
	      (store_div, ":castle_prosperity", ":total_prosperity", ":total_villages"),
	    (else_try),
	      (assign, ":castle_prosperity", 50),
	    (try_end),

	    (party_set_slot, ":cur_castle", slot_town_prosperity, ":castle_prosperity"),
	  (try_end),
	]),

  # 1175 feature: improve relation with allied lords who fought alongside the player.
  ("change_player_relation_with_lords_after_battle",
    [
      (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
        (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
        (gt, ":hero_present", 0),
        (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":reputation", ":hero", slot_lord_reputation_type),
        (call_script, "script_troop_get_player_relation", ":hero"),
        (assign, ":troop_relation", reg0),
        (assign, ":relation_change", 1),
        (try_begin),
          (lt, ":troop_relation", -5),
          (assign, ":relation_change", 0),
        (else_try),
          (eq, ":reputation", lrep_martial),
          (assign, ":relation_change", 2),
        (try_end),
        (call_script, "script_change_player_relation_with_troop", ":hero", ":relation_change"),
      (try_end),
    ]),

   #script_initialize_tavern_variables
]
scripts.extend(music_scripts)
scripts.extend(orders_scripts)
scripts.extend(siege_scripts)
scripts.extend(training_ground_scripts)
scripts.extend(multiplayer_scripts)
scripts.extend(economy_scripts)
scripts.extend(quest_scripts)
scripts.extend(morale_scripts)
scripts.extend(heraldry_scripts)
scripts.extend(arena_scripts)
scripts.extend(encounters_scripts)
scripts.extend(party_ai_scripts)
scripts.extend(centers_scripts)
scripts.extend(npcs_scripts)
scripts.extend(faction_ai_scripts)
scripts.extend(core_scripts)
scripts.extend(misc_scripts)
scripts.extend(misc_scripts_extra)
scripts.extend(misc_scripts_extra2)
scripts.extend(diplomacy_scripts)
scripts.extend(dickplomacy_scripts)
scripts.extend(feats_scripts)

# modmerger_start version=201 type=2
try:
    component_name = "scripts"
    var_set = { "scripts" : scripts }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
