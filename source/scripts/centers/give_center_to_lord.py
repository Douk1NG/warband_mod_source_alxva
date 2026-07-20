# ======================================================================
# SHARED DEPENDENCY
# Entity: give_center_to_lord (script)
# Called by menus in 3 domains: castle, diplomacy, notifications
# ======================================================================

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

give_center_to_lord_scripts = [
# script_change_troop_faction
# Input: arg1 = center_no, arg2 = lord_troop, arg3 = add_garrison_to_center
("give_center_to_lord",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":lord_troop_id", 2), #-1 only in the case of a player deferring ownership of a center
      (store_script_param, ":add_garrison", 3),
      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      ##diplomacy end

      ##diplomacy start+
      #For relation changes below, store all heroes' center points and closest fiefs.
      (call_script, "script_dplmc_prepare_hero_center_points_ignoring_center", ":center_no"),

      #(assign, ":player_declines_honor", 0),
      #(try_begin),
      #	  (gt, "$g_dont_give_fief_to_player_days", 1),
      #	  (assign, ":player_declines_honor", 1),
      #(try_end),
      ##diplomacy end+

      (try_begin),
      ##diplomacy start+ notable events like this should be logged by default
        (store_current_hours, ":hours"),
        (ge, ":hours", 1),#Don't spam the game log during world setup
        (ge, ":lord_troop_id", 0),
        (str_store_party_name_link, s4, ":center_no"),
        (str_store_troop_name_link, s5, ":lord_troop_id"),
        (store_troop_faction, ":msg_faction_no", ":lord_troop_id"),
        (faction_get_color, ":color", ":msg_faction_no"), #SB : colorize
        (str_store_faction_name_link, s7, ":msg_faction_no"),
        (try_begin),
           (faction_slot_eq, ":msg_faction_no", slot_faction_leader, ":lord_troop_id"),
           (display_log_message, "@{s5} of the {s7} has taken ownership of {s4}.", ":color"),
        (else_try),
           (display_log_message, "@{s4} has been awarded to {s5} of the {s7}.", ":color"),
        (try_end),
      (else_try),
	  ##diplomacy end+
	   (eq, "$cheat_mode", 1),
		(ge, ":lord_troop_id", 0),
		(str_store_party_name, s4, ":center_no"),
		(str_store_troop_name, s5, ":lord_troop_id"),
		(display_message, "@{!}DEBUG -- {s4} awarded to {s5}"),
	  (try_end),

	  (try_begin),
	    (eq, ":lord_troop_id", "trp_player"),
	    (unlock_achievement, ACHIEVEMENT_ROYALITY_PAYMENT),

	    (assign, ":number_of_fiefs_player_have", 1),
	    (try_for_range, ":cur_center", centers_begin, centers_end),
	      (neq, ":cur_center", ":center_no"),
	      (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
	      (val_add, ":number_of_fiefs_player_have", 1),
	    (try_end),

	    (ge, ":number_of_fiefs_player_have", 5),
	    (unlock_achievement, ACHIEVEMENT_MEDIEVAL_EMLAK),
	  (try_end),

      (party_get_slot, ":old_lord_troop_id", ":center_no", slot_town_lord),

	  (try_begin), #This script is ONLY called with lord_troop_id = -1 when it is the player faction
	  ##diplomacy start+
	  #The player can now also be co-ruler of a NPC kingdom.
         (eq, ":lord_troop_id", -1),

		 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		 (faction_get_slot, ":players_kingdom_liege", "$players_kingdom", slot_faction_leader),
		 (gt, ":players_kingdom_liege", -1),
		 (this_or_next|eq, ":players_kingdom_liege", "trp_player"),
		 (this_or_next|troop_slot_eq, ":players_kingdom_liege", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":players_kingdom_liege"),

		(assign, ":lord_troop_faction", "$players_kingdom"),
		(party_set_banner_icon, ":center_no", 0),#Removing banner
	  (else_try),
	  ##diplomacy end+
	    (eq, ":lord_troop_id", -1),
	    (assign, ":lord_troop_faction", "fac_player_supporters_faction"),
        (party_set_banner_icon, ":center_no", 0),#Removing banner

      (else_try),
	    (eq, ":lord_troop_id", "trp_player"),
	    (assign, ":lord_troop_faction", "$players_kingdom"), #was changed on Apr 27 from fac_plyr_sup_fac

      (else_try),
		(store_troop_faction, ":lord_troop_faction", ":lord_troop_id"),
	  (try_end),
	  (faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),

	  (try_begin),
	    (eq, ":faction_leader", "trp_player"),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_QUEEN),
        (try_end),
	  (try_end),

	  (try_begin),
		(eq, ":faction_leader", ":old_lord_troop_id"),
		(call_script, "script_add_log_entry", logent_liege_grants_fief_to_vassal, ":faction_leader", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
        (troop_set_slot, ":lord_troop_id", slot_troop_promised_fief, 0),
	  (try_end),

      (try_begin),
	    (eq, ":lord_troop_id", -1), #Lord troop ID -1 is only used when a player is deferring assignment of a fief
        (party_set_faction, ":center_no", "$players_kingdom"),
	  (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (gt, "$players_kingdom", 0),
        (party_set_faction, ":center_no", "$players_kingdom"),
      (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (neg|is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (party_set_faction, ":center_no", "fac_player_supporters_faction"),
      (else_try),
        (party_set_faction, ":center_no", ":lord_troop_faction"),
      (try_end),
      (party_set_slot, ":center_no", slot_town_lord, ":lord_troop_id"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party_no", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party_no", 0),
        (party_is_active, ":farmer_party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (party_set_faction, ":farmer_party_no", ":center_faction"),
      (try_end),

    (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
		(gt, ":lord_troop_id", -1),

#normal_banner_begin
        (troop_get_slot, ":cur_banner", ":lord_troop_id", slot_troop_banner_scene_prop),
        (try_begin),
            (gt, ":cur_banner", 0),
            (val_sub, ":cur_banner", banner_scene_props_begin),
            (val_add, ":cur_banner", banner_map_icons_begin),
            (party_set_banner_icon, ":center_no", ":cur_banner"),
# custom_banner_begin
       (else_try),
           (eq, ":cur_banner", -1),
           (troop_get_slot, ":flag_icon", ":lord_troop_id", slot_troop_custom_banner_map_flag_type),

           # (assign, reg0, ":flag_icon"),
           # (str_store_troop_name, s5, ":lord_troop_id",),
           # (display_message, "@{s5} : {reg0}"),

           (ge, ":flag_icon", 0),
           (val_add, ":flag_icon", custom_banner_map_icons_begin),
           (party_set_banner_icon, ":center_no", ":flag_icon"),
       (try_end),

       (neq, ":lord_troop_id", "trp_player"),
       #free all captive ladies
       (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
           (troop_get_slot, ":prisoner_of_party", ":lady", slot_troop_prisoner_of_party),
           (neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
           (eq, ":center_no", ":prisoner_of_party"),
           (call_script, "script_remove_troop_from_prison", ":lady"),
           (store_faction_of_troop, ":lady_faction", ":lady"),
           (store_faction_of_troop, ":release_faction", ":lord_troop_id"),
           (faction_get_color, ":lady_faction_color", ":lady_faction"),
           (str_store_troop_name_link, s1, ":lady"),
           (str_store_faction_name_link, s2, ":release_faction"),
           (str_store_faction_name_link, s3, ":lady_faction"),
           (display_log_message, "@{s1} of {s3} has been released from captivity by {s2}.", ":lady_faction_color"),
       (try_end),

    (try_end),

#    (try_begin),
#		(eq, 1, 0),
 #       (eq, ":lord_troop_id", "trp_player"),
 #       (neq, ":old_lord_troop_id", "trp_player"),
 #       (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
 #       (is_between, ":center_relation", -4, 5),
 #       (call_script, "script_change_player_relation_with_center", ":center_no", 5),
 #       (gt, ":old_lord_troop_id", 0),
 #       (call_script, "script_change_player_relation_with_troop", ":old_lord_troop_id", -25),
 #   (try_end),
	(try_begin),
		(gt, ":lord_troop_id", -1),
		(call_script, "script_update_troop_notes", ":lord_troop_id"),
	(try_end),

    (call_script, "script_update_center_notes", ":center_no"),

    (try_begin),
      (gt, ":lord_troop_faction", 0),
      (call_script, "script_update_faction_notes", ":lord_troop_faction"),
    (try_end),

    (try_begin),
        (ge, ":old_lord_troop_id", 0),
        (call_script, "script_update_troop_notes", ":old_lord_troop_id"),
        (store_troop_faction, ":old_lord_troop_faction", ":old_lord_troop_id"),
        (call_script, "script_update_faction_notes", ":old_lord_troop_faction"),
    (try_end),

    (try_begin),
        (eq, ":add_garrison", 1),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":garrison_strength", 3),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 9),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (try_for_range, ":unused", 0, 7),
          (store_mul, ":xp_range_min", 150, ":garrison_strength"),
          (store_mul, ":xp_range_max", 200, ":garrison_strength"),
          (store_random_in_range, ":xp", ":xp_range_min", ":xp_range_max"),
          (party_upgrade_with_xp, ":center_no", ":xp", 0),
        (try_end),
    (try_end),

	(faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),
	(store_current_hours, ":hours"),

	#the next block handles gratitude, objections and jealousies
	(try_begin),
	  	(gt, ":hours", 0),
		(gt, ":lord_troop_id", 0),

    	(call_script, "script_troop_change_relation_with_troop", ":lord_troop_id", ":faction_leader", 10),
		(val_add, "$total_promotion_changes", 10),

		#smaller factions are more dramatically influenced by internal jealousies
		#Disabled as of NOV 2010
#		(try_begin),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 4),
#			(assign, ":faction_size_multiplier", 6),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 8),
#			(assign, ":faction_size_multiplier", 5),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 16),
#			(assign, ":faction_size_multiplier", 4),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 32),
#			(assign, ":faction_size_multiplier", 3),
#		(else_try),
#			(assign, ":faction_size_multiplier", 2),
#		(try_end),

		#factional politics -- each lord in the faction adjusts his relation according to the relation with the lord receiving the faction
		##diplomacy start+ add support for kingdom ladies
		#(try_for_range, ":other_lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":other_lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":other_lord", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":other_lord", ":lord_troop_id"),

		    (store_troop_faction, ":other_troop_faction", ":other_lord"),
		    (eq, ":lord_troop_faction", ":other_troop_faction"),

		    (neq, ":other_lord", ":faction_leader"),

	        (call_script, "script_troop_get_relation_with_troop", ":other_lord", ":lord_troop_id"),
			(assign, ":relation_with_troop", reg0),

			#relation reduction = relation/10 minus 2. So,0 = -2, 8 = -1, 16+ = no change or bonus, 24+ gain one point
		    (store_div, ":relation_with_liege_change", ":relation_with_troop", 8), #changed from 16
		    (val_sub, ":relation_with_liege_change", 2),

		    (val_clamp, ":relation_with_liege_change", -5, 3),

			(try_begin),
				#upstanding and goodnatured lords will not lose relation unless they actively dislike the other lord
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
				 ##diplomacy start+ add companion/lady personality types
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_benefactor),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_conventional),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_moralist),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_otherworldly),
				 ##diplomacy end+
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_goodnatured),
				(ge, ":relation_with_troop", 0),
				(val_max, ":relation_with_liege_change", 0),
			(else_try),
				#penalty is increased for lords who have the more unpleasant reputation types
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
				(lt, ":relation_with_liege_change", 0),
				(val_mul, ":relation_with_liege_change", 3),
				(val_div, ":relation_with_liege_change", 2),
			(try_end),
			##diplomacy start+

			#TODO (idea for "high"): instead of being absolute, the sliding score system should be used.
			#(So you can use a score instead of using relations.)  The greater the
			#difference in score, the greater the relation loss -- so if the lord
			#was nearly indifferent between two candidates, the difference would be
			#lesser.
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					#Optional change: Non-jerkish lords will not object to giving a village to
					#someone fiefless, unless they dislike him.
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
					(lt, ":relation_with_liege_change", 0),
					(is_between, ":center_no", villages_begin, villages_end),
					(troop_slot_eq, ":lord_troop_id", slot_troop_temp_slot, 0),
					(ge, ":relation_with_troop", 0),
					(val_max, ":relation_with_liege_change", 0),
				(try_end),
				(try_begin),
					#Optional change: because taking a penalty for 'thrashing' the same fief
					#back and forth is silly, if you're giving the fief back to the lord who
					#last had it, reduce any penalty.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),
					(neq, ":lord_troop_id", 0),
					(val_add, ":relation_with_liege_change", 1),

					#If the other lord doesn't have any claim of his own on the center,
					#attenuate the penalty more.
					(lt, ":relation_with_liege_change", 0),
					(ge, ":relation_with_troop", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),
					(val_add, ":relation_with_liege_change", 1),
				(else_try),
					#Similar logic, but for "original lord" instead of most recent lord
					(lt, ":relation_with_liege_change", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),#don't apply this if the above "ex-center" check was applied
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":lord_troop_id"),
						(troop_slot_eq, ":lord_troop_id", slot_troop_home, ":center_no"),

					#Only attenuate the panelty if the other lord doesn't have any claim of his own on the center
					(ge, ":relation_with_troop", 0),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),

					(val_add, ":relation_with_liege_change", 1),
				(try_end),
				(try_begin),
					#On the minus side, lords whose homes and/or original fiefs are not
					#disposed according to their wishes are that much more cross.
					(lt, ":relation_with_liege_change", 1),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					   (troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(val_sub, ":relation_with_liege_change", 1),
				(else_try),
					#Optional change: martial lords are less displeased by awarding a fief to
					#the one who conquered it.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":lord_troop_id"),
					(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_martial),
					(val_add, ":relation_with_liege_change", 1),
				(try_end),
			(try_end),
			##diplomacy end+

		    (neq, ":relation_with_liege_change", 0),
			#removed Nov 2010
#		  	(val_mul, ":relation_reduction", ":faction_size_multiplier"),
#		  	(val_div, ":relation_reduction", 2),
			#removed Nov 2010

			(try_begin),
				(troop_slot_eq, ":other_lord", slot_troop_stance_on_faction_issue, ":lord_troop_id"),
				(val_add, ":relation_with_liege_change", 1),
				(val_max, ":relation_with_liege_change", 1),
			(try_end),

 	        (call_script, "script_troop_change_relation_with_troop", ":other_lord", ":faction_leader", ":relation_with_liege_change"),
			(val_add, "$total_promotion_changes", ":relation_with_liege_change"),

		    (try_begin),
				(this_or_next|le, ":relation_with_liege_change", -4), #Nov 2010 - changed from -8
				(this_or_next|troop_slot_eq, ":other_lord", slot_troop_promised_fief, 1), #1 is any fief
					(troop_slot_eq, ":other_lord", slot_troop_promised_fief, ":center_no"),
				(call_script, "script_add_log_entry", logent_troop_feels_cheated_by_troop_over_land, ":other_lord", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
		    (try_end),

		(try_end),
	(try_end),

	##diplomacy start+ invalidate cached center points
	(try_begin),
		(neq, ":old_lord_troop_id", ":lord_troop_id"),
		(try_begin),
			(gt, ":old_lord_troop_id", -1),
			(troop_set_slot, ":old_lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
		(try_begin),
			(gt, ":lord_troop_id", -1),
			(troop_set_slot, ":lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
	(try_end),
	##diplomacy end+

	#Villages from another faction will also be transferred along with a fortress
    (try_begin),
		(is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (try_for_range, ":cur_village", villages_begin, villages_end),
			(party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),
			(store_faction_of_party, ":cur_village_faction", ":cur_village"),
			(neq, ":cur_village_faction", ":lord_troop_faction"),

			(call_script, "script_give_center_to_lord", ":cur_village", ":lord_troop_id", 0),
        (try_end),
    (try_end),
  ])
]
