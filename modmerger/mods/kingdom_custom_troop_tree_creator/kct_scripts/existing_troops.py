# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from header_skills import *
from header_troops import *
from ID_items import *
from ID_meshes import *
from module_constants import *

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

# KCT existing-troops update (toggle "Update existing garrisons & party on
# save"). Option A - tier-preserving (fair):
# For every non-hero stack the script preserves its power level instead of
# maxing to leaves. It reads the stack's level (store_character_level),
# finds the new tree's tier whose level is closest (minimal abs diff),
# and redistributes the same number of troops evenly among ALL troops of
# that tier in the new tree (level-identical troops = same tier). Wounded
# are preserved proportionally (split evenly with remainder). Heroes,
# prisoners and lords are never touched (no party_clear). Natives are
# converted too but at their level-matched tier, not as elites.
# Gated by $cstm_update_existing_troops (0/1) in branch_display.py.

EXISTING_TROOPS_SCRIPTS = [
	# script_kct_reset_garrisons_focused - tier-preserving garrison update.
	("kct_reset_garrisons_focused",
	[
		(assign, ":grand_total", 0),
		(assign, ":centres", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":faction", ":center_no"),
			(eq, ":faction", "fac_player_supporters_faction"),

			(assign, ":converted_this_center", 0),
			(party_get_num_companion_stacks, ":num_stacks", ":center_no"),
			(try_for_range_backwards, ":stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":st_troop", ":center_no", ":stack"),
				(neg|troop_is_hero, ":st_troop"),
				(party_stack_get_size, ":st_size", ":center_no", ":stack"),
				(gt, ":st_size", 0),
				(party_stack_get_num_wounded, ":st_wounded", ":center_no", ":stack"),
				(store_character_level, ":orig_lvl", ":st_troop"),

				# Remove the original stack.
				(party_remove_members, ":center_no", ":st_troop", ":st_size"),
				(val_add, ":converted_this_center", ":st_size"),

				# Find the new-tree level closest to the original level.
				(assign, ":best_level", -1),
				(assign, ":best_diff", 1000),
				(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
					(store_character_level, ":nt_lvl", ":nt"),
					(store_sub, ":diff", ":nt_lvl", ":orig_lvl"),
					(val_abs, ":diff"),
					(lt, ":diff", ":best_diff"),
					(assign, ":best_diff", ":diff"),
					(assign, ":best_level", ":nt_lvl"),
				(try_end),
				(gt, ":best_level", 0),

				# Count how many new-tree troops share that level (tier size).
				(assign, ":match_count", 0),
				(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
					(store_character_level, ":nt_lvl", ":nt"),
					(eq, ":nt_lvl", ":best_level"),
					(val_add, ":match_count", 1),
				(try_end),
				(gt, ":match_count", 0),

				# Distribute evenly among the tier's troops, wounded proportionally.
				(assign, ":idx", 0),
				(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
					(store_character_level, ":nt_lvl", ":nt"),
					(eq, ":nt_lvl", ":best_level"),
					(store_div, ":cnt", ":st_size", ":match_count"),
					(store_mod, ":rem", ":st_size", ":match_count"),
					(try_begin),
						(lt, ":idx", ":rem"),
						(val_add, ":cnt", 1),
					(try_end),
					(store_div, ":wnd", ":st_wounded", ":match_count"),
					(store_mod, ":wrem", ":st_wounded", ":match_count"),
					(try_begin),
						(lt, ":idx", ":wrem"),
						(val_add, ":wnd", 1),
					(try_end),
					(try_begin),
						(gt, ":cnt", 0),
						(party_add_members, ":center_no", ":nt", ":cnt"),
						(gt, ":wnd", 0),
						(party_wound_members, ":center_no", ":nt", ":wnd"),
					(try_end),
					(val_add, ":idx", 1),
				(try_end),
			(try_end),

			(try_begin),
				(gt, ":converted_this_center", 0),
				(val_add, ":grand_total", ":converted_this_center"),
				(val_add, ":centres", 1),
			(try_end),
		(try_end),

		(try_begin),
			(gt, ":centres", 0),
			(assign, reg6, ":grand_total"),
			(assign, reg7, ":centres"),
			(display_message, "@Kingdom garrison update: {reg6} troops converted in {reg7} garrisons (tier-preserved)."),
		(try_end),
	]),

	# script_kct_update_player_party - tier-preserving player party update.
	("kct_update_player_party",
	[
		(assign, ":total", 0),
		(assign, ":total_wounded", 0),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		# Snapshot stacks first into temp arrays to avoid mixing remove/add,
		# then process tier-preserving replacement per original stack.
		(try_for_range_backwards, ":stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":st_troop", "p_main_party", ":stack"),
			(neg|troop_is_hero, ":st_troop"),
			(party_stack_get_size, ":st_size", "p_main_party", ":stack"),
			(gt, ":st_size", 0),
			(party_stack_get_num_wounded, ":st_wounded", "p_main_party", ":stack"),
			(store_character_level, ":orig_lvl", ":st_troop"),
			(party_remove_members, "p_main_party", ":st_troop", ":st_size"),
			(val_add, ":total", ":st_size"),
			(val_add, ":total_wounded", ":st_wounded"),

			(assign, ":best_level", -1),
			(assign, ":best_diff", 1000),
			(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
				(store_character_level, ":nt_lvl", ":nt"),
				(store_sub, ":diff", ":nt_lvl", ":orig_lvl"),
				(val_abs, ":diff"),
				(lt, ":diff", ":best_diff"),
				(assign, ":best_diff", ":diff"),
				(assign, ":best_level", ":nt_lvl"),
			(try_end),
			(gt, ":best_level", 0),

			(assign, ":match_count", 0),
			(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
				(store_character_level, ":nt_lvl", ":nt"),
				(eq, ":nt_lvl", ":best_level"),
				(val_add, ":match_count", 1),
			(try_end),
			(gt, ":match_count", 0),

			(assign, ":idx", 0),
			(try_for_range, ":nt", "$cstm_troops_begin", "$cstm_troops_end"),
				(store_character_level, ":nt_lvl", ":nt"),
				(eq, ":nt_lvl", ":best_level"),
				(store_div, ":cnt", ":st_size", ":match_count"),
				(store_mod, ":rem", ":st_size", ":match_count"),
				(try_begin),
					(lt, ":idx", ":rem"),
					(val_add, ":cnt", 1),
				(try_end),
				(store_div, ":wnd", ":st_wounded", ":match_count"),
				(store_mod, ":wrem", ":st_wounded", ":match_count"),
				(try_begin),
					(lt, ":idx", ":wrem"),
					(val_add, ":wnd", 1),
				(try_end),
				(try_begin),
					(gt, ":cnt", 0),
					(party_add_members, "p_main_party", ":nt", ":cnt"),
					(gt, ":wnd", 0),
					(party_wound_members, "p_main_party", ":nt", ":wnd"),
				(try_end),
				(val_add, ":idx", 1),
			(try_end),
		(try_end),

		(try_begin),
			(gt, ":total", 0),
			(assign, reg6, ":total"),
			(display_message, "@Player party rebalanced: {reg6} troops (tier-preserved)."),
		(try_end),
	]),
]
