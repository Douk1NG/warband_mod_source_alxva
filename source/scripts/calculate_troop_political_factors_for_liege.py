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

calculate_troop_political_factors_for_liege_scripts = [
("calculate_troop_political_factors_for_liege",
    [
	(store_script_param, ":troop", 1),
	(store_script_param, ":liege", 2),

	(troop_get_slot, ":lord_reputation", ":troop", slot_lord_reputation_type),

	##diplomacy start+ Work correctly in certain situations where this can be called w/o a liege.
	##OLD:
	#(store_faction_of_troop, ":faction", ":liege"),
	##NEW:
	(try_begin),
	   (eq, ":liege", "trp_player"),
	   (assign, ":faction", "fac_player_supporters_faction"),
	   (try_begin),
	     #Handle "player is co-ruler of NPC faction"
	     (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
	     (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	     (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
	     (assign, ":faction", "$players_kingdom"),
	     (faction_get_slot, reg0, ":faction", slot_faction_leader),
	     (gt, reg0, 0),
	     (assign, ":liege", reg0),
	   (try_end),
	(else_try),
	   #Ordinary case
	   (ge, ":liege", 0),
	   (store_faction_of_troop, ":faction", ":liege"),
	(else_try),
	   (store_faction_of_troop, reg0, ":troop"),
	   (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	   (assign, ":faction", reg0),
	(else_try),
	   (assign, ":faction", kingdoms_end),
	   (try_for_range, reg0, kingdoms_begin, ":faction"),
	      (faction_slot_eq, reg0, slot_faction_leader, ":liege"),
	      (assign, ":faction", reg0),
	   (try_end),
	   (neg|is_between, ":faction", kingdoms_begin, kingdoms_end),
	   (assign, ":faction", "fac_no_faction"),
	(try_end),
	##diplomacy end+


	(try_begin),
		(eq, ":faction", "fac_player_faction"),
		(assign, ":faction", "fac_player_supporters_faction"),
	(try_end),

	(assign, ":liege_is_undeclared_rebel", 0),
	(try_begin),
		(neg|faction_slot_eq, ":faction", slot_faction_leader, ":liege"),
		#the liege is a rebel
		(assign, ":liege_is_undeclared_rebel", 1),
		(try_begin),
			(eq, "$cheat_mode", 1),
                        ##diplomacy start+ Guard against bad liege
                        (ge, ":liege", 0),
                        ##diplomacy end+
			(str_store_troop_name, s32, ":liege"),
			(display_message, "str_s32_is_undeclared_rebel"),
		(try_end),
	(try_end),

	(assign, ":result_for_material", 0),
	(assign, ":penalty_for_changing_sides", 0),



	#FACTOR 1 - MILITARY SECURITY
	(assign, ":result_for_security", 0),

	#find the lord's home
	(assign, ":base_center", -1),
	(try_begin),
		##diplomacy start+ add support for promoted kingdom ladies
		(is_between, ":troop", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":troop", active_npcs_begin, active_npcs_end),
		(try_for_range, ":center", centers_begin, centers_end),
			(eq, ":base_center", -1),
			(party_slot_eq, ":center", slot_town_lord, ":troop"),
			(assign, ":base_center", ":center"),
		(try_end),
	(try_end),

	(assign, ":faction_has_base", 0),

	#add up all other centers for the security value
	(try_for_range, ":center", centers_begin, centers_end),
		(neq, ":center", ":base_center"),
		(gt, ":base_center", 0),

		(try_begin),
			(is_between, ":center", towns_begin, towns_end),
			(assign, ":weight", 9000),
		(else_try),
			(is_between, ":center", castles_begin, castles_end),
			(assign, ":weight", 6000),
		(else_try),
			(assign, ":weight", 1000),
		(try_end),

		(store_distance_to_party_from_party, ":distance", ":base_center", ":center"),
		(val_add, ":distance", 10),
		(val_div, ":weight", ":distance"),
		(val_div, ":weight", ":distance"),

		(store_faction_of_party, ":center_faction", ":center"),

		(try_begin),
			(eq, ":center_faction", ":faction"),

			(assign, ":faction_has_base", 1),
			(val_add, ":result_for_security", ":weight"),
		(else_try),
			(neq, ":center_faction", ":faction"),
			(store_relation, ":center_relation", ":center_faction", ":faction"),

			(try_begin), #potentially hostile center
				(this_or_next|eq, ":liege_is_undeclared_rebel", 1),
					(lt, ":center_relation", 0),
				(val_div, ":weight", 2),
			(else_try), #neutral center
				(val_div, ":weight", 4),
			(try_end),

			(val_sub, ":result_for_security", ":weight"),
		(try_end),
	(try_end),


	#if a faction controls no other centers, then there is a small bonus
	(try_begin),
		(eq, ":faction_has_base", 0),
		(val_add, ":result_for_security", 20),
		(try_begin),
			(eq, "$cheat_mode", 2),
			(display_message, "str_small_bonus_for_no_base"),
		(try_end),
	(try_end),
	(val_clamp, ":result_for_security", -100, 100),


	(assign, ":result_for_security_weighted", ":result_for_security"),
	##diplomacy start+
   #ADDED TO THIS, SEE BELOW
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_cunning),
	#	(val_mul, ":result_for_security_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_martial),
	#	(val_div, ":result_for_security_weighted", 2),
	#(try_end),
	#
    ##Use companion morality type "tmt_aristocratic" as a synonym/antonym for bold
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_aristocratic),
	(assign, ":lord_tmt_aristocratic", reg0),
	(try_begin),
		(lt, ":lord_tmt_aristocratic", 1),
		(this_or_next|lt, ":lord_tmt_aristocratic", 0),
		(eq, ":lord_reputation", lrep_cunning),
		(val_mul, ":result_for_security_weighted", 2),
	(else_try),
		(ge, ":lord_tmt_aristocratic", 0),
		(this_or_next|ge, ":lord_tmt_aristocratic", 1),
		(eq, ":lord_reputation", lrep_martial),
		(val_div, ":result_for_security_weighted", 2),
	(try_end),
	##diplomacy end+

	#FACTOR 2 - INTERNAL FACTION POLITICS
	#this is a calculation of how much influence the lord believes he will have in each faction
	(assign, ":result_for_political", 0),

    (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
        (assign, ":kingdom_hero", ":loop_var"),
	##diplomacy start+ Skip what follows when there is no liege
	(ge, ":liege", 0),
	##diplomacy end+

		(this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|eq, ":kingdom_hero", "trp_kingdom_heroes_including_player_begin"),
			(is_between, ":kingdom_hero", pretenders_begin, pretenders_end),

		(store_faction_of_troop, ":kingdom_hero_faction", ":kingdom_hero"),

        (try_begin),
            (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
            (assign, ":kingdom_hero", "trp_player"),
			(assign, ":kingdom_hero_faction", "$players_kingdom"),
			(try_begin), #do not count player relation if the player is trying to suborn the character. this has the slight potential for a miscalculation, if the script is called from outside dialogs and $g_talk_troop has not been reset
				(eq, "$g_talk_troop", ":troop"),
				(store_faction_of_troop, ":cur_faction", ":troop"),
				(eq, ":cur_faction", ":faction"),
				(assign, ":kingdom_hero_faction", 0),
			(try_end),
		(try_end),

		(eq, ":kingdom_hero_faction", ":faction"),
		(neg|faction_slot_eq, ":kingdom_hero_faction", slot_faction_leader, ":kingdom_hero"),
		(neq, ":liege_is_undeclared_rebel", 1),
		(neg|is_between, ":kingdom_hero", pretenders_begin, pretenders_end),


		(call_script, "script_troop_get_relation_with_troop", ":troop", ":kingdom_hero"),
		(assign, ":troop_rel_w_hero", reg0),

		(call_script, "script_troop_get_relation_with_troop", ":kingdom_hero", ":liege"),
		(assign, ":hero_rel_w_liege", reg0),

		(store_mul, ":lord_political_weight", ":troop_rel_w_hero", ":hero_rel_w_liege"),
		(val_div, ":lord_political_weight", 100),

		(try_begin),
			(eq, "$cheat_mode", 2), #disabled
			(eq, "$g_talk_troop", ":troop"),
			(str_store_faction_name, s20, ":kingdom_hero_faction"),
			(str_store_troop_name, s15, ":kingdom_hero"),
			(assign, reg15, ":lord_political_weight"),
			(display_message, "str_s15_considered_member_of_faction_s20_weight_of_reg15"),
		(try_end),

		(val_add, ":result_for_political", ":lord_political_weight"),
	(try_end),

	(val_clamp, ":result_for_political", -100, 101), #lords portion represents half

	(try_begin),
		##diplomacy start+ When there isn't a liege, use 0
		(assign, ":liege_relation", 0),
		(ge, ":liege", 0),
		##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":troop", ":liege"),
		(assign, ":liege_relation", reg0),
		(val_add, ":result_for_political", ":liege_relation"),
	(try_end),

	(val_div, ":result_for_political", 2),

	(val_clamp, ":result_for_political", -100, 101), #liege portion represents half

	(assign, ":result_for_political_weighted", ":result_for_political"),

	(try_begin),
		(this_or_next|eq, ":lord_reputation", lrep_goodnatured),
			(eq, ":lord_reputation", lrep_quarrelsome),
		(val_mul, ":result_for_political_weighted", 2),
	(try_end),

	#FACTOR 3 - PROMISES AND OTHER ANTICIPATED GAINS
	#lord's calculation of anticipated gains
	(assign, ":result_for_material", 0),
	(assign, ":result_for_material_weighted", ":result_for_material"),


	#FACTOR 4 - IDEOLOGY
	#lord's calculation of ideological comfort
	(try_begin),
		#Originally, the argument section was not used for a non-player liege. Actually, it can be used
		(eq, 1, 0),
		(neq, ":liege", "trp_player"),
		(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
		(assign, ":argument_strength", 0),
		(assign, ":argument_appeal", 0),
		(assign, ":result_for_argument", 0),
	(else_try),	#only if the recruitment candidate is either the player, or a supported pretender
		(troop_get_slot, ":recruitment_argument", ":troop", slot_lord_recruitment_argument),

		(call_script, "script_rebellion_arguments", ":troop", ":recruitment_argument", ":liege"),
		(assign, ":argument_appeal", reg0),
		(assign, ":argument_strength", reg1),

		(store_add, ":result_for_argument", ":argument_appeal", ":argument_strength"),

		(store_skill_level, ":player_persuasion_skill", "skl_persuasion", "trp_player"),
		(try_begin),
			(gt, ":result_for_argument", 0),
			#make sure player is the one making the overture

			#if player has 0 persuasion, ":result_for_argument" will be multiplied by 3/10.
			(store_add, ":player_persuasion_skill_plus_5_mul_066", ":player_persuasion_skill", 5),
			(val_mul, ":player_persuasion_skill_plus_5_mul_066", 2),
			(val_div, ":player_persuasion_skill_plus_5_mul_066", 3),

			(val_mul, ":result_for_argument", ":player_persuasion_skill_plus_5_mul_066"),
			(val_div, ":result_for_argument", 10),
		(else_try),
			(lt, ":result_for_argument", 0),
			(store_sub, ":ten_minus_player_persuasion_skill", 10, ":player_persuasion_skill"),
			(val_mul, ":result_for_argument", ":ten_minus_player_persuasion_skill"),
			(val_div, ":result_for_argument", 10),
		(try_end),

		(try_begin),
			(neq, ":liege", "trp_player"),
			(neq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(val_div, ":argument_strength", 2),
			(val_div, ":argument_appeal", 2),
			(val_div, ":result_for_argument", 2),
		(try_end),

	(try_end),

#	(try_begin),
#		(eq, ":lord_reputation", lrep_cunning),
#		(val_div, ":result_for_ideological_weighted", 2),
#	(else_try),
#		(eq, ":lord_reputation", lrep_upstanding),
#		(val_mul, ":result_for_ideological_weighted", 2),
#	(try_end),


	#FACTOR 5 - PENALTY FOR CHANGING SIDES
	(try_begin), #no penalty for the incumbent
		(store_faction_of_troop, ":cur_faction", ":troop"),
		(eq, ":cur_faction", ":faction"),
		(assign, ":penalty_for_changing_sides", 0),
	(else_try), #penalty for the player
		(eq, ":liege", "trp_player"),
		(store_sub, ":penalty_for_changing_sides", 60, "$player_right_to_rule"),
	(else_try), #same culture, such as a pretender
		##diplomacy start+ skip when there is no liege
		(ge, ":liege", 0),
		##diplomacy end+
		(troop_get_slot, ":orig_faction_of_lord", ":troop", slot_troop_original_faction),
		(troop_get_slot, ":orig_faction_of_liege", ":liege", slot_troop_original_faction),
		(eq, ":orig_faction_of_lord", ":orig_faction_of_liege"),
		(assign, ":penalty_for_changing_sides", 10),
	##diplomacy start+
	#"same culture, such as a pretender" pt. 2
	(else_try),
		(troop_slot_eq, ":troop", slot_troop_original_faction, ":faction"),
		(assign, ":penalty_for_changing_sides", 10),
	##diplomacy end+
	(else_try), #a liege from a different culture
		(assign, ":penalty_for_changing_sides", 50),
	(try_end),
	(val_clamp, ":penalty_for_changing_sides", 0, 101),

	(assign, ":penalty_for_changing_sides_weighted", ":penalty_for_changing_sides"),
	##diplomacy start+
	#(try_begin),
	#	(eq, ":lord_reputation", lrep_debauched),
	#	(val_div, ":penalty_for_changing_sides_weighted", 2),
	#(else_try),
	#	(eq, ":lord_reputation", lrep_upstanding),
	#	(val_mul, ":penalty_for_changing_sides_weighted", 2),
	#(try_end),
	#
	##Use companion morality type "tmt_honest" as a synonym/antonym for deal-keeping
	(call_script, "script_dplmc_get_troop_morality_value", ":troop", tmt_honest),
	(assign, ":lord_tmt_honest", reg0),
	(try_begin),
		(this_or_next|lt, ":lord_tmt_honest", 0),
		(eq, ":lord_reputation", lrep_debauched),
		(val_div, ":penalty_for_changing_sides_weighted", 2),
	(else_try),
		(this_or_next|ge, ":lord_tmt_honest", 1),
		(eq, ":lord_reputation", lrep_upstanding),
		(val_mul, ":penalty_for_changing_sides_weighted", 2),
	(try_end),
	##diplomacy end+



	(assign, reg1, ":result_for_security"),
	(assign, reg2, ":result_for_security_weighted"),
	(assign, reg3, ":result_for_political"),
	(assign, reg4, ":result_for_political_weighted"),
	(assign, reg5, ":result_for_material"),
	(assign, reg6, ":result_for_material_weighted"),
	(assign, reg7, ":argument_strength"),
	(assign, reg17, ":argument_appeal"),

	(assign, reg8, ":result_for_argument"),
	(assign, reg9, ":penalty_for_changing_sides"),
	(assign, reg10, ":penalty_for_changing_sides_weighted"),


	(try_begin),
		(eq, "$cheat_mode", 1),
		(eq, "$g_talk_troop", ":troop"),
		(str_store_troop_name, s20, ":troop"),
		(str_store_faction_name, s21, ":faction"),
		##diplomacy start+
		##OLD:
		#(str_store_troop_name, s22, ":liege"),
		##NEW:
		(try_begin),
		  (gt, ":liege", -1),
		  (str_store_troop_name, s22, ":liege"),
		(else_try),
		  (str_store_string, s22, "str_noone"),
		(try_end),
		##diplomacy end+

		(display_message, "@{!}G_talk_troop {s20} evaluates being vassal to {s22} of {s21}"),

		(display_message, "str_base_result_for_security_reg1"),
		(display_message, "str_result_for_security_weighted_by_personality_reg2"),
		(display_message, "str_base_result_for_political_connections_reg3"),
		(display_message, "str_result_for_political_connections_weighted_by_personality_reg4"),
#		(display_message, "@{!}Result for anticipated_gains: {reg5}"),
#		(display_message, "@{!}Result for anticipated_gains weighted by personality: {reg6}"),

		(try_begin),
			(this_or_next|eq, ":liege", "trp_player"),
				(eq, ":liege", "$supported_pretender"), #player is advocate for pretender
			(display_message, "str_result_for_argument_strength_reg7"),
			(display_message, "str_result_for_argument_appeal_reg17"),
			(display_message, "str_combined_result_for_argument_modified_by_persuasion_reg8"),
		(try_end),
		(display_message, "str_base_changing_sides_penalty_reg9"),
		(display_message, "str_changing_sides_penalty_weighted_by_personality_reg10"),
	(try_end),

	(store_add, ":total", ":result_for_security_weighted", ":result_for_political_weighted"),
	(val_add, ":total", ":result_for_material_weighted"),
	(val_add, ":total", ":result_for_argument"),
	(val_sub, ":total", ":penalty_for_changing_sides_weighted"),


	(assign, reg0, ":total"),

	(try_begin),
		(eq, "$cheat_mode", 2),
		(display_message, "@{!}DEBUG -- Analyzing lord allegiances, combined bonuses and penalties = {reg0}"),
		#(display_message, "str_combined_bonuses_and_penalties_=_reg0"),
	(try_end),
	])
]
