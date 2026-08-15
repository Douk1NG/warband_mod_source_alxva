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

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

# KCT guard integration (guard_kct_integration_tasks.md T2/T3).
#
# Once the player saves a troop tree, the faction slots that drive every guard
# site in the game are pointed at the custom tree's troops so the guards the
# player actually meets are their own. The writes are correlated to the Save
# event (script_kct_apply_guard_replacements is only called from the creator's
# Save button), never automatic: no tree saved = no slot touched, and the
# native guards stay exactly as the base module defined them.
#
# Guard unit selection (per the user's design, session 2026-08-15):
#   - Only the tree's INFANTRY and ARCHER units are used (no cavalry). A unit
#     counts as infantry/archer from its class override slot (533): explicit
#     1=infantry / 3=archers, or Auto (0) derived from its equipment (horse ->
#     cavalry, bow/crossbow -> archers, otherwise -> infantry) - the same rule
#     script_kct_apply_troop_class applies on Save.
#   - Tier floor: only tree tier index >= 3 is eligible (the tiers that fill
#     the game's tier_3/tier_4+ slots, level 19+ on 1_tier, 20+ on 2_tiers,
#     22+ on 3_tiers, 26+ on preset 4).
#   - Street slots (tier_2/tier_3/tier_4) are picked per branch: branch 0 for
#     tier_2, branch 1 for tier_3 (else branch 0), branch 2 for tier_4 (else
#     branch 0). Each branch is scanned top-down for its strongest infantry/
#     archer at tier >= 3; if the branch has none, it falls back to that
#     branch's tier-3 unit regardless of class.
#   - guard + castle_guard = the LAST infantry/archer tier (all branches
#     scanned top-down, infantry or archers - no cavalry). If none exists at
#     tier >= 3 the slot is left native (no write).
#   - prison_guard = branch 0, mid tier (num_tiers // 2, clamped to >= 3),
#     regardless of class (its class check falls back to the same unit).
# Written to BOTH fac_culture_player (the player faction's culture, read by
# villages/vassal recruitment paths) and fac_player_supporters_faction (the
# player faction itself, read by town/castle street and prison-break paths).
#
# The class is a runtime value (per-troop slot 533 + equipment), so the scan
# runs at Save time: script_kct_guard_cf_troop_eligible classifies one troop
# and the generated script walks the selected tree's candidate units.
#
# Mirrors layout.PRESET_TREES_1_3 + branch_display._build_create_setup_ops so
# the guard slots can be derived from the selected tree without re-deriving the
# troop range (same pattern as tree_io.PRESET_TREES_1_3).
PRESET_TREES_1_3 = [
	("1_tier", 1, 7),
	("2_tiers", 2, 6),
	("3_tiers", 3, 5),
]

# Preset 4 node indices per level (0 = weakest .. 5 = strongest). The tree's
# levels map to tiers; each level lists every node the player can build there.
PRESET_4_LEVELS = [
	[0], [1, 2], [3, 4, 5, 6], [7, 8, 9, 10, 11, 12],
	[13, 14, 15, 16, 17, 18], [19, 20, 21],
]

# Tree tier index used as the floor for every guard-picking scan ("tier 3 en
# adelante"): the tiers that fill the game's tier_3/tier_4 slots.
MIN_GUARD_TIER = 3

def _troop_id(tree_id, skin_id, branch_or_node, tier, preset4=False):
	# presets 1-3: (branch, tier) -> cstm_custom_troop_<tree>_<skin>_<branch>_<tier>
	# preset 4:    branch_or_node is the node index -> cstm_custom_troop_4_<skin>_<node>_0
	if preset4:
		return "trp_" + preset_4_troop_id(skin_id, branch_or_node)
	return "trp_cstm_custom_troop_%s_%d_%d_%d" % (tree_id, skin_id, branch_or_node, tier)

def _emit_class_scan_ops(candidates, infantry_only, fallback, best_reg=":best", found_reg=":found"):
	# Walk the candidates in priority order and keep the first one whose class
	# is usable (infantry_only: infantry only, else infantry or archers) in
	# best_reg / found_reg. If none is usable, use `fallback` (a troop id used
	# regardless of class) or, when fallback is None, leave found_reg = 0 so
	# the caller can skip the write and keep the native guard.
	ops = [(assign, found_reg, 0)]
	for troop in candidates:
		ops += [
			(try_begin,),
			(eq, found_reg, 0),
			(call_script, "script_kct_guard_cf_troop_eligible", troop, 1 if infantry_only else 0),
			(assign, best_reg, troop),
			(assign, found_reg, 1),
			(try_end,),
		]
	if fallback is not None:
		ops += [
			(try_begin,),
			(eq, found_reg, 0),
			(assign, best_reg, fallback),
			(assign, found_reg, 1),
			(try_end,),
		]
	return ops

def _emit_write_ops(slots, guarded, best_reg=":best"):
	ops = []
	if guarded:
		ops += [(try_begin,), (eq, ":found", 1)]
	for slot in slots:
		ops += [
			(faction_set_slot, "fac_culture_player", slot, best_reg),
			(faction_set_slot, "fac_player_supporters_faction", slot, best_reg),
		]
	if guarded:
		ops += [(try_end,)]
	return ops

def _build_tree_guard_ops(tree_id, num_branches, num_tiers, skin_id, preset4):
	ops = []
	if preset4:
		# Street slots scan their level (floor 3): tier_2 -> level 3, tier_3 ->
		# level 4, tier_4 -> level 5. Fallback = the level's first node,
		# regardless of class.
		street_slots = [slot_faction_tier_2_troop, slot_faction_tier_3_troop, slot_faction_tier_4_troop]
		for slot, level in zip(street_slots, (3, 4, 5)):
			nodes = PRESET_4_LEVELS[level]
			candidates = [_troop_id(None, skin_id, n, None, preset4=True) for n in nodes]
			ops += _emit_class_scan_ops(candidates, infantry_only=False, fallback=candidates[0])
			ops += _emit_write_ops([slot], guarded=False)
		# guard + castle_guard = last infantry/archer tier: levels 5..3, all nodes.
		guard_candidates = []
		for level in (5, 4, 3):
			guard_candidates += [_troop_id(None, skin_id, n, None, preset4=True) for n in PRESET_4_LEVELS[level]]
		ops += _emit_class_scan_ops(guard_candidates, infantry_only=False, fallback=None)
		ops += _emit_write_ops([slot_faction_guard_troop, slot_faction_castle_guard_troop], guarded=True)
		# prison = mid tier (6 // 2 = 3), first node, any class.
		prison_troop = _troop_id(None, skin_id, PRESET_4_LEVELS[3][0], None, preset4=True)
	else:
		# Street slots per branch: tier_2 -> branch 0, tier_3 -> branch 1 (if
		# the tree has two branches, else branch 0), tier_4 -> branch 2 (if it
		# has three, else branch 0). Each branch is scanned once top-down for
		# its strongest infantry/archer at tier >= 3; fallback = that branch's
		# tier-3 unit regardless of class.
		street_slots = [slot_faction_tier_2_troop, slot_faction_tier_3_troop, slot_faction_tier_4_troop]
		street_branches = [0, min(1, num_branches - 1), min(2, num_branches - 1)]
		branch_bests = {}
		for branch in sorted(set(street_branches)):
			candidates = [_troop_id(tree_id, skin_id, branch, t) for t in range(num_tiers - 1, MIN_GUARD_TIER - 1, -1)]
			fallback = _troop_id(tree_id, skin_id, branch, MIN_GUARD_TIER)
			best_reg = ":best_b%d" % branch
			found_reg = ":found_b%d" % branch
			ops += _emit_class_scan_ops(candidates, infantry_only=False, fallback=fallback, best_reg=best_reg, found_reg=found_reg)
			branch_bests[branch] = best_reg
		for slot, branch in zip(street_slots, street_branches):
			ops += _emit_write_ops([slot], guarded=False, best_reg=branch_bests[branch])
		# guard + castle_guard = last infantry/archer tier: all branches, top-down.
		guard_candidates = []
		for t in range(num_tiers - 1, MIN_GUARD_TIER - 1, -1):
			for b in range(min(t, num_branches - 1) + 1):
				guard_candidates.append(_troop_id(tree_id, skin_id, b, t))
		ops += _emit_class_scan_ops(guard_candidates, infantry_only=False, fallback=None)
		ops += _emit_write_ops([slot_faction_guard_troop, slot_faction_castle_guard_troop], guarded=True)
		# prison = branch 0, mid tier (num_tiers // 2, clamped to >= 3), any class.
		prison_tier = max(num_tiers // 2, MIN_GUARD_TIER)
		prison_troop = _troop_id(tree_id, skin_id, 0, prison_tier)
	# Prison write (always the mid-tier unit; its class fallback is the same
	# troop, so no scan is needed).
	ops += [(assign, ":best", prison_troop)]
	ops += _emit_write_ops([slot_faction_prison_guard_troop], guarded=False)
	return ops

def _build_apply_guard_replacements_ops():
	ops = []
	for i, (tree_id, num_branches, num_tiers) in enumerate(PRESET_TREES_1_3):
		ops.append((try_begin,) if i == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_tree", i))
		for s in (0, 1):
			ops.append((try_begin,) if s == 0 else (else_try,))
			ops.append((eq, "$cstm_selected_gender", s))
			ops.extend(_build_tree_guard_ops(tree_id, num_branches, num_tiers, s, preset4=False))
		ops.append((try_end,))
	# Preset 4 (6 tiers)
	ops.append((else_try,))
	ops.append((eq, "$cstm_selected_tree", 3))
	for s in (0, 1):
		ops.append((try_begin,) if s == 0 else (else_try,))
		ops.append((eq, "$cstm_selected_gender", s))
		ops.extend(_build_tree_guard_ops(None, None, 6, s, preset4=True))
	ops.append((try_end,))
	ops.append((try_end,))
	return ops

GUARD_REPLACEMENTS_SCRIPTS = [
# script_kct_guard_cf_troop_eligible - returns reg0 = 1 when the troop's class
# is usable for a guard slot, 0 otherwise. Param 2 = 1 to accept infantry only,
# 0 = infantry or archers. Guard/castle_guard use 0 (infantry or archers, no
# cavalry); streets/prison use it too. A troop that carries a horse is cavalry
# regardless of its class label (a "mounted archer" with class 3 or an
# "infantry" that rides still fights mounted), so a horse in the inventory
# disqualifies it from every guard slot, checked before the class label. Class
# from slot 533: 1 = infantry, 2 = cavalry (never usable), 3 = archers; 0 = Auto,
# derived from the troop's own equipment the same way script_kct_apply_troop_class
# derives it (horse -> cavalry, bow/crossbow -> archers, otherwise infantry).
	("kct_guard_cf_troop_eligible",
	[
		(store_script_param, ":troop", 1),
		(store_script_param, ":infantry_only", 2),

		(assign, reg0, 0),
		(troop_get_slot, ":class_override", ":troop", cstm_slot_troop_class_override),
		(call_script, "script_kct_cf_troop_has_horse", ":troop"),

		(try_begin),
			(eq, reg0, 1),
			(assign, reg0, 0),
		(else_try),
			(eq, ":class_override", 2),
			(assign, reg0, 0),
		(else_try),
			(eq, ":class_override", 1),
			(assign, reg0, 1),
		(else_try),
			(eq, ":class_override", 3),
			(eq, ":infantry_only", 0),
			(assign, reg0, 1),
		(else_try),
			(eq, ":class_override", 0),
			(call_script, "script_kct_cf_troop_has_bow_or_crossbow", ":troop"),
			(try_begin),
				(eq, ":infantry_only", 0),
				(assign, reg0, 1),
			(else_try),
				(assign, reg0, 0),
			(try_end),
		(else_try),
			(eq, ":class_override", 0),
			(assign, reg0, 1),
		(try_end),
	]),

	("kct_apply_guard_replacements", _build_apply_guard_replacements_ops()),

	# script_kct_restore_native_guards - heals saves polluted by earlier dev
	# builds (some native kingdoms' guard/prison/castle slots were written with
	# the tree's weakest troop). Runs on every load and restores each native
	# kingdom's guard/prison/castle slots to the native guard matching its
	# culture (the same mapping as initialize_faction_troop_types). The write is
	# unconditional: native kingdoms never legitimately hold custom troops (the
	# apply only writes fac_player_supporters_faction + fac_culture_player), and
	# on a clean save the slots already hold native values so the restore is a
	# no-op (idempotent). Culture is matched with faction_slot_eq because
	# faction_get_slot returns a RAW culture index while fac_culture_* constants
	# are ENCODED (0x6000...+index) - a plain eq of the two is always false, and
	# this is exactly why the old gated version never healed anything.
	("kct_restore_native_guards",
	[
		(try_for_range, ":kingdom", "fac_kingdom_1", "fac_kingdoms_end"),
			(assign, ":is_native", 0),
			(try_begin,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_1"),
				(assign, ":guard", "trp_swadian_sergeant"),
				(assign, ":prison", "trp_swadian_prison_guard"),
				(assign, ":castle", "trp_swadian_castle_guard"),
				(assign, ":is_native", 1),
			(else_try,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_2"),
				(assign, ":guard", "trp_vaegir_guard"),
				(assign, ":prison", "trp_vaegir_prison_guard"),
				(assign, ":castle", "trp_vaegir_castle_guard"),
				(assign, ":is_native", 1),
			(else_try,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_3"),
				(assign, ":guard", "trp_khergit_horseman"),
				(assign, ":prison", "trp_khergit_prison_guard"),
				(assign, ":castle", "trp_khergit_castle_guard"),
				(assign, ":is_native", 1),
			(else_try,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_4"),
				(assign, ":guard", "trp_nord_warrior"),
				(assign, ":prison", "trp_nord_prison_guard"),
				(assign, ":castle", "trp_nord_castle_guard"),
				(assign, ":is_native", 1),
			(else_try,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_5"),
				(assign, ":guard", "trp_rhodok_veteran_spearman"),
				(assign, ":prison", "trp_rhodok_prison_guard"),
				(assign, ":castle", "trp_rhodok_castle_guard"),
				(assign, ":is_native", 1),
			(else_try,),
				(faction_slot_eq, ":kingdom", slot_faction_culture, "fac_culture_6"),
				(assign, ":guard", "trp_sarranid_castle_guard"),
				(assign, ":prison", "trp_sarranid_prison_guard"),
				(assign, ":castle", "trp_sarranid_castle_guard"),
				(assign, ":is_native", 1),
			(try_end,),
			(try_begin,),
				(eq, ":is_native", 1),
				(faction_set_slot, ":kingdom", slot_faction_guard_troop, ":guard"),
				(faction_set_slot, ":kingdom", slot_faction_prison_guard_troop, ":prison"),
				(faction_set_slot, ":kingdom", slot_faction_castle_guard_troop, ":castle"),
			(try_end,),
		(try_end,),
	]),
]
