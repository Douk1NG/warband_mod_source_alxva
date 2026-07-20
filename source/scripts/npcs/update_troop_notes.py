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

update_troop_notes_scripts = [
("update_troop_notes",
    [
##      (store_script_param, ":troop_no", 1),
##     (str_store_troop_name, s54, ":troop_no"),
##     (try_begin),
##       (eq, ":troop_no", "trp_player"),
##       (this_or_next|eq, "$player_has_homage", 1),
##		(eq, "$players_kingdom", "fac_player_supporters_faction"),
##       (assign, ":troop_faction", "$players_kingdom"),
##     (else_try),
##       (store_troop_faction, ":troop_faction", ":troop_no"),
##     (try_end),
##
##	 (str_clear, s49),
##	 (try_begin),
##		(is_between, ":troop_no", lords_begin, kingdom_ladies_end),
##		(troop_get_slot, reg1, ":troop_no", slot_troop_age),
##		(str_store_string, s49, "str__age_reg1_family_"),
##
##		(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
##			(call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
##			(gt, reg0, 0),
##
##			(try_begin),
##				(neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
##				(str_store_troop_name_link, s12, ":aristocrat"),
##				(call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
##				(str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
##			(else_try),
##				(str_store_troop_name, s12, ":aristocrat"),
##				(str_store_string, s49, "str_s49_s12_s11"),
##			(try_end),
##
##		(try_end),
##	 (try_end),
##
##     (try_begin),
##       (neq, ":troop_no", "trp_player"),
##       (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
##       (str_clear, s54),
##       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
###     (else_try),
###       (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
###       (str_clear, s54),
###       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##     (else_try),
##       (is_between, ":troop_no", pretenders_begin, pretenders_end),
##       (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##       (neq, ":troop_no", "$supported_pretender"),
##       (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
##       (try_begin),
##         (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
##         (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
##         (str_store_faction_name_link, s56, ":orig_faction"),
##         (add_troop_note_from_sreg, ":troop_no", 0, "@{s54} is a claimant to the throne of {s56}.", 0),
##         (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##       (else_try),
##         (str_clear, s54),
##         (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##       (try_end),
##     (else_try),
##       (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
##       (str_store_troop_name_link, s55, ":faction_leader"),
##       (str_store_faction_name_link, s56, ":troop_faction"),
##       (assign, ":troop_is_player_faction", 0),
##       (assign, ":troop_is_faction_leader", 0),
##       (try_begin),
##         (eq, ":troop_faction", "fac_player_faction"),
##         (assign, ":troop_is_player_faction", 1),
##       (else_try),
##         (eq, ":faction_leader", ":troop_no"),
##         (assign, ":troop_is_faction_leader", 1),
##       (try_end),
##       (assign, ":num_centers", 0),
##       (str_store_string, s58, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s58, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{s57} and {s58}"),
##         (else_try),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{!}{s57}, {s58}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (troop_get_type, reg3, ":troop_no"),
##       (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##       (str_clear, s59),
##       (try_begin),
###         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
##         (call_script, "script_troop_get_player_relation", ":troop_no"),
##         (assign, ":relation", reg0),
##         (store_add, ":normalized_relation", ":relation", 100),
##         (val_add, ":normalized_relation", 5),
##         (store_div, ":str_offset", ":normalized_relation", 10),
##         (val_clamp, ":str_offset", 0, 20),
##         (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
##         (neq, ":str_id", "str_relation_plus_0_ns"),
##         (str_store_string, s60, "@{reg3?She:He}"),
##         (str_store_string, s59, ":str_id"),
##         (str_store_string, s59, "@{!}^{s59}"),
##       (try_end),
##
##	#lord recruitment changes begin
##	#This sends a bunch of political information to s47.
##
##
##
##
##	    #refresh registers
##        (assign, reg9, ":num_centers"),
##        (troop_get_type, reg3, ":troop_no"),
##        (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##		(assign, reg4, ":troop_is_faction_leader"),
##		(assign, reg6, ":troop_is_player_faction"),
##
##        (add_troop_note_from_sreg, ":troop_no", 0, "str_reg6reg4s54_is_the_ruler_of_s56_s54_is_a_vassal_of_s55_of_s56_renown_reg5_reg9reg3shehe_is_the_reg3ladylord_of_s58reg3shehe_has_no_fiefss59_s49", 0),
##	#lord recruitment changes end
##
##        (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##     (try_end),
     ])
]
