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

rebellion_scripts = [

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

("change_troop_intrigue_impatience", [
        (store_script_param_1, ":troop_no"),
        (store_script_param_2, ":amount"),
        (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
        (val_max, ":impatience", ":amount"),
        (troop_set_slot, ":troop_no", slot_troop_intrigue_impatience, ":impatience"),
    ]),
]