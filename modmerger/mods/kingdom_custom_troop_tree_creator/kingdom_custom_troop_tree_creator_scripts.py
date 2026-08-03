# -*- coding: cp1254 -*-
import collections

from header_common import *
from header_operations import *
from header_presentations import *
from ID_meshes import *
from module_constants import *

from kingdom_custom_troop_tree_creator_troops import PRESET_4_UNITS, preset_4_troop_id

# Troop slots used to link a real custom troop to its dummy. These MUST match the
# values in the base mod's custom_troops_constants (NEW_TROOP_SLOTS_BEGIN = 500)
# because the dummies for presets 1-3 are linked by the base mod at game start
# using those exact slot numbers.
cstm_slot_troop_dummy = 500
cstm_slot_troop_custom_troop = 501

# The troop whose name is used to store the custom troop tree prefix string
# (mirrors cstm_troop_tree_prefix in custom_troops_constants).
cstm_troop_tree_prefix = "trp_cstm_custom_troops_end"

# Self-contained copies of the presentation helper scripts used by
# prsnt_cstm_choose_troop_tree. Ported (not imported) from the custom_troops
# mod so this mod does not depend on it at runtime.

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
]

# Set the dummy/custom-troop slot links for preset 4 at game start, mirroring
# custom_tree_start_slot_operations for the base trees (slot linkage only; the
# stats/inventory initialisation comes with the customisation step).
new_start_operations = []
for skin_id in (0, 1):
	for node_index in xrange(len(PRESET_4_UNITS)):
		real_id = "trp_" + preset_4_troop_id(skin_id, node_index)
		dummy_id = real_id + "_dummy"
		new_start_operations.extend([
			(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
			(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
		])

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
