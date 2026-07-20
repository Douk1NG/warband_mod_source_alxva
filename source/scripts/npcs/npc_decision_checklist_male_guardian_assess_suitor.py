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

npc_decision_checklist_male_guardian_assess_suitor_scripts = [
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

	])
]
