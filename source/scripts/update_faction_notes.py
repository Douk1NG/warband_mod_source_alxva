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

update_faction_notes_scripts = [
#script_agent_reassign_team
# INPUT: faction_no
# OUTPUT: none
("update_faction_notes",
    [
      (store_script_param, ":faction_no", 1),

      (try_begin),
        (this_or_next|faction_slot_eq, ":faction_no", slot_faction_state, sfs_inactive),
        (eq, ":faction_no", "fac_player_faction"),
        (faction_set_note_available, ":faction_no", 0),
      (else_try),
        (faction_set_note_available, ":faction_no", 1),
      (try_end),
##
##	(try_begin),
##		(eq, 2, 1),
##		(str_store_faction_name, s14, ":faction_no"),
##		(assign, reg4, "$temp"),
##		(display_message, "str_updating_faction_notes_for_s14_temp_=_reg4"),
##	(try_end),
##
##    (try_begin),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
##       (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
##       (str_store_faction_name, s5, ":faction_no"),
##       (str_store_troop_name_link, s6, ":faction_leader"),
##       (assign, ":num_centers", 0),
##       (str_store_string, s8, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (store_faction_of_party, ":center_faction", ":cur_center"),
##         (eq, ":center_faction", ":faction_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s8, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":cur_center"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (assign, ":num_members", 0),
##       (str_store_string, s10, "@noone"),
##       (try_for_range_backwards, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
##         (assign, ":cur_troop", ":loop_var"),
##         (try_begin),
##           (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
##           (assign, ":cur_troop", "trp_player"),
##           (assign, ":troop_faction", "$players_kingdom"),
##         (else_try),
##           (store_troop_faction, ":troop_faction", ":cur_troop"),
##         (try_end),
##         (eq, ":troop_faction", ":faction_no"),
##         (neq, ":cur_troop", ":faction_leader"),
##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##         (try_begin),
##           (eq, ":num_members", 0),
##           (str_store_troop_name_link, s10, ":cur_troop"),
##         (else_try),
##           (eq, ":num_members", 1),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{s9} and {s10}"),
##         (else_try),
##           (str_store_troop_name_link, s9, ":cur_troop"),
##           (str_store_string, s10, "@{!}{s9}, {s10}"),
##         (try_end),
##         (val_add, ":num_members", 1),
##       (try_end),
##
##	   #wars
##       (str_store_string, s12, "@noone"),
###       (assign, ":num_enemies", 0),
###       (try_for_range_backwards, ":cur_faction", kingdoms_begin, kingdoms_end),
###         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
###         (store_relation, ":cur_relation", ":cur_faction", ":faction_no"),
###         (lt, ":cur_relation", 0),
###         (try_begin),
###           (eq, ":num_enemies", 0),
###           (str_store_faction_name_link, s12, ":cur_faction"),
###         (else_try),
###           (eq, ":num_enemies", 1),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11} and the {s12}"),
###         (else_try),
###           (str_store_faction_name_link, s11, ":cur_faction"),
###           (str_store_string, s12, "@the {s11}, the {s12}"),
###         (try_end),
###         (val_add, ":num_enemies", 1),
###       (try_end),
##
##       (str_store_string, s21, "str_foreign_relations__"),
##
##	   #other foreign relations
##       (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
##         (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
##		 (neq, ":faction_no", ":cur_faction"),
##		 (str_store_faction_name_link, s14, ":cur_faction"),
##         (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_no", ":cur_faction"),
##		 (assign, ":diplomatic_status", reg0),
##		 (assign, reg2, reg1), #length of events
##		 (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":cur_faction", ":faction_no"),
##		 (assign, ":reverse_diplomatic_status", reg0),
##
##
##		 (try_begin),
##			(eq, ":diplomatic_status", -2),
##			(str_store_string, s21, "str_s21__the_s5_is_at_war_with_the_s14"),
##
##			(store_add, ":slot_war_damage_inflicted", ":cur_faction", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_inflicted", kingdoms_begin),
##			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":slot_war_damage_inflicted"),
##			(store_mul, ":war_damage_inflicted_x_2", ":war_damage_inflicted", 2),
##
##			(store_add, ":slot_war_damage_suffered", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
##			(val_sub, ":slot_war_damage_suffered", kingdoms_begin),
##			(faction_get_slot, ":war_damage_suffered", ":cur_faction", ":slot_war_damage_suffered"),
##			(store_mul, ":war_damage_suffered_x_2", ":war_damage_suffered", 2),
##
##			(try_begin),
##				(gt, ":war_damage_inflicted", ":war_damage_suffered_x_2"),
##				(str_store_string, s21, "str_s21_the_s5_has_had_the_upper_hand_in_the_fighting"),
##			(else_try),
##				(gt, ":war_damage_suffered", ":war_damage_inflicted_x_2"),
##				(str_store_string, s21, "@{s21}. The {s14} has gotten the worst of the fighting."),
##			(else_try),
##				(gt, ":war_damage_inflicted", 100),
##				(gt, ":war_damage_inflicted", 100),
##				(str_store_string, s21, "str_s21_the_fighting_has_gone_on_for_some_time_and_the_war_may_end_soon_with_a_truce"),
##			(else_try),
##				(str_store_string, s21, "str_s21_the_fighting_has_begun_relatively_recently_and_the_war_may_continue_for_some_time"),
##			(try_end),
##
##			(try_begin),
##				(eq, "$cheat_mode", 1),
##				(assign, reg4, ":war_damage_inflicted"),
##				(assign, reg5, ":war_damage_suffered"),
##				(str_store_string, s21, "str_s21_reg4reg5"),
##			(try_end),
##		 (else_try),
##			(eq, ":diplomatic_status", 1),
##			(str_clear, s18),
##
##			(try_begin),
##				(neq, reg0, 1),
##				(str_store_string, s18, "str__however_the_truce_is_no_longer_binding_on_the_s14"),
##			(try_end),
##			(str_store_string, s21, "str_s21__the_s5_is_bound_by_truce_not_to_attack_the_s14s18_the_truce_will_expire_in_reg1_days"),
##
##		 (else_try),
##			(eq, ":diplomatic_status", -1),
##			(str_store_string, s21, "str_s21__the_s5_has_recently_suffered_provocation_by_subjects_of_the_s14_and_there_is_a_risk_of_war"),
##		 (else_try),
##			(eq, ":diplomatic_status", 0),
##			(str_store_string, s21, "str_s21__the_s5_has_no_outstanding_issues_with_the_s14"),
##		 (try_end),
##
##
##		 (try_begin),
##			(eq, ":reverse_diplomatic_status", -1),
##			(str_store_string, s21, "str_s21_the_s14_was_recently_provoked_by_subjects_of_the_s5_and_there_is_a_risk_of_war_"),
##		 (try_end),
##
##		 (try_begin),
##			(eq, "$cheat_mode", 1),
##			(call_script, "script_diplomacy_faction_assess_faction_to_s14", ":faction_no", ":cur_faction", -1),
##			(str_store_string, s21, "str_s21_cheat_mode_assessment_s14_"),
##	     (try_end),
##	  (try_end),
##
##
##	  (add_faction_note_from_sreg, ":faction_no", 0, "str_the_s5_is_ruled_by_s6_it_occupies_s8_its_vassals_are_s10__s21", 0),
##
##
##
##    (else_try),
##       (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
##       (faction_slot_eq, ":faction_no", slot_faction_state, sfs_defeated),
##       (str_store_faction_name, s5, ":faction_no"),
##       (add_faction_note_from_sreg, ":faction_no", 0, "@{s5} has been defeated!", 0),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (else_try),
##       (str_clear, s1),
##       (add_faction_note_from_sreg, ":faction_no", 0, s1, 0),
##       (add_faction_note_from_sreg, ":faction_no", 1, s1, 0),
##    (try_end),
##
##    (try_begin),
##       (is_between, ":faction_no", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh"),
##    (else_try),
##       (add_faction_note_tableau_mesh, ":faction_no", "tableau_faction_note_mesh_banner"),
##    (try_end),
     ])
]
