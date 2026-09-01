# -*- coding: cp1254 -*-
# Legacy save migration for the cstm/custom_troops -> kingdom_custom_troop_tree_creator
# upgrade. Runs once per save via a simple_trigger (0, ...) in
# kingdom_custom_troop_tree_creator_simple_triggers.py.
#
# Background (from git log/code review of commit ab9f385 onwards):
#   The cstm/custom_troops mod (pre-ab9f385) used the same troop id layout as
#   the KCT (cstm_custom_troop_<preset>_<skin>_<branch>_<tier> for real troops
#   and _dummy suffix for dummies) so the troop ids are stable across the
#   upgrade. The legacy feature stored the player's name on the DUMMY and
#   the equipment + attributes + skills + proficiencies on the REAL troop.
#   On every game_start it linked the two via cstm_slot_troop_dummy (slot 500)
#   and cstm_slot_troop_custom_troop (slot 501).
#
#   The KCT rewrite inverts the source of truth: it copies DUMMY -> REAL
#   every load (script_kct_replace_custom_troop_with_dummy). For a fresh KCT
#   save the dummy mirrors the real troop so the copy is a no-op. For a
#   legacy save the dummy carries only the name (and the default empty
#   inventory/stats) - the restore wipes the real troop's config.
#
#   The migration below runs BEFORE the restore in the simple_trigger and
#   copies REAL -> DUMMY for every troop in the detected range, so the
#   subsequent restore is a no-op. The name customisation on the dummy
#   (which the player did in the legacy editor) is preserved as-is.
#
# Detection: same heuristic the mod has always used - fac_culture_player
# slot 41 (slot_faction_tier_1_troop) is unset on legacy saves; set on
# KCT saves. We also require $cstm_migration_v1_done to be 0 for full
# idempotency. The legacy feature's "save fix" trigger sets a different
# flag ($g_cstm_save_fix_applied_2) so there is no collision.
#
# We also propagate a few globals the new UI reads:
#   $cstm_selected_tree    - 0/1/2 for the three legacy presets
#   $cstm_selected_gender  - 0 male / 1 female; from the dummy's tf_ flag
#   $cstm_troops_begin/end - the live range (set by script_kct_compute_tree_range)
# We do NOT call that script here because the simple_trigger order relative
# to the KCT presentation load is what initialises $cstm_troops_begin.
# The KCT picker's "fast path" check (custom_troops_game_menus.py) reads
# fac_culture_player.slot_faction_tier_1_troop directly, so setting that
# slot is enough to make the picker skip and jump to the viewer.

from header_common import *
from header_operations import *
from header_troops import *
from header_items import *
from module_constants import *

from custom_troops_constants import cstm_troops_end
from kingdom_custom_troop_tree_creator_constants import (
	cstm_slot_troop_dummy,
	cstm_slot_troop_configured,
	cstm_slot_tree_budget_begin,
	cstm_troop_tree_prefix,
)

MIGRATE_LEGACY_V1_SCRIPTS = [
# script_kct_migrate_legacy_v1
#   Idempotent legacy-save migration. Walks the three legacy preset ranges,
#   for each preset that has a tier-0 recruit (branch 0) with a populated
#   dummy slot it copies the real troop's stats and inventory onto the
#   dummy (preserving the dummy's player-edited name), then marks the
#   range as configured and writes the active-tree marker so the KCT
#   picker skips itself on the next load.
	("kct_migrate_legacy_v1",
	[
		# Already migrated or never was a legacy save: nothing to do.
		(try_begin),
			(eq, "$cstm_migration_v1_done", 1),
		(else_try),
			# KCT path: fac_culture_player tier-1 marker is set, the KCT
			# store has been entered. Do not touch.
			(faction_get_slot, ":tier1", "fac_culture_player", slot_faction_tier_1_troop),
			(gt, ":tier1", 0),
		(else_try),
			# Walk the three legacy presets in order. First preset that has
			# a populated dummy slot at tier 0 (branch 0) wins; male is
			# preferred over female because the legacy feature initialised
			# both skins in game_start, so the dummy link being present
			# alone is not enough to identify the player's choice. We
			# rely on the slot 503 (equipment_modified) flag: legacy code
			# never set it on its own, so a non-zero value means the
			# player actually edited this troop.
			(assign, ":detected_preset", -1),
			(assign, ":detected_recruit", 0),
			(assign, ":detected_skin", -1),

			# Preset 1 (1_tier)
			(try_for_range, ":skin", 0, 2),
				(try_begin),
					(eq, ":detected_preset", -1),
					(try_begin),
						(eq, ":skin", 0),
						(assign, ":recruit", "trp_cstm_custom_troop_1_tier_0_0_0"),
					(else_try),
						(assign, ":recruit", "trp_cstm_custom_troop_1_tier_1_0_0"),
					(try_end),
					(troop_get_slot, ":eqmod", ":recruit", cstm_slot_troop_equipment_modified),
					(gt, ":eqmod", 0),
					(assign, ":detected_preset", 0),
					(assign, ":detected_recruit", ":recruit"),
					(assign, ":detected_skin", ":skin"),
				(try_end),
			(try_end),
			# Preset 2 (2_tiers)
			(try_for_range, ":skin", 0, 2),
				(try_begin),
					(eq, ":detected_preset", -1),
					(try_begin),
						(eq, ":skin", 0),
						(assign, ":recruit", "trp_cstm_custom_troop_2_tiers_0_0_0"),
					(else_try),
						(assign, ":recruit", "trp_cstm_custom_troop_2_tiers_1_0_0"),
					(try_end),
					(troop_get_slot, ":eqmod", ":recruit", cstm_slot_troop_equipment_modified),
					(gt, ":eqmod", 0),
					(assign, ":detected_preset", 1),
					(assign, ":detected_recruit", ":recruit"),
					(assign, ":detected_skin", ":skin"),
				(try_end),
			(try_end),
			# Preset 3 (3_tiers)
			(try_for_range, ":skin", 0, 2),
				(try_begin),
					(eq, ":detected_preset", -1),
					(try_begin),
						(eq, ":skin", 0),
						(assign, ":recruit", "trp_cstm_custom_troop_3_tiers_0_0_0"),
					(else_try),
						(assign, ":recruit", "trp_cstm_custom_troop_3_tiers_1_0_0"),
					(try_end),
					(troop_get_slot, ":eqmod", ":recruit", cstm_slot_troop_equipment_modified),
					(gt, ":eqmod", 0),
					(assign, ":detected_preset", 2),
					(assign, ":detected_recruit", ":recruit"),
					(assign, ":detected_skin", ":skin"),
				(try_end),
			(try_end),

			# Only migrate if we detected a v1 tree.
			(try_begin),
				(ge, ":detected_preset", 0),
				(ge, ":detected_recruit", 0),

				# Persist the active-tree marker. custom_troops_game_menus.py
				# checks this slot to decide whether to skip the picker
				# and go straight to the viewer.
				(faction_set_slot, "fac_culture_player", slot_faction_tier_1_troop, ":detected_recruit"),

				# Set the selected tree and gender globals so the KCT
				# presentation can compute the live troop range on first
				# open. Preset 1/2/3 -> $cstm_selected_tree 0/1/2.
				(assign, "$cstm_selected_tree", ":detected_preset"),
				(assign, "$cstm_selected_gender", ":detected_skin"),

				# Seed the per-tree budget slot to 0 (Balanced). The v1
				# feature had no budget concept so any non-Auto default is
				# arbitrary; Balanced matches the base mod's table at
				# equipment_funds_available.
				(store_add, ":budget_slot", cstm_slot_tree_budget_begin, ":detected_preset"),
				(troop_set_slot, cstm_troop_tree_prefix, ":budget_slot", 0),

				# For every real troop in the detected preset range:
				#   1. Copy the real troop's stats and inventory onto its
				#      dummy via script_kct_copy_custom_troop_to_dummy.
				#      This preserves the legacy "name in dummy, config
				#      in real" layout: the dummy keeps the player's
				#      edited name (script_kct_troop_copy_stats/copy_inventory
				#      only touch stats + items), and from this point on
				#      carries the real troop's stats and inventory so the
				#      subsequent dummy->real restore is a no-op.
				#   2. Mark the troop as configured (slot 520) so the
				#      bottom-up editor gate treats it as already designed
				#      and does not block the player.
				#
				# Range:
				#   1_tier   -> 7 troops
				#   2_tiers  -> 12 troops
				#   3_tiers  -> 15 troops
				# We iterate to cstm_troops_end (the cstm_custom_troops_end
				# sentinel) and gate on slot 500 > 0 - real troops in a v1
				# save are always linked to a dummy, so this skips any
				# non-custom troop that happens to live in that range after
				# module updates. We do NOT use $cstm_troops_begin/end here
				# because those globals are 0 on the very first load.
				(try_for_range, ":troop", ":detected_recruit", cstm_troops_end),
					(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
					(gt, ":dummy", 0),
					(call_script, "script_kct_copy_custom_troop_to_dummy", ":troop"),
					(troop_set_slot, ":troop", cstm_slot_troop_configured, 1),
				(try_end),

				# One-shot flag. Persisted as a global; Warband globals
				# survive save/load.
				(assign, "$cstm_migration_v1_done", 1),

				(display_message, "@Custom troop tree migrated from legacy save. Visit the capital to view it.", 0x44ff44),
			(try_end),
		(try_end),
	]),
]
