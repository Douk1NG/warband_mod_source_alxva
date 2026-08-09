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
from kingdom_custom_troop_tree_creator.kct_presentations.layout import _tree_specs, _preset_4_positions, _draw_tree_ops

def _build_load_ops():
	ops = [
		(set_fixed_point_multiplier, 1000),
	]
	# Tree line: "Choose your kingdom's troop tree" -> [select]
	ops.append((str_store_string, s0, "@Choose your kingdom's troop tree"))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", TREE_LABEL_POS[0], TREE_LABEL_POS[1], TREE_LABEL_FONT, TREE_LABEL_AREA[0], TREE_LABEL_AREA[1], tf_left_align|tf_vertical_align_center))
	ops.append((call_script, "script_kct_create_combo_button_overlay", TREE_COMBO_POS[0], TREE_COMBO_POS[1]))
	ops.append((assign, "$cstm_tree_preview_selector", reg1))
	for name in PRESET_NAMES:
		ops.append((str_store_string, s1, "@" + name))
		ops.append((overlay_add_item, "$cstm_tree_preview_selector", s1))
	ops.append((overlay_set_val, "$cstm_tree_preview_selector", "$cstm_tree_preview_index"))
	# Gender line: "Gender" -> [select]
	ops.append((str_store_string, s0, "@Gender"))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", GENDER_LABEL_POS[0], GENDER_LABEL_POS[1], GENDER_LABEL_FONT, 200, 50, tf_left_align|tf_vertical_align_center))
	ops.append((call_script, "script_kct_create_combo_button_overlay", GENDER_COMBO_POS[0], GENDER_COMBO_POS[1]))
	ops.append((assign, "$cstm_gender_selector", reg1))
	ops.append((str_store_string, s1, "@Male"))
	ops.append((overlay_add_item, "$cstm_gender_selector", s1))
	ops.append((str_store_string, s1, "@Female"))
	ops.append((overlay_add_item, "$cstm_gender_selector", s1))
	ops.append((overlay_set_val, "$cstm_gender_selector", "$cstm_selected_gender"))
	# Draw whichever tree is currently selected
	specs = _tree_specs()
	for i, (tiers, edges, label_fn) in enumerate(specs):
		ops.append((try_begin,) if i == 0 else (else_try,))
		ops.append((eq, "$cstm_tree_preview_index", i))
		pos = _preset_4_positions() if i == 3 else None
		ops.extend(_draw_tree_ops(tiers, edges, label_fn, pos))
	ops.append((try_end,))
	# Choose + Exit buttons
	ops.append((str_store_string, s0, "@Choose"))
	ops.append((call_script, "script_kct_create_game_button_overlay", "str_s0", 880, 50))
	ops.append((assign, "$cstm_choose_tree_button", reg1))
	ops.append((str_store_string, s0, "@Exit"))
	ops.append((call_script, "script_kct_create_game_button_overlay", "str_s0", 100, 50))
	ops.append((assign, "$cstm_choose_tree_exit", reg1))
	ops.append((presentation_set_duration, 999999))
	return ops

def _build_run_ops():
	return [
		(try_begin,),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
		(try_end,),
	]

def _build_event_ops():
	return [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":value"),
		(try_begin,),
			(eq, ":object", "$cstm_tree_preview_selector"),
			(assign, "$cstm_tree_preview_index", ":value"),
			(start_presentation, "prsnt_cstm_choose_troop_tree"),
		(else_try,),
			(eq, ":object", "$cstm_gender_selector"),
			(assign, "$cstm_selected_gender", ":value"),
		(else_try,),
			(eq, ":object", "$cstm_choose_tree_button"),
			(assign, "$cstm_selected_tree", "$cstm_tree_preview_index"),
			# Set the kingdom troop tree prefix (like the working mod does on entry)
			(troop_set_name, cstm_troop_tree_prefix, "@Custom"),
			(start_presentation, "prsnt_cstm_create_troop_tree"),
		(else_try,),
			(eq, ":object", "$cstm_choose_tree_exit"),
			(change_screen_return),
			(presentation_set_duration, 0),
		(try_end,),
	]

new_presentation = ("cstm_choose_troop_tree", 0, mesh_load_window, [
	(ti_on_presentation_load, _build_load_ops()),
	(ti_on_presentation_run, _build_run_ops()),
	(ti_on_presentation_event_state_change, _build_event_ops()),
])
