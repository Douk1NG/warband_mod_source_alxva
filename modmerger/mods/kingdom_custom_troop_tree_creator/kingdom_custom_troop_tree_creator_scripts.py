# -*- coding: cp1254 -*-
import collections
import math

from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from header_skills import *
from header_troops import *
from ID_items import *
from ID_meshes import *
from module_constants import *

# Reuse (not re-declare) the custom_troops mod's slot/string/array constants,
# item-type strings and stat ranges - custom_troops is active and mandatory.
from custom_troops_constants import *

from kingdom_custom_troop_tree_creator_troops import PRESET_4_UNITS, preset_4_troop_id

# Troop slots used to link a real custom troop to its dummy. These MUST match the
# values in the base mod's custom_troops_constants (NEW_TROOP_SLOTS_BEGIN = 500)
# because the dummies for presets 1-3 are linked by the base mod at game start
# using those exact slot numbers.
cstm_slot_troop_dummy = 500
cstm_slot_troop_custom_troop = 501

# Marks a real troop as configured (its store Save pressed). Used by the bottom-up
# editing restriction (CSTM_TROOP_TREES_SPEC.md §7): a node's customise entry
# unlocks only after its upgrade parent has been configured. Must match
# cstm_slot_troop_configured in kingdom_custom_troop_tree_creator_presentations.py;
# the base mod's allocator ends at 519, so 520 is free.
cstm_slot_troop_configured = 520

# The troop whose name is used to store the custom troop tree prefix string
# (mirrors cstm_troop_tree_prefix in custom_troops_constants).
cstm_troop_tree_prefix = "trp_cstm_custom_troops_end"

# Self-contained copies of the presentation helper scripts used by
# prsnt_cstm_choose_troop_tree. Ported (not imported) from the custom_troops
# mod so this mod does not depend on it at runtime.

# WPT order matches proficiencies_begin..proficiencies_end:
# one handed, two handed, polearm, archery, crossbow, throwing, firearm.

new_scripts = [
	# script_kct_create_mesh_overlay
	("kct_create_mesh_overlay",
	[
		(store_script_param, ":mesh", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size_x", 4),
		(store_script_param, ":size_y", 5),

		(set_fixed_point_multiplier, 1000),
		(create_mesh_overlay, reg1, ":mesh"),
		(position_set_x, pos2, ":pos_x"),
		(position_set_y, pos2, ":pos_y"),
		(overlay_set_position, reg1, pos2),
		(position_set_x, pos3, ":size_x"),
		(position_set_y, pos3, ":size_y"),
		(overlay_set_size, reg1, pos3),
	]),

	# script_kct_create_text_overlay
	("kct_create_text_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":text_size", 4),
		(store_script_param, ":size_x", 5),
		(store_script_param, ":size_y", 6),
		(store_script_param, ":flags", 7),

		(set_fixed_point_multiplier, 1000),
		(create_text_overlay, reg1, ":string", ":flags"),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(position_set_x, pos1, ":text_size"),
		(position_set_y, pos1, ":text_size"),
		(overlay_set_size, reg1, pos1),
		(position_set_x, pos1, ":size_x"),
		(position_set_y, pos1, ":size_y"),
		(overlay_set_area_size, reg1, pos1),
		(overlay_set_text, reg1, ":string"),
	]),

	# script_kct_create_game_button_overlay
	("kct_create_game_button_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),

		(set_fixed_point_multiplier, 1000),
		(create_game_button_overlay, reg1, ":string"),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(overlay_set_text, reg1, ":string"),
	]),

	# script_kct_create_combo_button_overlay
	("kct_create_combo_button_overlay",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),

		(set_fixed_point_multiplier, 1000),
		(create_combo_button_overlay, reg1),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
	]),

	# script_kct_prsnt_lines
	("kct_prsnt_lines",
	[
		(store_script_param, ":size_x", 1),
		(store_script_param, ":size_y", 2),
		(store_script_param, ":pos_x", 3),
		(store_script_param, ":pos_y", 4),
		(store_script_param, ":color", 5),

		(val_mul, ":size_x", 50),
		(val_mul, ":size_y", 50),
		(call_script, "script_kct_create_mesh_overlay", "mesh_white_plane", ":pos_x", ":pos_y", ":size_x", ":size_y"),
		(overlay_set_color, reg1, ":color"),
	]),

	# script_kct_prsnt_lines_to
	("kct_prsnt_lines_to", # Drawing lines from (x1,y1) to (x2,y2), the line will be horizontal til half way, vertical and then horizontal again
	[
		(store_script_param, ":pos_x1", 1),
		(store_script_param, ":pos_y1", 2),
		(store_script_param, ":pos_x2", 3),
		(store_script_param, ":pos_y2", 4),
		(store_script_param, ":color", 5),

		(try_begin),
			(eq, ":pos_x1", ":pos_x2"),
			(store_sub, ":size", ":pos_y1", ":pos_y2"),
			(val_abs, ":size"),
			(val_min, ":pos_y1", ":pos_y2"),
			(call_script, "script_kct_prsnt_lines", 4, ":size", ":pos_x1", ":pos_y1", ":color"),
		(else_try),
			(eq, ":pos_y1", ":pos_y2"),
			(store_sub, ":size", ":pos_x1", ":pos_x2"),
			(val_abs, ":size"),
			(val_min, ":pos_x1", ":pos_x2"),
			(call_script, "script_kct_prsnt_lines", ":size", 5, ":pos_x1", ":pos_y1", ":color"),
		(else_try),
			(call_script, "script_kct_prsnt_lines_to", ":pos_x1", ":pos_y1", ":pos_x1", ":pos_y2", ":color"),
			(call_script, "script_kct_prsnt_lines_to", ":pos_x1", ":pos_y2", ":pos_x2", ":pos_y2", ":color"),
		(try_end),
	]),

	# script_kct_create_text_box_overlay
	("kct_create_text_box_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),

		(set_fixed_point_multiplier, 1000),
		(create_simple_text_box_overlay, reg1, ":string"),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(overlay_set_text, reg1, ":string"),
	]),

	# script_kct_create_troop_image
	("kct_create_troop_image",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size", 4),

		(set_fixed_point_multiplier, 1000),
		(store_mul, ":cur_troop", ":troop_no", 2),
		(create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
		(position_set_x, pos2, ":pos_x"),
		(position_set_y, pos2, ":pos_y"),
		(overlay_set_position, reg1, pos2),
		(position_set_x, pos3, ":size"),
		(position_set_y, pos3, ":size"),
		(overlay_set_size, reg1, pos3),
	]),

	# script_kct_create_troop_image_size
	("kct_create_troop_image_size",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size_x", 4),
		(store_script_param, ":size_y", 5),

		(set_fixed_point_multiplier, 1000),
		(store_mul, ":cur_troop", ":troop_no", 2),
		(create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
		(position_set_x, pos2, ":pos_x"),
		(position_set_y, pos2, ":pos_y"),
		(overlay_set_position, reg1, pos2),
		(position_set_x, pos3, ":size_x"),
		(position_set_y, pos3, ":size_y"),
		(overlay_set_size, reg1, pos3),
	]),

	# script_kct_troop_refresh_name
	("kct_troop_refresh_name",
	[
		(store_script_param, ":troop", 1),

		(str_store_troop_name, s0, cstm_troop_tree_prefix),

		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		(str_store_troop_name, s1, ":dummy"),

		(troop_set_name, ":troop", "@{s0} {s1}"),

		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		(str_store_troop_name_plural, s1, ":dummy"),

		(troop_set_plural_name, ":troop", "@{s0} {s1}"),
	]),

	# script_kct_create_troop_tree_images
	("kct_create_troop_tree_images",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":gap_x", 4),
		(store_script_param, ":gap_y", 5),
		(store_script_param, ":height", 6),

		(troop_get_upgrade_troop, ":upgrade_1", ":troop", 0),
		(troop_get_upgrade_troop, ":upgrade_2", ":troop", 1),

		(store_add, ":pos_x2", ":pos_x", ":gap_x"),

		(try_begin),
			(gt, ":upgrade_1", 0),

			(try_begin),
				(gt, ":upgrade_2", 0),

				(call_script, "script_kct_create_troop_tree_images", ":upgrade_1", ":pos_x2", ":pos_y", ":gap_x", ":gap_y", ":height"),
				(store_add, ":pos_y2", ":pos_y", reg0),

				(val_add, ":height", 1),
				(call_script, "script_kct_create_troop_tree_images", ":upgrade_2", ":pos_x2", ":pos_y", ":gap_x", ":gap_y", ":height"),
				(store_add, ":pos_y3", ":pos_y", reg0),

				(store_sub, ":difference", ":pos_y3", ":pos_y2"),
				(val_div, ":difference", 2),
				(store_sub, ":offset_y", ":pos_y2", ":pos_y"),
				(val_add, ":offset_y", ":difference"),
			(else_try),
				(call_script, "script_kct_create_troop_tree_images", ":upgrade_1", ":pos_x2", ":pos_y", ":gap_x", ":gap_y", ":height"),
				(assign, ":offset_y", reg0),
			(try_end),
		(else_try),
			(store_mul, ":offset_y", ":height", ":gap_y"),
		(try_end),

		(val_add, ":pos_y", ":offset_y"),

		(str_store_troop_name, s0, ":troop"),
		(call_script, "script_kct_create_text_overlay", "str_s0", ":pos_x", ":pos_y", 600, ":gap_x", 50, tf_center_justify|tf_vertical_align_center),
		(troop_set_slot, "trp_cstm_overlay_troops", reg1, ":troop"),

		(val_sub, ":pos_x", 52),

		(call_script, "script_kct_create_troop_image", ":troop", ":pos_x", ":pos_y", 500),
		(position_set_x, pos1, 375),
		(position_set_y, pos1, 500),
		(overlay_set_size, reg1, pos1),
		(troop_set_slot, "trp_cstm_overlay_troops", reg1, ":troop"),

		(assign, ":line_offset_x", 56),
		(store_div, ":line_offset_y", ":gap_y", 2),
		(val_add, ":pos_x", ":line_offset_x"),
		(val_add, ":pos_y", ":line_offset_y"),
		(try_begin),
			(gt, ":upgrade_1", 0),

			(try_begin),
				(gt, ":upgrade_2", 0),

				(val_add, ":pos_y2", ":line_offset_y"),
				(val_add, ":pos_y3", ":line_offset_y"),

				(store_add, ":pos_x2", ":pos_x", ":gap_x"),
				(val_add, ":pos_x2", 5),
				(call_script, "script_kct_prsnt_lines_to", ":pos_x", ":pos_y", ":pos_x2", ":pos_y2", 0x000000),
				(call_script, "script_kct_prsnt_lines_to", ":pos_x", ":pos_y", ":pos_x2", ":pos_y3", 0x000000),
			(else_try),
				(val_add, ":pos_x2", 5),
				(call_script, "script_kct_prsnt_lines_to", ":pos_x", ":pos_y", ":pos_x2", ":pos_y", 0x000000),
			(try_end),
		(try_end),

		(assign, reg0, ":offset_y"),
	]),

# Ported from custom_troops_scripts.py (self-contained kct_* copies).

# script_kct_print_attribute_to_s0
	("kct_print_attribute_to_s0",
	[
		(store_script_param, ":attribute", 1),
		
		(store_add, ":attribute_string", cstm_attribute_strings_begin, ":attribute"),
		(str_store_string, s0, ":attribute_string"),
	]),

# script_kct_print_skill_to_s0
	("kct_print_skill_to_s0",
	[
		(store_script_param, ":skill", 1),
		
		(store_add, ":skill_string", cstm_skill_strings_begin, ":skill"),
		(str_store_string, s0, ":skill_string"),
	]),

# script_kct_troop_reset_stats
	("kct_troop_reset_stats",
	[
		(store_script_param, ":troop", 1),
		
		(try_for_range, ":attribute", 0, 4),
			(store_attribute_level, ":points", ":troop", ":attribute"),
			(val_mul, ":points", -1),
			(troop_raise_attribute, ":troop", ":attribute", ":points"),
		(try_end),
		
		(try_for_range, ":skill", 0, 42),
			(store_skill_level, ":points", ":skill", ":troop"),
			(val_mul, ":points", -1),
			(troop_raise_skill, ":troop", ":skill", ":points"),
		(try_end),
		
		(try_for_range, ":proficiency", 0, 7),
			(troop_raise_proficiency_linear, ":troop", ":proficiency", -700),
		(try_end),
	]),

# script_kct_get_attribute_points
	("kct_get_attribute_points",
	[
		(store_script_param, ":troop", 1),
		
		(store_character_level, ":points_available", ":troop"),
		(val_add, ":points_available", 20),
		
		(assign, reg0, ":points_available"),
	]),

# script_kct_get_attribute_points_spent
	("kct_get_attribute_points_spent",
	[
		(store_script_param, ":troop", 1),
		
		(assign, ":points_spent", 0),
		(try_for_range, ":attribute", 0, attributes_end),
			(store_attribute_level, ":attribute_level", ":troop", ":attribute"),
			(val_add, ":points_spent", ":attribute_level"),
		(try_end),
		
		(assign, reg0, ":points_spent"),
	]),

# script_kct_get_attribute_points_available
	("kct_get_attribute_points_available",
	[
		(store_script_param, ":troop", 1),
		
		(call_script, "script_kct_get_attribute_points", ":troop"),
		(assign, ":points", reg0),
		(call_script, "script_kct_get_attribute_points_spent", ":troop"),
		(val_sub, ":points", reg0),
		
		(assign, reg0, ":points"),
	]),

# script_kct_get_attribute_points_available_to_upgrade
	("kct_get_attribute_points_available_to_upgrade",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":upgrade", 2),
		
		(call_script, "script_kct_get_attribute_points", ":upgrade"),
		(assign, ":points", reg0),
		
		(assign, ":points_spent", 0),
		(try_for_range, ":attribute", 0, attributes_end),
			(store_attribute_level, ":curr_level", ":troop", ":attribute"),
			(store_attribute_level, ":upgrade_level", ":upgrade", ":attribute"),
			(val_max, ":upgrade_level", ":curr_level"),
			
			(val_add, ":points_spent", ":upgrade_level"),
		(try_end),
		
		(store_sub, reg0, ":points", ":points_spent"),
	]),

# script_kct_troop_get_attribute_min_from_points
	("kct_troop_get_attribute_min_from_points",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":attribute", 2),
		
		(troop_get_type, ":gender", ":troop"),
		(try_begin),
			(troop_get_slot, ":base_troop", ":troop", cstm_slot_troop_base_troop),
			(gt, ":base_troop", 0),
			
			(store_attribute_level, ":min_level", ":base_troop", ":attribute"),
		(else_try),
			(eq, ":attribute", ca_strength),
			
			(assign, ":min_level", CSTM_STR_START),
			(try_begin),
				(neq, ":gender", 1),
				
				(val_add, ":min_level", 1),
			(try_end),
		(else_try),
			(eq, ":attribute", ca_agility),
			
			(assign, ":min_level", CSTM_AGI_START),
			(try_begin),
				(eq, ":gender", 1),
				
				(val_add, ":min_level", 1),
			(try_end),
		(else_try),
			(eq, ":attribute", ca_intelligence),
			
			(assign, ":min_level", CSTM_AGI_START),
		(else_try),
			(eq, ":attribute", ca_charisma),
			
			(assign, ":min_level", CSTM_CHA_START),
		(try_end),
		
		(assign, reg0, ":min_level"),
	]),

# script_kct_troop_get_attribute_min_from_tree
	("kct_troop_get_attribute_min_from_tree",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":base_troop", 2),
		(store_script_param, ":attribute", 3),
		
		(call_script, "script_kct_troop_get_attribute_min_from_points", ":troop", ":attribute"),
		(assign, ":min_level", reg0),
		
		# A child can never go below its parent's current value - inheritance only
		# goes up the tree (spec §7) - so floor the minimum on the parent troop's
		# current level.
		(troop_get_slot, ":parent_troop", ":troop", cstm_slot_troop_base_troop),
		(try_begin),
			(gt, ":parent_troop", 0),
			
			(store_attribute_level, ":parent_level", ":parent_troop", ":attribute"),
			(val_max, ":min_level", ":parent_level"),
		(try_end),
		
		# The root of a tree (no parent troop) keeps only its base minimum: the
		# upgrade-path walk below would hand it its whole subtree's requirements,
		# and auto-distribution would spend its entire budget meeting them.
		# Non-root nodes keep the upgrade-path minimums.
		(try_begin),
			(gt, ":parent_troop", 0),
			(troop_get_upgrade_troop, ":upgrade", ":base_troop", 0),
			(gt, ":upgrade", 0),
			
			# Get the minimum necessary for the upgrade troop to possibly have its current level
			(call_script, "script_kct_get_attribute_points", ":upgrade"),
			(assign, ":upgrade_points", reg0),
			(call_script, "script_kct_get_attribute_points", ":troop"),
			(val_sub, ":upgrade_points", reg0),
			(val_max, ":upgrade_points", 0),
			
			(store_attribute_level, ":upgrade_level", ":upgrade", ":attribute"),
			(val_sub, ":upgrade_level", ":upgrade_points"),
			
			#(call_script, "script_kct_print_attribute_to_s0", ":attribute"),
			#(str_store_troop_name, s1, ":upgrade"),
			#(str_store_troop_name, s2, ":troop"),
			#(assign, reg0, ":upgrade_points"),
			#(assign, reg1, ":upgrade_level"),
			#(display_message, "@{s1} gains {reg0} points, thus {s2} requires {reg1} in {s0}"),
			
			(val_max, ":min_level", ":upgrade_level"),
			
			# Recursively call up the tree
			(call_script, "script_kct_troop_get_attribute_min_from_tree", ":troop", ":upgrade", ":attribute"),
			(val_max, ":min_level", reg0),
			
			# As above for second upgrade troop
			(troop_get_upgrade_troop, ":upgrade", ":base_troop", 1),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_get_attribute_points", ":upgrade"),
			(assign, ":upgrade_points", reg0),
			(call_script, "script_kct_get_attribute_points", ":troop"),
			(val_sub, ":upgrade_points", reg0),
			(val_max, ":upgrade_points", 0),
			
			(store_attribute_level, ":upgrade_level", ":upgrade", ":attribute"),
			(val_sub, ":upgrade_level", ":upgrade_points"),
			
			#(call_script, "script_kct_print_attribute_to_s0", ":attribute"),
			#(str_store_troop_name, s1, ":upgrade"),
			#(str_store_troop_name, s2, ":troop"),
			#(assign, reg0, ":upgrade_points"),
			#(assign, reg1, ":upgrade_level"),
			#(display_message, "@{s1} gains {reg0} points, thus {s2} requires {reg1} in {s0}"),
			
			(val_max, ":min_level", ":upgrade_level"),
			
			(call_script, "script_kct_troop_get_attribute_min_from_tree", ":troop", ":upgrade", ":attribute"),
			(val_max, ":min_level", reg0),
		(try_end),
		
		(assign, reg0, ":min_level"),
	]),

# script_kct_troop_get_attribute_max_from_points
	("kct_troop_get_attribute_max_from_points",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":attribute", 2),
		
		# Add the available points to spend and the points used on this attribute to get the max points that could be spent
		(store_attribute_level, ":max_level", ":troop", ":attribute"),
		(call_script, "script_kct_get_attribute_points_available", ":troop"),
		(val_add, ":max_level", reg0),
		
		(assign, reg0, ":max_level"),
	]),

# script_kct_troop_get_attribute_max_from_upgrade
	("kct_troop_get_attribute_max_from_upgrade",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":upgrade", 2),
		(store_script_param, ":attribute", 3),
		
		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		
		# Add the available points to spend and the points used on this attribute to get the max points that could be spent
		(store_attribute_level, ":curr_level", ":dummy", ":attribute"),
		(store_attribute_level, ":upgrade_level", ":upgrade", ":attribute"),
		(val_max, ":upgrade_level", ":curr_level"),
		
		(call_script, "script_kct_get_attribute_points_available_to_upgrade", ":dummy", ":upgrade"),
		(val_add, reg0, ":upgrade_level"),
	]),

# script_kct_troop_get_attribute_max_from_tree
	("kct_troop_get_attribute_max_from_tree",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":attribute", 2),
		
		(call_script, "script_kct_troop_get_attribute_max_from_points", ":troop", ":attribute"),
		(assign, ":max_level", reg0),
		(store_attribute_level, ":curr_level", ":troop", ":attribute"),
		(val_max, ":max_level", ":curr_level"),
		
		(try_begin),
			(troop_get_upgrade_troop, ":upgrade", ":troop", 0),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_troop_get_attribute_max_from_upgrade", ":troop", ":upgrade", ":attribute"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(call_script, "script_kct_troop_get_attribute_max_from_tree", ":upgrade", ":attribute"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(troop_get_upgrade_troop, ":upgrade", ":troop", 1),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_troop_get_attribute_max_from_upgrade", ":troop", ":upgrade", ":attribute"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(call_script, "script_kct_troop_get_attribute_max_from_tree", ":upgrade", ":attribute"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
		(try_end),
		
		(assign, reg0, ":max_level"),
	]),

# script_kct_dummy_set_attribute
	("kct_dummy_set_attribute",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":attribute", 2),
		(store_script_param, ":amount", 3),
		
		(store_attribute_level, ":points", ":troop", ":attribute"),
		(store_sub, ":difference", ":amount", ":points"),
		(troop_raise_attribute, ":troop", ":attribute", ":difference"),
		
		(try_begin),
			(lt, ":difference", 0),
			(eq, ":attribute", ca_intelligence),
			
			(call_script, "script_kct_get_skill_points_available", ":troop"),
			(lt, reg0, 0),
			
			(store_mul, ":difference", reg0, -1),
			(troop_raise_attribute, ":troop", ":attribute", ":difference"),
			
			(assign, reg0, ":amount"),
			(display_message, "@Cannot reduce INT to {reg0} without taking back bonus skill points"),
		(else_try),
			(gt, ":difference", 0),
			
			(troop_get_slot, ":actual_troop", ":troop", cstm_slot_troop_custom_troop),
			
			(store_add, ":attribute_string", cstm_attribute_strings_begin, ":attribute"),
			(str_store_string, s0, ":attribute_string"),
			
			(call_script, "script_kct_troop_get_attribute_max_from_tree", ":actual_troop", ":attribute"),
			(try_begin),
				(gt, ":amount", reg0),
				
				(store_sub, ":difference", reg0, ":amount"),
				(troop_raise_attribute, ":troop", ":attribute", ":difference"),
				(display_message, "@Can't raise {s0} above that of {s10}"),
			(try_end),
		(try_end),
	]),

# script_kct_get_skill_points
	("kct_get_skill_points",
	[
		(store_script_param, ":troop", 1),
		
		(store_character_level, ":points_available", ":troop"),
		
		(store_attribute_level, ":intelligence", ":troop", ca_intelligence),
		(val_add, ":points_available", ":intelligence"),
		(val_add, ":points_available", 1),
		
		(assign, reg0, ":points_available"),
	]),

# script_kct_get_skill_points_spent
	("kct_get_skill_points_spent",
	[
		(store_script_param, ":troop", 1),
		
		(assign, ":points_spent", 0),
		(try_for_range, ":skill", 0, skills_end),
			(store_skill_level, ":skill_level", ":skill", ":troop"),
			(val_add, ":points_spent", ":skill_level"),
		(try_end),
		
		(assign, reg0, ":points_spent"),
	]),

# script_kct_get_skill_points_available
	("kct_get_skill_points_available",
	[
		(store_script_param, ":troop", 1),
		
		(call_script, "script_kct_get_skill_points", ":troop"),
		(assign, ":points", reg0),
		(call_script, "script_kct_get_skill_points_spent", ":troop"),
		(val_sub, ":points", reg0),
		
		(assign, reg0, ":points"),
	]),

# script_kct_get_skill_points_available_to_upgrade
	("kct_get_skill_points_available_to_upgrade",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":upgrade", 2),
		
		(call_script, "script_kct_get_skill_points", ":upgrade"),
		(assign, ":points", reg0),
		
		(assign, ":points_spent", 0),
		(try_for_range, ":skill", 0, skills_end),
			(store_skill_level, ":curr_level", ":skill", ":troop"),
			(store_skill_level, ":upgrade_level", ":skill", ":upgrade"),
			(val_max, ":upgrade_level", ":curr_level"),
			
			(val_add, ":points_spent", ":upgrade_level"),
		(try_end),
		
		(store_sub, reg0, ":points", ":points_spent"),
	]),

# script_kct_troop_get_skill_min_from_points
	("kct_troop_get_skill_min_from_points",
	[
		#(store_script_param, ":troop", 1),
		#(store_script_param, ":skill", 2),
		
		(assign, reg0, 0),
	]),

# script_kct_troop_get_skill_min_from_tree
	("kct_troop_get_skill_min_from_tree",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":base_troop", 2),
		(store_script_param, ":skill", 3),
		
		(call_script, "script_kct_troop_get_skill_min_from_points", ":troop", ":skill"),
		(assign, ":min_level", reg0),
		
		# A child can never go below its parent's current value - inheritance only
		# goes up the tree (spec §7) - so floor the minimum on the parent troop's
		# current level.
		(troop_get_slot, ":parent_troop", ":troop", cstm_slot_troop_base_troop),
		(try_begin),
			(gt, ":parent_troop", 0),
			
			(store_skill_level, ":parent_level", ":skill", ":parent_troop"),
			(val_max, ":min_level", ":parent_level"),
		(try_end),
		
		(try_begin),
			(troop_get_upgrade_troop, ":upgrade", ":base_troop", 0),
			(gt, ":upgrade", 0),
			
			# Get the minimum necessary for the upgrade troop to possibly have its current level
			(call_script, "script_kct_get_skill_points", ":upgrade"),
			(assign, ":upgrade_points", reg0),
			(call_script, "script_kct_get_skill_points", ":troop"),
			(val_sub, ":upgrade_points", reg0),
			(val_max, ":upgrade_points", 0),
			(assign, reg0, ":upgrade_points"),
			
			(store_skill_level, ":upgrade_level", ":skill", ":upgrade"),
			(val_sub, ":upgrade_level", ":upgrade_points"),
			(val_max, ":upgrade_level", 0),
			
			#(try_begin),
			#	(gt, ":upgrade_level", 0),
			#	
			#	(call_script, "script_kct_print_skill_to_s0", ":skill"),
			#	(str_store_troop_name, s1, ":upgrade"),
			#	(str_store_troop_name, s2, ":troop"),
			#	(assign, reg0, ":upgrade_points"),
			#	(assign, reg1, ":upgrade_level"),
			#	(display_message, "@{s1} gains {reg0} points, thus {s2} requires {reg1} in {s0}"),
			#(try_end),
			
			(val_max, ":min_level", ":upgrade_level"),
			
			# Recursively call up the tree
			(call_script, "script_kct_troop_get_skill_min_from_tree", ":troop", ":upgrade", ":skill"),
			(val_max, ":min_level", reg0),
			
			# As above for second upgrade troop
			(troop_get_upgrade_troop, ":upgrade", ":base_troop", 1),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_get_skill_points", ":upgrade"),
			(assign, ":upgrade_points", reg0),
			(call_script, "script_kct_get_skill_points", ":troop"),
			(val_sub, ":upgrade_points", reg0),
			(val_max, ":upgrade_points", 0),
			
			(store_skill_level, ":upgrade_level", ":skill", ":upgrade"),
			(val_sub, ":upgrade_level", ":upgrade_points"),
			(val_max, ":upgrade_level", 0),
			
			#(try_begin),
			#	(gt, ":upgrade_level", 0),
			#	
			#	(call_script, "script_kct_print_skill_to_s0", ":skill"),
			#	(str_store_troop_name, s1, ":upgrade"),
			#	(str_store_troop_name, s2, ":troop"),
			#	(assign, reg0, ":upgrade_points"),
			#	(assign, reg1, ":upgrade_level"),
			#	(display_message, "@{s1} gains {reg0} points, thus {s2} requires {reg1} in {s0}"),
			#(try_end),
			
			(val_max, ":min_level", ":upgrade_level"),
			
			(call_script, "script_kct_troop_get_skill_min_from_tree", ":troop", ":upgrade", ":skill"),
			(val_max, ":min_level", reg0),
		(try_end),
		
		(assign, reg0, ":min_level"),
	]),

# script_kct_troop_get_skill_max_from_points
	("kct_troop_get_skill_max_from_points",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":skill", 2),
		
		# Add the available points to spend and the points used on this skill to get the max points that could be spent
		(store_skill_level, ":max_level", ":skill", ":troop"),
		(call_script, "script_kct_get_skill_points_available", ":troop"),
		(val_add, ":max_level", reg0),
		
		(assign, reg0, ":max_level"),
	]),

# script_kct_troop_get_skill_max_from_upgrade
	("kct_troop_get_skill_max_from_upgrade",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":upgrade", 2),
		(store_script_param, ":skill", 3),
		
		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		
		# Add the available points to spend and the points used on this skill to get the max points that could be spent
		(store_skill_level, ":curr_level", ":skill", ":dummy"),
		(store_skill_level, ":upgrade_level", ":skill", ":upgrade"),
		(val_max, ":upgrade_level", ":curr_level"),
		
		(call_script, "script_kct_get_skill_points_available_to_upgrade", ":dummy", ":upgrade"),
		(val_add, reg0, ":upgrade_level"),
	]),

# script_kct_troop_get_skill_max_from_tree
	("kct_troop_get_skill_max_from_tree",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":skill", 2),
		
		(call_script, "script_kct_troop_get_skill_max_from_points", ":troop", ":skill"),
		(assign, ":max_level", reg0),
		(store_skill_level, ":curr_level", ":skill", ":troop"),
		(val_max, ":max_level", ":curr_level"),
		
		(try_begin),
			(troop_get_upgrade_troop, ":upgrade", ":troop", 0),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_troop_get_skill_max_from_upgrade", ":troop", ":upgrade", ":skill"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(call_script, "script_kct_troop_get_skill_max_from_tree", ":upgrade", ":skill"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(troop_get_upgrade_troop, ":upgrade", ":troop", 1),
			(gt, ":upgrade", 0),
			
			(call_script, "script_kct_troop_get_skill_max_from_upgrade", ":troop", ":upgrade", ":skill"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
			
			(call_script, "script_kct_troop_get_skill_max_from_tree", ":upgrade", ":skill"),
			(try_begin),
				(lt, reg0, ":max_level"),
				
				(assign, ":max_level", reg0),
				(str_store_troop_name, s10, ":upgrade"),
			(else_try),
				(str_store_troop_name, s10, ":troop"),
			(try_end),
		(try_end),
		
		(assign, reg0, ":max_level"),
	]),

# script_kct_troop_tree_raise_skill_to
	("kct_troop_tree_raise_skill_to",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":skill", 2),
		(store_script_param, ":amount", 3),
		
		(store_skill_level, ":current", ":skill", ":troop"),
		(try_begin),
			(lt, ":current", ":amount"),
			
			(store_sub, ":difference", ":amount", ":current"),
			(troop_raise_skill, ":troop", ":skill", ":difference"),
		(try_end),
		
		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		(try_begin),
			(gt, ":dummy", 0),
			(neq, ":dummy", ":troop"),
			
			(store_skill_level, ":current", ":skill", ":dummy"),
		(try_end),
		(try_begin),
			(gt, ":dummy", 0),
			(neq, ":dummy", ":troop"),
			(lt, ":current", ":amount"),
			
			(store_sub, ":difference", ":amount", ":current"),
			(troop_raise_skill, ":dummy", ":skill", ":difference"),
		(try_end),
		
		(troop_get_upgrade_troop, ":upgrade_1", ":troop", 0),
		(troop_get_upgrade_troop, ":upgrade_2", ":troop", 1),
		(try_begin),
			(gt, ":upgrade_1", 0),
			
			(call_script, "script_kct_troop_tree_raise_skill_to", ":upgrade_1", ":skill", ":amount"),
			
			(gt, ":upgrade_2", 0),
			
			(call_script, "script_kct_troop_tree_raise_skill_to", ":upgrade_2", ":skill", ":amount"),
		(try_end),
	]),

# script_kct_dummy_set_skill
	("kct_dummy_set_skill",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":skill", 2),
		(store_script_param, ":amount", 3),
		
		(store_skill_level, ":points", ":skill", ":troop"),
		(store_sub, ":difference", ":amount", ":points"),
		(troop_raise_skill, ":troop", ":skill", ":difference"),
		
		(try_begin),
			(gt, ":difference", 0),
			
			(troop_get_slot, ":actual_troop", ":troop", cstm_slot_troop_custom_troop),
			
			(troop_get_upgrade_troop, ":upgrade_1", ":actual_troop", 0),
			(troop_get_upgrade_troop, ":upgrade_2", ":actual_troop", 1),
			(try_begin),
				(gt, ":upgrade_1", 0),
				
				(call_script, "script_kct_troop_tree_raise_skill_to", ":upgrade_1", ":skill", ":amount"),
				
				(gt, ":upgrade_2", 0),
				
				(call_script, "script_kct_troop_tree_raise_skill_to", ":upgrade_2", ":skill", ":amount"),
			(try_end),
		(try_end),
	]),

# script_kct_dummy_set_proficiency
	("kct_dummy_set_proficiency",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":proficiency", 2),
		(store_script_param, ":amount", 3),
		
		(store_proficiency_level, ":curr_points", ":troop", ":proficiency"),
		(store_sub, ":difference", ":amount", ":curr_points"),
		(troop_raise_proficiency_linear, ":troop", ":proficiency", ":difference"),
	]),

	# script_kct_get_proficiency_points
	# Points pool from Weapon Master, level and AGI, using the shared
	# trp_cstm_proficiency_requirements cost table (see custom_troops).
	("kct_get_proficiency_points",
	[
		(store_script_param, ":troop", 1),

		(store_skill_level, ":weapon_master", skl_weapon_master, ":troop"),
		(store_mul, ":starting_proficiency", ":weapon_master", CSTM_WP_LEVELS_PER_WM),
		(val_add, ":starting_proficiency", CSTM_WP_LEVELS_START),

		(troop_get_slot, ":points_available", "trp_cstm_proficiency_requirements", ":starting_proficiency"),
		(val_mul, ":points_available", proficiencies_end),

		(store_character_level, ":level", ":troop"),
		(store_mul, ":level_bonus", ":level", CSTM_WP_POINTS_PER_LEVEL),
		(val_add, ":points_available", ":level_bonus"),

		(store_attribute_level, ":agility", ":troop", ca_agility),
		(store_mul, ":agility_bonus", ":agility", CSTM_WP_POINTS_PER_AGI),
		(val_add, ":points_available", ":agility_bonus"),

		(assign, reg0, ":points_available"),
	]),

	# script_kct_get_proficiency_points_spent
	("kct_get_proficiency_points_spent",
	[
		(store_script_param, ":troop", 1),

		(assign, ":points_spent", 0),
		(try_for_range, ":proficiency", 0, proficiencies_end),
			(store_proficiency_level, ":proficiency_level", ":troop", ":proficiency"),
			(troop_get_slot, ":points_requirement", "trp_cstm_proficiency_requirements", ":proficiency_level"),
			(val_add, ":points_spent", ":points_requirement"),
		(try_end),

		(assign, reg0, ":points_spent"),
	]),

	# script_kct_get_proficiency_points_available
	("kct_get_proficiency_points_available",
	[
		(store_script_param, ":troop", 1),

		(call_script, "script_kct_get_proficiency_points", ":troop"),
		(assign, ":points", reg0),
		(call_script, "script_kct_get_proficiency_points_spent", ":troop"),
		(val_sub, ":points", reg0),

		(assign, reg0, ":points"),
	]),

	# script_kct_troop_get_highest_proficiency_from_points
	("kct_troop_get_highest_proficiency_from_points",
	[
		(store_script_param, ":points", 1),

		(assign, ":max_level", 700),
		(assign, ":end_cond", 700),
		(try_for_range, ":proficiency_level", 1, ":end_cond"),
			(troop_get_slot, ":points_required", "trp_cstm_proficiency_requirements", ":proficiency_level"),

			(gt, ":points_required", ":points"),

			(store_sub, ":max_level", ":proficiency_level", 1),
			(assign, ":end_cond", 0),
		(try_end),

		(assign, reg0, ":max_level"),
	]),

	# script_kct_troop_get_proficiency_min_from_points
	# The floor each proficiency box keeps: the starting level the points pool
	# already guarantees (same constant as custom_troops).
	("kct_troop_get_proficiency_min_from_points",
	[
		(assign, reg0, CSTM_WP_LEVELS_START),
	]),

	# script_kct_troop_get_proficiency_max_from_points
	# The highest level this proficiency could be raised to with the points
	# available: the points already spent on it plus the free pool.
	("kct_troop_get_proficiency_max_from_points",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":proficiency", 2),

		(store_proficiency_level, ":curr_level", ":troop", ":proficiency"),
		(troop_get_slot, ":max_points", "trp_cstm_proficiency_requirements", ":curr_level"),
		(call_script, "script_kct_get_proficiency_points_available", ":troop"),
		(val_add, ":max_points", reg0),
		(call_script, "script_kct_troop_get_highest_proficiency_from_points", ":max_points"),
	]),

# script_kct_cf_troop_stats_are_different
	("kct_cf_troop_stats_are_different",
	[
		(store_script_param, ":troop_1", 1),
		(store_script_param, ":troop_2", 2),
		
		(assign, ":troops_different", 0),
		
		(try_for_range, ":attribute", 0, 4),
			(eq, ":troops_different", 0),
			
			(store_attribute_level, reg0, ":troop_1", ":attribute"),
			(store_attribute_level, reg1, ":troop_2", ":attribute"),
			(neq, reg0, reg1),
			
			(assign, ":troops_different", 1),
		(try_end),
		
		(try_for_range, ":skill", 0, 42),
			(eq, ":troops_different", 0),
			
			(store_skill_level, reg0, ":skill", ":troop_1"),
			(store_skill_level, reg1, ":skill",":troop_2"),
			(neq, reg0, reg1),
			
			(assign, ":troops_different", 1),
		(try_end),
		
		(try_for_range, ":proficiency", 0, 7),
			(eq, ":troops_different", 0),
			
			(store_proficiency_level, reg0, ":troop_1", ":proficiency"),
			(store_proficiency_level, reg1, ":troop_2", ":proficiency"),
			(neq, reg0, reg1),
			
			(assign, ":troops_different", 1),
		(try_end),
		
		(eq, ":troops_different", 1),
	]),

# script_kct_cf_troop_equipments_are_different
	("kct_cf_troop_equipments_are_different",
	[
		(store_script_param, ":troop_1", 1),
		(store_script_param, ":troop_2", 2),
		
		(assign, ":troops_different", 0),
		
		(troop_get_inventory_capacity, ":capacity", ":troop_1"),
		(try_for_range, ":inv_slot", 0, ":capacity"),
			(eq, ":troops_different", 0),
			
			# Get item from first troop and check if both troops have the same number of this item
			(troop_get_inventory_slot, ":item", ":troop_1", ":inv_slot"),
			(try_begin),
				(gt, ":item", 0),
				#(str_store_item_name, s0, ":item"),
				#(display_message, "@Checking {s0}"),
				
				(store_item_kind_count, reg0, ":item", ":troop_1"),
				(store_item_kind_count, reg1, ":item", ":troop_2"),
				(neq, reg0, reg1),
				
				(assign, ":troops_different", 1),
			(try_end),
			
			# As above for item the second troop has
			(troop_get_inventory_slot, ":item", ":troop_2", ":inv_slot"),
			(gt, ":item", 0),
			#(str_store_item_name, s0, ":item"),
			#(display_message, "@Checking {s0}"),
			
			(store_item_kind_count, reg0, ":item", ":troop_1"),
			(store_item_kind_count, reg1, ":item", ":troop_2"),
			(neq, reg0, reg1),
			
			(assign, ":troops_different", 1),
		(try_end),
		
		(eq, ":troops_different", 1),
	]),

# script_kct_cf_troop_has_horse
	("kct_cf_troop_has_horse",
	[
		(store_script_param, ":troop", 1),
		
		(assign, ":has_horse", 0),
		
		(troop_get_inventory_capacity, ":capacity", ":troop"),
		(try_for_range, ":inv_slot", 0, ":capacity"),
			(troop_get_inventory_slot, ":item", ":troop", ":inv_slot"),
			(gt, ":item", 0),
			
			(item_get_type, ":item_type", ":item"),
			(eq, ":item_type", itp_type_horse),
			
			(assign, ":has_horse", 1),
		(try_end),
		
		(eq, ":has_horse", 1),
	]),

# script_kct_cf_troop_has_bow_or_crossbow
	("kct_cf_troop_has_bow_or_crossbow",
	[
		(store_script_param, ":troop", 1),
		
		(assign, ":has_bow_or_crossbow", 0),
		
		(troop_get_inventory_capacity, ":capacity", ":troop"),
		(try_for_range, ":inv_slot", 0, ":capacity"),
			(troop_get_inventory_slot, ":item", ":troop", ":inv_slot"),
			(gt, ":item", 0),
			
			(item_get_type, ":item_type", ":item"),
			(this_or_next|eq, ":item_type", itp_type_bow),
			(eq, ":item_type", itp_type_crossbow),
			
			(assign, ":has_bow_or_crossbow", 1),
		(try_end),
		
		(eq, ":has_bow_or_crossbow", 1),
	]),

# script_kct_troop_copy_stats
	("kct_troop_copy_stats",
	[
		(store_script_param, ":destination_troop", 1),
		(store_script_param, ":source_troop", 2),
		
		(call_script, "script_kct_troop_reset_stats", ":destination_troop"),
		
		(try_for_range, ":attribute", 0, 4),
			(store_attribute_level, ":attribute_level", ":source_troop", ":attribute"),
			(troop_raise_attribute, ":destination_troop", ":attribute", ":attribute_level"),
		(try_end),
		
		(try_for_range, ":skill", 0, 42),
			(store_skill_level, ":skill_level", ":skill", ":source_troop"),
			(troop_raise_skill, ":destination_troop", ":skill", ":skill_level"),
		(try_end),
		
		(try_for_range, ":proficiency", 0, 7),
			(store_proficiency_level, ":proficiency_level", ":source_troop", ":proficiency"),
			(troop_raise_proficiency_linear, ":destination_troop", ":proficiency", ":proficiency_level"),
		(try_end),
		
		#(str_store_troop_name, s0, ":source_troop"),
		#(str_store_troop_name, s1, ":destination_troop"),
		#(display_log_message, "@Copying {s0} to {s1}"),
	]),

# script_kct_troop_copy_stats_if_higher
	("kct_troop_copy_stats_if_higher",
	[
		(store_script_param, ":destination_troop", 1),
		(store_script_param, ":source_troop", 2),
		
		(try_for_range, ":attribute", 0, 4),
			(store_attribute_level, ":source_level", ":source_troop", ":attribute"),
			(store_attribute_level, ":destination_level", ":destination_troop", ":attribute"),
			(store_sub, ":difference", ":source_level", ":destination_level"),
			(gt, ":difference", 0),
			
			(troop_raise_attribute, ":destination_troop", ":attribute", ":difference"),
		(try_end),
		
		(try_for_range, ":skill", 0, 42),
			(store_skill_level, ":source_level", ":skill", ":source_troop"),
			(store_skill_level, ":destination_level", ":skill", ":destination_troop"),
			(store_sub, ":difference", ":source_level", ":destination_level"),
			(gt, ":difference", 0),
			
			(troop_raise_skill, ":destination_troop", ":skill", ":difference"),
		(try_end),
		
		#(str_store_troop_name, s0, ":source_troop"),
		#(str_store_troop_name, s1, ":destination_troop"),
		#(display_log_message, "@Copying {s0} to {s1}"),
	]),

# script_kct_troop_tree_copy_stats_if_higher
	("kct_troop_tree_copy_stats_if_higher",
	[
		(store_script_param, ":destination_base_troop", 1),
		(store_script_param, ":source_troop", 2),
		
		(call_script, "script_kct_troop_copy_stats_if_higher", ":destination_base_troop", ":source_troop"),
		#(str_store_troop_name, s0, ":destination_base_troop"),
		#(display_message, "@Copying stats to {s0}"),
		
		# In the case of troops that have a corresponding dummy troop, copy stats to the dummy troop too
		(troop_get_slot, ":destination_base_troop_dummy", ":destination_base_troop", cstm_slot_troop_dummy),
		(try_begin),
			(gt, ":destination_base_troop_dummy", 0),
			(neq, ":destination_base_troop_dummy", ":source_troop"),
			
			(call_script, "script_kct_troop_copy_stats_if_higher", ":destination_base_troop_dummy", ":source_troop"),
		(try_end),
		
		(troop_get_upgrade_troop, ":upgrade_1", ":destination_base_troop", 0),
		(troop_get_upgrade_troop, ":upgrade_2", ":destination_base_troop", 1),
		
		(try_begin),
			(gt, ":upgrade_1", 0),
			
			(call_script, "script_kct_troop_tree_copy_stats_if_higher", ":upgrade_1", ":source_troop"),
		(try_end),
		(try_begin),
			(gt, ":upgrade_2", 0),
			
			(call_script, "script_kct_troop_tree_copy_stats_if_higher", ":upgrade_2", ":source_troop"),
		(try_end),
	]),

# script_kct_troop_tree_update_stat_minimums
	("kct_troop_tree_update_stat_minimums",
	[
		(store_script_param, ":troop", 1),
		
		(assign, ":updated", 0),
		
		(try_for_range, ":attribute", 0, attributes_end),
			(store_attribute_level, ":level", ":troop", ":attribute"),
			(call_script, "script_kct_troop_get_attribute_min_from_tree", ":troop", ":troop", ":attribute"),
			(gt, reg0, ":level"),
			
			(store_sub, ":difference", reg0, ":level"),
			(troop_raise_attribute, ":troop", ":attribute", ":difference"),
			(assign, ":updated", 1),
		(try_end),
		
		(try_for_range, ":skill", 0, skills_end),
			(store_skill_level, ":level", ":skill", ":troop"),
			(call_script, "script_kct_troop_get_skill_min_from_tree", ":troop", ":troop", ":skill"),
			(gt, reg0, ":level"),
			
			(store_sub, ":difference", reg0, ":level"),
			(troop_raise_skill, ":troop", ":skill", ":difference"),
			(assign, ":updated", 1),
		(try_end),
		
		(try_begin),
			(eq, ":updated", 1),
			
			(call_script, "script_kct_troop_tree_copy_stats_if_higher", ":troop", ":troop"),
		(try_end),
		
		(troop_get_slot, ":base_troop", ":troop", cstm_slot_troop_base_troop),
		(try_begin),
			(gt, ":base_troop", 0),
			
			(call_script, "script_kct_troop_tree_update_stat_minimums", ":base_troop"),
		(try_end),
	]),

# script_kct_setup_item_arrays
	("kct_setup_item_arrays",
	[
		# Empty arrays
		(try_for_range, ":array", cstm_items_arrays_begin, cstm_items_arrays_end),
			(troop_get_slot, ":num_items", ":array", cstm_slot_array_num_items),
			(try_for_range, ":item_index", 0, ":num_items"),
				(store_add, ":slot", ":item_index", cstm_slot_array_items_begin),
				(troop_set_slot, ":array", ":slot", 0),
			(try_end),
			
			(troop_set_slot, ":array", cstm_slot_array_num_items, 0),
		(try_end),
		
		# Add items
		(assign, ":end_cond", all_items_end),
		(try_for_range, ":item", all_items_begin, ":end_cond"),
			(try_begin),
				(call_script, "script_kct_cf_item_is_eligible_equipment_option", ":item"),
				
				(item_get_type, ":type", ":item"),
				(try_begin),
					(call_script, "script_kct_get_items_array", ":type"),
					(gt, reg0, 0),
					
					(assign, ":array", reg0),
					
					(troop_get_slot, ":num_items", ":array", cstm_slot_array_num_items),
					(store_add, ":slot", ":num_items", cstm_slot_array_items_begin),
					(troop_set_slot, ":array", ":slot", ":item"),
					(val_add, ":num_items", 1),
					(troop_set_slot, ":array", cstm_slot_array_num_items, ":num_items"),
				(try_end),
			(try_end),
		(try_end),
		
		# Sort arrays by item value using bubble sort
		(try_for_range, ":array", cstm_items_arrays_begin, cstm_items_arrays_end),
			(troop_get_slot, ":num_items", ":array", cstm_slot_array_num_items),
			(assign, ":end_cond", ":num_items"),
			(assign, ":swapped", 0),
			(try_for_range, ":unused", 0, ":end_cond"),
				(try_for_range, ":item_index", 1, ":num_items"),
					(store_sub, ":prev_item_index", ":item_index", 1),
					
					(store_add, ":prev_slot", ":prev_item_index", cstm_slot_array_items_begin),
					(troop_get_slot, ":prev_item", ":array", ":prev_slot"),
					(store_add, ":slot", ":item_index", cstm_slot_array_items_begin),
					(troop_get_slot, ":item", ":array", ":slot"),
					
					(item_get_value, ":prev_value", ":prev_item"),
					(item_get_value, ":value", ":item"),
					(lt, ":prev_value", ":value"),
					
					(troop_set_slot, ":array", ":prev_slot", ":item"),
					(troop_set_slot, ":array", ":slot", ":prev_item"),
					
					(assign, ":swapped", 1),
				(try_end),
				
				(eq, ":swapped", 0),
				
				(assign, ":end_cond", 0),
			(try_end),
		(try_end),
	]),

# script_kct_cf_item_is_ranged
	("kct_cf_item_is_ranged",
	[
		(store_script_param, ":item", 1),
		
		(item_get_type, ":item_type", ":item"),
		(call_script, "script_kct_cf_item_type_is_ranged", ":item_type"),
	]),

# script_kct_cf_item_type_is_ranged
	("kct_cf_item_type_is_ranged",
	[
		(store_script_param, ":item_type", 1),
		
		(this_or_next|eq, ":item_type", itp_type_bow),
		(this_or_next|eq, ":item_type", itp_type_crossbow),
		(this_or_next|eq, ":item_type", itp_type_thrown),
		(this_or_next|eq, ":item_type", itp_type_pistol),
		(eq, ":item_type", itp_type_musket),
	]),

# script_kct_cf_item_is_missile
	("kct_cf_item_is_missile",
	[
		(store_script_param, ":item", 1),
		
		(item_get_type, ":item_type", ":item"),
		(call_script, "script_kct_cf_item_type_is_missile", ":item_type"),
	]),

# script_kct_cf_item_type_is_missile
	("kct_cf_item_type_is_missile",
	[
		(store_script_param, ":item_type", 1),
		
		(this_or_next|eq, ":item_type", itp_type_arrows),
		(this_or_next|eq, ":item_type", itp_type_bolts),
		(eq, ":item_type", itp_type_bullets),
	]),

# script_kct_cf_cci_imod_appropriate_for_item
	("kct_cf_cci_imod_appropriate_for_item",
	[
		(store_script_param, ":item_type", 1),
		(store_script_param, ":imod", 2),
		#(assign, reg0, ":item_type"),
		#(display_message, "@Item type: {reg0}"),
		(assign, ":continue", 1),
		## FILTER - IMODs that are always blocked.
		(try_begin),
			# Inactive IMODs.	These have no game effects so they're removed for now.
			(this_or_next|eq, ":imod", imod_superb),
			(this_or_next|eq, ":imod", imod_well_made),
			(this_or_next|eq, ":imod", imod_sharp),
			(this_or_next|eq, ":imod", imod_deadly),
			(this_or_next|eq, ":imod", imod_exquisite),
			(this_or_next|eq, ":imod", imod_powerful),
			# Freshness IMODs.	Not Applicable to Equipment.
			(this_or_next|eq, ":imod", imod_fresh),
			(this_or_next|eq, ":imod", imod_day_old),
			(this_or_next|eq, ":imod", imod_two_day_old),
			(this_or_next|eq, ":imod", imod_smelling),
			(eq, ":imod", imod_rotten),
			(assign, ":continue", 0),
		(try_end),
		(eq, ":continue", 1),
		
		(assign, ":continue", 0),
		(try_begin),
			### WEAPON FILTER ###
			# Ranged weapons
			(assign, ":is_ranged", 0),
			(try_begin),
				(call_script, "script_kct_cf_item_type_is_ranged", ":item_type"),
				(assign, ":is_ranged", 1),
			(try_end),
			(this_or_next|eq, ":is_ranged", 1),
			(this_or_next|eq, ":item_type", itp_type_one_handed_wpn), # One-Handed
			(this_or_next|eq, ":item_type", itp_type_two_handed_wpn), # Two-Handed
			(eq, ":item_type", itp_type_polearm), # Polearm
			
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_strong),
			(this_or_next|eq, ":imod", imod_heavy),
			(this_or_next|eq, ":imod", imod_masterwork),
			(this_or_next|eq, ":imod", imod_tempered),
			(this_or_next|eq, ":imod", imod_balanced),
			#(this_or_next|eq, ":imod", imod_fine),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### AMMUNITION FILTER ###
			(call_script, "script_kct_cf_item_type_is_missile", ":item_type"), # Ammunition
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_large_bag),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### SHIELD FILTER ###
			(eq, ":item_type", itp_type_shield), # Shields
			# Valid IMODs.
			#(this_or_next|eq, ":imod", imod_lordly),
			(this_or_next|eq, ":imod", imod_reinforced),
			#(this_or_next|eq, ":imod", imod_hardened),
			(this_or_next|eq, ":imod", imod_thick),
			#(this_or_next|eq, ":imod", imod_sturdy),
			#(this_or_next|eq, ":imod", imod_heavy),
			#(this_or_next|eq, ":imod", imod_masterwork),
			#(this_or_next|eq, ":imod", imod_balanced),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### ARMOR FILTER ###
			(is_between, ":item_type", itp_type_head_armor, itp_type_hand_armor + 1),
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_lordly),
			(this_or_next|eq, ":imod", imod_reinforced),
			(this_or_next|eq, ":imod", imod_hardened),
			(this_or_next|eq, ":imod", imod_thick),
			(this_or_next|eq, ":imod", imod_sturdy),
			#(this_or_next|eq, ":imod", imod_heavy),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### MOUNTS FILTER ###
			(eq, ":item_type", itp_type_horse), # Horses
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_champion),
			(this_or_next|eq, ":imod", imod_spirited),
			#(this_or_next|eq, ":imod", imod_lordly),
			#(this_or_next|eq, ":imod", imod_sturdy),
			(this_or_next|eq, ":imod", imod_heavy),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
		(try_end),
		
		(eq, ":continue", 1),
	]),

# script_kct_cf_troop_can_use_item_with_modifier
	("kct_cf_troop_can_use_item_with_modifier",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":item", 2),
		(store_script_param, ":imod", 3),
		
		(item_get_type, ":item_type", ":item"),
		
		# Get requirement and adjust with modifiers
		(item_get_difficulty, ":requirement", ":item"),
		(try_begin),
			(eq, ":item_type", itp_type_horse),
			
			(try_begin),
				(eq, ":imod", imod_champion),
				(val_add, ":requirement", 2),
			(else_try),
				(eq, ":imod", imod_stubborn),
				(val_add, ":requirement", 1),
			(try_end),
		(else_try),
			(this_or_next|eq, ":item_type", itp_type_bow),
			(eq, ":item_type", itp_type_thrown),
			(gt, ":requirement", 0),
			
			(try_begin),
				(eq, ":imod", imod_masterwork),
				(val_add, ":requirement", 4),
			(else_try),
				(eq, ":imod", imod_strong),
				(val_add, ":requirement", 2),
			(else_try),
				(eq, ":imod", imod_heavy),
				(val_add, ":requirement", 1),
			(try_end),
		(try_end),
		
		# Get relevant stat
		(try_begin),
			(eq, ":item_type", itp_type_horse),
			(store_skill_level, ":stat", skl_riding, ":troop"),
		(else_try),
			(eq, ":item_type", itp_type_shield),
			(store_skill_level, ":stat", skl_shield, ":troop"),
		(else_try),
			(eq, ":item_type", itp_type_bow),
			(store_skill_level, ":stat", skl_power_draw, ":troop"),
		(else_try),
			(eq, ":item_type", itp_type_thrown),
			(store_skill_level, ":stat", skl_power_throw, ":troop"),
		(else_try),
			(store_attribute_level, ":stat", ":troop", ca_strength),
		(try_end),
		
		(assign, reg0, ":stat"),
		(assign, reg1, ":requirement"),
		
		# Compare
		(ge, ":stat", ":requirement"),
	]),

# script_kct_store_item_requirement_stat_to_s0
	("kct_store_item_requirement_stat_to_s0",
	[
		(store_script_param, ":item", 1),
		
		(item_get_type, ":item_type", ":item"),
		(try_begin),
			(eq, ":item_type", itp_type_horse),
			(str_store_string, s0, "@Riding skill"),
		(else_try),
			(eq, ":item_type", itp_type_shield),
			(str_store_string, s0, "@Shield skill"),
		(else_try),
			(eq, ":item_type", itp_type_bow),
			(str_store_string, s0, "@Power Draw"),
		(else_try),
			(eq, ":item_type", itp_type_thrown),
			(str_store_string, s0, "@Power Throw"),
		(else_try),
			(str_store_string, s0, "@Strength"),
		(try_end),
	]),

# script_kct_item_get_price_with_modifier
	("kct_item_get_price_with_modifier",
	[
		(store_script_param, ":item", 1),
		(store_script_param, ":imod", 2),
		
		(item_get_type, ":type", ":item"),
		(call_script, "script_kct_item_type_get_cost_modifier", ":type", ":imod"),
		(store_add, ":modifier", reg0, 100),
		(store_div, ":reduced_modifier", ":modifier", CSTM_IMOD_COST_DIVISOR),
		(val_add, ":reduced_modifier", 100),
		
		(store_mul, ":price_multiplier", ":reduced_modifier", 100),
		(val_div, ":price_multiplier", ":modifier"),
		
		(store_item_value, ":value", ":item"),
		(val_mul, ":value", ":modifier"),
		(val_div, ":value", 100),
		(val_mul, ":value", ":price_multiplier"),
		(val_div, ":value", 100),
		
		(assign, reg0, ":value"),
		(assign, reg1, ":price_multiplier"),
	]),

# script_kct_troop_get_inventory_value
	("kct_troop_get_inventory_value",
	[
		(store_script_param, ":troop", 1),
		
		(troop_get_inventory_capacity, ":capacity", ":troop"),
		
		(try_for_range, ":slot", cstm_slot_troop_armour_values_begin, cstm_slot_troop_horse_count + 1),
			(troop_set_slot, ":troop", ":slot", 0),
		(try_end),
		
		(try_for_range, ":slot", 0, ":capacity"),
			(troop_get_inventory_slot, ":item", ":troop", ":slot"),
			(troop_get_inventory_slot_modifier, ":imod", ":troop", ":slot"),
			(gt, ":item", 0),
			
			(item_get_type, ":item_type", ":item"),
			(call_script, "script_kct_item_get_price_with_modifier", ":item", ":imod"),
			(assign, ":value", reg0),
			(try_begin),
				(is_between, ":item_type", itp_type_head_armor, itp_type_pistol),
				
				(store_add, ":armour_values_slot", cstm_slot_troop_armour_values_begin - itp_type_head_armor, ":item_type"),
				(store_add, ":armour_count_slot", cstm_slot_troop_armour_counts_begin - itp_type_head_armor, ":item_type"),
				
				#(assign, reg0, ":armour_values_slot"),
				#(assign, reg1, ":armour_count_slot"),
				#(assign, reg2, ":item_type"),
				#(display_message, "@Writing armour type {reg2} value to {reg0} and count to {reg1}"),
				
				(troop_get_slot, ":values", ":troop", ":armour_values_slot"),
				(val_add, ":values", ":value"),
				(troop_set_slot, ":troop", ":armour_values_slot", ":values"),
				
				(troop_get_slot, ":count", ":troop", ":armour_count_slot"),
				(val_add, ":count", 1),
				(troop_set_slot, ":troop", ":armour_count_slot", ":count"),
			(else_try),
				(eq, ":item_type", itp_type_shield),
				
				(troop_get_slot, ":values", ":troop", cstm_slot_troop_shield_values),
				(val_add, ":values", ":value"),
				(troop_set_slot, ":troop", cstm_slot_troop_shield_values, ":values"),
				
				(troop_get_slot, ":count", ":troop", cstm_slot_troop_shield_count),
				(val_add, ":count", 1),
				(troop_set_slot, ":troop", cstm_slot_troop_shield_count, ":count"),
			(else_try),
				(eq, ":item_type", itp_type_horse),
				
				(troop_get_slot, ":values", ":troop", cstm_slot_troop_horse_values),
				(val_add, ":values", ":value"),
				(troop_set_slot, ":troop", cstm_slot_troop_horse_values, ":values"),
				
				(troop_get_slot, ":count", ":troop", cstm_slot_troop_horse_count),
				(val_add, ":count", 1),
				(troop_set_slot, ":troop", cstm_slot_troop_horse_count, ":count"),
			(else_try),
				(troop_is_guarantee_ranged, ":troop"),
				(assign, ":continue", 0),
				(try_begin),
					(call_script, "script_kct_cf_item_is_ranged", ":item"),
					(assign, ":continue", 1),
				(else_try),
					(call_script, "script_kct_cf_item_is_missile", ":item"),
					(assign, ":continue", 1),
				(else_try),
				(try_end),
				(eq, ":continue", 1),
				
				(troop_get_slot, ":values", ":troop", cstm_slot_troop_ranged_values),
				(val_add, ":values", ":value"),
				(troop_set_slot, ":troop", cstm_slot_troop_ranged_values, ":values"),
				
				(troop_get_slot, ":count", ":troop", cstm_slot_troop_ranged_count),
				(val_add, ":count", 1),
				(troop_set_slot, ":troop", cstm_slot_troop_ranged_count, ":count"),
			(else_try),
				(assign, reg0, cstm_slot_troop_weapon_values),
				(assign, reg1, cstm_slot_troop_weapon_count),
				#(display_message, "@Writing weapon value to {reg0} and count to {reg1}"),
				
				(troop_get_slot, ":values", ":troop", cstm_slot_troop_weapon_values),
				(val_add, ":values", ":value"),
				(troop_set_slot, ":troop", cstm_slot_troop_weapon_values, ":values"),
				
				(troop_get_slot, ":count", ":troop", cstm_slot_troop_weapon_count),
				(val_add, ":count", 1),
				(troop_set_slot, ":troop", cstm_slot_troop_weapon_count, ":count"),
			(try_end),
		(try_end),
		
		(assign, ":inventory_value", 0),
		(try_for_range, ":item_type", itp_type_head_armor, itp_type_pistol),
			(store_add, ":armour_values_slot", cstm_slot_troop_armour_values_begin - itp_type_head_armor, ":item_type"),
			(store_add, ":armour_count_slot", cstm_slot_troop_armour_counts_begin - itp_type_head_armor, ":item_type"),
			
			#(assign, reg0, ":armour_values_slot"),
			#(assign, reg1, ":armour_count_slot"),
			#(assign, reg2, ":item_type"),
			#(display_message, "@Getting armour type {reg2} values from {reg0} and count from {reg1}"),
			
			(troop_get_slot, ":values", ":troop", ":armour_values_slot"),
			(troop_get_slot, ":count", ":troop", ":armour_count_slot"),
			
			(gt, ":count", 0),
			
			(store_div, ":average_value", ":values", ":count"),
			(val_add, ":inventory_value", ":average_value"),
			
			#(assign, reg0, ":values"),
			#(assign, reg1, ":count"),
			#(assign, reg2, ":average_value"),
			#(assign, reg3, ":item_type"),
			#(display_message, "@Armour type {reg3}: {reg0} / {reg1} = {reg2}"),
		(try_end),
		
		(assign, ":weapon_slots_used", 0),
		(try_begin),
			(troop_is_guarantee_ranged, ":troop"),
			
			(troop_get_slot, ":values", ":troop", cstm_slot_troop_ranged_values),
			(troop_get_slot, ":count", ":troop", cstm_slot_troop_ranged_count),
			
			(gt, ":count", 0),
			
			(store_div, ":average_value", ":values", ":count"),
			(assign, ":multiplier", ":count"),
			(val_min, ":multiplier", 2),
			(val_mul, ":average_value", ":multiplier"),
			(val_add, ":inventory_value", ":average_value"),
			(val_add, ":weapon_slots_used", ":multiplier"),
			
			#(assign, reg0, ":values"),
			#(assign, reg1, ":count"),
			#(assign, reg2, ":average_value"),
			#(display_message, "@Ranged weapons: ({reg0} / {reg1}) * 2 = {reg2}"),
		(try_end),
		
		(try_begin),
			# There's no operation to check if shield is guaranteed, so this will simply be assumed (makes more sense to use average shield value even if it's not guaranteed anyway)
			(troop_get_slot, ":values", ":troop", cstm_slot_troop_shield_values),
			(troop_get_slot, ":count", ":troop", cstm_slot_troop_shield_count),
			
			(gt, ":count", 0),
			
			(store_div, ":average_value", ":values", ":count"),
			(val_add, ":inventory_value", ":average_value"),
			(val_add, ":weapon_slots_used", 1),
			
			#(assign, reg0, ":values"),
			#(assign, reg1, ":count"),
			#(assign, reg2, ":average_value"),
			#(display_message, "@Shields: ({reg0} / {reg1}) * 2 = {reg2}"),
		(try_end),
		
		(troop_get_slot, ":values", ":troop", cstm_slot_troop_weapon_values),
		(troop_get_slot, ":count", ":troop", cstm_slot_troop_weapon_count),
		
		(try_begin),
			(gt, ":count", 0),
			
			(store_div, ":average_value", ":values", ":count"),
			(store_sub, ":multiplier", 4, ":weapon_slots_used"),
			(val_min, ":multiplier", ":count"),
			(val_mul, ":average_value", ":multiplier"),
			(val_add, ":inventory_value", ":average_value"),
			
			#(assign, reg0, ":values"),
			#(assign, reg1, ":count"),
			#(assign, reg2, ":average_value"),
			#(display_message, "@Weapons: ({reg0} / {reg1}) * 2 = {reg2}"),
		(try_end),
		
		(troop_get_slot, ":values", ":troop", cstm_slot_troop_horse_values),
		(troop_get_slot, ":count", ":troop", cstm_slot_troop_horse_count),
		
		(try_begin),
			(gt, ":count", 0),
			
			(store_div, ":average_value", ":values", ":count"),
			(str_clear, s0),
			(try_begin),
				(neg|troop_is_guarantee_horse, ":troop"),
				(neg|troop_is_hero, ":troop"),
				
				(val_div, ":average_value", 2),
				
				(str_store_string, s0, "@ / 2"),
			(try_end),
			(val_add, ":inventory_value", ":average_value"),
			
			#(assign, reg0, ":values"),
			#(assign, reg1, ":count"),
			#(assign, reg2, ":average_value"),
			#(display_message, "@Horses: ({reg0} / {reg1}){s0} = {reg2}"),
		(try_end),
		
		(assign, reg0, ":inventory_value"),
	]),

# script_kct_get_item_from_array
	("kct_get_item_from_array",
	[
		(store_script_param, ":item_array", 1),
		(store_script_param, ":item_index", 2),
		
		(store_add, ":slot", cstm_slot_array_items_begin, ":item_index"),
		(troop_get_slot, reg0, ":item_array", ":slot"),
	]),

# script_kct_troop_copy_inventory
	("kct_troop_copy_inventory",
	[
		(store_script_param, ":destination_troop", 1),
		(store_script_param, ":source_troop", 2),
		
		(troop_clear_inventory, ":destination_troop"),
		
		(troop_get_inventory_capacity, ":num_slots", ":source_troop"),
		(try_for_range, ":slot", 0, ":num_slots"),
			(troop_get_inventory_slot, ":item", ":source_troop", ":slot"),
			(troop_get_inventory_slot_modifier, ":modifier", ":source_troop", ":slot"),
			
			(troop_set_inventory_slot, ":destination_troop", ":slot", ":item"),
			(troop_set_inventory_slot_modifier, ":destination_troop", ":slot", ":modifier"),
		(try_end),
	]),

# script_kct_troop_tree_copy_inventory_if_unmodified
	("kct_troop_tree_copy_inventory_if_unmodified",
	[
		(store_script_param, ":destination_base_troop", 1),
		(store_script_param, ":source_troop", 2),
		
		(try_begin),
			(troop_slot_eq, ":destination_base_troop", cstm_slot_troop_equipment_modified, 0),
			
			(call_script, "script_kct_troop_copy_inventory", ":destination_base_troop", ":source_troop"),
			(troop_sort_inventory, ":destination_base_troop"),
			(troop_equip_items, ":destination_base_troop"),
			
			(troop_get_class, ":class", ":source_troop"),
			(troop_set_class, ":destination_base_troop", ":class"),
			
			(try_begin),
				(troop_get_slot, ":dummy", ":destination_base_troop", cstm_slot_troop_dummy),
				(gt, ":dummy", 0),
				(neq, ":dummy", ":source_troop"),
				
				(call_script, "script_kct_troop_copy_inventory", ":dummy", ":source_troop"),
				(troop_sort_inventory, ":dummy"),
				(troop_equip_items, ":dummy"),
			(try_end),
			
			(troop_get_upgrade_troop, ":upgrade_1", ":destination_base_troop", 0),
			(troop_get_upgrade_troop, ":upgrade_2", ":destination_base_troop", 1),
			
			(try_begin),
				(gt, ":upgrade_1", 0),
				
				(call_script, "script_kct_troop_tree_copy_inventory_if_unmodified", ":upgrade_1", ":source_troop"),
				
				(gt, ":upgrade_2", 0),
				
				(call_script, "script_kct_troop_tree_copy_inventory_if_unmodified", ":upgrade_2", ":source_troop"),
			(try_end),
		(try_end),
	]),

# script_kct_copy_custom_troop_to_dummy
	("kct_copy_custom_troop_to_dummy",
	[
		(store_script_param, ":custom_troop", 1),
		
		(troop_get_slot, ":dummy", ":custom_troop", cstm_slot_troop_dummy),
		
		## STATS
		(call_script, "script_kct_troop_copy_stats", ":dummy", ":custom_troop"),
		
		## INVENTORY
		(call_script, "script_kct_troop_copy_inventory", ":dummy", ":custom_troop"),
		
		#(str_store_troop_name, s0, ":custom_troop"),
		#(assign, reg0, ":custom_troop"),
		#(assign, reg1, ":dummy"),
		#(display_log_message, "@Copying {s0} ({reg0}) to dummy: {reg1}"),
	]),

# script_kct_replace_custom_troop_with_dummy
	("kct_replace_custom_troop_with_dummy",
	[
		(store_script_param, ":custom_troop", 1),
		
		(troop_get_slot, ":dummy", ":custom_troop", cstm_slot_troop_dummy),
		
		## NAME
		(call_script, "script_kct_troop_refresh_name", ":custom_troop"),
		
		## STATS
		(call_script, "script_kct_troop_copy_stats", ":custom_troop", ":dummy"),
		
		## INVENTORY
		(call_script, "script_kct_troop_copy_inventory", ":custom_troop", ":dummy"),
		(troop_sort_inventory, ":custom_troop"),
		(troop_equip_items, ":custom_troop"),
		
	]),

# script_kct_get_grid_position
	("kct_get_grid_position",
	[
		(store_script_param, ":index", 1),
		(store_script_param, ":num_items", 2),
		(store_script_param, ":num_cols", 3),
		(store_script_param, ":col_width", 4),
		(store_script_param, ":col_height", 5),
		
		(store_mod, ":x", ":index", ":num_cols"),
		(store_mul, ":pos_x", ":x", ":col_width"),
		
		(store_sub, ":row", ":index", ":x"),
		(val_div, ":row", ":num_cols"),
		(val_sub, ":num_items", 1),
		(store_div, ":num_rows", ":num_items", ":num_cols"),
		(val_add, ":num_rows", 1),
		(store_sub, ":pos_y", ":num_rows", ":row"),
		(val_sub, ":pos_y", 1),
		(val_mul, ":pos_y", ":col_height"),
		
		(assign, reg0, ":pos_x"),
		(assign, reg1, ":pos_y"),
	]),

# script_kct_create_scrollable_container
	("kct_create_scrollable_container",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		(store_script_param, ":size_x", 3),
		(store_script_param, ":size_y", 4),
		
		(str_clear, s0),
		(call_script, "script_kct_create_text_overlay", "str_s0", ":pos_x", ":pos_y", 1000, ":size_x", ":size_y", tf_scrollable_style_2),
	]),

# script_kct_create_item_overlay
	("kct_create_item_overlay",
	[
		(store_script_param, ":item", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size", 4),
		
		(set_fixed_point_multiplier, 1000),
		(create_mesh_overlay_with_item_id, reg1, ":item"),
		(position_set_x, pos2, ":pos_x"),
		(position_set_y, pos2, ":pos_y"),
		(overlay_set_position, reg1, pos2),
		(position_set_x, pos3, ":size"),
		(position_set_y, pos3, ":size"),
		(overlay_set_size, reg1, pos3),
	]),

# script_kct_create_combo_label_overlay
	("kct_create_combo_label_overlay",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		
		(set_fixed_point_multiplier, 1000),
		(create_combo_label_overlay, reg1),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
	]),

# script_kct_create_number_box_overlay
	("kct_create_number_box_overlay",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		(store_script_param, ":min_value", 3),
		(store_script_param, ":max_value", 4),
		
		(set_fixed_point_multiplier, 1000),
		(create_number_box_overlay, reg1, ":min_value", ":max_value"),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
	]),

# script_kct_item_type_get_cost_modifier
	("kct_item_type_get_cost_modifier",
	[
		(store_script_param, ":item_type", 1),
		(store_script_param, ":imod", 2),
		
		(assign, ":cost_modifier", 0),
		
		# Armour modifiers
		(try_begin),
			(is_between, ":item_type", itp_type_head_armor, itp_type_hand_armor + 1),
			
			(try_begin),
				(eq, ":imod", imod_lordly),
				(assign, ":cost_modifier", 1050),
			(else_try),
				(eq, ":imod", imod_reinforced),
				(assign, ":cost_modifier", 550),
			(else_try),
				(eq, ":imod", imod_hardened),
				(assign, ":cost_modifier", 290),
			(else_try),
				(eq, ":imod", imod_thick),
				(assign, ":cost_modifier", 160),
			(else_try),
				(eq, ":imod", imod_sturdy),
				(assign, ":cost_modifier", 70),
			(else_try),
				(eq, ":imod", imod_crude),
				(assign, ":cost_modifier", -17),
			(else_try),
				(eq, ":imod", imod_battered),
				(assign, ":cost_modifier", -25),
			(else_try),
				(eq, ":imod", imod_ragged),
				(assign, ":cost_modifier", -30),
			(else_try),
				(eq, ":imod", imod_rusty),
				(assign, ":cost_modifier", -45),
			(else_try),
				(eq, ":imod", imod_tattered),
				(assign, ":cost_modifier", -50),
			(else_try),
				(eq, ":imod", imod_cracked),
				(assign, ":cost_modifier", -50),
			(try_end),
		(else_try),
			(eq, ":item_type", itp_type_shield),
			
			(try_begin),
				(eq, ":imod", imod_reinforced),
				(assign, ":cost_modifier", 110),
			(else_try),
				(eq, ":imod", imod_thick),
				(assign, ":cost_modifier", 60),
			(else_try),
				(eq, ":imod", imod_battered),
				(assign, ":cost_modifier", -15),
			(else_try),
				(eq, ":imod", imod_cracked),
				(assign, ":cost_modifier", -40),
			(try_end),
		(else_try),
			(this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_polearm + 1),
			(is_between, ":item_type", itp_type_bow, itp_type_thrown + 1),
			
			(try_begin),
				(eq, ":imod", imod_masterwork),
				(assign, ":cost_modifier", 1650),
			(else_try),
				(eq, ":imod", imod_tempered),
				(assign, ":cost_modifier", 670),
			(else_try),
				(eq, ":imod", imod_strong),
				(assign, ":cost_modifier", 360),
			(else_try),
				(eq, ":imod", imod_balanced),
				(assign, ":cost_modifier", 250),
			(else_try),
				(eq, ":imod", imod_heavy),
				(assign, ":cost_modifier", 90),
			(else_try),
				(eq, ":imod", imod_chipped),
				(assign, ":cost_modifier", -28),
			(else_try),
				(eq, ":imod", imod_rusty),
				(assign, ":cost_modifier", -45),
			(else_try),
				(eq, ":imod", imod_bent),
				(assign, ":cost_modifier", -35),
			(else_try),
				(eq, ":imod", imod_cracked),
				(assign, ":cost_modifier", -50),
			(try_end),
		(else_try),
			(is_between, ":item_type", itp_type_arrows, itp_type_bolts + 1),
			
			(try_begin),
				(eq, ":imod", imod_large_bag),
				(assign, ":cost_modifier", 90),
			(else_try),
				(eq, ":imod", imod_bent),
				(assign, ":cost_modifier", -35),
			(try_end),
		(else_try),
			(eq, ":item_type", itp_type_horse),
			
			(try_begin),
				(eq, ":imod", imod_champion),
				(assign, ":cost_modifier", 1350),
			(else_try),
				(eq, ":imod", imod_spirited),
				(assign, ":cost_modifier", 550),
			(else_try),
				(eq, ":imod", imod_heavy),
				(assign, ":cost_modifier", 90),
			(else_try),
				(eq, ":imod", imod_stubborn),
				(assign, ":cost_modifier", -10),
			(else_try),
				(eq, ":imod", imod_swaybacked),
				(assign, ":cost_modifier", -40),
			(else_try),
				(eq, ":imod", imod_lame),
				(assign, ":cost_modifier", -60),
			(try_end),
		(try_end),
		
		(assign, reg0, ":cost_modifier"),
	]),

# script_kct_cf_item_is_eligible_equipment_option
	("kct_cf_item_is_eligible_equipment_option",
	[
		(store_script_param, ":item", 1),
		
		(assign, ":item_eligible", 0),
		(try_begin),
			(item_has_property, ":item", itp_merchandise),
			(store_item_value, ":value", ":item"),
			(gt, ":value", 0),
			
			(this_or_next|gt, "$g_sexual_content", 0), # No adult armors if disabled
			(neg|is_between, ":item", itm_chest_b, itm_sonja_sword),
			
			(assign, ":item_eligible", 1),
		(else_try),
			(this_or_next|eq, ":item", "itm_strange_armor"),
			(this_or_next|eq, ":item", "itm_strange_boots"),
			(this_or_next|eq, ":item", "itm_strange_helmet"),
			(this_or_next|eq, ":item", "itm_strange_sword"),
			(this_or_next|eq, ":item", "itm_strange_great_sword"),
			(eq, ":item", "itm_strange_short_sword"),
			
			(assign, ":item_eligible", 1),
		(else_try),
			(eq, 0, 1),	## CHANGE THIS
			
			(assign, ":item_eligible", 1),
		(try_end),
		
		(eq, ":item_eligible", 1),
	]),
]

# script_kct_get_items_array
kct_get_items_array = ("kct_get_items_array",
	[
		(store_script_param, ":item_type", 1),
		
		(assign, reg0, -1),
		(try_begin),
	])
for item_type in cstm_item_type_strings.keys():
	array = "trp_" + cstm_items_array_id(item_type)
	kct_get_items_array[1].extend([
			(eq, ":item_type", item_type),
			
			(assign, reg0, array),
		(else_try),
	])
kct_get_items_array[1][-1] = (try_end)

new_scripts.append(kct_get_items_array)

# Set the dummy/custom-troop slot links for preset 4 at game start, mirroring
# custom_tree_start_slot_operations for the base trees (slot linkage only; the
# stats/inventory initialisation comes with the customisation step).
# Label -> index lookup for PRESET_4_UNITS (used for the parent links below).
preset_4_index_of_label = {}
for _i, (_label, _level, _children) in enumerate(PRESET_4_UNITS):
	preset_4_index_of_label[_label] = _i

new_start_operations = []
for skin_id in (0, 1):
	for node_index in xrange(len(PRESET_4_UNITS)):
		real_id = "trp_" + preset_4_troop_id(skin_id, node_index)
		dummy_id = real_id + "_dummy"
		new_start_operations.extend([
			(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
			(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
		])
		# Parent (upgrade) links for the bottom-up editing restriction (spec §7),
		# mirroring the base mod's loop for presets 1-3: each child's base_troop
		# is this node, so a node unlocks only after its parent is configured.
		# Also activates the min_from_tree stat minimums for preset 4.
		for child_label in PRESET_4_UNITS[node_index][2]:
			child_index = preset_4_index_of_label[child_label]
			child_real = "trp_" + preset_4_troop_id(skin_id, child_index)
			new_start_operations.append((troop_set_slot, child_real, cstm_slot_troop_base_troop, real_id))
# Populate the item arrays + funds/proficiency tables the kct store needs
# (self-contained copies of the custom_troops game-start ops).
new_start_operations.append((assign, "$cstm_items_array", cstm_items_arrays_begin))
new_start_operations.append((call_script, "script_kct_setup_item_arrays"))

# Record the required points for each proficiency level
previous_requirement = 0
for i in xrange(max(cstm_proficiency_requirements.keys()) + 1):
	requirement = previous_requirement
	if i in cstm_proficiency_requirements:
		requirement = cstm_proficiency_requirements[i]
		previous_requirement = requirement
	new_start_operations.append((troop_set_slot, "trp_cstm_proficiency_requirements", i, requirement))

# Set the allocated equipment funds for each troop level (unified at 1.5x to match
# the custom_troops save-fix trigger, so boot-time and load-restore agree; see
# CSTM_TROOP_TREES_SPEC.md §5).
for i in xrange(64):
	inventory_value = equipment_funds_available(i)
	inventory_value = int(round(inventory_value * 1.5))
	new_start_operations.append((troop_set_slot, "trp_cstm_inventory_values", i, inventory_value))

# Set item types of arrays
for item_type in cstm_item_type_strings.keys():
	new_start_operations.append((troop_set_slot, "trp_" + cstm_items_array_id(item_type), cstm_slot_array_item_type, item_type))


class Script:
	def __init__(self, id, operations):
		self.id = id
		self.operations = operations

	def convert_to_tuple(self):
		return (self.id, self.operations)

def modmerge(var_set):
	try:
		orig_scripts = var_set["scripts"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"scripts\".")

	orig_scripts.extend(new_scripts)

	scripts = collections.OrderedDict()
	for script_tuple in orig_scripts:
		scripts[script_tuple[0]] = Script(*script_tuple)

	scripts["game_start"].operations.extend(new_start_operations)

	del orig_scripts[:]
	for script_id in scripts:
		orig_scripts.append(scripts[script_id].convert_to_tuple())
