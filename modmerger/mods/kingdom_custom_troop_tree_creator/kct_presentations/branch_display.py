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
from kingdom_custom_troop_tree_creator.kct_presentations.layout import _preset_4_spec, _preset_4_viewer_positions, _preset_4_dummy_offset

####################################################################################################################
# TROOP TREE CREATION step (prsnt_cstm_create_troop_tree).
#
# Entered after the player picks a tree + gender in prsnt_cstm_choose_troop_tree
# ("Choose" button). State available on entry:
#   $cstm_selected_tree   0..3  index into PRESET_NAMES (0-2 = presets 1-3, 3 = preset 4)
#   $cstm_selected_gender 0/1   skin id (0 = male, 1 = female)
#
# The presentation is a self-contained port of the working mod's tree viewer
# (prsnt_cstm_view_custom_troop_tree): it shows the selected tree's custom troops
# as images connected by upgrade lines, lets the player edit the kingdom troop
# tree prefix, and (for now) reports the troop name when a node is clicked.
# Clicking a node to open the full customisation store interface is the next step.
# ESC / Exit return to the picker so the player can choose another preset.
####################################################################################################################

def _build_create_setup_ops():
	# Compute $cstm_troops_begin/_end/_num_tiers/_presentation_troop from the
	# picker's selection (mirrors the working mod's menu flow, but for all four
	# presets at runtime instead of one tree per menu option).
	ops = []
	for i, (tree_id, _, num_tiers) in enumerate(PRESET_TREES_1_3):
		ops.append((try_begin,) if i == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_tree", i))
		ops.append((assign, "$cstm_num_tiers", num_tiers))
		next_tree_id = PRESET_TREES_1_3[i + 1][0] if i + 1 < len(PRESET_TREES_1_3) else None
		for s in (0, 1):
			ops.append((try_begin,) if s == 0 else (else_try,))
			ops.append((eq, "$cstm_selected_gender", s))
			begin = "trp_cstm_custom_troop_%s_%d_0_0" % (tree_id, s)
			if s == 0:
				end = "trp_cstm_custom_troop_%s_%d_0_0" % (tree_id, 1)
			elif next_tree_id is not None:
				end = "trp_cstm_custom_troop_%s_%d_0_0" % (next_tree_id, 0)
			else:
				end = "trp_cstm_custom_troops_end"
			ops.append((assign, "$cstm_troops_begin", begin))
			ops.append((assign, "$cstm_troops_end", end))
			ops.append((assign, "$cstm_presentation_troop", "trp_cstm_presentation_troop_%d" % s))
		ops.append((try_end,))
	# Preset 4 (6 tiers)
	ops.append((else_try,))
	ops.append((eq, "$cstm_selected_tree", 3))
	ops.append((assign, "$cstm_num_tiers", 6))
	for s in (0, 1):
		ops.append((try_begin,) if s == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_gender", s))
		begin = "trp_" + preset_4_troop_id(s, 0)
		end = "trp_cstm_custom_troop_4_1_0_0" if s == 0 else "trp_cstm_custom_troop_4_end"
		ops.append((assign, "$cstm_troops_begin", begin))
		ops.append((assign, "$cstm_troops_end", end))
		ops.append((assign, "$cstm_presentation_troop", "trp_cstm_presentation_troop_%d" % s))
	ops.append((try_end,))
	ops.append((try_end,))
	return ops

def _build_preset4_viewer_ops():
	"""Preset-4 tree: a dummy portrait at each node (centred on the branch point)
	with the branch lines drawn ON TOP of the portraits so the connected tree stays
	visible through the overlap - same look as the presets 1-3 branches. Names stay
	hidden for now. The portrait is the node's dummy troop (averaged face); the
	overlay slot maps to the real troop so clicks target the customisable troop."""
	tiers, edges, _ = _preset_4_spec()
	positions = _preset_4_viewer_positions()
	children_by_index = {}
	for parent, child in edges:
		children_by_index.setdefault(parent, []).append(child)
	ops = []
	# Small dummy portrait per node (per skin)
	for s in (0, 1):
		ops.append((try_begin,) if s == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_gender", s))
		for row in tiers:
			for node_index in row:
				x, y = positions[node_index]
				dummy_id = "trp_" + preset_4_troop_id(s, node_index) + "_dummy"
				real_id = "trp_" + preset_4_troop_id(s, node_index)
				ops.append((troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id))
				ops.append((troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id))
				# Self-heal the parent (base_troop) links for saves made before the
				# game-start loop existed - the restriction reads these at click time.
				for child_node in children_by_index.get(node_index, []):
					child_real = "trp_" + preset_4_troop_id(s, child_node)
					ops.append((troop_set_slot, child_real, cstm_slot_troop_base_troop, real_id))
				# Equip the dummy before rendering so the portrait shows the saved
				# gear: the store moves the dummy's equipped items into its
				# inventory grid on load, so without re-equipping here the viewer
				# would render it naked after entering/exiting a unit.
				ops.append((troop_sort_inventory, dummy_id))
				ops.append((troop_equip_items, dummy_id))
				# kct_create_troop_image_size anchors by top-left; subtract half the
				# size so the portrait is centred on the branch point, then apply
				# the global dummy lift (Y) / shift (X) and the per-node nudge.
				dx, dy = _preset_4_dummy_offset(node_index)
				base_x = x - P4_PORTRAIT_W // 2 + P4_DUMMY_X_OFFSET
				base_y = y - P4_PORTRAIT_H // 2 - P4_DUMMY_Y_OFFSET
				ops.append((call_script, "script_kct_create_troop_image_size", dummy_id, base_x + dx, base_y + dy, P4_PORTRAIT_W, P4_PORTRAIT_H))
				ops.append((troop_set_slot, "trp_cstm_overlay_troops", reg1, real_id))
				# TEMP dummy drag tool: register the portrait as a draggable item
				# so its position can be tuned in-game. Disabled (ENABLE_DUMMY_TOOL
				# = False) - only the label tool is active (remove with the tool).
				if ENABLE_DUMMY_TOOL:
					ops.extend(p4_dummy_tool.register(node_index, reg1, base_x, base_y, dx, dy))
	ops.append((try_end,))
	# Branch lines centre-to-centre, on top of the portraits
	for parent, child in edges:
		px, py = positions[parent]
		qx, qy = positions[child]
		ops.append((call_script, "script_kct_prsnt_lines_to", px, py, qx, qy, EDGE_COLOR))
	return ops

def _build_preset4_label_ops():
	"""Name label for every preset-4 dummy portrait, showing the unit name only
	(the dummy troop's name, e.g. "Unit A"). TEMP tuning mode: every label is
	dropped at P4_LABEL_CENTER so none are lost off-screen, then registered with
	the label drag tool and moved by hand; Snapshot bakes each label's delta (vs
	the centre) into P4_LABEL_MANUAL. Labels are plain text overlays (no action),
	so they never block node clicks. Remove the tool and restore a per-label base
	when the offsets are baked."""
	tiers, _, _ = _preset_4_spec()
	last_tier = set(tiers[-1])
	ops = []
	for s in (0, 1):
		ops.append((try_begin,) if s == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_gender", s))
		for row in tiers:
			for node_index in row:
				dummy_id = "trp_" + preset_4_troop_id(s, node_index) + "_dummy"
				if node_index in last_tier:
					flags = tf_right_align | tf_vertical_align_center
				else:
					flags = tf_left_align | tf_vertical_align_center
				base_x, base_y = P4_LABEL_CENTER
				manual_dx, manual_dy = P4_LABEL_MANUAL.get(node_index, (0, 0))
				ops.append((str_store_troop_name, s0, dummy_id))
				ops.append((call_script, "script_kct_create_text_overlay", "str_s0", base_x + manual_dx, base_y + manual_dy, P4_LABEL_FONT, P4_LABEL_W, P4_LABEL_H, flags))
				# TEMP label drag tool: register the label as a draggable item.
				# Disabled (ENABLE_LABEL_TOOL = False) - labels now show at their
				# baked P4_LABEL_MANUAL positions (remove with the tool).
				if ENABLE_LABEL_TOOL:
					ops.extend(p4_label_tool.register(node_index, reg1, base_x, base_y, manual_dx, manual_dy))
	ops.append((try_end,))
	return ops

def _build_create_load_ops():
	ops = [
		(set_fixed_point_multiplier, 1000),
	]
	ops.extend(_build_create_setup_ops())
	# Ensure the store's default item array (horses) is set before first open
	ops.append((assign, "$cstm_items_array", cstm_items_arrays_begin))

	## INITIALISE VARIABLES
	ops.append((try_for_range, ":overlay_id", 0, 9999))
	ops.append((troop_set_slot, "trp_cstm_overlay_troops", ":overlay_id", -1))
	ops.append((try_end,))
	# P4 drag tools: clear their slots/globals before the portraits/labels
	# register below. Both tools are disabled (ENABLE_DUMMY_TOOL /
	# ENABLE_LABEL_TOOL) - their slots are not touched.
	if ENABLE_DUMMY_TOOL:
		ops.extend(p4_dummy_tool.reset())
	if ENABLE_LABEL_TOOL:
		ops.extend(p4_label_tool.reset())

	ops.append((try_for_range, ":custom_troop", "$cstm_troops_begin", "$cstm_troops_end"))
	ops.append((call_script, "script_kct_replace_custom_troop_with_dummy", ":custom_troop"))
	ops.append((try_end,))

	## TITLE
	ops.append((str_store_faction_name, s0, "fac_player_supporters_faction"))
	ops.append((str_store_string, s0, "@{s0} Troop Tree"))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", CSTM_TREE_TITLE_POS_X, CSTM_TREE_TITLE_POS_Y, CSTM_TREE_TITLE_SIZE, 900, 50, tf_left_align))

	## PREFIX
	ops.append((str_store_string, s0, "@Prefix: "))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", CSTM_PREFIX_LABEL_POS_X, CSTM_PREFIX_POS_Y, 1000, CSTM_PREFIX_LABEL_WIDTH, 50, tf_left_align))
	ops.append((str_store_troop_name, s0, cstm_troop_tree_prefix))
	ops.append((call_script, "script_kct_create_text_box_overlay", "str_s0", CSTM_PREFIX_LABEL_POS_X + CSTM_PREFIX_LABEL_WIDTH, CSTM_PREFIX_POS_Y))
	ops.append((assign, "$cstm_set_prefix", reg1))

	## TREE VIEWER
	# Preset 4 draws just the branch skeleton (big, connected) for now; presets
	# 1-3 use the working mod's recursive layout with portraits + names.
	ops.append((try_begin,))
	ops.append((eq, "$cstm_selected_tree", 3))
	ops.extend(_build_preset4_viewer_ops())
	ops.extend(_build_preset4_label_ops())
	ops.append((else_try,))
	ops.append((store_sub, ":num_splits", "$cstm_num_tiers", 1))
	ops.append((store_div, ":offset_x", 1000 - (CSTM_TREE_POS_X + CSTM_TREE_X_RIGHT_PADDING), ":num_splits"))
	ops.append((call_script, "script_kct_create_troop_tree_images", "$cstm_troops_begin", CSTM_TREE_POS_X, CSTM_TREE_POS_Y, ":offset_x", CSTM_TREE_Y_OFFSET, 0))
	ops.append((try_end,))

	## EXIT BUTTON
	ops.append((str_store_string, s0, "@Exit"))
	ops.append((call_script, "script_kct_create_game_button_overlay", "str_s0", CSTM_BUTTONS_POS_X + CSTM_BUTTONS_SIZE_X + CSTM_BUTTONS_GAP - 50, CSTM_BUTTONS_POS_Y - 10))
	ops.append((assign, "$cstm_customise_troop_exit", reg1))
	ops.append((position_set_x, pos1, 100))
	ops.append((position_set_y, pos1, 50))
	ops.append((overlay_set_size, "$cstm_customise_troop_exit", pos1))

	## TEMP P4 drag tools: SNAPSHOT buttons + live readouts (remove with the
	## tools). Both tools are disabled (ENABLE_DUMMY_TOOL / ENABLE_LABEL_TOOL) -
	## their readouts + Snapshot buttons are not created.
	if ENABLE_DUMMY_TOOL:
		ops.extend(p4_dummy_tool.create_snapshot_button(P4_DUMMY_TOOL_SNAPSHOT_POS))
		ops.extend(p4_dummy_tool.create_readout("P4 dummy tool: press a portrait and drag", P4_DUMMY_TOOL_TEXT_POS, P4_DUMMY_TOOL_TEXT_SIZE, P4_DUMMY_TOOL_TEXT_W))
	if ENABLE_LABEL_TOOL:
		ops.extend(p4_label_tool.create_snapshot_button(P4_LABEL_TOOL_SNAPSHOT_POS))
		ops.extend(p4_label_tool.create_readout("P4 label tool: press a label and drag", P4_LABEL_TOOL_TEXT_POS, P4_LABEL_TOOL_TEXT_SIZE, P4_LABEL_TOOL_TEXT_W))

	ops.append((presentation_set_duration, 999999))
	return ops

def _build_create_run_ops():
	ops = [
		(try_begin,),
			(key_clicked, key_escape),
			(start_presentation, "prsnt_cstm_choose_troop_tree"),
		(try_end,),
	]
	# TEMP P4 label drag tool: while the left button is held the pressed label
	# follows the mouse and its (dx, dy) vs its base shows in the readout; on
	# release the drag stops and the label stays where it was dropped. The
	# offsets are baked into P4_LABEL_MANUAL, so the tool is disabled
	# (ENABLE_LABEL_TOOL) and its run block is skipped (remove with the tool).
	ops.append((set_fixed_point_multiplier, 1000))
	if ENABLE_DUMMY_TOOL:
		ops.extend(p4_dummy_tool.run_ops())
	if ENABLE_LABEL_TOOL:
		ops.extend(p4_label_tool.run_ops())
	return ops

def _build_create_event_ops():
	ops = [
		(store_trigger_param_1, ":object"),
		(try_begin,),
			## NODE CLICKED -> open the customisation store for that troop
			(troop_get_slot, ":troop", "trp_cstm_overlay_troops", ":object"),
			(gt, ":troop", 0),
			# Bottom-up editing restriction (spec §7): a node unlocks only after
			# its upgrade parent has been configured (its store Save pressed).
			(troop_get_slot, ":parent", ":troop", cstm_slot_troop_base_troop),
			(try_begin,),
				(gt, ":parent", 0),
				(troop_get_slot, ":configured", ":parent", cstm_slot_troop_configured),
				(eq, ":configured", 0),
				(troop_get_slot, ":parent_dummy", ":parent", cstm_slot_troop_dummy),
				(str_store_troop_name, s0, ":parent_dummy"),
				(display_message, "@@{s0} must be customised before this unit is available."),
			(else_try,),
				(assign, "$cstm_troop_being_customised", ":troop"),
				# Back up the name/plural so Reset can restore them
				(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
				(str_store_troop_name, s0, ":dummy"),
				(troop_set_name, "$cstm_presentation_troop", s0),
				(str_store_troop_name_plural, s0, ":dummy"),
				(troop_set_plural_name, "$cstm_presentation_troop", s0),
				# Fresh store state on entry
				(assign, "$cstm_item_modifier_selected", 0),
				(assign, "$cstm_item_page_no", 0),
				# Mark this as a fresh entry so the store's load trigger re-derives
				# the baseline for unconfigured children (consumed there).
				(assign, "$g_kct_recalc_baseline", 1),
				(start_presentation, "prsnt_kct_customise_troop"),
			(try_end,),
		(else_try,),
			## PREFIX CHANGED
			(eq, ":object", "$cstm_set_prefix"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
			(start_presentation, "prsnt_cstm_create_troop_tree"),
	]
	# TEMP P4 drag tools: SNAPSHOT - log every label's current (dx, dy), ready to
	# paste into P4_LABEL_MANUAL. Each block MUST open its own else_try branch (a
	# bare condition after a body is swallowed into the previous branch and never
	# runs on its own) (remove with the tools). Both tools are disabled
	# (ENABLE_DUMMY_TOOL / ENABLE_LABEL_TOOL) - their snapshot branches are
	# dropped, so no else_try is emitted for them.
	if ENABLE_DUMMY_TOOL:
		ops.append((else_try,))
		ops.extend(p4_dummy_tool.snapshot_event_ops("P4 DUMMY SNAPSHOT - paste into P4_DUMMY_MANUAL:"))
	if ENABLE_LABEL_TOOL:
		ops.append((else_try,))
		ops.extend(p4_label_tool.snapshot_event_ops("P4 LABEL SNAPSHOT - paste into P4_LABEL_MANUAL:"))
	ops.append((else_try,))
	ops.append((eq, ":object", "$cstm_customise_troop_exit"))
	ops.append((start_presentation, "prsnt_cstm_choose_troop_tree"))
	ops.append((try_end,))
	return ops

new_create_presentation = ("cstm_create_troop_tree", 0, mesh_load_window, [
	(ti_on_presentation_load, _build_create_load_ops()),
	(ti_on_presentation_run, _build_create_run_ops()),
	(ti_on_presentation_event_state_change, _build_create_event_ops()),
	# TEMP P4 drag tools: a left press on any registered label starts a drag
	# (labels are mapped to items in trp_temp_array_a; everything else -
	# portraits, lines, buttons - reads -1 and is ignored). Both tools are
	# disabled (ENABLE_DUMMY_TOOL / ENABLE_LABEL_TOOL), so their mouse_press
	# blocks are skipped too. Remove with the tools.
	(ti_on_presentation_mouse_press, [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":mouse_state"),
	] + (p4_dummy_tool.mouse_press_ops() if ENABLE_DUMMY_TOOL else []) + (p4_label_tool.mouse_press_ops() if ENABLE_LABEL_TOOL else [])),
])
