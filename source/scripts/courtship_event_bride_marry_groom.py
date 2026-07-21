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

courtship_event_bride_marry_groom_scripts = [
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
	])
]
