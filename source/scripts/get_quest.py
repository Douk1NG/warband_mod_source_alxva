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

get_quest_scripts = [
# Input: arg1 = troop_no (of the troop in conversation), arg2 = min_importance (of the quest)
# Output: reg0 = quest_no (the slots of the quest will be filled after calling this script)
("get_quest",
    [
      (store_script_param_1, ":giver_troop"),

      (store_character_level, ":player_level", "trp_player"),
      (store_troop_faction, ":giver_faction_no", ":giver_troop"),

      (troop_get_slot, ":giver_party_no", ":giver_troop", slot_troop_leaded_party),
      (troop_get_slot, ":giver_reputation", ":giver_troop", slot_lord_reputation_type),

      (assign, ":giver_center_no", -1),
      (try_begin),
        (gt, ":giver_party_no", 0),
        (party_get_attached_to, ":giver_center_no", ":giver_party_no"),
      (else_try),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (assign, ":giver_center_no", "$g_encountered_party"),
      (try_end),

	  ##diplomacy start+
	  (call_script, "script_troop_get_player_relation", ":giver_troop"),
	  (assign, ":giver_relation", reg0),
	  (store_relation, ":giver_faction_relation", ":giver_faction_no", "fac_player_faction"),
	  #Assign some variables used later (mostly in lord checks) to re-enable
	  #quests which are usually disabled once the player has received homage.
	  (assign, ":is_close", 0),
	  (assign, ":nominal_superior", 0),
	  (try_begin),
		#is valid hero:
		(is_between, ":giver_troop", heroes_begin, heroes_end),
		(troop_slot_ge, ":giver_troop", slot_troop_occupation, slto_inactive + 1),
		(neg|troop_slot_ge, ":giver_troop", slot_troop_occupation, slto_retirement),

		#is close:
		(try_begin),
			#affiliates, and spouse
			(call_script, "script_dplmc_is_affiliated_family_member", ":giver_troop"),
			(this_or_next|ge, reg0, 1),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":giver_troop"),
			(assign, ":is_close", 1),
		(else_try),
			(ge, ":giver_faction_relation", 0),
			(ge, ":giver_relation", 50),
			(try_begin),
				(this_or_next|is_between, ":giver_troop", companions_begin, companions_end),
					(is_between, ":giver_troop", pretenders_begin, pretenders_end),
				(this_or_next|troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
					(troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_player_companion),
				(neg|troop_slot_eq, ":giver_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
				(assign, ":is_close", 1),
			(else_try),
				#(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop", "trp_player"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":giver_troop", "trp_player"),
				(ge, reg0, 2),
				(assign, ":is_close", 1),
			(try_end),
		(try_end),

		#is nominally the social superior of the player (or even if not the superior,
		#is allowed to give the player orders in at least one context)
		(try_begin),
			#quest giver is faction leader or marshall, or player's father or mother
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_father, ":giver_troop"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_mother, ":giver_troop"),
			(this_or_next|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
				(faction_slot_eq, ":giver_faction_no", slot_faction_marshall, ":giver_troop"),
			(assign, ":nominal_superior", 1),
		(else_try),
			#player has less than 3/4 of the quest giver's renown
			(troop_get_slot, reg0, ":giver_troop", slot_troop_renown),
			(val_mul, reg0, 3),
			(val_div, reg0, 4),
			(neg|troop_slot_ge, "trp_player", slot_troop_renown, reg0),
			(assign, ":nominal_superior", 1),
		(else_try),
			#quest giver is player's father-in-law or mother-in-law
			(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
			(is_between, ":player_spouse", heroes_begin, heroes_end),
			(this_or_next|troop_slot_eq, ":player_spouse", slot_troop_father, ":giver_troop"),
				(troop_slot_eq, ":player_spouse", slot_troop_mother, ":giver_troop"),
			(assign, ":nominal_superior", 1),
		(try_end),
	  (try_end),
	  ##diplomacy end+

      (try_begin),
        (troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
        (try_begin),
          (ge, "$g_talk_troop_faction_relation", 0),
          (assign, ":quests_begin", lord_quests_begin),
          (assign, ":quests_end", lord_quests_end),
          (assign, ":quests_begin_2", lord_quests_begin_2),
          (assign, ":quests_end_2", lord_quests_end_2),
        (else_try),
          (assign, ":quests_begin", enemy_lord_quests_begin),
          (assign, ":quests_end", enemy_lord_quests_end),
          (assign, ":quests_begin_2", 0),
          (assign, ":quests_end_2", 0),
        (try_end),
      (else_try),
        (is_between, ":giver_troop", village_elders_begin, village_elders_end),
        (assign, ":quests_begin", village_elder_quests_begin),
        (assign, ":quests_end", village_elder_quests_end),
        (assign, ":quests_begin_2", village_elder_quests_begin_2),
        (assign, ":quests_end_2", village_elder_quests_end_2),
      (else_try),
        (is_between, ":giver_troop", mayors_begin, mayors_end),
        (assign, ":quests_begin", mayor_quests_begin),
        (assign, ":quests_end", mayor_quests_end),
        (assign, ":quests_begin_2", mayor_quests_begin_2),
        (assign, ":quests_end_2", mayor_quests_end_2),
      (else_try),
        (assign, ":quests_begin", lady_quests_begin),
        (assign, ":quests_end", lady_quests_end),
        (assign, ":quests_begin_2", lady_quests_begin_2),
        (assign, ":quests_end_2", lady_quests_end_2),
      (try_end),

      (assign, ":result", -1),
	  (assign, ":quest_target_troop", -1),
	  (assign, ":quest_target_center", -1),
	  (assign, ":quest_target_faction", -1),
	  (assign, ":quest_object_faction", -1),
	  (assign, ":quest_object_troop", -1),
	  (assign, ":quest_object_center", -1),
	  (assign, ":quest_target_party", -1),
	  (assign, ":quest_target_party_template", -1),
	  (assign, ":quest_target_amount", -1),
	  (assign, ":quest_target_dna", -1),
	  (assign, ":quest_target_item", -1),
	  (assign, ":quest_importance", 1),
	  (assign, ":quest_xp_reward", 0),
	  (assign, ":quest_gold_reward", 0),
	  (assign, ":quest_convince_value", 0),
	  (assign, ":quest_expiration_days", 0),
	  (assign, ":quest_dont_give_again_period", 0),

	  (try_begin), #get dynamic quest is a separate script, so that we can scan a number of different troops at once for it
	   	(call_script, "script_get_dynamic_quest", "$g_talk_troop"),

	    (assign, ":result", reg0),
	    (assign, ":relevant_troop", reg1),
	    (assign, ":relevant_party", reg2),
	    (assign, ":relevant_faction", reg3),

	    #GUILDMASTER QUESTS
	    (try_begin),
			(eq, ":result", "qst_track_down_bandits"),
			(assign, ":quest_target_party", ":relevant_party"),
			(assign ,":quest_expiration_days", 60),
			(assign, ":quest_xp_reward", 1000),
			(assign, ":quest_gold_reward", 1000),

		(else_try),
			(eq, ":result", "qst_retaliate_for_border_incident"),
			(assign, ":quest_target_troop", ":relevant_troop"),
			(assign, ":quest_target_faction", ":relevant_faction"),

			(assign ,":quest_expiration_days", 30),
			(assign, ":quest_xp_reward", 1000),
			(assign, ":quest_gold_reward", 1000),

		#KINGDOM LORD QUESTS
		(else_try),
	        (eq, ":result", "qst_cause_provocation"),
			(assign, ":quest_target_faction", ":relevant_faction"),
	        (assign, ":quest_expiration_days", 30),
	        (assign, ":quest_dont_give_again_period", 100),
			(assign, ":quest_xp_reward", 1000),
			(assign, ":quest_gold_reward", 1000),

	    (else_try),
			(eq, ":result", "qst_destroy_bandit_lair"),
			(assign, ":quest_target_party", ":relevant_party"),
			(assign ,":quest_expiration_days", 60),
			(assign, ":quest_xp_reward", 3000),
			(assign, ":quest_gold_reward", 1500),

		#KINGDOM LADY OR KINGDOM HERO QUESTS
		(else_try),
			(eq, ":result", "qst_rescue_prisoner"),
			(assign, ":quest_target_troop", ":relevant_troop"),
			(assign, ":quest_target_center", ":relevant_party"),

			(assign, ":quest_expiration_days", 30),
			(assign, ":quest_dont_give_again_period", 5),
			(assign, ":quest_importance", 2),
			(assign, ":quest_xp_reward", 1500),
			(assign, ":quest_gold_reward", 2000), #actual reward in dialogues
            (store_character_level, ":quest_convince_value", ":quest_target_troop"),
			(val_mul, ":quest_convince_value", 65), #SB : we normalize this to match the gold reward for ~level 30 lords
            (call_script, "script_calculate_ransom_amount_for_troop", ":quest_target_troop"), #SB: calculate a set amount
            (assign, ":quest_target_amount", reg0),
		(try_end),
	  (try_end),

	  #no dynamic quest available
	  (try_begin),
		(eq, ":result", -1),

	    (try_for_range, ":unused", 0, 20), #Repeat trial twenty times
	        (eq, ":result", -1),
	        (assign, ":quest_target_troop", -1),
	        (assign, ":quest_target_center", -1),
	        (assign, ":quest_target_faction", -1),
	        (assign, ":quest_object_faction", -1),
	        (assign, ":quest_object_troop", -1),
	        (assign, ":quest_object_center", -1),
	        (assign, ":quest_target_party", -1),
	        (assign, ":quest_target_party_template", -1),
	        (assign, ":quest_target_amount", -1),
	        (assign, ":quest_target_dna", -1),
	        (assign, ":quest_target_item", -1),
	        (assign, ":quest_importance", 1),
	        (assign, ":quest_xp_reward", 0),
	        (assign, ":quest_gold_reward", 0),
	        (assign, ":quest_convince_value", 0),
	        (assign, ":quest_expiration_days", 0),
	        (assign, ":quest_dont_give_again_period", 0),

            (store_sub, ":num_possible_old_quests", ":quests_end", ":quests_begin"),
            (store_sub, ":num_possible_new_quests", ":quests_end_2", ":quests_begin_2"),
            (store_add, ":num_possible_total_quests", ":num_possible_old_quests", ":num_possible_new_quests"),

            (store_random_in_range, ":quest_no", 0, ":num_possible_total_quests"),
            (try_begin),
              (lt, ":quest_no", ":num_possible_old_quests"),
              (store_random_in_range, ":quest_no", ":quests_begin", ":quests_end"),
            (else_try),
              (store_random_in_range, ":quest_no", ":quests_begin_2", ":quests_end_2"),
            (try_end),

	        (neg|check_quest_active,":quest_no"),
	        (neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
	        (try_begin),
	          # Village Elder quests
	          (eq, ":quest_no", "qst_deliver_grain"),
	          (try_begin),
	            (is_between, ":giver_center_no", villages_begin, villages_end),
	            #The quest giver is the village elder
	            (call_script, "script_get_troop_item_amount", ":giver_troop", "itm_grain"),
	            (eq, reg0, 0),
	            (neg|party_slot_ge, ":giver_center_no", slot_town_prosperity, 40),
	            (assign, ":quest_target_center", ":giver_center_no"),
	            (store_random_in_range, ":quest_target_amount", 4, 8),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 20),
	            (assign, ":result", ":quest_no"),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_deliver_cattle"),
	          (try_begin),
	            (is_between, ":giver_center_no", villages_begin, villages_end),
	            #The quest giver is the village elder
	            (party_get_slot, ":num_cattle", ":giver_center_no", slot_village_number_of_cattle),
	            (lt, ":num_cattle", 50),
	            (assign, ":quest_target_center", ":giver_center_no"),
	            (store_random_in_range, ":quest_target_amount", 5, 10),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 20),
	            (assign, ":result", ":quest_no"),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_train_peasants_against_bandits"),
	          (try_begin),
	            (is_between, ":giver_center_no", villages_begin, villages_end),
	            #The quest giver is the village elder
	            (store_skill_level, ":player_trainer", "skl_trainer", "trp_player"),
	            (gt, ":player_trainer", 0),
	            (store_random_in_range, ":quest_target_amount", 5, 8),
                #SB : add condition to have at least this many farmers remaining to show up
                (party_count_members_of_type, ":num_villagers", ":giver_center_no", "trp_farmer"), #disallow peasant woman
                (gt, ":num_villagers", ":quest_target_amount"), #+1 for village elder
	            (assign, ":quest_target_center", ":giver_center_no"),
	            (assign, ":quest_expiration_days", 20),
	            (assign, ":quest_dont_give_again_period", 40),
	            (assign, ":result", ":quest_no"),
	          (try_end),
	        (else_try),
	          # Mayor quests
	          (eq, ":quest_no", "qst_escort_merchant_caravan"),
	          (is_between, ":giver_center_no", centers_begin, centers_end),
	          (store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
	          (store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
	          (assign, ":quest_gold_reward", ":dist"),
	          (val_add, ":quest_gold_reward", 25),
	          (val_mul, ":quest_gold_reward", 25),
	          (val_div, ":quest_gold_reward", 20),
	          (store_random_in_range, ":quest_target_amount", 6, 12),
	          # (assign, "$escort_merchant_caravan_mode", 0), #SB : useless global, use quest slots if necessary
	          (assign, ":result", ":quest_no"),
	        (else_try),
              (eq, ":quest_no", "qst_deliver_wine"),
              (is_between, ":giver_center_no", centers_begin, centers_end),
              (store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
              (store_random_in_range, ":random_no", 0, 2),
              #SB : add chance of random food product
              (try_begin),
                (eq, ":random_no", 0), #as before, but skip the need for a quest variant
                (store_random_in_range, ":quest_target_item", "itm_wine", food_begin),
              (else_try),
                (store_random_in_range, ":quest_target_item", food_begin, food_end),
              (try_end),
              (store_random_in_range, ":quest_target_amount", 6, 12),
              (store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),

              #SB : also, instead of emptying target center of merchandise, pick one that's actually missing food
              (assign, ":quest_gold_reward", ":dist"),
              (val_add, ":quest_gold_reward", 2),
              (assign, ":multiplier", 5),
              (val_add, ":multiplier", ":quest_target_amount"),
              (val_mul, ":quest_gold_reward", ":multiplier"),
              (val_div, ":quest_gold_reward", 100),
              (val_mul, ":quest_gold_reward", 10),
              (item_get_max_ammo, ":max_amount", ":quest_target_item"),

              (store_item_value,"$qst_deliver_wine_debt",":quest_target_item"),
              (val_mul,"$qst_deliver_wine_debt",":quest_target_amount"),
              (val_mul,"$qst_deliver_wine_debt", 6),
              (val_div,"$qst_deliver_wine_debt", 5),

              (val_mul, ":quest_target_amount", ":max_amount"), #store actual quantity

              (assign, ":quest_expiration_days", 7), #SB : probably calculate distance for possible spoilage?
              (assign, ":quest_dont_give_again_period", 20),
              (assign, ":result", ":quest_no"),
	        (else_try),
	          (eq, ":quest_no", "qst_troublesome_bandits"),
	          (is_between, ":giver_center_no", centers_begin, centers_end),
	          (store_character_level, ":quest_gold_reward", "trp_player"),
	          (val_add, ":quest_gold_reward", 20),
	          (val_mul, ":quest_gold_reward", 35),
	          (val_div, ":quest_gold_reward",100),
	          (val_mul, ":quest_gold_reward", 10),
	          (assign, ":quest_expiration_days", 30),
	          (assign, ":quest_dont_give_again_period", 30),
	          (assign, ":result", ":quest_no"),
	        (else_try),
	          (eq, ":quest_no", "qst_kidnapped_girl"),
	          (is_between, ":giver_center_no", centers_begin, centers_end),
	          (store_random_in_range, ":quest_target_center", villages_begin, villages_end),
	          (store_character_level, ":quest_target_amount"),
	          (val_add, ":quest_target_amount", 15),
	          (store_distance_to_party_from_party, ":dist", ":giver_center_no", ":quest_target_center"),
	          (val_add, ":dist", 15),
	          (val_mul, ":dist", 2),
	          (val_mul, ":quest_target_amount", ":dist"),
	          (val_div, ":quest_target_amount",100),
	          (val_mul, ":quest_target_amount",10),
	          (assign, ":quest_gold_reward", ":quest_target_amount"),
	          (val_div, ":quest_gold_reward", 40),
	          (val_mul, ":quest_gold_reward", 10),
              (assign, ":quest_expiration_days", 15),
	          (assign, ":quest_dont_give_again_period", 30),
	          (assign, ":result", ":quest_no"),
	        (else_try),
	          (eq, ":quest_no", "qst_move_cattle_herd"),
	          (is_between, ":giver_center_no", centers_begin, centers_end),
	          (call_script, "script_cf_select_random_town_at_peace_with_faction", ":giver_faction_no"),
	          (neq, ":giver_center_no", reg0),
	          (assign, ":quest_target_center", reg0),
	          (store_distance_to_party_from_party, ":dist",":giver_center_no",":quest_target_center"),
	          (assign, ":quest_gold_reward", ":dist"),
	          (val_add, ":quest_gold_reward", 25),
	          (val_mul, ":quest_gold_reward", 50),
	          (val_div, ":quest_gold_reward", 20),
	          (assign, ":quest_expiration_days", 30),
	          (assign, ":quest_dont_give_again_period", 20),
	          (assign, ":result", ":quest_no"),
	        (else_try),
	          (eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
	          (is_between, ":giver_center_no", centers_begin, centers_end),
	          (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
	          (call_script, "script_cf_faction_get_random_enemy_faction", ":cur_object_faction"),
	          (assign, ":cur_target_faction", reg0),
	          (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_object_faction"),
	          (assign, ":cur_object_troop", reg0),
			  ##diplomacy start+
			  #may also be anyone with tmt_aristocrat > 0
			  (call_script, "script_dplmc_get_troop_morality_value", ":cur_object_troop", tmt_aristocratic),
			  (this_or_next|ge, reg0, 1),
			  ##diplomacy+
			  (this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_quarrelsome),
			  (this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_selfrighteous),
			  (this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_martial),
				(troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_debauched),

	          (call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_target_faction"),
	          (assign, ":quest_target_troop", reg0),
			  ##diplomacy start+
			  #may also be anyone with tmt_aristocrat > 0
			  (call_script, "script_dplmc_get_troop_morality_value", ":quest_target_troop", tmt_aristocratic),
			  (this_or_next|ge, reg0, 1),
			  ##diplomacy+
			  (this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_quarrelsome),
			  (this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_selfrighteous),
			  (this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_martial),
			  (troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_debauched),

	          (assign, ":quest_object_troop", ":cur_object_troop"),
	          (assign, ":quest_target_faction", ":cur_target_faction"),
	          (assign, ":quest_object_faction", ":cur_object_faction"),
	          (assign, ":quest_gold_reward", 12000),
	          (assign, ":quest_convince_value", 7000),
	          (assign, ":quest_expiration_days", 30),
	          (assign, ":quest_dont_give_again_period", 100),
	          (assign, ":result", ":quest_no"),
	        (else_try),
              (eq, ":quest_no", "qst_deal_with_looters"),
                  ##diplomacy start+
                  #re-enable looters quest at all levels for variety
              #(is_between, ":player_level", 0, 15),
                  ##diplomacy end+
              (is_between, ":giver_center_no", centers_begin, centers_end),
              (store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
              (store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
              (party_template_set_slot,"pt_looters",slot_party_template_num_killed,":num_looters_destroyed"),
              (quest_set_slot,":quest_no",slot_quest_current_state,0),
              (quest_set_slot,":quest_no",slot_quest_target_party_template,"pt_looters"),
              (assign, ":quest_gold_reward", 500),
              (assign, ":quest_xp_reward", 500),
              (assign, ":quest_expiration_days", 20),
              (assign, ":quest_dont_give_again_period", 30),
          ##diplomacy start+
              (try_begin),
              #don't give full quest reward if outside the normal level range
                 (ge, ":player_level", 15),
                 (store_sub, ":quest_xp_award", ":player_level", 14),
                 (val_mul, ":quest_xp_award", -10),
                 (val_add, ":quest_xp_award", 500),
                 (val_max, ":quest_xp_award", 100),#XP drops by 10 per level over limit, until level 40
                 #To avoid being pestered with trivia, increase :quest_dont_give_again_period with the player's level
                 (store_add, ":quest_dont_give_again_period", ":player_level", 16),
              (try_end),
              ##diplomacy end+
              (assign, ":result", ":quest_no"),
            (else_try),
              (eq, ":quest_no", "qst_deal_with_night_bandits"),
                  ##diplomacy start+
                  #re-enable quest at all levels for variety
              #(is_between, ":player_level", 0, 15),
                  ##diplomacy end+
              (is_between, ":giver_center_no", centers_begin, centers_end),
              (party_slot_ge, ":giver_center_no", slot_center_has_bandits, 1),
              (assign, ":quest_target_center", ":giver_center_no"),
              (assign, ":quest_expiration_days", 4),
              (assign, ":quest_dont_give_again_period", 15),
              ##diplomacy start+
              (try_begin),
               #To avoid being pestered with trivia, increase :quest_dont_give_again_period with the player's level
                 (ge, ":player_level", 15),
                 (store_add, ":quest_dont_give_again_period", ":player_level", 1),
              (try_end),
              ##diplomacy end+
              (assign, ":result", ":quest_no"),
            (else_try),
              # Lady quests
              (eq, ":quest_no", "qst_rescue_lord_by_replace"),
              #(eq, 1, 0), dckplmc test
              (try_begin),
                (ge, "$g_talk_troop_faction_relation", 0),
                    ##diplomacy start+
                    #if this quest is not disabled, remove the upper level limit to increase play variety
                #(is_between, ":player_level", 5, 25),
                    (ge, ":player_level", 5),
                    ##diplomacy end+

                (assign, ":prisoner_relative", -1),

                (try_begin),
                  (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_father), #get giver_troop's father
                  (gt, ":cur_target_troop", 0), #if giver_troop has a father as a troop in game
                  (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0), #if giver_troop's father is in a prison
                  (assign, ":prisoner_relative", ":cur_target_troop"),
                (try_end),

                (try_begin),
                  (eq, ":prisoner_relative", -1), #if giver_troop has no father or giver_troop's father is not in prison.
                  (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_spouse), #get giver_troop's spouse
                  (gt, ":cur_target_troop", 0), #if giver_troop has a spouse as a troop in game
                  (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0), #if giver_troop's spouse is in a prison
                  (assign, ":prisoner_relative", ":cur_target_troop"),
                (try_end),

                (try_begin),
                  (eq, ":prisoner_relative", -1), #if ((giver_troop has no father) or (giver_troop's father is not in prison)) and ((giver_troop has no spouse) or (giver_troop's spouse is not in prison)).
                  (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_guardian), #get giver_troop's spouse
                  (gt, ":cur_target_troop", 0), #if giver_troop has a guardian as a troop in game
                  (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0), #if giver_troop's guardian is in a prison
                  (assign, ":prisoner_relative", ":cur_target_troop"),
                (try_end),

                (try_begin),
                  (eq, "$cheat_mode", 1),
                  (assign, reg0, ":prisoner_relative"),
                  (display_message, "str_prisoner_relative_is_reg0"),
                (try_end),

                (gt, ":prisoner_relative", -1),
                #(changed 2) no need to this anymore (troop_slot_ge, ":prisoner_relative", slot_troop_prisoner_of_party, 0),
                (call_script, "script_search_troop_prisoner_of_party", ":prisoner_relative"),
                (assign, ":cur_target_center", reg0),

                #(changed 3) no need to check only towns anymore (is_between, ":cur_target_center", towns_begin, towns_end),#Skip if he is not in a town
                (is_between, ":cur_target_center", walled_centers_begin, walled_centers_end), #Skip if he is not in a walled center

                (assign, ":quest_target_center", ":cur_target_center"),
                (assign, ":quest_target_troop", ":prisoner_relative"),
                (assign, ":quest_expiration_days", 30),
                (assign, ":quest_dont_give_again_period", 73),
                (assign, ":result", ":quest_no"),
              (try_end),
            (else_try),
	          (eq, ":quest_no", "qst_deliver_message_to_prisoner_lord"),

			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member
			  ##...or from a faction leader, a faction marshall, or your spouse
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
				##diplomacy start+
				#Remove the upper level limit to increase play variety
	            #(is_between, ":player_level", 5, 25),
				(ge, ":player_level", 5),
				##diplomacy end+
	            (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_father),
	            (try_begin),
	              (eq, ":cur_target_troop", 0),
	              (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_spouse),
	            (try_end),
	            #(troop_slot_eq, ":cur_target_troop", slot_troop_is_prisoner, 1),#Skip if the lady's father/husband is not in prison
				(gt, ":cur_target_troop", -1),
	            (troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0),
	            (call_script, "script_search_troop_prisoner_of_party", ":cur_target_troop"),
	            (assign, ":cur_target_center", reg0),
	            (is_between, ":cur_target_center", towns_begin, towns_end),#Skip if he is not in a town
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 30),
	            (assign, ":result", ":quest_no"),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_duel_for_lady"),

	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (ge, ":player_level", 10),

                (troop_get_slot, ":giver_husband", ":giver_troop", slot_troop_spouse), #dckplmc - lady has no enemies
	            #(call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", ":giver_troop", slto_kingdom_hero),#Can fail
	            (call_script, "script_cf_troop_get_random_enemy_troop_with_occupation", ":giver_husband", slto_kingdom_hero),#Can fail
	            (assign, ":cur_target_troop", reg0),

	            (neg|troop_slot_eq, ":giver_troop", slot_troop_spouse, ":cur_target_troop"), #must not be in the family
	            (neg|troop_slot_eq, ":giver_troop", slot_troop_father, ":cur_target_troop"),
	            (neg|troop_slot_ge, ":cur_target_troop", slot_troop_prisoner_of_party, 0),
	            (troop_slot_ge, ":cur_target_troop", slot_troop_leaded_party, 0),

                ##diplomacy start+ add benefactor ~ goodnatured/upstanding equivalence
                (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_benefactor),
                #also disable challenging conventional & moralist ladies
                (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_conventional),
                (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_moralist),
                #diplomacy end+
	            (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_goodnatured),
	            (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_upstanding),
	            (neg|troop_slot_eq, ":cur_target_troop", slot_lord_reputation_type, lrep_martial),

	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 50),
	            (assign, ":result", ":quest_no"),
	          (try_end),
	          # Enemy Lord Quests
	        (else_try),
              (eq, ":quest_no", "qst_lend_surgeon"),
              (try_begin),
                (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
                ##diplomacy start+
                #also disable for roguish lords with negative tmt_humanitarian ratings
                (call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
                (this_or_next|neq, ":giver_reputation", lrep_roguish),
                    (lt, reg0, 0),
            #Disable for anyone with a negative tmt_egalitarian rating, as this would be out of character.
                (call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_egalitarian),
                (ge, reg0, 0),
                ##diplomacy end+
                (neq, ":giver_reputation", lrep_quarrelsome),
                (neq, ":giver_reputation", lrep_debauched),
                (assign, ":max_surgery_level", 0),
                (assign, ":best_surgeon", -1),
                (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
                (try_for_range, ":i_stack", 1, ":num_stacks"),
                  (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
                  (troop_is_hero, ":stack_troop"),
                  #SB : has to be companion, otherwise pretender/wife gets called
                  (is_between, ":stack_troop", companions_begin, companions_end),
                  (store_skill_level, ":cur_surgery_skill", skl_surgery, ":stack_troop"),
                  (gt, ":cur_surgery_skill", ":max_surgery_level"),
                  (assign, ":max_surgery_level", ":cur_surgery_skill"),
                  (assign, ":best_surgeon", ":stack_troop"),
                (try_end),

                (store_character_level, ":cur_level", "trp_player"),
                (assign, ":required_skill", 5),
                (val_div, ":cur_level", 10),
                (val_add, ":required_skill", ":cur_level"),
                (ge, ":max_surgery_level", ":required_skill"), #Skip if party skill level is less than the required value

                (assign, ":quest_object_troop", ":best_surgeon"),
                (assign, ":quest_importance", 1),
                #SB : this seems extremely low for cost of surgery, give at least 50 gold
                (store_mul, ":quest_xp_reward", ":max_surgery_level", 10), #slightly better
                (assign, ":quest_gold_reward", ":quest_xp_reward"),
                (assign, ":quest_dont_give_again_period", 50),
                (assign, ":result", ":quest_no"),
              (try_end),
              # Lord Quests
            (else_try),
	          (eq, ":quest_no", "qst_meet_spy_in_enemy_town"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member
			  #...or from a faction leader, a faction marshall, or your spouse
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
	            (eq, "$players_kingdom", ":giver_faction_no"),
	            (neq, ":giver_reputation", lrep_goodnatured),
	            (neq, ":giver_reputation", lrep_martial),

	            (call_script, "script_troop_get_player_relation", ":giver_troop"),
	            (assign, ":giver_relation", reg0),
	            (gt, ":giver_relation", 3),
	            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
	            (assign, ":enemy_faction", reg0),
	            (store_relation, ":reln", ":enemy_faction", "fac_player_supporters_faction"),
	            (lt, ":reln", 0),
	            (call_script, "script_cf_select_random_town_with_faction", ":enemy_faction"),
	            (assign, ":cur_target_center", reg0),
	            #Just to make sure that there is a free walker
	            (call_script, "script_cf_center_get_free_walker", ":cur_target_center"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (store_random_in_range, ":quest_target_amount", secret_signs_begin, secret_signs_end),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_gold_reward", 500),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 50),
	            (quest_set_slot, "qst_meet_spy_in_enemy_town", slot_quest_gold_reward, 500),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_raid_caravan_to_start_war"),
			  (eq, 1, 0), #disable this as a random quest

	          (try_begin),
	            (eq, "$players_kingdom", ":giver_faction_no"),
                ##diplomacy start+
				#no lords who are opposed to raiding will suggest this, even if they match
				#one of the listed personalities.
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
				(lt, reg0, 1),
				#roguish lords can give this quest unless they're opposed to raiding
	            (this_or_next|eq, ":giver_reputation", lrep_roguish),
                ##diplomacy end+
	            (this_or_next|eq, ":giver_reputation", lrep_cunning),
	            (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
	            (             eq, ":giver_reputation", lrep_debauched),
	            (gt, ":player_level", 10),
				(eq, 1, 0), #disable this as a random quest

	            (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
	            (call_script, "script_cf_faction_get_random_friendly_faction", ":giver_faction_no"),#Can fail
	            (assign, ":quest_target_faction", reg0),
	            (store_troop_faction, ":quest_object_faction", ":giver_troop"),
	            (assign, ":quest_target_party_template", "pt_kingdom_caravan_party"),
	            (assign, ":quest_target_amount", 2),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 100),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_deliver_message"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member
			  #...or from a faction leader, a faction marshall, or your spouse
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
				##diplomacy start+
				#increase the level/renown range validity of this quest
	            #(lt, ":player_level", 20),
			    #(neg|troop_slot_ge, "trp_player", slot_troop_renown, 125),
				(store_character_level, reg0, ":giver_troop"),
				(val_max, reg0, 20),#20 or quest-giver's level, whichever is greater
				(lt, ":player_level", reg0),
				(troop_get_slot, reg0, ":giver_troop", slot_troop_renown),
				(val_div, reg0, 2),
				(val_max, reg0, 125),#125 or 50% of quest-giver's renown, whichever is greater
				##diplomacy end+
	            (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
	            (assign, ":cur_target_troop", reg0),
	            (neq, ":cur_target_troop", ":giver_troop"),#Skip himself
	            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
	            (assign, ":cur_target_center", reg0),#cur_target_center will definitely be a valid center
	            (neq,":giver_center_no", ":cur_target_center"),#Skip current center

	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_xp_reward", 30),
	            (assign, ":quest_gold_reward", 40),
	            (assign, ":quest_dont_give_again_period", 10),
				##diplomacy start+
				(try_begin),
					(this_or_next|troop_slot_ge, "trp_player", slot_troop_renown, 125),
						(ge, ":player_level", 20),
					(assign, ":quest_dont_give_again_period", ":player_level"),
					(val_clamp, ":quest_dont_give_again_period", 10, 61),
				(try_end),
				##diplomacy end+

	            (assign, ":result", ":quest_no"),

	            (assign, ":quest_expiration_days", 30),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_escort_lady"),
	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (ge, ":player_level", 10),

				(ge, ":giver_troop", 0), #skip troops without fathers in range

				(assign, ":cur_object_troop", -1),
                (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
				  (troop_slot_eq, ":lady", slot_troop_father, ":giver_troop"),
				  (assign, ":cur_object_troop", ":lady"),
				(try_end),

				(ge, ":cur_object_troop", 0),

				(troop_get_slot, ":giver_troop_confirm", ":cur_object_troop", slot_troop_father),  # just to make sure
				(eq, ":giver_troop", ":giver_troop_confirm"), # just to make sure

	            (store_random_in_range, ":random_no", 0, 2),
	            (try_begin),
	              (eq, ":random_no", 0),
	              (troop_get_slot, ":cur_object_troop_2", ":giver_troop", slot_troop_spouse),
				  (is_between, ":cur_object_troop_2", kingdom_ladies_begin, kingdom_ladies_end),
				  (troop_get_slot, ":giver_troop_confirm", ":cur_object_troop_2", slot_troop_spouse),  # just to make sure
				  (eq, ":giver_troop", ":giver_troop_confirm"), # just to make sure
	              (assign, ":cur_object_troop", ":cur_object_troop_2"),
	            (try_end),
	            (gt, ":cur_object_troop", 0),#Skip lords without a lady
				##diplomacy start+ use a script for gender
	            #(troop_get_type, ":cur_troop_gender", ":cur_object_troop"),
				(call_script, "script_dplmc_store_troop_is_female", ":cur_object_troop"),
				(assign, ":cur_troop_gender", reg0),
	            #(eq, ":cur_troop_gender", 1),#Skip if it is not female
				(neq, ":cur_troop_gender", 0),
				##diplomacy end+
	            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
	            (troop_slot_eq, ":cur_object_troop", slot_troop_cur_center, ":giver_center_no"),#Skip if the lady is not at the same center
	            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
	            (assign, ":cur_target_center", reg0),
	            (neq, ":cur_target_center", ":giver_center_no"),
	            (hero_can_join),#Skip if player has no available slots

	            (assign, ":quest_object_troop", ":cur_object_troop"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":quest_expiration_days", 20),
	            (assign, ":quest_dont_give_again_period", 30),
	            (assign, ":result", ":quest_no"),
	          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_hunt_down_raiders"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
##            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_object_center", reg0),
##            (neq, ":cur_object_center", ":giver_center_no"),#Skip current center
##            (call_script, "script_get_random_enemy_center", ":giver_party_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (is_between,  ":cur_target_faction", kingdoms_begin, kingdoms_end),
##
##            (assign, ":quest_object_center", ":cur_object_center"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 1500),
##            (assign, ":quest_gold_reward", 1000),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_back_deserters"),
##          (try_begin),
##            (gt, ":player_level", 5),
##            (faction_get_slot, ":cur_target_party_template", ":giver_faction_no", slot_faction_deserter_party_template),
##            (faction_get_slot, ":cur_target_troop", ":giver_faction_no", slot_faction_deserter_troop),
##            (gt, ":cur_target_party_template", 0),#Skip factions with no deserter party templates
##            (store_num_parties_of_template, ":num_deserters", ":cur_target_party_template"),
##            (ge, ":num_deserters", 2),#Skip if there are less than 2 active deserter parties
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_target_amount", 5),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_deliver_supply_to_center_under_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
##            (call_script, "script_cf_get_random_siege_location_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":quest_target_center", reg0),
##            (assign, ":quest_target_amount", 10),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 500),
##            (assign, ":quest_gold_reward", 300),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_rescue_lady_under_siege"),
##          (try_begin),
##            (gt, ":player_level", 15),
##            (troop_get_slot, ":cur_object_troop", ":giver_troop", slot_troop_daughter),
##            (store_random_in_range, ":random_no", 0, 2),
##            (try_begin),
##              (this_or_next|eq,  ":cur_object_troop", 0),
##              (eq, ":random_no", 0),
##              (troop_get_slot, ":cur_object_troop_2", ":giver_troop", slot_troop_spouse),
##              (gt, ":cur_object_troop_2", 0),
##              (assign, ":cur_object_troop", ":cur_object_troop_2"),
##            (try_end),
##            (gt, ":cur_object_troop", 0),#Skip lords without a lady
##            (troop_get_type, ":cur_troop_gender", ":cur_object_troop"),
##            (eq, ":cur_troop_gender", 1),#Skip if lady is not female
##            (troop_get_slot, ":cur_target_center", ":cur_object_troop", slot_troop_cur_center),
##            (is_between, ":cur_target_center", centers_begin, centers_end),#Skip if she is not in a center
##            (neq,":giver_center_no", ":cur_target_center"),#Skip current center
##            (call_script, "script_cf_get_random_siege_location_with_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_target_center", reg0),
##            (troop_set_slot, ":cur_object_troop", slot_troop_cur_center, ":cur_target_center"),#Move lady to the siege location
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_target_troop", ":giver_troop"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 200),
##            (assign, ":quest_gold_reward", 750),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_deliver_message_to_lover"),
##          (try_begin),
##            (is_between, ":player_level", 5, 30),
##            (troop_get_slot, ":cur_target_troop", ":giver_troop", slot_troop_lover),
##            (gt, ":cur_target_troop", 0),#Skip lords without a lover
##            (troop_get_slot, ":cur_target_center", ":cur_target_troop", slot_troop_cur_center),
##            (is_between, ":cur_target_center", centers_begin, centers_end),#Skip if she is not in a center
##            (neq,":giver_center_no", ":cur_target_center"),#Skip current center
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":result", ":quest_no"),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_reinforcements_to_siege"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (call_script, "script_cf_get_random_siege_location_with_attacker_faction", ":giver_faction_no"),#Can fail
##            (assign, ":cur_target_center", reg0),
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_cf_get_number_of_random_troops_from_party", ":giver_party_no", ":random_no"),#Can fail
##            (assign, ":cur_object_troop", reg0),
##            (party_get_battle_opponent, ":cur_target_party", ":cur_target_center"),
##            (party_get_num_companion_stacks, ":num_stacks", ":cur_target_party"),
##            (gt, ":num_stacks", 0),#Skip if the besieger party has no troops
##            (party_stack_get_troop_id, ":cur_target_troop", ":cur_target_party", 0),
##            (troop_is_hero, ":cur_target_troop"),#Skip if the besieger party has no heroes
##            (neq, ":cur_target_troop", ":giver_troop"),#Skip if the quest giver is the same troop
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_party", ":cur_target_party"),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 400),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_deliver_message_to_enemy_lord"),
	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
				##diplomacy start+
				#remove upper level limit to increase play variety
	            #(is_between, ":player_level", 5,25),
				(ge, ":player_level", 5),
				##diplomacy end+
	            (call_script, "script_cf_get_random_lord_from_another_faction_in_a_center", ":giver_faction_no"),#Can fail
	            (assign, ":cur_target_troop", reg0),
	            (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
	            (assign, ":quest_target_center", reg0),#quest_target_center will definitely be a valid center
	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_importance", 1),
	            (assign, ":quest_xp_reward", 200),
				##diplomacy start+
				#decrease XP reward as you exceed the maximum level
				(try_begin),
					(ge, ":player_level", 26),
					(store_sub, ":quest_xp_reward", 25, ":player_level"),
					(val_add, ":quest_xp_reward", 200),
					(val_max, ":quest_xp_reward", 50),#minus 10 xp for every level above 25, to a minimum of 50 XP at level 40
				(try_end),
				##diplomacy end+
	            (assign, ":quest_gold_reward", 0),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 40),
	          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_bring_prisoners_to_enemy"),
##          (try_begin),
##            (gt, ":player_level", 10),
##            (is_between, ":giver_center_no", centers_begin, centers_end),#Skip if the quest giver is not at a center
##            (store_random_in_range, ":random_no", 5, 11),
##            (troops_can_join_as_prisoner, ":random_no"),#Skip if the player doesn't have enough room
##            (call_script, "script_get_random_enemy_town", ":giver_center_no"),
##            (assign, ":cur_target_center", reg0),
##            (ge, ":cur_target_center", 0),#Skip if there are no enemy towns
##            (store_faction_of_party, ":cur_target_faction", ":cur_target_center"),
##            (faction_get_slot, ":cur_object_troop", ":cur_target_faction", slot_faction_tier_5_troop),
##            (assign, ":quest_target_center", ":cur_target_center"),
##            (assign, ":quest_object_troop", ":cur_object_troop"),
##            (assign, ":quest_target_amount", ":random_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 300),
##            (assign, ":quest_gold_reward", 200),
##            (assign, ":result", ":quest_no"),
##          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_deal_with_bandits_at_lords_village"),
	          (try_begin),
			    ##diplomacy start+
				#Does not have negative "tmt_humanitarian" rating
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
				(ge, reg0, 0),
				##diplomacy end+
	            (neq, ":giver_reputation", lrep_debauched),
	            (neq, ":giver_reputation", lrep_quarrelsome),
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (assign, ":end_cond", villages_end),
	            (assign, ":cur_target_center", -1),
	            (try_for_range, ":cur_village", villages_begin, ":end_cond"),
	              (party_slot_eq, ":cur_village", slot_town_lord, ":giver_troop"),
                  #SB : fix this to ge
	              (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
	              (party_slot_eq, ":cur_village", slot_village_state, svs_normal),
	              (assign, ":cur_target_center", ":cur_village"),
	              (assign, ":end_cond", 0),
	            (try_end),
	            (ge, ":cur_target_center", 0),
	            (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 30),
                #SB : do quest rewards here instead of upon completion
                (store_character_level, ":quest_gold_reward", "trp_player"),
                (val_mul, ":quest_gold_reward", 20),
                (val_add, ":quest_gold_reward", 300),
                (assign, ":quest_xp_reward", 350),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_raise_troops"),
	          (try_begin),
	            (neq, ":giver_reputation", lrep_martial),
				##diplomacy start+
				#RE-ENABLE for player's faction
	            #(neq, ":giver_faction_no", "fac_player_supporters_faction"), #we need tier_1_troop a valid value
				(assign, ":faction_for_troop", ":giver_faction_no"),
				(try_begin),
					(eq, ":giver_faction_no", "fac_player_supporters_faction"),
					(assign, ":faction_for_troop", "$g_player_culture"),
					(neg|is_between, ":faction_for_troop", npc_kingdoms_begin, npc_kingdoms_end),
					(troop_get_slot, ":faction_for_troop", ":giver_troop", slot_troop_original_faction),
				(try_end),
				(is_between, ":faction_for_troop", npc_kingdoms_begin, npc_kingdoms_end), #we need tier_1_troop a valid value
				##diplomacy end+
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (store_character_level, ":cur_level", "trp_player"),
	            (gt, ":cur_level", 5),
	            (troop_slot_ge, "trp_player", slot_troop_renown, 100),

	            (store_random_in_range, ":quest_target_amount", 5, 8),
	            (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
	            (le, ":quest_target_amount", ":free_capacity"),
	            (faction_get_slot, ":quest_object_troop", ":giver_faction_no", slot_faction_tier_1_troop),
	            (store_random_in_range, ":level_up", 20, 40),
	            (val_add, ":level_up", ":cur_level"),
	            (val_div, ":level_up", 10),

	            (store_mul, ":quest_gold_reward", ":quest_target_amount", 10),

	            (assign, ":quest_target_troop", ":quest_object_troop"),

	            (try_for_range, ":unused", 0, ":level_up"),
	              (troop_get_upgrade_troop, ":level_up_troop", ":quest_target_troop", 0),
	              (gt, ":level_up_troop", 0),
	              (assign, ":quest_target_troop", ":level_up_troop"),
				  ##diplomacy start+ Fix what appears to be a native bug,
	              #(val_mul, ":quest_gold_reward", ":quest_gold_reward", 7),
	              #(val_div, ":quest_gold_reward", ":quest_gold_reward", 4),
				  (val_mul, ":quest_gold_reward", 7),
				  (val_div, ":quest_gold_reward", 4),
				  ##diplomacy end+
	            (try_end),

	            (assign, ":quest_xp_reward", ":quest_gold_reward"),
	            (val_mul, ":quest_xp_reward", 3),
	            (val_div, ":quest_xp_reward", 10),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 120),
	            (assign, ":quest_dont_give_again_period", 15),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_collect_taxes"),
			  ##diplomacy start+ enable this quest even when a vassal,
   			  #if the quest giver is an affiliated family member
			  #...or from the faction leader, the faction marshall, or your spouse
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
                ##diplomacy start+ benefactor lords do not give tax-collection quest because good-natured/upstanding do not
	            (neq, ":giver_reputation", lrep_benefactor),
				#neither do certain lady personalities either (only ambitious do)
				(neg|is_between, ":giver_reputation", lrep_conventional, lrep_ambitious),
				(neq, ":giver_reputation", lrep_moralist),
                ##diplomacy end+
	            (neq, ":giver_reputation", lrep_goodnatured),
	            (neq, ":giver_reputation", lrep_upstanding),
	            (ge, "$g_talk_troop_faction_relation", 0),
				#SB : we've modified this script call with additional parameter
	            (call_script, "script_cf_troop_get_random_leaded_town_or_village_except_center", ":giver_troop", ":giver_center_no", svs_normal),
	            (assign, ":quest_target_center", reg0),
	            (assign, ":quest_importance", 1),
	            (assign, ":quest_gold_reward", 0),
	            (assign, ":quest_xp_reward", 100),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 50),
	            (assign, ":quest_dont_give_again_period", 20),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_hunt_down_fugitive"),
	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
                #SB : change conditions to prevent selecting a village that's being raided or infested by bandits
                ## although at higher levels we can make it so that the "kinsmen" are bandits
                (assign, ":cur_target_center", -1),
	            (try_for_range, ":unused_2", 0, 10),
	              (call_script, "script_cf_select_random_village_with_faction", ":giver_faction_no"),
                  (call_script, "script_cf_village_normal_cond", reg0),
                  (assign, ":cur_target_center", reg0),
	            (try_end),
                (neq, ":cur_target_center", -1),
	            # (call_script, "script_cf_select_random_village_with_faction", ":giver_faction_no"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (store_random_in_range, ":quest_target_dna", 0, 1000000),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 30),
	          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_messenger"),
##          (try_begin),
##            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),
##            (assign, ":cur_target_faction", reg0),
##            (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_messenger_troop),
##            (gt, ":cur_target_troop", 0),#Checking the validiy of cur_target_troop
##            (store_num_parties_destroyed_by_player, ":quest_target_amount", "pt_messenger_party"),
##
##            (assign, ":quest_target_troop", ":cur_target_troop"),
##            (assign, ":quest_target_party_template", ":cur_target_party_template"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 700),
##            (assign, ":quest_gold_reward", 400),
##            (assign, ":result", ":quest_no"),
##          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_kill_local_merchant"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member or your spouse
			  (this_or_next|ge, ":is_close", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
                ##diplomacy start+
				#Lords who dislike breaking deals do not give this quest
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_honest),
				(lt, reg0, 1),
				#Roguish lords can give the Kill Local Merchant quest, unless they dislike murder.
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
	            (this_or_next|neq, ":giver_reputation", lrep_roguish),
					(lt, reg0, 1),
				#Ambitious ladies can give this quest
				(this_or_next|eq, ":giver_reputation", lrep_ambitious),
				(this_or_next|eq, ":giver_reputation", lrep_roguish),
                ##diplomacy end+
	            (this_or_next|eq, ":giver_reputation", lrep_quarrelsome),
	            (this_or_next|eq, ":giver_reputation", lrep_cunning),
	            (             eq, ":giver_reputation", lrep_debauched),
	            (neg|faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),#Can not take the quest from the king
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (gt, ":player_level", 5),
	            (is_between, ":giver_center_no", towns_begin, towns_end),
	            (assign, ":quest_importance", 1),
	            (assign, ":quest_xp_reward", 300),
	            (assign, ":quest_gold_reward", 1000),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 10),
	            (assign, ":quest_dont_give_again_period", 30),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_bring_back_runaway_serfs"),
	          (try_begin),
                ##diplomacy start+
				#companions who have compassion for commoners do not give the Runaway Serfs quest
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
				(lt, reg0, 1),
				#neither do Benefactor lords
	            (neq, ":giver_reputation", lrep_benefactor),
				#neither do most lady personalities (only ambitious do)
				(neg|is_between, ":giver_reputation", lrep_conventional, lrep_ambitious),
				(neq, ":giver_reputation", lrep_moralist),
                ##diplomacy end+
	            (neq, ":giver_reputation", lrep_goodnatured),
	            (neq, ":giver_reputation", lrep_upstanding),
	            (ge, "$g_talk_troop_faction_relation", 0),
	            (ge, ":player_level", 5),
	            (gt, ":giver_center_no", 0),#Skip if lord is outside the center
	            (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)

	            (assign, ":cur_object_center", -1),
	            (try_for_range, ":cur_village", villages_begin, villages_end),
	              (party_slot_eq, ":cur_village", slot_town_lord, ":giver_troop"),
	              (store_distance_to_party_from_party, ":dist", ":cur_village", ":giver_center_no"),
	              (lt, ":dist", 25),
	              (assign, ":cur_object_center", ":cur_village"),
	            (try_end),
	            (ge, ":cur_object_center", 0),#Skip if the quest giver is not the owner of any villages around the center
	            (call_script, "script_cf_select_random_town_with_faction", ":giver_faction_no"),
	            (assign, ":cur_target_center", reg0),
	            (neq, ":cur_target_center", ":giver_center_no"),#Skip current center
	            (store_distance_to_party_from_party, ":dist", ":cur_target_center", ":giver_center_no"),
	            (ge, ":dist", 20),
	            (assign, ":quest_target_party_template", "pt_runaway_serfs"),
	            (assign, ":quest_object_center", ":cur_object_center"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":quest_importance", 1),
	            (assign, ":quest_xp_reward", 200),
	            (assign, ":quest_gold_reward", 150),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 20),
	            (assign, "$qst_bring_back_runaway_serfs_num_parties_returned", 0),
	            (assign, "$qst_bring_back_runaway_serfs_num_parties_fleed", 0),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_follow_spy"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member or your spouse
			  #or a nominal superior
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
				##diplomacy start+
				#Ladies other than the ambitious do not give this quest
                                (this_or_next|lt, reg0, 0),
				(this_or_next|eq, ":giver_reputation", lrep_ambitious),
                                (neg|is_between, ":giver_reputation", lrep_conventional, lrep_moralist + 1),
                                #As the "success" dialogue refers to torture, humanitarians do not either
                                (call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
                                (lt, reg0, 1),
                                #This is more open to interpretation, but I will also bar custodians from
										  #this, unless they have a negative tmt_humanitarian score.
                                (this_or_next|lt, reg0, 0),
                                   (neq, ":giver_reputation", lrep_custodian),
                                (neq, ":giver_reputation", lrep_benefactor),
				##diplomacy end+
	            (neq, ":giver_reputation", lrep_goodnatured),
	            (party_get_skill_level, ":tracking_skill", "p_main_party", "skl_tracking"),
	            (ge, ":tracking_skill", 2),
	            (ge, ":player_level", 10),
	            (eq, "$g_defending_against_siege", 0), #Skip if the center is under siege (because of resting)
	            (gt, ":giver_party_no", 0), #Skip if the quest giver doesn't have a party
	            (gt, ":giver_center_no", 0), #skip if the quest giver is not in a center
	            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #skip if we are not in a town.
	            (party_get_position, pos2, "p_main_party"),
	            (assign, ":min_distance", 99999),
                    (assign, ":cur_object_center", -1),
	            (try_for_range, ":unused_2", 0, 10),
	              (call_script, "script_cf_get_random_enemy_center", ":giver_party_no"),
	              (assign, ":random_object_center", reg0),
	              (party_get_position, pos3, ":random_object_center"),
	              (map_get_random_position_around_position, pos4, pos3, 6),
	              (get_distance_between_positions, ":cur_distance", pos2, pos4),
	              (lt, ":cur_distance", ":min_distance"),
	              (assign, ":min_distance", ":cur_distance"),
	              (assign, ":cur_object_center", ":random_object_center"),
	              (copy_position, pos63, pos4), #Do not change pos63 until quest is accepted
	            (try_end),
	            (gt, ":cur_object_center", 0), #Skip if there are no enemy centers

	            (assign, ":quest_object_center", ":cur_object_center"),
	            (assign, ":quest_dont_give_again_period", 50),
	            (assign, ":result", ":quest_no"),
	            (assign, "$qst_follow_spy_run_away", 0),
	            (assign, "$qst_follow_spy_meeting_state", 0),
	            (assign, "$qst_follow_spy_meeting_counter", 0),
	            (assign, "$qst_follow_spy_spy_back_in_town", 0),
	            (assign, "$qst_follow_spy_partner_back_in_town", 0),
	            (assign, "$qst_follow_spy_no_active_parties", 0),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_capture_enemy_hero"),
	          (try_begin),
	            (eq, "$players_kingdom", ":giver_faction_no"),
				##diplomacy start+
				(this_or_next|ge, ":is_close", 1),
			    (this_or_next|ge, ":nominal_superior", 1),
				##diplomacy end+
	            (neg|faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
	            (ge, ":player_level", 15),
	            (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
	            (assign, ":quest_target_faction", reg0),
	            (assign, ":quest_expiration_days", 30),
                ##diplomacy start+ change from 80 to 30
	            (assign, ":quest_dont_give_again_period", 30),#was 80
                ##diplomacy end+
	            (assign, ":quest_gold_reward", 2000),
	            (assign, ":result", ":quest_no"),
	          (try_end),
            (else_try),
              (eq, ":quest_no", "qst_lend_companion"),
              (try_begin),
                (ge, "$g_talk_troop_faction_relation", 0),
                (assign, ":total_heroes", 0),
                (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
                #SB : pre-process
                (try_for_range, ":troop_no", companions_begin, companions_end),
                  (troop_set_slot, ":troop_no", dplmc_slot_troop_temp_slot, 0),
                (try_end),
                (try_for_range, ":i_stack", 0, ":num_stacks"),
                  (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
                  (troop_is_hero, ":stack_troop"),
                  (is_between, ":stack_troop", companions_begin, companions_end),
                  (store_character_level, ":stack_level", ":stack_troop"),
                  (ge, ":stack_level", 15),
                  (assign, ":is_quest_hero", 0),
                  (try_for_range, ":i_quest", 0, all_quests_end),
                    (check_quest_active, ":i_quest"),
                    (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                    (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                    (assign, ":is_quest_hero", 1),
                  (try_end),
                  (eq, ":is_quest_hero", 0),
                  (val_add, ":total_heroes", 1),
                  (troop_set_slot, ":stack_troop", dplmc_slot_troop_temp_slot, 1), #SB : set flag here
                (try_end),
                (gt, ":total_heroes", 0),#Skip if party has no eligible heroes
                (store_random_in_range, ":random_hero", 0, ":total_heroes"),
                (assign, ":total_heroes", 0),
                (assign, ":cur_target_troop", -1),
                (try_for_range, ":stack_troop", companions_begin, companions_end),
                  (eq, ":cur_target_troop", -1),
                  # (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
                  # (troop_is_hero, ":stack_troop"),
                  # (is_between, ":stack_troop", companions_begin, companions_end),
                  # # (neq, ":stack_troop", "trp_player"), #SB : useless check
                  # (store_character_level, ":stack_level", ":stack_troop"),
                  # (ge, ":stack_level", 15),
                  # (assign, ":is_quest_hero", 0),
                  # (try_for_range, ":i_quest", 0, all_quests_end),
                    # (check_quest_active, ":i_quest"),
                    # (this_or_next|quest_slot_eq, ":i_quest", slot_quest_target_troop, ":stack_troop"),
                    # (quest_slot_eq, ":i_quest", slot_quest_object_troop, ":stack_troop"),
                    # (assign, ":is_quest_hero", 1),
                  # (try_end),
                  # (eq, ":is_quest_hero", 0),
                  #SB : check flag here
                  (troop_slot_eq, ":stack_troop", dplmc_slot_troop_temp_slot, 1),
                  (val_add, ":total_heroes", 1),
                  (gt, ":total_heroes", ":random_hero"),
                  (assign, ":cur_target_troop", ":stack_troop"),
                (try_end),
                (is_between, ":cur_target_troop", companions_begin, companions_end),

                (assign, ":quest_target_troop", ":cur_target_troop"),
                (store_current_day, ":quest_target_amount"),
                (val_add, ":quest_target_amount", 8),

                (assign, ":quest_importance", 1),
                #SB : scale reward by level
                (store_character_level, ":stack_level", ":quest_target_troop"),
                (store_mul, ":quest_xp_reward", ":stack_level", 20), #base level of 15
                # (assign, ":quest_xp_reward", 300),
                # (assign, ":quest_gold_reward", 400),
                (store_add, ":quest_gold_reward", ":quest_xp_reward", 100),
                (assign, ":result", ":quest_no"),
                (assign, ":quest_dont_give_again_period", 30),
              (try_end),
            (else_try),
              (eq, ":quest_no", "qst_collect_debt"),
              #(eq, 1, 0), #disable this quest pending talk with armagan
              #re-enabled, dckplmc
              (try_begin),
	            (ge, "$g_talk_troop_faction_relation", 0),
	          # Find a vassal (within the same kingdom?)
	            (call_script, "script_cf_get_random_lord_in_a_center_with_faction", ":giver_faction_no"),#Can fail
	            (assign, ":quest_target_troop", reg0),
	            (neq, ":quest_target_troop", ":giver_troop"),#Skip himself
	            (call_script, "script_get_troop_attached_party", ":quest_target_troop"),
	            (assign, ":quest_target_center", reg0),#cur_target_center will definitely be a valid center
	            (neq,":giver_center_no", ":quest_target_center"),#Skip current center

	            (assign, ":quest_xp_reward", 30),
	            (assign, ":quest_gold_reward", 40),
	            (assign, ":result", ":quest_no"),
	            (store_random_in_range, ":quest_target_amount", 6, 9),
	            (val_mul, ":quest_target_amount", 500),
	            (store_div, ":quest_convince_value", ":quest_target_amount", 5),
	            (assign, ":quest_expiration_days", 90),
	            (assign, ":quest_dont_give_again_period", 20),
	          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_capture_conspirators"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", towns_begin, towns_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##            (call_script, "script_cf_get_random_kingdom_hero", ":giver_faction_no"),#Can fail
##
##            (assign, ":quest_target_troop", reg0),
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 3),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_capture_conspirators_num_parties_to_spawn", 4, ":max_parties"),
##            (assign, "$qst_capture_conspirators_num_troops_to_capture", 0),
##            (assign, "$qst_capture_conspirators_num_parties_spawned", 0),
##            (assign, "$qst_capture_conspirators_leave_meeting_counter", 0),
##            (assign, "$qst_capture_conspirators_party_1", 0),
##            (assign, "$qst_capture_conspirators_party_2", 0),
##            (assign, "$qst_capture_conspirators_party_3", 0),
##            (assign, "$qst_capture_conspirators_party_4", 0),
##            (assign, "$qst_capture_conspirators_party_5", 0),
##            (assign, "$qst_capture_conspirators_party_6", 0),
##            (assign, "$qst_capture_conspirators_party_7", 0),
##          (try_end),
##        (else_try),
##          (eq, ":quest_no", "qst_defend_nobles_against_peasants"),
##          (try_begin),
##            (eq, 1,0), #TODO: disable this for now
##            (ge, ":player_level", 10),
##            (is_between, ":giver_center_no", towns_begin, towns_end),#Skip if quest giver's center is not a town
##            (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),#Skip if the current center is not ruled by the quest giver
##
##            (assign, ":quest_target_center", ":giver_center_no"),
##            (assign, ":quest_importance", 1),
##            (assign, ":quest_xp_reward", 10),
##            (assign, ":quest_gold_reward", 10),
##            (assign, ":result", ":quest_no"),
##            (store_character_level, ":cur_level"),
##            (val_div, ":cur_level", 5),
##            (val_max, ":cur_level", 4),
##            (store_add, ":max_parties", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_peasant_parties_to_spawn", 4, ":cur_level"),
##            (store_random_in_range, "$qst_defend_nobles_against_peasants_num_noble_parties_to_spawn", 4, ":cur_level"),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_to_save", 0),
##            (assign, "$qst_defend_nobles_against_peasants_num_nobles_saved", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_peasant_party_8", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##            (assign, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_incriminate_loyal_commander"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member
			  (this_or_next|ge, ":is_close", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
                ##diplomacy start+ benefactors & moralists will not give this quest
	            (neq, ":giver_reputation", lrep_benefactor),
	            (neq, ":giver_reputation", lrep_moralist),
				#neither will most lady personalities (only ambitious do)
				(neg|is_between, ":giver_reputation", lrep_conventional, lrep_ambitious),
				(neq, ":giver_reputation", lrep_moralist),
				#neither will lords who dislike mistreating their own men, or who
				#are forthright in their dealings
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_egalitarian),
				(lt, reg0, 1),
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_honest),
				(lt, reg0, 1),
				#neither will other lords who dislike murder
				(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
				(lt, reg0, 1),
                ##diplomacy end+
	            (neq, ":giver_reputation", lrep_upstanding),
	            (neq, ":giver_reputation", lrep_goodnatured),
	            (eq, "$players_kingdom", ":giver_faction_no"),
	            (ge, ":player_level", 10),
	            (faction_slot_eq, ":giver_faction_no", slot_faction_leader, ":giver_troop"),
	            (assign, ":try_times", 1),
	            (assign, ":found", 0),
	            (try_for_range, ":unused", 0, ":try_times"),
	              (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
	              (assign, ":cur_target_faction", reg0),

	              (faction_get_slot, ":cur_target_troop", ":cur_target_faction", slot_faction_leader),
	              (assign, ":num_centerless_heroes", 0),
	              ##diplomacy start+ add support for promoted ladies
	              (try_for_range, ":cur_kingdom_hero", heroes_begin, heroes_end),#<- changed active_npcs to heroes
	              ##diplomacy end+
	                (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
	                #(troop_slot_eq, ":cur_kingdom_hero", slot_troop_is_prisoner, 0),
	                (neg|troop_slot_ge, ":cur_kingdom_hero", slot_troop_prisoner_of_party, 0),
	                (neq, ":cur_target_troop", ":cur_kingdom_hero"),
	                (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
	                (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
##                (eq, reg0, 0),
	                (val_add, ":num_centerless_heroes", 1),
	              (try_end),
	              (gt, ":num_centerless_heroes", 0),
	              (assign, ":cur_object_troop", -1),
	              (store_random_in_range, ":random_kingdom_hero", 0, ":num_centerless_heroes"),
	              ##diplomacy start+ add support for promoted ladies
	              (try_for_range, ":cur_kingdom_hero", heroes_begin, heroes_end),#<- changed active_npcs to heroes
	              ##diplomacy end+
	                (eq, ":cur_object_troop", -1),
	                (troop_slot_eq, ":cur_kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
	                (neq, ":cur_target_troop", ":cur_kingdom_hero"),
	                (store_troop_faction, ":cur_kingdom_hero_faction", ":cur_kingdom_hero"),
	                (eq, ":cur_target_faction", ":cur_kingdom_hero_faction"),
##                (call_script, "script_get_number_of_hero_centers", ":cur_kingdom_hero"),
##                (eq, reg0, 0),
	                (val_sub, ":random_kingdom_hero", 1),
	                (lt, ":random_kingdom_hero", 0),
	                (assign, ":cur_object_troop", ":cur_kingdom_hero"),
	              (try_end),

	              (assign, ":cur_target_center", -1),
	              (call_script, "script_get_troop_attached_party", ":cur_target_troop"),
	              (is_between, reg0, towns_begin, towns_end),
	              (party_slot_eq, reg0, slot_town_lord, ":cur_target_troop"),
	              (assign, ":cur_target_center", reg0),

	              (assign, ":try_times", -1),#Exit the second loop
	              (assign, ":found", 1),
	            (try_end),
	            (eq, ":found", 1),

	            (assign, "$incriminate_quest_sacrificed_troop", 0),

	            (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
	            (try_for_range, ":i_stack", 1, ":num_stacks"),
	              (eq ,"$incriminate_quest_sacrificed_troop", 0),
	              (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
	              (neg|troop_is_hero, ":stack_troop"),
	              (store_character_level, ":stack_troop_level", ":stack_troop"),
	              (ge, ":stack_troop_level", 25), #this is "top tier"
	              (assign, "$incriminate_quest_sacrificed_troop", ":stack_troop"),
	            (try_end),
	            (gt, "$incriminate_quest_sacrificed_troop", 0),

	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_object_troop", ":cur_object_troop"),
	            (assign, ":quest_target_center", ":cur_target_center"),
	            (assign, ":quest_target_faction", ":cur_target_faction"),

	            (assign, ":quest_importance", 1),
	            (assign, ":quest_xp_reward", 700),
	            (assign, ":quest_gold_reward", 1000),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 30),
	            (assign, ":quest_dont_give_again_period", 180),
	          (try_end),
	        (else_try),
	          (eq, ":quest_no", "qst_capture_prisoners"),
			  ##diplomacy start+ enable this quest even when a vassal from an affiliated family member
			  (this_or_next|ge, ":is_close", 1),
			  (this_or_next|ge, ":nominal_superior", 1),
			  ##diplomacy end+
			  (eq, "$player_has_homage", 0),

	          (try_begin),
	            (eq, "$players_kingdom", ":giver_faction_no"),

	            # (store_add, ":max_tier_no", slot_faction_tier_5_troop, 1),
                #SB : makes sure the giver doesn't already have these as prisoners when offering
                (assign, ":cond", 20),
                (assign, ":cur_target_faction", -1),
                (assign, ":party_no", -1),
                (try_begin), #store prisoner count
                  (is_between, ":giver_center_no", walled_centers_begin, walled_centers_end),
                  (party_slot_eq, ":giver_center_no", slot_town_lord, ":giver_troop"),
                  (assign, ":party_no", ":giver_center_no"),
                (else_try), #technically we should store both, but while in center prisoners are dropped off
                  (party_is_active, ":giver_party_no"),
                  (assign, ":party_no", ":giver_party_no"),
                (try_end),
                # (gt, ":party_no", 0),
                (try_for_range, ":unused", 0, ":cond"),
	              (call_script, "script_cf_faction_get_random_enemy_faction", ":giver_faction_no"),#Can fail
	              (assign, ":cur_target_faction", reg0),
	              (store_random_in_range, ":random_tier_no", slot_faction_tier_2_troop, slot_faction_tier_5_troop + 1),
	              (faction_get_slot, ":cur_target_troop", ":cur_target_faction", ":random_tier_no"),
	              (gt, ":cur_target_troop", 0),
	              (store_random_in_range, ":quest_target_amount", 3, 7),
                  (try_begin),
                    (gt, ":party_no", 0),
                    (party_count_prisoners_of_type, ":count", ":party_no", ":cur_target_troop"),
                    (val_sub, ":quest_target_amount", ":count"),
                  (try_end),
                  (gt, ":quest_target_amount", 1), #too minor to give a quest for 1 soldier
                  (assign, ":cond", 0),
                (try_end),
                (eq, ":cond", 0),
	            (assign, ":quest_target_troop", ":cur_target_troop"),
	            (assign, ":quest_target_faction", ":cur_target_faction"),
	            (assign, ":quest_importance", 1),
	            (store_character_level, ":quest_gold_reward", ":cur_target_troop"),
	            (val_add, ":quest_gold_reward", 5),
	            (val_mul, ":quest_gold_reward", ":quest_gold_reward"),
	            (val_div, ":quest_gold_reward", 5),
	            (val_mul, ":quest_gold_reward", ":quest_target_amount"),
	            (assign, ":quest_xp_reward", ":quest_gold_reward"),
	            (assign, ":result", ":quest_no"),
	            (assign, ":quest_expiration_days", 90),
	            (assign, ":quest_dont_give_again_period", 20),
	          (try_end),
	        (try_end),
		(try_end),
	  (try_end),
	  #end of quest finding


      (try_begin),
        (neq, ":result", -1),

        (try_begin),
          (party_is_active, ":quest_target_center"),
          (store_faction_of_party, ":quest_target_faction", ":quest_target_center"),
        (try_end),

        (quest_set_slot, ":result", slot_quest_target_troop, ":quest_target_troop"),
        (quest_set_slot, ":result", slot_quest_target_center, ":quest_target_center"),
        (quest_set_slot, ":result", slot_quest_object_troop, ":quest_object_troop"),
        (quest_set_slot, ":result", slot_quest_target_faction, ":quest_target_faction"),
        (quest_set_slot, ":result", slot_quest_object_faction, ":quest_object_faction"),
        (quest_set_slot, ":result", slot_quest_object_center, ":quest_object_center"),
        (quest_set_slot, ":result", slot_quest_target_party, ":quest_target_party"),
        (quest_set_slot, ":result", slot_quest_target_party_template, ":quest_target_party_template"),
        (quest_set_slot, ":result", slot_quest_target_amount, ":quest_target_amount"),
        (quest_set_slot, ":result", slot_quest_importance, ":quest_importance"),
        (quest_set_slot, ":result", slot_quest_xp_reward, ":quest_xp_reward"),
        (quest_set_slot, ":result", slot_quest_gold_reward, ":quest_gold_reward"),
        (quest_set_slot, ":result", slot_quest_convince_value, ":quest_convince_value"),
        (quest_set_slot, ":result", slot_quest_expiration_days, ":quest_expiration_days"),
        (quest_set_slot, ":result", slot_quest_dont_give_again_period, ":quest_dont_give_again_period"),
        (quest_set_slot, ":result", slot_quest_current_state, 0),
        (quest_set_slot, ":result", slot_quest_giver_troop, ":giver_troop"),
        (quest_set_slot, ":result", slot_quest_giver_center, ":giver_center_no"),
        (quest_set_slot, ":result", slot_quest_target_dna, ":quest_target_dna"),
        (quest_set_slot, ":result", slot_quest_target_item, ":quest_target_item"),
      (try_end),

      (assign, reg0, ":result"),
  ])
]
