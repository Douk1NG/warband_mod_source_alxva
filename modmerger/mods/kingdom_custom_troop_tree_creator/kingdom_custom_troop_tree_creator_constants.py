# -*- coding: cp1254 -*-
from header_troops import *

tf_guarantee_all = tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield|tf_guarantee_ranged

man_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
man_face_younger_2 = 0x000000003f0052064deeffffffffffff00000000001efff90000000000000000
woman_face_1 = 0x0000000000000001000000000000000000000000001c00000000000000000000
woman_face_2 = 0x00000003bf0030067ff7fbffefff6dff00000000001f6dbf0000000000000000

# Preset 4 - 22 units matching extended_progression_tree.md (A -> B.1/B.2 ->
# C.1-C.4 -> D1-D6 -> E1-E6 -> F1-F3, one level per quality tier). Each entry:
# (unit label, troop level, [upgrade target labels]).
PRESET_4_UNITS = [
	("A",  4,  ["B1", "B2"]),
	("B1", 10, ["C1", "C2"]),
	("B2", 10, ["C3", "C4"]),
	("C1", 18, ["D1"]),
	("C2", 18, ["D2"]),
	("C3", 18, ["D3", "D4"]),
	("C4", 18, ["D5", "D6"]),
	("D1", 26, ["E1"]),
	("D2", 26, ["E2"]),
	("D3", 26, ["E3"]),
	("D4", 26, ["E4"]),
	("D5", 26, ["E5"]),
	("D6", 26, ["E6"]),
	("E1", 34, ["F1"]),
	("E2", 34, []),
	("E3", 34, ["F2"]),
	("E4", 34, []),
	("E5", 34, []),
	("E6", 34, ["F3"]),
	("F1", 40, []),
	("F2", 40, []),
	("F3", 40, []),
]

def preset_4_troop_id(skin_id, node_index):
	return "cstm_custom_troop_4_%d_%d_0" % (skin_id, node_index)

def average_face(face_1, face_2):
	age_and_skin_mask = 0xfffffffffffffffff00000000000000000000000000000000000000000000000
	average_features  = 0x000000000000000006db6db6db6db6db00000000000db6db0000000000000000
	return (((face_1 + face_2) / 2) & age_and_skin_mask) + average_features

# Troop slots used to link a real custom troop to its dummy. These MUST match the
# values in the base mod's custom_troops_constants (NEW_TROOP_SLOTS_BEGIN = 500)
# because the dummies for presets 1-3 are linked by the base mod at game start
# using those exact slot numbers.
cstm_slot_troop_dummy = 500
cstm_slot_troop_custom_troop = 501

# Marks a real troop as configured (its store Save pressed). Used by the bottom-up
# editing restriction (CSTM_TROOP_TREES_SPEC.md §7): a node's customise entry
# unlocks only after its upgrade parent has been configured. The base mod's
# allocator ends at 519, so 520 is free.
cstm_slot_troop_configured = 520

# Proficiency inheritance (bottom-up A -> B -> ... -> F):
# 531 = design lock: set on a troop when its first child is saved; while set,
#       only the equipment and name of that troop may be edited (stat boxes
#       are frozen). Persisted on the real troop.
# 532 = proficiency bonus: the parent's unspent proficiency points inherited
#       by this troop (rollover); added to the pool in kct_get_proficiency_points.
#       Persisted on the real troop (and mirrored on the dummy at store open).
cstm_slot_troop_design_lock = 531
cstm_slot_troop_proficiency_bonus = 532

# 528 = first-open marker for the proficiency inheritance snapshot: set on a
#      child the first time its store opens (parent configured, itself not yet
#      configured). Guarantees the inherited baseline is baked exactly once, so
#      Save/Reset only reflect real user edits and the snapshot never wipes them.
cstm_slot_troop_inherited = 528

# 533 = troop class override chosen in the store's Class selector
#      (0 = Auto / game-derived, 1 = grc_infantry, 2 = grc_cavalry, 3 = grc_archers).
#      Persisted on the real troop so the class survives game loads (re-applied
#      by the KCT start ops) and template export/import. Slot 533 is free: the
#      base mod's allocator ends at 519 and the KCT slots above use 520/528/531/532.
cstm_slot_troop_class_override = 533

# The troop whose name is used to store the custom troop tree prefix string
# (mirrors cstm_troop_tree_prefix in custom_troops_constants).
cstm_troop_tree_prefix = "trp_cstm_custom_troops_end"

# Save-slot registry shared by the creator's Export (auto-slot assignment) and
# the manage screen (prsnt_kct_manage_tree_files): kct_tree_slot_count numbered
# slots, each holding a saved tree's name (empty string = free). The name->file
# mapping lives in kct_tree_registry_file ("kct_trees.json").
kct_tree_slot_count = 8
kct_tree_registry_file = "@kct_trees"
