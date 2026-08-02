# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from ID_meshes import *
from module_constants import *

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
]

def modmerge(var_set):
	try:
		orig_scripts = var_set["scripts"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"scripts\".")
	orig_scripts.extend(new_scripts)
