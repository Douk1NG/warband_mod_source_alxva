# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_items import *
from header_skills import *
from header_troops import *
from module_constants import *

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

from kingdom_custom_troop_tree_creator.kct_presentations.layout import *

# Manage screen for vanilla savegame-backed KCTT template slots.
#
# There are kct_template_slot_count fixed slots. Each slot is stored in hidden
# hero troops, not in WSE files. The creator's Export button auto-saves into
# these slots (same-name overwrite, else first empty slot). This screen only
# loads and clears those in-save slots.

KTF_SLOT_COUNT = kct_template_slot_count

KTF_TITLE_POS = (50, 660)
KTF_TITLE_SIZE = 2000
KTF_EXIT_POS = (860, KTF_TITLE_POS[1])

KTF_ROWS_X = 60
KTF_ROWS_TOP = 585
KTF_ROW_H = 38
KTF_ROW_W = 880
KTF_ROW_FONT = 950
KTF_ROW_SEL_COLOR = 0xC8A000
KTF_ROW_SEL_TEXT_COLOR = 0x000000
KTF_ROW_UNSEL_TEXT_COLOR = 0x777777
KTF_ROW_LABEL_Y_OFFSET = 10
KTF_CHECKBOX_X = 18
KTF_CHECKBOX_Y = 4
KTF_CHECKBOX_SIZE = 0

KTF_BUTTON_ROW_Y = 90
KTF_BUTTON_SIZE_X = 140
KTF_BUTTON_SIZE_Y = 40
KTF_DELETE_POS = (700, KTF_BUTTON_ROW_Y)
KTF_LOAD_POS = (KTF_EXIT_POS[0], KTF_BUTTON_ROW_Y)

def _row_global(slot_index):
	return "$kct_slot_row_%d" % slot_index

def _checkbox_global(slot_index):
	return "$kct_slot_checkbox_%d" % slot_index

def _build_load_ops():
	ops = [
		(set_fixed_point_multiplier, 1000),
		(call_script, "script_kct_compute_tree_range"),

		(str_store_string, s0, "@Custom troop tree slots"),
		(call_script, "script_kct_create_text_overlay", "str_s0", KTF_TITLE_POS[0], KTF_TITLE_POS[1], KTF_TITLE_SIZE, 900, 50, tf_left_align),
	]

	for i in range(KTF_SLOT_COUNT):
		row_y = KTF_ROWS_TOP - i * KTF_ROW_H
		ops.extend([
			(try_begin,),
				(eq, "$kct_selected_slot", i),
				(call_script, "script_kct_create_mesh_overlay", "mesh_white_plane", KTF_ROWS_X, row_y, KTF_ROW_W, KTF_ROW_H),
				(overlay_set_color, reg1, KTF_ROW_SEL_COLOR),
			(try_end,),

			(call_script, "script_kct_get_template_meta_troop", i),
			(assign, ":meta", reg0),
			(assign, reg0, i + 1),
			(try_begin,),
				(troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
				(str_store_troop_name, s2, ":meta"),
			(else_try,),
				(str_store_string, s2, "@(empty)"),
			(try_end,),
			(str_store_string, s0, "@Slot {reg0}: {s2}"),
			(try_begin,),
				(lt, i, kct_seeded_template_slot_count),
				(str_store_string, s0, "@Default {reg0}: {s2}"),
			(try_end,),

			(call_script, "script_kct_create_check_box_overlay", KTF_CHECKBOX_X, row_y + KTF_CHECKBOX_Y, KTF_CHECKBOX_SIZE),
			(assign, _checkbox_global(i), reg1),
			(try_begin,),
				(eq, "$kct_selected_slot", i),
				(overlay_set_val, reg1, 1),
			(else_try,),
				(overlay_set_val, reg1, 0),
			(try_end,),

			(call_script, "script_kct_create_text_overlay", "str_s0", KTF_ROWS_X, row_y + KTF_ROW_LABEL_Y_OFFSET, KTF_ROW_FONT, KTF_ROW_W, KTF_ROW_H, tf_left_align|tf_vertical_align_center),
			(assign, _row_global(i), reg1),
			(try_begin,),
				(eq, "$kct_selected_slot", i),
				(overlay_set_color, reg1, KTF_ROW_SEL_TEXT_COLOR),
			(else_try,),
				(overlay_set_color, reg1, KTF_ROW_UNSEL_TEXT_COLOR),
			(try_end,),
		])

	ops.extend([
		(str_store_string, s0, "@Load"),
		(call_script, "script_kct_create_game_button_overlay", "str_s0", KTF_LOAD_POS[0], KTF_LOAD_POS[1]),
		(assign, "$kct_tree_files_load", reg1),
		(position_set_x, pos1, KTF_BUTTON_SIZE_X),
		(position_set_y, pos1, KTF_BUTTON_SIZE_Y),
		(overlay_set_size, "$kct_tree_files_load", pos1),

		(str_store_string, s0, "@Delete"),
		(call_script, "script_kct_create_game_button_overlay", "str_s0", KTF_DELETE_POS[0], KTF_DELETE_POS[1]),
		(assign, "$kct_tree_files_delete", reg1),
		(position_set_x, pos1, KTF_BUTTON_SIZE_X),
		(position_set_y, pos1, KTF_BUTTON_SIZE_Y),
		(overlay_set_size, "$kct_tree_files_delete", pos1),

		(str_store_string, s0, "@Exit"),
		(call_script, "script_kct_create_game_button_overlay", "str_s0", KTF_EXIT_POS[0], KTF_EXIT_POS[1]),
		(assign, "$kct_tree_files_exit", reg1),
		(position_set_x, pos1, KTF_BUTTON_SIZE_X),
		(position_set_y, pos1, KTF_BUTTON_SIZE_Y),
		(overlay_set_size, "$kct_tree_files_exit", pos1),

		(presentation_set_duration, 999999),
	])
	return ops

def _build_run_ops():
	return [
		(try_begin,),
			(key_clicked, key_escape),
			(start_presentation, "prsnt_cstm_choose_troop_tree"),
		(try_end,),
	]

def _build_mouse_press_ops():
	ops = [
		(store_trigger_param_1, ":overlay"),
		(store_trigger_param_2, ":mouse_button"),
		(try_begin,),
			(eq, ":mouse_button", 0),
	]
	for i in range(KTF_SLOT_COUNT):
		ops.extend([
			(try_begin,),
				(eq, ":overlay", _row_global(i)),
				(neq, "$kct_selected_slot", i),
				(assign, "$kct_selected_slot", i),
				(start_presentation, "prsnt_kct_manage_tree_files"),
			(try_end,),
		])
	ops.append((try_end,))
	return ops

def _build_event_ops():
	ops = [
		(store_trigger_param_1, ":object"),
		(assign, ":slot_clicked", 0),
	]
	for i in range(KTF_SLOT_COUNT):
		ops.extend([
			(try_begin,),
				(eq, ":object", _checkbox_global(i)),
				(assign, "$kct_selected_slot", i),
				(assign, ":slot_clicked", 1),
			(try_end,),
		])

	ops.extend([
		(try_begin,),
			(eq, ":slot_clicked", 1),
			(start_presentation, "prsnt_kct_manage_tree_files"),
		(else_try,),
			(eq, ":object", "$kct_tree_files_load"),
			(call_script, "script_kct_get_template_meta_troop", "$kct_selected_slot"),
			(assign, ":meta", reg0),
			(try_begin,),
				(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
				(display_message, "@This slot is empty", 0xff0000),
			(else_try,),
				(call_script, "script_kct_import_tree_from_slot", "$kct_selected_slot"),
				(try_begin,),
					(eq, reg0, 1),
					(assign, "$cstm_tree_preview_index", "$cstm_selected_tree"),
					(start_presentation, "prsnt_cstm_create_troop_tree"),
				(try_end,),
			(try_end,),
		(else_try,),
			(eq, ":object", "$kct_tree_files_delete"),
			(call_script, "script_kct_get_template_meta_troop", "$kct_selected_slot"),
			(assign, ":meta", reg0),
			(try_begin,),
				(lt, "$kct_selected_slot", kct_seeded_template_slot_count),
				(display_message, "@Default template slots cannot be deleted", 0xff0000),
			(else_try,),
				(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
				(display_message, "@This slot is empty", 0xff0000),
			(else_try,),
				(call_script, "script_kct_clear_template_slot", "$kct_selected_slot"),
				(start_presentation, "prsnt_kct_manage_tree_files"),
			(try_end,),
		(else_try,),
			(eq, ":object", "$kct_tree_files_exit"),
			(start_presentation, "prsnt_cstm_choose_troop_tree"),
		(try_end,),
	])
	return ops

new_manage_presentation = ("kct_manage_tree_files", 0, mesh_load_window, [
	(ti_on_presentation_load, _build_load_ops()),
	(ti_on_presentation_run, _build_run_ops()),
	(ti_on_presentation_event_state_change, _build_event_ops()),
	(ti_on_presentation_mouse_press, _build_mouse_press_ops()),
])
