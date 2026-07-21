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

cf_test_lord_incompatibility_to_s17_scripts = [
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

	])
]
