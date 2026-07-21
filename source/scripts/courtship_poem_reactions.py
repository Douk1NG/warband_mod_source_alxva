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

courtship_poem_reactions_scripts = [
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

	])
]
