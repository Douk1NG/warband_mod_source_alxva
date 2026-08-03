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
from kingdom_custom_troop_tree_creator_troops import PRESET_4_UNITS, preset_4_troop_id

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

# Creation viewer layout constants - ported verbatim from the working
# custom_troops_presentations (prsnt_cstm_view_custom_troop_tree).
CSTM_TREE_TITLE_SIZE = 2000
CSTM_TREE_TITLE_POS_X = 50
CSTM_TREE_TITLE_POS_Y = 650

CSTM_TREE_POS_X = 100
CSTM_TREE_POS_Y = 75
CSTM_TREE_X_RIGHT_PADDING = 150

CSTM_TREE_Y_OFFSET = 145

CSTM_PREFIX_LABEL_POS_X = CSTM_TREE_TITLE_POS_X
CSTM_PREFIX_LABEL_WIDTH = 75
CSTM_PREFIX_POS_Y = 590

CSTM_BUTTONS_POS_X = 800
CSTM_BUTTONS_POS_Y = 685
CSTM_BUTTONS_SIZE_X = 100
CSTM_BUTTONS_SIZE_Y = 30
CSTM_BUTTONS_GAP = 20

# Preset-4 node portrait size (sits inline with the branch skeleton).
P4_PORTRAIT_W = 330
P4_PORTRAIT_H = 441

# Troop used to store the kingdom troop tree prefix string (mirrors
# cstm_troop_tree_prefix in the custom_troops mod).
cstm_troop_tree_prefix = "trp_cstm_custom_troops_end"

def _preset_4_lanes():
	"""Lane per preset-4 node index: leaves get lanes 0..n-1 in left-to-right DFS
	order and internal nodes sit at the mean lane of their children. Shared by the
	picker preview and the creation viewer so both show the same shape."""
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
	return lane

def _preset_4_positions():
	"""Centred layout for the preset-4 tree so it matches the preset 1-3 look:
	the root sits at the preview's vertical middle and every parent sits at the
	vertical centre of its children (a 2-option parent is centred between its two
	options, never inline with one of them). Leaves each get a lane in left-to-
	right order; an internal node's lane is the mean of its children's lanes.
	Returns {node index: (x, y)}."""
	tiers, edges, _ = _preset_4_spec()
	lane = _preset_4_lanes()
	num_leaves = sum(1 for _, _, child_labels in PRESET_4_UNITS if len(child_labels) == 0)
	cx, cy, qw, qh = PREVIEW
	spacing = qh / float(num_leaves + 1)
	root_lane = lane[0]
	positions = {}
	for tier, row in enumerate(tiers):
		for key in row:
			x = 50 + tier * 156
			y = int(round(cy + (lane[key] - root_lane) * spacing))
			positions[key] = (x, y)
	return positions

# Manual per-node portrait nudge (dx, dy) for the preset-4 dummies, in points.
# Node index = order in PRESET_4_UNITS:
#   0=A  1=B1 2=B2 3=C1 4=C2 5=C3 6=C4 7=D1 8=D2 9=D3 10=D4 11=D5 12=D6
#   13=E1 14=E2 15=E3 16=E4 17=E5 18=E6 19=F1 20=F2 21=F3
# dx > 0 moves the portrait right, dx < 0 left; dy > 0 down, dy < 0 up.
P4_DUMMY_MANUAL = {
	0: (7, -49),
	1: (8, -35),
	2: (8, -35),
	3: (0, -30),
	4: (2, -30),
	5: (7, -35),
	6: (7, -34),
	7: (-4, -29),
	8: (0, -31),
	9: (-2, -30),
	10: (0, -32),
	11: (3, -34),
	12: (1, -32),
	13: (-1, -35),
	14: (3, -33),
	15: (5, -37),
	16: (4, -40),
	17: (5, -45),
	18: (6, -32),
	19: (0, -38),
	20: (-1, -39),
	21: (3, -35),
}

# Vertical lift applied to the whole preset-4 tree in the creation viewer
# (graph lines AND dummy portraits - everything shifts together so the dummies
# stay aligned to their nodes). Moved up 40 by the user's request.
P4_VIEWER_Y_SHIFT = -40

# MANUAL NUDGE: shift ALL preset-4 dummy portraits (NOT the graph/lines/rects)
# this many units. Tweak the value, recompile, and check in game; repeat until
# every dummy is reachable, then drag each to its final spot and press Snapshot
# to fill P4_DUMMY_MANUAL.
# NOTE: in-game testing showed positive = DOWN, negative = UP (e.g. -200 was the
# right vertical lift to bring the bottom dummies into reach).
P4_DUMMY_Y_OFFSET = -200

# MANUAL NUDGE: shift ALL preset-4 dummy portraits horizontally (same idea as
# P4_DUMMY_Y_OFFSET). Positive = RIGHT, negative = LEFT - but verify in game; if
# it moves the wrong way, flip the sign (the Y axis was inverted too).
P4_DUMMY_X_OFFSET = 110

# Name label for each preset-4 dummy portrait (unit name only, e.g. "Unit A").
# Font 600 matches the presets 1-3 name text. Labels sit just right of the
# portrait, vertically centred on it; the last tier (F dummies) labels sit left
# of the portrait and right-align so the text grows leftwards (no room on the
# right - the tree reaches the screen edge).
P4_LABEL_FONT = 600
P4_LABEL_W    = 400
P4_LABEL_H    = 50
P4_LABEL_GAP  = 12

# Each label sits relative to its dummy portrait: base position = portrait
# top-left + (P4_LABEL_RIGHT_DX / P4_LABEL_LEFT_DX, P4_LABEL_DY). The last tier
# (F dummies) labels sit on the left of the portrait (no room on the right - the
# tree reaches the screen edge); the rest sit on the right. P4_LABEL_MANUAL adds
# a per-label nudge on top, filled with the P4 label drag tool.
P4_LABEL_DY       = P4_PORTRAIT_H // 2 - P4_LABEL_H // 2   # vertical centre of the portrait
P4_LABEL_RIGHT_DX = P4_PORTRAIT_W + P4_LABEL_GAP           # label's left edge, right of the dummy
P4_LABEL_LEFT_DX  = -(P4_LABEL_GAP + P4_LABEL_W)           # label's left edge, left of the dummy

# Manual per-label position (dx, dy) relative to P4_LABEL_CENTER, baked from the
# label drag tool's Snapshot output (each label shows at CENTER + this delta).
# Key = preset-4 node index (0-21).
P4_LABEL_MANUAL = {
	0: (-435, -20),
	1: (-253, -162),
	2: (-254, 151),
	3: (-79, -204),
	4: (-79, -101),
	5: (-72, 44),
	6: (-74, 252),
	7: (94, -204),
	8: (96, -101),
	9: (95, 4),
	10: (97, 106),
	11: (99, 211),
	12: (98, 314),
	13: (277, -204),
	14: (280, -104),
	15: (281, 3),
	16: (281, 97),
	17: (283, 197),
	18: (285, 316),
	19: (423, -204),
	20: (426, 4),
	21: (427, 316),
}

# TEMP P4 drag tools: two tuning tools (dummy portraits + name labels) share the
# creation viewer's bottom strip. Each has its own live readout + Snapshot
# button; readouts sit ABOVE the buttons (y 555/610 vs buttons at y 675) and are
# kept narrow (x 430..830) so they never cover the buttons or each other.
# Remove both with the tools when the offsets are baked.
#
# Both tools are DISABLED by default: the dummy offsets are baked into
# P4_DUMMY_MANUAL and the label offsets into P4_LABEL_MANUAL. Flip a flag to
# True to bring back that tool's readout + Snapshot button and re-wire its drag.
ENABLE_DUMMY_TOOL = False
ENABLE_LABEL_TOOL = False
P4_DUMMY_TOOL_TEXT_POS      = (430, 555)
P4_DUMMY_TOOL_TEXT_SIZE     = 900
P4_DUMMY_TOOL_TEXT_W        = 400
P4_DUMMY_TOOL_SNAPSHOT_POS  = (140, 675)

P4_LABEL_TOOL_TEXT_POS      = (430, 610)
P4_LABEL_TOOL_TEXT_SIZE     = 900
P4_LABEL_TOOL_TEXT_W        = 400
P4_LABEL_TOOL_SNAPSHOT_POS  = (360, 675)

# TEMP tuning: every label is dropped at this screen-centre point instead of its
# portrait-relative spot, so none are lost off-screen (right-side labels for the
# rightmost dummies sat past x=1000). Move each label by hand, then Snapshot
# bakes its delta (vs this centre) into P4_LABEL_MANUAL. Remove with the tool.
P4_LABEL_CENTER = (500, 300)


# TEMP P4 drag tools - helper files in this mod folder (imported here so the
# presentation can wire them; modmerger does not auto-process them as
# components). Each tool is self-contained: own slots in trp_temp_array_a/b/c/d,
# own $<name>_* globals, own readout + Snapshot button.
from kct_dummy_drag_tool import p4_dummy_tool
from kct_label_drag_tool import p4_label_tool

def _preset_4_dummy_offset(node_index):
	"""Per-node nudge for the preset-4 dummy portraits (branch lines stay on the
	skeleton). Edit P4_DUMMY_MANUAL above to tweak individual dummies."""
	return P4_DUMMY_MANUAL.get(node_index, (0, 0))

def _preset_4_viewer_positions():
	"""Lane-based skeleton layout for the preset-4 tree, filling the whole tree
	area of the creation viewer (x 50..950, y 40..560)."""
	tiers, _, _ = _preset_4_spec()
	lane = _preset_4_lanes()
	num_tiers = len(tiers)
	gap_x = 900 / (num_tiers - 1)
	gap_y = 104
	root_lane = lane[0]
	center_y = 248
	positions = {}
	for tier, row in enumerate(tiers):
		for key in row:
			x = 50 + tier * gap_x
			y = int(round(center_y + (lane[key] - root_lane) * gap_y)) - P4_VIEWER_Y_SHIFT
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
	ops.append((call_script, "script_kct_troop_refresh_name", ":custom_troop"))
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
			## NODE CLICKED (inert for now - customisation store comes next)
			(troop_get_slot, ":troop", "trp_cstm_overlay_troops", ":object"),
			(gt, ":troop", 0),
			(str_store_troop_name, s0, ":troop"),
			(display_message, "@{s0} - customisation coming soon"),
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

def modmerge(var_set):
	try:
		orig_presentations = var_set["presentations"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"presentations\".")
	orig_presentations.append(new_presentation)
	orig_presentations.append(new_create_presentation)
