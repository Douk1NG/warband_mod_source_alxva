# ======================================================================
# SHARED DEPENDENCY
# Entity: troop_change_relation_with_troop (script)
# Called by menus in 2 domains: kingdom_management, notifications
# ======================================================================

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

troop_change_relation_with_troop_scripts = [
("troop_change_relation_with_troop",
    [
	(store_script_param, ":troop1", 1),
	(store_script_param, ":troop2", 2),
	(store_script_param, ":amount", 3),

	(try_begin),
		(eq, ":troop1", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop2", ":amount"),
	(else_try),
		(eq, ":troop2", "trp_player"),
		(call_script, "script_change_player_relation_with_troop", ":troop1", ":amount"),
	(else_try),
		##diplomacy start+ Cancel the result for bad troop values
		(this_or_next|lt, ":troop1", 0),
		(this_or_next|lt, ":troop2", 0),
		##diplomacy end+
		(eq, ":troop1", ":troop2"),
		##diplomacy start+ Do this to avoid the controversy check further below
		(assign, ":amount", 0),
		##diplomacy end+
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop1", ":troop2"),
		(store_add, ":new_relation", reg0, ":amount"),

		(val_clamp, ":new_relation", -100, 101),

		(try_begin),
			(eq, ":new_relation", 0),
			(assign, ":new_relation", 1), #this removes the need for a separate "met" slot - any non-zero relation will be a met
		(try_end),

		(store_add, ":troop1_slot_for_troop2", ":troop2", slot_troop_relations_begin),
		(troop_set_slot, ":troop1", ":troop1_slot_for_troop2", ":new_relation"),

		(store_add, ":troop2_slot_for_troop1", ":troop1", slot_troop_relations_begin),
		(troop_set_slot, ":troop2", ":troop2_slot_for_troop1", ":new_relation"),
	(try_end),


	(try_begin), #generate controversy if troops are in the same faciton
		(lt, ":amount", -5),
		(try_begin),
			(eq, ":troop1", "trp_player"),
			(assign, ":faction1", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction1", ":troop1"),
		(try_end),
		(try_begin),
			(eq, ":troop2", "trp_player"),
			(assign, ":faction2", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction2", ":troop2"),
		(try_end),
		(eq, ":faction1", ":faction2"),
		(is_between, ":faction1", kingdoms_begin, kingdoms_end),

		(store_mul, ":controversy_generated", ":amount", -1),

		(troop_get_slot, ":controversy1", ":troop1", slot_troop_controversy),
		(val_add, ":controversy1", ":controversy_generated"),
		(val_min, ":controversy1", 100),
		(troop_set_slot, ":troop1", slot_troop_controversy, ":controversy1"),

		(troop_get_slot, ":controversy2", ":troop2", slot_troop_controversy),
		(val_add, ":controversy2", ":controversy_generated"),
		(val_min, ":controversy2", 100),
		(troop_set_slot, ":troop2", slot_troop_controversy, ":controversy2"),

	(try_end),

	(try_begin),
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		#(is_between, ":troop1", active_npcs_begin, active_npcs_end),
		#(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(try_begin),
			(gt, ":amount", 0),
			(val_add, "$total_relation_adds", ":amount"),
		(else_try),
			(val_sub, "$total_relation_subs", ":amount"),
		(try_end),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 4), #change back to 4
		##diplomacy start+ Also enable messages for promoted kingdom ladies
		#OLD:
		# (is_between, ":troop1", active_npcs_begin, active_npcs_end),
		# (is_between, ":troop2", active_npcs_begin, active_npcs_end),
		#
		#NEW:
		(is_between, ":troop1", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop1", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop1", active_npcs_begin, active_npcs_end),

		(is_between, ":troop2", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":troop2", slot_troop_occupation, slto_kingdom_hero),
			(is_between, ":troop2", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(neq, ":troop1", ":troop2"),

		(str_store_troop_name, s20, ":troop1"),
		(str_store_troop_name, s15, ":troop2"),
		(assign, reg4, ":amount"),
		(assign, reg14, ":new_relation"),
		(display_message, "str_s20_relation_with_s15_changed_by_reg4_to_reg14"),

		(assign, reg4, "$total_relation_adds"),
		(display_message, "str_total_additions_reg4"),
		(assign, reg4, "$total_relation_subs"),
		(display_message, "str_total_subtractions_reg4"),

		(assign, reg4, "$total_courtship_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total courtship quarrel changes: {reg4}"),

		(assign, reg4, "$total_random_quarrel_changes"),
		(display_message, "@{!}DEBUG -- Total random quarrel changes: {reg4}"),

		(assign, reg4, "$total_battle_ally_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for allies: {reg4}"),

		(assign, reg4, "$total_battle_enemy_changes"),
		(display_message, "@{!}DEBUG -- Total battle changes for enemies: {reg4}"),

		(assign, reg4, "$total_promotion_changes"),
		(display_message, "@{!}DEBUG -- Total promotion changes: {reg4}"),

		(assign, reg4, "$total_feast_changes"),
		(display_message, "@{!}DEBUG -- Total feast changes: {reg4}"),

		(assign, reg4, "$total_policy_dispute_changes"),
		(assign, reg5, "$number_of_controversial_policy_decisions"),
		(display_message, "@{!}DEBUG -- Total policy dispute changes: {reg4} from {reg5} decisions"),

		(assign, reg4, "$total_indictment_changes"),
		(display_message, "@{!}DEBUG -- Total faction switch changes: {reg4}"),

		(assign, reg4, "$total_no_fief_changes"),
		(display_message, "@{!}DEBUG -- Total no fief changes: {reg4}"),

		(assign, reg4, "$total_relation_changes_through_convergence"),
		(display_message, "@{!}DEBUG -- Total changes through convergence: {reg4}"),

		(assign, reg4, "$total_vassal_days_responding_to_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal responses to campaign: {reg4}"),

		(assign, reg4, "$total_vassal_days_on_campaign"),
		(display_message, "@{!}DEBUG -- Total vassal campaign days: {reg4}"),

		(val_max, "$total_vassal_days_on_campaign", 1),
		(store_mul, ":response_rate", "$total_vassal_days_responding_to_campaign", 100),
		(val_div, ":response_rate", "$total_vassal_days_on_campaign"),
		(assign, reg4, ":response_rate"),
		(display_message, "@{!}DEBUG -- Vassal response rate: {reg4}"),



#		(assign, reg4, "$total_joy_battle_changes"),
#		(display_message, "@{!}DEBUG -- Total joy of battle changes"),

	(try_end),

	])
]
