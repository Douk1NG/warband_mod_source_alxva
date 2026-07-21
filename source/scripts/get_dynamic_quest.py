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

get_dynamic_quest_scripts = [
("get_dynamic_quest",
  #Dynamic quests are rarer, more important quests
  #this is a separate script from get_quest, so that tavern keepers can scan all NPCs for quests
    [
    (store_script_param_1, ":giver_troop"),

	(assign, ":result", -1),
	(assign, ":relevant_troop", -1),
	(assign, ":relevant_party", -1),
	(assign, ":relevant_faction", -1),

	(try_begin),
		##diplomacy start+
		##OLD:
		#(eq, ":giver_troop", -1),
		##NEW:
		(lt, ":giver_troop", 0),
		##diplomacy end+
	(else_try),
		#1 rescue prisoner
		(neg|check_quest_active, "qst_rescue_prisoner"),
		(this_or_next|troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_lady),

		(assign, ":target_troop", -1),
		##diplomacy start+ add support for promoted ladies
		#(try_for_range, ":possible_prisoner", active_npcs_begin, active_npcs_end),
		(try_for_range, ":possible_prisoner", heroes_begin, heroes_end),
			(this_or_next|troop_slot_eq, ":possible_prisoner", slot_troop_occupation, slto_kingdom_hero),
				(is_between, ":possible_prisoner", active_npcs_begin, active_npcs_end),
		##diplomacy end+
			(troop_get_slot, ":captor_location", ":possible_prisoner", slot_troop_prisoner_of_party),
			(is_between, ":captor_location", walled_centers_begin, walled_centers_end),
			(store_troop_faction, ":giver_troop_faction_no", ":giver_troop"),
			(store_faction_of_party, ":captor_location_faction_no", ":captor_location"),
			(store_relation, ":giver_captor_relation", ":giver_troop_faction_no", ":captor_location_faction_no"),
			(lt, ":giver_captor_relation", 0),

			(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop", ":possible_prisoner"),
			##diplomacy start+
			#If optional behavior changes are enabled, allow this for more relatives.
			#(In-laws, uncles, nieces.)
		   (try_begin),
			   (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
				(ge, reg0, 4),
				(val_max, reg0, 10),
			(else_try),
			#If the characters are related to each other, and both are
			#affiliated with the player, consider them to be close enough.
				 (ge, reg0, 1),
				 (lt, reg0, 10),
				 (call_script, "script_dplmc_is_affiliated_family_member", ":giver_troop"),
				 (ge, reg0, 1),
				 (call_script, "script_dplmc_is_affiliated_family_member", ":possible_prisoner"),
				 (ge, reg0, 1),
				 (assign, reg0, 10),
			(try_end),
			##diplomacy end+
			(ge, reg0, 10),

			(assign, ":offered_parole", 0),
			(try_begin),
				(call_script, "script_cf_prisoner_offered_parole", ":possible_prisoner"),
				(assign, ":offered_parole", 1),
			(try_end),
			(eq, ":offered_parole", 0),

			(neg|party_slot_eq, ":captor_location", slot_town_lord, "trp_player"),

			(assign, ":target_troop", ":possible_prisoner"),
			(assign, ":target_party", ":captor_location"),
		(try_end),

		(gt, ":target_troop", -1),
		(assign, ":result", "qst_rescue_prisoner"),
		(assign, ":relevant_troop", ":target_troop"),
		(assign, ":relevant_party", ":target_party"),

	(else_try),
		#2 retaliate for border incident
		(is_between, ":giver_troop", mayors_begin, mayors_end),
		(store_faction_of_troop, ":giver_faction", ":giver_troop"),

		(neg|check_quest_active, "qst_retaliate_for_border_incident"),
		(quest_slot_eq, "qst_retaliate_for_border_incident", slot_quest_dont_give_again_remaining_days, 0),
		(assign, ":target_leader", 0),

		(try_for_range, ":kingdom", "fac_kingdom_1", kingdoms_end),
			(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":giver_faction", ":kingdom"),
			(assign, ":diplomatic_status", reg0),
			(eq, ":diplomatic_status", -1),
			(assign, ":duration", reg1),
			(ge, ":duration", 10),

			##diplomacy start+ add support for promoted kingdom ladies
			#(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
			(try_for_range, ":lord", heroes_begin, heroes_end),
				(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
				(store_faction_of_troop, ":lord_faction", ":lord"),
				(eq, ":lord_faction", ":kingdom"),

				(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),

				(assign, ":target_leader", ":lord"),
				(assign, ":target_faction", ":kingdom"),
			(try_end),
		(try_end),
		##diplomacy start+ add support for promoted kingdom ladies
		#(is_between, ":target_leader", active_npcs_begin, active_npcs_end),
		(is_between, ":target_leader", heroes_begin, heroes_end),
		##diplomacy end+

		(assign, ":result", "qst_retaliate_for_border_incident"),
		(assign, ":relevant_troop", ":target_leader"),
		(assign, ":relevant_faction", ":target_faction"),
	(else_try), #Find bandit hideout
		(troop_slot_eq, ":giver_troop", slot_troop_occupation, slto_kingdom_hero),
		(neg|check_quest_active, "qst_destroy_bandit_lair"),
		(quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_dont_give_again_remaining_days, 0),

#		(display_message, "@Checking for bandit lair quest"),

		(assign, ":lair_found", -1),

		(try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
			(party_template_get_slot, ":bandit_lair", ":bandit_template", slot_party_template_lair_party),

			#No party is active because bandit lairs are removed as soon as they are attacked, by the player -- but can only be removed by the player. This will reset bandit lair to zero
			(gt, ":bandit_lair", "p_spawn_points_end"),

			(assign, ":closest_town", -1),
			(assign, ":score_to_beat", 99999),

			(try_for_range, ":town_no", towns_begin, towns_end),
				(store_distance_to_party_from_party, ":distance", ":bandit_lair", ":town_no"),
				(lt, ":distance", ":score_to_beat"),
				(assign, ":closest_town", ":town_no"),
				(assign, ":score_to_beat", ":distance"),
			(try_end),

			#(str_store_party_name, s7, ":closest_town"),
			#(party_get_slot, ":closest_town_lord", ":closest_town", slot_town_lord),
			#(str_store_troop_name, s8, ":closest_town_lord"),

			(party_slot_eq, ":closest_town", slot_town_lord, ":giver_troop"),
			(assign, ":lair_found", ":bandit_lair"),
		(try_end),

		(gt, ":lair_found", "p_spawn_points_end"),

		(assign ,":result", "qst_destroy_bandit_lair"),
		(assign, ":relevant_party", ":lair_found"),
	(else_try),  #3 - bounty on bandit party
		(is_between, ":giver_troop", mayors_begin, mayors_end),
		(neg|check_quest_active, "qst_track_down_bandits"),
		(quest_slot_eq, "qst_track_down_bandits", slot_quest_dont_give_again_remaining_days, 0),

		(assign, ":cur_town", -1),
		(try_for_range, ":town", towns_begin, towns_end),
			(party_slot_eq, ":town", slot_town_elder, ":giver_troop"),
			(assign, ":cur_town", ":town"),
		(try_end),
		(gt, ":cur_town", -1),

		(call_script, "script_merchant_road_info_to_s42", ":cur_town"),
		(assign, ":bandit_party_found", reg0),
		(party_is_active, ":bandit_party_found"),
		(gt, ":bandit_party_found", 0),

        (try_begin),
            (eq, "$cheat_mode", 1),
            (display_message, "str_traveller_attack_found"),
        (try_end),

		(assign ,":result", "qst_track_down_bandits"),
		(assign, ":relevant_party", ":bandit_party_found"),
	(else_try),  #raid a caravan to start war
		##diplomacy start+
        #SB : quest not already active
        (neg|check_quest_active, "qst_cause_provocation"),
	    ##Roguish and tmt_humanitarian < 0 also should qualify.
		(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
		(assign, ":humanitarian_value", reg0),
		(lt, ":humanitarian_value", 1),
		(assign, reg0, 0),#<-- satisfies requirement
		(try_begin),
			#Originally, only lrep_debauched qualified
			(troop_slot_eq, ":giver_troop", slot_lord_reputation_type, lrep_debauched),
			(assign, reg0, 1),
		(else_try),
			#Roguish qualifies for anti-humanitarians
			(troop_slot_eq, ":giver_troop", slot_lord_reputation_type, lrep_roguish),
			(lt, ":humanitarian_value", 1),
			(assign, reg0, 1),
		(try_end),
		(eq, reg0, 1),
		##diplomacy end+
		(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),

		(assign, ":junior_debauched_lord_in_faction", -1),
      ##diplomacy start+
		#Add support for promoted kingdom ladies
		#(try_for_range, ":lord_in_faction", active_npcs_begin, active_npcs_end),
		(try_for_range, ":lord_in_faction", heroes_begin, heroes_end),
			(this_or_next|is_between, ":lord_in_faction", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":lord_in_faction", slot_troop_occupation, slto_kingdom_hero),
			(call_script, "script_dplmc_get_troop_morality_value", ":giver_troop", tmt_humanitarian),
			(assign, ":other_humanitarian", reg0),
			(lt, ":other_humanitarian", 1),
			(assign, reg0, 0),#<-- satisfies personality requirement
			(try_begin),
				#originally just debauched lords
				(troop_slot_eq, ":lord_in_faction", slot_lord_reputation_type, lrep_debauched),
				(assign, reg0, 1),
			(else_try),
				#roguish qualifies for anti-humanitarians
				(troop_slot_eq, ":giver_troop", slot_lord_reputation_type, lrep_roguish),
				(lt, ":humanitarian_value", 1),
				(assign, reg0, 1),
			(try_end),
			(eq, reg0, 1),
	  ##diplomacy end+
			(store_faction_of_troop, ":debauched_lord_faction", ":lord_in_faction"),
			(eq, ":debauched_lord_faction", ":giver_troop_faction"),
			(assign, ":junior_debauched_lord_in_faction", ":lord_in_faction"),
		(try_end),
		(eq, ":giver_troop", ":junior_debauched_lord_in_faction"),

		(assign, ":faction_to_attack", -1),
		(assign, ":faction_to_attack_score", -1),

	    (try_for_range, ":faction_candidate", kingdoms_begin, kingdoms_end),
			(neq, ":faction_candidate", ":giver_troop_faction"),
			(faction_slot_eq, ":faction_candidate", slot_faction_state, sfs_active),
			(neq, ":faction_candidate", "$players_kingdom"),

			(store_relation, ":relation", ":faction_candidate", ":giver_troop_faction"),

			(store_add, ":provocation_slot", ":giver_troop_faction", slot_faction_provocation_days_with_factions_begin),
			(val_sub, ":provocation_slot", kingdoms_begin),
			(faction_get_slot, ":provocation_days", ":faction_candidate", ":provocation_slot"),

			(ge, ":relation", 0), #disqualifies if the faction is already at war
			(le, ":provocation_days", 0), #disqualifies if the faction has already provoked someone

			(store_random_in_range, ":faction_candidate_score", 0, 100),
			#add in scores - no truce?
#				(store_add, ":truce_slot", ":giver_troop_faction", slot_faction_truce_days_with_factions_begin),
#				(store_add, ":provocation_slot", ":giver_troop_faction", slot_faction_provocation_days_with_factions_begin),
#				(val_sub, ":truce_slot", kingdoms_begin),
#				(val_sub, ":provocation_slot", kingdoms_begin),
#				(faction_slot_eq, ":faction_candidate", ":provocation_slot", 0),
#				(try_begin),
#					(faction_slot_ge, ":faction_candidate", ":truce_slot", 1),
#					(val_sub, ":faction_to_attack_temp_score", 1),
#				(try_end),

			(gt, ":faction_candidate_score", ":faction_to_attack_score"),
				(assign, ":faction_to_attack", ":faction_candidate"),
			(assign, ":faction_to_attack_score", ":faction_candidate_score"),
	    (try_end),

		(is_between, ":faction_to_attack", kingdoms_begin, kingdoms_end),

		(assign ,":result", "qst_cause_provocation"),
		(assign, ":relevant_faction", ":faction_to_attack"),

	(try_end),

    (assign, reg0, ":result"),
    (assign, reg1, ":relevant_troop"),
    (assign, reg2, ":relevant_party"),
    (assign, reg3, ":relevant_faction"),

    ])
]
