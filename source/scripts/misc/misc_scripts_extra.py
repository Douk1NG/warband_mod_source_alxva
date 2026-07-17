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
from module_items import items
from ID_strings import str_key_0

####################################################################################################################
# NATIVE MISCELLANEOUS SCRIPTS (EXTRA)
# 
# This file contains remaining Native and mod-mixed scripts that were extracted in a second pass.
# Includes: rebellion logic, lord commentary, courtship/marriage, formations system,
# camera/death cam, disguises, WSE hooks, battle tactics, and UI helpers.
####################################################################################################################

#cross refs for alternate versions of weapons
def make_noswing_weapons(items):
  noswing_weapons = []
  for i_item in xrange(len(items)):
    noswing_name = 'noswing_' + items[i_item][0]
    i_noswing = find_object (items, noswing_name)
    if i_noswing > -1:
      noswing_weapons.append((item_set_slot, i_item, slot_item_alternate, i_noswing))
      noswing_weapons.append((item_set_slot, i_noswing, slot_item_alternate, i_item))
  return noswing_weapons[:]

def keys_array():
  keys_list = []
  for key_no in xrange(len(keys)):
    keys_list.append((troop_set_slot, "trp_temp_array_a", key_no, keys[key_no]))
    keys_list.append((troop_set_slot, "trp_temp_array_b", key_no, str_key_0+key_no))
  return keys_list[:]

misc_scripts_extra = [
("get_manhunt_information_to_s15",
    [
     (store_script_param, ":quest", 1),

	(str_store_string, s15, "str_the_roads_are_full_of_brigands_friend_but_that_name_in_particular_does_not_sound_familiar_good_hunting_to_you_nonetheless"),
    (quest_get_slot, ":quarry", ":quest", slot_quest_target_party),
	(try_begin),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":talk_party", "$g_talk_troop", slot_troop_leaded_party),
	(else_try),
		(gt, "$g_encountered_party", "p_spawn_points_end"),
		(assign, ":talk_party", "$g_encountered_party"),
	(else_try),
		(assign, ":talk_party", -1),
	(try_end),

    (try_for_range, ":log_entry", 0, "$num_log_entries"),
		(gt, ":talk_party", -1),
		(troop_get_slot, ":party", "trp_log_array_actor", ":log_entry"),
		(eq, ":party", ":talk_party"),
		(troop_get_slot, ":bandit_party", "trp_log_array_troop_object", ":log_entry"),
		(eq, ":bandit_party", ":quarry"),
		(store_current_hours, ":hours_ago"),
		(troop_get_slot, ":sighting_time", "trp_log_array_entry_time",  ":log_entry"),
		(val_sub, ":hours_ago", ":sighting_time"),
		(try_begin),
			(le, ":hours_ago", 1),
			(str_store_string, s16, "str_less_than_an_hour_ago"),
		(else_try),
			(le, ":hours_ago", 48),
			(assign, reg3, ":hours_ago"),
			(str_store_string, s16, "str_maybe_reg3_hours_ago"),
		(else_try),
			(val_div, ":hours_ago", 24),
			(assign, reg3, ":hours_ago"),
			(str_store_string, s16, "str_reg3_days_ago"),
		(try_end),

		(troop_get_slot, ":center", "trp_log_array_center_object", ":log_entry"),
		(str_store_party_name, s17, ":center"),
		(troop_get_slot, ":entry_type", "trp_log_array_entry_type", ":log_entry"),
		(eq, ":entry_type", logent_party_spots_wanted_bandits),
		(str_store_string, s15, "str_youre_in_luck_we_sighted_those_bastards_s16_near_s17_hurry_and_you_might_be_able_to_pick_up_their_trail_while_its_still_hot"),

#		(try_begin),
#			(eq, ":entry_type", logent_party_chases_wanted_bandits),
#			(str_store_string, s15, "@You're in luck. We gave chase to those bastards {s16} near {s17}. They have eluded us so far -- but perhaps you will do better..."),
#		(else_try),
#			(eq, ":entry_type", logent_party_runs_from_wanted_bandits),
#			(str_store_string, s15, "@As it happens, they tried to run us down near {s17} {s16}. By the heavens, I hope you teach them a lesson."),
#		(try_end),
	(try_end),
	]),


#Troop Commentaries end



  ("rebellion_arguments", #Right now, called only in one place. This is only used when for player overtures, and will need some changes if this script is called when NPCs try to suborn lords
    [
     (store_script_param, ":lord", 1),
     (store_script_param, ":argument", 2),
     (store_script_param, ":candidate", 3),

     (assign, ":argument_appeal", 0),
     (assign, ":argument_strength", 0),

     (troop_get_slot, ":reputation", ":lord", slot_lord_reputation_type),

	 (store_faction_of_troop, ":lord_faction", ":candidate"),
	 (store_faction_of_troop, ":candidate_faction", ":candidate"),

	 (try_begin),
		(eq, ":candidate", "trp_player"),
		(assign, ":right_to_rule", "$player_right_to_rule"),
	 (else_try), #default right to rule of 75 for pretenders claiming throne
		(is_between, ":candidate", pretenders_begin, pretenders_end),
		(troop_slot_eq, ":candidate", slot_troop_original_faction, ":lord_faction"),
		(assign, ":right_to_rule", 75),
	 (else_try), #default right to rule of 60 for all other lords
		(assign, ":right_to_rule", 60),
	 (try_end),

	 (try_begin),
		(eq, ":argument", argument_claim),
		(store_sub, ":argument_strength", ":right_to_rule", 30),
	 (else_try),
		(eq, ":argument", argument_ruler),
		(store_sub, ":argument_strength", "$player_honor", 20),
	 (else_try),
		(eq, ":argument", argument_lords),
		(store_sub, ":argument_strength", "$player_honor", 20),
	 (else_try),
	    #argument_strength is ((5 * number of centers player have) - 40) if argument type is argument_victory
		(eq, ":argument", argument_victory),
		(assign, ":argument_strength", 0),
		(try_for_range, ":center", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center"),
			(assign, ":argument_strength", -40),
			(try_begin),
				(eq, "$players_kingdom", ":candidate_faction"),
				##diplomacy start+
				(this_or_next|eq, ":center_faction", "$players_kingdom"),
				##diplomacy end+
				(this_or_next|eq, ":center_faction", "fac_player_faction"),
				(eq, ":center_faction", "fac_player_supporters_faction"),
				(val_add, ":argument_strength", 5),
			(else_try),
				(eq, ":center_faction", ":candidate_faction"),
				(val_add, ":argument_strength", 5),
			(try_end),
		(try_end),
	 (else_try),
	    #argument_strength is (20 - 20 * (number of lords in player's faction which not awareded fief by player although there is a fief awarding in future promise))
		(eq, ":argument", argument_benefit),
		(assign, ":argument_strength", 20),
		(try_for_range, ":lord_promised_fief", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":other_faction", ":lord_promised_fief"),
			(neq, ":lord", "$g_talk_troop"),
			(this_or_next|eq, ":other_faction", "fac_player_supporters_faction"),
			(eq, ":other_faction", "$players_kingdom"),
			(troop_slot_eq, ":lord_promised_fief", slot_troop_promised_fief, 1),
			(val_sub, ":argument_strength", 20),
		(try_end),
	 (try_end),
	 (val_clamp, ":argument_strength", -40, 41),

     (try_begin),
         (eq, ":reputation", lrep_martial),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 30),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_to_the_throne_good_there_is_nothing_id_rather_do_than_fight_for_a_good_cause"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_to_the_throne_well_there_is_nothing_id_rather_do_than_fight_for_a_good_cause_but_the_claim_you_make_seems_somewhat_weak"),
		     (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_i_am_pleased_that_you_speak_of_upholding_my_ancient_rights_which_are_sometimes_trod_upon_in_these_sorry_days"),
			 (else_try),
			    ##diplomacy start+ use culturally-approrpriate term
				(call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
				##diplomacy end+
				(str_store_string, s15, "str_i_am_pleased_that_you_speak_of_upholding_my_ancient_rights_but_sometimes_men_make_pledges_before_they_are_king_which_they_cannot_keep_once_they_take_the_throne"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 0),
			 (try_begin),
				##diplomacy start+: use culturally-approrpriate term
				(call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_USE_MY_WEAPON, s14),
				##diplomacy end+
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_well_i_supposed_thats_good_but_sometimes_the_commons_overstep_their_boundaries_im_more_concerned_that_your_claim_be_legal_so_i_can_swing_my_sword_with_a_good_conscience"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_good_i_ask_for_no_more_than_my_due"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_unfortunately_you_are_not_wellknown_for_rewarding_those_to_whom_you_have_made_such_offers"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", -30),
			 (str_store_string, s15, "str_you_speak_of_unifying_calradia_well_i_believe_that_well_always_be_fighting__its_important_that_we_fight_for_a_rightful_cause"),
         (try_end),
     (else_try),
        (eq, ":reputation", lrep_quarrelsome),
        (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),
 			 (str_store_string, s15, "str_you_talk_of_claims_to_the_throne_but_i_leave_bickering_about_legalities_to_the_lawyers_and_clerks"),
		(else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -30),
			  ##diplomacy start+ use culturally-approrpriate term
			  (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			  ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_ruling_justly_hah_ill_believe_theres_such_a_thing_as_a_just_king_when_i_see_one"),
		(else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 0),
			 ##diplomacy start+ use culturally-approrpriate term
			  (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			  ##diplomacy end+
			 (str_store_string, s15, "str_you_spoke_of_protecting_the_rights_of_the_nobles_if_you_did_youd_be_the_first_king_to_do_so_in_a_very_long_time"),
		(else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 30),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_ay_well_lets_see_if_you_deliver"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_bah_youre_not_known_for_delivering_on_your_pledges"),
			 (try_end),
	    (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_youve_done_a_good_job_at_making_calradia_bend_its_knee_to_you_so_maybe_thats_not_just_talk"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_id_be_impressed_if_i_thought_you_could_do_it_but_unfortunately_you_dont"),
			 (try_end),
		(try_end),
     (else_try),
         (eq, ":reputation", lrep_selfrighteous),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),
			 (str_store_string, s15, "str_you_speak_of_claims_to_the_throne_well_any_peasant_can_claim_to_be_a_kings_bastard"),
		 (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -30),
			 (str_store_string, s15, "str_well_its_a_fine_thing_to_court_the_commons_with_promises_but_what_do_you_have_to_offer_me"),
		 (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 0),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_that_would_make_a_fine_change_if_my_rights_as_lord_would_be_respected"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_that_would_make_a_fine_change_if_my_rights_as_lord_would_be_respected_however_it_is_easy_for_you_to_make_promises_while_you_are_weak_that_you_have_no_intention_of_keeping_when_you_are_strong"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_well_my_family_is_of_ancient_and_noble_lineage_so_you_promise_me_no_more_than_my_due_still_your_gesture_is_appreciated"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_well_you_make_that_pledge_but_i_am_not_impressed"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_much_of_this_land_now_bends_its_knee_to_you_so_perhaps_that_is_not_just_talk"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_but_right_now_yours_is_just_one_squabbling_faction_among_many"),
			 (try_end),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_cunning),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -30),
			 (str_store_string, s15, "str_you_speak_of_claims_well_no_offense_but_a_claim_unsupported_by_might_rarely_prospers"),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_well_i_suppose_that_will_make_for_a_more_prosperous_realm_ive_always_tried_to_treat_my_peasants_decently_saves_going_to_bed_worrying_about_whether_youll_wake_up_with_the_roof_on_fire"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_very_well_but_remember_that_peasants_are_more_likely_to_cause_trouble_if_you_make_promises_then_dont_deliver_than_if_you_never_made_the_promise_in_the_first_place"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", 15),
 			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_good_youd_be_well_advised_to_do_that__men_fight_better_for_a_king_wholl_respect_their_rights"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_very_well_but_remember__failing_to_keep_promises_which_you_made_while_scrambling_up_the_throne_is_the_quickest_way_to_topple_off_of_it_once_you_get_there"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -20),
			 (str_store_string, s15, "str_you_speak_of_giving_me_land_very_good_but_often_i_find_that_when_a_man_makes_too_many_promises_trying_to_get_to_the_top_he_has_trouble_keeping_them_once_he_reaches_it"),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_many_have_said_that_you_might_very_well_be_the_one_to_do_it"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_well_all_the_kings_say_that_im_not_sure_that_you_will_succeed_while_they_fail"),
			 (try_end),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_debauched),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", -20),
			 (str_store_string, s15, "str_you_speak_of_claims_do_you_think_i_care_for_the_nattering_of_lawyers"),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", -20),
             ##diplomacy start+ replace "swineherd" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_SWINEHERD, 14),
             ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_protecting_the_commons_how_kind_of_you_i_shall_tell_my_swineherd_all_about_your_sweet_promises_no_doubt_he_will_become_your_most_faithful_vassal"),
         (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", -10),
             ##diplomacy start+ replace "lords" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
             ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_protecing_the_rights_of_lords_such_sweet_words_but_ill_tell_you_this__the_only_rights_that_are_respected_in_this_world_are_the_rights_to_dominate_whoever_is_weaker_and_to_submit_to_whoever_is_stronger"),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_yes_very_good__but_you_had_best_deliver"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_giving_me_land_hah_perhaps_all_those_others_to_whom_you_promised_lands_will_simply_step_aside"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_you_may_indeed_humble_the_other_kings_of_this_land_and_in_that_case_i_would_hope_that_you_would_remember_me_as_your_faithful_servant"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_but_you_are_weak_and_i_think_that_you_will_remain_weak"),
			 (try_end),
         (try_end),
	 (else_try),
         (eq, ":reputation", lrep_goodnatured),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 10),
			 ##diplomacy start+ replace "king" with culturally-appropriate term
             (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_its_good_for_a_king_to_have_a_strong_claim_although_admittedly_im_more_concerned_that_he_rules_just_ly_than_with_legalities_anyway_your_claim_seems_wellfounded_to_me"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_but_your_claim_seems_a_bit_weak_to_me"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 20),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_like_that_my_tenants_are_a_happy_lot_i_think_but_i_hear_of_others_in_other_estates_that_arent_so_fortunate"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_im_glad_to_hear_you_say_that_but_do_me_a_favor__dont_promise_the_commons_anything_you_cant_deliver_thats_a_sure_way_to_get_them_to_rebel_and_it_breaks_my_heart_to_have_to_put_them_down"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_lords),
			 (assign, ":argument_appeal", 0),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 15),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 14),
			 ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_well_very_good_i_suppose_but_you_know__we_lords_can_take_of_ourselves_its_the_common_folk_who_need_a_strong_king_to_look_out_for_them_to_my_mind"),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -15),
			 (str_store_string, s15, "str_you_speak_of_giving_me_land_its_kind_of_you_really_though_that_is_not_necessary"),
         (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", -25),
             ##diplomacy start+
             #Save culturally-appropriate variant of "sword" (as in "by the sword") to s14
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_WEAPON, 14),
			 ##diplomacy end+
			 (str_store_string, s15, "str_you_speak_of_unifying_calradia_well_maybe_you_can_unite_this_land_by_the_sword_but_im_not_sure_that_this_will_make_you_a_good_ruler"),
         (try_end),
     (else_try),
         (eq, ":reputation", lrep_upstanding),
         (try_begin),
             (eq, ":argument", argument_claim),
             (assign, ":argument_appeal", 10),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_claims_a_king_must_have_a_strong_legal_claim_for_there_not_to_be_chaos_in_the_realm_and_yours_is_wellestablished"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_claims_a_king_must_have_a_strong_legal_claim_for_there_not_to_be_chaos_in_the_realm_but_your_claim_is_not_so_strong"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_lords),
             (assign, ":argument_appeal", -5),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_LORD_PLURAL, 15),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_it_is_of_course_important_that_a_king_respect_the_rights_of_his_vassals_although_i_worry_that_a_king_who_took_a_throne_without_proper_cause_would_not_rule_with_justice"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_rights_of_lords_it_is_of_course_important_that_a_king_respect_the_rights_of_his_vassals_however_i_would_like_to_know_that_you_would_indeed_deliver_on_your_promises"),
			 (try_end),
		 (else_try),
             (eq, ":argument", argument_ruler),
             (assign, ":argument_appeal", 5),
			 ##diplomacy start+ use culturally-approrpriate term
			 (call_script, "script_dplmc_print_cultural_word_to_sreg", ":lord", DPLMC_CULTURAL_TERM_KING, 14),
			 ##diplomacy end+
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_would_be_pleased_to_serve_a_king_who_respected_the_rights_of_his_subjects_although_i_worry_that_a_king_who_took_a_throne_without_proper_cause_would_not_rule_with_justice"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_protecting_the_commons_i_would_be_pleased_to_serve_a_king_who_respected_the_rights_of_his_subjects_however_i_would_like_to_know_that_you_would_indeed_deliver_on_your_promises"),
			 (try_end),
         (else_try),
             (eq, ":argument", argument_benefit),
             (assign, ":argument_appeal", -40),
			 (str_store_string, s15, "str_i_am_not_swayed_by_promises_of_reward"),
		 (else_try),
             (eq, ":argument", argument_victory),
             (assign, ":argument_appeal", 10),
			 (try_begin),
				(gt, ":argument_strength", 0),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_it_would_be_good_to_bring_peace_to_the_realm_and_i_believe_that_you_are_strong_enough_to_do_so"),
			 (else_try),
				(str_store_string, s15, "str_you_speak_of_unifying_calradia_it_would_be_good_to_bring_peace_the_realm_but_with_your_kingdom_in_its_current_state_i_worry_that_you_are_just_bringing_more_discord"),
			 (try_end),
         (try_end),
     (try_end),

	 (str_store_string, s14, "str_s15"),

     (assign, reg0, ":argument_appeal"),
     (assign, reg1, ":argument_strength"),
]),



#Rebellion changes end
  # Input: none
  # Output: none
  ("combat_music_set_situation_with_culture",
    [
      (assign, ":situation", mtf_sit_fight),
      (assign, ":num_allies", 0),
      (assign, ":num_enemies", 0),
      (try_for_agents, ":agent_no"),
        (agent_is_alive, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
        (store_character_level, ":troop_level", ":agent_troop_id"),
        (val_add,  ":troop_level", 10),
        (val_mul, ":troop_level", ":troop_level"),
        (try_begin),
          (agent_is_ally, ":agent_no"),
          (val_add, ":num_allies", ":troop_level"),
        (else_try),
          (val_add, ":num_enemies", ":troop_level"),
        (try_end),
      (try_end),
      (val_mul, ":num_allies", 4), #play ambushed music if we are 2 times outnumbered.
      (val_div, ":num_allies", 3),
      (try_begin),
        (lt, ":num_allies", ":num_enemies"),
        (assign, ":situation", mtf_sit_ambushed),
      (try_end),
      (call_script, "script_music_set_situation_with_culture", ":situation"),
     ]),

  # script_play_victorious_sound
  # Input: troop_no
  # Output: none
  #Other search terms: release, peace

  ("remove_troop_from_prison",
    [
      (store_script_param, ":troop_no", 1),
      (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
      (troop_set_slot, ":troop_no", slot_troop_courtesan, -1),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_lord_by_replace"),
        (quest_slot_eq, "qst_rescue_lord_by_replace", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_lord_by_replace"),
      (try_end),
      (try_begin),
        (eq, "$do_not_cancel_quest", 0),
        (check_quest_active, "qst_rescue_prisoner"),
        (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_rescue_prisoner"),
        #SB : cancel companion missions
        (try_for_range, ":companions", companions_begin, companions_end),
          (troop_slot_eq, ":companions", slot_troop_current_mission, dplmc_npc_mission_rescue_prisoner),
          (troop_slot_eq, ":companions", slot_troop_mission_object, ":troop_no"),
          (troop_set_slot, ":companions", slot_troop_current_mission, npc_mission_rejoin_when_possible),
          (troop_set_slot, ":companions", slot_troop_days_on_mission, 1),
        (try_end),
        # also accrues debts
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          # (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
          (gt, ":cur_debt", dplmc_ransom_debt_mask),
          (val_mod, ":cur_debt", dplmc_ransom_debt_mask),
          (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
        (try_end),
      (try_end),
      (try_begin),
        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
        (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":troop_no"),
        (call_script, "script_cancel_quest", "qst_deliver_message_to_prisoner_lord"),
      (try_end),
      ]),

  # script_debug_variables
  # Input: two variables which will be examined by coder, this script is only for debugging.
  # Output: none
  ("debug_variables",
    [
    ]),

#lord recruitment scripts begin
  ("troop_describes_troop_to_s15",
  [
	(store_script_param, ":troop_1", 1),
	(store_script_param, ":troop_2", 2),


	(str_store_troop_name, s15, ":troop_2"),

	(try_begin),
		(eq, ":troop_2", "trp_player"),
		(str_store_string, s15, "str_you"),
	(else_try),
		(eq, ":troop_2", ":troop_1"),
		(str_store_string, s15, "str_myself"),
	(else_try),
		(call_script, "script_troop_get_family_relation_to_troop", ":troop_2", ":troop_1"),
		(gt, reg0, 0),
		(str_store_string, s15, "str_my_s11_s15"),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop_2", ":troop_1"),
		(ge, reg0, 20),
		(str_store_string, s15, "str_my_friend_s15"),
	(try_end),

	]),

  ("troop_describes_quarrel_with_troop_to_s14",
  #perhaps replace this with get_relevant_comment at a later date
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":troop_2", 2),

	(str_store_troop_name, s15, ":troop"),
	(str_store_troop_name, s16, ":troop_2"),

	(str_store_string, s14, "str_stop_gap__s15_is_the_rival_of_s16"),

	(try_begin),
		(eq, ":troop", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop", ":troop_2"),
		(str_store_string, s14, s17),
	(else_try),
		(eq, ":troop_2", "$g_talk_troop"),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":troop_2", ":troop"),
		(str_store_string, s14, s17),
	(else_try),
		(str_store_string, s14, "str_general_quarrel"),
	(try_end),

]),

  ("cf_test_lord_incompatibility_to_s17", #writes rivalry chance to reg0
    [

	(store_script_param, ":source_lord", 1),
	(store_script_param, ":target_lord", 2),


	(assign, ":chance_of_rivalry", 0),

	(troop_get_slot, ":source_reputation", ":source_lord", slot_lord_reputation_type),
	(troop_get_slot, ":target_reputation", ":target_lord", slot_lord_reputation_type),

	##diplomacy start+ Note: the next line is in native, but as far as I can discern the register value wasn't actually used.
	(troop_get_type, reg15, ":target_lord"),
	##diplomacy end+

	(str_store_troop_name, s18, ":target_lord"),

	(assign, ":divisor", 1),

	(call_script, "script_troop_get_family_relation_to_troop", ":target_lord", ":source_lord"),
	(assign, ":family_relationship", reg0),

	(try_begin),
		(gt, ":family_relationship", 0),
		(store_div, ":family_divisor", reg0, 5),
		(val_add, ":divisor", ":family_divisor"),
		(str_store_string, s18, "str_my_s11_s18"),
	(else_try),
		(gt, ":target_reputation", lrep_upstanding),
		(this_or_next|eq, ":source_reputation", lrep_debauched),
			(eq, ":source_reputation", lrep_selfrighteous),
		(str_store_string, s18, "str_the_socalled_s11_s18"),
	(try_end),

   ##diplomacy start+ get gender types
	(assign, ":save_reg65", reg65),#save register values to revert at end of script
	(assign, ":save_reg3", reg3),
	(call_script, "script_dplmc_store_troop_is_female_reg", ":target_lord", 3),#reg3 used below for gender-correct pronouns
	(call_script, "script_dplmc_store_troop_is_female", ":source_lord"),
   (assign, reg65, reg0),#used below in some situations for speaker
   (assign, reg0, ":family_relationship"),#revert register to value before this section
	##diplomacy end+
	(try_begin), #test if reps are compatible
        (eq, ":source_reputation", lrep_martial),
		(is_between, ":family_relationship", 1, 5), #uncles and cousins

		(assign, ":chance_of_rivalry", 100),
        (str_store_string, s17, "str_s18_would_cheat_me_of_my_inheritance_by_heaven_i_know_my_rights_and_im_not_going_to_back_down"),
	(else_try),
        (eq, ":source_reputation", lrep_martial),
        (eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_s18_once_questioned_my_honour_and_my_bravery_i_long_for_the_day_when_i_can_meet_him_in_battle_and_make_him_retract_his_statement"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_martial),
        (eq, ":target_reputation", lrep_upstanding),
        (str_store_string, s17, "str_s18_once_questioned_my_judgment_in_battle_by_heaven_would_he_have_us_shirk_our_duty_to_smite_our_sovereigns_foes"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":target_reputation", lrep_martial),
		(is_between, ":family_relationship", 1, 5),

		(assign, ":chance_of_rivalry", 100),
        (str_store_string, s17, "str_s18_seems_to_think_he_has_the_right_to_some_of_my_property_well_he_does_not"),

	(else_try),
        (eq, ":source_reputation", lrep_quarrelsome),
        (eq, ":target_reputation", lrep_martial),
        (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_quarrelsome),
        (eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_s18_is_a_crafty_weasel_and_i_dont_trust_him_one_bit"),
		(assign, ":chance_of_rivalry", 100),


    (else_try),
        (eq, ":source_reputation", lrep_debauched),
        (eq, ":target_reputation", lrep_upstanding),
		(str_store_string, s17, "str_s18_i_despite_him_he_puts_on_such_a_nauseating_display_of_virtue_and_thinks_nothing_of_insulting_his_betters"),
		(assign, ":chance_of_rivalry", 100),

        #debauched insults upstanding

    (else_try),
        (eq, ":source_reputation", lrep_debauched),
        (eq, ":target_reputation", lrep_selfrighteous),
		(str_store_string, s17, "str_s18_entered_into_a_little_deal_with_me_and_is_now_trying_to_wriggle_out_of_it"),
		(assign, ":chance_of_rivalry", 100),

        #debauched insults selfrighteous



    (else_try),
        (eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_debauched),
		(str_store_string, s17, "str_s18_once_ran_an_errand_for_me_and_now_thinks_i_owe_him_something_i_owe_his_ilk_nothing"),
		(assign, ":chance_of_rivalry", 100),
        #selfrighteous dismisses debauched

    (else_try),
        (eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_goodnatured),
		(str_store_string, s17, "str_s18_is_soft_and_weak_and_not_fit_to_govern_a_fief_and_i_have_always_detested_him"),
		(assign, ":chance_of_rivalry", 100),



	(else_try),
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_s18_is_a_quarrelsome_oaf_and_a_liability_in_my_opinion_and_ive_let_him_know_as_much"),
		(assign, ":chance_of_rivalry", 100),
        #cunning insults quarrelsome

	(else_try),
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_goodnatured),
        (str_store_string, s17, "str_s18_i_am_sorry_to_say_is_far_too_softhearted_a_man_to_be_given_any_kind_of_responsibility_his_chivalry_will_allow_the_enemy_to_flee_to_fight_another_day_and_will_cost_the_lives_of_my_own_faithful_men"),
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_s18_seems_to_have_something_against_me_for_some_reason_i_dont_like_to_talk_ill_of_people_but_i_think_hes_can_be_a_bit_of_a_cad_sometimes"),
		(assign, ":chance_of_rivalry", 100),

	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"),
		(assign, ":chance_of_rivalry", 100),



	(else_try),
        (eq, ":source_reputation", lrep_upstanding),
        (eq, ":target_reputation", lrep_debauched),
        (str_store_string, s17, "str_s18_is_thoroughly_dishonorable_and_a_compulsive_spinner_of_intrigues_which_i_fear_will_drag_us_into_wars_or_incite_rebellions"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
        (eq, ":source_reputation", lrep_upstanding),
        (eq, ":target_reputation", lrep_martial),
        (str_store_string, s17, "str_s18_disappoints_me_i_once_scolded_for_his_rashness_in_battle_and_he_took_offense_i_do_not_care_to_apologize_for_my_efforts_to_save_his_life_and_the_lives_of_his_men"),
		(assign, ":chance_of_rivalry", 50),

	#for commons
	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_upstanding),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_roguish),
        (str_store_string, s17, "str_s18_squanders_money_and_carouses_in_a_way_most_unbefitting_a_noble_by_doing_so_he_disgraces_us_all"),
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (eq, ":source_reputation", lrep_roguish),
        (this_or_next|eq, ":target_reputation", lrep_upstanding),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_been_speaking_ill_of_me_behind_my_back_or_so_they_say"),
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_quarrelsome),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_custodian),
        (str_store_string, s17, "str_s18_is_a_disgrace_reg3shehe_consorts_with_merchants_lends_money_at_interest_uses_coarse_language_and_shows_no_attempt_to_uphold_the_dignity_of_the_honor_bestowed_upon_reg3herhim"),
		(assign, ":chance_of_rivalry", 100),

	(else_try),
        (eq, ":source_reputation", lrep_custodian),
		(this_or_next|eq, ":target_reputation", lrep_quarrelsome),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_condemned_me_for_engaging_in_commerce_what_could_possibly_be_wrong_with_that"),
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (this_or_next|eq, ":source_reputation", lrep_debauched),
		(this_or_next|eq, ":source_reputation", lrep_martial),
			(eq, ":source_reputation", lrep_selfrighteous),
        (eq, ":target_reputation", lrep_benefactor),
        (str_store_string, s17, "str_s18_i_have_heard_has_been_encouraging_seditious_ideas_among_the_peasantry__a_foolish_move_which_endangers_us_all"),
		(assign, ":chance_of_rivalry", 100),


	(else_try),
        (eq, ":source_reputation", lrep_benefactor),
		(this_or_next|eq, ":target_reputation", lrep_debauched),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_s18_has_called_me_out_for_the_way_i_deal_with_my_tenants_well_so_be_it_if_i_teach_them_that_they_are_the_equal_of_anyone_with_socalled_gentle_blood_what_is_it_to_reg3herhim"),
		(assign, ":chance_of_rivalry", 100),


	#lady incompatibilities
	(else_try),
		(eq, ":source_reputation", lrep_conventional),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_selfrighteous),
        (str_store_string, s17, "str_a_most_gallant_gentleman_who_knows_how_to_treat_a_lady"),
		(assign, ":chance_of_rivalry", -50),

	(else_try),
		(eq, ":source_reputation", lrep_conventional),
		(eq, ":target_reputation", lrep_quarrelsome),
        (str_store_string, s17, "str_a_base_cad"),
		(assign, ":chance_of_rivalry", 50),


	(else_try),
		(eq, ":source_reputation", lrep_adventurous),
		(eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_a_man_who_treats_me_as_his_equal_which_is_rare"),
		(assign, ":chance_of_rivalry", -50),

	(else_try),
		(eq, ":source_reputation", lrep_adventurous),
		(this_or_next|eq, ":target_reputation", lrep_martial),
			(eq, ":target_reputation", lrep_debauched),
		(str_store_string, s17, "str_appears_to_value_me_with_his_estate_and_his_horse_as_prizes_worth_having"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
		(eq, ":source_reputation", lrep_adventurous),
		(neq, ":target_reputation", lrep_goodnatured),

        (str_store_string, s17, "str_a_bit_dull_but_what_can_you_expect"),
		(assign, ":chance_of_rivalry", 10),

	(else_try),
		(eq, ":source_reputation", lrep_otherworldly),
		(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lord", ":target_lord"),
		(ge, reg0, 10),
        (str_store_string, s17, "str_the_man_whom_destiny_intends_for_me"),
		(assign, ":chance_of_rivalry", -50),

	(else_try),
		(eq, ":source_reputation", lrep_otherworldly),
		(lt, reg0, 0),

        (str_store_string, s17, "str_is_not_right_for_me__i_cannot_say_why_but_he_makes_my_skin_crawl"),
		(assign, ":chance_of_rivalry", 50),


	(else_try),
		(eq, ":source_reputation", lrep_ambitious),
		(this_or_next|eq, ":target_reputation", lrep_selfrighteous),
			(eq, ":target_reputation", lrep_cunning),
        (str_store_string, s17, "str_is_a_man_who_clearly_intends_to_make_his_mark_in_the_world"),
		(assign, ":chance_of_rivalry", -20),

	(else_try),
		(eq, ":source_reputation", lrep_ambitious),
		(eq, ":target_reputation", lrep_goodnatured),

        (str_store_string, s17, "str_is_a_layabout_a_naif_prey_for_others_who_are_cleverer_than_he"),
		(assign, ":chance_of_rivalry", 30),


	(else_try),
		(eq, ":source_reputation", lrep_moralist),
		(eq, ":target_reputation", lrep_upstanding),

        (str_store_string, s17, "str_is_a_man_of_stalwart_character"),
		(assign, ":chance_of_rivalry", -50),

	(else_try),
		(eq, ":source_reputation", lrep_moralist),
		(this_or_next|eq, ":target_reputation", lrep_debauched),
			(eq, ":target_reputation", lrep_cunning),

        (str_store_string, s17, "str_appears_to_be_a_man_of_low_morals"),
		(assign, ":chance_of_rivalry", 50),

	(else_try),
		(eq, ":source_reputation", lrep_moralist),
		(eq, ":target_reputation", lrep_quarrelsome),

        (str_store_string, s17, "str_appears_to_be_a_man_who_lacks_selfdiscipline"),
		(assign, ":chance_of_rivalry", 50),
##diplomacy start+ Support for promoted ladies:
   (else_try),
       #Ambitious vs otherworldly
       (eq, ":source_reputation", lrep_ambitious),
       (troop_slot_eq, ":source_lord", slot_troop_occupation, slto_kingdom_hero),
       (eq, ":target_reputation", lrep_otherworldly),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (str_store_string, s17, "str_s18_is_soft_and_weak_and_not_fit_to_govern_a_fief_and_i_have_always_detested_him"),
       (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"),
		(assign, ":chance_of_rivalry", 100),
   (else_try),
       #Otherworldly vs ambitious
       (eq, ":source_reputation", lrep_otherworldly),
       (troop_slot_eq, ":source_lord", slot_troop_occupation, slto_kingdom_hero),
       (eq, ":target_reputation", lrep_ambitious),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (str_store_string, s17, "str_s18_has_always_treated_me_contemptuously_although_i_have_done_him_no_wrong"),
		(assign, ":chance_of_rivalry", 100),
   (else_try),
       #Quarrelsome quarrels with conventional and moralist
       (eq, ":source_reputation", lrep_quarrelsome),
       (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
       (this_or_next|eq, ":target_reputation", lrep_moralist),
          (eq, ":target_reputation", lrep_conventional),
       (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"),
		(assign, ":chance_of_rivalry", 50),
   (else_try),
        #Cunning conflicts with moralist
        (eq, ":source_reputation", lrep_cunning),
        (eq, ":target_reputation", lrep_moralist),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (str_store_string, s17, "str_s18_i_am_sorry_to_say_is_far_too_softhearted_a_man_to_be_given_any_kind_of_responsibility_his_chivalry_will_allow_the_enemy_to_flee_to_fight_another_day_and_will_cost_the_lives_of_my_own_faithful_men"),
		(assign, ":chance_of_rivalry", 50),
    (else_try),
        #Debauched conflicts with moralist
        (eq, ":source_reputation", lrep_debauched),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":target_reputation", lrep_moralist),
		(str_store_string, s17, "str_s18_i_despite_him_he_puts_on_such_a_nauseating_display_of_virtue_and_thinks_nothing_of_insulting_his_betters"),
		(assign, ":chance_of_rivalry", 50),
    (else_try),
        #Martial or debauched conflicts with adventurous
	   (this_or_next|eq, ":source_reputation", lrep_martial),
	   (eq, ":source_reputation", lrep_debauched),
      (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
      (eq, ":target_reputation", lrep_adventurous),
      (str_store_string, s17, "str_s18_once_took_something_i_said_amiss_stubborn_bastard_wont_give_it_up_and_keeps_trying_to_get_me_to_recant_my_words"),
		(assign, ":chance_of_rivalry", 50),
	(else_try),
        (eq, ":source_reputation", lrep_goodnatured),
        (troop_slot_eq, ":target_lord", slot_troop_occupation, slto_kingdom_hero),
        (eq, ":target_reputation", lrep_ambitious),
        (str_store_string, s17, "str_s18_seems_to_have_something_against_me_for_some_reason_i_dont_like_to_talk_ill_of_people_but_i_think_hes_can_be_a_bit_of_a_cad_sometimes"),
		  (assign, ":chance_of_rivalry", 30),
##Add support for secondary morality types
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":target_lord", tmt_honest),
		(ge, reg0, 1),#This would apply (if no previous condition was reached) to Marnid, Rolf, Firentis, Alayan, and Jeremus.
		(eq, ":source_reputation", lrep_moralist),
		(str_store_string, s17, "str_is_a_man_of_stalwart_character"),#<- (does not apply to Rolf, since he is Cunning)
		(assign, ":chance_of_rivalry", -50),
	(else_try),
		(call_script, "script_dplmc_get_troop_morality_value", ":target_lord", tmt_pious),
		(ge, reg0, 1),#This doesn't apply to anyone at the moment.
		(eq, ":source_reputation", lrep_moralist),
		(str_store_string, s17, "str_is_a_man_of_stalwart_character"),
		(assign, ":chance_of_rivalry", -50),
	(try_end),

##diplomacy end+

	(val_div, ":chance_of_rivalry", ":divisor"),
##diplomacy start+ for companions, use compatability information
    (try_begin),
	   (is_between, ":source_lord", companions_begin, companions_end),
	   (troop_slot_eq, ":source_lord", slot_troop_personalitymatch_object, ":target_lord"),
	   (val_min, ":chance_of_rivalry", -100),
	(else_try),
	   (is_between, ":source_lord", companions_begin, companions_end),
	   (this_or_next|troop_slot_eq, ":source_lord", slot_troop_personalityclash_object, ":target_lord"),
	   (troop_slot_eq, ":source_lord", slot_troop_personalityclash2_object, ":target_lord"),
	   (try_begin),
	      (le, ":chance_of_rivalry", 0),
		  (str_store_string, s17, "str_general_quarrel"),
	   (try_end),
	   (val_max, ":chance_of_rivalry", 100),
	(try_end),
	(assign, reg3, ":save_reg3"),#revert reg3
	(assign, reg65, ":save_reg65"),#revert reg65
##diplomacy end+
	(assign, reg0, ":chance_of_rivalry"),

	(neq, ":chance_of_rivalry", 0),
#	(eq, ":incompatibility_found", 1), #cf can be removed with this

	]),

  ("troop_get_romantic_chemistry_with_troop", #source is lady, target is man
    [
      ##diplomacy start+ (players of either gender may marry opposite-gender lords)
      #Note: the above is misleading even in Native, since when target_lord is the player,
      #target_lord can be female and source_lady can be male.
	  (assign, ":save_reg1", reg1),
      ##diplomacy end+
      (store_script_param, ":source_lady", 1),
      (store_script_param, ":target_lord", 2),

      (store_add, ":chemistry_sum", ":source_lady", ":target_lord"),
      (val_add, ":chemistry_sum", "$romantic_attraction_seed"),

      #This calculates (modula ^ 2) * 3
      (store_mod, ":chemistry_remainder", ":chemistry_sum", 5),
      (val_mul, ":chemistry_remainder", ":chemistry_remainder"), #0, 1, 4, 9, 16
      (val_mul, ":chemistry_remainder", 3), #0, 3, 12, 27, 48

      (store_attribute_level, ":romantic_chemistry", ":target_lord", ca_charisma),
      (val_sub, ":romantic_chemistry", ":chemistry_remainder"),

      (val_mul, ":romantic_chemistry", 2),
      ##diplomacy start+ ensure companion compatability
      (try_begin),
         (is_between, ":source_lady", companions_begin, companions_end),
         (troop_slot_eq, ":source_lady", slot_troop_personalitymatch_object, ":target_lord"),
         (val_max, ":romantic_chemistry", 15),
      (else_try),
         (is_between, ":target_lord", companions_begin, companions_end),
         (troop_slot_eq, ":target_lord", slot_troop_personalitymatch_object, ":source_lady"),
         (val_max, ":romantic_chemistry", 15),
	  #...and companion incompatibility.
	  (else_try),
  	     (is_between, ":source_lady", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":source_lady", slot_troop_personalityclash_object, ":target_lord"),
			(troop_slot_eq, ":source_lady", slot_troop_personalityclash2_object, ":target_lord"),
		 (val_min, ":romantic_chemistry", -15),
  	  (else_try),
  	     (is_between, ":target_lord", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":target_lord", slot_troop_personalityclash_object, ":source_lady"),
			(troop_slot_eq, ":target_lord", slot_troop_personalityclash2_object, ":source_lady"),
		(val_min, ":romantic_chemistry", -15),
	  #Prevent glitches.  This can be enabled explicitly if intentional.
      (else_try),
	     (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
         (eq, reg0, reg1),#different genders
         #(val_min, ":romantic_chemistry", -15), #dckplmc
      (try_end),
	  (assign, reg1, ":save_reg1"),
      ##diplomacy end+
      (assign, reg0, ":romantic_chemistry"),

      #examples :
      #For a charisma of 18, yields (18 - 0) * 2 = 36, (18 - 3) * 2 = 30, (18 - 12) * 2 = 12, (18 - 27) * 2 = -18, (18 - 48) * 2 = -60
      #For a charisma of 10, yields (10 - 0) * 2 = 20, (10 - 3) * 2 = 14, (10 - 12) * 2 = -4, (10 - 27) * 2 = -34, (10 - 48) * 2 = -76
      #For a charisma of 7, yields  (7 - 0) * 2 = 14,  (7 - 3) * 2 = 8,   (7 - 12) * 2 = -10, (7 - 27) * 2 = -40,  (7 - 48) * 2 = -82

      #15 is high attraction, 0 is moderate attraction, -76 is lowest attraction
	]),


  ("cf_troop_get_romantic_attraction_to_troop", #source is lady, target is man
    [

	(store_script_param, ":source_lady", 1),
	(store_script_param, ":target_lord", 2),

	(assign, ":weighted_romantic_assessment", 0),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),
	#Use gender script
	#(troop_get_type, ":source_is_female", ":source_lady"),
	#(eq, ":source_is_female", 1),
	#(troop_get_type, ":target_is_female", ":target_lord"),
	#(eq, ":target_is_female", 0),
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
	(assign, ":source_is_female", reg0),
	(assign, ":target_is_female", reg1),
	(assign, reg1, ":save_reg1"),
    #(assign, reg0, -15), #dckplmc
	(neq, ":source_is_female", ":target_is_female"),
	##diplomacy end+

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lady", ":target_lord"),
	(assign, ":romantic_chemistry", reg0),


	#objective attraction - average renown
	(troop_get_slot, ":modified_renown", ":target_lord", slot_troop_renown),
	(assign, ":lady_status", 60),
   ##diplomacy start+ adjust status based on who they are
	(try_begin),
      #The renown bonus is decreased the more important the lady's relatives are.
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
      (troop_get_slot, ":best_renown", ":source_lady", slot_troop_renown),
      (try_begin),
        (troop_get_slot, ":relative", ":source_lady", slot_troop_father),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_guardian),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_mother),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (ge, ":best_renown", 600),
        (store_div, ":lady_status", ":best_renown", 10),
   	(else_try),
		  (lt, ":best_renown", 400),
        (store_div, ":lady_status", ":best_renown", 10),
		  (val_add, ":lady_status", 20),
   	(try_end),
   	(val_clamp, ":lady_status", 30, 90),
   (try_end),
   ##diplomacy end+
	(val_div, ":modified_renown", 5),
	(val_sub, ":modified_renown", ":lady_status"),
	(val_min, ":modified_renown", 60),



	#weight values
	(try_begin),
		(assign, ":personality_match", 0),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":source_lady", ":target_lord"),
		(store_sub, ":personality_match", 0, reg0),
	(try_end),

	(troop_get_slot, ":lady_reputation", ":source_lady", slot_lord_reputation_type),
	(try_begin),
		(eq, ":lady_reputation", lrep_ambitious),
		(val_mul, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_otherworldly),
		(val_div, ":modified_renown", 2),
		(val_mul, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_adventurous),
		(val_div, ":modified_renown", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_moralist),
		(val_div, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(try_end),

	(val_add, ":weighted_romantic_assessment", ":romantic_chemistry"),
	(val_add, ":weighted_romantic_assessment", ":personality_match"),
	(val_add, ":weighted_romantic_assessment", ":modified_renown"),

	(assign, reg0, ":weighted_romantic_assessment"),

	]),


  ("cf_random_political_event", #right now, just enmities
    [

	##diplomacy start+ Lay more groundwork for heroes other than active-npcs being lords
	##OLD:
	#(store_random_in_range, ":lord_1", active_npcs_begin, active_npcs_end),
	#(store_random_in_range, ":lord_2", active_npcs_begin, active_npcs_end),
	##NEW:
	(store_random_in_range, ":lord_1", heroes_begin, heroes_end),
	(try_begin),
	   (neg|is_between, ":lord_1", active_npcs_begin, active_npcs_end),
	   (neg|troop_slot_eq, ":lord_1", slot_troop_occupation, slto_kingdom_hero),
	   (store_random_in_range, ":lord_1", active_npcs_begin, active_npcs_end),
	(try_end),
	(store_random_in_range, ":lord_2", heroes_begin, heroes_end),
	(try_begin),
	   (neg|is_between, ":lord_2", active_npcs_begin, active_npcs_end),
	   (neg|troop_slot_eq, ":lord_2", slot_troop_occupation, slto_kingdom_hero),
	   (store_random_in_range, ":lord_2", active_npcs_begin, active_npcs_end),
	(try_end),
	##diplomacy end+

	(troop_slot_eq, ":lord_1", slot_troop_occupation, slto_kingdom_hero),
	(troop_slot_eq, ":lord_2", slot_troop_occupation, slto_kingdom_hero),

	(neq, ":lord_1", ":lord_2"),

	(val_add, "$total_political_events", 1),

	(store_troop_faction, ":lord_1_faction", ":lord_1"),
	(store_troop_faction, ":lord_2_faction", ":lord_2"),

	(assign, reg8, "$total_political_events"),


	(faction_get_slot, ":faction_1_leader", ":lord_1_faction", slot_faction_leader),
	(faction_get_slot, ":faction_2_leader", ":lord_2_faction", slot_faction_leader),

	(this_or_next|eq, ":lord_1_faction", ":lord_2_faction"),
	(this_or_next|eq, ":lord_1", ":faction_1_leader"),
		(eq, ":lord_2", ":faction_2_leader"),


	(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":lord_2"),
	(assign, ":relation", reg0),


	(store_random_in_range, ":random", 0, 100),

	(try_begin),
		#reconciliation
		#The chance of a liege reconciling two quarreling vassals is equal to (relationship with lord 1 x relationship with lord 2) / 4

		(eq, ":lord_1_faction", ":lord_2_faction"),
		(neq, ":faction_1_leader", "trp_player"),

		(le, ":relation", -10),

#		(ge, "$total_political_events", 5000),

		(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":faction_1_leader"),
		(gt, reg0, 0),
		(assign, ":lord_1_leader_rel", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":lord_2", ":faction_1_leader"),
		(gt, reg0, 0),
		(store_mul, ":reconciliation_chance", ":lord_1_leader_rel", reg0),
		(val_div, ":reconciliation_chance", 4),	#was 2 before

		(le, ":random", ":reconciliation_chance"),

		(str_store_troop_name, s4, ":faction_1_leader"),
		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_s4_reconciles_s5_and_s6_"),
		(try_end),

		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", 20),
		(val_add, "$total_random_quarrel_changes", 20),
	(else_try),	#lord intervenes in quarrel
		(eq, ":lord_1_faction", ":lord_2_faction"),

		(le, ":relation", -10),
#		(ge, ":random", 50),
		(try_begin),
			(eq, ":faction_1_leader", "trp_player"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_diagnostic__player_should_receive_consultation_quest_here_if_not_already_active"),
			(try_end),
			(neg|check_quest_active, "qst_consult_with_minister"),
			(neg|check_quest_active, "qst_resolve_dispute"),
			(eq, "$g_minister_notification_quest", 0),
			(assign, "$g_minister_notification_quest", "qst_resolve_dispute"),
			(quest_set_slot, "qst_resolve_dispute", slot_quest_target_troop, ":lord_1"),
			(quest_set_slot, "qst_resolve_dispute", slot_quest_object_troop, ":lord_2"),

			(call_script, "script_add_notification_menu", "mnu_notification_player_should_consult", 0, 0),


		(else_try),
			(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":faction_1_leader"),
			(assign, ":lord_1_rel_w_leader", reg0),

			(call_script, "script_troop_get_relation_with_troop", ":lord_2", ":faction_1_leader"),
			(assign, ":lord_2_rel_w_leader", reg0),

			(store_random_in_range, ":another_random", -5, 5),

			(val_add, ":lord_1_rel_w_leader", ":another_random"),

			(try_begin),
				(ge, ":lord_1_rel_w_leader", ":lord_2_rel_w_leader"),
				(assign, ":winner_lord", ":lord_1"),
				(assign, ":loser_lord", ":lord_2"),
			(else_try),
				(assign, ":loser_lord", ":lord_1"),
				(assign, ":winner_lord", ":lord_2"),
			(try_end),

			(str_store_troop_name, s4, ":faction_1_leader"),
			(str_store_troop_name, s5, ":winner_lord"),
			(str_store_troop_name, s6, ":loser_lord"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_check_reg8_s4_rules_in_s5s_favor_in_quarrel_with_s6_"),
			(try_end),

			(call_script, "script_add_log_entry", logent_ruler_intervenes_in_quarrel, ":faction_1_leader",  ":loser_lord", ":winner_lord", ":lord_1_faction"), #faction leader is actor, loser lord is center object, winner lord is troop_object

			(call_script, "script_troop_change_relation_with_troop", ":winner_lord", ":faction_1_leader", 10),
			(call_script, "script_troop_change_relation_with_troop", ":loser_lord", ":faction_1_leader", -20),
			(val_add, "$total_random_quarrel_changes", -10),

		(try_end),


	(else_try), #new quarrel - companions
		(is_between, ":lord_1", companions_begin, companions_end),
		(is_between, ":lord_2", companions_begin, companions_end),

		(ge, ":relation", -10),
		(this_or_next|troop_slot_eq, ":lord_1", slot_troop_personalityclash_object, ":lord_2"),
			(troop_slot_eq, ":lord_1", slot_troop_personalityclash2_object, ":lord_2"),

		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_new_rivalry_generated_between_s5_and_s6"),
		(try_end),

		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", -30),
		(val_add, "$total_random_quarrel_changes", -30),


	(else_try), #new quarrel - others
		(eq, ":lord_1_faction", ":lord_2_faction"),

		(ge, ":relation", -10), #can have two quarrels

		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":lord_1", ":lord_2"),
		(assign, ":chance_of_enmity", reg0),
		(gt, ":chance_of_enmity", 0),


		(lt, ":random", ":chance_of_enmity"), #50 or 100 percent, usually


		(str_store_troop_name, s5, ":lord_1"),
		(str_store_troop_name, s6, ":lord_2"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_check_reg8_new_rivalry_generated_between_s5_and_s6"),
		(try_end),

		(call_script, "script_troop_change_relation_with_troop", ":lord_1", ":lord_2", -30),
		(val_add, "$total_random_quarrel_changes", -30),

#		(call_script, "script_update_troop_notes", ":lord_1"),
#		(call_script, "script_update_troop_notes", ":lord_2"),
	(else_try), #a lord attempts to suborn a character
		(store_current_hours, ":hours"),
		(ge, ":hours", 24),

		(neq, ":lord_1_faction", ":lord_2_faction"),
#		(eq, ":lord_1", ":faction_1_leader"),
		(is_between, ":lord_1_faction", kingdoms_begin, kingdoms_end),

		(call_script, "script_cf_troop_can_intrigue", ":lord_2", 0),
		(neq, ":lord_2", ":faction_2_leader"),
		(neq, ":lord_2", ":faction_1_leader"),

		(str_store_troop_name, s5, ":faction_1_leader"),
		(str_store_troop_name, s6, ":lord_2"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "str_check_reg8_s5_attempts_to_win_over_s6"),
		(try_end),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord_2", ":faction_1_leader"),
		(assign, ":lord_1_score", reg0),

		(call_script, "script_calculate_troop_political_factors_for_liege", ":lord_2", ":faction_2_leader"),
		(assign, ":faction_2_leader_score", reg0),

		(try_begin),
			(gt, ":lord_1_score", ":faction_2_leader_score"),


			(try_begin),
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lord_2"),
				(display_message, "@{!}DEBUG - {s4} faction changed in subornment"),
			(try_end),

			(call_script, "script_change_troop_faction", ":lord_2", ":lord_1_faction"),
		(try_end),
	(try_end),



]),


#this calculates the average number of rivalries per lord, giving a rough indication of how easily a faction may be divided
("cf_troop_can_intrigue",
	#This script should be called from dialogs, and also prior to any event which might result in a lord changing sides
    [
      (store_script_param, ":troop", 1),
      (store_script_param, ":skip_player_party", 2),

		##diplomacy start+
		#Use this to filter out lords who are supposed to be "off the board"
		(assign, ":bad_occupation", 0),
		(try_begin),
		   (gt, ":troop", 0),
			(troop_is_hero, ":troop"),
		   (troop_slot_eq, ":troop", slot_lord_reputation_type, dplmc_slto_dead),
		   (assign, ":bad_occupation", 1),#altered 2011-06-08
		(try_end),
		(eq, ":bad_occupation", 0),
		##diplomacy end+

      (troop_get_slot, ":led_party_1", ":troop", slot_troop_leaded_party),
      (party_is_active, ":led_party_1"),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_active"),
      (try_end),

      (party_get_battle_opponent, ":battle_opponent", ":led_party_1"),
      (le, ":battle_opponent", 0), #battle opponent can be 0 for an attached party?

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_party_is_not_in_battle"),
      (try_end),

      (troop_slot_eq, ":troop", slot_troop_prisoner_of_party, -1),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_not_prisoner"),
      (try_end),

      (party_get_attached_to, ":led_party_1_attached", ":led_party_1"),

      (store_faction_of_party, ":led_party_1_faction", ":led_party_1"),

      (assign, ":other_lords_nearby", 0),
      (try_for_range, ":troop_2", active_npcs_begin, active_npcs_end),
        (neq, ":troop", ":troop_2"),
        (eq, ":other_lords_nearby", 0),

        (troop_slot_eq, ":troop_2", slot_troop_occupation, slto_kingdom_hero),

        (troop_get_slot, ":led_party_2", ":troop_2", slot_troop_leaded_party),
        (party_is_active, ":led_party_2"),
        (neq, ":led_party_1", ":led_party_2"),

        (store_faction_of_party, ":led_party_2_faction", ":led_party_2"),
        (eq, ":led_party_1_faction", ":led_party_2_faction"),

        (try_begin),
          (eq, ":led_party_1_attached", -1),
          (store_distance_to_party_from_party, ":distance", ":led_party_1", ":led_party_2"),
          (lt, ":distance", 3),
          (assign, ":other_lords_nearby", 1),
        (else_try),
          (is_between, ":led_party_1_attached", walled_centers_begin, walled_centers_end),
          (party_get_attached_to, ":led_party_2_attached", ":led_party_2"),
          (eq, ":led_party_1_attached", ":led_party_2_attached"),
          (assign, ":other_lords_nearby", 1),
        (try_end),
      (try_end),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (eq, ":troop", "$g_talk_troop"),
        (display_message, "str_intrigue_test_troop_is_nearby"),
      (try_end),

      (try_begin),
        (eq, ":skip_player_party", 0),
        #temporary spot
      (try_end),

      (eq, ":other_lords_nearby", 0),
	]),


    ("troop_change_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),
	(store_script_param, ":amount", 3),

	(try_begin),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop2", ":amount"),
	(else_try),
		(eq, ":troop2", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop1", ":amount"),
	(else_try),
		##diplomacy start+ Cancel the result for bad troop values
		(this_or_next|lt, ":troop1", 0),
		(this_or_next|lt, ":troop2", 0),
		##diplomacy end+
		(eq, ":troop1", ":troop2"),
		##diplomacy start+ Do this to avoid the controversy check further below
		(assign, ":amount", 0),
		##diplomacy end+
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop1", ":troop2"),
		(store_add, ":new_relation", reg0, ":amount"),

		(val_clamp, ":new_relation", -100, 101),

		(try_begin),
			(eq, ":new_relation", 0),
			(assign, ":new_relation", 1), #this removes the need for a separate "met" slot - any non-zero relation will be a met
		(try_end),

		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_set_slot, ":troop1", ":troop1_slot_for_troop2", ":new_relation"),

		(store_add, ":troop2_slot_for_troop1", ":troop1", slot_troop_relations_begin),
		(troop_set_slot, ":troop2", ":troop2_slot_for_troop1", ":new_relation"),
	(try_end),


	(try_begin), #generate controversy if troops are in the same faciton
		(lt, ":amount", -5),
		(try_begin),
			(eq, ":troop1", "trp_player"),
			(assign, ":faction1", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction1", ":troop1"),
		(try_end),
		(try_begin),
			(eq, ":troop2", "trp_player"),
			(assign, ":faction2", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction2", ":troop2"),
		(try_end),
		(eq, ":faction1", ":faction2"),
		(is_between, ":faction1", kingdoms_begin, kingdoms_end),

		(store_mul, ":controversy_generated", ":amount", -1),

		(troop_get_slot, ":controversy1", ":troop1", slot_troop_controversy),
		(val_add, ":controversy1", ":controversy_generated"),
		(val_min, ":controversy1", 100),
		(troop_set_slot, ":troop1", slot_troop_controversy, ":controversy1"),

		(troop_get_slot, ":controversy2", ":troop2", slot_troop_controversy),
		(val_add, ":controversy2", ":controversy_generated"),
		(val_min, ":controversy2", 100),
		(troop_set_slot, ":troop2", slot_troop_controversy, ":controversy2"),

	(try_end),

	(try_begin),
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		#(is_between, ":troop1", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(try_begin),
			(gt, ":amount", 0),
			(val_add, "$total_relation_adds", ":amount"),
		(else_try),
			(val_sub, "$total_relation_subs", ":amount"),
		(try_end),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 4), #change back to 4
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		# (is_between, ":troop1", active_npcs_begin, active_npcs_end),
		# (is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(str_store_troop_name, s20, ":troop1"),
		(str_store_troop_name, s15, ":troop2"),
		(assign, reg4, ":amount"),
		(assign, reg14, ":new_relation"),
		(display_message, "str_s20_relation_with_s15_changed_by_reg4_to_reg14"),

		(assign, reg4, "$total_relation_adds"),
		(display_message, "str_total_additions_reg4"),
		(assign, reg4, "$total_relation_subs"),
		(display_message, "str_total_subtractions_reg4"),

		(assign, reg4, "$total_courtship_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total courtship quarrel changes: {reg4}"),

		(assign, reg4, "$total_random_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total random quarrel changes: {reg4}"),

		(assign, reg4, "$total_battle_ally_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for allies: {reg4}"),

		(assign, reg4, "$total_battle_enemy_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for enemies: {reg4}"),

		(assign, reg4, "$total_promotion_changes"),
		(display_message, "@{!}DEBUG -- Total promotion changes: {reg4}"),

		(assign, reg4, "$total_feast_changes"),
		(display_message, "@{!}DEBUG -- Total feast changes: {reg4}"),

		(assign, reg4, "$total_policy_dispute_changes"),
		(assign, reg5, "$number_of_controversial_policy_decisions"),
		(display_message, "@{!}DEBUG -- Total policy dispute changes: {reg4} from {reg5} decisions"),

		(assign, reg4, "$total_indictment_changes"),
		(display_message, "@{!}DEBUG -- Total faction switch changes: {reg4}"),

		(assign, reg4, "$total_no_fief_changes"),
		(display_message, "@{!}DEBUG -- Total no fief changes: {reg4}"),

		(assign, reg4, "$total_relation_changes_through_convergence"),
		(display_message, "@{!}DEBUG -- Total changes through convergence: {reg4}"),

		(assign, reg4, "$total_vassal_days_responding_to_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal responses to campaign: {reg4}"),

		(assign, reg4, "$total_vassal_days_on_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal campaign days: {reg4}"),

		(val_max, "$total_vassal_days_on_campaign", 1),
		(store_mul, ":response_rate", "$total_vassal_days_responding_to_campaign", 100),
		(val_div, ":response_rate", "$total_vassal_days_on_campaign"),
		(assign, reg4, ":response_rate"),
		(display_message, "@{!}DEBUG -- Vassal response rate: {reg4}"),



#		(assign, reg4, "$total_joy_battle_changes"),
#		(display_message, "@{!}DEBUG -- Total joy of battle changes"),

	(try_end),

	]),


    ("troop_get_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),

	(assign, ":relation", 0),
	(try_begin),
		##diplomacy start+
		#Change "eq -1", to "lt 0"
		(this_or_next|lt, ":troop1", 0),
			(lt, ":troop2", 0),
		##diplomacy end+

		#Possibly switch to relation with liege
		(assign, ":relation", 0),
	(else_try),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop2"),
		(assign, ":relation", reg0),
	(else_try),
		(eq, ":troop2", "trp_player"),
		(call_script, "script_troop_get_player_relation", ":troop1"),
		(assign, ":relation", reg0),
	(else_try),
		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_get_slot, ":relation", ":troop1", ":troop1_slot_for_troop2"),
	(try_end),


	(val_clamp, ":relation", -100, 101),
	(assign, reg0, ":relation"),

	]),



	("locate_player_minister", #maybe deprecate this
    [
	##diplomacy start+ Handle player is co-ruler of NPC faction
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	##diplomacy end+
	(assign, ":walled_center_found", 0),
	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(lt, ":walled_center_found", centers_begin),
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+
		(this_or_next|eq, ":walled_center_faction", ":alt_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(neg|party_slot_ge, ":walled_center", slot_town_lord, active_npcs_begin), #ie, player or a reserved slot
		(assign, ":walled_center_found", ":walled_center"),
	(try_end),

	(troop_get_slot, ":old_location", "$g_player_minister", slot_troop_cur_center),
	(troop_set_slot, "$g_player_minister", slot_troop_cur_center, ":walled_center_found"),

	(try_begin),
		(neq, ":old_location", ":walled_center"),
		(str_store_party_name, s10, ":walled_center"),
		(str_store_troop_name, s11, "$g_player_minister"),
		(display_message, "str_s11_relocates_to_s10"),
	(try_end),

	]),


	("get_kingdom_lady_social_determinants", #Calradian society is rather patriarchal, at least among the upper classes
    [
	(store_script_param, ":kingdom_lady", 1),

	(store_faction_of_troop, ":faction_of_lady", ":kingdom_lady"),
	(assign, ":center", -1),
	(assign, ":closest_male_relative", -1),
	(assign, ":best_center_score", 0),

	##diplomacy start+
	##TODO: Re-implement, disabled for now.  "Don't get stuck attached to a MIA relative"
	(try_begin),
		(troop_slot_ge, ":kingdom_lady", slot_troop_spouse, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_spouse),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_father, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_father),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(else_try),
		#added
		(troop_slot_ge, ":kingdom_lady", slot_troop_mother, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_mother),
		(troop_slot_eq, ":closest_male_relative", slot_troop_occupation, slto_kingdom_hero),
	(else_try),
		(troop_slot_ge, ":kingdom_lady", slot_troop_guardian, 0),
		(troop_get_slot, ":closest_male_relative", ":kingdom_lady", slot_troop_guardian),
		#(neg|troop_slot_ge, ":closest_male_relative", slot_troop_occupation, slto_retirement),#added: has not been removed from play
	(try_end),
	##diplomacy end+

	##diplomacy start+
    #Avoid strange problems if the argument is not a kingdom lady.
	(try_begin),
		(this_or_next|is_between, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_lady),
		(neg|troop_slot_eq, ":kingdom_lady", slot_troop_occupation, slto_kingdom_hero),
		(assign, ":is_lady", 1),
	(else_try),
		(assign, ":is_lady", 0),
		(assign, ":closest_male_relative", ":kingdom_lady"),# is doing this useful for the way this script is used, or should we just set it to -1?
	(try_end),

	##OLD:
	#(try_begin), #if ongoing social event (maybe add if not besieged)
	##NEW:
	(try_begin),
		(eq, ":is_lady", 0),
		(call_script, "script_lord_get_home_center", ":kingdom_lady"),
		(assign, ":center", reg0),
		(is_between, ":center", walled_centers_begin, walled_centers_end),
	(else_try), #if ongoing social event (maybe add if not besieged)
	##diplomacy end+
		(faction_slot_eq, ":faction_of_lady", slot_faction_ai_state, sfai_feast),
		(faction_get_slot, ":feast_center", ":faction_of_lady", slot_faction_ai_object),

		(gt, ":closest_male_relative", -1),
		(troop_get_slot, ":closest_male_party", ":closest_male_relative", slot_troop_leaded_party),
		(party_is_active, ":closest_male_party"),
		(party_get_attached_to, ":closest_male_cur_location", ":closest_male_party"),

		(eq, ":closest_male_cur_location", ":feast_center"),
		(is_between, ":feast_center", walled_centers_begin, walled_centers_end),

		(assign, ":center", ":feast_center"),

	(else_try),
		(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),
		###diplomacy begin
    (try_begin),
    ##diplomacy end
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(assign, ":center", "$g_player_court"),
		##diplomacy begin
    (else_try),
      (troop_get_slot, ":cur_residence", ":kingdom_lady", slot_troop_cur_center),
      (is_between, ":cur_residence", walled_centers_begin, walled_centers_end),
      (party_slot_eq, ":cur_residence", slot_town_lord, "trp_player"),
      (assign, ":center", ":cur_residence"),
    (try_end),
    (is_between, ":center",  walled_centers_begin, walled_centers_end),
    ##diplomacy end
	(else_try),
		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":walled_center_faction", ":walled_center"),
			(this_or_next|eq, ":faction_of_lady", ":walled_center_faction"),
				(neg|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end), #lady married to a player without a faction

			(party_get_slot, ":castle_lord", ":walled_center", slot_town_lord),

			(gt, ":castle_lord", -1),

			(call_script, "script_troop_get_family_relation_to_troop", ":kingdom_lady", ":castle_lord"),
			##diplomacy start+
			(try_begin),
				(eq, ":is_lady", 0),
				(eq, ":castle_lord", ":kingdom_lady"),
				(val_max, reg0, 16),
			(try_end),
			##diplomacy end+

			(try_begin),
				(this_or_next|is_between, ":faction_of_lady", kingdoms_begin, kingdoms_end),
					(troop_slot_eq, "trp_player", slot_troop_spouse, ":kingdom_lady"),

				(faction_slot_eq, ":faction_of_lady", slot_faction_leader, ":castle_lord"),
				(val_max, reg0, 1),
			(try_end),

			(try_begin),
				(eq, "$cheat_mode", 2),
				(str_store_troop_name, s3, ":kingdom_lady"),
				(str_store_troop_name, s4, ":castle_lord"),
				(str_store_party_name, s5, ":walled_center"),
				(display_message, "str_checking_s3_at_s5_with_s11_relationship_with_s4_score_reg0"),
				(str_clear, s11),
			(try_end),

			(gt, reg0, ":best_center_score"),

			(assign, ":best_center_score", reg0),
			(assign, ":center", ":walled_center"),


	    (try_end),
	(try_end),

	(assign, reg0, ":closest_male_relative"),
	(assign, reg1, ":center"),


	]),


	#This is probably unnecessarily complicated, but can support a multi-generational mod
	("age_troop_one_year",
    [
	(store_script_param, ":troop_no", 1),
    ##diplomacy start+ use gender script
	#(troop_get_type, ":is_female", ":troop_no"),
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
	(assign, ":is_female", reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+

	(troop_get_slot, ":age", ":troop_no", slot_troop_age),
	(troop_get_slot, ":appearance", ":troop_no", slot_troop_age_appearance),

	(val_add, ":age", 1),
	(store_random_in_range, ":addition", 1, 5),

	(try_begin),
		(eq, ":is_female", 1),
#		(val_add, ":addition", 2), #the women's age slider seems to produce less change than the male one - commented out: makes women look too old.
	(try_end),

	(val_add, ":appearance", ":addition"),
	(try_begin),
		(gt, ":age", 45),
		(store_attribute_level, ":strength", ":troop_no", ca_strength),
		(store_attribute_level, ":agility", ":troop_no", ca_agility),
		(store_random_in_range, ":random", 0, 50), #2% loss brings it down to about 36% by age 90, but of course can be counteracted by new level gain
		(try_begin),
			(lt, ":random", ":strength"),
			(troop_raise_attribute, ":troop_no", ca_strength, -1),
		(try_end),
		(try_begin),
			(lt, ":random", ":agility"),
			(troop_raise_attribute, ":troop_no", ca_agility, -1),
		(try_end),
	(try_end),

	(val_clamp, ":appearance", 1, 100),

	(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(troop_set_slot, ":troop_no", slot_troop_age_appearance, ":appearance"),
	(troop_set_age, ":troop_no", ":appearance"),
	]),


	("init_troop_age",
	[
	(store_script_param, ":troop_no", 1),
	(store_script_param, ":age", 2), #minimum 20

	(try_begin),
		(gt, ":age", 20),
		(troop_set_slot, ":troop_no", slot_troop_age, 20),
	(else_try),
		(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
	(try_end),

	(store_sub, ":years_to_age", ":age", 20),
    (troop_set_age, ":troop_no", 0),

	(try_begin),
		(gt, ":years_to_age", 0),
		(try_for_range, ":unused", 0, ":years_to_age"),
			(call_script, "script_age_troop_one_year", ":troop_no"),
		(try_end),
	(try_end),

	]),


	("assign_troop_love_interests", #Called at the beginning, or whenever a lord is spurned
    [
	(store_script_param, ":cur_troop", 1),
    ##diplomacy start+
	#wrap the entire thing in a try-statement: do nothing when called erroneously
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(try_begin),
	(this_or_next|is_between, ":cur_troop", lords_begin, lords_end),
	(this_or_next|is_between, ":cur_troop", companions_begin, companions_end),
	(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),#kingdom heroes only
	(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),#not married, engaged
	(troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),

	#avoid unintentional erroneous pairings (intentional exceptions can be added)
	#(troop_get_type, ":troop_type", ":cur_troop"),
	(call_script, "script_dplmc_store_troop_is_female", ":cur_troop"),
	(assign, ":troop_type", reg0),

	(try_begin),
	    #Certain personality types don't care about flouting convention.
		(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_debauched),
        (this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_roguish),
        (troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_adventurous),
		(assign, ":troop_type", abs(tf_male) + abs(tf_female) + 1),#guaranteed not to equal tf_male or tf_female
	(try_end),
	(store_faction_of_troop, ":troop_faction", ":cur_troop"),
	#assign default initial courtships for companions
	(try_begin),
		(is_between, ":cur_troop", companions_begin, companions_end),
        (troop_get_slot, ":cur_lady", ":cur_troop", slot_troop_personalitymatch_object),
        (is_between, ":cur_lady", heroes_begin, heroes_end),

		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		#(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(lt, reg0, 2),#check not a close relative
        #(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),
		(ge, reg0, 0), #do not develop love interest if already spurned (but DO allow re-courting)

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_begin),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
    (try_end),
    ##diplomacy end+
	(try_for_range, ":unused", 0, 50),
		(store_random_in_range, ":cur_lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":cur_lady", slot_troop_spouse, -1),
		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		##diplomacy start+
		##(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
        (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		#(eq, reg0, 0),
		#right now nothing gives a value of 1, but change this check in case more distant relations are reported
		(lt, reg0, 2),#check not a close relative
		#(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
        ##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),

		(eq, reg0, 0), #do not develop love interest if already spurned or courted

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
	##diplomacy start+ also allow -1 to signify no-one courted
		(try_begin),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
	(try_end),
        (try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":save_reg0"),#revert register
	##diplomacy end+
	]),

	("courtship_event_lady_break_relation_with_suitor", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),

	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_slot_eq, ":suitor", ":love_interest_slot", ":lady"),
		##diplomacy start+ set to -1 instead, since 0 is the player (how annoying)
		#(troop_set_slot, ":suitor", ":love_interest_slot", 0),
		(troop_set_slot, ":suitor", ":love_interest_slot", -1),
		##diplomacy end+
	(try_end),
	(call_script, "script_assign_troop_love_interests", ":suitor"),

	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_betrothed, ":suitor"),


		(troop_set_slot, ":lady", slot_troop_betrothed, -1),
	##diplomacy start+ perform the same check for the suitor that was done,
	#for the lady, so this script has no unfortunate consequences even if
	#called inappropriately.
	(try_end),
	(try_begin),
		(troop_slot_eq, ":suitor", slot_troop_betrothed, ":lady"),
		(troop_set_slot, ":suitor", slot_troop_betrothed, -1),
	##diplomacy end+
	(try_end),


	]),


	("courtship_event_bride_marry_groom", #parameters from dialog or scripts
	[
	(store_script_param, ":bride", 1),
	(store_script_param, ":groom", 2),
	(store_script_param, ":elopement", 3),

	(try_begin),
		(eq, ":bride", "trp_player"),
		(assign, ":venue", "$g_encountered_party"),
	(else_try),
		(troop_get_slot, ":venue", ":bride", slot_troop_cur_center),
		##diplomacy start+
		#Ensure there is a venue.
		(lt, ":venue", 1),
		(troop_get_slot, ":venue", ":groom", slot_troop_cur_center),
		##diplomacy end+
	(try_end),

	(store_faction_of_troop, ":groom_faction", ":groom"),


	(try_begin),
		(eq, ":elopement", 0),
		(call_script, "script_add_log_entry", logent_lady_marries_suitor, ":bride", ":venue", ":groom", 0),
	(else_try),
		(call_script, "script_add_log_entry", logent_lady_elopes_with_lord, ":bride", ":venue", ":groom", 0),
	(try_end),

	(str_store_troop_name, s3, ":bride"),
	(str_store_troop_name, s4, ":groom"),
	(str_store_party_name, s5, ":venue"),

	(try_begin),
	##diplomacy start+ this should be globally-visible for notable personages
	#    (this_or_next|is_between, ":groom_faction", kingdoms_begin, kingdoms_end),
	#    (this_or_next|troop_slot_ge, ":groom", slot_troop_met, 1),
	#    (troop_slot_ge, ":bride", slot_troop_met, 1),
		(display_log_message, "str_s3_marries_s4_at_s5"),
	#(else_try),
    #    (eq, "$cheat_mode", 1),
	#    (display_message, "str_s3_marries_s4_at_s5"),
	##diplomacy end+
    (try_end),

	(troop_set_slot, ":bride", slot_troop_spouse, ":groom"),
	(troop_set_slot, ":groom", slot_troop_spouse, ":bride"),

	#Break groom's romantic relations
	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_set_slot, ":groom", ":love_interest_slot", 0),
	(try_end),

	#Break bride's romantic relations
	(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_slot_eq, ":active_npc", ":love_interest_slot", ":bride"),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":bride", ":active_npc"),
		(try_end),
	(try_end),



	(troop_set_slot, ":bride", slot_troop_betrothed, -1),
	(troop_set_slot, ":groom", slot_troop_betrothed, -1),



    #change relations with family
	##diplomacy start+ Include kingdom ladies
	#(try_for_range, ":family_member", lords_begin, lords_end),
	(try_for_range, ":family_member", heroes_begin, heroes_end),
		(neq, ":family_member", ":bride"),
		(neq, ":family_member", ":groom"),
	##diplomacy end+
		(call_script, "script_troop_get_family_relation_to_troop", ":bride", ":family_member"),
		(gt, reg0, 0),
		(store_div, ":family_relation_boost", reg0, 3),
		(try_begin),
			(eq, ":elopement", 1),
			(val_mul, ":family_relation_boost", -2),
		(try_end),
		##diplomacy start+ Fix error!  Change relation between groom and family member, not groom and bride.
		#(call_script, "script_troop_change_relation_with_troop", ":groom", ":bride", ":family_relation_boost"),
			(call_script, "script_troop_change_relation_with_troop", ":groom", ":family_member", ":family_relation_boost"),
		##diplomacy end+
		(val_add, "$total_courtship_quarrel_changes", ":family_relation_boost"),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":groom", "trp_player"),
			(eq, ":bride", "trp_player"),
		##diplomacy start+ fix bug where player didn't get right to rule
		(call_script, "script_change_player_right_to_rule", 15),##one argument, not two
		##diplomacy end+
	(try_end),


	(try_begin),
		(eq, ":groom", "trp_player"),
		(check_quest_active, "qst_wed_betrothed"),
		(call_script, "script_succeed_quest", "qst_wed_betrothed"),
		(call_script, "script_end_quest", "qst_wed_betrothed"),
	(try_end),


	(try_begin),
		(check_quest_active, "qst_visit_lady"),
		(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, ":bride"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),


	(try_begin),
		(eq, ":groom", "trp_player"),
		(neq, "$g_polygamy", 1),
		(check_quest_active, "qst_visit_lady"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),
	(try_begin),
		(eq, ":groom", "trp_player"),
		(neq, "$g_polygamy", 1),
		(check_quest_active, "qst_duel_courtship_rival"),
		(call_script, "script_abort_quest", "qst_duel_courtship_rival", 0),
	(try_end),


	(try_begin),
		(eq, ":bride", "trp_player"),
	    (call_script, "script_player_join_faction", ":groom_faction"),
		(assign, "$player_has_homage", 1),
	(else_try),
		(eq, ":groom", "trp_player"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!} DEBUG - {s4} faction change in marriage case 5"),
		(try_end),
		(troop_set_faction, ":bride", "$players_kingdom"),
        (call_script, "script_troop_set_title_according_to_faction", ":bride", "$players_kingdom"),
	(else_try),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 6"),
		(try_end),

		(troop_set_faction, ":bride", ":groom_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":bride", ":groom_faction"),
	(try_end),

    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),
        (unlock_achievement, ACHIEVEMENT_HAPPILY_EVER_AFTER),
		(try_begin),
			(eq, ":elopement", 1),
			(unlock_achievement, ACHIEVEMENT_HEART_BREAKER),
		(try_end),
    (try_end),



    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),

        (try_begin),
            (eq, ":elopement", 0),
            (call_script, "script_start_wedding_cutscene", ":groom", ":bride"),
        (else_try), #dckplmc: elope
             (assign, "$g_wedding_groom_troop", ":groom"),
             (assign, "$g_wedding_bride_troop", ":bride"),
             (assign, "$g_wedding_brides_dad_troop", "trp_nurse_for_lady"),
             (assign, "$g_wedding_bishop_troop", "trp_temporary_minister"),

             (modify_visitors_at_site,"scn_wedding"),
             (reset_visitors,0),
             (set_visitor, 0, ":groom"),
             (set_visitor, 1, ":bride"),
             (set_visitor, 2, "trp_nurse_for_lady"),
             (set_visitor, 3, "trp_temporary_minister"),
             (set_jump_mission,"mt_wedding"),
             (jump_to_scene,"scn_wedding"),
             (change_screen_mission),
         (try_end),
    (try_end),
	]),


    #script_npc_decision_checklist_party_ai
("npc_decision_checklist_male_guardian_assess_suitor", #parameters from dialog
	[
	(store_script_param, ":lord", 1),
	(store_script_param, ":suitor", 2),

	(troop_get_slot, ":lord_reputation", ":lord", slot_lord_reputation_type),
	(store_faction_of_troop, ":lord_faction", ":lord"),

	(try_begin),
		(eq, ":suitor", "trp_player"),
		(assign, ":suitor_faction", "$players_kingdom"),
	(else_try),
		(store_faction_of_troop, ":suitor_faction", ":suitor"),
	(try_end),
	(store_relation, ":faction_relation_with_suitor", ":lord_faction", ":suitor_faction"),

	(call_script, "script_troop_get_relation_with_troop", ":lord", ":suitor"),
	(assign, ":lord_suitor_relation", reg0),



	(troop_get_slot, ":suitor_renown", ":suitor", slot_troop_renown),


	(assign, ":competitor_found", -1),

	(try_begin),
		(eq, ":suitor", "trp_player"),
		(gt, "$marriage_candidate", 0),

		(try_for_range, ":competitor", lords_begin, lords_end),
			(store_faction_of_troop, ":competitor_faction", ":competitor"),
			(eq, ":competitor_faction", ":lord_faction"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_1, "$marriage_candidate"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_2, "$marriage_candidate"),
				(troop_slot_eq, ":competitor", slot_troop_love_interest_3, "$marriage_candidate"),

			(call_script, "script_troop_get_relation_with_troop", ":competitor", ":lord"),
			(gt, reg0, 5),

			(troop_slot_ge, ":competitor", slot_troop_renown, ":suitor_renown"),  #higher renown than player

			(assign, ":competitor_found", ":competitor"),
			(str_store_troop_name, s14, ":competitor"),
			(str_store_troop_name, s16, "$marriage_candidate"),
		(try_end),
	(try_end),

	#renown
	(try_begin),
		(lt, ":suitor_renown", 50),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
		(assign, ":explainer_string", "str_excuse_me_how_can_you_possibly_imagine_yourself_worthy_to_marry_into_our_family"),
		(assign, ":result", -3),
	(else_try),
		(lt, ":suitor_renown", 50),
		(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),

		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction_fight_hard_count_your_dinars_and_perhaps_some_day_in_the_future_we_may_speak_of_such_things_my_good_man"),
		(assign, ":result", -1),
	(else_try),
		(lt, ":suitor_renown", 50),

		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction"),
		(assign, ":result", -2),

	(else_try),
		(lt, ":suitor_renown", 200),
		(neg|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
		(assign, ":explainer_string", "str_it_is_too_early_for_you_to_be_speaking_of_such_things_you_are_still_making_your_mark_in_the_world"),

		(assign, ":result", -1),

	(else_try), #wrong faction
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(str_store_faction_name, s4, ":lord_faction"),
		(this_or_next|eq, ":lord_reputation", lrep_quarrelsome),
			(eq, ":lord_reputation", lrep_debauched),
		(assign, ":explainer_string", "str_you_dont_serve_the_s4_so_id_say_no_one_day_we_may_be_at_war_and_i_prefer_not_to_have_to_kill_my_inlaws_if_at_all_possible"),

		(assign, ":result", -1),

	(else_try),
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(neq, ":lord_reputation", lrep_goodnatured),
		(neq, ":lord_reputation", lrep_cunning),

		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),

		(assign, ":result", -1),
	(else_try),
		(eq, ":suitor", "trp_player"),
		(lt, ":faction_relation_with_suitor", 0),

		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),

		(assign, ":result", -1),

	(else_try),
		(eq, ":suitor", "trp_player"),
		(neq, "$player_has_homage", 1),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),

		(assign, ":explainer_string", "str_as_you_are_not_a_pledged_vassal_of_our_liege_with_the_right_to_hold_land_i_must_refuse_your_request_to_marry_into_our_family"),

		(assign, ":result", -1),
	(else_try),
		(gt, ":competitor_found", -1),

		(this_or_next|eq, ":lord_reputation", lrep_selfrighteous),
		(this_or_next|eq, ":lord_reputation", lrep_debauched),
		(this_or_next|eq, ":lord_reputation", lrep_martial),
			(eq, ":lord_reputation", lrep_quarrelsome),

		(assign, ":explainer_string",	"str_look_here_lad__the_young_s14_has_been_paying_court_to_s16_and_youll_have_to_admit__hes_a_finer_catch_for_her_than_you_so_lets_have_no_more_of_this_talk_shall_we"),
		(assign, ":result", -1),

	(else_try),
		(lt, ":lord_suitor_relation", -4),



		(assign, ":explainer_string", "str_i_do_not_care_for_you_sir_and_i_consider_it_my_duty_to_protect_the_ladies_of_my_household_from_undesirable_suitors"),
		(assign, ":result", -3),
	(else_try),
		(lt, ":lord_suitor_relation", 5),

		(assign, ":explainer_string",	"str_hmm_young_girls_may_easily_be_led_astray_so_out_of_a_sense_of_duty_to_the_ladies_of_my_household_i_think_i_would_like_to_get_to_know_you_a_bit_better_we_may_speak_of_this_at_a_later_date"),
		(assign, ":result", -1),
	(else_try),

		(assign, ":explainer_string",	"str_you_may_indeed_make_a_fine_match_for_the_young_mistress"),
		(assign, ":result", 1),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":explainer_string"),

	]),

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
	),


#	(
#	"npc_decision_checklist_king_chooses_lord_for_center",
#	[
#	(store_script_param, ":center", 1),

#	(store_faction_of_party, ":faction", ":center"),
#	(faction_get_slot, ":king", ":faction", slot_faction_leader),

#	(assign, ":total_renown_in_faction"),
#	(try_for_range, ":lord_iterator", active_npcs_including_player_begin, active_npcs_end),
#		(assign, ":lord", ":lord_iterator"),
#		(store_faction_of_troop, ":lord_faction", ":lord"),
#		(try_begin),
#			(eq, ":lord_iterator", "trp_kingdom_heroes_including_player_begin"),
#			(assign, ":lord", "trp_player"),
#			(assign, ":lord_faction", "$players_kingdom"),
#		(try_end),
#		(troop_get_slot, ":renown", ":lord", slot_troop_renown),
#		(val_add, ":total_renown_in_faction", ":renown"),

#		(troop_set_slot, ":lord", slot_troop_temp_slot, 0),
#	(try_end),

#	(assign, ":total_property_points_in_faction"),
#	(try_for_range, ":village", villages_begin, villages_end),

#	(try_end),



#	(try_begin),

	#I needed it for myself

	#The one who captured it was suitably deserving

	#I had not sufficiently recognized Lord X for his service

#	(try_end),


#	]),



	("courtship_poem_reactions", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":poem", 2),

	(troop_get_slot, ":lady_reputation", ":lady", slot_lord_reputation_type),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":poem"),
		(assign, reg5, ":lady_reputation"),
		(display_message, "str_poem_choice_reg4_lady_rep_reg5"),
	(try_end),

	(try_begin), #conventional ++, ambitious -, adventurous -
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_ah__kais_and_layali__such_a_sad_tale_many_a_time_has_it_been_recounted_for_my_family_by_the_wandering_poets_who_come_to_our_home_and_it_has_never_failed_to_bring_tears_to_our_eyes"),
		(assign, ":result", 5),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_kais_and_layali_three_hundred_stanzas_of_pathetic_sniveling_if_you_ask_me_if_kais_wanted_to_escape_heartbreak_he_should_have_learned_to_live_within_his_station_and_not_yearn_for_what_he_cannot_have"),
		(assign, ":result", 0),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_kais_and_layali_no_one_should_ever_have_written_such_a_sad_poem_if_it_was_the_destiny_of_kais_and_layali_to_be_together_than_their_love_should_have_conquered_all_obstacles"),
		(assign, ":result", 1),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
#		moralizing and adventurous
		(str_store_string, s11, "str_ah_kais_and_layali_a_very_old_standby_but_moving_in_its_way"),
		(assign, ":result", 3),
	#Heroic
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_such_happy_times_in_which_our_ancestors_lived_women_like_kara_could_venture_out_into_the_world_like_men_win_a_name_for_themselves_and_not_linger_in_their_husbands_shadow"),
		(assign, ":result", 5),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_ah_the_saga_of_helgered_and_kara_now_there_was_a_lady_who_knew_what_she_wanted_and_was_not_afraid_to_obtain_it"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_a_terrible_tale__but_it_speaks_of_a_very_great_love_if_she_were_willing_to_make_war_on_her_own_family"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_as_i_recall_kara_valued_her_own_base_passions_over_duty_to_her_family_that_she_made_war_on_her_own_father_i_have_no_time_for_a_poem_which_praises_such_a_woman"),
		(assign, ":result", 0),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_how_could_a_woman_don_armor_and_carry_a_sword_how_could_a_man_love_so_ungentle_a_creature"),
		(assign, ":result", 0),
	#Comic
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_conversation_in_the_garden_i_cannot_understand_the_lady_in_that_poem_if_she_loves_the_man_why_does_she_tease_him_so"),
		(assign, ":result", 0),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_conversation_in_the_garden_let_us_see__it_is_morally_unedifying_it_exalts_deception_it_ends_with_a_maiden_surrendering_to_her_base_passions_and_yet_i_cannot_help_but_find_it_charming_perhaps_because_it_tells_us_that_love_need_not_be_tragic_to_be_memorable"),
		(assign, ":result", 1),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_conversation_in_the_garden_now_that_is_a_tale_every_lady_should_know_by_heart_to_learn_the_subtleties_of_the_politics_she_must_practice"),
		(assign, ":result", 5),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		#adventurous, conventional
		(str_store_string, s11, "str_a_conversation_in_the_garden_it_is_droll_i_suppose__although_there_is_nothing_there_that_truly_stirs_my_soul"),
		(assign, ":result", 3),

	#Allegoric
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_the_lady_sits_within_doing_nothing_while_the_man_is_the_one_who_strives_and_achieves_i_have_enough_of_that_in_my_daily_life_why_listen_to_poems_about_it"),
		(assign, ":result", 0),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(this_or_next|eq, ":lady_reputation", lrep_conventional),
			(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_an_uplifting_tribute_to_the_separate_virtues_of_man_and_woman"),
		(assign, ":result", 3),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_but_although_it_is_a_fine_tale_of_virtues_it_speaks_nothing_of_passion"),
		(assign, ":result", 1),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_a_sermon_dressed_up_as_a_love_poem_if_you_ask_me"),
		(assign, ":result", 1),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_hearts_desire_ah_such_a_beautiful_account_of_the_perfect_perfect_love_to_love_like_that_must_be_to_truly_know_rapture"),
		(assign, ":result", 4),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_hearts_desire_silly_if_you_ask_me_if_the_poet_desires_a_lady_then_he_should_endeavor_to_win_her__and_not_dress_up_his_desire_with_a_pretense_of_piety"),
		(assign, ":result", 0),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_hearts_desire_hmm__it_is_an_interesting_exploration_of_earthly_and_divine_love_it_does_speak_of_the_spiritual_quest_which_brings_out_the_best_in_man_but_i_wonder_if_the_poet_has_not_confused_his_yearning_for_higher_things_with_his_baser_passions"),
		(assign, ":result", 2),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(str_store_string, s11, "str_a_hearts_desire_oh_yes__it_is_very_worthy_and_philosophical_but_if_i_am_to_listen_to_a_bard_strum_a_lute_for_three_hours_i_personally_prefer_there_to_be_a_bit_of_a_story"),
		(assign, ":result", 1),
	(try_end),


	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":result"),
		(display_message, "str_result_reg4_string_s11"),
	(try_end),


	(assign, reg0, ":result"),

	]),

	("internal_politics_rate_feast_to_s9",
	[
	(store_script_param, ":householder", 1),
	(store_script_param, ":num_servings", 2),
#	(store_script_param, ":faction", 3),
	(store_script_param, ":consume_items", 4),

	(val_max, ":num_servings", 1),

	(try_for_range, ":item", trade_goods_begin, trade_goods_end),
		(item_set_slot, ":item", slot_item_amount_available, 0), #had no "item"
	(try_end),

	(troop_get_inventory_capacity, ":capacity", ":householder"),
	(try_for_range, ":inventory_slot", ek_food + 1, ":capacity"), #SB : skip equipment
		(troop_get_inventory_slot, ":item", ":householder", ":inventory_slot"),
		(is_between, ":item", trade_goods_begin, trade_goods_end),
	    (troop_inventory_slot_get_item_amount, ":slot_amount", ":householder", ":inventory_slot"),
        #SB : TODO : evaluate quality of food, for now just make sure it's not rotten
        (troop_get_inventory_slot_modifier, ":imod", ":householder", ":inventory_slot"),
        (neq, ":imod", imod_rotten),
		(item_get_slot, ":item_amount", ":item", slot_item_amount_available),
		(val_add, ":item_amount", ":slot_amount"),
		(item_set_slot, ":item", slot_item_amount_available, ":item_amount"),
	(try_end),
	#food
	(assign, ":food_amount", 0),
	(assign, ":food_variety", 0),

	(store_div, ":servings_div_by_12", ":num_servings", 12),
	(try_for_range, ":food_item", food_begin, food_end),
		(item_get_slot, ":food_in_slot", ":food_item", slot_item_amount_available),
		(val_add, ":food_amount", ":food_in_slot"),


##		(str_store_item_name, s4, ":food_item"),
##		(assign, reg3, ":food_in_slot"),
##		(assign, reg5, ":servings_div_by_12"),
##		(display_message, "str_reg3_units_of_s4_for_reg5_guests_and_retinue"),


		(ge, ":food_in_slot", ":servings_div_by_12"),
		(val_add, ":food_variety", 1),
	(try_end),

	(val_mul, ":food_amount", 100),
	(val_div, ":food_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":food_amount", 100),

	(val_mul, ":food_variety", 85), #1 to 100 for each
	(val_div, ":food_variety", 10),
	(val_min, ":food_variety", 100),

	#drink
	(assign, ":drink_amount", 0),
	(assign, ":drink_variety", 0),
	(store_div, ":servings_div_by_4", ":num_servings", 4),
	(try_for_range, ":drink_iterator", "itm_wine", "itm_smoked_fish"),
		(assign, ":drink_item", ":drink_iterator"),
		(item_get_slot, ":drink_in_slot", ":drink_item", slot_item_amount_available),

		(val_add, ":drink_amount", ":drink_in_slot"),

		(ge, ":drink_in_slot", ":servings_div_by_4"),
		(val_add, ":drink_variety", 1),
	(try_end),

	(val_mul, ":drink_amount", 200), #amount needed is 50% of the number of guests
	(val_max, ":num_servings", 1),

	(val_div, ":drink_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":drink_amount", 100),
	(val_mul, ":drink_variety", 50), #1 to 100 for each

	#in the future, it might be worthwhile to add different varieties of spices
	(item_get_slot, ":spice_amount", "itm_spice", slot_item_amount_available),
	(store_mul, ":spice_percentage", ":spice_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":spice_amount", ":servings_div_by_12"),
	(val_min, ":spice_percentage", 100),
##	(assign, reg3, ":spice_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":spice_percentage"),
##	(display_message, "str_reg3_units_of_spice_of_reg5_to_be_consumed"),

	#oil availability. In the future, this may become an "atmospherics" category, including incenses
	(item_get_slot, ":oil_amount", "itm_oil", slot_item_amount_available),
	(store_mul, ":oil_percentage", ":oil_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":oil_amount", ":servings_div_by_12"),
	(val_min, ":oil_percentage", 100),
##	(assign, reg3, ":oil_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":oil_percentage"),
##	(display_message, "str_reg3_units_of_oil_of_reg5_to_be_consumed"),

    #SB : salt + date fruit probably useful too
	(store_div, ":food_amount_string", ":food_amount", 20),
	(val_add, ":food_amount_string", "str_feast_description"),
	(str_store_string, s8, ":food_amount_string"),
	(str_store_string, s9, "str_of_food_which_must_come_before_everything_else_the_amount_is_s8"),

	(store_div, ":food_variety_string", ":food_variety", 20),
	(val_add, ":food_variety_string", "str_feast_description"),
	(str_store_string, s8, ":food_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),

	(store_div, ":drink_amount_string", ":drink_amount", 20),
	(val_add, ":drink_amount_string", "str_feast_description"),
	(str_store_string, s8, ":drink_amount_string"),
	(str_store_string, s9, "str_s9_of_drink_which_guests_will_expect_in_great_abundance_the_amount_is_s8"),

	(store_div, ":drink_variety_string", ":drink_variety", 20),
	(val_add, ":drink_variety_string", "str_feast_description"),
	(str_store_string, s8, ":drink_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),

	(store_div, ":spice_string", ":spice_percentage", 20),
	(val_add, ":spice_string", "str_feast_description"),
	(str_store_string, s8, ":spice_string"),
	(str_store_string, s9, "str_s9_of_spice_which_is_essential_to_demonstrate_that_we_spare_no_expense_as_hosts_the_amount_is_s8_"),

	(store_div, ":oil_string", ":oil_percentage", 20),
	(val_add, ":oil_string", "str_feast_description"),
	(str_store_string, s8, ":oil_string"),
	(str_store_string, s9, "str_s9_of_oil_which_we_shall_require_to_light_the_lamps_the_amount_is_s8"),

	(store_mul, ":food_amount_cap", ":food_amount", 8),
	(store_add, ":total", ":food_amount", ":food_variety"),
	(val_mul, ":total", 2), #x4
	(val_add, ":total", ":drink_variety"),
	(val_add, ":total", ":drink_amount"), #x6
	(val_add, ":total", ":spice_amount"), #x7
	(val_add, ":total", ":oil_amount"), #x8
	(val_min, ":total", ":food_amount_cap"),
	(val_div, ":total", 8),
	(val_clamp, ":total", 1, 101),
	(store_div, ":total_string", ":total", 20),
	(val_add, ":total_string", "str_feast_description"),
	(str_store_string, s8, ":total_string"),
	(str_store_string, s9, "str_s9_overall_our_table_will_be_considered_s8"),

	(assign, reg0, ":total"), #zero to 100



	(try_begin),
		(eq, ":consume_items", 1),

		(assign, ":num_of_servings_to_serve", ":num_servings"),
		(try_for_range, ":unused", 0, 1999),
			(gt, ":num_of_servings_to_serve", 0),

			(try_for_range, ":item", trade_goods_begin, trade_goods_end),
				(item_set_slot, ":item", slot_item_is_checked, 0),
			(try_end),

			(troop_get_inventory_capacity, ":inv_size", ":householder"),
			(try_for_range, ":i_slot", 0, ":inv_size"),
				(troop_get_inventory_slot, ":item", ":householder", ":i_slot"),
				(this_or_next|eq, ":item", "itm_spice"),
				(this_or_next|eq, ":item", "itm_oil"),
				(this_or_next|eq, ":item", "itm_wine"),
				(this_or_next|eq, ":item", "itm_ale"),
					(is_between, ":item",  food_begin, food_end),
				(item_slot_eq, ":item", slot_item_is_checked, 0),
				(troop_inventory_slot_get_item_amount, ":cur_amount", ":householder", ":i_slot"),
				(gt, ":cur_amount", 0),

				(val_sub, ":cur_amount", 1),
				(troop_inventory_slot_set_item_amount, ":householder", ":i_slot", ":cur_amount"),
				(val_sub, ":num_of_servings_to_serve", 1),
				(item_set_slot, ":item", slot_item_is_checked, 1),
			(try_end),
                ##diplomacy start+ Fix Native bug: "try_begin" to "try_end"
		#(try_begin),
                (try_end),
                ##diplomacy end+
	(try_end),
	]),


		("cf_prisoner_offered_parole",
	[
	  (store_script_param, ":prisoner", 1),

	  (eq, 1, 0), #disabled, this will always return false

	  (troop_get_slot, ":captor_party", ":prisoner", slot_troop_prisoner_of_party),
	  (party_is_active, ":captor_party"),
	  (is_between, ":captor_party", walled_centers_begin, walled_centers_end),
	  (party_get_slot, ":captor", ":captor_party", slot_town_lord),

	  (troop_get_slot, ":prisoner_rep", ":prisoner", slot_lord_reputation_type),
	  (troop_get_slot, ":captor_rep", ":captor", slot_lord_reputation_type),

	  (neq, ":prisoner_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_debauched),
	  (neq, ":captor_rep", lrep_quarrelsome),

     #Prisoner is a noble, or lord is goodnatured
    (this_or_next|eq, ":captor_rep", lrep_goodnatured),
    (this_or_next|troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_hero),
    (troop_slot_eq, ":prisoner", slot_troop_occupation, slto_kingdom_lady),

	(call_script, "script_troop_get_relation_with_troop", ":captor", ":prisoner"),
##	(display_message, "str_relation_of_prisoner_with_captor_is_reg0"),
	(ge, reg0, -10),
	]),

	("neutral_behavior_in_fight",
	[
      (get_player_agent_no, ":player_agent"),
      (agent_get_position, pos3, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),

      (try_begin),
        (gt, "$g_main_attacker_agent", 0),
        (agent_get_team, ":attacker_team_no", "$g_main_attacker_agent"),
        (agent_get_position, pos5, "$g_main_attacker_agent"),
      (else_try),
        (eq, ":attacker_team_no", -1),
        (agent_get_position, pos5, ":player_agent"),
      (try_end),

      (set_fixed_point_multiplier, 100),

      (try_for_agents, ":agent"),
        (agent_get_team, ":other_team", ":agent"),
        (neq, ":other_team", ":attacker_team_no"),
        (neq, ":other_team", ":player_team"),

        (agent_get_troop_id, ":troop_id", ":agent"),
        #SB : better range checks
        (this_or_next|eq, ":troop_id", "trp_farmer"), #farmers are "neutral"
        (neg|is_between, ":troop_id", soldiers_begin, soldiers_end), #but lie within this range
        (troop_slot_eq, ":troop_id", slot_troop_mission_participation, mp_unaware), #neutral prisoners?

        (agent_get_position, pos4, ":agent"),

        (assign, ":best_position_score", 0),
        (assign, ":best_position", -1),

        (try_begin),
          (neg|agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is running away
          (agent_get_slot, ":target_entry_point_plus_one",  ":agent", slot_agent_is_running_away),
          (store_sub, ":target_entry_point", ":target_entry_point_plus_one", 1),
          (entry_point_get_position, pos6, ":target_entry_point"),
          (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
          (lt, ":agent_distance_to_target", 100),
          (agent_set_slot, ":agent", slot_agent_is_running_away, 0),
        (try_end),

        (agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is not already running away

        (try_begin), #stand in place
          (get_distance_between_positions, ":distance", pos4, pos5),
          (get_distance_between_positions, ":distance_to_player", pos4, pos3),

          (val_min, ":distance", ":distance_to_player"),

          (this_or_next|gt, ":distance", 700), #7 meters away from main belligerents
          (main_hero_fallen),

          (agent_set_scripted_destination, ":agent", pos4),
        (else_try), #get out of the way
          (try_for_range, ":target_entry_point", 0, 64),
            (neg|entry_point_is_auto_generated, ":target_entry_point"),
            (entry_point_get_position, pos6, ":target_entry_point"),
            (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
            (get_distance_between_positions, ":player_distance_to_target", pos6, pos3),
            (store_sub, ":position_score", ":player_distance_to_target", ":agent_distance_to_target"),
            (ge, ":position_score", 0),
            (try_begin),
              (ge, ":agent_distance_to_target", 2000),
              (store_sub, ":extra_distance", ":agent_distance_to_target", 2000),
              (val_min, ":extra_distance", 1000),
              (val_min, ":agent_distance_to_target", 2000), #if more than 10 meters assume it is 10 meters far while calculating best run away target
              (val_sub, ":agent_distance_to_target", ":extra_distance"),
            (try_end),
            (val_mul, ":position_score", ":agent_distance_to_target"),
            (try_begin),
              (ge, ":position_score", ":best_position_score"),
              (assign, ":best_position_score", ":position_score"),
              (assign, ":best_position", ":target_entry_point"),
            (try_end),
          (try_end),

          (try_begin),
            (ge, ":best_position", 0),
            (entry_point_get_position, pos6, ":best_position"),
            (agent_set_speed_limit, ":agent", 10),
            (agent_set_scripted_destination, ":agent", pos6),
            (store_add, ":best_position_plus_one", ":best_position", 1),
            (agent_set_slot, ":agent", slot_agent_is_running_away, ":best_position_plus_one"),
          (try_end),
        (try_end),
	  (try_end),
	]),

	("party_inflict_attrition", #parameters from dialog
	[
	(store_script_param, ":party", 1),
	(store_script_param, ":attrition_rate", 2),
#	(store_script_param, ":attrition_type", 3), #1 = desertion, 2 = sickness

    (party_clear, "p_temp_casualties"),

	(party_get_num_companion_stacks, ":num_stacks", ":party"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", ":party", ":stack"),
		(neg|troop_is_hero, ":troop_type"),
		(party_stack_get_size, ":size", ":party", ":stack"),
		(store_mul, ":casualties_x_100", ":attrition_rate", ":size"),
		(store_div, ":casualties", ":casualties_x_100", 100),
		(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),

		(store_mul, ":subtractor", ":casualties", 100),
		(store_sub, ":chance_of_additional_casualty", ":casualties_x_100", ":subtractor"),

		(try_begin),
			(gt, ":chance_of_additional_casualty", 0),
			(store_random_in_range, ":random", 0, 100),
			(lt, ":random", ":chance_of_additional_casualty"),
			(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),
		(try_end),

#		(try_begin),
#			(eq, "$cheat_mode", 1),
#			(str_store_party_name, s7, ":party"),
#           		...
#		(try_end),
	(try_end),

	#take temp casualties from main party
	(party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", "p_temp_casualties", ":stack"),
		(party_stack_get_size, ":size", "p_temp_casualties", ":stack"),
		(party_remove_members, ":party", ":troop_type", ":size"),

		(eq, "$cheat_mode", 1),
		(assign, reg3, ":size"),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, ":party"),
#		(display_message, "str_s5_suffers_attrition_reg3_x_s4"),
		(str_store_string, s65, "str_s5_suffers_attrition_reg3_x_s4"),
		(display_message, "str_s65"),
		(try_begin),
			(eq, "$debug_message_in_queue", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, "$debug_message_in_queue", 1),
		(try_end),
	(try_end),

	]),


##diplomacy start+ (documentation only)
#
# Registers changed:
#   reg4 - (sometimes, cheat only) current troop rumor of :object_1 or :object_2
#
# String registers changed:
#    s10 - speaker name
#    s11 - the third argument
#     s1 - the date
#     s5 - str_s10_said_on_s1_s11__
#     s3 - (sometimes, cheat only) the troop name of :object_1 or :object_2
#
#
# Diplomacy+ mod change:
# - Use reg4 to contain the gender of the subject of a rumor string
##diplomacy end+ (documentation only)
	("add_rumor_string_to_troop_notes", #parameters from dialog
	[
      (store_script_param, ":object_1", 1),
      (store_script_param, ":object_2", 2),
      (store_script_param, ":string", 3),

      (str_store_troop_name, s10, "$g_talk_troop"),
      (str_store_string_reg, s11, ":string"),

      (store_current_hours, ":hours"),
      (call_script, "script_game_get_date_text", 0, ":hours"),

      (str_store_string, s5, "str_s10_said_on_s1_s11__"),

      (try_begin),
        (is_between, ":object_1", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_1", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
        # Lav modifications start (custom lord notes)
                  (neg|is_between, ":current_rumor_note", 3, 15), # Was 16 in original Native, thus using notes slot #15 as well. Now it will leave notes slot #15 for custom notes.
        # Lav modifications end (custom lord notes)
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_1", slot_troop_current_rumor, ":current_rumor_note"),

        (add_troop_note_from_sreg, ":object_1", ":current_rumor_note", s5, 0), #troop, note slot, string, show

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_1"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),

      (try_begin),
        (is_between, ":object_2", active_npcs_begin, kingdom_ladies_end),
        (troop_get_slot, ":current_rumor_note", ":object_2", slot_troop_current_rumor),
        (val_add, ":current_rumor_note", 1),
        (try_begin),
# Lav modifications start (custom lord notes)
          (neg|is_between, ":current_rumor_note", 3, 15), # Was 16 in original Native, thus using notes slot #15 as well. Now it will leave notes slot #15 for custom notes.
# Lav modifications end (custom lord notes)
          (assign, ":current_rumor_note", 3),
        (try_end),
        (troop_set_slot, ":object_2", slot_troop_current_rumor, ":current_rumor_note"),

        (add_troop_note_from_sreg, ":object_2", ":current_rumor_note", s5, 0), #troop, note slot, string, show

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, s3, ":object_2"),
          (assign, reg4, ":current_rumor_note"),
          (display_message, "str_rumor_note_to_s3s_slot_reg4_s5"),
        (try_end),
      (try_end),
	]),

	("character_can_wed_character", #empty now, but might want to add mid-game
	[
	]),

	("troop_change_career", #empty now, but might want to add mid-game
	[
	]),

	("lord_find_alternative_faction", #Also, make it so that lords will try to keep at least one center unassigned
	[
	  (store_script_param, ":troop_no", 1),
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),

	  (assign, ":new_faction", -1),
	  (assign, ":score_to_beat", -5),
	  ##diplomacy start+
	  (troop_get_slot, ":true_original_faction", ":troop_no", slot_troop_original_faction),#not necessarily ":orig_faction"
	  (try_begin),
	     (neg|is_between, ":true_original_faction", kingdoms_begin, kingdoms_end),
	     (troop_get_slot, reg0, ":troop_no", slot_troop_home),
	     (is_between, reg0, centers_begin, centers_end),
	     (party_get_slot, reg0, reg0, slot_center_original_faction),
	     (gt, reg0, 0),
	     (assign, ":true_original_faction", reg0),
	  (try_end),
	  (assign, ":original_culture", -2),
	  (try_begin),
	     (gt, ":true_original_faction", 0),
		 (faction_get_slot, ":original_culture", ":true_original_faction", slot_faction_culture),
		 (lt, ":original_culture", 1),
		 (assign, ":original_culture", ":true_original_faction"),
	  (try_end),
	  ##diplomacy end+

	  #Factions with an available center
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
	    (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
	    (store_faction_of_party, ":center_faction", ":center_no"),
	    ##diplomacy start+ In Warband 1.142 / 1.143, this variable was added.
	    #To make certain kinds of mistakes or saved-game issues less likely,
	    #instead of checking for value 1 I'll check if the value matches the troop.
	    (this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
	    ##diplomacy end+
	    (neq, ":center_faction", ":orig_faction"),
	    (faction_get_slot, ":liege", ":center_faction", slot_faction_leader),
	    (this_or_next|neq, ":liege", "trp_player"),
	    (ge, "$player_right_to_rule", 25),
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	    (assign, ":liege_relation", reg0),

		##diplomacy start+
		(try_begin),
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
			#If behavioral changes are enabled, bias heavily towards joining the
			#faction that contains your home (if you have one), or that has the
			#greatest cultural similarity.
			(ge, reg0, 0),
			(try_begin),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_original_faction, ":center_faction"),
				(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
					(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
				(val_add, ":liege_relation", 20),
			(else_try),
				(gt, ":true_original_faction", 0),
				(party_slot_eq, ":center_no", slot_center_original_faction, ":true_original_faction"),
				(val_add, ":liege_relation", 5),
			(else_try),
				(gt, ":original_culture", 0),
				(faction_slot_eq, ":center_faction", slot_faction_culture, ":original_culture"),
				(val_add, ":liege_relation", 5),
			(try_end),
		(try_end),
		##diplomacy end+

	    (gt, ":liege_relation", ":score_to_beat"),
	    (assign, ":new_faction", ":center_faction"),
	    (assign, ":score_to_beat", ":liege_relation"),
	  (try_end),

	  #Factions without an available center
	  (try_begin),
	    (eq, ":new_faction", -1),
	    (assign, ":score_to_beat", 0),
	     #diplomacy start+
	     #If AI changes are explicitly enabled, slightly ease the requirements for entry.
	     (try_begin),
		    (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
	        (assign, ":score_to_beat", -5),
	     (try_end),
		 (store_add, ":min_acceptable_score", ":score_to_beat", 1),#used below
	     ##diplomacy end+

	    (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	      (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	      (faction_get_slot, ":liege", ":kingdom", slot_faction_leader),
	      (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
	      (assign, ":liege_relation", reg0),

		  ##diplomacy start+
		  (try_begin),
				#In Warband 1.142 / 1.143, this variable was added.
				#To make certain kinds of mistakes or saved-game issues less likely,
				#instead of checking for value 1 I'll check if the value matches the troop.
				(this_or_next|eq, "$g_give_advantage_to_original_faction", ":troop_no"),
				(neq, ":kingdom", ":orig_faction"),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
				#If behavioral changes are enabled, base your decision in part
				#on how many friends you have in the faction.
				(ge, reg0, ":min_acceptable_score"),
				(try_for_range, ":lord", heroes_begin, heroes_end),
					(troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
					(neq, ":lord", ":troop_no"),
					(neq, ":lord", ":liege"),
					(store_faction_of_troop, ":lord_faction", ":lord"),
					(eq, ":lord_faction", ":kingdom"),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":lord"),
					(try_begin),
						(ge, reg0, 20),
						(val_add, ":liege_relation", 1),
					(else_try),
						(lt, reg0, -19),
						(val_sub, ":liege_relation", 1),
					(try_end),
				(try_end),
				#Also give a bonus towards rejoining the lord's original faction.
				#if it isn't the one the lord has just left.
				(try_begin),
					(eq, ":true_original_faction", ":kingdom"),
					(val_add, ":liege_relation", 5),
				(else_try),
					#Not the same but similar
					(gt, ":original_culture", 0),
					(faction_slot_eq, ":kingdom", slot_faction_culture, ":original_culture"),
					(val_add, ":liege_relation", 2),
				(try_end),
				#The next bit is to prevent this change from increasing the number of
				#lords who find all kingdoms unacceptable.
				(val_max, ":liege_relation", ":min_acceptable_score"),
		  (try_end),
		  ##diplomacy end+

	      (gt, ":liege_relation", ":score_to_beat"),

	      (assign, ":new_faction", ":kingdom"),
	      (assign, ":score_to_beat", ":liege_relation"),
	    (try_end),
	  (try_end),

	  (assign, reg0, ":new_faction"),
	]),

	("set_up_duel_with_troop", #now the setup is handled through the menu
	[
	  (store_script_param, "$g_duel_troop", 1),
      #SB : change by parameter instead of always one
	  (store_script_param, "$g_start_arena_fight_at_nearest_town", 2),
	  (store_faction_of_troop, ":troop_faction", "$g_duel_troop"),
	  (try_begin),
	    (eq, "$g_start_arena_fight_at_nearest_town", 1),
        # (assign, ":closest_town", -1),
        (assign, ":minimum_dist", 500),
        (try_for_range, ":cur_town", walled_centers_begin, walled_centers_end),
          (store_distance_to_party_from_party, ":dist", ":cur_town", "$g_encountered_party"),
          (lt, ":dist", ":minimum_dist"),
          #make sure it's at least neutral, so we don't fight in an enemy town's arena
          (store_faction_of_party, ":center_faction", ":cur_town"),
          (store_relation, ":relation", ":troop_faction", ":center_faction"),
          (ge, ":relation", 0),
          (assign, ":minimum_dist", ":dist"),
          (assign, "$g_start_arena_fight_at_nearest_town", ":cur_town"),
        (try_end),
	  (try_end),
	  (unlock_achievement, ACHIEVEMENT_PUGNACIOUS_D),
      (jump_to_menu, "mnu_arena_duel_fight"),
	  (finish_mission),

	]),

	("test_player_for_career_and_marriage_incompatability", #empty now, but might want to add mid-game
	[
	#Married to a lord of one faction, while fighting for another
	#Married to one lord while holding a stipend from the king
	]),

	("deduct_casualties_from_garrison", #after a battle in a center, deducts any casualties from "$g_encountered_party"
	[
	##(display_message, "str_totalling_casualties_caused_during_mission"),

	(try_for_agents, ":agent"),
		(agent_get_troop_id, ":troop_type", ":agent"),
		(is_between, ":troop_type", regular_troops_begin, regular_troops_end),

		(neg|agent_is_alive, ":agent"),

		(try_begin), #if troop not present, search for another type which is
			(store_troop_count_companions, ":number", ":troop_type", "$g_encountered_party"),
			(eq, ":number", 0),
			(assign, ":troop_type", 0),
			(try_for_range, ":new_tier", slot_faction_tier_1_troop, slot_faction_tier_5_troop),
			(faction_get_slot, ":troop_type", "$g_encountered_party_faction", ":new_tier"),
				(faction_get_slot, ":new_troop_type", "$g_encountered_party_faction", ":new_tier"),
				(store_troop_count_companions, ":number", ":new_troop_type", "$g_encountered_party"),
				(gt, ":number", 0),
				(assign, ":troop_type", ":new_troop_type"),
			(try_end),
		(try_end),

		(gt, ":troop_type", 0),

		(party_remove_members, "$g_encountered_party", ":troop_type", 1),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, "$g_encountered_party"),
	(try_end),
	]),

	("get_enterprise_prosperity_numerator",
    #reg0: prosperity quantity numerator (denominator is 100) for the given center.
    #      very poor (<30): 50 | poor (30-49): 75 | normal (50-69): 100 | rich (70-89): 150 | very rich (90-100): 200
    #Used so rich towns produce more goods (and earn more) while poor towns produce less.
    # INPUTS:
    #   arg1: center
    [
      (store_script_param, ":center", 1),
      (party_get_slot, ":prosperity", ":center", slot_town_prosperity),
      (try_begin),
        (lt, ":prosperity", 30),
        (assign, reg0, 50),
      (else_try),
        (lt, ":prosperity", 50),
        (assign, reg0, 75),
      (else_try),
        (lt, ":prosperity", 70),
        (assign, reg0, 100),
      (else_try),
        (lt, ":prosperity", 90),
        (assign, reg0, 150),
      (else_try),
        (assign, reg0, 200),
      (try_end),
    ]),

	("process_player_enterprise",
    #reg0: Profit per cycle
	##diplomacy start+
	#Actual documentation of original parameters and outputs.
	# INPUTS:
	#   arg1: item_type
	#   arg2: center
	# OUTPUTS:
    #   reg0:  profit_per_cycle"),
	#   reg1:  final_price_for_total_produced_goods"),
	#   reg2:  final_price_for_total_inputs"),
	#   reg3:  price_of_labor"),
	#   reg4:  final_price_for_single_produced_good"),
	#   reg5:  final_price_for_single_input"),
	#	reg10: final_price_for_secondary_input"),
	#
	# Further, if experimental changes are enabled, modify the price.
	##diplomacy end+
	[
	  (store_script_param, ":item_type", 1),
	  (store_script_param, ":center", 2),

	  (item_get_slot, ":price_of_labor", ":item_type", slot_item_overhead_per_run),

	  (item_get_slot, ":base_price", ":item_type", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":item_type", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_produced_good", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_produced_good", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_outputs_produced", ":item_type", slot_item_output_per_run),
	  (store_mul, ":final_price_for_total_produced_goods", ":number_of_outputs_produced", ":final_price_for_single_produced_good"),

	  (item_get_slot, ":primary_raw_material", ":item_type", slot_item_primary_raw_material),
	  (item_get_slot, ":base_price", ":primary_raw_material", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":primary_raw_material", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		 (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":primary_raw_material", ":center"),
		 (val_max, ":cur_price_modifier", reg0),
	  (try_end),
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_input", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_input", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_inputs_required", ":item_type", slot_item_input_number),
	  (try_begin),
	    (lt, ":number_of_inputs_required", 0),
	    (store_div, ":final_price_for_total_inputs", ":final_price_for_single_input", 2),
	  (else_try),
	    (store_mul, ":final_price_for_total_inputs", ":final_price_for_single_input", ":number_of_inputs_required"),
	  (try_end),

	  (try_begin),
	    (item_slot_ge, ":item_type", slot_item_secondary_raw_material, 1),
	    (item_get_slot, ":secondary_raw_material", ":item_type", slot_item_secondary_raw_material),
	    (item_get_slot, ":base_price", ":secondary_raw_material", slot_item_base_price),
	    (store_sub, ":cur_good_price_slot", ":secondary_raw_material", trade_goods_begin),
	    (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	    (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
		##diplomacy start+
		(try_begin),
	      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		  (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":secondary_raw_material", ":center"),
		  (val_max, ":cur_price_modifier", reg0),
	    (try_end),
	    (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
		##diplomacy end+
		(store_mul, ":final_price_for_secondary_input", ":base_price", ":cur_price_modifier"),#fixes
	    (try_begin),
	      (lt, ":number_of_inputs_required", 0),
	      (val_div, ":final_price_for_secondary_input", 2),
	    (else_try),
	      (val_mul, ":final_price_for_secondary_input", ":number_of_inputs_required"),
	    (try_end),

		##diplomacy start+
	    (val_div, ":final_price_for_secondary_input", average_price_factor),#Replaced "1000" with "average_price_factor"
		##diplomacy end+
	  (else_try),
	    (assign, ":final_price_for_secondary_input", 0),
	  (try_end),

	  #Scale production by town prosperity tier (rich towns produce more, poor towns less; overhead stays fixed)
	  (call_script, "script_get_enterprise_prosperity_numerator", ":center"),
	  (assign, ":prosperity_num", reg0),
	  (val_mul, ":final_price_for_total_produced_goods", ":prosperity_num"),
	  (val_div, ":final_price_for_total_produced_goods", 100),
	  (val_mul, ":final_price_for_total_inputs", ":prosperity_num"),
	  (val_div, ":final_price_for_total_inputs", 100),
	  (val_mul, ":final_price_for_secondary_input", ":prosperity_num"),
	  (val_div, ":final_price_for_secondary_input", 100),

	  (store_sub, ":profit_per_cycle", ":final_price_for_total_produced_goods", ":final_price_for_total_inputs"),
	  (val_sub, ":profit_per_cycle", ":price_of_labor"),
	  (val_sub, ":profit_per_cycle", ":final_price_for_secondary_input"),

	  (assign, reg0, ":profit_per_cycle"),
	  (assign, reg1, ":final_price_for_total_produced_goods"),
	  (assign, reg2, ":final_price_for_total_inputs"),
	  (assign, reg3, ":price_of_labor"),
	  (assign, reg4, ":final_price_for_single_produced_good"),
	  (assign, reg5, ":final_price_for_single_input"),
	  (assign, reg10, ":final_price_for_secondary_input"),
	]),

  # script_replace_scene_items_with_spawn_items_before_ms
  # Input: none
  # Output: none
  ("replace_scene_items_with_spawn_items_before_ms",
    [
      (try_for_range, ":item_no", all_items_begin, all_items_end),
        (item_get_type, ":item_type", ":item_no"),
        (neq, ":item_type", itp_type_goods),
        (neq, ":item_type", itp_type_book),
        (scene_item_get_num_instances, ":num_instances", ":item_no"),
        (item_set_slot, ":item_no", slot_item_num_positions, 0),
        (assign, ":num_positions", 0),
        (try_for_range, ":cur_instance", 0, ":num_instances"),
          (scene_item_get_instance, ":scene_item", ":item_no", ":cur_instance"),
          (prop_instance_get_position, "$g_position_to_use_for_replacing_scene_items", ":scene_item"),
          (store_add, ":cur_slot", slot_item_positions_begin, ":num_positions"),
          (item_set_slot, ":item_no", ":cur_slot", "$g_position_to_use_for_replacing_scene_items"),
          (val_add, ":num_positions", 1),
          (val_add, "$g_position_to_use_for_replacing_scene_items", 1),
          (item_set_slot, ":item_no", slot_item_num_positions, ":num_positions"),
        (try_end),
        (replace_scene_items_with_scene_props, ":item_no", "spr_empty"),
      (try_end),
     ]),

  # script_replace_scene_items_with_spawn_items_after_ms
  # Input: none
  # Output: none
  ("replace_scene_items_with_spawn_items_after_ms",
    [
      (try_for_range, ":item_no", all_items_begin, all_items_end),
        (item_get_slot,  ":num_positions", ":item_no", slot_item_num_positions),
        (item_get_type, ":item_type",":item_no"),
        (try_for_range, ":cur_position", 0, ":num_positions"),
          (store_add, ":cur_slot", slot_item_positions_begin, ":cur_position"),
          (item_get_slot, ":pos_no", ":item_no", ":cur_slot"),
          (set_spawn_position, ":pos_no"),
          (try_begin),
            (eq, ":item_type", itp_type_horse),
            (spawn_horse, ":item_no"),
          (else_try),
            (spawn_item, ":item_no", 0),
          (try_end),
        (try_end),
      (try_end),
     ]),

  # script_cf_is_melee_weapon_for_tutorial
  # Input: arg1 = item_no
  # Output: none (can fail)
  ("cf_is_melee_weapon_for_tutorial",
    [
      (store_script_param, ":item_no", 1),
      (assign, ":result", 0),
      (try_begin),
        (this_or_next|eq, ":item_no", "itm_quarter_staff"),
        (eq, ":item_no", "itm_practice_sword"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
     ]),

  # script_iterate_pointer_arrow
  # Input: none
  # Output: none
  ("iterate_pointer_arrow",
    [
      (store_mission_timer_a_msec, ":cur_time"),
      (try_begin),
        (assign, ":up_down", ":cur_time"),
        (assign, ":turn_around", ":cur_time"),
        (val_mod, ":up_down", 1080),
        (val_div, ":up_down", 3),
        (scene_prop_get_instance, ":prop_instance", "spr_pointer_arrow", 0),
        (prop_instance_get_position, pos0, ":prop_instance"),
        (position_set_z_to_ground_level, pos0),
        (position_move_z, pos0, "$g_pointer_arrow_height_adder", 1),
        (set_fixed_point_multiplier, 100),
        (val_mul, ":up_down", 100),
        (store_sin, ":up_down_sin", ":up_down"),
        (position_move_z, pos0, ":up_down_sin", 1),
        (position_move_z, pos0, 100, 1),
        (val_mod, ":turn_around", 2880),
        (val_div, ":turn_around", 8),
        (init_position, pos1),
        (position_rotate_z, pos1, ":turn_around"),
        (position_copy_rotation, pos0, pos1),
        (prop_instance_set_position, ":prop_instance", pos0),
      (try_end),
     ]),

   ("indict_lord_for_treason",#originally included in simple_triggers. Needed to be moved here to allow player to indict
   [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":faction", 2),

	##diplomacy start+ use gender script
	#(troop_get_type, reg4, ":troop_no"),
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg3", reg3),
	(assign, ":save_reg4", reg4),
	##diplomacy end+

	(try_for_range, ":center", centers_begin, centers_end), #transfer properties to liege
		(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
		(party_set_slot, ":center", slot_town_lord, stl_unassigned),
		###(((removing banner FIX
		(party_set_banner_icon, ":center", 0),
		###)))
	(try_end),

	(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
	(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
	(assign, ":liege_to_lord_relation", reg0),
	(store_sub, ":base_relation_modifier", -150, ":liege_to_lord_relation"),
	(val_div, ":base_relation_modifier", 40),#-1 at -100, -2 at -70, -3 at -30,etc.
	(val_min, ":base_relation_modifier", -1),

    # #SB : redistribute wealth to faction ruler
    (try_begin),
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
    # (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
    # (troop_set_slot, ":troop_no", slot_troop_wealth, 0),
    # (call_script, "script_dplmc_distribute_gold_to_lord_and_holdings", ":cur_wealth", ":faction_leader"), #add to ruler
    (try_end),
	#Indictments, cont: Influence relations
	##diplomacy start+ Alter to include promoted ladies
	##OLD:
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end), #this effects all lords in all factions
	##NEW:
	(try_for_range, ":active_npc", heroes_begin, heroes_end), #this effects all lords in all factions
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(eq, ":faction", ":active_npc_faction"),

		(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":active_npc"),
		(assign, ":family_relation", reg0),

		##diplomacy start+
		(val_max, ":family_relation", 0),
		#Take into account friendship or enmity
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
		(assign, ":liking_relation", reg0),
		(try_begin),
			(ge, ":liking_relation", 20),
			(store_div, reg0, ":liking_relation", 20),
			(val_add, ":family_relation", reg0),
		(else_try),
			(lt, ":liking_relation", 0),
			(store_div, reg0, ":liking_relation", 20),
			(val_sub, reg0, 1),
			(val_add, ":family_relation", reg0),
		(try_end),
		(store_random_in_range, reg0, 0, 3),#+0, +1, or +2 (because below we divide by three...)
		(val_add, ":family_relation", reg0),
		(assign, reg0, ":family_relation"),
		##diplomacy end+
		(assign, ":relation_modifier", ":base_relation_modifier"),
		(try_begin),
			##diplomacy start+
			#(gt, ":family_relation", 1),##OLD
			(neq, ":family_relation", 0),##NEW (allow lessening penalty for hated characters)
			##diplomacy end+
			(store_div, ":family_multiplier", reg0, 3),
			(val_sub, ":relation_modifier", ":family_multiplier"),
		(try_end),

		(lt, ":relation_modifier", 0),

		(call_script, "script_troop_change_relation_with_troop", ":faction_leader", ":active_npc", ":relation_modifier"),
		(val_add, "$total_indictment_changes", ":relation_modifier"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s17, ":active_npc"),
			(str_store_troop_name, s18, ":faction_leader"),

			(assign, reg3, ":relation_modifier"),
			(display_message, "str_trial_influences_s17s_relation_with_s18_by_reg3"),
		(try_end),
	(try_end),

	#Indictments, cont: Check for other factions
	(assign, ":new_faction", "fac_outlaws"),
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(assign, ":new_faction", 0), #kicked out of faction
	(else_try),
		(call_script, "script_lord_find_alternative_faction", ":troop_no"),
		(assign, ":new_faction", reg0),
	(try_end),

	#Indictments, cont: Finalize where the lord goes
	(try_begin),
		(is_between, ":new_faction", kingdoms_begin, kingdoms_end),


		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in indictment"),
		(try_end),

		(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
		(try_begin), #new-begin
		  (neq, ":new_faction", "fac_player_supporters_faction"),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
		  (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(try_end), #new-end
		(str_store_faction_name_link, s10, ":new_faction"),
		(str_store_string, s11, "str_with_the_s10"),
	(else_try),
		(neq, ":troop_no", "trp_player"),
		##diplomacy start+
		#Set "exile" occupation to differentiate between someone outside of Calradia
		#and an outlaw lord leading a party of bandits.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		##diplomacy end+
		(call_script, "script_change_troop_faction", ":troop_no", "fac_outlaws"),
		(str_store_string, s11, "str_outside_calradia"),
	(else_try),
		(eq, ":troop_no", "trp_player"),
		(call_script, "script_player_leave_faction", 1),
	(try_end),

	#Indictments, cont: Set up string
	(try_begin),
		(eq, ":troop_no", "trp_player"),
		(str_store_string, s9, "str_you_have_been_indicted_for_treason_to_s7_your_properties_have_been_confiscated_and_you_would_be_well_advised_to_flee_for_your_life"),
	(else_try),
		# (str_store_troop_name_plural, s4, ":troop_no"), #this now holds the new faction title, need to be changed
		(str_store_faction_name_link, s5, ":faction"),
		(str_store_troop_name_link, s6, ":faction_leader"),

		##diplomacy start+
		#(troop_get_type, reg4, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg4, reg0),
		(store_sub, ":title", ":faction", kingdoms_begin),
		(try_begin),
		  (eq, reg4, tf_male),
		  (val_add, ":title", kingdom_titles_male_begin),
		(else_try),
		  (eq, reg4, tf_female),
		  (val_add, ":title", kingdom_titles_female_begin),
		(else_try), #default to lord
		  (assign, ":title", kingdom_titles_male_begin),
		(try_end),
		(str_store_troop_name_plural, s0, ":troop_no"),
		(str_store_string, s4, ":title"),
		##diplomacy end+
		(str_store_string, s9, "str_by_order_of_s6_s4_of_the_s5_has_been_indicted_for_treason_the_lord_has_been_stripped_of_all_reg4herhis_properties_and_has_fled_for_reg4herhis_life_he_is_rumored_to_have_gone_into_exile_s11"),
	(try_end),
	##diplomacy start+ important political events should be in the log
    #SB : colorize with former faction
    (faction_get_color, ":color", s9),
	(display_log_message, s9, ":color"),#display_message changed to display_log_message
	##diplomacy end+

	#Indictments, cont: Remove party
	(troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
	(try_begin),
		(party_is_active, ":led_party"),
		(neq, ":led_party", "p_main_party"),
		(remove_party, ":led_party"),
		(troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 1),
		##diplomacy start+
		(this_or_next|eq, ":faction", "fac_player_supporters_faction"),
		(this_or_next|eq, ":new_faction", "fac_player_supporters_faction"),
		##diplomacy end+
		(this_or_next|eq, ":faction", "$players_kingdom"),
			(eq, ":new_faction", "$players_kingdom"),
		(call_script, "script_add_notification_menu", "mnu_notification_treason_indictment", ":troop_no", ":faction"),
	(try_end),
	##diplomacy start+
	(assign, reg0, ":save_reg0"),
	(assign, reg3, ":save_reg3"),
	(assign, reg4, ":save_reg4"),
	##diplomacy end+
   ]),


  # script_give_center_to_faction_while_maintaining_lord
  ("check_concilio_calradi_achievement",
  [
   (try_begin),
     (eq, "$players_kingdom", "fac_player_supporters_faction"),
     (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
     (eq, ":player_faction_king", "trp_player"),
     (assign, ":number_of_vassals", 0),
     (try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
       (store_faction_of_troop, ":cur_faction", ":cur_troop"),
       (eq, ":cur_faction", "fac_player_supporters_faction"),
       (val_add, ":number_of_vassals", 1),
     (try_end),
     (ge, ":number_of_vassals", 3),
     (unlock_achievement, ACHIEVEMENT_CONCILIO_CALRADI),
   (try_end),
  ]),

  # script_refresh_center_inventories
   ###################################################################################
   # REPORT PRESENTATIONS v1.2 scripts
   # Script overlay_container_add_listbox_item
   # use ...
   # return ...
   ("overlay_container_add_listbox_item", [
        (store_script_param, ":line_y", 1),
        (store_script_param, ":npc_id", 2),

        (set_container_overlay, "$g_jrider_character_relation_listbox"),

        # create text overlay for entry
        (create_text_overlay, reg10, s1, tf_left_align),
        (overlay_set_color, reg10, 0xDDDDDD),
        (position_set_x, pos1, 650),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),

        # create button
        (create_image_button_overlay, reg10, "mesh_white_plane", "mesh_white_plane"),
        (position_set_x, pos1, 0), # 590 real, 0 scrollarea
        (position_set_y, pos1, ":line_y"),
        (overlay_set_position, reg10, pos1),
        (position_set_x, pos1, 16000),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg10, pos1),
        (overlay_set_alpha, reg10, 0),
        (overlay_set_color, reg10, 0xDDDDDD),

        # store relation of button id to character number for use in triggers
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", reg10),
        (troop_set_slot, "trp_temp_array_b", ":current_storage_index", "$num_charinfo_candidates"),

        # reset variables if appropriate flags are up
        (try_begin),
            (try_begin),
                (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
                (ge, "$g_jrider_reset_selected_on_faction", 1),

                (assign, "$character_info_id", ":npc_id"),
                (assign, "$g_jrider_last_checked_indicator", reg10),
                (assign, "$g_latest_character_relation_entry", "$num_charinfo_candidates"),
            (try_end),
        (try_end),

        # close the container
        (set_container_overlay, -1),
   ]),

   # script get_relation_candidate_list_for_presentation
   # return a list of candidate according to type of list and restrict options
   # Use ...
   ("fill_relation_canditate_list_for_presentation",
    [
        (store_script_param, ":pres_type", 1),
        (store_script_param, ":base_candidates_y", 2),

        # Type of list from global variable: 0 courtship, 1 known lords
        (try_begin),
        ## For courtship:
            (eq, ":pres_type", 0),

            (try_for_range_backwards, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                (troop_slot_ge, ":lady", slot_troop_met, 1), # met or better
                (troop_slot_eq, ":lady", slot_troop_spouse, -1), # unmarried

                # use faction filter
                (store_troop_faction, ":lady_faction", ":lady"),
                (val_sub, ":lady_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":lady_faction"),

                (call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
                (gt, reg0, 0),
                (assign, reg3, reg0),

                (str_store_troop_name, s2, ":lady"),

                (store_current_hours, ":hours_since_last_visit"),
                (troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
                (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
                (store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
                (assign, reg4, ":days_since_last_visit"),

                #(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
                (str_store_string, s1, "@{s2}: {reg3}, {reg4} days"),

                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":lady"),

                # candidate found, store troop id for later use
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":lady"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## End courtship relations
        (else_try),
        ## For lord relations
            (eq, ":pres_type", 1),

            # Loop to identify
            (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                (troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
            (try_end),

            (try_for_range, ":unused", active_npcs_begin, active_npcs_end),

                (assign, ":score_to_beat", 101),
                (assign, ":best_relation_remaining_npc", -1),

                (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                        (troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
                        (troop_slot_ge, ":active_npc", slot_troop_met, 1),
                        (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

                        (call_script, "script_troop_get_player_relation", ":active_npc"),
                        (assign, ":relation_with_player", reg0),
                        (le, ":relation_with_player", ":score_to_beat"),

                        (assign, ":score_to_beat", ":relation_with_player"),
                        (assign, ":best_relation_remaining_npc", ":active_npc"),
                (try_end),
                (gt, ":best_relation_remaining_npc", -1),

                (str_store_troop_name, s4, ":best_relation_remaining_npc"),
                (assign, reg4, ":score_to_beat"),

                (str_store_string, s1, "@{s4}: {reg4}"),
                (troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),

                # use faction filter
                (store_troop_faction, ":npc_faction", ":best_relation_remaining_npc"),
                (val_sub, ":npc_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":npc_faction"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":best_relation_remaining_npc"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":best_relation_remaining_npc"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## END Lords relations
        (else_try),
        ## Character and Companions
            (eq, ":pres_type", 2),

            # companions
            (try_for_range_backwards, ":companion", companions_begin, companions_end),
                (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

                (str_store_troop_name, s1, ":companion"),

        (try_begin),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
                    (str_store_string, s1, "@{s1}(gathering support)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
                    (str_store_string, s1, "@{s1} (intelligence)" ),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
                    (neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
                    (str_store_string, s1, "@{s1} (ambassy)"),
                (else_try),
                        (eq, ":companion", "$g_player_minister"),
                    (str_store_string, s1, "@{s1} (minister"),
                (else_try),
                    (main_party_has_troop, ":companion"),
                    (str_store_string, s1, "@{s1} (under arms)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                    (str_store_string, s1, "@{s1} (attempting to rejoin)"),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_cur_center, 1),
                    (str_store_string, s1, "@{s1} (separated after battle)"),
                (try_end),
                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":companion"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":companion"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # END companions

            # Wife/Betrothed
            # END Wife/Betrothed

            (try_begin),
            # Character
                (str_store_troop_name, s1, "trp_player"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", "trp_player"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", "trp_player"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # End Character

        (try_end),
        ## END Character and Companions
    ]),

    # script get_troop_relation_to_player_string
    # return relation to player string in the specified parameters
    #
    ("get_troop_relation_to_player_string",
     [
         (store_script_param, ":target_string", 1),
         (store_script_param, ":troop_no", 2),

         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (str_clear, s61),

         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20),
         (store_add, ":str_rel_id", "str_relation_mnus_100_ns",  ":str_offset"),

         ## Make something if troop has relation but not strong enought to warrant a string
         (try_begin),
           (neq, ":str_rel_id", "str_relation_plus_0_ns"),
           (str_store_string, s61, ":str_rel_id"),
         (else_try),
           (neg|eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ knows of you."),
         (else_try),
           (eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ has no opinion about you."),
         (try_end),

         ## copy result string to target string
         (str_store_string_reg, ":target_string", s61),
     ]),

    # script get_troop_holdings
    # returns number of fief and list name (reg50, s50)
    ("get_troop_holdings",
     [
         (store_script_param, ":troop_no", 1),

         (assign, ":owned_centers", 0),
         (assign, ":num_centers", 0),
         (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
             (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
             (try_begin),
               (eq, ":num_centers", 0),
               (str_store_party_name, s50, ":cur_center"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (eq, ":num_centers", 1),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{s57} and {s50}"),
               (val_add, ":owned_centers", 1),
             (else_try),
               (str_store_party_name, s57, ":cur_center"),
               (str_store_string, s50, "@{!}{s57}, {s50}"),
               (val_add, ":owned_centers", 1),
             (try_end),
             (val_add, ":num_centers", 1),
         (try_end),
         (assign, reg50, ":owned_centers"),
     ]),

    # script generate_extended_troop_relation_information_string
    # return information about troop according to type (lord, lady, maiden)
    # Use (hm lots of registers and strings)
    # result stored in s1
    ("generate_extended_troop_relation_information_string",
     [
         (store_script_param, ":troop_no", 1),

         # clear the strings and registers we'll use to prevent external interference
         (str_clear, s1),
         (str_clear, s2),
         (str_clear, s60),
         (str_clear, s42),
         (str_clear, s43),
         (str_clear, s44),
         (str_clear, s45),
         (str_clear, s46),
         (str_clear, s47),
         (str_clear, s48),
         (str_clear, s49),
         (str_clear, s50),
         (assign, reg40,0),
         (assign, reg41,0),
         (assign, reg43,0),
         (assign, reg44,0),
         (assign, reg46,0),
         (assign, reg47,0),
         (assign, reg48,0),
         (assign, reg49,0),
         (assign, reg50,0),
         (assign, reg51,0),

         (try_begin),
             (eq, ":troop_no", "trp_player"),
             (overlay_set_display, "$g_jrider_character_faction_filter", 0),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Honor - $player_honor
             (assign, reg42, "$player_honor"),

             # Right to rule - $player_right_to_rule
             (assign, reg43, "$player_right_to_rule"),

             # Current faction
             (store_add, reg45, "$players_kingdom"),
             (try_begin),
                 (is_between, "$players_kingdom", "fac_player_supporters_faction", npc_kingdoms_end),
                 (str_store_faction_name, s45, "$players_kingdom"),
             (else_try),
                 (assign, reg45, 0),
                 (str_store_string, s45, "@Calradia."),
             (try_end),

             # status
             (assign, ":origin_faction", "$players_kingdom"),
             #SB : gender strings
             (try_begin),
                 (is_between, ":origin_faction", npc_kingdoms_begin, npc_kingdoms_end),
                 (str_store_string, s44, "@sworn {man/woman}"),
             (else_try),
                 (eq, ":origin_faction", "fac_player_supporters_faction"),
                 (str_store_string, s44, "@ruler"),
             (else_try),
                 (str_store_string, s44, "@free {man/woman}"),
             (try_end),

             # Current liege and relation
             (faction_get_slot, ":liege", "$players_kingdom", slot_faction_leader),
             (str_store_troop_name, s46, ":liege"),
             (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
             (else_try),
                 (assign, reg46, ":liege"),
                 (str_clear, s47),
                 (str_clear, s60),

                 # Relation to liege
                 (call_script, "script_get_troop_relation_to_player_string", s47, ":liege"),
             (end_try),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

             #### Final Storage
             (str_store_string, s1, "@{s1} Renown: {reg40}, Controversy: {reg41}^Honor: {reg42}, Right to rule: {reg43}^\
You are a {s44} of {s45}^{reg45?{reg46?Your liege, {s46},{s47}:You are the ruler of {s45}}:}^^Friends: ^Enemies: ^^Fiefs:^  {reg50?{s50}:no fief}"),
         #######################
         # END Player information
         (else_try),
         #######################
         # Lord information
             (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Get Reputation type - slot_lord_reputation_type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (assign, reg42, "str_personality_archetypes"),
             (val_add, reg42, ":reputation"),
             (str_store_string, s42, reg42),

             (assign, reg42, ":reputation"),
             # Intrigue impatience - slot_troop_intrigue_impatience
             (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
             (assign, reg43, ":impatience"),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin), #SB : do not display original faction string if same
               (neq, ":faction", ":origin_faction"),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
               (assign, reg44, 1),
             (else_try), #if same, start line with capitalized Noble
               (assign, reg44, 0),
             (try_end), #actually skip this line altogether if ruler
             (str_store_faction_name, s45, ":faction"),

             # Current liege - deduced from current faction
             (faction_get_slot, ":liege", ":faction", slot_faction_leader),
             (try_begin),
               #When a member of a faction without a valid leader
               (lt, ":liege", 0),
               (assign, reg46, ":liege"),
               (str_store_string, s46, "str_noone"),
               (assign, reg47, 0),
             (else_try),
               (str_store_troop_name, s46, ":liege"),
               (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
               (else_try),
                 (assign, reg46, ":liege"),
                 # Relation to liege
                 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
                 (assign, reg47, reg0),
               (end_try),
             (try_end),

             # Promised a fief ?
             (troop_get_slot, reg51, ":troop_no", slot_troop_promised_fief),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

              # slot_troop_prisoner_of_party
              (assign, reg48, 0),
              (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
              (try_end),

              # Days since last meeting
              (store_current_hours, ":hours_since_last_visit"),
              (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
              (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
              (store_div, reg49, ":hours_since_last_visit", 24),

              #### Final Storage (8 lines)
              (str_store_string, s1, "@{s1}{s2} {reg46?Reputed to be {s42}:}^Renown: {reg40}, Controversy: {reg41} {reg46?Impatience: {reg43}:}^\
{reg46?{reg44?{s44} noble:Noble} of the {s45}^Liege: {s46}, Relation: {reg47}:Ruler of the {s45}}^^{reg48?Currently prisoner of the {s48}:}^\
Days since last meeting: {reg49}^^Fiefs {reg51?(was promised a fief):}:^  {reg50?{s50}:no fief}"),
        ######################
        ## END lord infomation
        (else_try),
        #########################
        # kingdom lady, unmarried
             (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
             (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),

             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Reputation type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (try_begin),
                 (eq, ":reputation", lrep_conventional),
                 (str_store_string, s42, "@conventional"),
             (else_try),
                 (eq, ":reputation", lrep_adventurous),
                 (str_store_string, s42, "@adventurous"),
             (else_try),
                 (eq, ":reputation", lrep_otherworldly),
                 (str_store_string, s42, "@otherwordly"),
             (else_try),
                 (eq, ":reputation", lrep_ambitious),
                 (str_store_string, s42, "@ambitious"),
             (else_try),
                 (eq, ":reputation", lrep_moralist),
                 (str_store_string, s42, "@moralist"),
             (else_try),
                 (assign, reg42, "str_personality_archetypes"),
                 (val_add, reg42, ":reputation"),
                 (str_store_string, s42, reg42),
             (try_end),

             # courtship state - slot_troop_courtship_state
             (troop_get_slot, ":courtship_state", ":troop_no", slot_troop_courtship_state),
             (try_begin),
               (eq, ":courtship_state", 1),
               (str_store_string, s43, "@just met"),
             (else_try),
               (eq, ":courtship_state", 2),
               (str_store_string, s43, "@admirer"),
             (else_try),
               (eq, ":courtship_state", 3),
               (str_store_string, s43, "@promised"),
             (else_try),
               (eq, ":courtship_state", 4),
               (str_store_string, s43, "@breakup"),
             (else_try),
               (str_store_string, s43, "@unknown"),
             (try_end),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
             (end_try),
             (str_store_faction_name, s45, ":faction"),

             # Father/Guardian
             (assign, reg46, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_father, 0),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
                 (assign, reg46, 1),
             (else_try),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
             (try_end),
             (str_store_troop_name, s46, ":guardian"),

             # Relation with player
             (str_clear, s47),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s47, ":guardian"),

             # courtship permission - slot_lord_granted_courtship_permission
             (try_begin),
                 (troop_slot_ge, ":guardian", slot_lord_granted_courtship_permission, 1),
                 (assign, reg45, 1),
             (else_try),
                 (assign, reg45, 0),
             (try_end),

             # betrothed
             (assign, reg48, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_betrothed, 0),
                 (troop_get_slot, reg48, ":troop_no", slot_troop_betrothed),
                 (str_store_troop_name, s48, reg48),
                 (assign, reg48, 1),
             (try_end),

             # Days since last meeting
             (store_current_hours, ":hours_since_last_visit"),
             (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
             (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
             (store_div, reg49, ":hours_since_last_visit", 24),

             # Heard poems
             (assign, reg50, 0),
             (str_clear, s50),

             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_heroic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Heroic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_allegoric_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Allegoric {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_comic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Comic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_mystic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Mystic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_tragic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Tragic {s50}"),
             (try_end),

             #### Final Storage (8 lines)
             (str_store_string, s1, "@{s1}{s2} Controversy: {reg41}^Reputation: {s42}, Courtship state: {s43}^\
Belongs to the {s45}^{reg46?Her father, {s46}:Her guardian, {s46}}{s47}^Allowed to visit: {reg45?yes:no} {reg48?Betrothed to {s48}:}^^\
Days since last meeting: {reg49}^^Poems:^  {reg50?{s50}:no poem heard}"),
        #########################
        # END kingdom lady, unmarried
        (else_try),
        #########################
        # companions
            (is_between, ":troop_no", companions_begin, companions_end),
            (overlay_set_display, "$g_jrider_character_faction_filter", 0),

            (str_store_troop_name, s1, ":troop_no"),

            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),

            (assign, reg42, "str_personality_archetypes"),
            (val_add, reg42, ":reputation"),
            (str_store_string, s42, reg42),

            # birthplace
            (troop_get_slot, ":home", ":troop_no", slot_troop_home),
            (str_store_party_name, s43, ":home"),

            # contacts town - slot_troop_town_with_contacts
            (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
            (str_store_party_name, s44, ":contact_town"),

            # current faction of contact town
            (store_faction_of_party, ":town_faction", ":contact_town"),
            (str_store_faction_name, s45, ":town_faction"),

            # slot_troop_prisoner_of_party
            (assign, reg48, 0),
            (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
            (try_end),

            # Days since last meeting
            (store_current_hours, ":hours_since_last_visit"),
            (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
            (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
            (store_div, reg49, ":hours_since_last_visit", 24),

            (try_begin), # Companion gathering support for Right to Rule
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_kingsupport),
                (str_store_string, s50, "@Gathering support"),
            (else_try), # Companion gathering intelligence
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_gather_intel),
                (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
                (store_faction_of_party, ":town_faction", ":contact_town"),
                (str_store_faction_name, s66, ":town_faction"),
                (str_store_string, s50, "@Gathering intelligence in the {s66}"),
            (else_try), # Companion on peace mission
                (troop_slot_ge, ":troop_no", slot_troop_current_mission, npc_mission_peace_request),
                (neg|troop_slot_ge, ":troop_no", slot_troop_current_mission, 8),

                (troop_get_slot, ":troop_no", ":troop_no", slot_troop_mission_object),
                (str_store_faction_name, s66, ":faction"),

                (str_store_string, s50, "@Ambassy to {s66}"),
            (else_try), # Companion is serving as minister player has court
                (eq, ":troop_no", "$g_player_minister"),
                (str_store_string, s50, "@Minister"),
            (else_try),
                (str_store_string, s50, "str_dplmc_none"),
        (try_end),

            # days left
            (troop_get_slot, reg50, ":troop_no", slot_troop_days_on_mission),

            #### Final Storage (8 lines)
            (str_store_string, s1, "@{s1}, {s2}^Reputation: {s42}^\
Born at {s43}^Contact in {s44} of the {s45}.^\
^{reg48?Currently prisoner of the {s48}:}^Days since last talked to: {reg49}^^Current mission:^  {s50}{reg50?, back in {reg50} days.:}"),
        #########################
        # END companions
        (try_end),
    ]),

    # Script generate_known_poems_string
    # generate in s1 list of known poems filling with blank lines for unknown ones
    ("generate_known_poems_string",
     [
        # Known poems string
        (assign, ":num_poems", 0),
        (str_store_string, s1, "str_s1__poems_known"),
        (try_begin),
            (gt, "$allegoric_poem_recitations", 0),
            (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$tragic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$comic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$heroic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$mystic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
            (val_add, ":num_poems", 1),
        (try_end),

        # fill blank lines
        (try_for_range, ":num_poems", 5),
            (str_store_string, s1, "@{s1}^"),
        (try_end),
    ]),
   # Jrider -

##diplomacy end+

  #Equipment cost fix
   ("player_get_value_of_original_items",
    [
      (store_script_param, ":player_no", 1),
      (store_script_param, ":agent_no", 2),
      (store_script_param, ":troop_id", 3),
      (assign, ":total_equipment_cost", 0),
      (try_for_range, ":i_item_slot", 0, 8),
          (neg|player_item_slot_is_picked_up, ":player_no", ":i_item_slot"),
          (agent_get_item_slot, ":item_id", ":agent_no", ":i_item_slot"), #value between 0-7, order is weapon1, weapon2, weapon3, weapon4, head_armor, body_armor, leg_armor, hand_armor
          #(player_get_item_id, ":item_id", ":player_no", ":i_item_slot"), #only for server
          (neq, ":item_id", -1),
          (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_id"),
          (val_add, ":total_equipment_cost", reg0),

          #Debugging
          #(assign, reg1, ":total_equipment_cost"),
          #(str_store_item_name, s0, ":item_id"),
          #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@{s0} for {reg0}g added to total equipment cost, which is now: {reg1}g"),
          ##
      (try_end),
      (try_for_agents, ":cur_horse"),
         #Check all horses in the scene and see if one of them is agent_no's bought horse. Won't be enough to just do (agent_get_horse, ":horse", ":agent_no"),
         #since you get money back for a bought horse, even if you have dismounted it, if the horse is still alive and has no other rider.
         (agent_is_alive, ":cur_horse"),
         (neg|agent_is_human, ":cur_horse"),  #Spawned agent is horse
         (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
         (eq, ":agent_no_bought_horse", ":cur_horse"),
         (assign, ":add_horse_cost_to_equipment_value", 0),
         (try_begin),
             (agent_get_rider, ":rider_agent_id", ":cur_horse"),
             (try_begin),
                 (neq, ":rider_agent_id", -1),
                 (neg|agent_is_non_player, ":rider_agent_id"),
                 (agent_get_slot, ":agent_no_bought_horse", ":rider_agent_id", slot_agent_bought_horse),
                 (eq, ":agent_no_bought_horse", ":cur_horse"), #agent_no is mounted on the same horse he bought
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@You are mounted on your bought {s0} and will get money for it"),
                 ##
             (else_try),
                 (eq, ":rider_agent_id", -1), #If cur_horse doesn't have a rider
                 (agent_get_horse, ":agent_no_mount", ":agent_no"),
                 (eq, ":agent_no_mount", -1), #If agent_no is not mounted on another horse
                 (agent_get_slot, ":agent_no_bought_horse", ":agent_no", slot_agent_bought_horse),
                 (eq, ":agent_no_bought_horse", ":cur_horse"),
                 (assign, ":add_horse_cost_to_equipment_value", 1),

                 #Debugging
                 #(agent_get_item_id, ":mount_type", ":cur_horse"), #(works only for horses, returns -1 otherwise)
                 #(str_store_item_name, s0, ":mount_type"),
                 #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Your bought {s0} is alive so you get money for it"),
                 ##
            (try_end),
            (eq, ":add_horse_cost_to_equipment_value", 1),
            (agent_get_item_id, ":cur_mount_type", ":cur_horse"), #Checks which type the horse is
            (call_script, "script_multiplayer_get_item_value_for_troop", ":cur_mount_type", ":troop_id"),
            (val_add, ":total_equipment_cost", reg0),
            (multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@Added money for your old horse"),
         (try_end),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_bought_horse, -1),
      (assign, reg0, ":total_equipment_cost"),
     ]),
     ###

     ##script_improve_center
     #helper script for building in centers
    ("improve_center", [
        (store_script_param, ":center_no", 1),
        (store_script_param, ":builder", 2),
        (store_script_param, ":improvement_time", 3),
        (party_set_slot, ":center_no", slot_center_current_improvement, "$g_improvement_type"),
        (store_current_hours, ":cur_hours"),
        (store_mul, ":hours_takes", ":improvement_time", 24),
        (val_add, ":hours_takes", ":cur_hours"),
        (party_set_slot, ":center_no", slot_center_improvement_end_hour, ":hours_takes"),
        (assign, reg6, ":improvement_time"),
        (call_script, "script_get_improvement_details", "$g_improvement_type"),
        (add_party_note_from_sreg, ":center_no", 2, "@A {s0} is being built. It will finish in {reg6} days", 1),
        (try_begin), #should probably raise this depending on project instead of constant reward
          (troop_is_hero, ":builder"),
          (neq, ":builder", "trp_player"),
          (call_script, "script_change_troop_renown", ":builder", dplmc_companion_skill_renown),
        (try_end),
    ]),

     ##script_calculate_improvement_limit
     #calculate threshold for building stuff
     #input: troop_no, center_no (unused)
     #output: reg0
    ("calculate_improvement_limit", [
        (store_script_param_1, ":troop_no"),
        (assign, ":limit", dplmc_improvement_limit),
        (troop_get_slot, ":personality", ":troop_no", slot_lord_reputation_type),
        (try_begin), #bad personality, unlikely to ever build property
            (is_between, ":personality", lrep_selfrighteous, lrep_goodnatured),
            (val_mul, ":limit", ":personality"),
            (val_div, ":limit", 2),
        (else_try), #include companion personality types
            (is_between, ":personality", lrep_goodnatured, lrep_custodian),
            (try_begin), #exception
              (neq, ":personality", lrep_roguish),
              (store_mul, ":level", ":personality", 250),
              (val_sub, ":limit", ":level"),
            (try_end),
        (try_end),
        (assign, reg0, ":limit"),
    ]),

     ##script_calculate_equipment_limit
     #calculate threshold for upgrading equipment imod from merchants
     #input: troop_no, center_no (unused)
     #output: reg0
    ("calculate_equipment_limit", [
        (store_script_param_1, ":troop_no"),
        (store_script_param_2, ":center_no"),
        (assign, ":limit", dplmc_equipment_limit),
        (troop_get_slot, ":personality", ":troop_no", slot_lord_reputation_type),

        (try_begin), #focus on arms
          (is_between, ":personality", lrep_martial, lrep_selfrighteous),
          (val_div, ":limit", 2),
        (else_try), #invest in gear not fief
          (eq, ":personality", lrep_roguish),
          (val_sub, ":limit", 1000),
        (try_end),

        #aristocracy modifier as enthusiasm for shopping
        (store_faction_of_party, ":faction_no", ":center_no"),
        (faction_get_slot, ":aristocracy", ":faction_no", dplmc_slot_faction_aristocracy),
        (val_mul, ":aristocracy", -100), #high plutocracy more shopping, decreasing threshold
        (val_add, ":limit", ":aristocracy"),

        (assign, reg0, ":limit"),
    ]),
    #script_change_troop_intrigue_impatience
    #inputs: troop_no ($g_talk_troop), amount
    #output: slot_troop_intrigue_impatience changed
    ("change_troop_intrigue_impatience", [
        (store_script_param_1, ":troop_no"),
        (store_script_param_2, ":amount"),
        (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
        (val_max, ":impatience", ":amount"),
        (troop_set_slot, ":troop_no", slot_troop_intrigue_impatience, ":impatience"),
    ]),
    #script_center_get_bandits
    #inputs: center_no, mode
    #output: bandit_troop in reg0
    # get an appropriate bandit to infest the village
  ("center_get_bandits",[

    (store_script_param_1, ":village_no"),
    (store_script_param_2, ":mode"),
    (assign, ":bandit_troop", "trp_looter"),

    (try_begin), #native mode
      (eq, ":mode", -1),
      (store_random_in_range, ":random_no", 0, 3),
      (try_begin),
        (eq, ":random_no", 0),
        (assign, ":bandit_troop", "trp_bandit"),
      (else_try),
        (eq, ":random_no", 1),
        (assign, ":bandit_troop", "trp_mountain_bandit"),
      (else_try),
        (assign, ":bandit_troop", "trp_forest_bandit"),
      (try_end),
    (else_try), #faction mode
      (eq, ":mode", 0),

      (assign, ":bandit_troop", "trp_looter"),
      # (store_faction_of_party, ":faction", ":village_no"),
      (party_get_slot, ":faction", ":village_no", slot_center_original_faction),
      (store_random_in_range, ":random_no", 0, 10),
      (try_begin), #deserter troops, 10% chance
        (eq, ":random_no", 0),
        (faction_get_slot, ":bandit_troop", ":faction", slot_faction_deserter_troop),
      (else_try),
        (lt, ":random_no", 6),  #regular bandits (looter to brigand), 50%
        (val_div, ":random_no", 2),
        (store_add, ":bandit_troop","trp_looter",":random_no"),
      (else_try), #regional bandits, 40% (should be terrain based though)
        (try_begin),
          (eq, ":faction", "fac_kingdom_6"),
          (assign, ":bandit_troop", "trp_desert_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_5"),
          (assign, ":bandit_troop", "trp_mountain_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_4"),
          (assign, ":bandit_troop", "trp_sea_raider"),
        (else_try),
          (eq, ":faction", "fac_kingdom_3"),
		  (try_begin),
			(lt, ":random_no", 3),
			(assign, ":bandit_troop", "trp_black_khergit_horseman"), # dckplmc - 20% chance of black khergits
		  (else_try),
			(assign, ":bandit_troop", "trp_steppe_bandit"),
		  (try_end),
        (else_try),
          (eq, ":faction", "fac_kingdom_2"),
          (assign, ":bandit_troop", "trp_taiga_bandit"),
        (else_try),
          (eq, ":faction", "fac_kingdom_1"),
          (assign, ":bandit_troop", "trp_forest_bandit"),
        (try_end),
      (try_end),
    (else_try), #terrain mode
      (eq, ":mode", 1),
      #base type first
      (party_get_current_terrain, ":terrain_type", ":village_no"),
      (try_begin),
        (this_or_next|eq, ":terrain_type", rt_steppe),
        (eq, ":terrain_type", rt_steppe_forest),
		(store_random_in_range, ":random_no", 0, 10),
	    (try_begin),
		  (lt, ":random_no", 3),
		  (assign, ":bandit_troop", "trp_black_khergit_horseman"), # dckplmc - 20% chance of black khergits
	    (else_try),
		  (assign, ":bandit_troop", "trp_steppe_bandit"),
	    (try_end),
      # (else_try),
        # (eq, ":terrain_type", rt_plain),
        # (assign, ":bandit_troop", "trp_bandit"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_snow),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":bandit_troop", "trp_taiga_bandit"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_desert),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":bandit_troop", "trp_desert_bandit"),
      # (else_try),
        # (eq, ":terrain_type", rt_forest),
        # (assign, ":bandit_troop", "trp_forest_bandit"),
      (try_end),
      (try_begin),
        (eq, ":bandit_troop", "trp_looter"), #still not picked
        #proximity to features (forest, mountain, ocean),
        (party_get_position, pos1, ":village_no"),
        (try_begin), #cf operation to see if it's near water
          (map_get_water_position_around_position, pos2, pos1, 5),
          # after finding water limit range of spawning (so sea raiders don't appear upriver)
          (store_add, ":limit", "p_sea_raider_spawn_point_1", num_sea_raider_spawn_points),
          (try_for_range, ":spawn_point", "p_sea_raider_spawn_point_1", ":limit"),
            (store_distance_to_party_from_party, ":distance", ":village_no", ":spawn_point"),
            (lt, ":distance", 50), # 200% bandit spawning radius
            (assign, ":limit", -1),
          (try_end),
          (eq, ":limit", -1), #within boundaries
          (assign, ":bandit_troop", "trp_sea_raider"),
        (else_try), #sample random points until we find forest/mountain (coast)
          (assign, ":forest_count", 0),
          (assign, ":mountain_count", 0),
          (assign, ":other_count", 0),
          (try_for_range, ":unused", 0, 100),
            (map_get_land_position_around_position, pos2, pos1, 5),
            (party_set_position, "p_temp_party", pos2),
            (party_get_current_terrain, ":terrain_type", "p_temp_party"),
            (try_begin),
              (eq, ":terrain_type", rt_forest),
              (val_add, ":forest_count", 1),
            (else_try),
              (eq, ":terrain_type", rt_mountain),
              (val_add, ":mountain_count", 1),
            (else_try),
              (val_add, ":other_count", 1),
            (try_end),
          (try_end),
          (try_begin), # not enough features
            (gt, ":other_count", 75), #pass through to faction calls
            (call_script, "script_center_get_bandits", ":village_no", 0),
            (assign, ":bandit_troop", reg0),
          (else_try),
            (gt, ":forest_count", ":mountain_count"),
            (gt, ":forest_count", 15),
            (assign, ":bandit_troop", "trp_forest_bandit"),
          (else_try),
            (gt, ":mountain_count", ":forest_count"),
            (gt, ":mountain_count", 15),
            (assign, ":bandit_troop", "trp_mountain_bandit"),
          (try_end),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg0, ":bandit_troop"),
  ]),


  ("create_wpn_slot_overlay", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":pos", 2),
      (init_position, pos1),
      (position_set_x, pos1, 270),
      (position_set_y, pos1, ":pos"),
      (create_combo_button_overlay, ":obj"),
      (overlay_set_position, ":obj", pos1),
      (assign, ":sub_overlay_id", 0),
      (store_add, ":upgrade_slot", ":slot", dplmc_slot_upgrade_wpn_0),

      # #SB : add meta-types
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_pikes"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_lance"),
      # (overlay_add_item, ":obj", "str_dplmc_hero_wpn_slot_morningstar"),
      # (try_for_range_backwards, ":item_type", dplmc_itp_morningstar, dplmc_itp_pike + 1),
        # (troop_slot_eq, "$temp", ":upgrade_slot", ":item_type"),
        # (overlay_set_val, ":obj", ":sub_overlay_id"),
      # (else_try),
        # (val_add, ":sub_overlay_id", 1),
      # (try_end),
      (call_script, "script_dplmc_get_current_item_for_autoloot", ":slot"), #goes to "keep current", s10
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        (overlay_add_item, ":obj", ":out_string"),
        (try_begin), #find base type
          (troop_get_slot, ":cur_value", "$temp", ":upgrade_slot"),
          (val_mod, ":cur_value", meta_itp_mask),
          (eq, ":cur_value", ":item_type"),
          (overlay_set_val, ":obj", ":sub_overlay_id"),
        (try_end),
        (val_add, ":sub_overlay_id", 1),
      (try_end),

      #store id in slot
      (troop_set_slot, "trp_stack_selection_ids", ":slot", ":obj"),
      # # only works for original button, not drop-down lists
      # (overlay_set_additional_render_height, ":obj", 99),

      (assign, reg1, ":obj"), #return overlay id
  ]),


  ("update_wpn_slot_itp", [
      (store_script_param, ":slot", 1),
      (store_script_param, ":value", 2),
      (troop_get_slot, ":item_type", "trp_temp_array_c", ":value"),
      (troop_get_slot, ":slot_value", "$temp", ":slot"),
      (try_begin), #if new value supports metamods, inherit
        (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
        (store_mod, ":original_value", ":slot_value", meta_itp_mask),
        (val_sub, ":slot_value", ":original_value"), #remove original itp
        (val_add, ":slot_value", ":item_type"), #add new
      (else_try), #otherwise replace value
        (assign, ":slot_value", ":item_type"),
      (try_end),
      (troop_set_slot, "$temp", ":slot", ":slot_value"),
      (assign, "$temp_2", ":slot"),
      #restart presentation instead of updating overlay value (because we can't)
      (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
  ]),
  #script_item_get_type_aux : auxiliary item classification script, see header_items for values
  #input : item
  #output: reg0, item type or meta-type
  ("item_get_type_aux", [
    (store_script_param, ":item", 1),

    (item_get_type, ":itp", ":item"),
    (try_begin),
      # (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
      # (item_has_property, ":item", itp_type_two_handed_wpn),
      (eq, ":itp", itp_type_two_handed_wpn),
      (neg|item_has_property, ":item", itp_two_handed),
      (assign, ":itp", dplmc_itp_morningstar), # type 11 = two-handed/one-handed
    (else_try),
      (eq, ":itp", itp_type_polearm),
      (item_get_swing_damage, ":swing", ":item"),
      (item_get_thrust_damage, ":thrust", ":item"),
      (try_begin),
        (ge, ":swing", ":thrust"),
        (item_get_swing_damage_type, ":damage_type", ":item"),
        (eq, ":damage_type", cut),
        (assign, ":itp", dplmc_itp_halberd),
      (else_try),
        (lt, ":swing", ":thrust"),
        (try_begin), #lances
          (item_has_property, ":item", itp_couchable),
          (assign, ":itp", dplmc_itp_lance),
        (else_try), #can't be both lance and pike
          # (item_has_property, ":item", itp_cant_use_on_horseback), #too restrictive
          (item_get_weapon_length, ":length", ":item"),
          (ge, ":length", dplmc_pike_length_cutoff), #arbitrary value to allow awlpikes to fall in range
          (item_has_capability, ":item", itcf_thrust_polearm), #has two-handed thrust
          (this_or_next|item_has_property, ":item", itp_two_handed),
          (item_has_property, ":item", itp_penalty_with_shield),
          (assign, ":itp", dplmc_itp_pike),
        (try_end),
      (try_end),
    (try_end),
    (assign, reg0, ":itp"),
  ]),

  #check if weapons are wholly inappropriate for actual combat
  ("cf_melee_weapon_is_civilian", [
    (store_script_param, ":item", 1),
    (this_or_next|is_between, ":item", "itm_sickle", "itm_dagger"),
    (this_or_next|is_between, ":item", "itm_scythe", "itm_military_fork"),
    (this_or_next|eq, ":item", "itm_wooden_stick"),
    (eq, ":item", "itm_torch"),
    # (eq, ":item", "itm_stones"),
     #include arena weapons here as well
  ]),

  #check if the item type has advanced auto-loot options available (damage type, meta-type)
  ("cf_item_type_has_advanced_autoloot", [
    (store_script_param, ":item_type", 1),
    (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_shield),
    (eq, ":item_type", itp_type_thrown), #throwing axe vs jaridss vs rocks
    #all other ranged weapons are pierce (for now) excluding arena ones
  ]),

  #script_display_policy_string_to_reg
  #unify string register usage to one temp s0 and one output s20
  #register reg2,3 are used for mode and postfix
  ("display_policy_string_to_reg", [
    (store_script_param, ":faction_no", 1),
    (store_script_param, reg2, 2), #whether it is third person "the" or first person "our"
    (store_script_param, reg3, 3), #spaces or line breaks as the postfix delimiter

    (str_store_faction_name_link, s5, ":faction_no"),
    (assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
    (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
    (val_add, ":string", ":centralization"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our government:The goverment of the {s5}} is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
    (faction_get_slot, ":aristocraty", ":faction_no", dplmc_slot_faction_aristocracy),
    (val_add, ":string", ":aristocraty"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}The upper class society is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mixture_serfs"),
    (faction_get_slot, ":serfdom", ":faction_no", dplmc_slot_faction_serfdom),
    (val_add, ":string", ":serfdom"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} people are {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mediocre_quality"),
    (faction_get_slot, ":quality", ":faction_no", dplmc_slot_faction_quality),
    (val_add, ":string", ":quality"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} troops have {s0}.{reg3?^: }"),

    ##nested diplomacy start+ add mercantilism
    (assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
    (faction_get_slot, ":mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
    (val_add, ":string", ":mercantilism"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The government's} approach to trade is {s0}.{reg3?^: }"),
  ]),

  #native stuff for startup merchants
  ("get_troop_of_merchant",
  [
        (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
        (store_sub, ":troop_of_merchant", ":starting_town_faction", npc_kingdoms_begin),
        (val_add, ":troop_of_merchant", startup_merchants_begin),
        (assign, reg0, ":troop_of_merchant"),
  ]),

  #reusable code to check whether npcs in a specific range have been met
  #input : troop_no, amount expected, properly set up qst_rescue_prisoner targets
  #assumes no other sources of debt (dialog prevents condition) and quest troop is active and related
  #output : amount lord_no personally pays in reg0, cached in slot_troop_player_debt, cleared when player rejects it
  ("calculate_ransom_contribution", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (store_script_param_2, ":ransom_size"), #2000 from quest giver, up to 125*strength for other relatives
    #because kingdom ladies aren't landholders, they give it without consequence of debt if quest fails (also less dialogue to write)
    (assign, ":ransom_amount", 0),

    (try_begin),
      (check_quest_active, "qst_rescue_prisoner"),
      (quest_get_slot, ":prisoner", "qst_rescue_prisoner", slot_quest_target_troop),
      (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
      (try_begin),
        #each +-2 relation has 1% effect on calculation to the effect of 50%/150% initial value
        (call_script, "script_troop_get_relation_with_troop", ":lord_no", ":prisoner"),
        (store_div, ":relation", reg0, 2),
        (val_add, ":relation", 100),
        (val_mul, ":ransom_amount", ":relation"),
        (val_div, ":ransom_amount", 100),
      (try_end),
      # problem is this script has variance in output, we can use the cached slot_quest_target_amount
      (call_script, "script_calculate_ransom_amount_for_troop", ":prisoner"),
      (assign, ":ransom", reg0), #original amount
      (val_add, ":ransom_size", ":cur_ransom"),
      (try_begin), #contributed too much, get remainder before arbitrary cap
        (gt, ":ransom_size", ":ransom"),
        (store_sub, ":ransom_amount", ":ransom", ":cur_ransom"),
      (else_try), #give full amount
        (store_sub, ":ransom_amount", ":ransom_size", ":cur_ransom"), #undo adding existing ransom
      (try_end),

      (try_begin), #active npcs have wealth
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_wealth", ":lord_no", slot_troop_wealth),
        (val_div, ":cur_wealth", 2), #at most half for contributing
        (val_min, ":cur_wealth", ":ransom"),
        (val_min, ":ransom_amount", ":cur_wealth"), #actual amount the lord can give
      (try_end),
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),
    (assign, reg0, ":ransom_amount"),
    ]
  ),

  #script_lend_money_for_ransom
  #actually parcels out the amount calculated in the above script
  ("lend_money_for_ransom", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (try_begin),
      (troop_get_slot, ":ransom_amount", ":lord_no", slot_troop_player_debt),
      (le, ":ransom_amount", 0),
      (store_script_param_2, ":ransom_amount"),
    (try_end),
    (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
    (val_add, ":cur_ransom", ":ransom_amount"), #actual amount to give

    #set up quests
    (quest_set_slot, "qst_rescue_prisoner", slot_quest_target_state, ":cur_ransom"),
    (assign, reg0, ":cur_ransom"),
    #the amount calculated at the start, will differ from expected ransom
    (quest_get_slot, reg1, "qst_rescue_prisoner", slot_quest_target_amount),
    (str_store_string, s1, "@You have raised {reg0}/{reg1} denars for the ransom"),
    (add_quest_note_from_sreg, "qst_rescue_prisoner", 4, s1, 1), #0:date, 1:giver, 2:desc 3:time

    #move actual gold
    (troop_add_gold, "trp_player", ":ransom_amount"),
    (try_begin),
      (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
      (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":lord_no"),
      (val_add, ":ransom_amount", dplmc_ransom_debt_mask), #masking this from "real" debt
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),

    ]
  ),


  #script_cf_dplmc_battle_continuation
("init_keys_array", keys_array()),
    ("setup_camera_keys", [

      # (assign, "$g_dplmc_cam_default", camera_keyboard),
      # (assign, "$g_camera_up", key_w),
      # (assign, "$g_camera_down", key_s),
      # (assign, "$g_camera_left", key_a),
      # (assign, "$g_camera_right", key_d),

      #default custom commander y/z offsets
      (call_script, "script_setup_camera_offset"),
      #these will be retained after being changed inside missions

      #deathcam
      (assign, "$g_cam_tilt_left", key_numpad_1),
      (assign, "$g_cam_tilt_right", key_numpad_3),

      (assign, "$g_camera_adjust_add", key_numpad_plus),
      (assign, "$g_camera_adjust_sub", key_numpad_minus),

      #normally numpad swaps equipment, but we're dead so w/e
      (assign, "$g_camera_rot_up", key_numpad_8),
      (assign, "$g_camera_rot_down", key_numpad_2),
      (assign, "$g_camera_rot_left", key_numpad_4),
      (assign, "$g_camera_rot_right", key_numpad_6),
    ]),

    #call when camera positions get weird
    ("setup_camera_offset",
      [
      (assign, "$g_camera_z", 200),
      (assign, "$g_camera_y", -175),
      (assign, "$g_camera_rotate_x", 0),
      (assign, "$g_camera_rotate_y", 0),
      (assign, "$g_camera_rotate_z", 0),

      ]),

    #initialize all active death cam globals
    ("init_death_cam",
      [
        (assign, "$deathcam_mouse_last_x", 5000),
        (assign, "$deathcam_mouse_last_y", 3750),
        (assign, "$deathcam_mouse_last_notmoved_x", 5000),
        (assign, "$deathcam_mouse_last_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_x", 5000), #Center screen (10k fixed pos)
        (assign, "$deathcam_mouse_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_counter", 0),

        (assign, "$deathcam_total_rotx", 0),

        (assign, "$deathcam_sensitivity_x", 200), #4:3 ratio may be best
        (assign, "$deathcam_sensitivity_y", 150), #If modified, change values in common_move_deathcam

        (assign, "$deathcam_prsnt_was_active", 0),

        (assign, "$deathcam_keyboard_rotation_x", 0),
        (assign, "$deathcam_keyboard_rotation_y", 0),

        (assign, "$g_dplmc_cam_activated", 0),
        (assign, "$dmod_current_agent", -1),
        # check if keys are not set/invalid
        (try_begin),
          (neg|is_between, "$g_dplmc_cam_default", camera_keyboard, camera_follow + 1),
          (call_script, "script_setup_camera_keys"),
          (assign, "$g_dplmc_cam_default", camera_keyboard),
        (try_end),

        (get_player_agent_no, "$g_player_agent"),
        (agent_get_team, "$g_player_team", "$g_player_agent"),
      ]),

    ("cf_cancel_camera_keys", [
      (this_or_next|game_key_is_down, gk_view_char),
      (this_or_next|game_key_is_down, gk_zoom),
      (game_key_is_down, gk_cam_toggle),
      (mission_cam_set_mode, 0),
    ]),

    ("dmod_closest_agent", [
          (assign, ":cur_agent", -1),
          (assign, ":distance", 999999),
          (mission_cam_get_position, pos11),
          (position_set_z_to_ground_level, pos11),
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            #position on the ground
            (agent_get_position, pos13, ":agent_no"),
            # (position_get_screen_projection, pos14, pos13),
            # (get_distance_between_positions, ":cur_distance", pos12, pos14),
            (get_distance_between_positions, ":cur_distance", pos11, pos13),
            (lt, ":cur_distance", ":distance"),
            (assign, ":distance", ":cur_distance"),
            (assign, ":cur_agent", ":agent_no"),
          (try_end),
          (try_begin),
            (neq, ":cur_agent", 1),
            (assign, "$dmod_current_agent", ":cur_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
          (try_end),

      ]
    ),
    # script_dmod_cycle_forwards
      # Output: New $dmod_current_agent
      # Used to cycle forwards through valid agents
      ("dmod_cycle_forwards",[

         (assign, ":agent_moved", 0),
         (assign, ":first_agent", -1),
         # (get_player_agent_no, ":player_agent"),
         # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_moved", 1),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            # (agent_get_team, ":cur_team", ":agent_no"),
            # (this_or_next|eq, ":cur_team", 5), #bodyguards
            # (eq, ":cur_team", ":player_team"),
            (try_begin),
              (lt, ":first_agent", 0),
              (assign, ":first_agent", ":agent_no"),
            (try_end),
            (gt, ":agent_no", "$dmod_current_agent"),
            (assign, "$dmod_current_agent", ":agent_no"),
            (assign, ":agent_moved", 1),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 0),
            (neq, ":first_agent", -1),
            (assign, "$dmod_current_agent", ":first_agent"),
            (assign, ":agent_moved", 1),
        (else_try),
            (eq, ":agent_moved", 0),
            (eq, ":first_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 1),
            (str_store_agent_name, s1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      #(assign, "$dmod_move_camera", 1),
      ]),

      # script_dmod_cycle_backwards
      # Output: New $dmod_current_agent
      # Used to cycle backwards through valid agents
      ("dmod_cycle_backwards",[

        (assign, ":new_agent", -1),
        (assign, ":last_agent", -1),
        # (get_player_agent_no, ":player_agent"),
        # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
        # (agent_get_team, ":cur_team", ":agent_no"),
        # (this_or_next|eq, ":cur_team", 5), #bodyguards
        # (eq, ":cur_team", ":player_team"),
            (assign, ":last_agent", ":agent_no"),
            (lt, ":agent_no", "$dmod_current_agent"),
            (assign, ":new_agent", ":agent_no"),
        (try_end),

        (try_begin),
            (eq, ":new_agent", -1),
            (neq, ":last_agent", -1),
            (assign, ":new_agent", ":last_agent"),
        (else_try),
            (eq, ":new_agent", -1),
            (eq, ":last_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (neq, ":new_agent", -1),
            (assign, "$dmod_current_agent", ":new_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      ]),



  #script_start_town_conversation

	("start_courtyard_conversation",
	[
      (store_script_param, ":conversation_troop", 1),
      (store_script_param, ":center_no", 2),

      (party_get_slot, ":conversation_scene", ":center_no", slot_town_center), #castle's exterior
      (modify_visitors_at_site, ":conversation_scene"),
      (reset_visitors),
      (try_begin), #player vs troop, not much processing
        (neg|troop_is_hero, ":conversation_troop"),

      (else_try), #talking to lords, compare relative positions
        (assign, ":supplicant", "trp_player"),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
        (assign, ":player_standing", reg0),
        (call_script, "script_dplmc_get_troop_standing_in_faction", ":conversation_troop", ":faction_no"),
        (assign, ":other_troop_standing", reg0),

        #23 : castle guard (adjacent), 2: lord's hall door
        (assign, ":entry_lower", 23),
        (assign, ":entry_upper", 2),
        #overwrite standing if center owned
        (try_begin),
          (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
          (assign, ":player_standing", 9999),
        (else_try),
          (party_slot_eq, ":center_no", slot_town_lord, ":conversation_troop"),
          (assign, ":other_troop_standing", 9999),
        (else_try), #strangers, use default street entry point (this may be outside in towns, 0 preferred)
          (this_or_next|eq, ":player_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (eq, ":other_troop_standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
          (assign, ":entry_lower", 1),
        (try_end),

        (try_begin), #player is usually supplicant
          (gt, ":player_standing", ":other_troop_standing"),
          (assign, ":supplicant", ":conversation_troop"),
          (assign, ":conversation_troop", "trp_player"),
        (else_try),
          (is_between, ":center_no", towns_begin, towns_end),
          (eq, ":player_standing", ":other_troop_standing"),
          (assign, ":entry_upper", 27),
          (assign, ":entry_lower", 28),
        (try_end),
      (try_end),

      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_lower", af_override_horse|af_override_head|af_override_weapons),
      (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_upper", af_override_horse|af_override_fullhelm),
      (set_visitor, ":entry_lower", ":supplicant"),
      (set_visitor, ":entry_upper", ":conversation_troop"),

      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene, ":conversation_scene"),
      (change_screen_map_conversation, ":conversation_troop"),
    ]),

    #talking to people within the court (after capture for instance)
    ("start_court_conversation",
    [
        (store_script_param, ":conversation_troop", 1),
        (store_script_param, ":center_no", 2),

        (party_get_slot, ":conversation_scene", ":center_no", slot_town_castle),
        (modify_visitors_at_site, ":conversation_scene"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),

        #clear flags for actual courtly conversations?
        (store_random_in_range, ":entry_no", 16, 32),
        (mission_tpl_entry_set_override_flags, "mt_conversation_encounter", ":entry_no", af_override_horse),
        (try_begin),
          (troop_is_hero, ":conversation_troop"),
          (set_visitor, ":entry_no", ":conversation_troop"),
        (else_try),
          (store_script_param, ":troop_dna", 3),
          (set_visitor, ":entry_no", ":conversation_troop", ":troop_dna"),
        (try_end),
        (set_jump_mission,"mt_conversation_encounter"),
        (jump_to_scene, ":conversation_scene"),
        (change_screen_map_conversation, ":conversation_troop"),
    ]),


    #script_companion_get_mission_string
    #input: companion troop_id
    #output: "{!}{s4}: {s8} ({s5})" to s0
    #unify the menu (rarely called) and troop notes for consistency
    #side-effects include overwriting s9, reg3, etc.
    ("companion_get_mission_string", [
        (store_script_param, ":companion", 1),
        (try_begin), #do not impose conditions here, do so from calling script
            # (this_or_next|main_party_has_troop, ":companion"),
            # (this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
                # (eq, "$g_player_minister", ":companion"),
            (str_store_troop_name, s4, ":companion"),
            (str_clear, s5),
            (str_clear, s8),
            (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),
            (troop_get_slot, ":mission", ":companion", slot_troop_current_mission),
            (try_begin),
                (le, ":days_left", 0),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (eq, ":days_left", 1),
                (str_store_string, s5, "str_expected_back_imminently"),
            (else_try),
                (assign, reg3, ":days_left"),
                (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
            (try_end),


            (try_begin),
                (eq, ":mission", npc_mission_kingsupport),
                (str_store_string, s8, "str_gathering_support"),
            (else_try),
                (this_or_next|eq, ":mission", npc_mission_gather_intel),
                (eq, ":mission", dplmc_npc_mission_rescue_prisoner), #new mission
                (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
                (str_store_party_name, s9, ":town_with_contacts"),
                (try_begin),
                  (eq, ":mission", npc_mission_gather_intel),
                  (str_store_string, s8, "str_gathering_intelligence"),
                (else_try),
                  (eq, ":mission", dplmc_npc_mission_rescue_prisoner),
                  (str_store_string, s8, "str_preparing_prison_break"),
                (try_end),
            (else_try),
                (this_or_next|is_between, ":mission", npc_mission_peace_request, npc_mission_rejoin_when_possible),
                (is_between, ":mission", dplmc_npc_mission_war_request, dplmc_npc_mission_rescue_prisoner),

                (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
                (str_store_faction_name, s9, ":faction"),
                (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
            # (else_try), #diplomacy missions

            (else_try),
                (eq, ":companion", "$g_player_minister"),
                (str_store_string, s8, "str_serving_as_minister"),
                (try_begin),
                  (is_between, "$g_player_court", centers_begin, centers_end),
                  (str_store_party_name, s9, "$g_player_court"),
                  (str_store_string, s5, "str_in_your_court_at_s9"),
                (else_try),
                  (str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
                (try_end),
            (else_try),
                (eq, ":mission", npc_mission_rejoin_when_possible),
                (str_store_string, s8, "str_attempting_to_rejoin_party"),
            (else_try),
                (main_party_has_troop, ":companion"),
                (str_store_string, s8, "str_under_arms"),
                (str_store_string, s5, "str_in_your_party"),
            (else_try),    #Companions who are in a center
                (troop_slot_ge, ":companion", slot_troop_cur_center, centers_begin),
                (str_store_string, s8, "str_separated_from_party"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),    #Companions who are (imprisoned) in a center
                (troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),
                (str_store_string, s8, "str_missing_after_battle"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (try_begin),
                    (check_quest_active, "qst_lend_companion"),
                    (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_companion", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (else_try),
                    (check_quest_active, "qst_lend_surgeon"),
                    (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_surgeon", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (try_end),
            (try_end),

            (str_store_string, s0, "str_s4_s8_s5"),
        (try_end),
        ]
      ),
    #iterates through list of obtainable soldiers (and check if the player has reclassified them to a custom class > grc_cavalry)
    #instead of going through all troops globally, we check the selected center's garrison's upgraded troops
    ("cf_troop_class_activated",
    [
        (store_script_param, ":grc", 1),
        (store_script_param, ":party_no", 2),
        (is_between, ":grc", grc_infantry, grc_everyone),
        (try_begin), #first 3 always available
          (le, ":grc", grc_cavalry),
          (assign, ":end", -1),
        (else_try),
          (party_get_num_companion_stacks, ":end", ":party_no"),

          (try_for_range, ":stack_no", 0, ":end"),
            (party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
            (neg|troop_is_hero, ":troop_no"),
            (try_begin),
              (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 0),
              (gt, ":upgrade_troop", 0),
              (troop_get_class, ":class_no", ":upgrade_troop"),
              (eq, ":class_no", ":grc"),
              (assign, ":end", -1),
            (try_end),
            (try_begin), #not found, check other upgrade
              (neq, ":end", -1),
              (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 1),
              (gt, ":upgrade_troop", 0),
              (troop_get_class, ":class_no", ":upgrade_troop"),
              (eq, ":class_no", ":grc"),
              (assign, ":end", -1),
            (try_end),
          (try_end),
        # (try_for_range, ":troop_no", soldiers_begin, soldiers_end),
          # (neg|troop_is_hero, ":troop_no"),
          # (troop_get_class, ":class", ":troop_no"),
        # (try_end),
        (try_end),
        (eq, ":end", -1),

    ]),

    ("cf_troop_is_class",
    [
        (store_script_param, ":grc", 1),
        (store_script_param, ":troop_no", 2),
        (is_between, ":grc", grc_infantry, grc_everyone), #usually $g_constable_training_type
        (gt, ":troop_no", 0), #this is usually obtained through troop_get_upgrade_troop, sanitize it here

        (troop_get_class, ":class_no", ":troop_no"),
        (eq, ":grc", ":class_no"),
    ]),
    #script_dplmc_npc_morale
    #input: sreg, other info based off global background_answer variables
    #output: story to s0, side effects are reg11, s10 through s13
    ("build_background_answer_story", [
        (store_script_param_1, ":sreg"),
        (assign, reg11, "$character_gender"),
        (store_sub, ":string", "$background_answer_4", cb4_revenge),
        (val_add, ":string", "str_story_reason_revenge"),
        (str_store_string, s13, ":string"),
        (store_sub, ":string", "$background_answer_3", dplmc_cb3_bravo),
        (val_add, ":string", "str_story_job_bravo"),
        (str_store_string, s12, ":string"),
        (store_sub, ":string", "$background_answer_2", cb2_page), #values for this start from 0
        (val_add, ":string", "str_story_childhood_page"),
        (str_store_string, s11, ":string"),
        (store_sub, ":string", "$background_type", cb_noble),
        (val_add, ":string", "str_story_parent_noble"),
        (str_store_string, s10, ":string"),
        (str_store_string, ":sreg", "str_story_all"),
    ]),

    #whenever the player does something nice, spectators cheer
    ("agents_cheer_during_training", [
      (party_get_morale, ":cur_morale", "p_main_party"),
      (assign, ":boundary", 150),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        # (agent_get_troop_id, ":troop_no", ":agent_no"), #a spectator
        (neg|agent_has_item_equipped, ":agent_no", "itm_practice_boots"),
        (store_random_in_range, ":random_no", ":cur_morale", 250),
        (gt, ":random_no", ":boundary"),
        (val_add, ":boundary", 15),
        (agent_set_animation, ":agent_no", "anim_cheer"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
    ]),

    #a separate trigger handles when they're actually knocked out
    ("troop_set_training_health_from_agent", [
      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        # (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":troop_no", ":agent_no"),
        (troop_is_hero, ":troop_no"),
        (store_troop_health, ":health", ":troop_no", 0), #this is not yet deducted
        (store_agent_hit_points, ":hp", ":agent_no", 0),
        (val_sub, ":hp", ":health"), #this is the difference
        (try_begin),
          (agent_is_alive, ":agent_no"),
          (store_skill_level, ":skill", "skl_first_aid", ":troop_no"),
          (val_add, ":skill", ":first_aid"),
        (else_try),
          (assign, ":skill", ":first_aid"),
        (try_end),
        (val_mul, ":skill", -5),  #as per skill description
        (val_add, ":skill", 100), # 100 - skill effect
        #apply skill effect and set health
        (val_mul, ":hp", ":skill"),
        (val_div, ":hp", 100),
        (val_add, ":hp", ":health"), #subtract modified difference
        (troop_set_health, ":troop_no", ":hp", 0),
      (try_end),
    ]),

    #script_agent_apply_training_health
    #input: player_agent, called from abm_training during melee fights, can also be used for tournament if desired
    ("agent_apply_training_health", [
      (store_script_param_1, ":agent_no"),
      # (store_script_param_2, "$current_town"),

      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
      (party_get_slot, ":relation", "$current_town", slot_center_player_relation), #range from -100 to 100
      (store_sub, ":relation", 200, ":relation"), #300 to 100

      (store_troop_health, ":health", "trp_player", 0), #this is not yet deducted
      (store_agent_hit_points, ":hp", ":agent_no", 0),

      (val_sub, ":hp", ":health"), #this is the difference (non-positive)
      (try_begin),
        (agent_is_alive, ":agent_no"),
        (store_skill_level, ":skill", "skl_first_aid", "trp_player"),
      (else_try),
        (assign, ":skill", 0),
      (try_end),
      (val_add, ":skill", ":first_aid"),
      (val_mul, ":skill", -5),  #as per skill description
      (val_add, ":skill", 100), # 100 - skill effect
      #apply skill effect, relation effect and set health
      (val_mul, ":hp", ":skill"),
      (val_div, ":hp", 100),
      (val_mul, ":hp", ":relation"),
      (val_div, ":hp", 200),
      (val_add, ":health", ":hp"), #subtract modified difference
      (val_max, ":health", 5),
      (troop_set_health, "trp_player", ":health", 0),
    ]),

    # script_party_heal_all_members_aux, opposite of script_party_wound_all_members_aux
    # Input: arg1 = party_no
    ("party_heal_all_members_aux",
      [
        (store_script_param_1, ":party_no"),

        (party_get_num_companion_stacks, ":num_stacks",":party_no"),
        (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
          (try_begin),
            (neg|troop_is_hero, ":stack_troop"),
            # (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
            (party_stack_get_num_wounded, ":stack_size",":party_no",":i_stack"),
            (party_add_members, ":party_no", ":stack_troop", ":stack_size"),
            (party_remove_members_wounded_first, ":party_no", ":stack_troop", ":stack_size"),
          (else_try),
            (troop_set_health, ":stack_troop", 100),
          (try_end),
        (try_end),
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_party_heal_all_members_aux", ":attached_party"),
        (try_end),
      ]
    ),

  #script_cf_village_normal_cond
  # INPUT: center, usually $current_town
  # OUTPUT: none
  ("get_chest_troop",
  [
    (store_script_param, ":party_no", 1),
    (try_begin),
        (gt, "$g_player_chamberlain", 0),
        (assign, ":chest_troop", "trp_household_possessions"),
    (else_try), #assume troops same order as parties
        # (party_get_slot, ":chest_troop", ":party_no", slot_town_seneschal),
        (val_sub, ":party_no", towns_begin),
        (store_add, ":chest_troop", ":party_no", "trp_town_1_seneschal"),
    (try_end),
    (assign, reg0, ":chest_troop"),
  ]),

	#script_change_faction_troop_morale
    #input: troop, head or tail, sreg
    #output: reg0 as head or tail, sreg holding a short description
    ("cf_troop_debug_range",
    [
        (store_script_param, ":troop_no", 1),
        (store_script_param, ":sreg", 2),
        (store_script_param, ":direction", 3),
        (assign, ":result", ":troop_no"),
        (try_begin),
          (is_between, ":troop_no", heroes_begin, heroes_end),
          (str_store_string, ":sreg", "@hero"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", heroes_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", heroes_end, ":direction"),
          (try_end),
          (try_begin),
            (is_between, ":troop_no", companions_begin, companions_end),
            (str_store_string, ":sreg", "@companion"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", companions_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", companions_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", kings_begin, kings_end),
            (str_store_string, ":sreg", "@king"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", kings_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", kings_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", lords_begin, lords_end),
            (str_store_string, ":sreg", "@lord"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", lords_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", lords_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", pretenders_begin, pretenders_end),
            (str_store_string, ":sreg", "@pretender"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", pretenders_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", pretenders_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
            (str_store_string, ":sreg", "@lady"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", kingdom_ladies_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", kingdom_ladies_end, ":direction"),
            (try_end),
          (try_end),
        (else_try),
          (is_between, ":troop_no", bandits_begin, bandits_end),
          (str_store_string, ":sreg", "@bandit"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", bandits_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", bandits_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
          (str_store_string, ":sreg", "@minstrel"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", tavern_minstrels_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", tavern_minstrels_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
          (str_store_string, ":sreg", "@bookseller"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", tavern_booksellers_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", tavern_booksellers_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
          (str_store_string, ":sreg", "@traveler"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", tavern_travelers_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", tavern_travelers_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
          (str_store_string, ":sreg", "@ransom broker"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", ransom_brokers_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", ransom_brokers_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
          (str_store_string, ":sreg", "@mercenary"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", mercenary_troops_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", mercenary_troops_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", multiplayer_troops_begin, multiplayer_troops_end),
          (str_store_string, ":sreg", "@multiplayer troop"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", multiplayer_troops_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", multiplayer_troops_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", quick_battle_troops_begin, quick_battle_troops_end),
          (str_store_string, ":sreg", "@quick battler"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", quick_battle_troops_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", quick_battle_troops_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", training_ground_trainers_begin, training_ground_trainers_end),
          (str_store_string, ":sreg", "@trainer"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", training_ground_trainers_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", training_ground_trainers_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", arena_masters_begin, arena_masters_end),
          (str_store_string, ":sreg", "@arena master"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", arena_masters_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", arena_masters_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", walkers_begin, walkers_end),
          (str_store_string, ":sreg", "@walker"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", walkers_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", walkers_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", merchants_begin, merchants_end),
          (str_store_string, ":sreg", "@merchant"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", merchants_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", merchants_end, ":direction"),
          (try_end),
          (try_begin),
            (is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
            (str_store_string, ":sreg", "@armor merchant"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", armor_merchants_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", armor_merchants_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
            (str_store_string, ":sreg", "@weapon merchant"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", weapon_merchants_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", weapon_merchants_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", tavernkeepers_begin, tavernkeepers_end),
            (str_store_string, ":sreg", "@tavernkeeper"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", tavernkeepers_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", tavernkeepers_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", goods_merchants_begin, goods_merchants_end),
            (str_store_string, ":sreg", "@goods merchant"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", goods_merchants_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", goods_merchants_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", horse_merchants_begin, horse_merchants_end),
            (str_store_string, ":sreg", "@horse merchant"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", horse_merchants_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", horse_merchants_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", mayors_begin, mayors_end),
            (str_store_string, ":sreg", "@guildmaster"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", mayors_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", mayors_end, ":direction"),
            (try_end),
          (else_try),
            (is_between, ":troop_no", village_elders_begin, village_elders_end),
            (str_store_string, ":sreg", "@village elder"),
            (try_begin),
              (eq, ":direction", -1),
              (assign, ":result", village_elders_begin),
            (else_try),
              (eq, ":direction", 1),
              (store_sub, ":result", village_elders_end, ":direction"),
            (try_end),
          (try_end),
        (else_try),
          (is_between, ":troop_no", startup_merchants_begin, startup_merchants_end),
          (str_store_string, ":sreg", "@startup merchant"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", startup_merchants_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", startup_merchants_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", tournament_champions_begin, tournament_champions_end),
          (str_store_string, ":sreg", "@tournament fighter"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", tournament_champions_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", tournament_champions_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", dplmc_employees_begin, dplmc_employees_end),
          (str_store_string, ":sreg", "@court member"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", dplmc_employees_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", dplmc_employees_end, ":direction"),
          (try_end),
        (else_try),
          (is_between, ":troop_no", fighters_begin, fighters_end),
          (str_store_string, ":sreg", "@fighter"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", fighters_begin),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", fighters_end, ":direction"),
          (try_end),
        (else_try), #sarranids
          (is_between, ":troop_no", "trp_sarranid_recruit", "trp_looter"),
          (str_store_string, ":sreg", "str_kingdom_6_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_sarranid_recruit"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_looter", ":direction"),
          (try_end),
        (else_try), #rhodoks
          (is_between, ":troop_no", "trp_rhodok_tribesman", "trp_sarranid_recruit"),
          (str_store_string, ":sreg", "str_kingdom_5_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_rhodok_tribesman"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_sarranid_recruit", ":direction"),
          (try_end),
        (else_try), #nords
          (is_between, ":troop_no", "trp_nord_recruit", "trp_rhodok_tribesman"),
          (str_store_string, ":sreg", "str_kingdom_4_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_nord_recruit"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_rhodok_tribesman", ":direction"),
          (try_end),
        (else_try), #khergits
          (is_between, ":troop_no", "trp_khergit_tribesman", "trp_nord_recruit"),
          (str_store_string, ":sreg", "str_kingdom_3_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_khergit_tribesman"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_nord_recruit", ":direction"),
          (try_end),
        (else_try), #vaegirs
          (is_between, ":troop_no", "trp_vaegir_recruit", "trp_khergit_tribesman"),
          (str_store_string, ":sreg", "str_kingdom_2_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_vaegir_recruit"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_khergit_tribesman", ":direction"),
          (try_end),
        (else_try), #swadians
          (is_between, ":troop_no", "trp_swadian_recruit", "trp_vaegir_recruit"),
          (str_store_string, ":sreg", "str_kingdom_1_adjective"),
          (try_begin),
            (eq, ":direction", -1),
            (assign, ":result", "trp_swadian_recruit"),
          (else_try),
            (eq, ":direction", 1),
            (store_sub, ":result", "trp_vaegir_recruit", ":direction"),
          (try_end),
        (try_end),
        (this_or_next|eq, ":direction", 0),
        (neq, ":result", ":troop_no"),
        (assign, reg0, ":result"),

    ]),

    #script_get_proficient_melee_training_weapon
    #input : troop_no
    #output : item_no as the practice weapon
    ("get_proficient_melee_training_weapon",
    [
        (store_script_param, ":troop_no", 1),
        (store_proficiency_level, ":onehands", ":troop_no", wpt_one_handed_weapon),
        (store_proficiency_level, ":twohands", ":troop_no", wpt_two_handed_weapon),
        (store_proficiency_level, ":polearms", ":troop_no", wpt_polearm),

        (assign, ":item_no", -1),
        (try_begin), #practice shield will be added automatically
          (ge, ":onehands", ":twohands"),
          (ge, ":onehands", ":polearms"),
          # (agent_equip_item, ":agent_no", "itm_practice_shield"),
          (assign, ":item_no", "itm_practice_sword"),
        (else_try),
          (ge, ":twohands", ":onehands"),
          (ge, ":twohands", ":polearms"),
          (assign, ":item_no", "itm_heavy_practice_sword"),
        (else_try),
          (ge, ":polearms", ":onehands"),
          (ge, ":polearms", ":twohands"),
          (assign, ":item_no", "itm_practice_staff"),
        (try_end),
        (assign, reg0, ":item_no"),
    ]),

  # script_spawn_looters
  # Input: arg1 = center_no, arg2 = number of looters to spawn
  # Output: none
  ("spawn_looters",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":num_looters", 2),
      # (party_set_slot, ":center_no", slot_center_is_besieged_by, -1), #clear siege
      # (call_script, "script_village_set_state",  ":center_no", 0), #clear siege flag
      (set_spawn_radius, 4),
      (try_for_range, ":unused", 0, ":num_looters"),
        (spawn_around_party, ":center_no", "pt_looters"),
        #(party_set_ai_behavior, reg0, ai_bhvr_avoid_party),
        #(party_set_ai_object, reg0, ":center_no"),
      (try_end),
    ]),

  #script_troop_transfer_gold
  ("troop_transfer_gold",
    [
      (store_script_param, ":source", 1),
      (store_script_param, ":destination", 2),
      (store_script_param, ":amount", 3),
      (store_troop_gold, ":cur_amount", ":source"),
      (try_begin),
        (gt, ":amount", 0), #0 means move all
        (val_min, ":cur_amount", ":amount"),
      (try_end),
      (troop_remove_gold, ":source", ":cur_amount"),
      # (troop_add_gold, ":destination", ":cur_amount"),
      (call_script, "script_troop_add_gold", ":destination", ":cur_amount"),
      (assign, reg0, ":cur_amount"),
    ]),
  # script_move_inventory_and_gold
   #calculate the string offset by iteratively dividing by 2
   ("get_disguise_string", [
      (store_script_param, ":cur_val", 1),
      (store_script_param, ":sreg", 2),
      (store_add, ":end_val", "str_pilgrim_disguise", num_disguises),
      (str_clear, ":sreg"),
      (try_for_range, ":string", "str_pilgrim_disguise", ":end_val"),
        (eq, ":cur_val", 1), #
        (assign, ":end_val", -1), #loop break
        (str_store_string, ":sreg", ":string"),
      (else_try),
        (val_div, ":cur_val", 2), #divide by 2, next iteration
      (try_end),
      ]),
   #script_acquire_disguise
   #lets the player use the disguise by setting the slot, shows message
   ("acquire_disguise", [
      (store_script_param, ":disguise", 1),
      (troop_get_slot, ":cur_disguise", "trp_player", slot_troop_player_disguise_sets),
      (val_or, ":cur_disguise", ":disguise"),
      (troop_set_slot, "trp_player", slot_troop_player_disguise_sets, ":cur_disguise"),
      (call_script, "script_get_disguise_string", ":disguise", 0),
      # (str_store_string, s0, reg0),
      (display_message, "@Acquired {s0}'s clothing", message_alert),
      ]),
   #script_set_disguise_overide_items
   #see also start of module_mission_templates for static list of items
   #note that the override flags are not being set here
   ("set_disguise_override_items", [
      (store_script_param, ":mission_template", 1),
      (store_script_param, ":entry_no", 2),
      (store_script_param, ":with_weapon", 3),

      (mission_tpl_entry_clear_override_items, ":mission_template", ":entry_no"),
      (try_begin),
        (eq, "$sneaked_into_town", disguise_pilgrim),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_disguise"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_pilgrim_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_wrapping_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_practice_staff"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_throwing_daggers"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_farmer),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_hat"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_coarse_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_nomad_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_battle_fork"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_cleaver"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_stones"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_hunter),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_black_hood"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_gloves"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_light_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_sword_khergit_1"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_hunting_bow"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_barbed_arrows"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_merchant),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jacket"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_woolen_hose"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_felt_steppe_cap"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_dagger"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_guard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_footman_helmet"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_mittens"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_shirt"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_jerkin"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_mail_chausses"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_fighting_pick"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_tab_shield_round_c"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_war_spear"),
        (try_end),
      (else_try),
        (eq, "$sneaked_into_town", disguise_bard),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_linen_tunic"),
        (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_leather_boots"),
        (try_begin),
          (eq, ":with_weapon", 1),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_winged_mace"),
          (mission_tpl_entry_add_override_item, ":mission_template", ":entry_no", "itm_lyre"),
        (try_end),
      (try_end),
   ]),


    ("get_dest_color_from_rgb",
    [
      (store_script_param, ":red", 1),
      (store_script_param, ":green", 2),
      (store_script_param, ":blue", 3),

      (assign, ":cur_color", 0xFF000000),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":cur_color", ":blue"),
      (val_add, ":cur_color", ":green"),
      (val_add, ":cur_color", ":red"),
      (assign, reg0, ":cur_color"),
    ]),

    ("convert_rgb_code_to_html_code",
    [
      (store_script_param, ":red", 1),
      (store_script_param, ":green", 2),
      (store_script_param, ":blue", 3),

      # (str_store_string, s0, "@#"),

      (store_div, reg11, ":red", 0x10),
      #(store_add, ":dest_string", "str_key_0", reg11"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg12, ":red", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":r_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_div, reg13, ":green", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":g_1"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg14, ":green", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":g_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_div, reg15, ":blue", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":b_1"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),

      (store_mod, reg16, ":blue", 0x10),
      #(store_add, ":dest_string", "str_key_0", ":b_2"),
      #(str_store_string, s1, ":dest_string"),
      #(str_store_string, s0, "@{s0}{s1}"),
      (str_store_string, s0, "str_html_color"),
    ]),

    ("convert_slot_no_to_color",
    [
      (store_script_param, ":cur_color", 1),

      (store_mod, ":blue", ":cur_color", 6),
      (val_div, ":cur_color", 6),
      (store_mod, ":green", ":cur_color", 6),
      (val_div, ":cur_color", 6),
      (store_mod, ":red", ":cur_color", 6),
      (val_mul, ":blue", 0x33),
      (val_mul, ":green", 0x33),
      (val_mul, ":red", 0x33),
      (assign, ":dest_color", 0xFF000000),
      (val_mul, ":green", 0x100),
      (val_mul, ":red", 0x10000),
      (val_add, ":dest_color", ":blue"),
      (val_add, ":dest_color", ":green"),
      (val_add, ":dest_color", ":red"),
      (assign, reg0, ":dest_color"),
    ]),

    ("change_color",
    [
      (call_script, "script_get_dest_color_from_rgb", reg2, reg3, reg4),
      (assign, ":cur_color", reg0),
      (overlay_set_color, "$g_presentation_obj_2", ":cur_color"),
      (try_begin),
        (eq, "$g_presentation_state", recolor_kingdom),
        (troop_get_slot, ":cur_faction", "trp_temp_array_a", "$temp"),
        (faction_set_color, ":cur_faction", ":cur_color"),
      (else_try),
        (eq, "$g_presentation_state", recolor_heraldic),
        (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
        (val_sub, ":banner", banner_scene_props_begin),
        (troop_set_slot, "trp_banner_background_color_array", ":banner", ":cur_color"),
      (else_try),
        (eq, "$g_presentation_state", recolor_groups),
        (troop_set_slot, "trp_multiplayer_data", "$temp", ":cur_color"),
      (try_end),
      (call_script, "script_convert_rgb_code_to_html_code", reg2, reg3, reg4),
      (overlay_set_text, "$g_presentation_obj_9", "str_html"),
    ]),


#WSE

#script_wse_multiplayer_message_received
# Called each time a composite multiplayer message is received
# INPUT
# script param 1 = sender player no
# script param 2 = event no
("wse_multiplayer_message_received", [
]),

#script_wse_game_saved
# Called each time after game is saved successfully
("wse_game_saved", [
]),

#script_wse_chat_message_received
# Called each time a chat message is received (both for servers and clients)
# INPUT
# script param 1 = sender player no
# script param 2 = chat type (0 = global, 1 = team)
# s0 = message
# OUTPUT
# trigger result = anything non-zero suppresses default chat behavior. Server will not even broadcast messages to clients.
# result string = changes message text for default chat behavior (if not suppressed).
("wse_chat_message_received", [
]),

#script_wse_console_command_received
# Called each time a command is typed on the dedicated server console or received with RCON (after parsing standard commands)
# INPUT
# script param 1 = command type (0 - local, 1 - remote)
# s0 = text
# OUTPUT
# trigger result = anything non-zero if the command succeeded
# result string = message to display on success (if empty, default message will be used)
("wse_console_command_received", [
]),

#script_wse_get_agent_scale
# Called each time an agent is created
# INPUT
# script param 1 = troop no
# script param 2 = horse item no
# script param 3 = horse item modifier
# script param 4 = player no
# OUTPUT
# trigger result = agent scale (fixed point)
("wse_get_agent_scale", [

    # (set_fixed_point_multiplier, 100),

    # (assign, ":scale", 100),

    # # (try_begin),
        # # (gt, ":horse_item_no", -1),
        # # (eq, ":horse_item_modifier", imodbit_heavy),
        # # (val_add, ":scale", 5),
        # # (set_trigger_result, ":scale"),
    # # (try_end),

    # (try_begin),
        # (gt, ":troop_no", -1),
        # (neg|troop_is_hero, ":troop_no"),
        # (troop_get_type, ":type", ":troop_no"),
        # (lt, ":type", 2),
        # (store_random_in_range, ":scale", 95, 105),
        # (store_attribute_level, ":str", ":troop_no", ca_strength),
        # (val_sub, ":str", 6),
        # (val_div, ":str", 3),
        # (val_add, ":scale", ":str"),

        # (try_begin),
            # (eq, ":type", 1),
            # (val_mul, ":scale", 93),
            # (val_div, ":scale", 100),
        # (try_end),

        # # (assign, reg0, ":scale"),
        # # (display_message, "@{reg0}"),

        # (set_trigger_result, ":scale"),
    # (try_end),


]),

#script_wse_window_opened
# Called each time a window (party/inventory/character) is opened
# INPUT
# script param 1 = window no
# script param 2 = window param 1
# script param 3 = window param 2
# OUTPUT
# trigger result = presentation that replaces the window (if not set or negative, window will open normally)
("wse_window_opened", [
]),

#script_game_missile_dives_into_water
# Called each time a missile dives into water
# INPUT
# script param 1 = missile item no
# script param 2 = missile item modifier
# script param 3 = launcher item no
# script param 4 = launcher item modifier
# script param 5 = shooter agent no
# script param 6 = missile no
# pos1 = water impact position and rotation
("game_missile_dives_into_water", [
	# (store_script_param, ":launcher_item_modifier", 4),
	# (store_script_param, ":shooter_agent_no", 5),
	# (store_script_param, ":missile_no", 6),

    (play_sound_at_position, "snd_jump_end_water", pos1),
    (particle_system_burst, "psys_game_water_splash_2", pos1, 40),

]),

#script_all_enemies_routed
# This script checks that all enemies are routed or killed.
# INPUT: none
# OUTPUT: reg0 = enemies routed 0 or 1
("all_enemies_routed", [
  (assign, ":enemies_remaining", 0),
  (try_for_agents, ":agent"),
    (neg|agent_is_ally, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_slot, ":routing", ":agent", slot_agent_is_running_away),
    (eq, ":routing", 0),
    (val_add, ":enemies_remaining", 1),
  (try_end),
  (assign, reg10, ":enemies_remaining"),
]),

#jacobhinds Morale Code BEGIN

#script_cf_calculate_battle_ratio
#assigns battle size difference
#Inputs = none
#Outputs = none
	("cf_calculate_battle_ratio",
		[
			#bugfix; prevents earlier scripts from enforcing
			#fixed_point_* operations
			#(set_fixed_point_multiplier, 1),

			(assign, "$battle_ratio", 0),

			(assign, "$j_num_us_ready", 0),
			(assign, "$j_num_us_wounded", 0),
			(assign, "$j_num_us_routed", 0),
			(assign, "$j_num_us_dead", 0),

			(assign, "$j_num_allies_ready", 0),
			(assign, "$j_num_allies_wounded", 0),
			(assign, "$j_num_allies_routed", 0),
			(assign, "$j_num_allies_dead", 0),

			(assign, "$j_num_enemies_ready", 0),
			(assign, "$j_num_enemies_wounded", 0),
			(assign, "$j_num_enemies_routed", 0),
			(assign, "$j_num_enemies_dead", 0),

			#count and categorize agents (me, ally, enemy/wounded, dead, routed, alive)
			(try_for_agents, ":cur_agent"),
			  (agent_is_human, ":cur_agent"),
			  (agent_get_party_id, ":agent_party", ":cur_agent"),
			  (try_begin),
				(eq, ":agent_party", "p_main_party"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_us_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_us_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_us_routed", 1),
				(else_try),
				  (val_add, "$j_num_us_dead", 1),
				(try_end),
			  (else_try),
				(agent_is_ally, ":cur_agent"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_allies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_allies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_allies_routed", 1),
				(else_try),
				  (val_add, "$j_num_allies_dead", 1),
				(try_end),
			  (else_try),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_enemies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_enemies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_enemies_routed", 1),
				(else_try),
				  (val_add, "$j_num_enemies_dead", 1),
				(try_end),
			  (try_end),
			(try_end),

			#don't think I need these
			# (assign, ":ratio", 0),
			# (assign, ":ratio_3", 0),
			# (assign, ":difference", 0),
			# (assign, ":enemy_sqrt", 0),
			# (assign, ":ally_sqrt", 0),

			# ALLY STRENGTH
			(assign, ":ally_strength", 1),
			(val_add, ":ally_strength", "$j_num_enemies_routed"),
			(val_add, ":ally_strength", "$j_num_enemies_dead"),
			(val_add, ":ally_strength", "$j_num_enemies_wounded"),
			#ready is counted three times
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),

			# ENEMY STRENGTH
			(assign, ":enemy_strength", 1),
			(val_add, ":enemy_strength", "$j_num_us_dead"),
			(val_add, ":enemy_strength", "$j_num_us_wounded"),
			(val_add, ":enemy_strength", "$j_num_us_routed"),
			(val_add, ":enemy_strength", "$j_num_allies_dead"),
			(val_add, ":enemy_strength", "$j_num_allies_wounded"),
			(val_add, ":enemy_strength", "$j_num_allies_routed"),
			#ready is counted three times
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),

			#(A*10/E)
			#10/1 ratio = 10,000 morale penalty
			(store_mul, ":enemy_value", ":enemy_strength", battle_ratio_multiple),
			(val_div, ":enemy_value", ":ally_strength"),

			#(E*10/A)
			(store_mul, ":ally_value", ":ally_strength", battle_ratio_multiple),
			(val_div, ":ally_value", ":enemy_strength"),

			#if enemy value is greater, use negative of that.
			(try_begin),
				(gt, ":enemy_value", ":ally_value"),
				(val_sub, ":enemy_value", battle_ratio_multiple),
				(store_sub, ":enemy_value", 0, ":enemy_value"),
				(assign, "$battle_ratio", ":enemy_value"),
			(else_try),
				(val_sub, ":ally_value", battle_ratio_multiple),
				(assign, "$battle_ratio", ":ally_value"),
			(try_end),

			#(val_clamp, "$battle_ratio", -max_ratio, max_ratio),

			# (assign, reg2, ":enemy_value"),
			# (assign, reg1, ":ally_value"),

			#(assign, reg0, "$battle_ratio"),
			#(display_message, "@Battle Ratio:{reg0}"),


			#(sqrt A - sqrt E)^3 + (A-E) (unused)

				#(sqrt A - sqrt E)^3
				# (store_sqrt, ":enemy_sqrt", ":enemy_strength"),
				# (store_sqrt, ":ally_sqrt", ":ally_strength"),
				# (store_sub, ":ratio", ":ally_sqrt", ":enemy_sqrt"),
				# #I get the feeling store_pow doesn't work or is deprecated in some way; keep getting weird results
				# #perhaps use cumbersome approach instead:
				# (store_pow, ":ratio_3", ":ratio", 3),
				# # (store_mul, ":ratio_3", ":ratio", ":ratio"), #squared
				# # (val_mul, ":ratio_3", ":ratio"), #cubed

				# #(A-E)
				# (store_sub, ":difference", ":ally_strength", ":enemy_strength"),

			# (store_add, "$battle_ratio", ":difference", ":ratio_3"),
			# (val_mul, "$battle_ratio", 10),
			# (val_mul, "$battle_ratio", 10),

		#housekeeping BEGIN
			# (assign, reg2, "$battle_ratio"),
			# (assign, reg3, ":ally_strength"),
			# (assign, reg4, ":enemy_strength"),
			# (display_message, "@{reg3}/{reg4}={reg2}"),

			#find average morale for each side
			# (assign, ":enemy_morale", 1),
			# (assign, ":ally_morale", 1),
			# (assign, ":ally_amount", 1),

			#store morale for all troops
			# (try_for_agents,":cur_agent"),
				# (agent_is_human, ":cur_agent"),
				# (agent_is_alive, ":cur_agent"),
				# (agent_get_slot, ":agent_courage_score", ":cur_agent", slot_agent_courage_score),
				# (try_begin),
					# (agent_is_ally, ":cur_agent"),
					# (val_add, ":ally_morale", ":agent_courage_score"),
				# (else_try),
					# (val_add, ":enemy_morale", ":agent_courage_score"),
				# (try_end),
			# (try_end),

			# (store_add, ":ally_amount", "$j_num_us_ready", "$j_num_allies_ready"),

			# (store_div, reg6, ":ally_morale", ":ally_amount"),
			# (store_div, reg7, ":enemy_morale", "$j_num_enemies_ready"),
			# (display_message, "@Morale: {reg6}/{reg7}"),

			#check that fixed_point_whatever or something else isn't screwing me over
			#answer: it is, and tends to fluctuate
			# (store_sqrt, ":four", 16),
			# (assign, reg5, ":four"),
			# (display_message, "@the square root of sixteen is {reg5}"),
		#housekeeping END

			#100-10	= ~400
			#100-30	= ~150
			#100-50	= ~75

			#50-10	= ~100
			#50-30	= ~25
			#50-40	= ~10
		]
	),

#scipt_cf_agent_can_rout
#determines whether a troop can rout or not (more than 10% casualties)
#input: cur_agent
("cf_agent_can_rout", [
	(store_script_param, ":agent", 1),

	(try_begin),
		(agent_is_ally, ":agent"),
		#count ready allies
		(assign, ":ready", "$j_num_us_ready"),
		(val_add, ":ready", "$j_num_allies_ready"),

		#count deady allies
		(store_add, ":deady", "$j_num_us_wounded", "$j_num_us_routed"),
		(val_add, ":deady", "$j_num_us_dead"),
		(val_add, ":deady", "$j_num_allies_wounded"),
		(val_add, ":deady", "$j_num_allies_routed"),
		(val_add, ":deady", "$j_num_allies_dead"),
		(val_mul, ":deady", 10),
	(else_try),
		#count ready enemies
		(assign, ":ready", "$j_num_enemies_ready"),

		#count deady enemies
		(store_add, ":deady", "$j_num_enemies_wounded", "$j_num_enemies_routed"),
		(val_add, ":deady", "$j_num_enemies_dead"),
		(val_mul, ":deady", 10),
	(try_end),
	# (display_message, "@agents cannot rout"),
	(gt, ":deady", ":ready"),
	# (display_message, "@agents can rout"),
]),
#jacobhinds Morale Code END

###dckplmc scripts - begin TODO: append in different file

  # script_setup_camp_scene
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("setup_camp_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (try_begin),
        (this_or_next|eq, ":terrain_type", rt_steppe),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_camp_scene_steppe"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_plain),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_snow),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_camp_scene_snow"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_desert),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_camp_scene_desert"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water), #figure this out later
        (assign, ":scene_to_use", "scn_sea_1"),

        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (eq, ":ship_type", 1),
          (assign, ":scene_to_use", "scn_sea_1"),
        (else_try),
          (eq, ":ship_type", 2),
          (assign, ":scene_to_use", "scn_sea_2"),
        (else_try),
          (eq, ":ship_type", 3),
          (assign, ":scene_to_use", "scn_sea_3"),
        (else_try),
          (eq, ":ship_type", 4),
          (assign, ":scene_to_use", "scn_sea_4"),
        (try_end),

       (try_for_range, ":entry_no", 33, 40),
         (mission_tpl_entry_set_override_flags, "mt_camp", ":entry_no", af_override_horse),
       (try_end),

      (else_try),
        (eq, ":terrain_type", rt_bridge),
		(try_for_parties, ":party_no"),
			(is_between, ":party_no", "p_bridge_1", "p_looter_spawn_point"),
			(store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
			(lt, ":distance", 2),
			(party_get_icon, ":icon", ":party_no"),
			(try_begin),
				(eq, ":icon", "icon_bridge_snow_a"),
				(assign, ":scene_to_use", "scn_camp_scene_snow"),
			(else_try),
				(assign, ":scene_to_use", "scn_camp_scene_plain"),
			(try_end),
		(try_end),
      (try_end),
	  (modify_visitors_at_site, ":scene_to_use"),
	  (reset_visitors),
	# (set_visitor,1,"trp_follower_woman"),

	(assign, ":cur_entry", 2),

    (assign, ":entry_1_assigned", 0),

    (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),

   (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":num_stacks"), #1st pass: grab all heroes
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
         (eq, ":cur_troop_id", ":spouse"),
		 (set_visitor, 1, ":cur_troop_id"), #is spouse
         (assign, ":entry_1_assigned", 1),
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (val_add, ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (try_for_range, ":troop_iterator", 0, ":num_stacks"),
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
		 (party_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (party_stack_get_num_wounded, ":num_wounded","p_main_party",":troop_iterator"),
		 (val_sub, ":stack_size", ":num_wounded"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 40),
				(assign, ":stack_size", -1), #break the loop
             (else_try),
                 (neq, ":entry_1_assigned", 1),
                 (this_or_next|eq, ":cur_troop_id", "trp_prostitute"),
                 (eq, ":cur_troop_id", "trp_courtesan"),
                 (set_visitor, 1, ":cur_troop_id"),
                 (assign, ":entry_1_assigned", 1),
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	#prisoners
	(assign, ":cur_entry", 40),
	(party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
    (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"), #1st pass: grab all heroes
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":prisoner_stacks"), #break the loop
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (store_add, ":cur_entry", ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"),
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":num_stacks"), #break the loop
	 (else_try),
		 (party_prisoner_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 48),
				(assign, ":stack_size", -1), #break the loop
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	(mission_tpl_entry_clear_override_items,"mt_camp",1),
	(store_random_in_range,":r",0,2),
	(try_begin),
		(eq,":r",0),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lute"),
	(else_try),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lyre"),
	(try_end),

	  (assign, "$talk_context", tc_camp_talk),
      (jump_to_scene,":scene_to_use"),
  ]),

  #script_training_ground_sub_routine_2_for_melee_details_fuck
  # script_field_start_position by motomataru
  # Input: team
  # Output: pos2 = current army position advanced by cavalry wedge depth over
  # infantry formation depth
  # Originally written to prevent map border accidents when setting up player
  # army at its spawn point
  ("field_start_position", [
      (store_script_param, ":fteam", 1),

      (assign, ":depth_cavalry", 0),
      (assign, ":largest_mounted_division_size", 0),
      (team_get_leader, ":fleader", ":fteam"),

      (try_begin),
        (ge, ":fleader", 0),
        (agent_get_position, pos2, ":fleader"),
      (else_try),
        (call_script, "script_battlegroup_get_position", pos2, ":fteam", grc_everyone),
      (try_end),

      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_slot_eq, ":fteam", ":slot", sdt_cavalry),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (lt, ":largest_mounted_division_size", reg0),
        (assign, ":largest_mounted_division_size", reg0),
      (try_end),

      (try_begin),
        (gt, ":largest_mounted_division_size", 0),
        (val_mul, ":largest_mounted_division_size", 2),
        (convert_to_fixed_point, ":largest_mounted_division_size"),
        (store_sqrt, ":depth_cavalry", ":largest_mounted_division_size"),
        (convert_from_fixed_point, ":depth_cavalry"),
        (val_sub, ":depth_cavalry", 1),

        (store_mul, reg0, formation_start_spread_out, 50),
        (val_add, reg0, formation_minimum_spacing_horse_length),
        (val_mul, ":depth_cavalry", reg0),

        (store_mul, ":depth_infantry", formation_start_spread_out, 50),
        (val_add, ":depth_infantry", formation_minimum_spacing),
        (val_mul, ":depth_infantry", 2),
        (val_sub, ":depth_cavalry", ":depth_infantry"),

        (gt, ":depth_cavalry", 0),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (call_script, "script_point_y_toward_position", pos2, Enemy_Team_Pos),
        (position_move_y, pos2, ":depth_cavalry"),
      (try_end),]),

  # script_division_reset_places by motomataru
  # Input: none
  # Output: none
  # Resets globals for placing divisions around player for
  # script_battlegroup_place_around_leader
  ("division_reset_places", [
      (assign, "$next_cavalry_place", formation_minimum_spacing_horse_width),	#first spot RIGHT of the player
      (assign, "$next_archer_place", 1000),	#first spot 10m FRONT of the player
      (assign, "$next_infantry_place", -1 * formation_minimum_spacing_horse_width),	#first spot LEFT of the player
  ]),

  # script_battlegroup_place_around_leader by motomataru
  # Input: team, division, team leader
  # Output: pos61 division position, moves pos1
  ("battlegroup_place_around_leader", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (try_begin),
        (le, ":fleader", 0),
        (display_message, "@{!}script_battlegroup_place_around_leader: invalid leader agent (bad call)"),

      (else_try),
        (agent_get_group, reg0, ":fleader"),
        (neq, reg0, ":fteam"),
        (display_message, "@{!}script_battlegroup_place_around_leader: leader team mismatch (bad call)"),

      (else_try),
        (agent_get_position, pos1, ":fleader"),
        (call_script, "script_battlegroup_place_around_pos1", ":fteam", ":fdivision", ":fleader"),
      (try_end),]),

  # script_battlegroup_place_around_pos1 by motomataru
  # Input: team, division
  # Output: pos61 division position, moves pos1
  ("battlegroup_place_around_pos1", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),

      (assign, ":store_fpm", 1),
      (convert_to_fixed_point, ":store_fpm"),
      (set_fixed_point_multiplier, 100),

      (store_sub, ":player_division", "$FormAI_player_in_division", 1),
      (try_begin),
        (eq, ":player_division", ":fdivision"),
        (assign, ":first_member_is_player", 1),
      (else_try),
        (assign, ":first_member_is_player", 0),
      (try_end),

      (try_begin),
        (eq, "$FormAI_autorotate", 1),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
      (team_get_slot, ":fformation", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
      (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),

      #handle memorized placement
      (try_begin),
        (eq, ":first_member_is_player", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (neq, ":value", 0),

        (position_move_x, pos1, ":value", 0),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":fdivision"),
        (faction_get_slot, ":value", "fac_player_faction", ":slot"),	#only used for player now
        (position_move_y, pos1, ":value", 0),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (try_begin),
            (this_or_next | eq, ":sd_type", sdt_cavalry),
            (eq, ":sd_type", sdt_harcher),
            (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0),
          (else_try),
            (eq, ":sd_type", sdt_archer),
            (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (else_try),
            (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
            (position_move_x, pos1, reg0, 0),
            (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", 0, ":fformation"),
          (try_end),
        (try_end),

      #default placement per division type
      (else_try),
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_cavalry_place", 0),
        (try_end),

        (try_begin),
          (gt, ":fformation", formation_none),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing_horse_width),
          (convert_to_fixed_point, ":num_troops"),
          (store_sqrt, ":formation_width", ":num_troops"),
          (val_mul, ":formation_width", ":troop_space"),
          (convert_from_fixed_point, ":formation_width"),
          (val_sub, ":formation_width", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
          (call_script, "script_form_cavalry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player"),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 133),	#cm added by each Spread Out
          (val_add, ":troop_space", 150),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 200),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (position_move_x, pos1, reg0, 0),	#cavalry set up RIGHT of leader
          (copy_position, pos61, pos1),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_add, "$next_cavalry_place", ":formation_width"),
          (val_add, "$next_cavalry_place", formation_minimum_spacing_horse_width),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_archer),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#archers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
          (val_mul, reg0, -1),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_archers", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (eq, ":sd_type", sdt_skirmisher),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_y, pos1, "$next_archer_place"),	#skirmishers set up FRONT of leader
          (val_add, "$next_archer_place", 500),	#next archers 5m FRONT of these
        (try_end),
        (copy_position, pos61, pos1),
        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (position_move_x, pos1, reg0, 0),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
        (try_end),

      (else_try),
        (try_begin),
          (eq, ":first_member_is_player", 0),
          (position_move_x, pos1, "$next_infantry_place", 0),
        (try_end),
        (copy_position, pos61, pos1),

        (try_begin),
          (gt, ":fformation", formation_none),
          (call_script, "script_form_infantry", ":fteam", ":fdivision", ":fleader", ":formation_extra_spacing", ":first_member_is_player", ":fformation"),
          (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (store_mul, ":formation_width", 2, reg0),
          (store_mul, ":troop_space", ":formation_extra_spacing", 50),
          (val_add, ":troop_space", formation_minimum_spacing),
          (val_add, ":formation_width", ":troop_space"),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),

        #handle Native's way of doing things
        (else_try),
          (store_mul, ":troop_space", ":formation_extra_spacing", 75),	#Native minimum spacing not consistent but less than this
          (val_add, ":troop_space", 100),	#minimum spacing

          #WFaS multi-ranks
          (try_begin),
            (eq, ":fformation", formation_2_row),
            (val_div, ":num_troops", 2),
          (else_try),
            (eq, ":fformation", formation_3_row),
            (val_div, ":num_troops", 3),
          (else_try),
            (eq, ":fformation", formation_4_row),
            (val_div, ":num_troops", 4),
          (else_try),
            (eq, ":fformation", formation_5_row),
            (val_div, ":num_troops", 5),

          (else_try),	#WB multi-ranks
            (lt, ":formation_extra_spacing", 0),
            (assign, ":troop_space", 150),
            (val_mul, ":formation_extra_spacing", -1),
            (val_add, ":formation_extra_spacing", 1),
            (val_div, ":num_troops", ":formation_extra_spacing"),
          (try_end),

          (store_mul, ":formation_width", ":num_troops", ":troop_space"),
          (store_div, reg0, ":formation_width", 2),
          (val_mul, reg0, -1),	#infantry set up LEFT of leader
          (position_move_x, pos61, reg0, 0),
        (try_end),

        (try_begin),
          (eq, ":first_member_is_player", 0),
          (val_sub, "$next_infantry_place", ":formation_width"),	#next infantry 1m LEFT of these
          (val_sub, "$next_infantry_place", 100),
        (try_end),
      (try_end),

      (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", mordr_hold),
      (set_show_messages, 0),
      (team_get_movement_order, reg0, ":fteam", ":fdivision"),
      (try_begin),
        (neq, reg0, mordr_hold),
        (team_give_order, ":fteam", ":fdivision", mordr_hold),
      (try_end),
      (call_script, "script_set_formation_destination", ":fteam", ":fdivision", pos61),
      (set_show_messages, 1),
      (set_fixed_point_multiplier, ":store_fpm"),]),

  # script_form_cavalry by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation
  # Output: none
  # Form in wedge, (now not) excluding horse archers
  # Creates formation starting at pos1
  ("form_cavalry", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":x_distance", formation_minimum_spacing_horse_width, ":extra_space"),
      (store_add, ":y_distance", formation_minimum_spacing_horse_length, ":extra_space"),
      (assign, ":max_level", 0),
      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_get_troop_id, ":troop_id", ":agent"),
        (store_character_level, ":troop_level", ":troop_id"),
        (gt, ":troop_level", ":max_level"),
        (assign, ":max_level", ":troop_level"),
      (end_try),
      (assign, ":column", 1),
      (assign, ":rank_dimension", 1),
      (store_mul, ":neg_y_distance", ":y_distance", -1),
      (store_mul, ":neg_x_distance", ":x_distance", -1),
      (store_div, ":wedge_adj", ":x_distance", 2),
      (store_div, ":neg_wedge_adj", ":neg_x_distance", 2),
      (assign, ":form_left", 1),
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (try_begin),
          (eq, ":form_left", 1),
          (position_move_x, pos1, ":neg_x_distance", 0),
        (else_try),
          (position_move_x, pos1, ":x_distance", 0),
        (try_end),
        (val_add, ":column", 1),
        (gt, ":column", ":rank_dimension"),
        (position_move_y, pos1, ":neg_y_distance", 0),
        (try_begin),
          (neq, ":form_left", 1),
          (assign, ":form_left", 1),
          (position_move_x, pos1, ":neg_wedge_adj", 0),
        (else_try),
          (assign, ":form_left", 0),
          (position_move_x, pos1, ":wedge_adj", 0),
        (try_end),
        (assign, ":column", 1),
        (val_add, ":rank_dimension", 1),
      (try_end),

      (val_add, ":max_level", 1),
      (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
        (try_for_agents, ":agent"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (eq, ":troop_level", ":rank_level"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (agent_set_scripted_destination, ":agent", pos1, 1),
          (try_begin),	#First Agent
            (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
            (neg | team_slot_ge, ":fteam", ":slot", 0),
            (team_set_slot, ":fteam", ":slot", ":agent"),
          (try_end),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_x_distance", 0),
          (else_try),
            (position_move_x, pos1, ":x_distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":rank_dimension"),
          (position_move_y, pos1, ":neg_y_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_wedge_adj", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":wedge_adj", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank_dimension", 1),
        (end_try),
      (end_try),]),

  # script_form_archers by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation, formation
  # Output: none
  # Form in line, staggered if formation = formation_ranks
  # Creates formation starting at pos1
  ("form_archers", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_script_param, ":archers_formation", 6),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
      (assign, ":total_move_y", 0),	#staggering variable
      (try_begin),
        (eq, ":include_leader", 0),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", -1),
      (else_try),	#after leader, move to next position (copied from below)
        (team_set_slot, ":fteam", ":slot", ":fleader"),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),

      (try_for_agents, ":agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
        (agent_set_scripted_destination, ":agent", pos1, 1),
        (try_begin),	#First Agent
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (neg | team_slot_ge, ":fteam", ":slot", 0),
          (team_set_slot, ":fteam", ":slot", ":agent"),
        (try_end),
        (position_move_x, pos1, ":distance", 0),
        (try_begin),
          (eq, ":archers_formation", formation_ranks),
          (val_add, ":total_move_y", 75),
          (try_begin),
            (le, ":total_move_y", 150),
            (position_move_y, pos1, 75, 0),
          (else_try),
            (position_move_y, pos1, -150, 0),
            (assign, ":total_move_y", 0),
          (try_end),
        (try_end),
      (try_end),]),

  # script_form_infantry by motomataru
  # Input: (pos1), team, division, agent number of team leader, spacing, flag
  # TRUE to include team leader in formation, formation
  # Output: none
  # If input "formation" is formation_default, will select a formation based on
  # faction
  # Creates formation starting at pos1
  ("form_infantry", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":formation_extra_spacing", 4),
      (store_script_param, ":include_leader", 5),
      (store_script_param, ":infantry_formation", 6),
      (store_mul, ":extra_space", ":formation_extra_spacing", 50),
      (store_add, ":distance", formation_minimum_spacing, ":extra_space"),		#minimum distance between troops
      (store_mul, ":neg_distance", ":distance", -1),
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (try_begin),
        (eq, ":infantry_formation", formation_default),
        (call_script, "script_get_default_formation", ":fteam"),
        (assign, ":infantry_formation", reg0),
      (try_end),
      (team_get_weapon_usage_order, ":weapon_order", ":fteam", ":fdivision"),
      (team_get_hold_fire_order, ":fire_order", ":fteam", ":fdivision"),
      (assign, ":form_left", 1),
      (assign, ":column", 1),
      (assign, ":rank", 1),

      (try_begin),
        (eq, ":infantry_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, ":square_dimension", ":num_troops"),
        (convert_from_fixed_point, ":square_dimension"),
        (val_add, ":square_dimension", 1),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":square_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),

        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (call_script, "script_switch_to_noswing_weapons", ":agent", ":distance"),

          (try_begin),
            (eq, "$battle_phase", BP_Deploy),
            (agent_set_scripted_destination, ":agent", pos1),
          (else_try),
            (call_script, "script_formation_process_agent_move", ":fteam", ":fdivision", ":agent", ":rank"),
          (try_end),

          (try_begin),
            (eq, formation_reequip, 1),
            (eq, ":weapon_order", wordr_use_any_weapon),
            (try_begin),
              (this_or_next | eq, ":rank", 1),
              (this_or_next | ge, ":rank", ":square_dimension"),
              (this_or_next | eq, ":column", 1),
              (ge, ":column", ":square_dimension"),
              (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
              (agent_ai_set_always_attack_in_melee, ":agent", 0),
            (else_try),
              (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
              (try_begin),
                (neq, ":closest_enemy", -1),
                (agent_get_position, pos0, ":closest_enemy"),
                (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                (neg | position_is_behind_position, pos0, pos1),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                (try_begin),
                  (position_is_behind_position, pos1, pos0),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (else_try),
                  (agent_ai_set_always_attack_in_melee, ":agent", 0),
                (try_end),
              (else_try),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 1, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 1),
              (try_end),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
            (try_end),
          (try_end),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":square_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (end_try),

      (else_try),
        (eq, ":infantry_formation", formation_wedge),
        (try_for_range, reg0, 0, 50),
          (troop_set_slot, "trp_temp_array_a", reg0, 0),
        (try_end),
        (assign, ":max_level", 0),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (call_script, "script_switch_to_noswing_weapons", ":agent", ":distance"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (troop_set_slot, "trp_temp_array_a", ":troop_level", 1),
          (gt, ":troop_level", ":max_level"),
          (assign, ":max_level", ":troop_level"),
        (end_try),

        (assign, ":rank_dimension", 1),
        (store_div, ":wedge_adj", ":distance", 2),
        (store_div, ":neg_wedge_adj", ":neg_distance", 2),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),
          (gt, ":column", ":rank_dimension"),
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_wedge_adj", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":wedge_adj", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank_dimension", 1),
        (try_end),

        (val_add, ":max_level", 1),
        (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
          (troop_slot_eq, "trp_temp_array_a", ":rank_level", 1),
          (try_for_agents, ":agent"),
            (agent_get_troop_id, ":troop_id", ":agent"),
            (store_character_level, ":troop_level", ":troop_id"),
            (eq, ":troop_level", ":rank_level"),
            (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),

            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move", ":fteam", ":fdivision", ":agent", ":rank_dimension"),
            (try_end),

            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (try_begin),
                (this_or_next | eq, ":column", 1),
                (ge, ":column", ":rank_dimension"),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (try_begin),
                  (neq, ":closest_enemy", -1),
                  (agent_get_position, pos0, ":closest_enemy"),
                  (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                  (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                  (neg | position_is_behind_position, pos0, pos1),
                  (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                  (try_begin),
                    (position_is_behind_position, pos1, pos0),
                    (agent_ai_set_always_attack_in_melee, ":agent", 1),
                  (else_try),
                    (agent_ai_set_always_attack_in_melee, ":agent", 0),
                  (try_end),
                (else_try),
                  (call_script, "script_equip_best_melee_weapon", ":agent", 0, 1, ":fire_order"),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (try_end),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
              (try_end),
            (try_end),
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),
            (gt, ":column", ":rank_dimension"),
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_wedge_adj", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":wedge_adj", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank_dimension", 1),
          (end_try),
        (end_try),

      (else_try),
        (eq, ":infantry_formation", formation_ranks),
        (try_for_range, reg0, 0, 50),
          (troop_set_slot, "trp_temp_array_a", reg0, 0),
        (try_end),
        (call_script, "script_calculate_default_ranks", ":num_troops"),
        (store_div, ":rank_dimension", ":num_troops", reg1),
        (val_add, ":rank_dimension", 1),
        (assign, ":max_level", 0),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (call_script, "script_switch_to_noswing_weapons", ":agent", ":distance"),
          (agent_get_troop_id, ":troop_id", ":agent"),
          (store_character_level, ":troop_level", ":troop_id"),
          (troop_set_slot, "trp_temp_array_a", ":troop_level", 1),
          (gt, ":troop_level", ":max_level"),
          (assign, ":max_level", ":troop_level"),
        (end_try),

        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),

          (gt, ":column", ":rank_dimension"),	#next rank?
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),

        (val_add, ":max_level", 1),
        (try_for_range_backwards, ":rank_level", 0, ":max_level"),	#put troops with highest exp in front
          (troop_slot_eq, "trp_temp_array_a", ":rank_level", 1),
          (try_for_agents, ":agent"),
            (agent_get_troop_id, ":troop_id", ":agent"),
            (store_character_level, ":troop_level", ":troop_id"),
            (eq, ":troop_level", ":rank_level"),
            (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),

            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),

            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (try_begin),
                (eq, ":rank", 1),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (try_begin),
                  (neq, ":closest_enemy", -1),
                  (agent_get_position, pos0, ":closest_enemy"),
                  (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                  (le, ":enemy_distance", ":distance"),	#enemy closer than friends?
                  (neg | position_is_behind_position, pos0, pos1),
                  (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                  (try_begin),
                    (position_is_behind_position, pos1, pos0),
                    (agent_ai_set_always_attack_in_melee, ":agent", 1),
                  (else_try),
                    (agent_ai_set_always_attack_in_melee, ":agent", 0),
                  (try_end),
                (else_try),
                  (call_script, "script_equip_best_melee_weapon", ":agent", 0, 1, ":fire_order"),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (try_end),
                (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
              (try_end),
            (try_end),
            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),

            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),
          (end_try),
        (end_try),

      (else_try),
        (eq, ":infantry_formation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":num_troops"),
        (store_div, ":rank_dimension", ":num_troops", reg1),
        (val_add, ":rank_dimension", 1),
        (try_begin),
          (eq, ":include_leader", 0),
          (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", -1),
        (else_try),	#after leader, move to next position (copied from below)
          (team_set_slot, ":fteam", ":slot", ":fleader"),
          (try_begin),
            (eq, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (val_add, ":column", 1),

          (gt, ":column", ":rank_dimension"),	#next rank?
          (position_move_y, pos1, ":neg_distance", 0),
          (try_begin),
            (neq, ":form_left", 1),
            (assign, ":form_left", 1),
            (position_move_x, pos1, ":neg_distance", 0),
          (else_try),
            (assign, ":form_left", 0),
            (position_move_x, pos1, ":distance", 0),
          (try_end),
          (assign, ":column", 1),
          (val_add, ":rank", 1),
        (try_end),

        (troop_set_slot, "trp_temp_array_a", 0, 0),	#short weap agent array
        (troop_set_slot, "trp_temp_array_b", 0, 0),	#medium weap agent array
        (troop_set_slot, "trp_temp_array_c", 0, 0),	#long weap agent array

        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":fleader", ":agent"),
          (call_script, "script_switch_to_noswing_weapons", ":agent", ":distance"),

          (assign, ":cur_score", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (gt, ":item", itm_no_item),
            (item_get_type, ":weapon_type", ":item"),
            (neq, ":weapon_type", itp_type_shield),

            (try_begin),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),

            (else_try),
              (item_get_weapon_length, ":item_length", ":item"),
              (lt, ":cur_score", ":item_length"),
              (assign, ":cur_score", ":item_length"),
            (try_end),
          (try_end),

          (try_begin),
            (eq, ":cur_score", 0),	#no melee weapons
            (assign, ":cur_array", "trp_temp_array_c"),
          (else_try),
            (le, ":cur_score", Third_Max_Weapon_Length),
            (assign, ":cur_array", "trp_temp_array_a"),
          (else_try),
            (gt, ":cur_score", 2 * Third_Max_Weapon_Length),
            (assign, ":cur_array", "trp_temp_array_c"),
          (else_try),
            (assign, ":cur_array", "trp_temp_array_b"),
          (try_end),

          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),
          (troop_set_slot, ":cur_array", ":array_end", ":agent"),
          (troop_set_slot, ":cur_array", 0, ":array_end"),
          (agent_set_slot, ":agent", slot_agent_positioned, 0),
        (try_end),

        #find shields first
        (store_add, ":arrays_end", "trp_temp_array_c", 1),
        (try_for_range, ":cur_array", "trp_temp_array_a", ":arrays_end"),
          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),

          (try_for_range, ":slot", 1, ":array_end"),
            (troop_get_slot, ":agent", ":cur_array", ":slot"),
            (assign, ":form_up", 0),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (agent_get_item_slot, ":item", ":agent", ":item_slot"),
              (gt, ":item", itm_no_item),
              (item_get_type, ":weapon_type", ":item"),
              (eq, ":weapon_type", itp_type_shield),
              (item_get_weapon_length, reg0, ":item"),	#gets shield width, which is always defined (see header_items)
              (ge, reg0, 25),	#wider than troop?
              (assign, ":form_up", 1),
            (try_end),

            (eq, ":form_up", 1),
            (agent_set_slot, ":agent", slot_agent_positioned, 1),
            (agent_set_slot, ":agent", slot_agent_inside_formation, 0),

            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),

            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),
              (call_script, "script_equip_best_melee_weapon", ":agent", 1, 0, ":fire_order"),	#best weapon, force shield
            (try_end),

            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),

            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),

            #break loops
            (assign, ":array_end", ":slot"),
            (assign, ":arrays_end", ":cur_array"),
          (try_end),
        (try_end),

        #add rest of division
        (store_add, ":arrays_end", "trp_temp_array_c", 1),
        (try_for_range, ":cur_array", "trp_temp_array_a", ":arrays_end"),
          (troop_get_slot, ":array_end", ":cur_array", 0),
          (val_add, ":array_end", 1),

          (try_for_range, ":slot", 1, ":array_end"),
            (troop_get_slot, ":agent", ":cur_array", ":slot"),
            (agent_slot_eq, ":agent", slot_agent_positioned, 0),
            (agent_set_slot, ":agent", slot_agent_positioned, 1),

            (try_begin),
              (eq, ":rank", 1),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
            (else_try),
              (agent_set_slot, ":agent", slot_agent_inside_formation, 1),
            (try_end),

            (try_begin),
              (eq, "$battle_phase", BP_Deploy),
              (agent_set_scripted_destination, ":agent", pos1),
            (else_try),
              (call_script, "script_formation_process_agent_move", ":fteam", ":fdivision", ":agent", ":rank"),
            (try_end),

            (try_begin),
              (eq, formation_reequip, 1),
              (eq, ":weapon_order", wordr_use_any_weapon),

              (try_begin),
                (eq, ":rank", 1),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 0),

              #enemy closer than friends?
              (else_try),
                (agent_get_slot, ":closest_enemy", ":agent", slot_agent_nearest_enemy_agent),
                (neq, ":closest_enemy", -1),
                (agent_get_position, pos0, ":closest_enemy"),
                (get_distance_between_positions, ":enemy_distance", pos0, pos1),
                (le, ":enemy_distance", ":distance"),
                (neg | position_is_behind_position, pos0, pos1),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 0, ":fire_order"),

                #behind enemy?
                (try_begin),
                  (position_is_behind_position, pos1, pos0),
                  (agent_ai_set_always_attack_in_melee, ":agent", 1),
                (else_try),
                  (agent_ai_set_always_attack_in_melee, ":agent", 0),
                (try_end),

              #equip longest weapon and avoid defensive
              (else_try),
                (call_script, "script_equip_best_melee_weapon", ":agent", 0, 1, ":fire_order"),
                (agent_ai_set_always_attack_in_melee, ":agent", 1),
              (try_end),
            (try_end),

            (try_begin),
              (eq, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (val_add, ":column", 1),

            (gt, ":column", ":rank_dimension"),	#next rank?
            (position_move_y, pos1, ":neg_distance", 0),
            (try_begin),
              (neq, ":form_left", 1),
              (assign, ":form_left", 1),
              (position_move_x, pos1, ":neg_distance", 0),
            (else_try),
              (assign, ":form_left", 0),
              (position_move_x, pos1, ":distance", 0),
            (try_end),
            (assign, ":column", 1),
            (val_add, ":rank", 1),
          (try_end),
        (try_end),
      (try_end),

      #calculate percent in place from counts from section above (see
      #script_formation_process_agent_move)
      (store_add, ":slot", slot_team_d0_size, ":fdivision"),
      (team_get_slot, ":num_troops", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),

      (try_begin),
        (eq, ":num_troops", 0),
        (team_set_slot, ":fteam", ":slot", 0),
      (else_try),
        (team_get_slot, reg0, ":fteam", ":slot"),
        (val_mul, reg0, 100),
        (val_div, reg0, ":num_troops"),
        (team_set_slot, ":fteam", ":slot", reg0),
      (try_end),
  ]),

  # script_get_default_formation by motomataru
  # Input: team id
  # Output: reg0 default formation
  ("get_default_formation", [
      (store_script_param, ":fteam", 1),
      (team_get_slot, ":ffaction", ":fteam", slot_team_faction),
      (try_begin),
        (this_or_next | eq, ":ffaction", fac_player_supporters_faction),
        (eq, ":ffaction", fac_player_faction),
        (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":ffaction", "$players_kingdom"),
      (try_end),

      (try_begin),
        (is_between, ":ffaction", "fac_player_faction", kingdoms_end),
        (faction_slot_ge, ":ffaction", slot_faction_culture, 1),
        (faction_get_slot, ":ffaction", ":ffaction", slot_faction_culture),
      (try_end),

      #assign default formation
      (try_begin),
        (eq, ":ffaction", fac_kingdom_1),	#Swadians
        (assign, reg0, formation_shield),	#use shields, stabby weapons
      (else_try),
        (eq, ":ffaction", fac_kingdom_2),	#Vaegirs
        (assign, reg0, formation_ranks),	#have a mix, so favor those nasty axes
      (else_try),
        (eq, ":ffaction", fac_kingdom_3),	#Khergit
        (assign, reg0, formation_none),	#Khergit have underdeveloped infantry
      (else_try),
        (eq, ":ffaction", fac_kingdom_4),	#Nords
        (assign, reg0, formation_ranks),	#favor swung weapons
      (else_try),
        (eq, ":ffaction", fac_kingdom_5),	#Rhodoks
        (assign, reg0, formation_shield),	#have a mix, so favor those big shields and pikes
      (else_try),
        (eq, ":ffaction", fac_kingdom_6),	#Sarranid
        (assign, reg0, formation_shield),
      (else_try),
        (this_or_next | eq, ":ffaction", fac_player_supporters_faction),
        (eq, ":ffaction", fac_player_faction),	#independent player
        (assign, reg0, formation_ranks),
      (else_try),
        (assign, reg0, formation_none),	#riffraff don't use formations
      (try_end),]),

  # script_switch_to_noswing_weapons by motomataru
  # Input: agent, formation spacing
  # Output: none
  ("switch_to_noswing_weapons", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":formation_spacing", 2),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (call_script, "script_cf_is_thrusting_weapon", ":item"),
        (item_get_weapon_length, ":weap_len",":item"),

        (try_begin),
          (ge, ":weap_len", ":formation_spacing"),	#avoid switching when weapon still has room to be swung
          (item_get_slot, ":noswing_version", ":item", slot_item_alternate),
          (gt, ":noswing_version", "itm_items_end"),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":noswing_version", ":item_slot"),	#assumes first ek_* are the weapons

        #undo legacy switches
        (else_try),
          (gt, ":item", "itm_items_end"),
          (item_get_slot, ":original_version", ":item", slot_item_alternate),
          (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
          (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
        (try_end),
      (try_end),]),

  # script_switch_from_noswing_weapons by motomataru
  # Input: agent
  # Output: none
  ("switch_from_noswing_weapons", [
      (store_script_param, ":agent", 1),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        (agent_get_item_slot, ":item", ":agent", ":item_slot"),
        (gt, ":item", "itm_items_end"),
        (item_get_slot, ":original_version", ":item", slot_item_alternate),
        (agent_unequip_item, ":agent", ":item", ":item_slot"),	#assumes first ek_* are the weapons
        (agent_equip_item, ":agent", ":original_version", ":item_slot"),	#assumes first ek_* are the weapons
      (try_end),]),

  # script_formation_process_agent_move by motomataru
  # Input: (pos1), team, division, agent, which rank of formation agent is in
  # Output: (pos1) may change to reference first agent's anticipated position
  # This function sets scripted destination and performs other tasks related to
  # making the formation look nice on the move (and more)
  ("formation_process_agent_move", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":agent", 3),
      (store_script_param, ":rank", 4),

      (agent_set_scripted_destination, ":agent", pos1, 1),

      (agent_get_position, Current_Pos, ":agent"),
      (get_distance_between_positions, ":distance_to_go", Current_Pos, pos1),

      (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
      (team_get_slot, ":speed_limit", ":fteam", ":slot"),

      (agent_get_speed, Speed_Pos, ":agent"),
      (position_transform_position_to_parent, Temp_Pos, Current_Pos, Speed_Pos),
      (call_script, "script_point_y_toward_position", Current_Pos, Temp_Pos),	#get direction of travel
      (store_mul, ":expected_travel", reg0, formation_reform_interval),
      (store_div, ":speed", ":expected_travel", Km_Per_Hour_To_Cm),

      #First Agent
      (try_begin),
        (store_add, ":slot", slot_team_d0_first_member, ":fdivision"),
        (neg | team_slot_ge, ":fteam", ":slot", 0),
        (team_set_slot, ":fteam", ":slot", ":agent"),

        (try_begin),	#reset speed when first member stopped
          (le, ":speed", 5),	#minimum observed speed
          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", Top_Speed),
          (agent_set_speed_limit, ":agent", Top_Speed),

        (else_try),	#first member in motion
          (val_mul, ":speed", 2),	#after terrain & encumbrance, agents tend to move about half their speed limit
          (try_begin),	#speed up if everyone caught up
            (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
            (team_slot_ge, ":fteam", ":slot", 100),
            (try_begin),
              (ge, ":speed", ":speed_limit"),
              (val_add, ":speed_limit", 1),
            (try_end),
          (else_try),	#else slow down
            (val_min, ":speed_limit", ":speed"),
            (val_sub, ":speed_limit", 1),
            (val_max, ":speed_limit", 5),	#minimum observed speed
          (try_end),

          #build formation from first agent
          (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", ":agent"),	#looking at same first member as last call?

          (call_script, "script_battlegroup_get_position", Temp_Pos, ":fteam", ":fdivision"),
          (get_distance_between_positions, ":distance_from_group", Current_Pos, Temp_Pos),
          (call_script, "script_battlegroup_get_action_radius", ":fteam", ":fdivision"),
          (val_div, reg0, 2),	#function returns length of bg
          (val_sub, ":distance_from_group", reg0),
          (lt, ":distance_from_group", 2000),	#within 20m of rest of division?

          (store_mul, ":expected_travel", ":speed_limit", Km_Per_Hour_To_Cm),
          (lt, ":expected_travel", ":distance_to_go"),	#more than one call from destination?

          (store_add, ":slot", slot_team_d0_speed_limit, ":fdivision"),
          (team_set_slot, ":fteam", ":slot", ":speed_limit"),
          (agent_set_speed_limit, ":agent", ":speed_limit"),

          (copy_position, Temp_Pos, Current_Pos),
          (call_script, "script_point_y_toward_position", Temp_Pos, pos1),
          (position_move_y, Temp_Pos, ":expected_travel", 0),	#anticipate where first member will be next
          (position_copy_rotation, Temp_Pos, pos1),	#conserve destination facing of formation
          (copy_position, pos1, Temp_Pos),	#reference the rest of the formation to first member's anticipated position
        (try_end),

        (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", 1),	#reinit: always count first member as having arrived
        (store_add, ":slot", slot_team_d0_prev_first_member, ":fdivision"),
        (team_set_slot, ":fteam", ":slot", ":agent"),

      #Not First Agent
      (else_try),
        (try_begin),
          (le, ":speed", 0),
          (assign, ":speed_limit", Top_Speed),
        (else_try),
          (neg | position_is_behind_position, pos1, Current_Pos),
          (store_div, ":speed_limit", ":distance_to_go", Km_Per_Hour_To_Cm),
          (val_max, ":speed_limit", 1),
        (else_try),
          (store_add, ":slot", slot_team_d0_is_fighting, ":fdivision"),
          (team_slot_eq, ":fteam", ":slot", 0),
          (assign, ":speed_limit", 1),
        (else_try),
          (assign, ":speed_limit", Top_Speed),
        (try_end),
        (agent_set_speed_limit, ":agent", ":speed_limit"),
        (try_begin),
          (this_or_next | le, ":speed", 0),	#reached previous destination or blocked OR
          (this_or_next | lt, ":speed_limit", Top_Speed),	#destination within reach OR
          (position_is_behind_position, pos1, Current_Pos),	#agent ahead of formation
          (store_add, ":slot", slot_team_d0_percent_in_place, ":fdivision"),
          (team_get_slot, reg0, ":fteam", ":slot"),
          (val_add, reg0, 1),
          (team_set_slot, ":fteam", ":slot", reg0),
        (try_end),
      (try_end),

      #Housekeeping
      (agent_set_slot, ":agent", slot_agent_formation_rank, ":rank"),]),

  # script_pick_native_formation by motomataru
  # Input: team, division
  # Output: reg0 with formation_*_row (see module_constants)
  #         reg1 with number of rows
  ("pick_native_formation", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),

      (store_add, ":slot", slot_team_d0_size, ":division"),
      (team_get_slot, ":bg_size", ":team", ":slot"),

      (try_begin),
        (eq, ":bg_size", 0),	#script_store_battlegroup_data is not being called
        (team_get_leader, ":leader", ":team"),
        (try_for_agents, ":agent"),
          (call_script, "script_cf_valid_formation_member", ":team", ":division", ":leader", ":agent"),
          (val_add, ":bg_size", 1),
        (try_end),
      (try_end),

      (call_script, "script_calculate_default_ranks", ":bg_size"),
      (try_begin),
        (eq, reg1, 1),
        (assign, reg0, formation_1_row),
      (else_try),
        (eq, reg1, 2),
        (assign, reg0, formation_2_row),
      (else_try),
        (eq, reg1, 3),
        (assign, reg0, formation_3_row),
      (else_try),
        (this_or_next | eq, reg1, 4),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (assign, reg0, formation_4_row),
        (assign, reg1, 4),
      (else_try),
        (assign, reg0, formation_5_row),
        (assign, reg1, 5),
      (try_end)]),

  # script_calculate_default_ranks by motomataru
  # Input: number of troops
  # Output: reg1 with number of rows
  # calculates number of rows closest to the old Roman 5:1 cohort arrangement
  # (80 troops in 4 rows)
  # quadratic formula to solve (5R^2 + 5(R+1)^2)/2
  ("calculate_default_ranks", [
      (store_script_param, ":bg_size", 1),

      (val_mul, ":bg_size", 20),
      (val_sub, ":bg_size", 25),
      (convert_to_fixed_point, ":bg_size"),
      (store_sqrt, reg1, ":bg_size"),
      (convert_from_fixed_point, reg1),
      (val_sub, reg1, 5),
      (val_div, reg1, 10),
      (val_add, reg1, 1),]),

  # script_get_centering_amount by motomataru
  # Input: formation type, number of troops, extra spacing
  #        Use formation type formation_default to use script for archer line
  # Output: reg0 number of centimeters to adjust x-position to center formation
  ("get_centering_amount", [
      (store_script_param, ":troop_formation", 1),
      (store_script_param, ":num_troops", 2),
      (store_script_param, ":extra_spacing", 3),
      (store_mul, ":troop_space", ":extra_spacing", 50),
      (val_add, ":troop_space", formation_minimum_spacing),
      (assign, reg0, 0),
      (try_begin),
        (eq, ":troop_formation", formation_square),
        (convert_to_fixed_point, ":num_troops"),
        (store_sqrt, reg0, ":num_troops"),
        (convert_from_fixed_point, reg0),
        (val_mul, reg0, ":troop_space"),
        # (val_sub, reg0, ":troop_space"), MOTO not needed because column added in
        # script_form_infantry
      (else_try),
        (this_or_next | eq, ":troop_formation", formation_ranks),
        (eq, ":troop_formation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":num_troops"),
        (assign, ":num_ranks", reg1),
        (store_div, reg0, ":num_troops", ":num_ranks"),
        (try_begin),
          (store_mod, reg1, ":num_troops", ":num_ranks"),
          (eq, reg1, 0),
          (val_sub, reg0, 1),
        (try_end),
        (val_mul, reg0, ":troop_space"),
      (else_try),
        (eq, ":troop_formation", formation_default),	#assume these are archers in a line
        (store_mul, reg0, ":num_troops", ":troop_space"),
      (try_end),
      (val_div, reg0, 2),]),

  # script_formation_end
  # Input: team, division
  # Output: none
  ("formation_end", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (try_begin),
        (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
        (neg | team_slot_eq, ":fteam", ":slot", formation_none),
        (team_slot_ge, ":fteam", ":slot", formation_none),

        (try_begin),
          (eq, Native_Formations_Implementation, WFaS_Implementation),
          (team_set_slot, ":fteam", ":slot", formation_2_row),
        (else_try),
          (team_set_slot, ":fteam", ":slot", formation_none),
        (try_end),

        (team_get_leader, ":leader", ":fteam"),

        (try_for_agents, ":agent"),
          (agent_is_alive, ":agent"),
          (agent_is_human, ":agent"),
          (agent_get_group, ":team", ":agent"),
          (eq, ":team", ":fteam"),
          (neq, ":leader", ":agent"),
          (agent_get_division, ":bgdivision", ":agent"),
          (eq, ":bgdivision", ":fdivision"),
          (agent_clear_scripted_mode, ":agent"),
          (call_script, "script_switch_from_noswing_weapons", ":agent"),
          (agent_ai_set_always_attack_in_melee, ":agent", 0),
          (agent_set_speed_limit, ":agent", 100),
          (agent_set_slot, ":agent", slot_agent_formation_rank, 0),
          (agent_set_slot, ":agent", slot_agent_inside_formation, 0),
        (try_end),

        (try_begin),
          (eq, ":fteam", "$fplayer_team_no"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),

          #adjust for differences between the systems of spreading out (Native spreads
          #out about twice as much)
          (try_begin),
            (eq, Native_Formations_Implementation, WFaS_Implementation),
            (assign, ":max_spacing", 3),
          (else_try),
            (assign, ":max_spacing", 2),
          (try_end),

          (store_mul, ":double_max", ":max_spacing", 2),

          (try_begin),
            (ge, ":div_spacing", ":double_max"),	#beyond Native max
            (assign, ":div_spacing", ":max_spacing"),
          (else_try),
            (gt, ":div_spacing", 0),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_stand_closer),
            (set_show_messages, 1),
            (val_div, ":div_spacing", 2),
          (try_end),

          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),
      (try_end),]),

  # script_formation_move_position by motomataru
  # Input: team, division, formation current position, (1 to advance or -1 to
  # withdraw or 0 to redirect)
  # Output: pos1 (offset for centering)
  ("formation_move_position", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fcurrentpos", 3),
      (store_script_param, ":direction", 4),
      (copy_position, pos1, ":fcurrentpos"),
      (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":fteam", grc_everyone),
      (try_begin),
        (neq, reg0, 0),	#more than 0 enemies still alive?
        (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),	#record angle from center to enemy
        (assign, ":distance_to_enemy", reg0),
        (call_script, "script_get_formation_destination", pos61, ":fteam", ":fdivision"),
        (get_distance_between_positions, ":move_amount", pos1, pos61),	#distance already moving from previous orders
        (val_add, ":move_amount", 1000),
        (try_begin),
          (gt, ":direction", 0),	#moving forward?
          (gt, ":move_amount", ":distance_to_enemy"),
          (assign, ":move_amount", ":distance_to_enemy"),
        (try_end),
        (val_mul, ":move_amount", ":direction"),
        (position_move_y, pos1, ":move_amount", 0),
        (position_get_x, ":from_x", pos1),
        (position_get_y, ":from_y", pos1),
        (try_begin),
          (is_between, ":from_x", "$g_bound_left", "$g_bound_right"),
          (is_between, ":from_y", "$g_bound_bottom", "$g_bound_top"),
          (try_begin),
            (lt, ":distance_to_enemy", 1000),	#less than a move away?
            (position_copy_rotation, pos1, pos61),	#avoid rotating formation
          (try_end),
          (call_script, "script_set_formation_destination", ":fteam", ":fdivision", pos1),
          (store_add, ":slot", slot_team_d0_size, ":fdivision"),
          (team_get_slot, ":num_troops", ":fteam", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":formation_extra_spacing", ":fteam", ":slot"),
          (try_begin),
            (store_add, ":slot", slot_team_d0_type, ":fdivision"),
            (neg | team_slot_eq, ":fteam", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
            (team_get_slot, ":fformation", ":fteam", ":slot"),
            (call_script, "script_get_centering_amount", ":fformation", ":num_troops", ":formation_extra_spacing"),
          (else_try),
            (call_script, "script_get_centering_amount", formation_default, ":num_troops", ":formation_extra_spacing"),
            (val_mul, reg0, -1),
          (try_end),
          (position_move_x, pos1, reg0, 0),

          #out of bounds
        (else_try),
          (copy_position, pos1, ":fcurrentpos"),	#restore current formation "position"
        (try_end),
      (try_end),]),

  # script_cf_battlegroup_valid_formation
  # Input: team, division, formation
  # Output: reg0: troop count/1 if too few troops/0 if wrong type
  ("cf_battlegroup_valid_formation", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fformation", 3),

      (assign, ":valid_type", 0),
      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_get_slot, ":sd_type", ":fteam", ":slot"),
      (try_begin), #Eventually make this more complex with the sub-divisions
        (this_or_next | eq, ":sd_type", sdt_cavalry),
        (eq, ":sd_type", sdt_harcher),
        (assign, ":size_minimum", formation_min_cavalry_troops),
        (try_begin),
          (eq, ":fformation", formation_wedge),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (eq, ":sd_type", sdt_archer),
        (assign, ":size_minimum", formation_min_foot_troops),
        (try_begin),
          # (this_or_next|eq, ":fformation", formation_ranks), uncheck for proper
          # ranks
          (eq, ":fformation", formation_default),
          (assign, ":valid_type", 1),
        (try_end),
      (else_try),
        (assign, ":size_minimum", formation_min_foot_troops),
        (gt, ":fformation", formation_none),
        (assign, ":valid_type", 1), #all types valid
      (try_end),

      (try_begin),
        (eq, ":valid_type", 0),
        (assign, ":num_troops", 0),
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":fdivision"),
        (team_get_slot, ":num_troops", ":fteam", ":slot"),
        (lt, ":num_troops", ":size_minimum"),
        (assign, ":num_troops", 1),
      (try_end),

      (assign, reg0, ":num_troops"),
      (gt, ":num_troops", 1)]),

  # script_cf_valid_formation_member by motomataru #CABA - Modified for
  # Classify_agent phase out
  # Input: team, division, agent number of team leader, test agent
  # Output: failure indicates agent is not member of formation
  ("cf_valid_formation_member", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fleader", 3),
      (store_script_param, ":agent", 4),
      (neq, ":fleader", ":agent"),
      (agent_get_division, ":bgdivision", ":agent"),
      (eq, ":bgdivision", ":fdivision"),
      (agent_get_group, ":team", ":agent"),
      (eq, ":team", ":fteam"),
      (agent_is_alive, ":agent"),
      (agent_is_human, ":agent"),
      (agent_slot_eq, ":agent", slot_agent_is_running_away, 0),]),

  # #Player team formations functions
  # script_player_attempt_formation
  # Inputs: arg1: division
  #			arg2: formation identifier (formation_*)
  #         arg3: flag 1 to form at current location (rather than next to
  #         player), flag 2 to form as if player were at Target_Pos
  # Output: none
  # Designed JUST for infantry
  ("player_attempt_formation", [
      (store_script_param, ":fdivision", 1),
      (store_script_param, ":fformation", 2),
      (store_script_param, ":form_on_spot", 3),
      (set_fixed_point_multiplier, 100),
      (try_begin),
        (eq, ":fformation", formation_ranks),
        (str_store_string, s1, "@ranks"),
      (else_try),
        (eq, ":fformation", formation_shield),
        (str_store_string, s1, "@shield wall"),
      (else_try),
        (eq, ":fformation", formation_wedge),
        (str_store_string, s1, "@wedge"),
      (else_try),
        (eq, ":fformation", formation_square),
        (str_store_string, s1, "@square"),
      (else_try),
        (str_store_string, s1, "@up"),
      (try_end),
      (str_store_class_name, s2, ":fdivision"),

      (try_begin),
        (call_script, "script_cf_battlegroup_valid_formation", "$fplayer_team_no", ":fdivision", ":fformation"),
        (try_begin),	#new formation?
          (store_add, ":slot", slot_team_d0_formation, ":fdivision"),
          (neg | team_slot_eq, "$fplayer_team_no", ":slot", ":fformation"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":fformation"),
          (store_add, reg1, ":fdivision", 1),
          (display_message, "@Division {reg1} {s2} forming {s1}."),
          (store_add, ":slot", slot_team_d0_fclock, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_target_team, ":fdivision"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),

          (store_add, ":slot", slot_team_d0_formation_space, ":fdivision"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),

          #bring unformed divisions into sync with formations' minimum
          (set_show_messages, 0),
          (assign, reg0, ":div_spacing"),
          (try_for_range, reg1, reg0, formation_start_spread_out),	#spread out for ease of forming up
            (team_give_order, "$fplayer_team_no", ":fdivision", mordr_spread_out),
            (val_add, ":div_spacing", 1),
          (try_end),
          (set_show_messages, 1),

          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
        (try_end),

        #divisions must stop to order themselves
        (store_add, ":slot", slot_team_d0_move_order, ":fdivision"),
        (team_get_slot, ":div_order", "$fplayer_team_no", ":slot"),
        (try_begin),
          (this_or_next | eq, ":div_order", mordr_stand_ground),
          (this_or_next | eq, ":div_order", mordr_charge),
          (eq, ":div_order", mordr_retreat),
          (call_script, "script_battlegroup_get_position", pos1, "$fplayer_team_no", ":fdivision"),
          (team_give_order, "$fplayer_team_no", ":fdivision", mordr_hold),
          (call_script, "script_set_formation_destination", "$fplayer_team_no", ":fdivision", pos1),
        (try_end),

      (else_try),
        (assign, ":return_val", reg0),
        (call_script, "script_formation_end", "$fplayer_team_no", ":fdivision"),
        (gt, ":fformation", formation_none),
        (store_add, reg1, ":fdivision", 1),
        (try_begin),
          (gt, ":return_val", 0),
          (display_message, "@Not enough troops in division {reg1} {s2} to form {s1}."),
        (else_try),
          (store_add, ":slot", slot_team_d0_type, ":fdivision"),
          (team_get_slot, reg0, "$fplayer_team_no", ":slot"),
          (call_script, "script_str_store_division_type_name", s3, reg0),
          (display_message, "@Division {reg1} {s2} is an {s3} division and cannot form {s1}."),
        (try_end),
      (try_end),

      (try_begin),
        (eq, ":form_on_spot", 0),
        (call_script, "script_battlegroup_place_around_leader", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (else_try),
        (eq, ":form_on_spot", 2),
        (copy_position, pos1, Target_Pos),
        (call_script, "script_battlegroup_place_around_pos1", "$fplayer_team_no", ":fdivision", "$fplayer_agent_no"),
      (try_end),]),

  # script_player_formation_end
  # Input: division
  # Output: none
  ("player_formation_end", [
      (store_script_param, ":fdivision", 1),

      (call_script, "script_formation_end", "$fplayer_team_no", ":fdivision"),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (str_store_class_name, s1, ":fdivision"),
      (try_begin),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_infantry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_polearm),
        (display_message, "@{s1}: infantry formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
        (display_message, "@{s1}: archer formation disassembled."),
      (else_try),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_skirmisher),
        (display_message, "@{s1}: skirmisher formation disassembled."),
      (else_try),
        (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
        (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
        (display_message, "@{s1}: cavalry formation disassembled."),
      (else_try),
        (display_message, "@{s1}: formation disassembled."),
      (try_end),]),

  # script_player_order_formations by motomataru TODO add native weapon
  # commands
  # Inputs: arg1: order to formation (mordr_*)
  # Output: none
  ("player_order_formations", [
      (store_script_param, ":forder", 1),
      (set_fixed_point_multiplier, 100),

      (try_begin), #On hold, any formations reform in new location
        (eq, ":forder", mordr_hold),
        (call_script, "script_division_reset_places"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),	#apply to all divisions (not just formations)
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (call_script, "script_player_attempt_formation", ":division", ":formation", 0),
        (try_end),

      (else_try),	#Follow is hold repeated frequently
        (eq, ":forder", mordr_follow),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_size, ":division"),	#apply to all divisions (not just formations)
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),

          (store_add, ":slot", slot_team_d0_formation, ":division"),	#update formations
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (call_script, "script_player_attempt_formation", ":division", ":formation", 0),

          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),
        (try_end),

      (else_try),	#charge or retreat ends formation
        (this_or_next | eq, ":forder", mordr_charge),
        (eq, ":forder", mordr_retreat),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),
          (call_script, "script_player_formation_end", ":division"),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_form_1_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_1_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_form_2_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_2_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 2),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_form_3_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_3_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 3),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_form_4_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_4_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 4),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_form_5_row),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":formation", formation_none),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", formation_5_row),
          (store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 5),
        (try_end),

      (else_try),	#dismount ends formation
        (eq, ":forder", mordr_dismount),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (neg | team_slot_eq, "$fplayer_team_no", ":slot", formation_none),
          (team_slot_ge, "$fplayer_team_no", ":slot", formation_none),
          (try_begin),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
            (display_message, "@Cavalry formation disassembled."),

          (else_try),	#address bug that cavalry in scripted mode won't dismount
            (try_for_agents, ":agent"),
              (agent_is_alive, ":agent"),
              (agent_is_human, ":agent"),
              (agent_get_group, ":team", ":agent"),
              (eq, ":team", "$fplayer_team_no"),
              (neq, "$fplayer_agent_no", ":agent"),
              (agent_get_division, ":bgdivision", ":agent"),
              (eq, ":bgdivision", ":division"),
              (agent_clear_scripted_mode, ":agent"),
              (agent_set_speed_limit, ":agent", 100),
            (try_end),
          (try_end),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_advance),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_get_slot, ":prev_order", "$fplayer_team_no", ":slot"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),

          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

          (call_script, "script_formation_current_position", pos63, "$fplayer_team_no", ":division"),
          (try_begin),
            (neq, ":prev_order", mordr_advance),
            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos63),
          (try_end),
          (call_script, "script_formation_move_position", "$fplayer_team_no", ":division", pos63, 1),

          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0),
          (else_try),
            (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (try_end),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_fall_back),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_get_slot, ":prev_order", "$fplayer_team_no", ":slot"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),

          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

          (call_script, "script_formation_current_position", pos63, "$fplayer_team_no", ":division"),
          (try_begin),
            (neq, ":prev_order", mordr_fall_back),
            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos63),
          (try_end),
          (call_script, "script_formation_move_position", "$fplayer_team_no", ":division", pos63, -1),

          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0),
          (else_try),
            (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":formation"),
          (try_end),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_stand_closer),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),

          (try_begin),
            (eq, Native_Formations_Implementation, WB_Implementation),
            (assign, ":min_spacing", -3),	#WB formations go down to four ranks by using Stand Closer
          (else_try),
            (assign, ":min_spacing", 0),
          (try_end),

          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (gt, ":div_spacing", ":min_spacing"),
          (val_sub, ":div_spacing", 1),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),

          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

          (try_begin),	#bring unformed divisions into sync with formations' minimum
            (lt, ":div_spacing", 0),
            (set_show_messages, 0),
            (assign, reg0, ":div_spacing"),
            (try_for_range, reg1, reg0, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
              (val_add, ":div_spacing", 1),
            (try_end),
            (set_show_messages, 1),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),

          (else_try),
            (call_script, "script_get_formation_destination", pos1, "$fplayer_team_no", ":division"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (try_begin),
              (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
              (store_add, ":slot", slot_team_d0_size, ":division"),
              (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
              (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
            (else_try),
              (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
              (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
              (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
            (else_try),
              (store_add, ":slot", slot_team_d0_size, ":division"),
              (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
              (call_script, "script_get_centering_amount", ":formation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
            (try_end),
          (try_end),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_spread_out),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),

          (try_begin),
            (eq, Native_Formations_Implementation, WFaS_Implementation),
            (assign, ":max_spacing", 3),
          (else_try),
            (assign, ":max_spacing", 2),
          (try_end),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
          (try_begin),
            (this_or_next | lt, ":div_spacing", ":max_spacing"),
            (gt, ":formation", formation_none),
            (val_add, ":div_spacing", 1),
          (try_end),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),

          (gt, ":formation", formation_none),

          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

          #bring unformed divisions into sync with formations' minimum
          (set_show_messages, 0),
          (assign, reg0, ":div_spacing"),
          (try_for_range, reg1, reg0, 1),
            (team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
            (val_add, ":div_spacing", 1),
          (try_end),
          (set_show_messages, 1),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),

          (call_script, "script_get_formation_destination", pos1, "$fplayer_team_no", ":division"),
          (try_begin),
            (store_add, ":slot", slot_team_d0_first_member, ":division"),
            (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
            (assign, ":first_member_is_player", 1),
          (else_try),
            (assign, ":first_member_is_player", 0),
          (try_end),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
          (else_try),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount", ":formation", ":troop_count", ":div_spacing"),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (try_end),
        (try_end),

      (else_try),
        (eq, ":forder", mordr_stand_ground),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", ":forder"),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
          (gt, ":formation", formation_none),

          (store_add, ":slot", slot_team_d0_fclock, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

          (call_script, "script_formation_current_position", pos63, "$fplayer_team_no", ":division"),
          (copy_position, pos1, pos63),
          (store_add, ":slot", slot_team_d0_formation_space, ":division"),
          (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),

          (try_begin),
            (store_add, ":slot", slot_team_d0_first_member, ":division"),
            (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
            (assign, ":first_member_is_player", 1),
          (else_try),
            (assign, ":first_member_is_player", 0),
          (try_end),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (try_begin),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_archer),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
            (val_mul, reg0, -1),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (else_try),
            (this_or_next | team_slot_eq, "$fplayer_team_no", ":slot", sdt_cavalry),
            (team_slot_eq, "$fplayer_team_no", ":slot", sdt_harcher),
            (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
          (else_try),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
            (call_script, "script_get_centering_amount", ":formation", ":troop_count", ":div_spacing"),
            (position_move_x, pos1, reg0),
            (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":formation"),
          (try_end),
          (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos63),
        (try_end),
      (try_end)]),

  # script_memorize_division_placements by motomataru
  # Inputs: none
  # Output: none
  ("memorize_division_placements", [
      (set_fixed_point_multiplier, 100),
      (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
      (assign, ":num_enemies", reg0),

      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),

        (store_add, ":slot", slot_team_d0_formation, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation_space, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (agent_get_position, pos1, "$fplayer_agent_no"),
        (try_begin),
          (neq, ":num_enemies", 0),	#more than 0 enemies still alive?
          (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
        (try_end),
        # (call_script, "script_get_formation_destination", Current_Pos,
        # "$fplayer_team_no", ":division"),
        (team_get_order_position, Current_Pos, "$fplayer_team_no", ":division"),	#use this to capture Native Advance and Fall Back positioning
        (position_transform_position_to_local, Temp_Pos, pos1, Current_Pos), #Temp_Pos = vector to division w.r.t.  leader facing enemy

        (position_get_x, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (position_get_y, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} memorized."),
      (try_end),]),

  # script_default_division_placements by motomataru
  # Inputs: none
  # Output: none
  ("default_division_placements", [
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),	#use as flag
        (faction_set_slot, "fac_player_faction", ":slot", 0),

        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} set to default."),
      (try_end),]),

  # script_process_place_divisions by motomataru
  # Inputs: none
  # Output: none
  # Expects team_set_order_position has been done
  ("process_place_divisions", [
      (assign, ":num_bgroups", 0),
      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", -1),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),
        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_set_slot, "$fplayer_team_no", ":slot", 1),
        (team_get_order_position, pos1, "$fplayer_team_no", ":division"),
        (val_add, ":num_bgroups", 1),
      (try_end),

      (try_begin),
        (gt, ":num_bgroups", 0),
        (copy_position, Target_Pos, pos1),	#kludge around team_get_order_position rotation problems

        (try_begin),
          (eq, "$battle_phase", BP_Deploy),

          (try_begin),
            (eq, "$g_is_quick_battle", 1),
            (assign, reg0, 5),
          (else_try),
            (party_get_skill_level, reg0, "p_main_party", "skl_tactics"),
          (try_end),
          (store_mul, ":range_limit", reg0, 1000),

          (agent_get_position, Temp_Pos, "$fplayer_agent_no"),
          (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
          (lt, ":range_limit", reg0),
          (display_message, "@Your party's tactical skill limits how far away you can deploy your troops!"),
          (call_script, "script_point_y_toward_position", Temp_Pos, Target_Pos),
          (copy_position, Target_Pos, Temp_Pos),
          (position_move_y, Target_Pos, ":range_limit"),
        (try_end),

        #player designating target battlegroup?
        (assign, ":distance_to_enemy", Far_Away),
        (try_for_range, ":team", 0, 4),
          (teams_are_enemies, ":team", "$fplayer_team_no"),
          (team_slot_ge, ":team", slot_team_size, 1),
          (try_for_range, ":division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":division"),
            (team_slot_ge, ":team", ":slot", 1),
            (call_script, "script_battlegroup_get_position", Temp_Pos, ":team", ":division"),
            (get_distance_between_positions, reg0, Target_Pos, Temp_Pos),
            (gt, ":distance_to_enemy", reg0),
            (assign, ":distance_to_enemy", reg0),
            (assign, ":closest_enemy_team", ":team"),
            (assign, ":closest_enemy_division", ":division"),
          (try_end),
        (try_end),

        (call_script, "script_battlegroup_get_action_radius", ":closest_enemy_team", ":closest_enemy_division"),
        (assign, ":radius_enemy_battlegroup", reg0),

        (try_begin),
          (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
          (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
          #selecting them
          (call_script, "script_battlegroup_get_position", Target_Pos, ":closest_enemy_team", ":closest_enemy_division"),
          (gt, ":num_bgroups", 1),
          (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
          (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),
          (display_message, "@...and attack enemy {s1} division!"),
        (try_end),

        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", Target_Pos, Enemy_Team_Pos),

        #place player divisions
        (agent_get_position, pos49, "$fplayer_agent_no"),
        (try_for_range, ":division", 0, 9),
          (class_is_listening_order, "$fplayer_team_no", ":division"),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
          (gt, ":troop_count", 0),

          (try_begin),
            (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
            (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
            #selecting them
            (store_add, ":slot", slot_team_d0_target_team, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_team"),
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_set_slot, "$fplayer_team_no", ":slot", ":closest_enemy_division"),
          (try_end),

          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),

          (try_begin),
            (gt, ":num_bgroups", 1),
            (agent_set_position, "$fplayer_agent_no", Target_Pos),	#fake out script_battlegroup_place_around_leader
            (call_script, "script_player_attempt_formation", ":division", ":fformation", 0),
          (else_try),
            (try_begin),
              (le, ":distance_to_enemy", ":radius_enemy_battlegroup"),	#target position within radius of an enemy battlegroup?
              (le, ":distance_to_enemy", AI_charge_distance),	#limit so player can place divisions near large enemy battlegroups without
              #selecting them
              (call_script, "script_battlegroup_get_attack_destination", Target_Pos, "$fplayer_team_no", ":division", ":closest_enemy_team", ":closest_enemy_division"),
              (store_add, ":slot", slot_team_d0_type, ":closest_enemy_division"),
              (team_get_slot, reg0, ":closest_enemy_team", ":slot"),
              (call_script, "script_str_store_division_type_name", s1, reg0),
              (display_message, "@...and attack enemy {s1} division!"),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", Target_Pos),

            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (try_begin),
              (store_add, ":slot", slot_team_d0_type, ":division"),
              (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (try_begin),
                (eq, ":sd_type", sdt_archer),
                (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
                (val_mul, reg0, -1),
                (assign, ":script", "script_form_archers"),
              (else_try),
                (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
                (assign, ":script", "script_form_infantry"),
              (try_end),
              (position_move_x, Target_Pos, reg0),
            (else_try),
              (assign, ":script", "script_form_cavalry"),
            (try_end),
            (copy_position, pos1, Target_Pos),
            (call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", 0, ":fformation"),
          (try_end),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_hold),
        (try_end), #division loop
        (agent_set_position, "$fplayer_agent_no", pos49),
      (try_end),	#num_bgroups > 0
  ]),

  # script_process_player_division_positioning by motomataru
  # Inputs: none
  # Output: none
  # Expects Enemy_Team_Pos
  ("process_player_division_positioning", [
      (call_script, "script_division_reset_places"),

      #implement HOLD OVER THERE when player lets go of key
      (try_begin),
        (ge, "$gk_order_hold_over_there", HOT_F1_held),
        (neg | game_key_is_down, gk_order_1),
        (assign, "$gk_order_hold_over_there", HOT_no_order),
        (call_script, "script_process_place_divisions"),
      (try_end),	#HOLD OVER THERE

      #periodic functions
      (assign, ":save_autorotate", "$FormAI_autorotate"),
      (assign, "$FormAI_autorotate", 0),
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
        (gt, ":troop_count", 0),

        (store_add, ":slot", slot_team_d0_target_team, ":division"),
        (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_target_division, ":division"),
        (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
        (try_begin),
          (ge, ":target_team", 0),	#enemy battlegroup targeted?
          (store_add, ":slot", slot_team_d0_size, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),

          (le, reg0, 0),	#target destroyed?
          (store_add, ":slot", slot_team_d0_target_team, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", -1),

          (store_add, ":slot", slot_team_d0_type, ":target_division"),
          (team_get_slot, reg0, ":target_team", ":slot"),
          (call_script, "script_str_store_division_type_name", s1, reg0),

          (str_store_class_name, s2, ":division"),
          (display_message, "@{s2}: returning after destroying enemy {s1} division."),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
        (try_end),

        (store_add, ":slot", slot_team_d0_fclock, ":division"),
        (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
        (store_mod, ":time_slice", ":fclock", Reform_Trigger_Modulus),
        (val_add, ":fclock", 1),
        (team_set_slot, "$fplayer_team_no", ":slot", ":fclock"),

        (try_begin),
          (store_add, ":slot", slot_team_d0_move_order, ":division"),
          (team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
          (call_script, "script_battlegroup_place_around_leader", "$fplayer_team_no", ":division", "$fplayer_agent_no"),
          (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),	#override script_battlegroup_place_around_leader

        #periodically reform
        (else_try),
          (eq, ":time_slice", 0),
          (team_get_movement_order, reg0, "$fplayer_team_no", ":division"),
          (neq, reg0, mordr_stand_ground),

          (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
          (store_add, ":slot", slot_team_d0_formation, ":division"),
          (team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
          (try_begin),
            (gt, ":fformation", formation_none),
            (store_add, ":slot", slot_team_d0_formation_space, ":division"),
            (team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
            (store_add, ":slot", slot_team_d0_type, ":division"),
            (team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),

            (try_begin),
              (store_add, ":slot", slot_team_d0_first_member, ":division"),
              (team_slot_eq, "$fplayer_team_no", ":slot", "$fplayer_agent_no"),
              (assign, ":first_member_is_player", 1),
            (else_try),
              (assign, ":first_member_is_player", 0),
            (try_end),

            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (try_begin),
                (this_or_next | eq, ":sd_type", sdt_archer),
                (this_or_next | eq, ":sd_type", sdt_harcher),
                (eq, ":sd_type", sdt_skirmisher),
                (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
                (call_script, "script_formation_current_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
              (else_try),
                (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
              (try_end),

            (else_try),
              (call_script, "script_get_formation_destination", pos1, "$fplayer_team_no", ":division"),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_get_slot, ":is_fighting", "$fplayer_team_no", ":slot"),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, -2000),
              (try_end),
              (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
              (try_begin),
                (neq, ":sd_type", sdt_cavalry),
                (neq, ":sd_type", sdt_harcher),
                (neq, ":is_fighting", 0),
                (eq, ":first_member_is_player", 0),
                (position_move_y, pos1, 2000),
              (try_end),
            (try_end),

            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
              (val_mul, reg0, -1),
              (position_move_x, pos1, reg0),
            (else_try),
              (neq, ":sd_type", sdt_cavalry),
              (neq, ":sd_type", sdt_harcher),
              (call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
              (position_move_x, pos1, reg0),
            (try_end),

            (try_begin),
              (eq, ":sd_type", sdt_archer),
              (call_script, "script_form_archers", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (else_try),
              (this_or_next | eq, ":sd_type", sdt_cavalry),
              (eq, ":sd_type", sdt_harcher),
              (try_begin),
                (ge, ":target_team", 0),	#enemy battlegroup targeted?
                (call_script, "script_formation_current_position", pos29, "$fplayer_team_no", ":division"),
                (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
                (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

                (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
                (assign, ":combined_radius", reg0),
                (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
                (val_add, ":combined_radius", reg0),

                (le, ":distance_to_enemy", ":combined_radius"),
                (call_script, "script_formation_end", "$fplayer_team_no", ":division"),
                (str_store_class_name, s1, ":division"),
                (display_message, "@{s1}: cavalry formation disassembled."),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (else_try),
                (call_script, "script_form_cavalry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player"),
              (try_end),
            (else_try),
              (call_script, "script_form_infantry", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":first_member_is_player", ":fformation"),
            (try_end),

          (else_try),	#divisions not in formation
            (ge, ":target_team", 0),	#enemy battlegroup targeted?
            (store_add, ":slot", slot_team_d0_target_division, ":division"),
            (team_get_slot, ":target_division", "$fplayer_team_no", ":slot"),
            (try_begin),
              (this_or_next | eq, ":sd_type", sdt_archer),
              (this_or_next | eq, ":sd_type", sdt_harcher),
              (eq, ":sd_type", sdt_skirmisher),
              (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
              (team_slot_ge, "$fplayer_team_no", ":slot", 1),	#ranged are firing?
              (call_script, "script_battlegroup_get_position", pos1, "$fplayer_team_no", ":division"),	#stop advancing
            (else_try),
              (call_script, "script_battlegroup_get_attack_destination", pos1, "$fplayer_team_no", ":division", ":target_team", ":target_division"),
            (try_end),
            (call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", pos1),
            (team_get_movement_order, ":existing_order", "$fplayer_team_no", ":division"),
            (try_begin),
              (ge, ":target_team", 0),	#enemy battlegroup targeted?
              (call_script, "script_battlegroup_get_position", pos29, "$fplayer_team_no", ":division"),
              (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":target_team", ":target_division"),
              (get_distance_between_positions, ":distance_to_enemy", pos29, Enemy_Team_Pos),

              (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", ":division"),
              (assign, ":combined_radius", reg0),
              (call_script, "script_battlegroup_get_action_radius", ":target_team", ":target_division"),
              (val_add, ":combined_radius", reg0),

              (le, ":distance_to_enemy", ":combined_radius"),
              (try_begin),
                (neq, ":existing_order", mordr_charge),
                (set_show_messages, 0),
                (team_give_order, "$fplayer_team_no", ":division", mordr_charge),
                (set_show_messages, 1),
              (try_end),
            (else_try),
              (neq, ":existing_order", mordr_hold),
              (set_show_messages, 0),
              (team_give_order, "$fplayer_team_no", ":division", mordr_hold),
              (set_show_messages, 1),
            (try_end),
          (try_end),
        (try_end),	#Periodic Reform
      (try_end),	#Division Loop

      (assign, "$FormAI_autorotate", ":save_autorotate"),]),


  # #Utilities used by formations
  # script_cf_is_thrusting_weapon by motomataru
  # Input: item
  # Output: T/F
  ("cf_is_thrusting_weapon", [
      (store_script_param, ":item", 1),
      (is_between, ":item", weapons_begin, weapons_end),
      (item_get_thrust_damage, ":thrust_damage", ":item"),
      (item_get_swing_damage, ":swing_damage", ":item"),
      (val_mul, ":thrust_damage", 3),	#it seems thrusts connect faster than swings (as they should) although the
      #animations seem to take the same time
      (val_div, ":thrust_damage", 2),	#factor this in with approximation 2*PI/4 (distance swing must travel vs.
      #thrust) This ignores length, which creates too large a differential.  This is
      #a happy medium.
      (ge, ":thrust_damage", ":swing_damage"),]),

  # script_cf_is_weapon_ranged by motomataru
  # Input: weapon ID, flag 0/1 to consider thrown weapons
  # Output: T/F
  ("cf_is_weapon_ranged", [
      (store_script_param, ":weapon", 1),
      (store_script_param, ":include_thrown", 2),

      (assign, ":test_val", 0),
      (try_begin),
        (ge, ":weapon", 0),
        (item_get_type, ":type", ":weapon"),
        (try_begin),
          (this_or_next | eq, ":type", itp_type_bow),
          (this_or_next | eq, ":type", itp_type_crossbow),
          (this_or_next | eq, ":type", itp_type_pistol),
          (eq, ":type", itp_type_musket),
          (assign, ":test_val", 1),
        (else_try),
          (eq, ":type", itp_type_thrown),
          (neq, ":include_thrown", 0),
          (assign, ":test_val", 1),
        (try_end),
      (try_end),

      (neq, ":test_val", 0),]),

  # script_equip_best_melee_weapon by motomataru
  # Input: agent id, flag to force shield, flag to force for length ALONE,
  # current fire order
  # Output: none
  ("equip_best_melee_weapon", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":force_shield", 2),
      (store_script_param, ":force_length", 3),
      (store_script_param, ":fire_order", 4),

      (agent_get_wielded_item, ":cur_wielded", ":agent", 0),
      (try_begin),
        (call_script, "script_cf_is_weapon_ranged", ":cur_wielded", 0),
        (agent_get_ammo, ":ammo", ":agent", 1),
        (gt, ":ammo", 0),

      (else_try),
        #priority items
        (assign, ":shield", itm_no_item),
        (assign, ":weapon", itm_no_item),
        (try_for_range, ":item_slot", ek_item_0, ek_head),
          (agent_get_item_slot, ":item", ":agent", ":item_slot"),
          (gt, ":item", itm_no_item),
          (item_get_type, ":weapon_type", ":item"),
          (try_begin),
            (eq, ":weapon_type", itp_type_shield),
            (assign, ":shield", ":item"),
          (else_try),
            (eq, ":weapon_type", itp_type_thrown),
            (eq, ":fire_order", aordr_fire_at_will),
            # (agent_get_ammo, ":ammo", ":agent", 0), #assume infantry would have no
            # other kind of ranged weapon
            # (gt, ":ammo", 0),
            (assign, ":weapon", ":item"),	#use thrown weapons first
          (try_end),
        (try_end),

        #select weapon
        (try_begin),
          (eq, ":weapon", itm_no_item),
          (assign, ":cur_score", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (gt, ":item", itm_no_item),
            (item_get_type, ":weapon_type", ":item"),
            (neq, ":weapon_type", itp_type_shield),

            (try_begin),
              (item_has_property, ":item", itp_two_handed),
              (assign, reg0, 1),
            (else_try),
              (assign, reg0, 0),
            (try_end),

            (this_or_next | eq, reg0, 0),
            (this_or_next | eq, ":force_shield", 0),
            (eq, ":shield", itm_no_item),

            (try_begin),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),

            (else_try),
              (try_begin),
                (neq, ":force_length", 0),
                (item_get_weapon_length, ":item_length", ":item"),
                (try_begin),
                  (lt, ":cur_score", ":item_length"),
                  (assign, ":cur_score", ":item_length"),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (troop_is_guarantee_horse, ":troop_id"),
                (agent_get_horse, ":horse", ":agent"),
                (le, ":horse", 0),
                (try_for_range, ":item_slot", ek_item_0, ek_head),
                  (agent_get_item_slot, ":item", ":agent", ":item_slot"),
                  (gt, ":item", itm_no_item),
                  (item_get_type, ":weapon_type", ":item"),
                  (eq, ":weapon_type", itp_type_one_handed_wpn),
                  (item_get_swing_damage, ":swing", ":item"),
                  (gt, ":swing", 19),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (assign, ":imod", imod_plain),
                (try_begin),    #only heroes have item modifications
                  (troop_is_hero, ":troop_id"),
                  (try_for_range, ":troop_item_slot",  ek_item_0, ek_head),    # heroes have only 4 possible weapons (equipped)
                    (troop_get_inventory_slot, reg0, ":troop_id", ":troop_item_slot"),  #Find Item Slot with same item ID as Equipped Weapon
                    (eq, reg0, ":item"),
                    (troop_get_inventory_slot_modifier, ":imod", ":troop_id", ":troop_item_slot"),
                  (try_end),
                (try_end),
                (call_script, "script_evaluate_item", ":item", ":imod"),
                (lt, ":cur_score", reg0),
                (assign, ":cur_score", reg0),
                (assign, ":weapon", ":item"),
              (try_end),
            (try_end),  #melee weapon
          (try_end),  #weapon slot loop
        (try_end),  #select weapon

        #equip selected items if needed
        (try_begin),
          (neq, ":cur_wielded", ":weapon"),
          (try_begin),
            (gt, ":shield", itm_no_item),
            (agent_get_wielded_item, reg0, ":agent", 1),
            (neq, reg0, ":shield"),	#reequipping secondary will UNequip (from experience)
            (agent_set_wielded_item, ":agent", ":shield"),
          (try_end),
          (gt, ":weapon", itm_no_item),
          (agent_set_wielded_item, ":agent", ":weapon"),
        (try_end),
      (try_end),]),

  # script_set_formation_destination by motomataru
  # Input: team, troop class, position
  # Kluge around buggy *_order_position functions for teams 0-3
  ("set_formation_destination", [
      (store_script_param, ":fteam", 1),
      (store_script_param, ":fdivision", 2),
      (store_script_param, ":fposition", 3),

      (position_get_x, ":x", ":fposition"),
      (position_get_y, ":y", ":fposition"),
      (position_get_rotation_around_z, ":zrot", ":fposition"),

      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":x"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":y"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":zrot"),

      (team_set_order_position, ":fteam", ":fdivision", ":fposition"),]),

  # script_get_formation_destination by motomataru
  # Input: position, team, troop class
  # Output: input position (pos0 used)
  # Kluge around buggy *_order_position functions for teams 0-3
  ("get_formation_destination", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (init_position, ":fposition"),
      # (try_begin),
      #(is_between, ":fteam", 0, 4), #Caba - this will always pass MOTO except in
      #mods with more than four teams (eg SWC arena) but now obsolete by other
      #limits
      (store_add, ":slot", slot_team_d0_destination_x, ":fdivision"),
      (team_get_slot, ":x", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_y, ":fdivision"),
      (team_get_slot, ":y", ":fteam", ":slot"),
      (store_add, ":slot", slot_team_d0_destination_zrot, ":fdivision"),
      (team_get_slot, ":zrot", ":fteam", ":slot"),

      (position_set_x, ":fposition", ":x"),
      (position_set_y, ":fposition", ":y"),
      (position_rotate_z, ":fposition", ":zrot"),
      # (else_try),
      # (store_add, ":slot", slot_team_d0_first_member, ":fdivision"), #only
      # defined for divisions in formation
      # (team_get_slot, reg0, ":fteam", ":slot"),
      # (try_begin), # "launder" team_get_order_position shutting down
      # position_move_x
      # (gt, reg0, -1),
      # (team_get_order_position, ":fposition", ":fteam", ":fdivision"),
      # (agent_get_position, pos0, reg0),
      # (agent_set_position, reg0, ":fposition"),
      # (agent_get_position, ":fposition", reg0),
      # (agent_set_position, reg0, pos0),
      # (try_end),
      # (try_end),
      (position_set_z_to_ground_level, ":fposition"),]),

  # script_formation_current_position by motomataru
  # Input: destination position (not pos0), team, division
  # Output: in destination position
  # As opposed to script_battlegroup_get_position, this obtains target rotation
  # from formation destination and positions at the center of the front
  ("formation_current_position", [
      (store_script_param, ":fposition", 1),
      (store_script_param, ":fteam", 2),
      (store_script_param, ":fdivision", 3),
      (call_script, "script_battlegroup_get_position", ":fposition", ":fteam", ":fdivision"),
      (call_script, "script_get_formation_destination", pos0, ":fteam", ":fdivision"),
      (position_copy_rotation, ":fposition", pos0),
      (call_script, "script_battlegroup_dist_center_to_front", ":fteam", ":fdivision"),
      (position_move_y, ":fposition", reg0, 0),]),

  # script_str_store_division_type_name by motomataru
  # Input: destination, division type (sdt_*)
  # Output: none
  ("str_store_division_type_name", [
      (store_script_param, ":str_reg", 1),
      (store_script_param, ":division_type", 2),
      (try_begin),
        (eq, ":division_type", sdt_infantry),
        (str_store_string, ":str_reg", "@infantry"),
      (else_try),
        (eq, ":division_type", sdt_archer),
        (str_store_string, ":str_reg", "@archer"),
      (else_try),
        (eq, ":division_type", sdt_cavalry),
        (str_store_string, ":str_reg", "@cavalry"),
      (else_try),
        (eq, ":division_type", sdt_polearm),
        (str_store_string, ":str_reg", "@polearm"),
      (else_try),
        (eq, ":division_type", sdt_skirmisher),
        (str_store_string, ":str_reg", "@skirmisher"),
      (else_try),
        (eq, ":division_type", sdt_harcher),
        (str_store_string, ":str_reg", "@mounted archer"),
      (else_try),
        (eq, ":division_type", sdt_support),
        (str_store_string, ":str_reg", "@support"),
      (else_try),
        (eq, ":division_type", sdt_bodyguard),
        (str_store_string, ":str_reg", "@bodyguard"),
      (else_try),
        (str_store_string, ":str_reg", "@undetermined type of"),
      (try_end),]),

  # script_formation_to_native_order by motomataru
  # Input: team, division, formation
  # Output: issues team_give_order with appropriate command to make formation
  ("formation_to_native_order", [
      (store_script_param, ":team", 1),
      (store_script_param, ":division", 2),
      (store_script_param, ":formation", 3),

      (try_begin),
        (gt, ":formation", formation_none),	#custom formation (bad call)

      (else_try),
        (eq, Native_Formations_Implementation, WB_Implementation),
        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":spacing", ":team", ":slot"),
        (val_sub, ":spacing", ":formation"),	#formation constants indicate number of "Stand Closer"
        (set_show_messages, 0),
        (try_for_range, reg0, 0, ":spacing"),
          (team_give_order, ":team", ":division", mordr_stand_closer),
        (try_end),
        (set_show_messages, 1),
        (team_set_slot, ":team", ":slot", ":spacing"),

      #WFAS implementation
      (else_try),
        (eq, ":formation", formation_1_row),
        (team_give_order, ":team", ":division", mordr_form_1_row),
      (else_try),
        (eq, ":formation", formation_2_row),
        (team_give_order, ":team", ":division", mordr_form_2_row),
      (else_try),
        (eq, ":formation", formation_3_row),
        (team_give_order, ":team", ":division", mordr_form_3_row),
      (else_try),
        (eq, ":formation", formation_4_row),
        (team_give_order, ":team", ":division", mordr_form_4_row),
      (else_try),
        (eq, ":formation", formation_5_row),
        (team_give_order, ":team", ":division", mordr_form_5_row),
      (try_end)]),

  # script_point_y_toward_position by motomataru
  # Input: from position, to position
  # Output: reg0 distance in cm
  # Basically, points the first position at the second, so then simple move_y
  # will move back and forth and move_x side to side
  # Things like cast_ray work with this as well
  ("point_y_toward_position", [
      (store_script_param, ":from_position", 1),
      (store_script_param, ":to_position", 2),
      (assign, ":save_fpm", 1),
      (convert_to_fixed_point, ":save_fpm"),
      (set_fixed_point_multiplier, 100),  #to match cm returned by get_distance_between_positions

      #remove current rotation
      (position_get_x, ":from_x", ":from_position"),
      (position_get_y, ":from_y", ":from_position"),
      (position_get_z, ":from_z", ":from_position"),
      (init_position, ":from_position"),
      (position_set_x, ":from_position", ":from_x"),
      (position_set_y, ":from_position", ":from_y"),
      (position_set_z, ":from_position", ":from_z"),

      #horizontal rotation
      (position_get_x, ":change_in_x", ":to_position"),
      (val_sub, ":change_in_x", ":from_x"),
      (position_get_y, ":change_in_y", ":to_position"),
      (val_sub, ":change_in_y", ":from_y"),

      (try_begin),
        (this_or_next | neq, ":change_in_y", 0),
        (neq, ":change_in_x", 0),
        (store_atan2, ":theta", ":change_in_y", ":change_in_x"),
        (assign, ":ninety", 90),
        (convert_to_fixed_point, ":ninety"),
        (val_sub, ":theta", ":ninety"),	#point Y axis at to position
        (position_rotate_z_floating, ":from_position", ":theta"),
      (try_end),

      #vertical rotation
      (get_distance_between_positions, ":distance_between", ":from_position", ":to_position"),
      (try_begin),
        (gt, ":distance_between", 0),
        (position_get_z, ":dist_z_to_sine", ":to_position"),
        (val_sub, ":dist_z_to_sine", ":from_z"),
        (val_div, ":dist_z_to_sine", ":distance_between"),
        (store_asin, ":theta", ":dist_z_to_sine"),
        (position_rotate_x_floating, ":from_position", ":theta"),
      (try_end),

      (assign, reg0, ":distance_between"),
      (set_fixed_point_multiplier, ":save_fpm"),]),

  #script_agent_fix_division
  #Input: agent_id
  #Output: nothing (agent divisions changed, slot set)
  #To fix AI troop divisions from the engine applying player's party divisions
  #on all agents
  #This is called after agent_reassign_team, so can safely assume correct team
  #is set
  ("agent_fix_division", [
      (store_script_param_1, ":agent"),
      (agent_set_slot, ":agent", slot_agent_new_division, -1),
      (get_player_agent_no, ":player"),	#after_mission_start triggers are called after spawn, so globals can't be used
      #yet

      (try_begin),
        (ge, ":player", 0),
        (neq, ":agent", ":player"),
        (agent_is_human, ":agent"),
        (agent_get_group, ":player_team", ":player"),
        (agent_get_group, ":team", ":agent"),
        (this_or_next | main_hero_fallen),
        (neq, ":team", ":player_team"),

        (assign, ":target_division", grc_infantry),
        (agent_get_horse, ":horse", ":agent"),
        (agent_get_troop_id, ":troop_no", ":agent"),

        #logic from script_troop_default_division
        #limited to the three divisions the AI currently uses
        (try_begin),
          (this_or_next | ge, ":horse", 0),
          (troop_is_guarantee_horse, ":troop_no"),
          (assign, ":target_division", grc_cavalry),

          #(troop_is_guarantee_ranged, ":troop_no"),
          # (try_for_range, ":ranged", "itm_darts", "itm_flintlock_pistol"),
              # (agent_has_item_equipped, ":agent", ":ranged"),
              # (agent_get_ammo, reg1, ":agent", 0),
              # (gt, reg1, 0),
              # (assign, ":target_division", sdt_harcher),
          # (try_end),


          # (try_begin),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_weapon_ranged", ":item", 1),
          # (assign, ":target_division", sdt_harcher),
          # (try_end),
          # (try_end),

        (else_try),
          (troop_is_guarantee_ranged, ":troop_no"),
          # (assign, ":has_ranged", 0),

          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (call_script, "script_cf_is_weapon_ranged", ":item", 1),
            (agent_get_ammo, reg1, ":agent", 0),
            (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
            # (item_get_type, reg1, ":item"),
            # (try_begin),
            # (eq, reg1, itp_type_thrown),
            # (eq, ":flag_0_for_expanded", 0),
            # (neq, ":target_division", grc_archers),
            # (assign, ":target_division", sdt_skirmisher),
            # (else_try),
            (assign, ":target_division", grc_archers),
            # (try_end),
            # (assign, ":has_ranged", 1),
          (try_end),

          # (neq, ":has_ranged", 0),

          # (else_try),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_thrusting_weapon", ":item"),
          # (item_get_type, reg1, ":item"),
          # (eq, reg1, itp_type_polearm),
          # (assign, ":target_division", sdt_polearm),
          # (try_end),
        (try_end),

        (agent_get_division, ":division", ":agent"),
        (neq, ":division", ":target_division"),
        (agent_set_division, ":agent", ":target_division"),
        (agent_set_slot, ":agent", slot_agent_new_division, ":target_division"),
      (try_end),]),

  # script_store_battlegroup_type
  # Input: team, division
  # Output: reg0 and slot_team_dx_type with sdt_* value
  # Automatically called from store_battlegroup_data
  ("store_battlegroup_type", [
      (store_script_param_1, ":fteam"),
      (store_script_param_2, ":fdivision"),

      (assign, ":count_infantry", 0),
      (assign, ":count_archer", 0),
      (assign, ":count_cavalry", 0),
      (assign, ":count_harcher", 0),
      (assign, ":count_polearms", 0),
      (assign, ":count_skirmish", 0),
      (assign, ":count_support", 0),
      (assign, ":count_bodyguard", 0),

      (team_get_leader, ":leader", ":fteam"),

      (try_for_agents, ":cur_agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":leader", ":cur_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        (try_begin),
          (neg | troop_is_hero, ":cur_troop"),
          (try_begin), #Cavalry
            (agent_get_horse, reg0, ":cur_agent"),
            (ge, reg0, 0),
            (try_begin),
              (ge, ":cur_ammo", minimum_ranged_ammo),
              (val_add, ":count_harcher", 1),
            (else_try),
              (val_add, ":count_cavalry", 1),
            (try_end),
          (else_try), #Archers
            (ge, ":cur_ammo", minimum_ranged_ammo),
            # #use when troops are equipped with ranged at start of battle
            # (agent_get_class, ":bgclass", ":cur_agent"),
            # (eq, ":bgclass", grc_archers),
            # #end use when troops equipped with ranged at start of battle
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (gt, ":item", 0),
              (item_get_type, ":weapontype", ":item"),
              (is_between, ":weapontype", itp_type_bow, itp_type_thrown),  # bow or crossbow
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find bow or crossbow
              (val_add, ":count_skirmish", 1),
            (else_try),
              (val_add, ":count_archer", 1),
            (try_end),
          (else_try), #Infantry
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, ":weapontype", ":item"),
              (eq, ":weapontype", itp_type_polearm),
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find a polearm
              (val_add, ":count_infantry", 1),
            (else_try),
              (val_add, ":count_polearms", 1),
            (try_end),
          (try_end),
        (else_try), #Heroes
          (assign, ":support_skills", 0), #OPEN TO SUGGESTIONS HERE ?skl_trade, skl_spotting, skl_pathfinding,
          #skl_tracking?
          (store_skill_level, reg0, skl_engineer, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_first_aid, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_surgery, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_wound_treatment, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (try_begin),
            (gt, ":support_skills", 5),
            (val_add, ":count_support", 1),
          (else_try),
            (val_add, ":count_bodyguard", 1),
          (try_end),
        (try_end), #Regular v Hero
      (try_end), #Agent Loop

      #Do Comparisons With Counts, set ":div_type"
      (assign, ":slot", slot_team_d0_type),
      (team_set_slot, scratch_team, ":slot", ":count_infantry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_archer"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_cavalry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_polearms"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_skirmish"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_harcher"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_support"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_bodyguard"),

      (assign, ":count_to_beat", 0),
      (assign, ":count_total", 0),
      (try_for_range, ":type", sdt_infantry, sdt_infantry + 8), #only 8 sdt_types at the moment
        (store_add, ":slot", slot_team_d0_type, ":type"),
        (team_get_slot, ":count", scratch_team, ":slot"),
        (val_add, ":count_total", ":count"),
        (lt, ":count_to_beat", ":count"),
        (assign, ":count_to_beat", ":count"),
        (assign, ":div_type", ":type"),
      (try_end),

      (val_mul, ":count_to_beat", 2),
      (try_begin),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":count_to_beat", 0),
        (assign, ":div_type", -1),
        (try_for_range, ":type", sdt_infantry, sdt_infantry + 3), #check main types for a majority
          (store_add, ":slot", slot_team_d0_type, ":type"),
          (team_get_slot, ":count", scratch_team, ":slot"),
          (val_add, ":slot", 3),	#subtype is three more than main type
          (team_get_slot, reg0, scratch_team, ":slot"),
          (val_add, ":count", reg0),
          (lt, ":count_to_beat", ":count"),
          (assign, ":count_to_beat", ":count"),
          (assign, ":div_type", ":type"),
        (try_end),

        (val_mul, ":count_to_beat", 2),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":div_type", sdt_unknown), #Or 0
      (try_end),

      #hard-code traditional infantry division (avoid player confusion for mods
      #which arm troops with ranged at start of battle)
      (try_begin),
        (eq, ":fdivision", grc_infantry),
        (neq, ":div_type", sdt_polearm),
        (assign, ":div_type", sdt_infantry),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":div_type"),
      (assign, reg0, ":div_type"),]),

  # script_store_battlegroup_data by motomataru #EDITED TO SLOTS FOR MANY
  # DIVISIONS BY CABA'DRIN
  # Input: none
  # Output: sets positions and globals to track data on ALL groups in a battle
  # Globals used: pos0, pos1, reg0
  ("store_battlegroup_data", [
      (assign, ":team0_leader", 0),
      (assign, ":team0_x_leader", 0),
      (assign, ":team0_y_leader", 0),
      (assign, ":team0_zrot_leader", 0),
      (assign, ":team0_level_leader", 0),
      (assign, ":team1_leader", 0),
      (assign, ":team1_x_leader", 0),
      (assign, ":team1_y_leader", 0),
      (assign, ":team1_zrot_leader", 0),
      (assign, ":team1_level_leader", 0),
      (assign, ":team2_leader", 0),
      (assign, ":team2_x_leader", 0),
      (assign, ":team2_y_leader", 0),
      (assign, ":team2_zrot_leader", 0),
      (assign, ":team2_level_leader", 0),
      (assign, ":team3_leader", 0),
      (assign, ":team3_x_leader", 0),
      (assign, ":team3_y_leader", 0),
      (assign, ":team3_zrot_leader", 0),
      (assign, ":team3_level_leader", 0),

      #save some info
      (try_for_range, ":division", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (try_begin),
          (team_slot_ge, "$fplayer_team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 1),

        (else_try),
          (store_add, ":slot", slot_team_d0_exists, ":division"),
          (team_set_slot, "$fplayer_team_no", ":slot", 0),
        (try_end),
      (try_end),

      #Team Slots reset every mission, like agent slots, but just to be sure for
      #when it gets called during the mission
      (try_for_range, ":slot", reset_team_stats_begin, reset_team_stats_end), #Those within the "RESET GROUP" in formations_constants
        (try_for_range, ":team", 0, 4),
          (team_set_slot, ":team", ":slot", 0),
        (try_end),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, -1),

        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 0),

        (agent_get_group, ":bgteam", ":cur_agent"),
        (agent_get_division, ":bgdivision", ":cur_agent"),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (agent_get_position, pos1, ":cur_agent"),

        (try_begin),
          (agent_is_non_player, ":cur_agent"),

          (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
          (team_get_slot, ":bgtype", ":bgteam", ":slot"),
          (this_or_next | eq, ":bgtype", sdt_cavalry),	#assigned to horsed division
          (eq, ":bgtype", sdt_harcher),

          (team_get_riding_order, reg0, ":bgteam", ":bgdivision"),
          (neq, reg0, rordr_dismount),

          (team_get_order_position, pos0, ":bgteam", ":bgdivision"),
          (get_distance_between_positions, ":old_distance", pos0, pos1),
          (gt, ":old_distance", AI_charge_distance),	#agent is out of formation?

          (assign, ":target_type", ":bgtype"),

          (try_begin),
            (eq, ":agent_class", grc_infantry),	#Native has transferred this agent to infantry
            (assign, ":target_type", sdt_infantry),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_polearm),
              (assign, ":target_type", sdt_polearm),
            (try_end),

          (else_try),
            (eq, ":agent_class", grc_archers),	#Native has transferred this agent to archers
            (assign, ":target_type", sdt_archer),

            (try_for_range, ":item_slot", ek_item_0, ek_head),
              (eq, ":bgteam", "$fplayer_team_no"),	#AI doesn't use extended right now
              (agent_get_item_slot, ":item", ":cur_agent", ":item_slot"),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),
              (agent_get_ammo, reg1, ":cur_agent", 0),
              (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
              (item_get_type, reg0, ":item"),
              (eq, reg0, itp_type_thrown),
              (assign, ":target_type", sdt_skirmisher),
            (try_end),
          (try_end),

          (neq, ":target_type", ":bgtype"),
          (assign, ":bgdivision", ":target_type"),

          (try_for_range_backwards, ":new_division", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (gt, reg0, 0),

            (store_add, ":slot", slot_team_d0_type, ":new_division"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (eq, reg0, ":target_type"),

            (assign, ":bgdivision", ":new_division"),
          (try_end),

          (try_begin),
            (store_add, ":slot", slot_team_d0_exists, ":bgdivision"),
            (team_slot_eq, "$fplayer_team_no", ":slot", 0),	#division does not yet exist?
            (agent_is_alive, "$fplayer_agent_no"),
            (store_add, ":slot", slot_team_d0_move_order, ":bgdivision"),
            (neg | team_slot_eq, "$fplayer_team_no", ":slot", mordr_follow),
            (team_set_slot, "$fplayer_team_no", ":slot", mordr_follow),
            (set_show_messages, 0),
            (team_give_order, "$fplayer_team_no", ":bgdivision", mordr_follow),
            (set_show_messages, 1),
          (try_end),

          (agent_set_slot, ":cur_agent", slot_agent_new_division, ":bgdivision"),	#reassign
          (agent_set_division, ":cur_agent", ":bgdivision"),

        (else_try),	#Maintain any changed divisions (apparently agents get switched back)
          (agent_is_non_player, ":cur_agent"),
          (agent_slot_ge, ":cur_agent", slot_agent_new_division, 0),
          (neg | agent_slot_eq, ":cur_agent", slot_agent_new_division, ":bgdivision"),
          (agent_get_slot, ":bgdivision", ":cur_agent", slot_agent_new_division),
          (agent_set_division, ":cur_agent", ":bgdivision"),
        (try_end),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (try_begin),
          (game_in_multiplayer_mode),
          (try_begin),
            (is_between, ":cur_troop", multiplayer_troops_begin, multiplayer_troops_end),	#it's a player
            (assign, ":bgdivision", -1),
          (try_end),
        (else_try),
          (team_get_leader, ":leader", ":bgteam"),
          (eq, ":leader", ":cur_agent"),
          (assign, ":bgdivision", -1),
        (try_end),
        (store_character_level, ":cur_level", ":cur_troop"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        #get weapon characteristics
        (assign, ":cur_weapon_type", 0),
        (assign, ":cur_weapon_length", 0),
        (assign, ":cur_swung_weapon_length", 0),
        (agent_get_wielded_item, ":cur_weapon", ":cur_agent", 0),
        (try_begin),
          (is_between, ":cur_weapon", weapons_begin, weapons_end),
          # (neg | is_between, ":cur_weapon", estandartes_begin, estandartes_end),	#put exceptions here, such as standards, that will otherwise force a lot of
          #extra spacing for nothing
          (item_get_weapon_length, ":cur_weapon_length", ":cur_weapon"),

          (try_begin),
            (call_script, "script_cf_is_thrusting_weapon", ":cur_weapon"),
          (else_try),
            (assign, ":cur_swung_weapon_length", ":cur_weapon_length"),
          (try_end),
        (try_end),

        #add up armor
        (assign, ":cur_avg_armor", 0),
        (try_for_range, ":item_slot", ek_head, ek_horse),
          (agent_get_item_slot, ":armor", ":cur_agent", ":item_slot"),
          (gt, ":armor", itm_no_item),
          (item_get_head_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
          (item_get_leg_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (agent_get_wielded_item, ":armor", ":cur_agent", 1),	#include shield
        (try_begin),
          (gt, ":armor", itm_no_item),
          (item_get_type, ":item_type", ":armor"),
          (eq, ":item_type", itp_type_shield),
          (item_get_body_armor, reg0, ":armor"),
          (val_add, ":cur_avg_armor", reg0),
        (try_end),
        (val_div, ":cur_avg_armor", 3),	#average the zones (head, body, leg)

        #average with horse armor for mounted agents
        (agent_get_horse, ":cur_horse", ":cur_agent"),
        (try_begin),
          (gt, ":cur_horse", -1),
          (agent_get_item_id, ":itm_horse", ":cur_horse"),
          (gt, ":itm_horse", itm_no_item),
          (item_get_body_armor, reg0, ":itm_horse"),
          (val_add, ":cur_avg_armor", reg0),
          (val_div, ":cur_avg_armor", 2),
        (try_end),

        (position_get_x, ":x_value", pos1),
        (position_get_y, ":y_value", pos1),
        (position_get_rotation_around_z, ":zrot_value", pos1),
        (try_begin),
          (eq, ":bgdivision", -1), #Leaders
          (try_begin),
            (eq, ":bgteam", 0),
            (assign, ":team0_leader", 1),
            (assign, ":team0_x_leader", ":x_value"),
            (assign, ":team0_y_leader", ":y_value"),
            (assign, ":team0_zrot_leader", ":zrot_value"),
            (assign, ":team0_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 1),
            (assign, ":team1_leader", 1),
            (assign, ":team1_x_leader", ":x_value"),
            (assign, ":team1_y_leader", ":y_value"),
            (assign, ":team1_zrot_leader", ":zrot_value"),
            (assign, ":team1_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 2),
            (assign, ":team2_leader", 1),
            (assign, ":team2_x_leader", ":x_value"),
            (assign, ":team2_y_leader", ":y_value"),
            (assign, ":team2_zrot_leader", ":zrot_value"),
            (assign, ":team2_level_leader", ":cur_level"),
          (else_try),
            (eq, ":bgteam", 3),
            (assign, ":team3_leader", 1),
            (assign, ":team3_x_leader", ":x_value"),
            (assign, ":team3_y_leader", ":y_value"),
            (assign, ":team3_zrot_leader", ":zrot_value"),
            (assign, ":team3_level_leader", ":cur_level"),
          (try_end),
        (else_try),
          # (agent_get_ammo, reg0, ":cur_agent", 1), #Division in Melee
          (try_begin),
            # (le, reg0, 0), #not wielding ranged weapon?
            (agent_get_attack_action, reg0, ":cur_agent"),
            (gt, reg0, 0),
            (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
            (team_get_slot, reg0, ":bgteam", ":slot"),
            (val_add, reg0, 1),
            (team_set_slot, ":bgteam", ":slot", reg0),
          (try_end),

          (store_add, ":slot", slot_team_d0_size, ":bgdivision"), #Division Count
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),
            (ge, ":cur_ammo", minimum_ranged_ammo),
            (store_add, ":slot", slot_team_d0_percent_ranged, ":bgdivision"), #Division Percentage are Archers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (else_try),
            (store_add, ":slot", slot_team_d0_low_ammo, ":bgdivision"), #Division Running out of Ammo Flag
            (team_set_slot, ":bgteam", ":slot", 1),
          (try_end),

          (try_begin),
            (eq, ":cur_weapon_type", itp_type_thrown),
            (store_add, ":slot", slot_team_d0_percent_throwers, ":bgdivision"), #Division Percentage are Throwers
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (val_add, ":value", 1),
            (team_set_slot, ":bgteam", ":slot", ":value"),
          (try_end),

          (store_add, ":slot", slot_team_d0_level, ":bgdivision"), #Division Level
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_level"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":bgdivision"), #Division Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_weapon_length"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_swung_weapon_length, ":bgdivision"), #Division Swung Weapon Length
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (try_begin),
            (lt, ":value", ":cur_swung_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_swung_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_armor, ":bgdivision"), #Division Armor
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":cur_avg_armor"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (try_begin),	#Division First Rank Shortest Weapon Length
            (agent_slot_eq, ":cur_agent", slot_agent_formation_rank, 1),
            (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, ":value", 0),
            (gt, ":value", ":cur_weapon_length"),
            (team_set_slot, ":bgteam", ":slot", ":cur_weapon_length"),
          (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"), #Position X
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":x_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"), #Position Y
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":y_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"), #Rotation
          (team_get_slot, ":value", ":bgteam", ":slot"),
          (val_add, ":value", ":zrot_value"),
          (team_set_slot, ":bgteam", ":slot", ":value"),
        (try_end), #Leader vs Regular

        (try_begin),
          (eq, ":agent_class", grc_archers),
          (team_get_slot, ":value", ":bgteam", slot_team_num_archers),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_archers, ":value"),

        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_cavalry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_cavalry, ":value"),

        (else_try),
          (eq, ":agent_class", grc_infantry),
          (team_get_slot, ":value", ":bgteam", slot_team_num_infantry),
          (val_add, ":value", 1),
          (team_set_slot, ":bgteam", slot_team_num_infantry, ":value"),
        (try_end),

        #find nearest enemy agent
        (assign, ":nearest_runner", -1),
        (agent_ai_get_num_cached_enemies, ":num_nearby_agents", ":cur_agent"),
        (try_for_range, reg0, 0, ":num_nearby_agents"),
          (agent_ai_get_cached_enemy, ":enemy_agent", ":cur_agent", reg0),
          (agent_is_alive, ":enemy_agent"),

          (try_begin),
            (eq, ":nearest_runner", -1),
            (assign, ":nearest_runner", ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":nearest_runner"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (assign, ":nearest_runner", ":enemy_agent"),
          (try_end),

          (agent_slot_eq, ":enemy_agent", slot_agent_is_running_away, 0),

          (try_begin),
            (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
            (eq, ":closest_enemy", -1),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),

          (else_try),
            (agent_get_position, pos0, ":enemy_agent"),
            (get_distance_between_positions, ":new_distance", pos0, pos1),
            (agent_get_position, pos0, ":closest_enemy"),
            (get_distance_between_positions, ":old_distance", pos0, pos1),
            (lt, ":new_distance", ":old_distance"),
            (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":enemy_agent"),
          (try_end),
        (try_end),
        (try_begin),
          (agent_slot_eq, ":cur_agent", slot_agent_nearest_enemy_agent, -1),
          (agent_set_slot, ":cur_agent", slot_agent_nearest_enemy_agent, ":nearest_runner"),
        (try_end),

        #exploit closest agent data
        (try_begin),
          (agent_get_slot, ":closest_enemy", ":cur_agent", slot_agent_nearest_enemy_agent),
          (neq, ":closest_enemy", -1),
          (agent_get_position, pos0, ":closest_enemy"),
          (get_distance_between_positions, ":closest_distance", pos0, pos1),

          #check target of AI agent behavior
          (try_begin),
            (agent_is_non_player, ":cur_agent"),

            (agent_ai_get_behavior_target, ":cur_targeted_agent", ":cur_agent"),
            (neq, ":closest_enemy", ":cur_targeted_agent"),

            (this_or_next | neg | agent_is_non_player, ":closest_enemy"),	#AI can always sense player behind them (balancing factor, dedicated to
            #Idibil)
            (neg | position_is_behind_position, pos0, pos1),

            (lt, ":closest_distance", 2000),	#Assuming rethink is expensive, don't bother beyond 20m

            (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),
            (this_or_next | eq, formation_rethink_for_formations_only, 0),
            (gt, ":value", formation_none),

            (agent_force_rethink, ":cur_agent"),
          (try_end),

          #update division information
          (try_begin),
            (ge, ":bgdivision", 0),	#not leaders

            (try_begin),
              (lt, ":closest_distance", 350),
              (agent_get_division, reg0, ":closest_enemy"),
              (store_add, ":slot", slot_team_d0_enemy_supporting_melee, reg0),
              (agent_get_group, reg0, ":closest_enemy"),
              (team_get_slot, ":value", reg0, ":slot"),
              (val_add, ":value", 1),
              (team_set_slot, reg0, ":slot", ":value"),
            (try_end),

            (store_add, ":slot", slot_team_d0_closest_enemy_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),

            (assign, ":doit", 0),
            (agent_get_class, ":enemy_agent_class", ":closest_enemy"),
            (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
            (team_get_slot, ":value", ":bgteam", ":slot"),

            #AI infantry division tracks non-infantry to preferably chase
            (try_begin),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (neq, ":enemy_agent_class", grc_cavalry),
              (assign, ":doit", 1),

              #AI archer division tracks infantry to avoid
            (else_try),
              (this_or_next | eq, ":value", sdt_archer),
              (eq, ":value", sdt_skirmisher),
              (eq, ":enemy_agent_class", grc_infantry),
              (assign, ":doit", 1),
            (try_end),

            (eq, ":doit", 1),
            (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":bgdivision"),
            (team_get_slot, ":old_distance", ":bgteam", ":slot"),
            (try_begin),
              (this_or_next | eq, ":old_distance", 0),
              (lt, ":closest_distance", ":old_distance"),
              (team_set_slot, ":bgteam", ":slot", ":closest_distance"),
              (store_add, ":slot", slot_team_d0_closest_enemy_special, ":bgdivision"),
              (team_set_slot, ":bgteam", ":slot", ":closest_enemy"),
            (try_end),
          (try_end),	#update division info
        (try_end),	#exploit closest agent data
      (try_end), #Agent Loop

      #calculate team sizes, sum positions; within calculate battle group averages
      (try_for_range, ":team", 0, 4),
        (assign, ":team_size", 0),
        (assign, ":team_level", 0),
        (assign, ":team_x", 0),
        (assign, ":team_y", 0),
        (assign, ":team_zrot", 0),

        (try_for_range, ":division", 0, 9),
          #sum for team averages
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_get_slot, ":division_size", ":team", ":slot"),
          (gt, ":division_size", 0),
          (val_add, ":team_size", ":division_size"),

          (store_add, ":slot", slot_team_d0_level, ":division"),
          (team_get_slot, ":division_level", ":team", ":slot"),
          (val_add, ":team_level", ":division_level"),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (team_get_slot, ":division_x", ":team", ":slot"),
          (val_add, ":team_x", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (team_get_slot, ":division_y", ":team", ":slot"),
          (val_add, ":team_y", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (team_get_slot, ":division_zrot", ":team", ":slot"),
          (val_add, ":team_zrot", ":division_zrot"),

          #calculate battle group averages
          (store_add, ":slot", slot_team_d0_level, ":division"),
          (val_div, ":division_level", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_level"),

          (store_add, ":slot", slot_team_d0_percent_ranged, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_mul, ":value", 100),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          (store_add, ":slot", slot_team_d0_weapon_length, ":division"),
          (team_get_slot, ":value", ":team", ":slot"),
          (val_div, ":value", ":division_size"),
          (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_swung_weapon_length, ":division"), MOTO
          # systematic testing shows best to use max swung weapon length as basis for
          # formation spacing
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", ":division_size"),
          # (team_set_slot, ":team", ":slot", ":value"),

          # (store_add, ":slot", slot_team_d0_front_agents, ":division"), MOTO front
          # rank should be within shortest weapon distance, not average
          # (team_get_slot, reg0, ":team", ":slot"),
          # (try_begin),
          # (gt, reg0, 0),
          # (store_add, ":slot", slot_team_d0_front_weapon_length, ":division"),
          # (team_get_slot, ":value", ":team", ":slot"),
          # (val_div, ":value", reg0),
          # (team_set_slot, ":team", ":slot", ":value"),
          # (try_end),

          (store_add, ":slot", slot_team_d0_avg_x, ":division"),
          (val_div, ":division_x", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_x"),

          (store_add, ":slot", slot_team_d0_avg_y, ":division"),
          (val_div, ":division_y", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_y"),

          (store_add, ":slot", slot_team_d0_avg_zrot, ":division"),
          (val_div, ":division_zrot", ":division_size"),
          (team_set_slot, ":team", ":slot", ":division_zrot"),

          (store_add, ":slot", slot_team_d0_type, ":division"),
          (team_get_slot, reg0, ":team", ":slot"),
          (try_begin),
            (neg | is_between, reg0, 0, 8),	#TODO reset on reinforcements
            (call_script, "script_store_battlegroup_type", ":team", ":division"),
          (try_end),
        (try_end), #Division Loop

        #Team Leader Additions
        (try_begin),
          (eq, ":team", 0),
          (val_add, ":team_size", ":team0_leader"),
          (val_add, ":team_level", ":team0_level_leader"),
          (val_add, ":team_x", ":team0_x_leader"),
          (val_add, ":team_y", ":team0_y_leader"),
          (val_add, ":team_zrot", ":team0_zrot_leader"),
        (else_try),
          (eq, ":team", 1),
          (val_add, ":team_size", ":team1_leader"),
          (val_add, ":team_level", ":team1_level_leader"),
          (val_add, ":team_x", ":team1_x_leader"),
          (val_add, ":team_y", ":team1_y_leader"),
          (val_add, ":team_zrot", ":team1_zrot_leader"),
        (else_try),
          (eq, ":team", 2),
          (val_add, ":team_size", ":team2_leader"),
          (val_add, ":team_level", ":team2_level_leader"),
          (val_add, ":team_x", ":team2_x_leader"),
          (val_add, ":team_y", ":team2_y_leader"),
          (val_add, ":team_zrot", ":team2_zrot_leader"),
        (else_try),
          (eq, ":team", 3),
          (val_add, ":team_size", ":team3_leader"),
          (val_add, ":team_level", ":team3_level_leader"),
          (val_add, ":team_x", ":team3_x_leader"),
          (val_add, ":team_y", ":team3_y_leader"),
          (val_add, ":team_zrot", ":team3_zrot_leader"),
        (try_end),

        #calculate team averages
        (gt, ":team_size", 0),
        (team_set_slot, ":team", slot_team_size, ":team_size"),
        (val_div, ":team_level", ":team_size"),
        (team_set_slot, ":team", slot_team_level, ":team_level"),

        (val_div, ":team_x", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_x, ":team_x"),
        (val_div, ":team_y", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_y, ":team_y"),
        (val_div, ":team_zrot", ":team_size"),
        (team_set_slot, ":team", slot_team_avg_zrot, ":team_zrot"),
      (try_end), #Team Loop
  ]),

  # script_cf_division_data_available by motomataru
  ("cf_division_data_available", [
      (assign, ":evidence", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (assign, ":evidence", 1),
      (try_end),
      (neq, ":evidence", 0)]),

  # script_battlegroup_get_position by motomataru #CABA - EDITED TO USE SLOTS,
  # NOT STORED POS NUMBERS
  # Input: destination position, team, division
  # Output: battle group position
  #			average team position if division input NOT set to 0-8
  ("battlegroup_get_position", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),

      (assign, ":x", 0),
      (assign, ":y", 0),
      (init_position, ":bgposition"),
      (try_begin),
        (neg | is_between, ":bgdivision", 0, 9),
        (team_slot_ge, ":bgteam", slot_team_size, 1),
        (team_get_slot, ":x", ":bgteam", slot_team_avg_x),
        (team_get_slot, ":y", ":bgteam", slot_team_avg_y),
        (team_get_slot, ":zrot", ":bgteam", slot_team_avg_zrot),
      (else_try),
        (is_between, ":bgdivision", 0, 9),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_slot_ge, ":bgteam", ":slot", 1),

        (store_add, ":slot", slot_team_d0_avg_x, ":bgdivision"),
        (team_get_slot, ":x", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_y, ":bgdivision"),
        (team_get_slot, ":y", ":bgteam", ":slot"),

        (store_add, ":slot", slot_team_d0_avg_zrot, ":bgdivision"),
        (team_get_slot, ":zrot", ":bgteam", ":slot"),
      (try_end),
      (position_set_x, ":bgposition", ":x"),
      (position_set_y, ":bgposition", ":y"),
      (position_rotate_z, ":bgposition", ":zrot", 0),
      (position_set_z_to_ground_level, ":bgposition"),]),

  # script_battlegroup_get_attack_destination by motomataru
  # Input: destination position, team, division, target team, target division
  # Output: melee position against target battlegroup
  ("battlegroup_get_attack_destination", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":bgteam", 2),
      (store_script_param, ":bgdivision", 3),
      (store_script_param, ":enemy_team", 4),
      (store_script_param, ":enemy_division", 5),

      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (try_begin),
        (le, ":bgformation", formation_none),
        (call_script, "script_battlegroup_get_position", ":bgposition", ":bgteam", ":bgdivision"),
      (else_try),
        (call_script, "script_formation_current_position", ":bgposition", ":bgteam", ":bgdivision"),
      (try_end),

      #distance to enemy center
      (store_add, ":slot", slot_team_d0_formation, ":enemy_division"),
      (team_get_slot, ":enemy_formation", ":enemy_team", ":slot"),
      (call_script, "script_battlegroup_get_position", Enemy_Team_Pos, ":enemy_team", ":enemy_division"),
      (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos),

      (call_script, "script_battlegroup_get_action_radius", ":bgteam", ":bgdivision"),
      (assign, ":bgwidth", reg0),
      (call_script, "script_battlegroup_get_action_radius", ":enemy_team", ":enemy_division"),
      (store_add, ":combined_width", ":bgwidth", reg0),

      (assign, ":min_radius", reg0),
      (val_min, ":min_radius", ":bgwidth"),
      (val_div, ":min_radius", 2),	#function returns length of bg

      (try_begin),
        (gt, ":bgformation", formation_none),	#in formation AND
        (le, ":distance_to_move", ":combined_width"),	#close to enemy
        (store_mul, reg0, -350, formation_reform_interval),	#back up one move (to avoid wild swings / reversals on overruns)
        (position_move_y, ":bgposition", reg0),
        (get_distance_between_positions, ":distance_to_move", ":bgposition", Enemy_Team_Pos),
      (try_end),

      #subtract enemy center to edge-of-contact (determined by minimum half-width
      #between the two battlegroups)
      (call_script, "script_get_distance_to_battlegroup", ":enemy_team", ":enemy_division", ":bgposition"),
      (store_mul, ":angle_adjusted_half_depth", ":min_radius", reg2),	#reg2 is cosine glancing angle, FP
      (convert_from_fixed_point, ":angle_adjusted_half_depth"),
      (try_begin),
        (neq, ":enemy_formation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front", ":enemy_team", ":enemy_division"),
        (val_max, ":angle_adjusted_half_depth", reg0),
      (try_end),
      (val_sub, ":distance_to_move", ":angle_adjusted_half_depth"),

      #modify by bg center to edge-of-contact, if needed
      (call_script, "script_battlegroup_dist_center_to_front", ":bgteam", ":bgdivision"),
      (assign, ":bg_half_depth", reg0),
      (try_begin),
        (le, ":bgformation", formation_none),
        (val_sub, ":distance_to_move", ":bg_half_depth"),	#position from script_battlegroup_get_position is in middle of bg
      (else_try),
        (eq, ":bgformation", formation_wedge),
        (call_script, "script_battlegroup_dist_center_to_front", ":enemy_team", ":enemy_division"),
        (val_add, ":distance_to_move", reg0),	#move in from nearest edge found by script_get_distance_to_battlegroup
        (val_add, ":distance_to_move", ":bg_half_depth"),	#drive wedge through target formation!
      (try_end),

      #modify by speed differential
      (try_begin),
        (gt, ":enemy_formation", formation_none),
        (neq, ":enemy_formation", formation_default),

        (store_add, ":slot", slot_team_d0_first_member, ":enemy_division"),
        (team_get_slot, reg0, ":enemy_team", ":slot"),
        (agent_is_active, reg0),

        (agent_get_speed, Speed_Pos, reg0),
        (init_position, Temp_Pos),
        (get_distance_between_positions, ":enemy_formation_speed", Speed_Pos, Temp_Pos),
        (val_mul, ":enemy_formation_speed", formation_reform_interval),	#calculate distance to next call

        (try_begin),
          (position_is_behind_position, ":bgposition", Enemy_Team_Pos),	#attacking from rear?
          (val_add, ":distance_to_move", ":enemy_formation_speed"),	#catch up to anticipated position
        (else_try),	#attacking enemy formation from front
          (store_add, ":slot", slot_team_d0_is_fighting, ":bgdivision"),
          (team_slot_eq, ":bgteam", ":slot", 0),
          (val_sub, ":distance_to_move", ":enemy_formation_speed"),	#avoid overrunning enemy
        (try_end),
      (try_end),

      (store_add, ":slot", slot_team_d0_front_weapon_length, ":bgdivision"),
      (team_get_slot, ":striking_distance", ":bgteam", ":slot"),
      (val_sub, ":distance_to_move", ":striking_distance"),

      (call_script, "script_point_y_toward_position", ":bgposition", Enemy_Team_Pos),
      (position_move_y, ":bgposition", ":distance_to_move"),]),

  # script_battlegroup_dist_center_to_front by motomataru
  # Input: team, division
  # Output: reg0 distance to front of battlegroup from center in cm
  ("battlegroup_dist_center_to_front", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),

      (try_begin),
        (eq, ":bgformation", formation_none),	#single row
        (assign, ":depth", 0),

        #WFaS multi-ranks
      (else_try),
        (eq, ":bgformation", formation_2_row),
        (assign, ":depth", 100),
      (else_try),
        (eq, ":bgformation", formation_3_row),
        (assign, ":depth", 200),
      (else_try),
        (eq, ":bgformation", formation_4_row),
        (assign, ":depth", 300),
      (else_try),
        (eq, ":bgformation", formation_5_row),
        (assign, ":depth", 400),

      (else_try),	#WB multi-ranks
        (lt, ":spacing", 0),
        (store_mul, ":depth", ":spacing", -1),
        (val_mul, ":depth", 100),

      #Non Native
      (else_try),
        (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
        (team_get_slot, ":size_enemy_battlegroup", ":bgteam", ":slot"),
        (store_mul, ":row_depth", ":spacing", 50),
        (val_add, ":row_depth", formation_minimum_spacing),

        (this_or_next | eq, ":bgformation", formation_ranks),
        (eq, ":bgformation", formation_shield),
        (call_script, "script_calculate_default_ranks", ":size_enemy_battlegroup"),
        (val_sub, reg1, 1),
        (store_mul, ":depth", ":row_depth", reg1),

      (else_try),
        (convert_to_fixed_point, ":size_enemy_battlegroup"),
        (store_sqrt, ":columns", ":size_enemy_battlegroup"),

        (eq, ":bgformation", formation_square),
        (convert_from_fixed_point, ":columns"),
        (val_add, ":columns", 1),	#see script_form_infantry
        (store_div, ":rows", ":size_enemy_battlegroup", ":columns"),
        (store_mul, ":depth", ":row_depth", ":rows"),
        (convert_from_fixed_point, ":depth"),
        (val_sub, ":depth", ":row_depth"),

      (else_try),
        (eq, ":bgformation", formation_wedge),
        (store_mul, ":depth", ":row_depth", ":columns"),	#approximation
        (convert_from_fixed_point, ":depth"),
      (try_end),

      (try_begin),
        (neq, ":bgformation", formation_wedge),
        (store_div, reg0, ":depth", 2),
      (else_try),
        (store_mul, reg0, ":depth", 2),	#another approximation (height - inner radius)
        (val_div, reg0, 3),
      (try_end),]),

  # script_battlegroup_get_action_radius by motomataru
  # Input: team, division
  # Output: reg0 radius of battlegroup's "zone of control" (now length of
  # battlegroup in cm)
  ("battlegroup_get_action_radius", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),

      (store_add, ":slot", slot_team_d0_size, ":bgdivision"),
      (team_get_slot, ":size_battlegroup", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":formation", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_type, ":bgdivision"),
      (team_get_slot, ":div_type", ":bgteam", ":slot"),
      (store_add, ":slot", slot_team_d0_formation_space, ":bgdivision"),
      (team_get_slot, ":spacing", ":bgteam", ":slot"),

      (try_begin),
        (this_or_next | eq, ":div_type", sdt_archer),
        (le, ":formation", formation_none),	#Native formation

        (store_mul, ":troop_space", ":spacing", 75),	#Native minimum spacing not consistent but about this
        (val_add, ":troop_space", 100),	#minimum spacing

        #WFaS multi-ranks
        (try_begin),
          (eq, ":formation", formation_2_row),
          (val_div, ":size_battlegroup", 2),
        (else_try),
          (eq, ":formation", formation_3_row),
          (val_div, ":size_battlegroup", 3),
        (else_try),
          (eq, ":formation", formation_4_row),
          (val_div, ":size_battlegroup", 4),
        (else_try),
          (eq, ":formation", formation_5_row),
          (val_div, ":size_battlegroup", 5),

        (else_try),	#WB multi-ranks
          (lt, ":spacing", 0),
          (assign, ":troop_space", 150),
          (val_mul, ":spacing", -1),
          (val_add, ":spacing", 1),
          (val_div, ":size_battlegroup", ":spacing"),
        (try_end),

        (store_mul, ":formation_width", ":size_battlegroup", ":troop_space"),
        (store_div, reg0, ":formation_width", 2),

      (else_try),
        (eq, ":formation", formation_wedge),
        (call_script, "script_get_centering_amount", formation_square, ":size_battlegroup", ":spacing"),	#approximation
        (val_mul, reg0, 7),
        (val_div, reg0, 6),
      (else_try),
        (try_begin),
          (lt, ":spacing", 0),
          (assign, reg0, ":bgteam"),
          (assign, reg1, ":bgdivision"),
          (assign, reg2, ":formation"),
          (display_message, "@{!}battlegroup_get_action_radius: negative radius for team {reg0} division {reg1} formation {reg2}"),
        (try_end),
        (call_script, "script_get_centering_amount", ":formation", ":size_battlegroup", ":spacing"),
      (try_end),

      (val_mul, reg0, 2),]),

  # script_team_get_position_of_enemies by motomataru
  # Input: destination position, team, troop class/division
  # Output: destination position: average position if reg0 > 0
  #			reg0: number of enemies
  # Run script_store_battlegroup_data before calling!
  ("team_get_position_of_enemies", [
      (store_script_param, ":enemy_position", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":troop_type", 3),
      (assign, ":pos_x", 0),
      (assign, ":pos_y", 0),
      (assign, ":total_size", 0),
      (try_begin),
        (neq, ":troop_type", grc_everyone),
        (assign, ":closest_distance", Far_Away),
        (call_script, "script_battlegroup_get_position", Temp_Pos, ":team_no", grc_everyone),
      (try_end),

      (try_for_range, ":other_team", 0, 4),
        (teams_are_enemies, ":other_team", ":team_no"),
        (try_begin),
          (eq, ":troop_type", grc_everyone),
          (team_get_slot, ":team_size", ":other_team", slot_team_size),
          (try_begin),
            (gt, ":team_size", 0),
            (call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", grc_everyone),
            (position_get_x, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_x", reg0),
            (position_get_y, reg0, ":enemy_position"),
            (val_mul, reg0, ":team_size"),
            (val_add, ":pos_y", reg0),
          (try_end),
        (else_try),	#for multiple divisions, should find the CLOSEST of a given type
          (assign, ":team_size", 0),
          (try_for_range, ":enemy_battle_group", 0, 9),
            (store_add, ":slot", slot_team_d0_size, ":enemy_battle_group"),
            (team_get_slot, ":troop_count", ":other_team", ":slot"),
            (gt, ":troop_count", 0),
            (store_add, ":slot", slot_team_d0_type, ":enemy_battle_group"),
            (team_get_slot, ":bg_type", ":other_team", ":slot"),
            (store_sub, ":bg_root_type", ":bg_type", 3), #subtype is three more than main type
            (this_or_next | eq, ":bg_type", ":troop_type"),
            (eq, ":bg_root_type", ":troop_type"),
            (val_add, ":team_size", ":troop_count"),
            (call_script, "script_battlegroup_get_position", ":enemy_position", ":other_team", ":enemy_battle_group"),
            (get_distance_between_positions, reg0, Temp_Pos, ":enemy_position"),
            (lt, reg0, ":closest_distance"),
            (assign, ":closest_distance", reg0),
            (position_get_x, ":pos_x", ":enemy_position"),
            (position_get_y, ":pos_y", ":enemy_position"),
          (try_end),
        (try_end),
        (val_add, ":total_size", ":team_size"),
      (try_end),

      (try_begin),
        (eq, ":total_size", 0),
        (init_position, ":enemy_position"),
      (else_try),
        (eq, ":troop_type", grc_everyone),
        (val_div, ":pos_x", ":total_size"),
        (position_set_x, ":enemy_position", ":pos_x"),
        (val_div, ":pos_y", ":total_size"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (else_try),
        (position_set_x, ":enemy_position", ":pos_x"),
        (position_set_y, ":enemy_position", ":pos_y"),
        (position_set_z_to_ground_level, ":enemy_position"),
      (try_end),

      (assign, reg0, ":total_size"),]),

  # script_get_distance_to_battlegroup by motomataru
  # Gets distance from "from position" to the theoretical nearest side of the
  # battlegroup, accounting for rotation of battlegroup
  # Input: bg team, bg division, from position
  # Output: reg2 abs (cos (BG direction - 90 - direction from "from position"))
  # fixed point
  #         reg1 BG radius x reg2 in cms
  #         reg0 distance in cms between BG position and "from position" minus
  #         reg1 (could be negative)
  # Uses pos0, pos61
  ("get_distance_to_battlegroup", [
      (store_script_param, ":bgteam", 1),
      (store_script_param, ":bgdivision", 2),
      (store_script_param, ":from_pos", 3),

      (store_add, ":slot", slot_team_d0_formation, ":bgdivision"),
      (team_get_slot, ":bgformation", ":bgteam", ":slot"),
      (call_script, "script_battlegroup_get_action_radius", ":bgteam", ":bgdivision"),
      (store_div, ":radius", reg0, 2),	#function returns length of bg
      (assign, ":min_cos_theta", 1),
      (convert_to_fixed_point, ":min_cos_theta"),
      (try_begin),
        (eq, ":bgformation", formation_wedge),
        (val_mul, ":min_cos_theta", 58),	#relation inscribed circle radius to half side: 1 / sqrt 3
        (val_div, ":min_cos_theta", 100),
      (else_try),
        (gt, ":radius", 0),
        (call_script, "script_battlegroup_dist_center_to_front", ":bgteam", ":bgdivision"),
        (val_mul, ":min_cos_theta", reg0),
        (val_div, ":min_cos_theta", ":radius"),
      (else_try),
        (assign, ":min_cos_theta", 0),
      (try_end),

      #acquire rotations
      (call_script, "script_battlegroup_get_position", pos0, ":bgteam", ":bgdivision"),
      (try_begin),
        (gt, ":bgformation", formation_none),
        (neq, ":bgformation", formation_default),
        (call_script, "script_get_formation_destination", pos61, ":bgteam", ":bgdivision"),
        (position_copy_rotation, pos0, pos61),
      (try_end),

      (copy_position, pos61, ":from_pos"),
      (call_script, "script_point_y_toward_position", pos61, pos0),
      (assign, ":distance_to_battlegroup", reg0),

      #calculate difference from center of bg
      (get_angle_between_positions, ":theta", pos61, pos0),
      (val_sub, ":theta", 9000),
      (store_cos, ":cos_theta", ":theta"),
      (val_abs, ":cos_theta"),
      (val_max, ":cos_theta", ":min_cos_theta"),	#doing depth considerations this way allows calling func to use angle; it also
      #avoids Pythagorean calcs

      (store_mul, reg1, ":radius", ":cos_theta"),
      (convert_from_fixed_point, reg1),
      (val_sub, ":distance_to_battlegroup", reg1),
      (assign, reg0, ":distance_to_battlegroup"),
      (assign, reg2, ":cos_theta"),]),

  # script_get_item_modifier_effects
  # Input: itp_*, imod_*
  # Output: reg0 damage effect
  #         reg1 speed effect
  #         reg2 armor effect
  #         reg3 hit points effect
  #         reg4 difficulty effect
  #         reg5 price factor
  #         s0 descriptor string
  # derived from autoloot by Rubik
  ("get_item_modifier_effects", [(store_script_param, ":type", 1),
      (store_script_param, ":imod", 2),

      (assign, ":damage", 0),
      (assign, ":speed", 0),
      (assign, ":armor", 0),
      (assign, ":hit_points", 0),
      (assign, ":difficulty", 0),
      (assign, ":price_factor", 100),

      (try_begin),
        (eq, ":type", itp_type_horse),
        (try_begin),
          (eq, ":imod", imod_lame),
          (assign, ":speed", -10),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Lame"),
        (else_try),
          (eq, ":imod", imod_swaybacked),
          (assign, ":speed", -4),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Swaybacked"),
        (else_try),
          (eq, ":imod", imod_timid),
          (assign, ":speed", 2),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Timid"),
        (else_try),
          (eq, ":imod", imod_meek),
          (assign, ":speed", 2),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Meek"),
        (else_try),
          (eq, ":imod", imod_stubborn),
          (assign, ":hit_points", 5),
          (assign, ":difficulty", 1),
          (assign, ":price_factor", 90),
          (str_store_string, s0, "@Stubborn"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 4),
          (assign, ":armor", 3),
          (assign, ":hit_points", 10),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_spirited),
          (assign, ":damage", 1),
          (assign, ":speed", 2),
          (assign, ":price_factor", 160),
          (str_store_string, s0, "@Spirited"),
        (else_try),
          (eq, ":imod", imod_champion),
          (assign, ":damage", 2),
          (assign, ":speed", 4),
          (assign, ":difficulty", 2),
          (assign, ":price_factor", 170),
          (str_store_string, s0, "@Champion"),
        (try_end),

      (else_try),
        (eq, ":type", itp_type_shield),
        (try_begin),
          (eq, ":imod", imod_cracked),
          (assign, ":armor", -4),
          (assign, ":hit_points", -56),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":armor", -2),
          (assign, ":hit_points", -26),
          (assign, ":price_factor", 75),
          (str_store_string, s0, "@Battered"),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":armor", 2),
          (assign, ":hit_points", 47),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Thick"),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":armor", 4),
          (assign, ":hit_points", 63),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Reinforced"),
        (try_end),

      (else_try),
        (ge, ":type", itp_type_head_armor),
        (le, ":type", itp_type_hand_armor),
        (try_begin),
          (eq, ":imod", imod_cracked),
          (assign, ":armor", -4),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":armor", -3),
          (assign, ":price_factor", 55),
          (str_store_string, s0, "@Rusty"),
        (else_try),
          (eq, ":imod", imod_tattered),
          (assign, ":armor", -3),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Tattered"),
        (else_try),
          (eq, ":imod", imod_ragged),
          (assign, ":armor", -2),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Ragged"),
        (else_try),
          (eq, ":imod", imod_battered),
          (assign, ":armor", -2),
          (assign, ":price_factor", 75),
          (str_store_string, s0, "@Battered"),
        (else_try),
          (eq, ":imod", imod_crude),
          (assign, ":armor", -1),
          (assign, ":price_factor", 83),
          (str_store_string, s0, "@Crude"),
        (else_try),
          (eq, ":imod", imod_sturdy),
          (assign, ":armor", 1),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Sturdy"),
        (else_try),
          (eq, ":imod", imod_thick),
          (assign, ":armor", 2),
          (assign, ":price_factor", 140),
          (str_store_string, s0, "@Thick"),
        (else_try),
          (eq, ":imod", imod_hardened),
          (assign, ":armor", 3),
          (assign, ":price_factor", 160),
          (str_store_string, s0, "@Hardened"),
        (else_try),
          (eq, ":imod", imod_reinforced),
          (assign, ":armor", 4),
          (assign, ":price_factor", 180),
          (str_store_string, s0, "@Reinforced"),
        (else_try),
          (eq, ":imod", imod_lordly),
          (assign, ":armor", 5),
          (assign, ":price_factor", 400),
          (str_store_string, s0, "@Lordly"),
        (try_end),

      (else_try),
        (this_or_next | eq, ":type", itp_type_one_handed_wpn),
        (this_or_next | eq, ":type", itp_type_two_handed_wpn),
        (this_or_next | eq, ":type", itp_type_polearm),
        (this_or_next | eq, ":type", itp_type_bow),
        (this_or_next | eq, ":type", itp_type_crossbow),
        (this_or_next | eq, ":type", itp_type_pistol),
        (eq, ":type", itp_type_musket),

        (try_begin),
          (eq, ":imod", imod_rotten),		#idea is to use this for a completly broken weapon
          (assign, ":damage", -20),
          (assign, ":price_factor", 5),
          (str_store_string, s0, "@Broken"),
        (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":damage", -5),
          (assign, ":price_factor", 40),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_rusty),
          (assign, ":damage", -3),
          (assign, ":price_factor", 55),
          (str_store_string, s0, "@Rusty"),
        (else_try),
          (eq, ":imod", imod_bent),
          (assign, ":damage", -3),
          (assign, ":speed", -3),
          (assign, ":price_factor", 60),
          (str_store_string, s0, "@Bent"),
        (else_try),
          (eq, ":imod", imod_chipped),
          (assign, ":damage", -1),
          (assign, ":price_factor", 72),
          (str_store_string, s0, "@Chipped"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 2),
          (assign, ":speed", -2),
          (assign, ":difficulty", 1),
          (assign, ":price_factor", 120),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_strong),
          (assign, ":damage", 3),
          (assign, ":speed", -3),
          (assign, ":difficulty", 2),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Strong"),
        (else_try),
          (eq, ":imod", imod_balanced),
          (assign, ":damage", 3),
          (assign, ":speed", 3),
          (assign, ":price_factor", 165),
          (str_store_string, s0, "@Balanced"),
        (else_try),
          (eq, ":imod", imod_tempered),
          (assign, ":damage", 4),
          (assign, ":price_factor", 180),
          (str_store_string, s0, "@Tempered"),
        (else_try),
          (eq, ":imod", imod_masterwork),
          (assign, ":damage", 5),
          (assign, ":speed", 1),
          (assign, ":difficulty", 4),
          (assign, ":price_factor", 400),
          (str_store_string, s0, "@Masterwork"),
        (else_try),
          (eq, ":imod", imod_crude),
          (assign, ":damage", -2),
          (assign, ":price_factor", 83),
        (try_end),

      (else_try),
        (this_or_next | eq, ":type", itp_type_arrows),
        (this_or_next | eq, ":type", itp_type_bolts),
        (this_or_next | eq, ":type", itp_type_bullets),
        (eq, ":type", itp_type_thrown),

        (try_begin),
          (eq, ":imod", imod_large_bag),
          #       (assign, ":damage", 1), #just make better than plain
          (assign, ":price_factor", 110),
          (str_store_string, s0, "@Large Bag of"),
        (else_try),
          (eq, ":imod", imod_bent),
          (assign, ":damage", -3),
          (assign, ":price_factor", 65),
          (str_store_string, s0, "@Bent"),
        (else_try),
          (eq, ":imod", imod_cracked),
          (assign, ":damage", -5),
          (assign, ":price_factor", 50),
          (str_store_string, s0, "@Cracked"),
        (else_try),
          (eq, ":imod", imod_heavy),
          (assign, ":damage", 2),
          (assign, ":price_factor", 130),
          (str_store_string, s0, "@Heavy"),
        (else_try),
          (eq, ":imod", imod_balanced),
          (assign, ":damage", 3),
          (assign, ":price_factor", 150),
          (str_store_string, s0, "@Balanced"),
        (try_end),
      (try_end),

      (assign, reg0, ":damage"),
      (assign, reg1, ":speed"),
      (assign, reg2, ":armor"),
      (assign, reg3, ":hit_points"),
      (assign, reg4, ":difficulty"),
      (assign, reg5, ":price_factor"),]),

  # script_evaluate_item moto chief
  # Input: item_id, item_mod
  # Output: reg0 value meant to compare items of a given type
  ("evaluate_item", [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":item_mod", 2),

      (assign, ":ret_val", 0),
      (try_begin),
        (gt, ":item_id", "itm_no_item"),

        (item_get_type, ":item_type", ":item_id"),
        (call_script, "script_get_item_modifier_effects", ":item_type", ":item_mod"),
        (assign, ":damage", reg0),
        (assign, ":speed", reg1),
        (assign, ":armor", reg2),
        (assign, ":hit_points", reg3),

        #Armor
        (try_begin),
          (ge, ":item_type", itp_type_head_armor),
          (le, ":item_type", itp_type_hand_armor),

          #construct comparison value
          (item_get_head_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_leg_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),

          #Ranged Weapons
        (else_try),
          (call_script, "script_cf_is_weapon_ranged", ":item_id", 1),

          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (val_add, ":damage", ":value"),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),

          (item_get_missile_speed,  ":value", ":item_id"),
          (val_mul, ":damage", ":value"),

          (item_get_accuracy, ":value", ":item_id"),
          (val_mul, ":damage", ":value"),
          (assign, ":ret_val", ":damage"),

          #Melee Weapons
        (else_try),
          (ge, ":item_type", itp_type_one_handed_wpn),
          (le, ":item_type", itp_type_polearm),

          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (item_get_swing_damage, reg2, ":item_id"),
          (val_max, ":value", reg2),  #TW formula.  Also avoids problems with script_switch_to_noswing_weapons
          (val_add, ":damage", ":value"),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),

          (item_get_weapon_length, ":value", ":item_id"),
          (convert_to_fixed_point, ":value"),
          (store_sqrt, reg2, ":value"),
          (convert_from_fixed_point, reg2),
          (val_mul, ":damage", reg2),
          (assign, ":ret_val", ":damage"),

          #Shields
        (else_try),
          (eq, ":item_type", itp_type_shield),

          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),

          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_div, ":value", 17),  #attempt to make it comparable to armors
          (val_add, ":armor", ":value"),

          #shields' protection modified by size, speed
          (item_get_weapon_length, ":value", ":item_id"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Thorax_Length),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Fast_Weapon_Speed),

          (val_mul, ":armor", 3), #fudge factor
          (assign, ":ret_val", ":armor"),

          #Horses
        (else_try),
          (eq, ":item_type", itp_type_horse),

          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (val_mul, ":armor", 4), #figure it takes 3-4 hits to kill a horse, so this is the hit value of each
          #point of armor

          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_add, ":armor", ":value"),

          (item_get_horse_speed, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),

          #Missiles
        (else_try),
          (this_or_next | eq, ":item_type", itp_type_arrows),
          (this_or_next | eq, ":item_type", itp_type_bolts),
          (eq, ":item_type", itp_type_bullets),
        (try_end),
      (try_end),

      (assign, reg0, ":ret_val"),]),

  ("init_noswing_weapons", make_noswing_weapons(items)),

# # M&B Standard AI with changes for formations #CABA - OK; Need expansion when new AI divisions to work with
  # script_calculate_decision_numbers by motomataru
  # Input: AI team, size relative to battle in %
  # Output: reg0 - battle presence plus level bump, reg1 - level bump (team avg
  # level / 3)
  ("calculate_decision_numbers", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_presence", 2),
      (try_begin),
        (team_get_slot, reg0, ":team_no", slot_team_level),
        (store_div, reg1, reg0, 3),
        (store_add, reg0, ":battle_presence", reg1),	#decision w.r.t.  all enemy teams
      (try_end)]),


  # script_team_field_ranged_tactics by motomataru
  # Input: AI team, size relative to largest team in %, size relative to battle
  # in %
  # Output: none
  ("team_field_ranged_tactics", [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (assign, ":division", grc_archers), #Pre-Many Divisions
      (assign, ":bg_pos", Archers_Pos), #Pre-Many Divisions

      (try_begin),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_eq, ":team_no", ":slot", 0),
        (try_begin),	#undo reversion to BP_Jockey (see below)
          (lt, "$battle_phase", BP_Fight),
          (call_script, "script_cf_any_fighting"),
          (call_script, "script_cf_count_casualties"),
          (assign, "$battle_phase", BP_Fight),
        (try_end),

      (else_try),
        (call_script, "script_battlegroup_get_position", ":bg_pos", ":team_no", ":division"),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),
        (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),

        (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, ":division"),	#distance to nearest enemy infantry agent
        (team_get_slot, ":distance_to_enemy", ":team_no", ":slot"),
        (try_begin),
          (eq, ":distance_to_enemy", 0),
          (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
          (assign, ":distance_to_enemy", reg0),
        (try_end),

        (try_begin),	#avoid being provoked from defensive position
          (ge, "$battle_phase", BP_Fight),
          (try_begin),
            (call_script, "script_cf_any_fighting"),
          (else_try),
            (assign, "$battle_phase", BP_Jockey),
            (assign, "$clock_reset", 0),
          (try_end),
        (try_end),

        (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
        (team_get_slot, ":is_firing", ":team_no", ":slot"),
        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),

        (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),
        (assign, ":decision_index", reg0),
        (assign, ":level_bump", reg1),

        (try_begin),
          (gt, ":decision_index", 86),	#outpower enemies more than 6:1?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (lt, ":decision_index", 14),	#outpowered more than 6:1?
          (eq, ":num_infantry", 0),	#no infantry to delay enemy?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_retreat),
            (team_give_order, ":team_no", ":division", mordr_retreat),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Jockey),
          (store_add, ":slot", slot_team_d0_low_ammo, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),	#running out of ammo?
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),

        (else_try),
          (ge, "$battle_phase", BP_Fight),
          (eq, ":is_firing", 0),
          (gt, ":decision_index", Advance_More_Point),
          (le, ":distance_to_enemy", AI_long_range),	#closer than reposition?
          (team_give_order, ":team_no", ":division", mordr_advance),

        #hold somewhere
        (else_try),
          (store_add, ":decision_index", ":rel_army_size", ":level_bump"),	#decision w.r.t. largest enemy team
          (assign, ":move_archers", 0),

          (init_position, Team_Starting_Point),
          (team_get_slot, reg0, ":team_no", slot_team_starting_x),
          (position_set_x, Team_Starting_Point, reg0),
          (team_get_slot, reg0, ":team_no", slot_team_starting_y),
          (position_set_y, Team_Starting_Point, reg0),
          (position_set_z_to_ground_level, Team_Starting_Point),

          (try_begin),
            (eq, "$battle_phase", BP_Setup),
            (assign, ":move_archers", 1),
          (else_try),
            (ge, "$battle_phase", BP_Fight),
            (try_begin),
              (neg | is_between, ":distance_to_enemy", AI_charge_distance, AI_long_range),
              (assign, ":move_archers", 1),
            (else_try),
              (lt, ":decision_index", Hold_Point),	#probably coming from a defensive position (see below)
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (eq, ":is_firing", 0),	#probably because player team has retreated
              (assign, ":move_archers", 1),
            (try_end),
          (else_try),	#jockey phase
            (this_or_next | gt, "$FormAI_AI_no_defense", 0),	#player has set disallow defense option OR
            (ge, ":decision_index", Hold_Point),	#not starting in a defensive position (see below)
            (try_begin),
              (gt, ":distance_to_enemy", AI_long_range),	#enemy very far off
              (assign, ":move_archers", 1),
            (else_try),
              (call_script, "script_point_y_toward_position", Team_Starting_Point, ":bg_pos"),
              (position_get_rotation_around_z, reg0, Team_Starting_Point),
              (position_get_rotation_around_z, reg1, ":bg_pos"),
              (val_sub, reg0, reg1),
              (this_or_next | is_between, reg0, -45, 45),	#only move if within "cone of advancement" to prevent constant adjusting at
              #border OR
              (eq, ":is_firing", 0),	#if not firing for some reason (hill in way?)

              (try_begin),
                (eq, ":num_infantry", 0),	#no infantry to wait for
                (assign, ":move_archers", 1),
              (else_try),
                (call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
                (get_distance_between_positions, ":infantry_to_enemy", Infantry_Pos, Enemy_Team_Pos),
                (get_distance_between_positions, ":archers_to_enemy", ":bg_pos", Enemy_Team_Pos),
                (val_sub, ":infantry_to_enemy", ":archers_to_enemy"),
                (le, ":infantry_to_enemy", 1500),	#don't outstrip infantry when closing
                (assign, ":move_archers", 1),
              (try_end),
            (try_end),
          (try_end),

          (try_begin),
            (gt, ":move_archers", 0),
            (try_begin),
              (lt, ":decision_index", Hold_Point),	#outnumbered?
              (eq, "$FormAI_AI_no_defense", 0),	#player hasn't set disallow defense option?
              (lt, "$battle_phase", BP_Fight),
              (neq, ":team_no", 1),	#not attacker?
              (neq, ":team_no", 3),	#not ally of attacker?
              (store_div, ":distance_to_move", ":distance_to_enemy", 6),	#middle of rear third of battlefield
              (assign, ":hill_search_radius", ":distance_to_move"),

            (else_try),
              (try_begin),
                (ge, "$battle_phase", BP_Fight),
                (copy_position, ":bg_pos", Team_Starting_Point),
                (call_script, "script_point_y_toward_position", ":bg_pos", Enemy_Team_Pos),
                (try_begin),
                  (gt, ":num_infantry", 0),
                  (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
                  (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
                  (le, ":enemy_agent_nearest_infantry", 0),
                  (agent_get_team, ":target_team", ":enemy_agent_nearest_infantry"),
                  (agent_get_division, ":target_division", ":enemy_agent_nearest_infantry"),
                  (call_script, "script_battlegroup_get_position", Nearest_Enemy_Battlegroup_Pos, ":target_team", ":target_division"),
                  (get_distance_between_positions, ":distance_to_enemy", ":bg_pos", Nearest_Enemy_Battlegroup_Pos),
                (else_try),
                  (call_script, "script_get_nearest_enemy_battlegroup_location", Nearest_Enemy_Battlegroup_Pos, ":team_no", ":bg_pos"),
                  (assign, ":distance_to_enemy", reg0),
                (try_end),
              (try_end),

              (try_begin),
                (eq, "$battle_phase", BP_Setup),
                (assign, ":shot_distance", AI_long_range),
              (else_try),
                (assign, ":shot_distance", AI_firing_distance),
                (store_sub, reg1, AI_firing_distance, AI_charge_distance),
                (val_sub, reg1, 200),	#subtract two meters to prevent automatically provoking melee from forward
                #enemy infantry
                (store_add, ":slot", slot_team_d0_percent_throwers, ":division"),
                (team_get_slot, reg0, ":team_no", ":slot"),
                (val_mul, reg1, reg0),
                (val_div, reg1, 100),
                (val_sub, ":shot_distance", reg1),
              (try_end),

              (store_sub, ":distance_to_move", ":distance_to_enemy", ":shot_distance"),
              (store_div, ":hill_search_radius", ":shot_distance", 3),	#limit so as not to run into enemy
              (try_begin),
                (lt, "$battle_phase", BP_Fight),
                (try_begin),
                  (this_or_next | eq, "$battle_phase", BP_Setup),
                  (lt, ":battle_presence", Advance_More_Point),	#expect to meet halfway?
                  (val_div, ":distance_to_move", 2),
                (try_end),
              (try_end),
            (try_end),

            (position_move_y, ":bg_pos", ":distance_to_move", 0),
            (try_begin),
              (lt, "$battle_phase", BP_Fight),
              (copy_position, pos1, ":bg_pos"),
              (store_div, reg0, ":hill_search_radius", 100),
              (call_script, "script_find_high_ground_around_pos1_corrected", ":bg_pos", reg0),
            (try_end),
          (try_end),

          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_hold),
            (team_give_order, ":team_no", ":division", mordr_hold),
          (try_end),
          (call_script, "script_set_formation_destination", ":team_no", ":division", ":bg_pos"),
        (try_end),
      (try_end)]),


  # script_team_field_melee_tactics by motomataru #EDITED FOR SLOTS BY
  # CABA...many divisions changes necessary
  # Input: AI team, size relative to largest team in %, size relative to battle
  # in %
  # Output: none
  ("team_field_melee_tactics", [
      (store_script_param, ":team_no", 1),
      #	(store_script_param, ":rel_army_size", 2),
      (store_script_param, ":battle_presence", 3),
      (call_script, "script_calculate_decision_numbers", ":team_no", ":battle_presence"),

      #mop up if outnumber enemies more than 6:1
      (try_begin),
        (gt, reg0, 86),
        (try_for_range, ":division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":division"),
          (team_slot_ge, ":team_no", ":slot", 1),
          (store_add, ":slot", slot_team_d0_type, ":division"),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_archer),
          (neg | team_slot_eq, ":team_no", ":slot", sdt_skirmisher),
          (call_script, "script_formation_end", ":team_no", ":division"),
          (team_get_movement_order, reg0, ":team_no", ":division"),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":team_no", ":division", mordr_charge),
          (try_end),
        (try_end),

      (else_try),
        (assign, ":num_enemies", 0),
        (try_for_range, ":enemy_team_no", 0, 4),
          (teams_are_enemies, ":enemy_team_no", ":team_no"),
          (team_get_slot, ":value", ":enemy_team_no", slot_team_size),
          (val_add, ":num_enemies", ":value"),
        (try_end),

        (gt, ":num_enemies", 0),
        (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, ":team_no", grc_everyone),

        (store_add, ":slot", slot_team_d0_size, grc_archers),
        (team_get_slot, ":num_archers", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_archers", 0),
          (assign, ":enemy_bg_nearest_archers_dist", Far_Away),
          (assign, ":archer_order", mordr_charge),
        (else_try),
          (call_script, "script_battlegroup_get_position", Archers_Pos, ":team_no", grc_archers),
          (call_script, "script_point_y_toward_position", Archers_Pos, Enemy_Team_Pos),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Archers_Pos),
          (assign, ":enemy_bg_nearest_archers_dist", reg0),
          (team_get_movement_order, ":archer_order", ":team_no", grc_archers),
        (try_end),

        (store_add, ":slot", slot_team_d0_size, grc_infantry),
        (team_get_slot, ":num_infantry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_infantry", 0),
          (assign, ":enemy_bg_nearest_infantry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_infantry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position", Infantry_Pos, ":team_no", grc_infantry),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Infantry_Pos),
          (assign, ":enemy_bg_nearest_infantry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_infantry),
          (team_get_slot, ":enemy_agent_nearest_infantry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_infantry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_infantry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),

        (store_add, ":slot", slot_team_d0_size, grc_cavalry),
        (team_get_slot, ":num_cavalry", ":team_no", ":slot"),
        (try_begin),
          (eq, ":num_cavalry", 0),
          (assign, ":enemy_bg_nearest_cavalry_dist", Far_Away),
          (assign, ":enemy_agent_nearest_cavalry_dist", Far_Away),
        (else_try),
          (call_script, "script_battlegroup_get_position", Cavalry_Pos, ":team_no", grc_cavalry),
          (call_script, "script_get_nearest_enemy_battlegroup_location", pos0, ":team_no", Cavalry_Pos),
          (assign, ":enemy_bg_nearest_cavalry_dist", reg0),
          (store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_cavalry),
          (team_get_slot, ":enemy_agent_nearest_cavalry_dist", ":team_no", ":slot"),
          (eq, ":enemy_agent_nearest_cavalry_dist", 0),	#happens when player turns off closest agent mechanism (see mod options)
          (assign, ":enemy_agent_nearest_cavalry_dist", ":enemy_bg_nearest_infantry_dist"),
        (try_end),

        (try_begin),
          (lt, "$battle_phase", BP_Fight),
          (this_or_next | le, ":enemy_bg_nearest_infantry_dist", AI_charge_distance),
          (this_or_next | le, ":enemy_bg_nearest_cavalry_dist", AI_charge_distance),
          (le, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
          (assign, "$battle_phase", BP_Fight),
        (else_try),
          (lt, "$battle_phase", BP_Jockey),
          (this_or_next | le, ":enemy_agent_nearest_infantry_dist", AI_long_range),
          (le, ":enemy_agent_nearest_cavalry_dist", AI_long_range),
          (assign, "$battle_phase", BP_Jockey),
        (try_end),

        (team_get_leader, ":team_leader", ":team_no"),
        (assign, ":place_leader_by_infantry", 0),

        #infantry AI
        (store_add, ":slot", slot_team_d0_closest_enemy, grc_infantry),
        (team_get_slot, ":enemy_agent_nearest_infantry", ":team_no", ":slot"),
        (try_begin),
          (this_or_next | le, ":num_infantry", 0),
          (le, ":enemy_agent_nearest_infantry", 0),
          (assign, ":infantry_order", ":archer_order"),

          #deal with mounted heroes that team_give_order() treats as infantry
          ##CABA...could change their division?
          (team_get_movement_order, reg0, ":team_no", grc_infantry),
          (try_begin),
            (neq, reg0, ":infantry_order"),
            (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
          (try_end),
          (try_begin),
            (gt, ":num_archers", 0),
            (copy_position, pos1, Archers_Pos),
            (position_move_y, pos1, 1000, 0),
            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, pos1),
          (else_try),
            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, Cavalry_Pos),
          (try_end),

        (else_try),
          (agent_get_position, Nearest_Enemy_Troop_Pos, ":enemy_agent_nearest_infantry"),
          (agent_get_team, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry"),
          (agent_get_division, ":enemy_agent_nearest_infantry_div", ":enemy_agent_nearest_infantry"),

          (assign, ":sum_level_enemy_infantry", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_type, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (this_or_next | eq, ":value", sdt_polearm),
              (eq, ":value", sdt_infantry),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":value", ":enemy_team_no", ":slot"),
              (store_add, ":slot", slot_team_d0_level, ":enemy_division"),
              (team_get_slot, reg0, ":enemy_team_no", ":slot"),
              (val_mul, ":value", reg0),
              (val_add, ":sum_level_enemy_infantry", ":value"),
            (try_end),
          (try_end),

          (store_mul, ":percent_level_enemy_infantry", ":sum_level_enemy_infantry", 100),
          (val_div, ":percent_level_enemy_infantry", ":num_enemies"),
          (try_begin),
            (teams_are_enemies, ":team_no", "$fplayer_team_no"),
            (assign, ":combined_level", 0),
            (assign, ":combined_team_size", 0),
            (assign, ":combined_num_infantry", ":num_infantry"),
          (else_try),
            (store_add, ":slot", slot_team_d0_level, grc_infantry),
            (team_get_slot, ":combined_level", "$fplayer_team_no", ":slot"),
            (team_get_slot, ":combined_team_size", "$fplayer_team_no", slot_team_size),
            (store_add, ":slot", slot_team_d0_size, grc_infantry),
            (team_get_slot, ":combined_num_infantry", "$fplayer_team_no", ":slot"),
            (val_add, ":combined_num_infantry", ":num_infantry"),
          (try_end),
          (store_mul, ":percent_level_infantry", ":combined_num_infantry", 100),
          (store_add, ":slot", slot_team_d0_level, grc_infantry),
          (team_get_slot, ":level_infantry", ":team_no", ":slot"),
          (val_add, ":combined_level", ":level_infantry"),
          (val_mul, ":percent_level_infantry", ":combined_level"),
          (team_get_slot, reg0, ":team_no", slot_team_size),
          (val_add, ":combined_team_size", reg0),
          (val_div, ":percent_level_infantry", ":combined_team_size"),

          (assign, ":infantry_order", mordr_charge),
          (try_begin),	#enemy far away AND ranged not charging
            (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),
            (gt, ":enemy_agent_nearest_infantry_dist", AI_charge_distance),
            (neq, ":archer_order", mordr_charge),
            (try_begin),	#fighting not started OR not enough infantry
              (this_or_next | le, "$battle_phase", BP_Jockey),
              (lt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
              (assign, ":infantry_order", mordr_hold),
            (try_end),
          (try_end),

          # bum rush enemy archers?
          (try_begin),
            # (le, ":level_infantry", AI_Poor_Troop_Level), unfortunately leaves them
            # susceptible to rings of archers
            (store_add, ":slot", slot_team_d0_type, ":enemy_agent_nearest_infantry_div"),
            (this_or_next | team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_archer),
            (team_slot_eq, ":enemy_agent_nearest_infantry_team", ":enemy_agent_nearest_infantry_div", sdt_skirmisher),
            (get_distance_between_positions, reg0, Infantry_Pos, Nearest_Enemy_Troop_Pos),
            (le, reg0, AI_charge_distance),
            (call_script, "script_formation_end", ":team_no", grc_infantry),
            (team_get_movement_order, reg0, ":team_no", grc_infantry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_infantry, mordr_charge),
            (try_end),

          #else attempt to make formation somewhere
          (else_try),
            (store_add, ":slot", slot_team_d0_formation, grc_infantry),
            (team_get_slot, ":infantry_formation", ":team_no", ":slot"),
            (team_get_leader, ":enemy_leader", ":enemy_agent_nearest_infantry_team"),

            #consider new formation
            (try_begin),
              (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
              (this_or_next | le, ":infantry_formation", formation_none),
              (this_or_next | eq, ":infantry_formation", formation_default),
              (team_slot_eq, ":team_no", ":slot", 0),

              (call_script, "script_get_default_formation", ":team_no"),
              (assign, ":infantry_formation", reg0),
              (agent_get_class, ":enemy_nearest_troop_class", ":enemy_agent_nearest_infantry"),

              (assign, ":num_enemy_cavalry", 0),
              (try_for_range, ":enemy_team_no", 0, 4),
                (teams_are_enemies, ":enemy_team_no", ":team_no"),
                (team_get_slot, ":value", ":enemy_team_no", slot_team_num_cavalry),
                (val_add, ":num_enemy_cavalry", ":value"),
              (try_end),

              (store_mul, ":percent_enemy_cavalry", ":num_enemy_cavalry", 100),
              (val_div, ":percent_enemy_cavalry", ":num_enemies"),
              (try_begin),
                (gt, ":infantry_formation", formation_none),
                (try_begin),
                  (gt, ":percent_enemy_cavalry", 66),
                  (assign, ":infantry_formation", formation_square),
                (else_try),
                  (neq, ":enemy_nearest_troop_class", grc_cavalry),
                  (neq, ":enemy_nearest_troop_class", grc_archers),
                  (neq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (ge, ":num_infantry", 21),
                  (store_add, ":slot", slot_team_d0_size, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, reg0, ":num_infantry"),	#got fewer troops?
                  (store_add, ":slot", slot_team_d0_armor, grc_infantry),
                  (team_get_slot, ":average_armor", ":team_no", ":slot"),
                  (store_add, ":slot", slot_team_d0_armor, ":enemy_agent_nearest_infantry_div"),
                  (team_get_slot, reg0, ":enemy_agent_nearest_infantry_team", ":slot"),
                  (gt, ":average_armor", reg0),	#got better armor?
                  (assign, ":infantry_formation", formation_wedge),
                (try_end),
              (try_end),
            (try_end),	#consider new formation

            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_infantry, ":infantry_formation"),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":infantry_formation"),

              #adjust spacing for long swung weapons
              (store_add, ":slot", slot_team_d0_swung_weapon_length, grc_infantry),
              (team_get_slot, ":spacing", ":team_no", ":slot"),
              (val_add, ":spacing", 25),	#rounding for 50cm
              (val_div, ":spacing", 50),
              (store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
              (team_set_slot, ":team_no", ":slot", ":spacing"),

              (assign, ":place_leader_by_infantry", 1),

            (else_try),
              (call_script, "script_formation_end", ":team_no", grc_infantry),
              (team_get_movement_order, reg0, ":team_no", grc_infantry),
              (try_begin),
                (neq, reg0, ":infantry_order"),
                (team_give_order, ":team_no", grc_infantry, ":infantry_order"),
              (try_end),
              (eq, ":infantry_order", mordr_hold),
              (assign, ":place_leader_by_infantry", 1),
            (try_end),

            #hold near archers?
            (try_begin),
              (eq, ":infantry_order", mordr_hold),
              (gt, ":num_archers", 0),
              # (copy_position, pos1, Archers_Pos),
              (team_get_order_position, pos1, ":team_no", grc_archers),	#anticipate archers
              (position_move_x, pos1, -100, 0),
              (try_begin),
                (this_or_next | eq, ":enemy_agent_nearest_infantry_div", grc_cavalry),
                (gt, ":percent_level_infantry", ":percent_level_enemy_infantry"),
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),	#make sure to clear archers
                (store_mul, ":distance_to_move", reg0, 2),
                (val_add, ":distance_to_move", 1000),
                (position_move_y, pos1, ":distance_to_move", 0),	#move ahead of archers in anticipation of charges
              (else_try),
                (position_move_y, pos1, -1000, 0),
              (try_end),

            #obtain destination
            (else_try),
              (assign, ":target_division", -1),
              (try_begin),
                (store_add, ":slot", slot_team_d0_is_fighting, grc_infantry),
                (team_slot_eq, ":team_no", ":slot", 0),	#not engaged?
                (gt, ":enemy_bg_nearest_archers_dist", AI_charge_distance),	#don't have to protect archers?
                # (lt, ":percent_enemy_cavalry", 100), #non-cavalry exist?  MOTO next
                # command tests

                #prefer non-cavalry target (that infantry can catch)
                (store_add, ":slot", slot_team_d0_closest_enemy_special_dist, grc_infantry),
                (team_get_slot, ":distance_to_enemy_troop", ":team_no", ":slot"),
                (gt, ":distance_to_enemy_troop", 0),
                (store_add, ":slot", slot_team_d0_closest_enemy_special, grc_infantry),
                (team_get_slot, ":enemy_nearest_non_cav_agent", ":team_no", ":slot"),
                (gt, ":enemy_nearest_non_cav_agent", 0),
                (agent_get_position, pos60, ":enemy_nearest_non_cav_agent"),
                (agent_get_team, ":enemy_non_cav_team", ":enemy_nearest_non_cav_agent"),
                (team_get_leader, reg0, ":enemy_non_cav_team"),
                (try_begin),
                  (eq, ":enemy_nearest_non_cav_agent", reg0),	#team leader?
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (agent_get_division, ":target_division", ":enemy_nearest_non_cav_agent"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_non_cav_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination", pos1, ":team_no", grc_infantry, ":enemy_non_cav_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup", ":enemy_non_cav_team", ":target_division", Infantry_Pos),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),

              #chase nearest target
              (else_try),
                (assign, ":distance_to_enemy_troop", ":enemy_agent_nearest_infantry_dist"),
                (copy_position, pos60, Nearest_Enemy_Troop_Pos),
                (try_begin),
                  (eq, ":enemy_agent_nearest_infantry", ":enemy_leader"),
                  (assign, ":distance_to_enemy_group", Far_Away),
                (else_try),
                  (assign, ":target_division", ":enemy_agent_nearest_infantry_div"),
                  (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":enemy_agent_nearest_infantry_team"),
                  (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                  (team_set_slot, ":team_no", ":slot", ":target_division"),
                  (call_script, "script_battlegroup_get_attack_destination", pos1, ":team_no", grc_infantry, ":enemy_agent_nearest_infantry_team", ":target_division"),
                  (call_script, "script_get_distance_to_battlegroup", ":enemy_agent_nearest_infantry_team", ":target_division", Infantry_Pos),
                  (assign, ":distance_to_enemy_group", reg0),
                (try_end),
              (try_end),

              #reassemble if too scattered
              (try_begin),
                (call_script, "script_get_distance_to_battlegroup", ":team_no", grc_infantry, pos60),	#we're using enemy troop as a reference
                (val_sub, reg0, ":distance_to_enemy_troop"),
                (gt, reg0, 1500),	#division center too far from where it should be (probably because of
                #reinforcing troops)
                (position_copy_origin, pos1, Infantry_Pos),	#gather at average position
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),
                (assign, ":distance_to_move", reg0),
                (store_mul, reg0, 350, formation_reform_interval),
                (val_add, ":distance_to_move", reg0),	#one interval movement
                (position_move_y, pos1, ":distance_to_move"),	#keep rear moving forward

              #attack leader if is closest troop
              (else_try),
                (eq, ":target_division", -1),
                (position_copy_origin, pos1, pos60),
                (call_script, "script_point_y_toward_position", Infantry_Pos, pos1),
                (position_copy_rotation, pos1, Infantry_Pos),

              #move no farther than nearest troop if its unit is far off
              (else_try),
                (call_script, "script_battlegroup_dist_center_to_front", ":team_no", grc_infantry),
                (val_add, ":distance_to_enemy_troop", reg0),	#distance to center of bg from nearest edge
                (store_sub, reg0, ":distance_to_enemy_group", ":distance_to_enemy_troop"),
                (gt, reg0, AI_charge_distance),
                (position_copy_origin, pos1, Infantry_Pos),
                (position_move_y, pos1, ":distance_to_enemy_troop"),

              #shift dead player troops right to clear allies when both attacking the
              #same enemy battlegroup
              (else_try),
                (eq, ":team_no", "$fplayer_team_no"),
                (store_add, ":ally_team", "$fplayer_team_no", 2),
                (neg | teams_are_enemies, ":ally_team", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, ":ally_team", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":ally_team", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, ":ally_team", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position", pos0, ":ally_team", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius", ":ally_team", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, 2),	#function returns length of bg
                (position_move_x, pos1, reg0),

              #shift allies left to clear dead player troops when both attacking the
              #same enemy battlegroup
              (else_try),
                (main_hero_fallen),
                (eq, AI_Replace_Dead_Player, 1),
                (neq, ":team_no", "$fplayer_team_no"),
                (neg | teams_are_enemies, ":team_no", "$fplayer_team_no"),
                (store_add, ":slot", slot_team_d0_size, grc_infantry),
                (team_slot_ge, "$fplayer_team_no", ":slot", 1),
                (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
                (team_get_slot, ":target_team", "$fplayer_team_no", ":slot"),
                (team_slot_eq, ":team_no", ":slot", ":target_team"),
                (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
                (team_slot_eq, "$fplayer_team_no", ":slot", ":target_division"),
                (call_script, "script_battlegroup_get_position", pos0, "$fplayer_team_no", grc_infantry),
                (get_distance_between_positions, ":distance_to_ally", Infantry_Pos, pos0),
                (lt, ":distance_to_ally", ":distance_to_enemy_group"),	#shift only when not in melee to avoid rotation
                (call_script, "script_battlegroup_get_action_radius", "$fplayer_team_no", grc_infantry),	#move larger group less to maintain center
                (val_div, reg0, -2),	#function returns length of bg
                (position_move_x, pos1, reg0),
              (try_end),
            (try_end),	#obtain destination

            (call_script, "script_set_formation_destination", ":team_no", grc_infantry, pos1),

            (try_begin),
              (store_add, ":slot", slot_team_d0_formation, grc_infantry),
              (neg | team_slot_eq, ":team_no", ":slot", formation_none),
              (team_slot_ge, ":team_no", ":slot", formation_none),
              (call_script, "script_get_centering_amount", ":infantry_formation", ":num_infantry", ":spacing"),
              (position_move_x, pos1, reg0),
              (call_script, "script_form_infantry", ":team_no", grc_infantry, ":team_leader", ":spacing", 0, ":infantry_formation"),
            (try_end),
          (try_end),	#attempt to make formation somewhere
        (try_end),

        #cavalry AI
        (try_begin),
          (gt, ":num_cavalry", 0),

          #get distance to nearest enemy battlegroup(s)
          (store_add, ":slot", slot_team_d0_armor, grc_cavalry),
          (team_get_slot, ":average_armor", ":team_no", ":slot"),
          (assign, ":nearest_threat_distance", Far_Away),
          (assign, ":nearest_target_distance", Far_Away),
          (assign, ":num_targets", 0),
          (try_for_range, ":enemy_team_no", 0, 4),
            (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
            (teams_are_enemies, ":enemy_team_no", ":team_no"),
            (try_for_range, ":enemy_division", 0, 9),
              (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
              (team_get_slot, ":size_enemy_battle_group", ":enemy_team_no", ":slot"),
              (gt, ":size_enemy_battle_group", 0),
              (call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_division"),
              (get_distance_between_positions, ":distance_of_enemy", Cavalry_Pos, pos0),
              (try_begin),	#threat or target?
                (store_add, ":slot", slot_team_d0_weapon_length, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (assign, ":decision_index", reg0),
                (store_add, ":slot", slot_team_d0_armor, ":enemy_division"),
                (team_get_slot, reg0, ":enemy_team_no", ":slot"),
                (val_mul, ":decision_index", reg0),
                (val_mul, ":decision_index", ":size_enemy_battle_group"),
                (val_div, ":decision_index", ":average_armor"),
                (val_div, ":decision_index", ":num_cavalry"),
                (try_begin),
                  (neq, ":enemy_division", grc_cavalry),
                  (val_div, ":decision_index", 2),	#double count cavalry vs.  foot soldiers
                (try_end),
                (gt, ":decision_index", 100),
                (try_begin),
                  (gt, ":nearest_threat_distance", ":distance_of_enemy"),
                  (copy_position, Nearest_Threat_Pos, pos0),
                  (assign, ":nearest_threat_distance", ":distance_of_enemy"),
                (try_end),
              (else_try),
                (val_add, ":num_targets", 1),
                (gt, ":nearest_target_distance", ":distance_of_enemy"),
                (copy_position, Nearest_Target_Pos, pos0),
                (assign, ":nearest_target_distance", ":distance_of_enemy"),
                (store_add, ":slot", slot_team_d0_target_team, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_team_no"),
                (store_add, ":slot", slot_team_d0_target_division, grc_cavalry),
                (team_set_slot, ":team_no", ":slot", ":enemy_division"),
              (try_end),
            (try_end),
          (try_end),
          (try_begin),
            (eq, ":nearest_threat_distance", Far_Away),
            (assign, ":nearest_target_guarded", 0),
          (else_try),
            (eq, ":nearest_target_distance", Far_Away),
            (assign, ":nearest_target_guarded", 1),
          (else_try),
            (get_distance_between_positions, reg0, Nearest_Target_Pos, Nearest_Threat_Pos),
            (store_div, reg1, AI_charge_distance, 2),
            (try_begin),	#ignore target too close to threat
              (le, reg0, reg1),
              (assign, ":nearest_target_guarded", 1),
            (else_try),
              (assign, ":nearest_target_guarded", 0),
            (try_end),
          (try_end),

          (assign, ":cavalry_order", mordr_charge), ##CABA HERE
          (try_begin),
            (teams_are_enemies, ":team_no", 0),
            (neg | team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 1, slot_team_reinforcement_stage, "$attacker_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (teams_are_enemies, ":team_no", 1),
            (neg | team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
            (neg | team_slot_eq, 0, slot_team_reinforcement_stage, "$defender_reinforcement_stage"),
            (assign, ":cavalry_order", mordr_hold),
          (else_try),
            (neq, ":infantry_order", mordr_charge),
            (try_begin),
              (le, "$battle_phase", BP_Jockey),
              (assign, ":cavalry_order", mordr_hold),
            (else_try),
              (eq, ":nearest_target_distance", Far_Away),
              (try_begin),
                (eq, ":num_archers", 0),
                (assign, ":distance_to_archers", 0),
              (else_try),
                (get_distance_between_positions, ":distance_to_archers", Cavalry_Pos, Archers_Pos),
              (try_end),
              (try_begin),
                (this_or_next | gt, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
                (gt, ":distance_to_archers", AI_charge_distance),
                (assign, ":cavalry_order", mordr_hold),
              (try_end),
            (try_end),
          (try_end),

          (try_begin),
            (eq, ":team_no", 0),
            (assign, ":cav_destination", Team0_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 1),
            (assign, ":cav_destination", Team1_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 2),
            (assign, ":cav_destination", Team2_Cavalry_Destination),
          (else_try),
            (eq, ":team_no", 3),
            (assign, ":cav_destination", Team3_Cavalry_Destination),
          (try_end),
          (store_add, ":slot", slot_team_d0_percent_ranged, grc_cavalry),
          (team_get_slot, reg0, ":team_no", ":slot"),

          #horse archers don't use wedge
          (try_begin),
            (ge, reg0, 50),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (try_begin),
              (eq, ":num_archers", 0),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, mordr_charge),
                (team_give_order, ":team_no", grc_cavalry, mordr_charge),
              (try_end),
            (else_try),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
              (copy_position, ":cav_destination", Archers_Pos),
              (position_move_y, ":cav_destination", -500, 0),
              (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),
            (try_end),

          #close in with no unguarded target farther off, free fight
          (else_try),
            (eq, ":cavalry_order", mordr_charge),
            (this_or_next | eq, ":num_archers", 0),
            (le, ":enemy_agent_nearest_cavalry_dist", AI_charge_distance),
            (try_begin),
              (eq, ":num_targets", 1),
              (eq, ":nearest_target_guarded", 0),
              (gt, ":nearest_target_distance", ":nearest_threat_distance"),
              (assign, reg0, 0),
            (else_try),
              (ge, ":num_targets", 2),
              (eq, ":nearest_target_guarded", 1),
              (assign, reg0, 0),
            (else_try),
              (assign, reg0, 1),
            (try_end),
            (eq, reg0, 1),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_charge),
              (team_give_order, ":team_no", grc_cavalry, mordr_charge),
            (try_end),

          #grand charge if target closer than threat AND not guarded
          (else_try),
            (lt, ":nearest_target_distance", ":nearest_threat_distance"),
            (eq, ":nearest_target_guarded", 0),
            (call_script, "script_formation_end", ":team_no", grc_cavalry),
            (team_get_movement_order, reg0, ":team_no", grc_cavalry),
            (try_begin),
              (neq, reg0, mordr_hold),
              (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (try_end),

            #lead archers up to firing point
            (try_begin),
              (gt, ":nearest_target_distance", AI_firing_distance),
              (eq, ":cavalry_order", mordr_hold),
              (try_begin),
                (eq, ":num_archers", 0),
                (copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
              (else_try),
                (copy_position, ":cav_destination", Archers_Pos),
                (position_move_y, ":cav_destination", AI_charge_distance, 0),
              (try_end),

            #then CHARRRRGE!
            (else_try),
              (copy_position, ":cav_destination", Cavalry_Pos),
              (call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
            (try_end),
            (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),

          #make a wedge somewhere
          (else_try),
            (try_begin),
              (eq, ":cavalry_order", mordr_charge),
              (neq, ":nearest_target_distance", Far_Away),
              (copy_position, ":cav_destination", Cavalry_Pos),
              (call_script, "script_point_y_toward_position", ":cav_destination", Nearest_Target_Pos),
              (position_move_y, ":cav_destination", ":nearest_target_distance", 0),
              (position_move_y, ":cav_destination", AI_charge_distance, 0),	#charge on through to the other side
            (else_try),
              (neq, ":cavalry_order", mordr_charge),
              (eq, ":num_archers", 0),
              (copy_position, ":cav_destination", Cavalry_Pos),	#must be reinforcements, so gather at average position
            (else_try),
              (copy_position, ":cav_destination", Archers_Pos),	#hold near archers
              (position_move_x, ":cav_destination", 500, 0),
              (position_move_y, ":cav_destination", -1000, 0),
            (try_end),

            #move around threat in the way to destination
            (try_begin),
              (neq, ":nearest_threat_distance", Far_Away),
              (call_script, "script_point_y_toward_position", Cavalry_Pos, Nearest_Threat_Pos),
              (call_script, "script_point_y_toward_position", Nearest_Threat_Pos, ":cav_destination"),
              (position_get_rotation_around_z, reg0, Cavalry_Pos),
              (position_get_rotation_around_z, reg1, Nearest_Threat_Pos),
              (store_sub, ":rotation_diff", reg0, reg1),
              (try_begin),
                (lt, ":rotation_diff", -180),
                (val_add, ":rotation_diff", 360),
              (else_try),
                (gt, ":rotation_diff", 180),
                (val_sub, ":rotation_diff", 360),
              (try_end),

              (try_begin),
                (is_between, ":rotation_diff", -135, 136),
                (copy_position, ":cav_destination", Cavalry_Pos),
                (assign, ":distance_to_move", AI_firing_distance),
                (try_begin),	#target is left of threat
                  (is_between, ":rotation_diff", -135, 0),
                  (val_mul, ":distance_to_move", -1),
                (try_end),
                (position_move_x, ":cav_destination", ":distance_to_move", 0),
                (store_sub, ":distance_to_move", ":nearest_threat_distance", AI_firing_distance),
                (position_move_y, ":cav_destination", ":distance_to_move", 0),
                (call_script, "script_point_y_toward_position", ":cav_destination", Cavalry_Pos),
                (position_rotate_z, ":cav_destination", 180),
              (try_end),
            (try_end),
            (get_scene_boundaries, pos0, pos1),
            (position_get_x, reg0, ":cav_destination"),
            (position_get_x, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_x, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_x, ":cav_destination", reg0),
            (position_get_y, reg0, ":cav_destination"),
            (position_get_y, reg1, pos0),
            (val_max, reg0, reg1),
            (position_get_y, reg1, pos1),
            (val_min, reg0, reg1),
            (position_set_y, ":cav_destination", reg0),
            (position_set_z_to_ground_level, ":cav_destination"),

            (try_begin),
              (call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_cavalry, formation_wedge),
              (copy_position, pos1, ":cav_destination"),
              (call_script, "script_form_cavalry", ":team_no", grc_cavalry, ":team_leader", 0, 0),
              (store_add, ":slot", slot_team_d0_formation, grc_cavalry),
              (team_set_slot, ":team_no", ":slot", formation_wedge),
              # (team_give_order, ":team_no", grc_cavalry, mordr_hold),
            (else_try),
              (call_script, "script_formation_end", ":team_no", grc_cavalry),
              (team_get_movement_order, reg0, ":team_no", grc_cavalry),
              (try_begin),
                (neq, reg0, ":cavalry_order"),
                (team_give_order, ":team_no", grc_cavalry, ":cavalry_order"),
              (try_end),
            (try_end),
            (call_script, "script_set_formation_destination", ":team_no", grc_cavalry, ":cav_destination"),
          (try_end),
        (try_end),

        #place leader
        (try_begin),
          (ge, ":team_leader", 0),
          (agent_is_alive, ":team_leader"),
          (agent_slot_eq, ":team_leader", slot_agent_is_running_away, 0),
          (try_begin),
            (le, ":num_infantry", 0),
            (try_begin),
              (this_or_next | le, ":num_archers", 0),
              (eq, ":archer_order", mordr_retreat),

              (assign, ":more_reinforcements", 1),
              (try_begin),
                (teams_are_enemies, ":team_no", 0),
                (team_slot_ge, 1, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (else_try),
                (teams_are_enemies, ":team_no", 1),
                (team_slot_ge, 0, slot_team_reinforcement_stage, AI_Max_Reinforcements),
                (assign, ":more_reinforcements", 0),
              (try_end),
              (eq, ":more_reinforcements", 0),

              (agent_get_troop_id, ":troop_id", ":team_leader"), #for now do not let heroes to run away from battle
              (neg|troop_is_hero, ":troop_id"),
              (agent_clear_scripted_mode, ":team_leader"),
              (agent_start_running_away, ":team_leader"),
              (agent_set_slot, ":team_leader",  slot_agent_is_running_away, 1),
            (else_try),
              (eq, ":archer_order", mordr_charge),
              (agent_clear_scripted_mode, ":team_leader"),
            (else_try),
              (copy_position, pos1, Archers_Pos),
              (position_move_y, pos1, -1000, 0),
              (agent_set_scripted_destination, ":team_leader", pos1, 1),
            (try_end),
          (else_try),
            (neq, ":place_leader_by_infantry", 0),
            (call_script, "script_battlegroup_get_position", pos1, ":team_no", grc_infantry),
            (team_get_order_position, pos0, ":team_no", grc_infantry),
            (call_script, "script_point_y_toward_position", pos1, pos0),
            (call_script, "script_battlegroup_get_action_radius", ":team_no", grc_infantry),
            (val_div, reg0, 2),	#bring to edge of battlegroup
            (position_move_x, pos1, reg0, 0),
            (position_move_x, pos1, 100, 0),
            (agent_set_scripted_destination, ":team_leader", pos1, 1),
          (else_try),
            (agent_clear_scripted_mode, ":team_leader"),
          (try_end),
        (try_end),
      (try_end),

  ]),

  # script_field_tactics by motomataru
  # Input: flag 1 to include ranged
  # Output: none
  ("field_tactics", [
      (store_script_param, ":include_ranged", 1),

      (assign, ":largest_team_size", 0),
      (assign, ":battle_size", 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":team_size", ":ai_team", slot_team_size),
        (gt, ":team_size", 0),
        (team_get_slot, ":team_cav_size", ":ai_team", slot_team_num_cavalry),
        (store_add, ":team_adj_size", ":team_size", ":team_cav_size"),	#double count cavalry to capture effect on battlefield
        (val_add, ":battle_size", ":team_adj_size"),

        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (neg | teams_are_enemies, ":ai_team", "$fplayer_team_no"),
          (team_get_slot, ":player_team_adj_size", "$fplayer_team_no", slot_team_adj_size),
          (val_add, ":team_adj_size", ":player_team_adj_size"),	#ally team takes player team into account
          (team_set_slot, "$fplayer_team_no", slot_team_adj_size, ":team_adj_size"),	#and vice versa
        (try_end),
        (team_set_slot, ":ai_team", slot_team_adj_size, ":team_adj_size"),

        (lt, ":largest_team_size", ":team_adj_size"),
        (assign, ":largest_team_size", ":team_adj_size"),
      (try_end),

      #apply tactics to every AI team
      (set_show_messages, 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":ai_team_size", ":ai_team", slot_team_adj_size),
        (gt, ":ai_team_size", 0),

        (assign, ":do_it", 0),
        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (assign, ":do_it", 1),
        (else_try),
          (main_hero_fallen),    #have AI take over for mods with post-player battle action
          (eq, AI_Replace_Dead_Player, 1),
          (assign, ":do_it", 1),
        (try_end),
        (eq, ":do_it", 1),

        (team_get_slot, ":ai_faction", ":ai_team", slot_team_faction),
        (try_begin),
          (neq, AI_for_kingdoms_only, 0),
          (neq, ":ai_faction", fac_deserters),	#deserters have military training
          (neq, ":ai_faction", fac_black_khergits),
          (neq, ":ai_faction", fac_dark_knights),
          #(neq, ":ai_faction", fac_mountain_bandits),	#scoti, frank and dena pirates have military training Chief anade
          (neg | is_between, ":ai_faction", kingdoms_begin, kingdoms_end),

          (call_script, "script_formation_end", ":ai_team", grc_everyone),
          (team_get_movement_order, reg0, ":ai_team", grc_everyone),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":ai_team", grc_everyone, mordr_charge),
          (try_end),

        #uses tactics
        (else_try),
          (val_mul, ":ai_team_size", 100),
          (store_div, ":team_percentage", ":ai_team_size", ":largest_team_size"),
          (store_div, ":team_battle_presence", ":ai_team_size", ":battle_size"),
          (try_begin),
            (eq, ":include_ranged", 1),
            (try_begin),
              (store_mod, ":team_phase", ":ai_team", 2),
              (eq, ":team_phase", 0),
              (assign, ":time_slice", 0),
            (else_try),
              (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
            (try_end),

            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (this_or_next | eq, reg0, ":time_slice"),
            (eq, "$battle_phase", BP_Setup),
            (call_script, "script_team_field_ranged_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
          (try_end),

          (try_begin),
            (gt, "$fplayer_team_no", 0),	#not a spectator
            (neg | main_hero_fallen),
            (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
            (team_slot_eq, ":ai_team", ":slot", "$fplayer_team_no"),
            (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
            (team_get_slot, ":enemy_division", ":ai_team", ":slot"),
            (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
            (team_slot_ge, "$fplayer_team_no", ":slot", 1),
            (store_add, ":slot", slot_team_d0_fclock, ":enemy_division"),
            (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
            (store_mod, reg0, ":fclock", Reform_Trigger_Modulus),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (else_try),
            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (store_mod, ":team_phase", ":ai_team", 2),
            (eq, ":team_phase", 0),
            (assign, ":time_slice", 0),
          (else_try),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (try_end),

          (eq, reg0, ":time_slice"),
          (call_script, "script_team_field_melee_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
        (try_end),
      (try_end),
      (set_show_messages, 1),]),


  # # Utilities used by AI by motomataru

  # script_find_high_ground_around_pos1_corrected by motomataru
  # Input: arg1: destination position
  #			arg2: search_radius (in meters)
  #			pos1 should hold center_position_no
  # Output: destination contains highest ground within a <search_radius> meter
  # square around pos1
  # Also uses position registers: pos0
  ("find_high_ground_around_pos1_corrected", [
      (store_script_param, ":destination_pos", 1),
      (store_script_param, ":search_radius", 2),
      (assign, ":fixed_point_multiplier", 1),
      (convert_to_fixed_point, ":fixed_point_multiplier"),
      (set_fixed_point_multiplier, 1),

      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),

      (get_scene_boundaries, ":destination_pos", pos0),
      (position_get_x, ":scene_min_x", ":destination_pos"),
      (position_get_x, ":scene_max_x", pos0),
      (position_get_y, ":scene_min_y", ":destination_pos"),
      (position_get_y, ":scene_max_y", pos0),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (assign, ":highest_pos_z", -100),
      (copy_position, ":destination_pos", pos1),
      (init_position, pos0),

      (try_for_range, ":i_x", ":min_x", ":max_x"),
        (try_for_range, ":i_y", ":min_y", ":max_y"),
          (position_set_x, pos0, ":i_x"),
          (position_set_y, pos0, ":i_y"),
          (position_set_z_to_ground_level, pos0),
          (position_get_z, ":cur_pos_z", pos0),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, ":destination_pos", pos0),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),

      (set_fixed_point_multiplier, ":fixed_point_multiplier"),]),


  # script_cf_count_casualties by motomataru
  # Input: none
  # Output: evalates T/F, reg0 num casualties
  ("cf_count_casualties", [
      (assign, ":num_casualties", 0),
      (try_for_agents,":cur_agent"),
        (try_begin),
          (this_or_next | agent_is_wounded, ":cur_agent"),
          (this_or_next | agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
          (neg | agent_is_alive, ":cur_agent"),
          (val_add, ":num_casualties", 1),
        (try_end),
      (try_end),
      (assign, reg0, ":num_casualties"),
      (gt, ":num_casualties", 0)]),


  # script_cf_any_fighting by motomataru
  # Input: none
  # Output: evalates T/F
  ("cf_any_fighting", [
      (assign, ":any_fighting", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (eq, ":any_fighting", 0),
        (assign, ":num_divs", 9),
        (try_for_range, ":division", 0, ":num_divs"),
          (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
          (team_slot_ge, ":team", ":slot", 1),
          (assign, ":any_fighting", 1),
          (assign, ":num_divs", 0),
        (try_end),
      (try_end),

      #lag this check to be sure
      (store_mission_timer_c, ":time_stamp"),
      (try_begin),	#time lag
        (gt, ":any_fighting", 0),
        (assign, "$teams_last_fighting", ":time_stamp"),
      (try_end),
      (assign, ":fighting_finished", formation_reform_interval),
      (val_max, ":fighting_finished", 5),
      (val_add, ":fighting_finished", "$teams_last_fighting"),
      (gt, ":fighting_finished", ":time_stamp"),]),


  # script_get_nearest_enemy_battlegroup_location by motomataru
  # Input: destination position, fron team, from position
  # Output: destination position, reg0 with distance
  # Run script_store_battlegroup_data before calling!
  ("get_nearest_enemy_battlegroup_location", [
      (store_script_param, ":bgposition", 1),
      (store_script_param, ":team_no", 2),
      (store_script_param, ":from_pos", 3),
      (assign, ":distance_to_nearest_enemy_battlegoup", Far_Away),
      (try_for_range, ":enemy_team_no", 0, 4),
        (team_slot_ge, ":enemy_team_no", slot_team_size, 1),
        (teams_are_enemies, ":enemy_team_no", ":team_no"),
        (try_for_range, ":enemy_division", 0, 9),
          (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
          (team_slot_ge, ":enemy_team_no", ":slot", 1),
          (call_script, "script_battlegroup_get_position", pos0, ":enemy_team_no", ":enemy_division"),
          (get_distance_between_positions, reg0, pos0, ":from_pos"),
          (try_begin),
            (gt, ":distance_to_nearest_enemy_battlegoup", reg0),
            (assign, ":distance_to_nearest_enemy_battlegoup", reg0),
            (copy_position, ":bgposition", pos0),
          (try_end),
        (try_end),
      (try_end),
      (assign, reg0, ":distance_to_nearest_enemy_battlegoup")]),
  # #AI end



	("find_nearest_enemy_position",
		[
			(store_script_param, ":agent", 1),
			(store_script_param, ":agent_team", 2),
			(store_script_param, ":threshold", 3), #if under threshold then stop searching
			(assign, ":nearest_dist", 100000),
			(assign, ":nearest_agent", -1),
			(agent_get_position, pos1, ":agent"),
			(try_for_agents, ":agent2"),
				(gt, ":nearest_dist", ":threshold"),
				(agent_is_alive, ":agent2"),
				(agent_is_active, ":agent2"),
				(agent_is_human, ":agent2"),
				(agent_get_team, ":agent2_team", ":agent2"),
				(teams_are_enemies, ":agent2_team", ":agent_team"),
				(agent_get_position, pos2, ":agent2"),
				(get_distance_between_positions, ":enemy_dist", pos2, pos1),
				(lt, ":enemy_dist", ":nearest_dist"),
				(assign, ":nearest_agent", ":agent2"),
				(assign, ":nearest_dist", ":enemy_dist"),
			(try_end),
			(assign, reg1, ":nearest_dist"),
			(assign, reg4, ":nearest_agent")
		]),

	("horse_archer_skirmish",
		[
			(store_script_param, ":agent", 1), #agent
			(store_script_param, ":enemy_agent", 2), #enemy agent
			(store_script_param, ":enemy_dist", 3), #distance from enemy
			(store_script_param, ":min_dist", 4), #min distance (inner radius)
			(store_script_param, ":max_dist", 5), #max distance (outer radius)
			(store_script_param, ":script_param_6", 6), #new position adder
			(try_begin),
				(assign, ":min_dist_from_enemy", ":min_dist"),
				(gt, ":enemy_agent", 0),
				(agent_get_position, pos0, ":agent"),
				(agent_get_position, pos1, ":enemy_agent"),
				# (agent_get_slot, ":skirmish_direction", ":agent", 106), #1/2 agents go clockwise
				(agent_get_slot, ":dist_to_add", ":agent", slot_agent_make_dist_with_enemy),
				# (try_begin),
					# (eq, ":skirmish_direction", 0),
					# (store_random_in_range, ":skirmish_direction", 1, 3),
					# (agent_set_slot, ":agent", 106, ":skirmish_direction"),
				# (try_end),
				(try_begin),
					(le, ":enemy_dist", ":max_dist"),
					(val_add, ":dist_to_add", ":script_param_6"),
					(try_begin),
						(ge, ":dist_to_add", 360),
						(assign, ":dist_to_add", 0),
					(try_end),
					(agent_set_slot, ":agent", slot_agent_make_dist_with_enemy, ":dist_to_add"),
					# (try_begin),
						# (eq, ":skirmish_direction", 1),
						# (val_mul, ":dist_to_add", -1),
						# (val_sub, ":min_dist_from_enemy", 1500), #clockwise agents stay closer to enemy
					# (try_end),
					(position_get_rotation_around_z, reg1, 1),
					(store_sub, reg0, 360, reg1),
					(val_add, ":dist_to_add", reg0),
					(position_rotate_z, pos1, ":dist_to_add"),
					(position_move_x, pos1, ":min_dist_from_enemy", 0),
					(agent_set_scripted_destination, ":agent", pos1, 1), #no rethink?
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 1),
				(else_try),
					(agent_clear_scripted_mode, ":agent"),
					(agent_set_slot, ":agent", slot_agent_is_skirmishing, 0),
				(try_end),
			(try_end)
		]),


	("assign_seneschals",
		[
          #seneschals - dckplmc
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (store_sub, ":offset", ":center_no", walled_centers_begin),
            (store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
            (troop_set_slot, ":cur_object_no", slot_troop_occupation, slto_kingdom_seneschal),
            (party_set_slot,":center_no", slot_town_seneschal, ":cur_object_no"),
          (try_end),
		]),


  # script_get_random_tournament_participant
("simple_remove_disguise",
 [
	(try_begin),
		(gt, "$sneaked_into_town", disguise_none),
		(display_message, "@You retrieve your hidden items.", message_alert),
		(try_begin),
			(eq, "$g_dplmc_player_disguise", 1),
			(set_show_messages, 0),
		(try_for_range, ":i_slot", ek_item_0, ek_food + 1),
			(troop_get_inventory_slot, ":item", "trp_player", ":i_slot"),
			(neq, ":item", -1),
			(troop_get_inventory_slot_modifier, ":imod", "trp_player", ":i_slot"),
			(troop_add_item, "trp_random_town_sequence", ":item", ":imod"),
		(try_end),
			(call_script, "script_move_inventory_and_gold", "trp_player", "trp_random_town_sequence", 0),
			(call_script, "script_dplmc_copy_inventory", "trp_random_town_sequence", "trp_player"),
			(call_script, "script_troop_transfer_gold", "trp_random_town_sequence", "trp_player", 0),
			(set_show_messages, 1),
		(try_end),
		(assign, "$sneaked_into_town", disguise_none),
	(try_end),
]),

### MMC gambler end ###
  # Input: arg1 = controversy difference
  # Output: none
  ("change_player_controversy",
    [
      (store_script_param_1, ":controversy_dif"),
	  (troop_set_slot, "trp_player", slot_troop_controversy, ":controversy_dif"),
      (try_begin),
        (lt, ":controversy_dif", 0),
        (display_message, "@Things cool down.", message_positive),
      (else_try),
        (gt, ":controversy_dif", 0),
        (display_message, "@Rumors will certianly spread over this.", message_negative),
      (try_end),
  ]),

# script_pos_helper
# Description: Little Pos Helper by Kuba
# Input1: ti_on_presentation_***
# Output: none
("pos_helper",
 [  (store_script_param, ":ti_on", 1),
    (try_begin),
        (eq, ":ti_on", 1),# ti_on_presentation_load
		(create_text_overlay, "$g_little_pos_helper", "@00,00"),
		(overlay_set_color, "$g_little_pos_helper", 0xFFFFFFFF),
		(position_set_x, pos1, 10),
		(position_set_y, pos1, 700),
		(overlay_set_position, "$g_little_pos_helper", pos1),
    (try_end),
    (try_begin),
        (eq, ":ti_on", 2),# ti_on_presentation_run
		(mouse_get_position, pos1),
		(position_get_x, reg1, pos1),
		(position_get_y, reg2, pos1),
		(overlay_set_text, "$g_little_pos_helper", "@{reg1},{reg2}"),
    (try_end),
 ]),
 # script_update_order_panel_map
  # Input: none
  # Output: none
  ("update_map_bar",
   [
    (set_fixed_point_multiplier, 1000),

    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
      (try_begin),
        (agent_is_alive, ":cur_agent"),
        (call_script, "script_update_agent_position_on_map_bar", ":cur_agent"),
      (else_try),
        (overlay_set_alpha, ":agent_overlay", 0),
      (try_end),
    (try_end),
    # player_chest
    (try_begin),
      (scene_prop_get_instance, ":player_chest", "spr_inventory", 0),
      (ge, ":player_chest", 0),
      (prop_instance_get_position, pos1, ":player_chest"),
      (call_script, "script_convert_3d_pos_to_map_bar_pos", -5),
      (overlay_set_position, "$g_player_chest_overlay", pos0),
      (overlay_set_alpha, "$g_player_chest_overlay", 0xFF),
    (else_try),
      (overlay_set_alpha, "$g_player_chest_overlay", 0),
    (try_end),
    # Horse Stamina
    #(agent_get_horse, ":horse_agent", ":player_agent"),
    #(try_begin),
    #  (eq, "$g_horse_charging_for_player", 1),
    #  (ge, ":horse_agent", 0),
    #  (agent_get_slot, ":horse_stamina", ":player_agent", slot_agent_horse_stamina),
    #  (store_agent_hit_points, ":horse_hp", ":horse_agent"),
    #  (assign, reg1, ":horse_stamina"),
    #  (assign, reg2, ":horse_hp"),
    #  (overlay_set_text, "$g_horse_stamina_overlay", "@Horse Stamina: {reg1}/{reg2}"),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0xFF),
    #(else_try),
    #  (overlay_set_alpha, "$g_horse_stamina_overlay", 0),
    #(try_end),
    # enemies-allies-us
    (assign, ":num_us_ready_men", 0),
    (assign, ":num_allies_ready_men", 0),
    (assign, ":num_enemies_ready_men", 0),
    (agent_get_team, ":player_team", ":player_agent"),
    (try_for_agents,":agent_no"),
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (try_begin),
        (neg|agent_is_ally, ":agent_no"),
        (val_add, ":num_enemies_ready_men", 1),
      (else_try),
        (eq, ":agent_team", ":player_team"),
        (val_add, ":num_us_ready_men", 1),
      (else_try),
        (val_add, ":num_allies_ready_men", 1),
      (try_end),
    (try_end),
    (assign, reg10, ":num_enemies_ready_men"),
    (assign, reg11, ":num_allies_ready_men"),
    (assign, reg12, ":num_us_ready_men"),
    (overlay_set_text, "$g_battle_enemies_ready", "@{!}{reg10}"),
    (overlay_set_text, "$g_battle_allies_ready", "@{!}{reg11}"),
    (overlay_set_text, "$g_battle_us_ready", "@{!}{reg12}"),
  ]),
  #Presentation line
 ("prsnt_line",
    [
      (store_script_param, ":size_x", 1),
      (store_script_param, ":size_y", 2),
      (store_script_param, ":pos_x", 3),
      (store_script_param, ":pos_y", 4),
      (store_script_param, ":color", 5),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (val_mul, ":size_x", 50),
      (val_mul, ":size_y", 50),
      (position_set_x, pos0, ":size_x"),
      (position_set_y, pos0, ":size_y"),
      (overlay_set_size, reg1, pos0),
      (position_set_x, pos0, ":pos_x"),
      (position_set_y, pos0, ":pos_y"),
      (overlay_set_position, reg1, pos0),
      (overlay_set_color, reg1, ":color"),
  ]),
  # script_update_agent_position_on_map_bar
  # Input: arg1 = agent_no
  # Output: none
  ("update_agent_position_on_map_bar",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 300),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (agent_get_team, ":player_team", ":player_agent"),
    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (try_begin),
        (neg|agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0xFF4040),
        (assign, ":y_offset", 10),
      (else_try),
        (eq, ":agent_team", ":player_team"),
        (overlay_set_color, ":agent_overlay", 0x80FF80),
        (assign, ":y_offset", -10),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0x8080FF),
        (assign, ":y_offset", 0),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (position_set_x, pos0, 620),
      (position_set_y, pos0, 721),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_bar_pos", ":y_offset"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ]),

  # script_convert_3d_pos_to_map_bar_pos
  ("convert_3d_pos_to_map_bar_pos",
   [
    (store_script_param_1, ":y_offset"),

    (set_fixed_point_multiplier, 1000),
    (position_move_z, pos1, 170),
    (position_get_screen_projection, pos3, pos1),
    (position_get_x, ":pos_x", pos3),
    (try_begin),
      (is_between, ":pos_x", -200, 1201),
      (val_clamp, ":pos_x", 0, 1001),
    (else_try), # hide on the left
      (lt, ":pos_x", -200),
      (assign, ":pos_x", -250),
    (else_try), # hide on the right
      (gt, ":pos_x", 1200),
      (assign, ":pos_x", 1250),
    (try_end),
    (val_sub, ":pos_x", 500),
    (val_mul, ":pos_x", 20),
    (val_div, ":pos_x", 100),
    (val_add, ":pos_x", 500),
    (store_add, ":pos_y", 721, ":y_offset"),
    (position_set_x, pos0, ":pos_x"),
    (position_set_y, pos0, ":pos_y"),
  ]),

  # # script_convert_map_pos_to_3d_pos
  # ("convert_map_pos_to_3d_pos",
   # [
    # (set_fixed_point_multiplier, 1000),
    # (store_sub, ":map_x", 980, "$g_battle_map_width"),
    # (store_sub, ":map_y", 730, "$g_battle_map_height"),
    # (position_get_x, ":point_x_pos", pos1),
    # (position_get_y, ":point_y_pos", pos1),
    # (val_sub, ":point_x_pos", ":map_x"),
    # (val_sub, ":point_y_pos", ":map_y"),
    # (val_mul, ":point_x_pos", "$g_battle_map_scale"),
    # (val_mul, ":point_y_pos", "$g_battle_map_scale"),
    # (position_set_x, pos3, ":point_x_pos"),
    # (position_set_y, pos3, ":point_y_pos"),
    # (set_fixed_point_multiplier, 1000),
    # (position_transform_position_to_parent, pos0, pos2, pos3),
  # ]),

  ("update_agent_hp_bar",
   [
    (set_fixed_point_multiplier, 1000),

    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":agent_no"),
      (agent_is_human, ":agent_no"),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_slot, ":agent_hp_overlay", ":agent_no", slot_agent_hp_bar_overlay_id),
      (agent_get_slot, ":agent_hp_bg_overlay", ":agent_no", slot_agent_hp_bar_bg_overlay_id),
      #(agent_get_slot, ":agent_name_overlay", ":agent_no", slot_agent_name_overlay_id),
      (try_begin),
        (agent_is_alive, ":agent_no"),
        # (agent_get_slot, ":agent_hp_overlay", ":agent_no", slot_agent_hp_bar_overlay_id),
        # (agent_get_slot, ":agent_hp_bg_overlay", ":agent_no", slot_agent_hp_bar_bg_overlay_id),
        # (agent_get_slot, ":agent_name_overlay", ":agent_no", slot_agent_name_overlay_id),

        (assign, ":create_hp_bar", 0),
        #(assign, ":create_name", 0),
        (try_begin), # create or not
          (agent_is_ally, ":agent_no"),
          (assign, ":create_hp_bar", "$g_hp_bar_ally"),
          #(assign, ":create_name", "$g_name_of_ally"),
        (else_try),
          (assign, ":create_hp_bar", "$g_hp_bar_enemy"),
          #(assign, ":create_name", "$g_name_of_enemy"),
        (try_end),

        (try_begin),
          (le, ":agent_hp_overlay", 0),
          (le, ":agent_hp_bg_overlay", 0),
          #(le, ":agent_name_overlay", 0),
          (set_fixed_point_multiplier, 1000),
          (try_begin),
            (eq, ":create_hp_bar", 1),
            # hp bg
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_alpha, reg1, 0x44),
            (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, reg1),
            (assign, ":agent_hp_bg_overlay", reg1),
            # hp
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_alpha, reg1, 0x44),
            (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, reg1),
            (assign, ":agent_hp_overlay", reg1),
          (try_end),
          # (try_begin),
            # (eq, ":create_name", 1),
            ## name
            # (agent_get_troop_id, ":troop_id", ":agent_no"),
            # (str_store_troop_name, s1, ":troop_id"),
            # (create_text_overlay, reg1, "@{s1}", tf_center_justify),
            # (overlay_set_alpha, reg1, 0xCC),
            # (agent_set_slot, ":agent_no", slot_agent_name_overlay_id, reg1),
            # (assign, ":agent_name_overlay", reg1),
          # (try_end),
        (try_end),

        # color
        (agent_get_team, ":player_team", ":player_agent"),
        (agent_get_team, ":agent_team", ":agent_no"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (try_begin),
          (eq, ":agent_team", ":player_team"),
          (assign, ":dest_color", 0x00FF00),
        (else_try),
          (agent_is_ally, ":agent_no"),
          (assign, ":dest_color", 0x0000FF),
        (else_try),
          (troop_is_hero, ":troop_id"),
          (assign, ":dest_color", 0xFFFF00),
        (else_try),
          (assign, ":dest_color", 0xFF0000),
        (try_end),
        (try_begin),
          (gt, ":agent_hp_overlay", 0),
          (gt, ":agent_hp_bg_overlay", 0),
          (overlay_set_color, ":agent_hp_overlay", ":dest_color"),
          (overlay_set_color, ":agent_hp_bg_overlay", 0x000000),
        (try_end),
        # (try_begin),
          # (gt, ":agent_name_overlay", 0),
          # (overlay_set_color, ":agent_name_overlay", ":dest_color"),
        # (try_end),

        # size & position
        # (this_or_next|gt, ":agent_name_overlay", 0),
        (gt, ":agent_hp_overlay", 0),

        (agent_get_position, pos1, ":agent_no"),
        (agent_get_horse, ":horse_agent", ":agent_no"),
        (try_begin),
          (ge, ":horse_agent", 0),
          (position_move_z, pos1, 280, 1),
        (else_try),
          (position_move_z, pos1, 180, 1),
        (try_end),
        (position_get_screen_projection, pos2, pos1),
        (position_get_x, ":head_x_pos", pos2),
        (position_get_y, ":head_y_pos", pos2),
        # base size
        (copy_position, pos6, pos1),
        (copy_position, pos7, pos1),
        (position_move_z, pos7, 100, 1),
        (position_get_screen_projection, pos6, pos6),
        (position_get_screen_projection, pos7, pos7),
        (position_get_y, ":screen_y_pos_1", pos6),
        (position_get_y, ":screen_y_pos_2", pos7),
        (store_sub, ":base_x", ":screen_y_pos_2", ":screen_y_pos_1"),
        (val_mul, ":base_x", 3),
        (val_div, ":base_x", 4),
        (val_clamp, ":base_x", 20, 161),
        (store_div, ":base_y", ":base_x", 20),
        (try_begin),
          (is_between, ":head_x_pos", -100, 1100),
          (is_between, ":head_y_pos", -100, 850),
          (agent_get_position, pos3, ":agent_no"),
          (agent_get_position, pos4, ":player_agent"),
          (get_distance_between_positions_in_meters, ":distance", pos3, pos4),
          (try_begin),
            (troop_is_hero, ":troop_id"),
            (val_div, ":distance", 2),
          (try_end),
          (le, ":distance", "$g_hp_bar_dis_limit"),
          # agent no
          (agent_get_horse, ":horse_agent", ":agent_no"),
          (try_begin),
            (ge, ":horse_agent", 0),
            (position_move_z, pos3, 280, 1),
          (else_try),
            (position_move_z, pos3, 180, 1),
          (try_end),
          # player agent
          (agent_get_horse, ":player_horse", ":player_agent"),
          (try_begin),
            (ge, ":player_horse", 0),
            (position_move_z, pos4, 280, 1),
          (else_try),
            (position_move_z, pos4, 180, 1),
          (try_end),
          (position_move_z, pos3, 50, 1),
          (position_move_z, pos4, 50, 1),
          (position_has_line_of_sight_to_position, pos3, pos4),

          (try_begin),
            (gt, ":agent_hp_overlay", 0),
            (gt, ":agent_hp_bg_overlay", 0),
            ## hp bg
            (assign, ":x_offset", ":base_x"),
            (val_div, ":x_offset", 2),
            (val_add, ":x_offset", 1),
            (store_sub, ":hp_bg_x", ":head_x_pos", ":x_offset"),
            (store_sub, ":hp_bg_y", ":head_y_pos", 1),
            (position_set_x, pos1, ":hp_bg_x"),
            (position_set_y, pos1, ":hp_bg_y"),
            (overlay_set_position, ":agent_hp_bg_overlay", pos1),
            (store_add, ":bg_width", ":base_x", 2),
            (val_mul, ":bg_width", 50),
            (store_add, ":bg_height", ":base_y", 2),
            (val_mul, ":bg_height", 50),
            (position_set_x, pos1, ":bg_width"),
            (position_set_y, pos1, ":bg_height"),
            (overlay_set_size, ":agent_hp_bg_overlay", pos1),
            (overlay_set_alpha, ":agent_hp_bg_overlay", 0x44),
            ## hp
            (store_add, ":hp_x", ":hp_bg_x", 1),
            (store_add, ":hp_y", ":hp_bg_y", 1),
            (position_set_x, pos1, ":hp_x"),
            (position_set_y, pos1, ":hp_y"),
            (overlay_set_position, ":agent_hp_overlay", pos1),
            (store_agent_hit_points, ":agent_hp",":agent_no"),
            (store_mul, ":hp_width", ":agent_hp", 50),
            (val_mul, ":hp_width", ":base_x"),
            (val_div, ":hp_width", 100),
            (val_min, ":hp_width", ":bg_width"),
            (store_mul, ":hp_height", ":base_y", 50),
            (position_set_x, pos1, ":hp_width"),
            (position_set_y, pos1, ":hp_height"),
            (overlay_set_size, ":agent_hp_overlay", pos1),
            (overlay_set_alpha, ":agent_hp_overlay", 0x44),
          (try_end),

          # name
          # (try_begin),
            # (gt, ":agent_name_overlay", 0),
            # (assign, ":name_x", ":head_x_pos"),
            # (store_add, ":name_y", ":head_y_pos", 5),
            # (position_set_x, pos1, ":name_x"),
            # (position_set_y, pos1, ":name_y"),
            # (overlay_set_position, ":agent_name_overlay", pos1),
            # (store_mul, ":name_size", ":base_x", 9),
            # (position_set_x, pos1, ":name_size"),
            # (position_set_y, pos1, ":name_size"),
            # (overlay_set_size, ":agent_name_overlay", pos1),
            # (overlay_set_alpha, ":agent_name_overlay", 0xCC),
          # (try_end),
        (else_try),
          (overlay_set_alpha, ":agent_hp_overlay", 0),
          (overlay_set_alpha, ":agent_hp_bg_overlay", 0),
          # (overlay_set_alpha, ":agent_name_overlay", 0),
        (try_end),
      (else_try),
        (try_begin),
          (gt, ":agent_hp_overlay", 0),
          (gt, ":agent_hp_bg_overlay", 0),
          (overlay_set_alpha, ":agent_hp_overlay", 0),
          (overlay_set_alpha, ":agent_hp_bg_overlay", 0),
        (try_end),
        # (try_begin),
          # (gt, ":agent_name_overlay", 0),
          # (overlay_set_alpha, ":agent_name_overlay", 0),
        # (try_end),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_overlay_id, 0),
        (agent_set_slot, ":agent_no", slot_agent_hp_bar_bg_overlay_id, 0),
        #(agent_set_slot, ":agent_no", slot_agent_name_overlay_id, 0),
      (try_end),
    (try_end),
  ]),

  #("get_troop_backup_hp_times_factor",
    #[
      #(store_script_param, ":troop_no", 1),

      #(store_character_level, ":troop_level", ":troop_no"),
      #(store_mul, ":backup_hp_factor", ":troop_level", 4),
      #(assign, reg0, ":backup_hp_factor"),
    #]),

  #("get_agent_backup_hp_times_factor",
    #[
      #(store_script_param, ":agent_no", 1),

      #(agent_get_party_id, ":party_no", ":agent_no"),
      #(try_begin),
        #(le, ":party_no", -1),
        #(assign, ":backup_hp_factor", 0),
      #(else_try),
        #(party_stack_get_troop_id, ":leader", ":party_no", 0),
        #(troop_is_hero, ":leader"),
        #(store_skill_level, ":leadership_level", "skl_leadership", ":leader"),
        #(store_mul, ":backup_hp_factor", ":leadership_level", 6),
        #(try_begin),
          #(eq, ":party_no", "p_main_party"),
          #(agent_get_troop_id, ":troop_no", ":agent_no"),
          #(call_script, "script_game_get_morale_of_troops_from_faction", ":troop_no"),
          #(assign, ":troop_morale", reg0),
          #(val_clamp, ":troop_morale", 0, 100),
          #(val_mul, ":backup_hp_factor", ":troop_morale"),
          #(val_div, ":backup_hp_factor", 99),
        #(try_end),
      #(else_try),
        #(assign, ":backup_hp_factor", 0),
      #(try_end),
      #(assign, reg0, ":backup_hp_factor"),
    #]),
    #CC
 #Universal Sorting scripts
 #script_rearrange_inventory
#input: arg1 - troop_id, arg2 - sorting order; 0 - simple (compact inventory, removing spaces), 1 - by cost, 2 - by type.
#output : none
 ("rearrange_inventory",
  [(store_script_param, ":troop_id", 1),
   (store_script_param, ":type", 2),
   (troop_get_inventory_capacity, ":inv_cap", ":troop_id"),
   (try_begin),
     (eq, ":type", 0),
     (try_for_range, ":slot_no", 11, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop_id", ":slot_no"),
        (gt, ":item", 0),
        (troop_get_inventory_slot_modifier, ":mod", ":troop_id", ":slot_no"),
        (troop_inventory_slot_get_item_amount, ":amount", ":troop_id", ":slot_no"),
        (assign, ":target_slot", -1),
        (try_for_range_backwards, ":to_slot", 10, ":slot_no"),
          (troop_get_inventory_slot, ":is_full", ":troop_id", ":to_slot"),
          (le, ":is_full", 0),
          (assign, ":target_slot", ":to_slot"),
        (try_end),
        (neq, ":target_slot", -1),
        (troop_set_inventory_slot, ":troop_id", ":target_slot", ":item"),
        (troop_set_inventory_slot_modifier, ":troop_id", ":target_slot", ":mod"),
        (try_begin),
         (gt, ":amount", 0),
         (troop_inventory_slot_set_item_amount, ":troop_id", ":target_slot", ":amount"),
        (try_end),
        (troop_set_inventory_slot, ":troop_id", ":slot_no", -1),
        (troop_inventory_slot_set_item_amount, ":troop_id", ":slot_no", 0),
     (try_end),
    (else_try),
       (eq, ":type", 1),
       (troop_sort_inventory, ":troop_id"),
    (else_try),
       (eq, ":type", 2),
       (assign, ":temp_slot", 0),
#define sorting order
       (troop_set_slot, "trp_temp_array_a", 0, itp_type_one_handed_wpn),
       (troop_set_slot, "trp_temp_array_a", 1, itp_type_two_handed_wpn),
       (troop_set_slot, "trp_temp_array_a", 2, itp_type_polearm),
       (troop_set_slot, "trp_temp_array_a", 3, itp_type_bow),
       (troop_set_slot, "trp_temp_array_a", 4, itp_type_crossbow),
       (troop_set_slot, "trp_temp_array_a", 5, itp_type_thrown),
       (troop_set_slot, "trp_temp_array_a", 6, itp_type_arrows),
       (troop_set_slot, "trp_temp_array_a", 7, itp_type_bolts),
       (troop_set_slot, "trp_temp_array_a", 8, itp_type_shield),
       (troop_set_slot, "trp_temp_array_a", 9, itp_type_head_armor),
       (troop_set_slot, "trp_temp_array_a", 10, itp_type_body_armor),
       (troop_set_slot, "trp_temp_array_a", 11, itp_type_foot_armor),
       (troop_set_slot, "trp_temp_array_a", 12, itp_type_hand_armor),
       (troop_set_slot, "trp_temp_array_a", 13, itp_type_horse),
       (troop_set_slot, "trp_temp_array_a", 14, itp_type_goods),
       (troop_set_slot, "trp_temp_array_a", 15, itp_type_book),
       (troop_set_slot, "trp_temp_array_a", 16, itp_type_pistol),
       (troop_set_slot, "trp_temp_array_a", 17, itp_type_musket),
       (troop_set_slot, "trp_temp_array_a", 18, itp_type_bullets),
       (troop_set_slot, "trp_temp_array_a", 19, itp_type_animal),
#define sorting order
       (call_script, "script_clear_inventory", "trp_temp_array_a"),
       (troop_sort_inventory, ":troop_id"),
       (try_for_range, ":array_pos", 0, 20),
         (try_for_range, ":slot_no", 10, ":inv_cap"),
           (troop_get_inventory_slot, ":item", ":troop_id", ":slot_no"),
           (gt, ":item", 0),
           (item_get_type, ":item_type", ":item"),
           (troop_slot_eq, "trp_temp_array_a", ":array_pos", ":item_type"),
           (troop_inventory_slot_get_item_amount, ":amount", ":troop_id", ":slot_no"),
           (troop_get_inventory_slot_modifier, ":mod", ":troop_id", ":slot_no"),
           (troop_set_inventory_slot, "trp_temp_array_a", ":temp_slot", ":item"),
           (troop_set_inventory_slot_modifier, "trp_temp_array_a", ":temp_slot", ":mod"),
           (try_begin),
             (gt, ":amount", 0),
             (troop_inventory_slot_set_item_amount, "trp_temp_array_a", ":temp_slot", ":amount"),
           (try_end),
           (val_add, ":temp_slot", 1),
          (try_end),
       (try_end),
       (troop_clear_inventory, ":troop_id"),
       (try_for_range, ":slot_no", 0, ":inv_cap"),
            (troop_get_inventory_slot, ":item", "trp_temp_array_a", ":slot_no"),
            (troop_get_inventory_slot_modifier, ":mod", "trp_temp_array_a", ":slot_no"),
            (troop_inventory_slot_get_item_amount, ":amount", "trp_temp_array_a", ":slot_no"),
            (val_add, ":slot_no", 10),
            (troop_set_inventory_slot, ":troop_id", ":slot_no", ":item"),
            (troop_set_inventory_slot_modifier, ":troop_id", ":slot_no", ":mod"),
            (try_begin),
              (gt, ":amount", 0),
              (troop_inventory_slot_set_item_amount, ":troop_id", ":slot_no", ":amount"),
            (try_end),
            (try_begin),
              (le, ":item", 0),
              (assign, ":inv_cap", 0),
            (try_end),
         (try_end),
    (try_end),
   ]),
#script_clear_inventory
#INPUT: arg1 = troop_id
  ("clear_inventory",
   [(store_script_param_1, ":troop_id"),
    (troop_clear_inventory,":troop_id"),
    (try_for_range, ":item", 0, 10),
       (troop_set_inventory_slot, ":troop_id", ":item",  -1),
    (try_end),]),
 #End Universal Sorting scripts
  # Used to automatically buy and sell trade goods at a center
  #Input: center_no
  #Output: none
  ("auto_trade_at_center", [
    (store_script_param, ":center_no", 1),
    (try_begin),
      #For Towns:
      (is_between, ":center_no", towns_begin, towns_end),
      (try_begin),
        #Sell to non-trade good merchants first so player has plenty of cash and inventory space when dealing with goods merchant
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_weaponsmith),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_armorer),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_horse_merchant),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_merchant),
        (ge, ":merchant_troop", 1),
        #Player should be in a good position to buy after selling to other merchants
        (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
    (else_try),
      #For Villages:
      (is_between, ":center_no", villages_begin, villages_end),
      (party_get_slot, ":merchant_troop", ":center_no", slot_town_elder),
      (ge, ":merchant_troop", 1),
      #Villages tend to not have much coin, so we buy first to make sure they can afford the player's goods
      (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
      (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
    (try_end),
  ]),

  # script_auto_trade_sell_to_merchant
  # This may need to be changed to take a parameter for customer if ever used for anyone other than player
  # Buying and selling are split into separate scripts since there's no point trying to buy from armor/weapon/horse merchants
  # Input: :merchant_troop
  # Output: none
  ("auto_trade_sell_to_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_sold", 0),
    (assign, ":gold_gained", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (set_show_messages, 0),

    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":customer", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":customer", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      #Don't sell if player has disabled auto selling for this item
      (item_get_slot, ":sell_enabled", ":item", slot_item_auto_trade_sell_enabled),
      (gt, ":sell_enabled", 0),

      #Don't sell if the current amount is less than or equal to the player's minimum quantity
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (item_get_slot, ":min_qty", ":item", slot_item_auto_trade_min_quantity),
      (gt, ":item_count", ":min_qty"),

      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":sell_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score", 1),

      (item_get_slot, ":sell_price", ":item", slot_item_auto_trade_sell_over_price),
      (gt, ":score", ":sell_price"),

      (troop_set_inventory_slot, ":customer", ":i_slot", -1),
      (troop_add_gold, ":customer", ":score"),
      (call_script, "script_game_event_sell_item", ":item", 0),
      (val_add, ":items_sold", 1),
      (val_add, ":gold_gained", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_sold", 1),
      (assign, reg0, ":gold_gained"),
      (assign, reg1, ":items_sold"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You sold {reg1} {reg3?items:item} to {s0} and gained {reg0} {reg3?denars:denar}."),
    (try_end),
  ]),

  # script_auto_trade_buy_from_merchant
  # This may need to be changed to take a parameter for customer if ever used for anyone other than player
  # Input: :merchant_troop
  # Output: none
  ("auto_trade_buy_from_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_bought", 0),
    (assign, ":gold_spent", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      (store_free_inventory_capacity, ":free_inv_cap", ":customer"),
      (gt, ":free_inv_cap", 0),

      #Don't buy if player has disabled auto buying for this item
      (item_get_slot, ":buy_enabled", ":item", slot_item_auto_trade_buy_enabled),
      (gt, ":buy_enabled", 0),

      #Don't buy if the quantity would exceed player's max quantity
      #Since there is a separate option to enable/disable, a max quantity of 0 is treated as no max
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (assign, ":qty_valid", 1),
      (try_begin),
        (item_get_slot, ":max_qty", ":item", slot_item_auto_trade_max_quantity),
        (gt, ":max_qty", 0),
        (ge, ":item_count", ":max_qty"),
        (assign, ":qty_valid", 0),
      (try_end),
      (eq, ":qty_valid", 1),

      (call_script, "script_game_get_item_buy_price_factor", ":item"),
      (assign, ":buy_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":buy_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":customer_gold", ":customer"),
      (val_sub, ":customer_gold", "$g_auto_trade_minimum_wealth"),
      (ge, ":customer_gold", ":score"),

      (item_get_slot, ":buy_price", ":item", slot_item_auto_trade_buy_under_price),
      (lt, ":score", ":buy_price"),

      (troop_add_item, ":customer", ":item"),
      (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
      (troop_remove_gold, ":customer", ":score"),
      (troop_add_gold, ":merchant_troop", ":score"),
      (call_script, "script_game_event_buy_item", ":item", 0),
      (val_add, ":items_bought", 1),
      (val_add, ":gold_spent", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_bought", 1),
      (assign, reg0, ":gold_spent"),
      (assign, reg1, ":items_bought"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You bought {reg1} {reg3?items:item} from {s0} for {reg0} {reg3?denars:denar}."),
    (try_end),
  ]),
  #Autotrade end

("initialize_exchange_screen_extensions", [
	(store_script_param, ":troop_id", 1),

	(try_begin), #MASS PRISONER TRANSFER AFTER BATTLE
		(key_is_down, key_left_control), (key_is_down, key_a),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 10),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_temp_party"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_prisoner_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(ge, ":player_prisoner_capacity", ":stack_size"),
				(party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
			(else_try),	
				(party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_prisoner_capacity"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_prisoner_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_prisoners, "p_temp_party", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_prisoners, "p_temp_party", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ MASS TRANSFER OF RESCUED PRISONERS AFTER BATTLE
	(try_begin), 
		(key_is_down, key_left_control), (key_is_down, key_s),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 10),
		(party_get_num_companion_stacks, ":num_companion_stacks","p_temp_party"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(try_begin),
				(ge, ":player_companion_capacity", ":stack_size"),
				(party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
				(party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
			(else_try),	
				(party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_companion_capacity"),
				(val_add, ":stack_no_wounded", ":player_companion_capacity"),
				(store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
				(val_max, ":excess", 0),
				(party_wound_members, "p_main_party", ":stack_troop", ":excess"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_companion_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_members, "p_temp_party", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_members, "p_temp_party", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ SORTING GARRISONS
	(try_begin), #ARROW UP
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_up),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", 0), #key_up can't be used with stack 0
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(store_sub, ":key_stack_minus_one", ":key_stack", 1),
		(store_add, ":key_stack_plus_one", ":key_stack", 1),
		(try_for_range, ":stack_no", 0, ":key_stack_minus_one"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack_minus_one"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack_minus_one"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack_minus_one"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_for_range, ":stack_no", ":key_stack_plus_one", ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1), #restoring the balance in town
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #ARROW DOWN
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_down),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(store_add, ":key_stack_plus_one", ":key_stack", 1),
		(store_add, ":key_stack_plus_two", ":key_stack", 2),
		(try_for_range, ":stack_no", 0, ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack_plus_one"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack_plus_one"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack_plus_one"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(try_for_range, ":stack_no", ":key_stack_plus_two", ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #PAGE UP
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_page_up),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", 0), #key_page_up can't be used with stack 0
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(neq, ":stack_no", ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #PAGE DOWN
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_page_down),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(neq, ":stack_no", ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ MASSIVE TRANSFERS TO/FROM GARRISON
	(try_begin), #TROOPS FROM GARRISON TO PLAYER'S PARTY
		(key_is_down, key_right_control), (key_is_down, key_right),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_companion_stacks, ":num_companion_stacks","$current_town"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","$current_town",":stack_no"),
			(try_begin),
				(ge, ":player_companion_capacity", ":stack_size"),
				(party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
				(party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
			(else_try),	
				(party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_companion_capacity"),
				(val_add, ":stack_no_wounded", ":player_companion_capacity"),
				(store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
				(val_max, ":excess", 0),
				(party_wound_members, "p_main_party", ":stack_troop", ":excess"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_companion_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_members, "$current_town", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	
	(try_begin), #TROOPS FROM PLAYER'S PARTY TO GARRISON
		(key_is_down, key_right_control), (key_is_down, key_left),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_companion_stacks, ":num_companion_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_main_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_remove_members, "p_main_party", ":stack_troop", ":stack_size"),
		(try_end),
	(try_end),
	
	(try_begin), #PRISONERS FROM GARRISON TO PLAYER'S PARTY
		(key_is_down, key_left_control), (key_is_down, key_a),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","$current_town"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(ge, ":player_prisoner_capacity", ":stack_size"),
				(party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
			(else_try),	
				(party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_prisoner_capacity"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_prisoners, "$current_town", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_prisoners, "$current_town", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	
	(try_begin), #PRISONERS FROM PLAYER'S PARTY TO GARRISON
		(key_is_down, key_left_control), (key_is_down, key_d),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_add_prisoners, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_remove_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
		(try_end),
	(try_end),
    ]
  ),

]
