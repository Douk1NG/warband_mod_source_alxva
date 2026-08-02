# -*- coding: cp1254 -*-
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from header_items import *
from module_constants import *

# Preset-4 troops (single source of truth for the 22-unit tree shape).
from kingdom_custom_troop_tree_creator_troops import PRESET_4_UNITS

# Pick screen (prsnt_cstm_choose_troop_tree):
# A column of two label -> select lines at the top: the tree select labelled
# "Choose your kingdom's troop tree" with the gender select below it. The selected
# tree is drawn large in the centre as a HORIZONTAL tree (root on the left, each
# tier a column to the right; preset 4 is the full 22-unit tree with short codes).
# The branch lines stop at each node's label and resume after it, so every code
# label (|A1|) sits in a clean gap on the line in dark purple - the line never
# passes behind a label.
# "Choose" records the selection and hands off to prsnt_cstm_create_troop_tree;
# ESC / "Exit" close without recording.

# Presets 1-3: (tree id, num branches, num tiers) - match custom_troops_constants
PRESET_TREES_1_3 = [
	("1_tier", 1, 7),
	("2_tiers", 2, 6),
	("3_tiers", 3, 5),
]

PRESET_NAMES = [
	"Preset 1 - 1 branch, 7 tiers",
	"Preset 2 - 2 branches, 6 tiers",
	"Preset 3 - 3 branches, 5 tiers",
	"Preset 4 - custom (22 units)",
]

NODE_LABEL_SIZE = 900
NODE_LABEL_W = 100
NODE_LABEL_H = 40

# How far branch lines stop from a node center. The label text (|A1| etc.) is
# only ~20-25 units half-width wide inside the 100-wide box; this keeps the line
# just past the glyphs instead of leaving a wide empty band of box before it.
NODE_CONNECTOR_HALF = 30

LABEL_COLOR = 0x000000
EDGE_COLOR = 0x000000

# Preview area (screen ~1000 wide x 750 tall, y up): (cx, cy, width, height).
# cy lowered from 430 to 380 so the whole tree sits 50 units lower, clear of the
# gender/preset selects above it (y=660-680). Sits ~95 units clear of the buttons
# (y=50).
PREVIEW = (500, 380, 880, 470)

# Select column: label then combo on the same line, tree line above gender line.
TREE_LABEL_POS = (20, 680)
TREE_LABEL_FONT = 900
TREE_LABEL_AREA = (620, 50)
TREE_COMBO_POS = (420, 660)
GENDER_LABEL_POS = (610, 680)
GENDER_LABEL_FONT = 900
GENDER_COMBO_POS = (810, 660)

def _preset_4_positions():
	"""Centred layout for the preset-4 tree so it matches the preset 1-3 look:
	the root sits at the preview's vertical middle and every parent sits at the
	vertical centre of its children (a 2-option parent is centred between its two
	options, never inline with one of them). Leaves each get a lane in left-to-
	right order; an internal node's lane is the mean of its children's lanes.
	Returns {node index: (x, y)}."""
	tiers, edges, _ = _preset_4_spec()
	children = {}
	parent = {}
	for p, c in edges:
		children.setdefault(p, []).append(c)
		parent[c] = p
	# Find the root (the one node with no parent)
	root = None
	for row in tiers:
		for key in row:
			if key not in parent:
				root = key
	lane = {}
	next_lane = [0]
	def assign_leaves(u):
		"""Depth-first left-to-right: each leaf claims the next lane."""
		if u not in children:
			lane[u] = next_lane[0]
			next_lane[0] += 1
		else:
			for c in children[u]:
				assign_leaves(c)
	assign_leaves(root)
	def centre(u):
		"""Internal nodes sit at the mean lane of their children."""
		if u not in children:
			return lane[u]
		lane[u] = sum(centre(c) for c in children[u]) / float(len(children[u]))
		return lane[u]
	centre(root)
	cx, cy, qw, qh = PREVIEW
	spacing = qh / float(next_lane[0] + 1)
	root_lane = lane[root]
	positions = {}
	for tier, row in enumerate(tiers):
		for key in row:
			x = 50 + tier * 156
			y = int(round(cy + (lane[key] - root_lane) * spacing))
			positions[key] = (x, y)
	return positions

def _layout_positions(cx, cy, qw, qh, tiers):
	"""tiers: list of lists of node keys. Returns {key: (x, y)} with tier 0 on the
	left and each subsequent tier a column to the right (horizontal, root-left)."""
	num_tiers = len(tiers)
	left_x = cx - qw / 2
	gap_x = qw / max(1, num_tiers - 1)
	positions = {}
	for tier, keys in enumerate(tiers):
		x = left_x + tier * gap_x
		n = len(keys)
		for i, key in enumerate(keys):
			y = (cy - qh / 2) + qh * (i + 1) / (n + 1)
			positions[key] = (x, y)
	return positions

def _tree_specs_1_3(tree_id, num_branches, num_tiers):
	tiers = []
	for tier in xrange(num_tiers):
		tiers.append([(branch, tier) for branch in xrange(min(tier + 1, num_branches))])
	edges = []
	for tier in xrange(num_tiers - 1):
		for branch in xrange(min(tier + 1, num_branches)):
			edges.append(((branch, tier), (branch, tier + 1)))
			if branch == tier and branch < num_branches - 1:
				edges.append(((branch, tier), (branch + 1, tier + 1)))
	return tiers, edges

def _preset_4_spec():
	"""Build (tiers, edges, codes) from the troops file so the preview always
	matches the generated troops. Node indices are the list order in PRESET_4_UNITS."""
	index_of = {}
	for i, (label, _, _) in enumerate(PRESET_4_UNITS):
		index_of[label] = i
	children = []
	edges = []
	for i, (_, _, child_labels) in enumerate(PRESET_4_UNITS):
		child_idx = [index_of[c] for c in child_labels]
		children.append(child_idx)
		for c in child_idx:
			edges.append((i, c))
	tiers = []
	frontier = [0]
	while frontier:
		tiers.append(frontier)
		nxt = []
		for parent in frontier:
			nxt.extend(children[parent])
		frontier = nxt
	codes = [label for label, _, _ in PRESET_4_UNITS]
	return tiers, edges, codes

def _branch_tier_code_ops(branch, tier):
	return [(str_store_string, s0, "@|" + chr(ord('A') + branch) + str(tier + 1) + "|")]

def _code_label_ops(code):
	return [(str_store_string, s0, "@|" + code + "|")]

def _edge_endpoints(px, py, qx, qy):
	"""Endpoints for the line between two node centers so it starts just past the
	parent label's text and stops just before the child label's text (the line
	never passes behind a label)."""
	if qx >= px:
		return (px + NODE_CONNECTOR_HALF, py), (qx - NODE_CONNECTOR_HALF, qy)
	return (px - NODE_CONNECTOR_HALF, py), (qx + NODE_CONNECTOR_HALF, qy)

def _draw_tree_ops(tiers, edges, label_fn, positions=None):
	"""Ops that draw one tree in the preview area. Each edge is drawn from the
	parent label box's border to the child label box's border so the labels sit in
	clean gaps and the line never passes behind them. label_fn(key) stores the
	node's code into s0. If positions is given it overrides the default layout
	(used by preset 4's lane-based layout)."""
	cx, cy, qw, qh = PREVIEW
	ops = []
	if positions is None:
		positions = _layout_positions(cx, cy, qw, qh, tiers)
	keys = []
	for row in tiers:
		for key in row:
			keys.append(key)
	for parent, child in edges:
		px, py = positions[parent]
		qx, qy = positions[child]
		(sx, sy), (ex, ey) = _edge_endpoints(px, py, qx, qy)
		ops.append((call_script, "script_kct_prsnt_lines_to", sx, sy, ex, ey, EDGE_COLOR))
	for key in keys:
		x, y = positions[key]
		ops.extend(label_fn(key))
		ops.append((call_script, "script_kct_create_text_overlay", "str_s0", x, y, NODE_LABEL_SIZE, NODE_LABEL_W, NODE_LABEL_H, tf_center_justify|tf_vertical_align_center))
		ops.append((overlay_set_color, reg1, LABEL_COLOR))
	return ops

def _tree_specs():
	specs = []
	for tree_id, num_branches, num_tiers in PRESET_TREES_1_3:
		tiers, edges = _tree_specs_1_3(tree_id, num_branches, num_tiers)
		specs.append((tiers, edges, lambda key: _branch_tier_code_ops(key[0], key[1])))
	tiers, edges, codes = _preset_4_spec()
	specs.append((tiers, edges, lambda key: _code_label_ops(codes[key])))
	return specs

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
			(start_presentation, "prsnt_cstm_create_troop_tree"),
			(presentation_set_duration, 0),
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

####################################################################################################################
# BRIDGE / HAND-OFF for the troop tree CREATION step (next agent).
#
# prsnt_cstm_create_troop_tree is entered after the player picks a tree + gender in
# prsnt_cstm_choose_troop_tree ("Choose" button). State available on entry:
#   $cstm_selected_tree   0..3  index into PRESET_NAMES (0-2 = presets 1-3, 3 = preset 4)
#   $cstm_selected_gender 0/1   skin id (0 = male, 1 = female)
#
# The creation agent replaces this stub's load/event ops below with the real
# creation UI (the troop tree creator). The camp test entry (game_menus.py,
# mno_kct_test_tree_picker) opens the picker; "Exit" here returns to camp.
####################################################################################################################

def _build_create_load_ops():
	ops = [
		(set_fixed_point_multiplier, 1000),
	]
	ops.append((str_store_string, s0, "@Create your kingdom's troop tree"))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", 500, 700, 1000, 900, 50, tf_center_justify))
	# Debug line: which tree was chosen
	ops.append((assign, reg0, "$cstm_selected_tree"))
	ops.append((val_add, reg0, 1))
	ops.append((str_store_string, s0, "@Tree chosen: {reg0}"))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", 500, 560, 900, 500, 50, tf_center_justify))
	# Debug line: which gender was chosen
	ops.append((try_begin,))
	ops.append((eq, "$cstm_selected_gender", 1))
	ops.append((str_store_string, s0, "@Gender: Female"))
	ops.append((else_try,))
	ops.append((str_store_string, s0, "@Gender: Male"))
	ops.append((try_end,))
	ops.append((call_script, "script_kct_create_text_overlay", "str_s0", 500, 480, 900, 500, 50, tf_center_justify))
	# Exit button
	ops.append((str_store_string, s0, "@Exit"))
	ops.append((call_script, "script_kct_create_game_button_overlay", "str_s0", 500, 60))
	ops.append((assign, "$cstm_create_tree_exit", reg1))
	ops.append((presentation_set_duration, 999999))
	return ops

def _build_create_run_ops():
	return [
		(try_begin,),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
		(try_end,),
	]

def _build_create_event_ops():
	return [
		(store_trigger_param_1, ":object"),
		(try_begin,),
			(eq, ":object", "$cstm_create_tree_exit"),
			(change_screen_return),
			(presentation_set_duration, 0),
		(try_end,),
	]

new_create_presentation = ("cstm_create_troop_tree", 0, mesh_load_window, [
	(ti_on_presentation_load, _build_create_load_ops()),
	(ti_on_presentation_run, _build_create_run_ops()),
	(ti_on_presentation_event_state_change, _build_create_event_ops()),
])

def modmerge(var_set):
	try:
		orig_presentations = var_set["presentations"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"presentations\".")
	orig_presentations.append(new_presentation)
	orig_presentations.append(new_create_presentation)
