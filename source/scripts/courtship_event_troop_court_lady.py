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

courtship_event_troop_court_lady_scripts = [
("courtship_event_troop_court_lady",
	[
	(store_script_param, ":suitor", 1),
	(store_script_param, ":lady", 2),


	#(try_begin),
	  #(eq, "$cheat_mode", 1),
	  #(str_store_troop_name, s4, ":suitor"),
	  #(str_store_troop_name, s5, ":lady"),
	  #(troop_get_slot, ":lady_location", ":lady", slot_troop_cur_center),
	  #(str_store_party_name, s7, ":lady_location"),
	  #(display_message, "str_s4_pursues_suit_with_s5_in_s7"),
	#(try_end),

	(troop_get_slot, ":previous_suitor", ":lady", slot_lady_last_suitor),
	(troop_set_slot, ":lady", slot_lady_last_suitor, ":suitor"), #can determine quarrels

	(try_begin),
		(eq, ":previous_suitor", "trp_player"),

		(troop_slot_ge, ":lady", slot_troop_met, 2),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", "trp_player"), #add this to list of quarrels
		(assign, ":suitor_relation_w_player", reg0),

		(try_begin),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
			(gt, ":suitor_relation_w_player", -20),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(else_try),
			(is_between, ":suitor_relation_w_player", -5, -25),
			(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", "trp_player", ":lady", 0),
		(try_end),
	(else_try),
		(neq, ":previous_suitor", "trp_player"), #not the player

		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),

		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":suitor", ":previous_suitor"),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),

		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),
	(else_try),	 #quarrelsome lords quarrel anyway
		(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),
		(neq, ":suitor", ":previous_suitor"),
		(ge, ":previous_suitor", active_npcs_begin),

#		(neq, ":previous_suitor", "trp_player"),

		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":previous_suitor"), #add this to list of quarrels
		(lt, reg0, 10),
		(call_script, "script_add_log_entry", logent_lords_quarrel_over_woman, ":suitor", ":previous_suitor", ":lady", 0),
		(ge, reg0, 0),
		(call_script, "script_troop_change_relation_with_troop", ":suitor", ":previous_suitor", -20),
		(val_add, "$total_courtship_quarrel_changes", -20),

	(try_end),


#	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
#	(assign, ":orig_relation", reg0),

    (call_script, "script_lady_evaluate_troop_as_suitor", ":lady", ":suitor"),

	(store_random_in_range, ":random", 5, 16),
	(store_div, ":relationship_change", reg0, ":random"),

	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":orig_relation", reg0),

	(call_script, "script_troop_change_relation_with_troop", ":lady", ":suitor", ":relationship_change"),

	(call_script, "script_troop_get_relation_with_troop", ":lady", ":suitor"),
	(assign, ":lady_suitor_relation", reg0),

	(try_begin),
		(ge, ":lady_suitor_relation", 10),
		(lt, ":orig_relation", 10),
		(call_script, "script_add_log_entry", logent_lady_favors_suitor, ":lady", 0, ":suitor", 0),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(display_message, "str_note__favor_event_logged"),
		(try_end),

	(else_try),
		(this_or_next|lt, ":lady_suitor_relation", -20),
			(ge, ":lady_suitor_relation", 20),

		(call_script, "script_get_kingdom_lady_social_determinants", ":lady"),
		(assign, ":guardian", reg0),
		(call_script, "script_troop_get_relation_with_troop", ":suitor", ":guardian"),
		(assign, ":suitor_guardian_relation", reg0),
		#things come to a head, one way or another

		(assign, ":highest_competitor_lady_score", -1),
		(assign, ":competitor_preferred_by_lady", -1),

		(assign, ":highest_competitor_guardian_score", ":suitor_guardian_relation"),
		(assign, ":competitor_preferred_by_guardian", -1),

		#log potential competitors
		(try_for_range, ":possible_competitor", lords_begin, lords_end),
			(neq, ":possible_competitor", ":suitor"),

			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_1, ":lady"),
			(this_or_next|troop_slot_eq, ":possible_competitor", slot_troop_love_interest_2, ":lady"),
				(troop_slot_eq, ":possible_competitor", slot_troop_love_interest_3, ":lady"),

			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":lady"),
				(gt, reg0, ":highest_competitor_lady_score"),
				(assign, ":competitor_preferred_by_lady", ":possible_competitor"),
				(assign, ":highest_competitor_lady_score", reg0),
			(try_end),

			(try_begin),
				(call_script, "script_troop_get_relation_with_troop", ":possible_competitor", ":guardian"),
				(gt, reg0, ":highest_competitor_guardian_score"),
				(assign, ":competitor_preferred_by_guardian", ":possible_competitor"),
				(assign, ":highest_competitor_guardian_score", reg0),
			(try_end),
		(try_end),

		#RESULTS
		#Guardian forces lady to be betrothed to suitor now
		(try_begin),
			(lt, ":lady_suitor_relation", -20),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_quarrelsome),
			(eq, ":competitor_preferred_by_guardian", -1),

			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_debauched),
				(troop_slot_eq, ":suitor", slot_lord_reputation_type, lrep_quarrelsome),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_family, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_forced_to_agree_to_engagement"),
			(try_end),

		#Lady rejects the suitor
		(else_try),
			(lt, ":lady_suitor_relation", -20),

			(call_script, "script_add_log_entry", logent_lady_rejects_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_lady_rejects_suitor"),
			(try_end),

		#A happy engagement, with parental blessing
		(else_try),
			(gt, ":lady_suitor_relation", 20),
			(gt, ":suitor_guardian_relation", 0),
			(eq, ":competitor_preferred_by_lady", -1),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_choice, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_happy_engagement_between_s4_and_s5"),
			(try_end),

		#Lady elopes
		(else_try),
			(gt, ":lady_suitor_relation", 20),

			(eq, ":competitor_preferred_by_lady", -1),
			##diplomacy start+
			##Fix Native bug, the following line should be checking ":lady", not ":guardian"
			##OLD:
			#(this_or_next|troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_adventurous),
			#	(troop_slot_eq, ":guardian", slot_lord_reputation_type, lrep_ambitious),
			##NEW:
			(this_or_next|troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_adventurous),
				(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_ambitious),
			##diplomacy end+

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			#lady elopes
			(call_script, "script_courtship_event_bride_marry_groom", ":lady", ":suitor", 1),
			#add elopements to quarrel descriptions

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_s4_elopes_with_s5"),
			(try_end),

		#Lady reluctantly agrees to marry under pressure from family
		(else_try),
			(troop_slot_eq, ":lady", slot_lord_reputation_type, lrep_conventional),
			(eq, ":competitor_preferred_by_guardian", -1),
			(gt, ":suitor_guardian_relation", 4),

			(store_random_in_range, ":random", 0, 5),
			(eq, ":random", 0),

			(troop_slot_eq, ":suitor", slot_troop_betrothed, -1),
			(troop_slot_eq, ":lady", slot_troop_betrothed, -1),

			(call_script, "script_add_log_entry", logent_lady_betrothed_to_suitor_by_pressure, ":lady", 0, ":suitor", 0),
			(troop_set_slot, ":suitor", slot_troop_betrothed, ":lady"),
			(troop_set_slot, ":lady", slot_troop_betrothed, ":suitor"),
			(store_current_hours, ":hours"),
			(troop_set_slot, ":lady", slot_troop_betrothal_time, ":hours"),
			(troop_set_slot, ":suitor", slot_troop_betrothal_time, ":hours"),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":lady"),
				(str_store_troop_name, s5, ":suitor"),
				(display_message, "str_result_s4_reluctantly_agrees_to_engagement_with_s5"),
			(try_end),

		#Stalemate -- make patience roll
		(else_try),
			(gt, ":lady_suitor_relation", 20),

			(store_random_in_range, reg3, 0, 3),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(display_message, "str_result_stalemate_patience_roll_=_reg3"),
			(try_end),

			(eq, reg3, 0),
			(call_script, "script_add_log_entry", logent_lady_rejected_by_suitor, ":lady", 0, ":suitor", 0),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":lady", ":suitor"),
		(try_end),

	(try_end),

	])
]
