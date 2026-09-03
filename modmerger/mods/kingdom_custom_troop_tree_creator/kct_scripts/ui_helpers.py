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

# Neutral prsnt_* helpers now live in source/scripts/prsnt_*.py (canonical).
# These kct_* wrappers are kept as thin aliases for save-compat / ModMerger
# presentations that still call script_kct_*. All new presentations should
# call script_prsnt_* directly.

UI_HELPER_SCRIPTS = [
	("kct_create_mesh_overlay",
	[
		(store_script_param, ":mesh", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size_x", 4),
		(store_script_param, ":size_y", 5),
		(call_script, "script_prsnt_create_mesh_overlay", ":mesh", ":pos_x", ":pos_y", ":size_x", ":size_y"),
	]),
	("kct_create_text_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":text_size", 4),
		(store_script_param, ":size_x", 5),
		(store_script_param, ":size_y", 6),
		(store_script_param, ":flags", 7),
		(call_script, "script_prsnt_create_text_overlay", ":string", ":pos_x", ":pos_y", ":text_size", ":size_x", ":size_y", ":flags"),
	]),
	("kct_create_check_box_overlay",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		(store_script_param, ":size", 3),
		(call_script, "script_prsnt_create_check_box_overlay", ":pos_x", ":pos_y", ":size"),
	]),
	("kct_create_game_button_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(call_script, "script_prsnt_create_game_button_overlay", ":string", ":pos_x", ":pos_y"),
	]),
	("kct_create_combo_button_overlay",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		(call_script, "script_prsnt_create_combo_button_overlay", ":pos_x", ":pos_y"),
	]),
	("kct_prsnt_lines",
	[
		(store_script_param, ":size_x", 1),
		(store_script_param, ":size_y", 2),
		(store_script_param, ":pos_x", 3),
		(store_script_param, ":pos_y", 4),
		(store_script_param, ":color", 5),
		(call_script, "script_prsnt_prsnt_lines", ":size_x", ":size_y", ":pos_x", ":pos_y", ":color"),
	]),
	("kct_prsnt_lines_to",
	[
		(store_script_param, ":pos_x1", 1),
		(store_script_param, ":pos_y1", 2),
		(store_script_param, ":pos_x2", 3),
		(store_script_param, ":pos_y2", 4),
		(store_script_param, ":color", 5),
		(call_script, "script_prsnt_prsnt_lines_to", ":pos_x1", ":pos_y1", ":pos_x2", ":pos_y2", ":color"),
	]),
	("kct_create_text_box_overlay",
	[
		(store_script_param, ":string", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(call_script, "script_prsnt_create_text_box_overlay", ":string", ":pos_x", ":pos_y"),
	]),
	("kct_create_troop_image",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size", 4),
		(call_script, "script_prsnt_create_troop_image", ":troop_no", ":pos_x", ":pos_y", ":size"),
	]),
	# Troop-image with explicit size (was inline in branch_display, now neutral)
	("kct_create_troop_image_size",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":pos_x", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":size_x", 4),
		(store_script_param, ":size_y", 5),
		(call_script, "script_prsnt_create_troop_image_size", ":troop_no", ":pos_x", ":pos_y", ":size_x", ":size_y"),
	]),
]
