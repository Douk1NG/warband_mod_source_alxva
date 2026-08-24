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

from kingdom_custom_troop_tree_creator_constants import *

BRANCH_DISPLAY_SCRIPTS = [
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

		(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
		(str_store_troop_name, s0, ":dummy"),
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
