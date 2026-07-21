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

get_political_quest_scripts = [
("get_political_quest",
  #Political quests are given by the player's political "coach" -- ie, a spouse or the minister -- to improve standing in the faction
  [
	(store_script_param, ":giver_troop", 1),

	(assign, ":result", -1),
	(assign, ":quest_target_troop", -1),
	(assign, ":quest_object_troop", -1),
	(assign, ":quest_dont_give_again_period", 7), #one week on average



	(try_begin), #this for kingdom hero, "we have a mutual enemy"
		(neg|check_quest_active, "qst_denounce_lord"),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(quest_get_slot, reg4, "qst_denounce_lord", slot_quest_dont_give_again_remaining_days),
			(display_message, "@{!}DEBUG -- Checking for denounce lord, eligible in {reg4} days"),
		(try_end),

		(neg|quest_slot_ge, "qst_denounce_lord", slot_quest_dont_give_again_remaining_days, 1),
		(neq, ":giver_troop", "$g_player_minister"),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":giver_troop"),
		(neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),


#		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_martial),
		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		(neg|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_goodnatured),

#		(neg|troop_slot_ge, "trp_player", slot_troop_controversy, 10),


		(assign, ":target_lord", -1),
		(assign, ":score_to_beat", 1),

		##diplomacy start+ support promoted ladies
		#(try_for_range, ":potential_target", active_npcs_begin, active_npcs_end),
		(try_for_range, ":potential_target", heroes_begin, heroes_end),
		   (this_or_next|is_between, ":potential_target", active_npcs_begin, active_npcs_end),
			   (troop_slot_eq, ":potential_target", slot_troop_occupation, slto_kingdom_hero),
            (neg|troop_slot_ge, ":potential_target", slot_troop_occupation, slto_retirement),
            ##diplomacy end+
			(store_faction_of_troop, ":potential_target_faction", ":potential_target"),
			(eq, ":potential_target_faction", "$players_kingdom"),
			(neq, ":potential_target", ":giver_troop"),
			(neg|faction_slot_eq, ":potential_target_faction", slot_faction_leader, ":potential_target"),

			#cannot denounce if you also have an intrigue against lord active
			(this_or_next|neg|check_quest_active, "qst_intrigue_against_lord"),
				(neg|quest_slot_eq, "qst_intrigue_against_lord", slot_quest_target_troop, ":potential_target"),

			(call_script, "script_troop_get_relation_with_troop", ":potential_target", ":giver_troop"),
			(assign, ":relation_with_giver_troop", reg0),
			(lt, ":relation_with_giver_troop", ":score_to_beat"),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(display_message, "@{!}DEBUG -- Rival found in {s4}"),
			(try_end),

			(try_begin),
				(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
				(assign, ":max_rel_w_player", 15),
			(else_try),
				##diplomacy start+
				(this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_ambitious),
				##diplomacy end+
				(troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
				(assign, ":max_rel_w_player", 10),
			(else_try),
				(assign, ":max_rel_w_player", 5),
			(try_end),

			(call_script, "script_troop_get_relation_with_troop", ":potential_target", "trp_player"),
			(assign, ":relation_with_player", reg0),
			(lt, ":relation_with_player", ":max_rel_w_player"),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(display_message, "@{!}DEBUG -- {s4} is not close friend of player"),
			(try_end),

			(assign, ":enemies_in_faction", 0),
			##diplomacy start+ support promoted ladies
			#(try_for_range, ":other_lord", active_npcs_begin, active_npcs_end),
			(try_for_range, ":other_lord", heroes_begin, heroes_end),
			   (this_or_next|is_between, ":other_lord", active_npcs_begin, active_npcs_end),
				   (troop_slot_eq, ":other_lord", slot_troop_occupation, slto_kingdom_hero),
            #do not scheme regarding dead/exiled lords
                (neg|troop_slot_ge, ":other_lord", slot_troop_occupation, slto_retirement),
                ##diplomacy end+
				(store_faction_of_troop, ":other_lord_faction", ":other_lord"),
				(eq, ":other_lord_faction", "$players_kingdom"),
				(call_script, "script_troop_get_relation_with_troop", ":potential_target", ":other_lord"),
				(lt, reg0, 0),
				(val_add, ":enemies_in_faction", 1),
			(try_end),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg3, ":enemies_in_faction"),
				(display_message, "@{!}DEBUG -- {s4} has {reg3} rivals"),
			(try_end),

			(this_or_next|ge, ":enemies_in_faction", 3),
				(ge, "$cheat_mode", 1),

			(assign, ":score_to_beat", ":relation_with_giver_troop"),
			(assign, ":target_lord", ":potential_target"),
		(try_end),

		##diplomacy start+ support promoted ladies
		#(is_between, ":target_lord", active_npcs_begin, active_npcs_end),
		(is_between, ":target_lord", heroes_begin, heroes_end),
		##diplomacy end+

		(assign, ":result", "qst_denounce_lord"),
		(assign, ":quest_target_troop", ":target_lord"),

	(else_try),
		(neg|check_quest_active, "qst_intrigue_against_lord"),
		(try_begin),
			(eq, "$cheat_mode", 1),
			(quest_get_slot, reg4, "qst_intrigue_against_lord", slot_quest_dont_give_again_remaining_days),
			(display_message, "@{!}DEBUG -- Checking for intrigue, eligible in {reg4} days"),
		(try_end),

		(neg|quest_slot_ge, "qst_intrigue_against_lord", slot_quest_dont_give_again_remaining_days, 1),



		(neq, ":giver_troop", "$g_player_minister"),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":giver_troop"),
		(neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG -- Trying for intrigue against lord"),
		(try_end),


		(assign, ":target_lord", -1),
		(assign, ":score_to_beat", 10),

		##diplomacy start+ Support promoted kingdom ladies
		#(try_for_range, ":potential_target", active_npcs_begin, active_npcs_end),
		(try_for_range, ":potential_target", heroes_begin, heroes_end),
		    (this_or_next|is_between, ":potential_target", active_npcs_begin, active_npcs_end),
		    (troop_slot_eq, ":potential_target", slot_troop_occupation, slto_kingdom_hero),
           #do not scheme regarding dead/exiled lords
            (neg|troop_slot_ge, ":potential_target", slot_troop_occupation, slto_retirement),
            ##diplomacy end+
			(store_faction_of_troop, ":potential_target_faction", ":potential_target"),
			(eq, ":potential_target_faction", "$players_kingdom"),
			(neq, ":potential_target", ":giver_troop"),
			(neg|faction_slot_eq, ":potential_target_faction", slot_faction_leader, ":potential_target"),


			(this_or_next|neg|check_quest_active, "qst_denounce_lord"),
				(neg|quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, ":potential_target"),

			(faction_get_slot, ":faction_liege", "$players_kingdom", slot_faction_leader),
			(call_script, "script_troop_get_relation_with_troop", ":potential_target", ":faction_liege"),
			(assign, ":relation_with_liege", reg0),
			(lt, ":relation_with_liege", ":score_to_beat"),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(display_message, "@{!}DEBUG -- {s4} has sufficiently low relation with liege"),
			(try_end),


			(call_script, "script_troop_get_relation_with_troop", ":potential_target", ":giver_troop"),
			(assign, ":relation_with_giver_troop", reg0),
			(lt, ":relation_with_giver_troop", 0),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(display_message, "@{!}DEBUG -- {s4} has sufficiently low relation with giver troop"),
			(try_end),


			(call_script, "script_troop_get_relation_with_troop", ":potential_target", "trp_player"),
			(assign, ":relation_with_player", reg0),
			(lt, ":relation_with_player", 0),

			(str_store_troop_name, s4, ":potential_target"),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(display_message, "@{!}DEBUG -- {s4} has sufficiently low relation with player"),
			(try_end),

			(assign, ":score_to_beat", ":relation_with_liege"),
			(assign, ":target_lord", ":potential_target"),
		(try_end),

		##diplomacy start+ support promoted ladies
		#(is_between, ":target_lord", active_npcs_begin, active_npcs_end),
		(is_between, ":target_lord", heroes_begin, heroes_end),
		##diplomacy end+

		(assign, ":result", "qst_intrigue_against_lord"),
		(assign, ":quest_target_troop", ":target_lord"),


	(else_try),
		#Resolve dispute, if there is a good chance of achieving the result
		(try_begin),
			(ge, "$cheat_mode", 1),
			(quest_get_slot, reg4, "qst_resolve_dispute", slot_quest_dont_give_again_remaining_days),
			(display_message, "@{!}DEBUG -- Checking for resolve dispute, eligible in {reg4} days"),
		(try_end),

		(neg|quest_slot_ge, "qst_resolve_dispute", slot_quest_dont_give_again_remaining_days, 1),


		##diplomacy start+
		#Add additional relative options
		##(call_script, "script_troop_get_family_relation_to_troop", "trp_player", ":giver_troop"),
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", "trp_player", ":giver_troop"),
		(this_or_next|ge, reg0, 4),
		##diplomacy end+
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_talk_troop"),
			(eq, "$g_talk_troop", "$g_player_minister"),

		(assign, ":target_lord", -1),
		(assign, ":object_lord", -1),
		(assign, ":best_chance_of_success", 20),

      ##diplomacy start+ support promoted ladies
		#(try_for_range, ":lord_1", active_npcs_begin, active_npcs_end),
      (try_for_range, ":lord_1", heroes_begin, heroes_end),
		   (this_or_next|is_between, ":lord_1", active_npcs_begin, active_npcs_end),
			   (troop_slot_eq, ":lord_1", slot_troop_occupation, slto_kingdom_hero),
         #do not use dead/exiled lords
            (neg|troop_slot_ge, ":lord_1", slot_troop_occupation, slto_retirement),
            ##diplomacy end+
			(store_faction_of_troop, ":lord_1_faction", ":lord_1"),
			(eq, ":lord_1_faction", "$players_kingdom"),
			(neq, ":lord_1", "$g_talk_troop"),

	      ##diplomacy start+ support promoted ladies
			#(try_for_range, ":lord_2", active_npcs_begin, active_npcs_end),
			(try_for_range, ":lord_2", heroes_begin, heroes_end),
			   (this_or_next|is_between, ":lord_2", active_npcs_begin, active_npcs_end),
				   (troop_slot_eq, ":lord_2", slot_troop_occupation, slto_kingdom_hero),
			   #do not use dead/exiled lords
                (neg|troop_slot_ge, ":lord_2", slot_troop_occupation, slto_retirement),
                ##diplomacy end+
				(store_faction_of_troop, ":lord_2_faction", ":lord_2"),
				(eq, ":lord_2_faction", "$players_kingdom"),

				(neq, ":lord_1", ":lord_2"),
				(neq, ":lord_2", "$g_talk_troop"),

				(call_script, "script_troop_get_relation_with_troop", ":lord_1", ":lord_2"),
				(assign, ":lord_1_relation_with_lord_2", reg0),
				(lt, ":lord_1_relation_with_lord_2", -5),

				(call_script, "script_troop_get_relation_with_troop", ":lord_1", "trp_player"),
				(assign, ":relation_with_lord_1", reg0),

				(call_script, "script_troop_get_relation_with_troop", ":lord_2", "trp_player"),
				(assign, ":relation_with_lord_2", reg0),

				(gt, ":relation_with_lord_1", 0),
				(gt, ":relation_with_lord_2", 0),

				(store_mul, ":chance_of_success", ":relation_with_lord_1", ":relation_with_lord_2"),


				(gt, ":chance_of_success", ":best_chance_of_success"),
				(assign, ":best_chance_of_success", ":chance_of_success"),
				(assign, ":target_lord", ":lord_1"),
				(assign, ":object_lord", ":lord_2"),
			(try_end),
		(try_end),

		##diplomacy start+ support promoted ladies
		#(is_between, ":target_lord", active_npcs_begin, active_npcs_end),
		(is_between, ":target_lord", heroes_begin, heroes_end),
		##diplomacy end+

		(assign, ":result", "qst_resolve_dispute"),
		(assign, ":quest_target_troop", ":target_lord"),
		(assign, ":quest_object_troop", ":object_lord"),

	(else_try),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(quest_get_slot, reg4, "qst_offer_gift", slot_quest_dont_give_again_remaining_days),
			(display_message, "@{!}DEBUG -- Checking for offer gift, eligible in {reg4} days"),
		(try_end),

		##diplomacy start+ conventional ladies have a quicker "reset" time on this quest
		(neg|quest_slot_ge, "qst_offer_gift", slot_quest_dont_give_again_remaining_days, 4),
        (this_or_next|troop_slot_eq, ":giver_troop", slot_lord_reputation_type, lrep_conventional),
		##diplomacy end+
		(neg|quest_slot_ge, "qst_offer_gift", slot_quest_dont_give_again_remaining_days, 1),

		(assign, ":relative_found", -1),
		(assign, ":score_to_beat", 5),
		##diplomacy start+
		#Slightly expand the range of potential targets if changes are enabled
		(try_begin),
         (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		   (assign, ":score_to_beat", 4),
		   (troop_slot_eq, ":giver_troop", slot_lord_reputation_type, lrep_conventional),
		   (assign, ":score_to_beat", 3),
	   (try_end),
		##diplomacy end+

		##diplomacy start+
		#(try_for_range, ":potential_relative", active_npcs_begin, active_npcs_end),
		#Add support for promoted ladies (TODO: add a variant for ordinary ladies as well)
		(try_for_range, ":potential_relative", heroes_begin, heroes_end),
			#do not use dead/exiled lords
			(this_or_next|is_between, ":potential_relative", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":potential_relative", slot_troop_occupation, slto_kingdom_hero),
         (neg|troop_slot_ge, ":potential_relative", slot_troop_occupation, slto_retirement),
        ##diplomacy end+
			(store_faction_of_troop, ":relative_faction", ":potential_relative"),
			(eq, ":relative_faction", "$players_kingdom"),
			(neq, ":potential_relative", ":giver_troop"),
			(neg|faction_slot_eq, ":relative_faction", slot_faction_leader, ":potential_relative"),

			(call_script, "script_troop_get_family_relation_to_troop", ":giver_troop", ":potential_relative"),
			(assign, ":family_relation", reg0),
			(ge, ":family_relation", ":score_to_beat"),

			(store_sub, ":min_relation_w_player", 0, ":family_relation"),

			(call_script, "script_troop_get_relation_with_troop", "trp_player", ":potential_relative"),
			(assign, ":relation_with_player", reg0),
			(is_between, ":relation_with_player", ":min_relation_w_player", 0),

			(assign, ":score_to_beat", ":family_relation"),
			(assign, ":relative_found", ":potential_relative"),

		(try_end),

		(is_between, ":relative_found", active_npcs_begin, active_npcs_end),

		(assign, ":result", "qst_offer_gift"),
		(assign, ":quest_target_troop", ":relative_found"),
	(try_end),


	(try_begin),
		(gt, ":result", -1),
		(quest_set_slot, ":result", slot_quest_target_troop, ":quest_target_troop"),
		(quest_set_slot, ":result", slot_quest_target_troop, ":quest_object_troop"),

		(quest_set_slot, ":result", slot_quest_giver_troop, ":giver_troop"),
        (quest_set_slot, ":result", slot_quest_dont_give_again_period, ":quest_dont_give_again_period"),
    (try_end),

    (assign, reg0, ":result"),
    (assign, reg1, ":quest_target_troop"),
    (assign, reg2, ":quest_object_troop"),

  ])
]
