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

npc_decision_checklist_marry_female_pc_scripts = [
("npc_decision_checklist_marry_female_pc", #
	[
	(store_script_param, ":npc", 1),
    #diplomacy start+ (players of either gender may marry opposite-gender lords)
    #  Note that many of the strings used here have been altered to change based on the player's gender.
	#  Also, it should be mention that reason is written to s14.
	(assign, ":save_reg1", reg1),
	#Use gender script
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", "trp_player", ":npc"),
	(assign, ":is_female", reg0),
	(assign, ":npc_female", reg1),
    #diplomacy end+

	(troop_get_slot, ":npc_reputation_type", ":npc", slot_lord_reputation_type),

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":npc", "trp_player"),
	(assign, ":romantic_chemistry", reg0),

	(call_script, "script_troop_get_relation_with_troop", ":npc", "trp_player"),
	(assign, ":relation_with_player", reg0),

	(assign, ":competitor", -1),
	(try_for_range, ":competitor_candidate", kingdom_ladies_begin, kingdom_ladies_end),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_1, ":competitor_candidate"),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_2, ":competitor_candidate"),
			(troop_slot_eq, ":npc", slot_troop_love_interest_3, ":competitor_candidate"),
		(call_script, "script_troop_get_relation_with_troop", ":npc", ":competitor"),
		(assign, ":competitor_relation", reg0),

		(gt, ":competitor_relation", ":relation_with_player"),
		(assign, ":competitor", ":competitor_candidate"),
	(try_end),

	(assign, ":player_possessions", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(troop_slot_eq, ":center", slot_town_lord, "trp_player"),
		(val_add, ":player_possessions", 1),
	(try_end),

	(assign, ":lord_agrees", 0),
	#reasons for refusal
	(try_begin),
		(troop_slot_ge, "trp_player", slot_troop_betrothed, active_npcs_begin),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":npc"),

		(str_store_string, s14, "str_my_lady_engaged_to_another"),
	(else_try),
		#bad relationship - minor
		(lt, ":relation_with_player", -3),
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
		(this_or_next|eq, ":npc_reputation_type", lrep_cunning),
		##diplomacy start+ also test commoner types
		(this_or_next|eq, ":npc_reputation_type", lrep_roguish),
		(this_or_next|eq, ":npc_reputation_type", lrep_custodian),
		(this_or_next|eq, ":npc_reputation_type", lrep_benefactor),
		#And certain lady types?
		(this_or_next|eq, ":npc_reputation_type", lrep_ambitious),
		(this_or_next|eq, ":npc_reputation_type", lrep_moralist),
		##diplomacy end+
			(eq, ":npc_reputation_type", lrep_goodnatured),

		(str_store_string, s14, "str_madame__given_our_relations_in_the_past_this_proposal_is_most_surprising_i_do_not_think_that_you_are_the_kind_of_woman_who_can_be_bent_to_a_hushands_will_and_i_would_prefer_not_to_have_our_married_life_be_a_source_of_constant_acrimony"),

	(else_try), #really bad relationship
		(lt, ":relation_with_player", -10),

		(this_or_next|eq, ":npc_reputation_type", lrep_quarrelsome),
		(this_or_next|eq, ":npc_reputation_type", lrep_debauched),
			(eq, ":npc_reputation_type", lrep_selfrighteous),

		(str_store_string, s14, "str_i_would_prefer_to_marry_a_proper_maiden_who_will_obey_her_husband_and_is_not_likely_to_split_his_head_with_a_sword"),
	(else_try),
		(lt, ":romantic_chemistry", 5),

		(str_store_string, s14, "str_my_lady_not_sufficient_chemistry"),

	(else_try), #would prefer someone more ladylike
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
			(eq, ":npc_reputation_type", lrep_martial),
        #diplomacy start+ (players of either gender may marry opposite-gender lords)
        #I tried to keep this as symmetric as possible, but this sentence is ridiculous with reversed genders
		(neq, ":npc_female", 1),
        (eq, ":is_female", 1),
		#To reduce annoyance, I've changed this away from an absolute prohibition.
		(troop_get_slot, ":veto", ":npc", slot_troop_set_decision_seed),
		(val_add, ":veto", "$romantic_attraction_seed"),
		(val_mod, ":veto", 5),#4 out of 5 will still automatically refuse
		(try_begin),#make an exception for companions
			(is_between, ":npc", companions_begin, companions_end),
			(assign, ":veto", 0),
		(else_try),
			#On diminished prejudice mode, get rid of the "80% automatically refuse" condition.
			(ge, "$g_disable_condescending_comments", 2),
			(assign, ":veto", 0),
		(try_end),
		(try_begin),
			#Skip the subsequent checks if there's no way for them to pass
			(neq, ":veto", 0),
		(else_try),
			#Requires high chemistry, high relation, and positive honor
			(this_or_next|lt, ":romantic_chemistry", 15),
			(this_or_next|lt, ":relation_with_player", 30),
				(lt, "$player_honor", 10),
			(assign, ":veto", 1),
		(else_try),
			#Relation must be above some arbitrary threshold (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_sub, reg0, 100, ":romantic_chemistry"),
			(lt, ":relation_with_player", reg0),
			(assign, ":veto", 1),
		(else_try),
			#The lord's level must not be less than 75% of the player's (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_character_level, reg0, "trp_player"),
			(val_mul, reg0, 3),
			(val_div, reg0, 4),
			(store_character_level, reg1, ":npc"),
			(lt, reg1, reg0),
			(assign, ":veto", 1),
		(else_try),
			#One of the lord's female relatives must like the player, if any such lords exist.
			(lt, "$g_disable_condescending_comments", 2),
			(troop_get_slot, ":npc_mother", ":npc", slot_troop_mother),
			(assign, reg1, 0),#3 = some disapproved, 2 = some approved, 1 = some existed and had no opinion, 0 = there were none
			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
				(assign, reg0, 0),
				(try_begin),
					(troop_slot_eq, ":kingdom_lady", slot_troop_guardian, ":npc"),
					(assign, reg0, 1),
				(else_try),
					(is_between, ":npc_mother", heroes_begin, heroes_end),
					(this_or_next|eq, ":kingdom_lady", ":npc_mother"),
						(troop_slot_eq, ":kingdom_lady", slot_troop_mother, ":npc_mother"),
					(assign, reg0, 1),
				(try_end),
				(neq, reg0, 0),
				(call_script, "script_troop_get_player_relation", ":kingdom_lady"),
				(try_begin),#some were found and like the player
					(ge, reg0, 1),
					(val_max, reg1, 2),
				(else_try),#some were found and have no opinion
					(eq, reg0, 0),
					(val_max, reg1, 1),
				(else_try),#some were found and dislike the player
					(val_max, reg1, 3),
				(try_end),
			(try_end),
			(neq, reg0, 0),
			(neq, reg0, 2),
			(assign, ":veto", 1),
		(try_end),
		#Check if the veto holds
		(neq, ":veto", 0),
        #diplomacy end+

		(str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	(else_try),
		(eq, ":npc_reputation_type", lrep_quarrelsome),
		(lt, ":romantic_chemistry", 15),

		(str_store_string, s14, "str_nah_i_want_a_woman_wholl_keep_quiet_and_do_what_shes_told_i_dont_think_thats_you"),
	(else_try), #no properties
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),

		(ge, ":romantic_chemistry", 10),
		(eq, ":player_possessions", 0),

		(str_store_string, s14, "str_my_lady_you_are_possessed_of_great_charms_but_no_properties_until_you_obtain_some_to_marry_you_would_be_an_act_of_ingratitude_towards_my_ancestors_and_my_lineage"),

	(else_try), #you're a nobody - I can do better
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),

		(eq, ":player_possessions", 0),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_no_known_family_of_no_possessions__in_short_a_nobody_do_you_think_that_you_are_fit_to_marry_into_may_family"),
	(else_try), #just not that into you
		(lt, ":romantic_chemistry", 5),
		(lt, ":relation_with_player", 20),

		(neq, ":npc_reputation_type", lrep_debauched),
		(neq, ":npc_reputation_type", lrep_selfrighteous),

		(str_store_string, s14, "str_my_lady__forgive_me__the_quality_of_our_bond_is_not_of_the_sort_which_the_poets_tell_us_is_necessary_to_sustain_a_happy_marriage"),

	(else_try), #you're a liability, given your relation with the liege
		(eq, ":npc_reputation_type", lrep_cunning),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		(str_store_troop_name, s4, ":leader"),
		(call_script, "script_troop_get_relation_with_troop", ":leader", "trp_player"),
		(lt, reg0, -10),

		(str_store_string, s14, "str_um_i_think_that_if_i_want_to_stay_on_s4s_good_side_id_best_not_marry_you"),
	(else_try),	#part of another faction
		(gt, "$players_kingdom", 0),
		(neq, "$players_kingdom", "$g_talk_troop_faction"),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		##diplomacy start+ use gender script
		#(troop_get_type, reg4, ":leader"),
		(call_script, "script_dplmc_store_troop_is_female_reg", ":leader", 4),
		##diplomacy end+

		(str_store_string, s14, "str_you_serve_another_realm_i_dont_see_s4_granting_reg4herhis_blessing_to_our_union"),
	(else_try), #there's a competitor
		(gt, ":competitor", -1),
		(str_store_troop_name, s4, ":competitor"),

		(str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
    ##diplomacy start+
	#By default these should not be reachable, but future changes may expose them
	#unintentionally.
	(else_try),#redundant: shouldn't be called for betrothed lords
	   (troop_slot_ge, ":npc", slot_troop_betrothed, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_betrothed),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for married lords
	   (troop_slot_ge, ":npc", slot_troop_spouse, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_spouse),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for claimants or kings
	   (this_or_next|is_between, ":npc", kings_begin, kings_end),
	      (is_between, ":npc", pretenders_begin, pretenders_end),
	   #This probably wouldn't ever occur, but put a string here just in case.
	   #The male version is ridiculous.
	   (str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	##diplomacy end+
	(else_try),
		(lt, ":relation_with_player", 10),
		(assign, ":lord_agrees", 2),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_shall_give_your_proposal_consideration"),
	(else_try),
		(assign, ":lord_agrees", 1),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_would_be_most_honored_were_you_to_become_my_wife"),
	(try_end),

    ##diplomacy start+ revert register
	(assign, reg1, ":save_reg1"),
	##diplomacy end+
	(assign, reg0, ":lord_agrees"),

	]
	)
]
