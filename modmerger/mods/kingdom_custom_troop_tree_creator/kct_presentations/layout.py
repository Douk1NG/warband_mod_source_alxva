# -*- coding: cp1254 -*-
import module_skills
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

# Reuse (not re-declare) the custom_troops mod's slot/string/array constants,
# item-type strings and stat ranges - custom_troops is active and mandatory.
from custom_troops_constants import *

# KCTT custom preset troops (single source of truth for additional graph shapes).
from kingdom_custom_troop_tree_creator_constants import KCT_CUSTOM_PRESETS, PRESET_4_UNITS, PRESET_TREES_1_3, preset_4_troop_id, kct_custom_preset_units

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

PRESET_NAMES = [
	"Preset 1 - 1 branch, 7 tiers",
	"Preset 2 - 2 branches, 6 tiers",
	"Preset 3 - 3 branches, 5 tiers",
] + [name for _, name, _ in KCT_CUSTOM_PRESETS]

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
CSTM_TREE_TITLE_POS_Y = 690

CSTM_TREE_POS_X = 100
CSTM_TREE_POS_Y = 75
CSTM_TREE_X_RIGHT_PADDING = 150

CSTM_TREE_Y_OFFSET = 145

CSTM_PREFIX_LABEL_POS_X = CSTM_TREE_TITLE_POS_X - 20
CSTM_PREFIX_LABEL_WIDTH = 75
CSTM_PREFIX_POS_Y = 660

CSTM_BUTTONS_POS_X = 800
CSTM_BUTTONS_POS_Y = 685
CSTM_BUTTONS_SIZE_X = 100
CSTM_BUTTONS_SIZE_Y = 30
CSTM_BUTTONS_GAP = 20

CSTM_EXPORT_BUTTON_POS = (CSTM_BUTTONS_POS_X - 60, CSTM_BUTTONS_POS_Y - 10)

# Per-tree equipment budget selector (creator header, below the prefix input):
# picker-style "label -> select": a separate "Budget" text label overlay sits to
# the LEFT of a combo BUTTON (dropdown); the option strings carry no prefix, so
# the select shows just Balanced (0) / Boosted (1) / Cheater (2) / Auto (3).
# Auto uses the gear cost (import default).
# BUDGET_COMBO_SIZE is applied with overlay_set_size exactly like the troop
# editor's item-type / item-modifier selects (750x750 - the proven store
# pattern), so the combo renders at that size instead of the native default.
BUDGET_OPTIONS = ("Balanced", "Boosted", "Cheater", "Auto")
BUDGET_COMBO_POS  = (225, 610)
BUDGET_LABEL_POS  = (60, 625)
BUDGET_LABEL_FONT = 900
BUDGET_LABEL_AREA = (130, 50)
BUDGET_COMBO_SIZE = (750, 750)   # store-proven combo resize

# Existing-troops toggle (below the Budget combo): a checkbox labelled
# "Update troops:" - the text label is aligned with the Budget label (X=60,
# same font/style) but sits lower on screen so it never overlaps the budget
# row; the checkbox sits to its right. Checked (1) = Yes: on Save the owned
# garrisons get the 50/50 infantry/archer focused refill (default refill when
# the tree cannot provide both lineages) and the player's party custom stacks
# are re-created fresh. Value persisted in $cstm_update_existing_troops (0/1,
# default 0 = unchecked).
UPDATE_EXISTING_LABEL_POS      = (90, 570)
UPDATE_EXISTING_LABEL_FONT     = 900
UPDATE_EXISTING_LABEL_AREA     = (260, 50)
UPDATE_EXISTING_CHECKBOX_POS   = (160, 560)
UPDATE_EXISTING_CHECKBOX_SIZE  = 0   # 0 = native mesh size (no overlay_set_size)

# Preset-4 node portrait size (sits inline with the branch skeleton).
P4_PORTRAIT_W = 330
P4_PORTRAIT_H = 441

# First KCT attribute-tooltip string. The three kct_tip_* attribute strings are
# appended contiguously (strength, agility, intelligence) in custom_troops_strings,
# so begin + attribute_id resolves the right one.
kct_attribute_tooltips_begin = "str_kct_tip_strength"

# --- Customisation store layout (ported from the custom_troops store, renamed
# CSTM_* -> KCT_* so the viewer's own CSTM_BUTTONS_* constants stay separate).

ACTIVE_FIGHTING_SKILLS = [skill for skill in module_skills.skills
	if skill[2] & sf_inactive == 0 and skill[2] & 0xf in (ca_strength, ca_agility)]

KCT_INV_SLOT_SIZE = 80
KCT_INV_CONT_WIDTH = 3
KCT_INV_CONT_HEIGHT = 4
KCT_INV_POS_X = 40
KCT_INV_POS_Y = 50

KCT_STORE_SLOT_SIZE = 80
KCT_STORE_CONT_WIDTH = 3
KCT_STORE_CONT_HEIGHT = 7

KCT_STORE_POS_X = KCT_INV_POS_X + KCT_INV_SLOT_SIZE * KCT_INV_CONT_WIDTH + 45
KCT_STORE_POS_Y = KCT_INV_POS_Y

KCT_STATS_POS_X = KCT_STORE_POS_X + KCT_STORE_SLOT_SIZE * KCT_STORE_CONT_WIDTH + 35
KCT_STATS_POS_Y = 0

KCT_STATS_SIZE_X = 960 - KCT_STATS_POS_X
KCT_STATS_SIZE_Y = KCT_STORE_CONT_HEIGHT * KCT_STORE_SLOT_SIZE + KCT_STORE_POS_Y - KCT_STATS_POS_Y - 15

KCT_STATS_POINTS_TEXT_SIZE = 900
KCT_STATS_POINTS_ROW_HEIGHT = 25
KCT_STATS_POINTS_COL_WIDTH = 185

KCT_STATS_ATTR_TEXT_SIZE = 1000
KCT_STATS_ATTR_ROW_HEIGHT = 27
KCT_STATS_ATTR_COL_WIDTH = 120
KCT_STATS_ATTR_CONT_WIDTH = 3
KCT_STATS_ATTR_SECTION_HEIGHT = KCT_STATS_ATTR_ROW_HEIGHT + KCT_STATS_POINTS_ROW_HEIGHT

KCT_STATS_PROF_TEXT_SIZE = 950
KCT_STATS_PROF_ROW_HEIGHT = 27
KCT_STATS_PROF_COL_WIDTH = 185
KCT_STATS_PROF_CONT_WIDTH = 2
KCT_STATS_PROF_POINTS_ROW_HEIGHT = 25
# Proficiency section: "Proficiency points: {reg0}" label on top, then the
# 7 number boxes in a 2-column grid below (original custom_troops design).
KCT_STATS_PROF_SECTION_HEIGHT = KCT_STATS_PROF_POINTS_ROW_HEIGHT + int((((proficiencies_end - 1) / KCT_STATS_PROF_CONT_WIDTH)) + 1) * KCT_STATS_PROF_ROW_HEIGHT

KCT_STATS_SKL_TEXT_SIZE = 900
KCT_STATS_SKL_ROW_HEIGHT = 27
KCT_STATS_SKL_COL_WIDTH = 185
KCT_STATS_SKL_CONT_WIDTH = 2
KCT_STATS_SKL_GRID_HEIGHT = int((((len(ACTIVE_FIGHTING_SKILLS) - 1) / KCT_STATS_SKL_CONT_WIDTH)) + 1) * KCT_STATS_SKL_ROW_HEIGHT
KCT_STATS_SKL_SECTION_HEIGHT = KCT_STATS_SKL_GRID_HEIGHT + KCT_STATS_POINTS_ROW_HEIGHT

KCT_STATS_GAP_Y = 40

KCT_NAME_POS_X = 40
KCT_NAME_POS_Y = 685
KCT_NAME_LABEL_WIDTH = 125
KCT_NAME_GAP = 340

# Gender select
KCT_GENDER_POS = (730, 60)
KCT_GENDER_SECTION_HEIGHT = 60


# Troop class selector:
# (0 = Auto / game-derived, 1 = Infantry, 2 = Cavalry, 3 = Archers)
KCT_CLASS_SECTION_HEIGHT = 60

KCT_CLASS_LABEL = (0, 490)
KCT_CLASS_SELECT = (200, 490)

KCT_BUTTONS_POS_X = 800
KCT_BUTTONS_POS_Y = KCT_NAME_POS_Y
KCT_BUTTONS_SIZE_X = 100
KCT_BUTTONS_SIZE_Y = 30
KCT_BUTTONS_GAP = 20

def _build_spec_from_units(units):
	"""Build (tiers, edges, codes) from a list of (label, level, [children_labels])
	units. Node indices are the list order in `units`."""
	index_of = {}
	for i, (label, _, _) in enumerate(units):
		index_of[label] = i
	children = []
	edges = []
	for i, (_, _, child_labels) in enumerate(units):
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
	codes = [label for label, _, _ in units]
	return tiers, edges, codes

def _compute_lanes(tiers, edges):
	"""Lane per node index: leaves get lanes 0..n-1 in left-to-right DFS order
	and internal nodes sit at the mean lane of their children. Returns {key: lane}."""
	children = {}
	parent = {}
	for p, c in edges:
		children.setdefault(p, []).append(c)
		parent[c] = p
	root = None
	for row in tiers:
		for key in row:
			if key not in parent:
				root = key
				break
		if root is not None:
			break
	lane = {}
	next_lane = [0]
	def assign_leaves(u):
		if u not in children:
			lane[u] = next_lane[0]
			next_lane[0] += 1
		else:
			for c in children[u]:
				assign_leaves(c)
	assign_leaves(root)
	def centre(u):
		if u not in children:
			return lane[u]
		lane[u] = sum(centre(c) for c in children[u]) / float(len(children[u]))
		return lane[u]
	centre(root)
	return lane

def _compute_positions_lane(tiers, lane, x_offset, gap_x, center_y, gap_y, y_shift=0):
	"""Lane-based position computation. Returns {key: (x, y)} with
	X = x_offset + tier * gap_x and Y = center_y + (lane[key] - root_lane) * gap_y - y_shift."""
	root_lane = lane[0]
	positions = {}
	for tier, row in enumerate(tiers):
		for key in row:
			x = x_offset + tier * gap_x
			y = int(round(center_y + (lane[key] - root_lane) * gap_y)) - y_shift
			positions[key] = (x, y)
	return positions

def _custom_preset_positions(tree_index):
	units = kct_custom_preset_units(tree_index)
	tiers, edges, _ = _build_spec_from_units(units)
	lane = _compute_lanes(tiers, edges)
	num_leaves = sum(1 for _, _, child_labels in units if len(child_labels) == 0)
	cx, cy, qw, qh = PREVIEW
	spacing = qh / float(num_leaves + 1)
	num_tiers = max(1, len(tiers) - 1)
	return _compute_positions_lane(tiers, lane, 50, 780.0 / num_tiers, cy, spacing)

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
	19: (423, -224),
	20: (426, -16),
	21: (427, 296),
}

P4_LABEL_CENTER = (500, 300)


def _preset_4_dummy_offset(node_index):
	"""Per-node nudge for the preset-4 dummy portraits (branch lines stay on the
	skeleton). Edit P4_DUMMY_MANUAL above to tweak individual dummies."""
	return P4_DUMMY_MANUAL.get(node_index, (0, 0))

def _preset_4_viewer_positions():
	"""Lane-based skeleton layout for the preset-4 tree, filling the whole tree
	area of the creation viewer (x 50..950, y 40..560)."""
	tiers, edges, _ = _build_spec_from_units(PRESET_4_UNITS)
	lane = _compute_lanes(tiers, edges)
	num_tiers = len(tiers)
	gap_x = 900 / (num_tiers - 1)
	return _compute_positions_lane(tiers, lane, 50, gap_x, 248, 104, y_shift=P4_VIEWER_Y_SHIFT)

def _custom_preset_viewer_positions(tree_index):
	units = kct_custom_preset_units(tree_index)
	tiers, edges, _ = _build_spec_from_units(units)
	lane = _compute_lanes(tiers, edges)
	num_tiers = max(1, len(tiers) - 1)
	gap_x = 900 / num_tiers
	return _compute_positions_lane(tiers, lane, 50, gap_x, 248, 104, y_shift=P4_VIEWER_Y_SHIFT)

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

def _custom_preset_spec(tree_index):
	return _build_spec_from_units(kct_custom_preset_units(tree_index))


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
	for tree_index, _, _ in KCT_CUSTOM_PRESETS:
		tiers, edges, codes = _custom_preset_spec(tree_index)
		specs.append((tiers, edges, lambda key, codes=codes: _code_label_ops(codes[key])))
	return specs


# Inventory area
KCT_INV_AREA_W       = 240
KCT_INV_AREA_H       = 320
KCT_INV_SLOT_FIXED   = 800   # mesh fixed-point (slot_size * 10)
KCT_INV_HALF_SLOT    = 40    # slot_size / 2 - item center inside its slot
KCT_INV_BELOW_Y      = 22

# Store area
KCT_STORE_RIGHT_EDGE = 565
KCT_STORE_BOTTOM     = 610
KCT_STORE_AREA_W     = 240
KCT_STORE_AREA_H     = 560
KCT_STORE_GRID_TOTAL = 21
KCT_STORE_SLOT_FIXED = 800   # mesh fixed-point (slot_size * 10)
KCT_STORE_HALF_SLOT  = 40    # slot_size / 2
KCT_STORE_BELOW_Y    = 22
KCT_TYPE_COMBO_POS_X = 700
KCT_TYPE_COMBO_POS_Y = 630
KCT_MOD_COMBO_POS_X  = 910
KCT_MOD_COMBO_POS_Y  = 630
KCT_PAGE_LABEL_POS_X = 485
KCT_PAGE_LABEL_POS_Y = 625
KCT_FUNDS_LABEL_POS_X= 322
KCT_FUNDS_VALUE_POS_X= 565

# Stats area
KCT_LEVEL_HP_POS_Y   = 525
KCT_ATTR_POS_Y       = 433
KCT_ATTR_POINTS_POS_Y = 460
KCT_PROF_POINTS_POS_Y = 168
KCT_SKL_GRID_Y       = 233
KCT_SKL_POINTS_POS_Y = 368

# Name area
KCT_NAME_COLUMN_X      = 165
KCT_NAME_PLURAL_COLUMN_X = 505

# Buttons
KCT_BUTTON_RIGHT_X   = 920


