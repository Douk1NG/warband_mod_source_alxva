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

# Manage screen for saved kingdom custom troop trees (prsnt_kct_manage_tree_files).
#
# Fixed-slot design: there are kct_tree_slot_count numbered slots, each holding
# one saved tree. Saving is NOT done here - the creator's Export button saves
# directly with auto-slot assignment (script_kct_save_tree_to_slot: overwrite a
# slot with the same name, else first empty slot). This screen only LOADS and
# DELETES saved trees: click a slot to select it, then Load or Delete.
#
# WSE cannot enumerate files in its managed directory, so the slot->name mapping
# is kept in a fixed-size string-array file (kct_tree_registry_file, "kct_trees"):
# entry i = the name of slot i (empty string = free slot). The actual tree data
# lives in <name>.json (written by script_kct_export_tree_to_file / read by
# script_kct_import_tree_from_file). A free slot has no file on disk.
#
# Entry point: the picker's Import button (branch_selector) starts this
# presentation. Exit returns to the picker.

# Layout (screen ~1000 x 750, y up): title top, 8 selectable slot rows, buttons
# along the bottom. Rows are drawn as large text overlays (the engine's listbox
# text can't be resized) with a highlight bar behind the selected row - the same
# restart-to-redraw pattern the picker and creator use.
KTF_SLOT_COUNT = kct_tree_slot_count

KTF_TITLE_POS = (50, 660)
KTF_TITLE_SIZE = 2000

# Exit button sits on the same row as the title, right of the title text
KTF_EXIT_POS = (860, KTF_TITLE_POS[1])

KTF_ROWS_X = 60
KTF_ROWS_TOP = 560
KTF_ROW_H = 55
KTF_ROW_W = 880
KTF_ROW_FONT = 1200
KTF_ROW_SEL_COLOR = 0xC8A000
KTF_ROW_SEL_TEXT_COLOR = 0x000000
KTF_ROW_UNSEL_TEXT_COLOR = 0x777777
# Radio-style checkbox indicator at the left of each row
KTF_CHECKBOX_X = 18
KTF_CHECKBOX_Y = 8
KTF_CHECKBOX_SIZE = 0   # 0 = native mesh size (no overlay_set_size)

KTF_BUTTON_ROW_Y = 90
KTF_BUTTON_SIZE_X = 140
KTF_BUTTON_SIZE_Y = 40
# Bottom-right: Delete sits just left of Load; Load is aligned in X with Exit
KTF_DELETE_POS = (700, KTF_BUTTON_ROW_Y)
KTF_LOAD_POS = (KTF_EXIT_POS[0], KTF_BUTTON_ROW_Y)

def _build_load_ops():
	ops = [
		(set_fixed_point_multiplier, 1000),
		# Ensure $cstm_troops_begin/_end/_num_tiers are set from the picker state
		# (needed by Load when this screen is opened from the picker, where the
		# creator has not run yet).
		(call_script, "script_kct_compute_tree_range"),

		## LOAD THE SAVED-SLOTS REGISTRY (free any previous session's arrays first)
		(try_begin,),
			(gt, "$kct_tree_registry", 0),
			(array_free, "$kct_tree_registry"),
			(assign, "$kct_tree_registry", 0),
		(try_end,),
		(try_begin,),
			(gt, "$kct_slot_row_texts", 0),
			(array_free, "$kct_slot_row_texts"),
			(assign, "$kct_slot_row_texts", 0),
		(try_end,),
		(try_begin,),
			(gt, "$kct_slot_checkboxes", 0),
			(array_free, "$kct_slot_checkboxes"),
			(assign, "$kct_slot_checkboxes", 0),
		(try_end,),
		(str_store_string, s4, kct_tree_registry_file),
		(assign, "$kct_tree_registry", 0),
		(array_load_file, "$kct_tree_registry", s4),
		# array_load_file does NOT return fail when the file is missing - it logs
		# a script error and leaves the destination at 0, so a try/else_try
		# fallback never runs. Check the destination instead: if it is still 0
		# the file did not exist - start with an empty slot array and write it to
		# disk so the file exists from now on (no more missing-file errors). If
		# the file loads but has the wrong size (older name-list format), rebuild
		# it as exactly kct_tree_slot_count entries, migrating any names it had.
		(try_begin,),
			(eq, "$kct_tree_registry", 0),
			(array_create, "$kct_tree_registry", 1, kct_tree_slot_count),
			(array_save_file, "$kct_tree_registry", s4),
		(else_try,),
			(array_get_dim_size, ":size", "$kct_tree_registry", 0),
			(neq, ":size", kct_tree_slot_count),
			(array_create, "$kct_tree_registry_new", 1, kct_tree_slot_count),
			(array_get_dim_size, ":old_size", "$kct_tree_registry", 0),
			(assign, ":copy", 0),
			(try_begin,),
				(lt, ":old_size", kct_tree_slot_count),
				(assign, ":copy", ":old_size"),
			(else_try,),
				(assign, ":copy", kct_tree_slot_count),
			(try_end,),
			(try_for_range, ":i", 0, ":copy"),
				(array_get_val, s1, "$kct_tree_registry", ":i"),
				(array_set_val, "$kct_tree_registry_new", s1, ":i"),
			(try_end,),
			(array_free, "$kct_tree_registry"),
			(assign, "$kct_tree_registry", "$kct_tree_registry_new"),
			(str_store_string, s4, kct_tree_registry_file),
			(array_save_file, "$kct_tree_registry", s4),
		(try_end,),
		# Overlay-id -> slot mapping for row clicks (fresh each redraw).
		(array_create, "$kct_slot_row_texts", 0, 0),
		(array_create, "$kct_slot_checkboxes", 0, 0),

		## TITLE
		(str_store_string, s0, "@Custom troop tree management"),
		(call_script, "script_kct_create_text_overlay", "str_s0", KTF_TITLE_POS[0], KTF_TITLE_POS[1], KTF_TITLE_SIZE, 900, 50, tf_left_align),
	]

	## SLOT ROWS (checkbox indicator + big text overlays + a highlight bar behind
	## the selected row). The checkbox mirrors $kct_selected_slot (1 = checked,
	## radio-style) and is clickable like a row, so both the box and the text pick
	## a slot - same restart-to-redraw pattern the picker and creator use.
	for i in range(KTF_SLOT_COUNT):
		row_y = KTF_ROWS_TOP - i * KTF_ROW_H
		ops.append((try_begin,))
		ops.append((eq, "$kct_selected_slot", i))
		ops.append((call_script, "script_kct_create_mesh_overlay", "mesh_white_plane", KTF_ROWS_X, row_y, KTF_ROW_W, KTF_ROW_H))
		ops.append((overlay_set_color, reg1, KTF_ROW_SEL_COLOR))
		ops.append((try_end,))
		ops.append((assign, reg0, i + 1))
		ops.append((array_get_val, s2, "$kct_tree_registry", i))
		ops.append((try_begin,))
		ops.append((str_is_empty, s2))
		ops.append((str_store_string, s2, "@(empty)"))
		ops.append((try_end,))
		ops.append((str_store_string, s0, "@Slot {reg0}: {s2}"))
		# Radio-style checkbox (checked = selected), mapped to the same slot
		ops.append((call_script, "script_kct_create_check_box_overlay", KTF_CHECKBOX_X, row_y + KTF_CHECKBOX_Y, KTF_CHECKBOX_SIZE))
		ops.append((try_begin,))
		ops.append((eq, "$kct_selected_slot", i))
		ops.append((overlay_set_val, reg1, 1))
		ops.append((else_try,))
		ops.append((overlay_set_val, reg1, 0))
		ops.append((try_end,))
		ops.append((array_push, "$kct_slot_checkboxes", reg1))
		ops.append((call_script, "script_kct_create_text_overlay", "str_s0", KTF_ROWS_X, row_y, KTF_ROW_FONT, KTF_ROW_W, KTF_ROW_H, tf_left_align|tf_vertical_align_center))
		ops.append((try_begin,))
		ops.append((eq, "$kct_selected_slot", i))
		ops.append((overlay_set_color, reg1, KTF_ROW_SEL_TEXT_COLOR))
		ops.append((else_try,))
		ops.append((overlay_set_color, reg1, KTF_ROW_UNSEL_TEXT_COLOR))
		ops.append((try_end,))
		ops.append((array_push, "$kct_slot_row_texts", reg1))

	ops.extend([
		## BUTTONS (explicit size so they render readable, like the troop editor)
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
			# ESC leaves the screen (same as the Exit button)
			(key_clicked, key_escape),
			(start_presentation, "prsnt_cstm_choose_troop_tree"),
		(try_end,),
	]

def _build_mouse_press_ops():
	# Slot rows are TEXT overlays, and text overlays only fire the mouse press
	# trigger (ti_on_presentation_event_state_change fires only for buttons).
	# So row selection is handled here: a left-click on one of the row overlay
	# ids (tracked in $kct_slot_row_texts) selects that slot and restarts the
	# presentation so the highlight moves. Button clicks (Load/Delete/Exit) are
	# not in the row array, so they fall through to event_state_change.
	return [
		(store_trigger_param_1, ":overlay"),
		(store_trigger_param_2, ":mouse_button"),
		(try_begin,),
			(eq, ":mouse_button", 0),
			(array_get_dim_size, ":count", "$kct_slot_row_texts", 0),
			(try_for_range, ":i", 0, ":count"),
				(array_get_val, ":row_overlay", "$kct_slot_row_texts", ":i"),
				(try_begin,),
					(eq, ":overlay", ":row_overlay"),
					(neq, "$kct_selected_slot", ":i"),
					(assign, "$kct_selected_slot", ":i"),
					(start_presentation, "prsnt_kct_manage_tree_files"),
				(try_end,),
			(try_end,),
		(try_end,),
	]

def _build_event_ops():
	ops = [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":value"),
	]
	# CHECKBOX CLICKED? - scan the checkbox overlays first and set a flag, then
	# branch on that flag. Checkboxes are button-type overlays (they fire this
	# trigger, unlike the text rows), so a click here selects the slot and
	# redraws. The scan must NOT be the first branch of the try/else_try chain
	# (a try_begin whose body never fails a top-level condition always succeeds,
	# so the else_try buttons below would never run).
	ops.append((assign, ":slot_clicked", 0))
	ops.append((array_get_dim_size, ":count", "$kct_slot_checkboxes", 0))
	ops.append((try_for_range, ":i", 0, ":count"))
	ops.append((array_get_val, ":cb_overlay", "$kct_slot_checkboxes", ":i"))
	ops.append((try_begin,))
	ops.append((eq, ":object", ":cb_overlay"))
	ops.append((assign, "$kct_selected_slot", ":i"))
	ops.append((assign, ":slot_clicked", 1))
	ops.append((try_end,))
	ops.append((try_end,))
	ops.extend([
		(try_begin,),
			## CHECKBOX CLICKED - redraw so the indicator moves
			(eq, ":slot_clicked", 1),
			(start_presentation, "prsnt_kct_manage_tree_files"),
		(else_try,),
			## LOAD - import the selected slot's name; on success open the creator.
			(eq, ":object", "$kct_tree_files_load"),
			(array_get_val, s2, "$kct_tree_registry", "$kct_selected_slot"),
			(try_begin,),
				(str_is_empty, s2),
				(display_message, "@This slot is empty", 0xff0000),
			(else_try,),
				(call_script, "script_kct_import_tree_from_file", s2),
				(try_begin,),
					(eq, reg0, 1),
					(assign, "$cstm_tree_preview_index", "$cstm_selected_tree"),
					(start_presentation, "prsnt_cstm_create_troop_tree"),
				(try_end,),
			(try_end,),
		(else_try,),
			## DELETE - clear the selected slot: drop its .json and blank it.
			(eq, ":object", "$kct_tree_files_delete"),
			(array_get_val, s2, "$kct_tree_registry", "$kct_selected_slot"),
			(try_begin,),
				(str_is_empty, s2),
				(display_message, "@This slot is empty", 0xff0000),
			(else_try,),
				(dict_delete_file, s2),
				(str_clear, s1),
				(array_set_val, "$kct_tree_registry", s1, "$kct_selected_slot"),
				(str_store_string, s4, kct_tree_registry_file),
				(array_save_file, "$kct_tree_registry", s4),
				(start_presentation, "prsnt_kct_manage_tree_files"),
			(try_end,),
		(else_try,),
			## EXIT - leave the screen back to the picker
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
