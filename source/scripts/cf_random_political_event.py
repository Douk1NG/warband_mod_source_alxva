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

cf_random_political_event_scripts = [
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



])
]
