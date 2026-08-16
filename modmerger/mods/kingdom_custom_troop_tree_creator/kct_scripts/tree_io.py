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

# Import/export of the current custom troop tree as a WSE dict JSON file
# (CSTM_TROOP_TREES_SPEC.md sections 8 & 11). The whole tree round-trips:
# per-troop name/plural, attributes, skills, proficiencies, equipment with
# modifiers, the configured flag, plus the tree index and the troop prefix.
#
# File layout (saved with dict_save_json -> <name>.json in the WSE managed
# directory, see become_king_troop_config.md):
#   kct_version (int = 1), kct_tree (int 0..3), kct_count (int),
#   kct_prefix (string, the kingdom troop tree prefix)
#   per troop i: t{i}_name, t{i}_plural, t{i}_att{j} j=0..3,
#   t{i}_skl{j} j=0..41 (42 skills), t{i}_wpt{j} j=0..6,
#   t{i}_eq_item{j} / t{i}_eq_mod{j} j=0..9 (num_equipment_kinds slots),
#   t{i}_conf (int, the configured flag)
#
# Source of truth = the real custom troop (non-hero, inventory capacity =
# num_equipment_kinds); the dummy troop (hero) supplies the unit names - the
# same split the store's Save uses (kct_replace_custom_troop_with_dummy).

# Mirrors layout.PRESET_TREES_1_3 + branch_display._build_create_setup_ops so
# the import (started from the picker, where $cstm_troops_begin/_end are not
# set) can compute the troop range without re-rendering the presentation.
PRESET_TREES_1_3 = [
	("1_tier", 1, 7),
	("2_tiers", 2, 6),
	("3_tiers", 3, 5),
]

def _build_compute_range_ops():
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

TREE_IO_SCRIPTS = [
# script_kct_compute_tree_range - sets $cstm_num_tiers / $cstm_troops_begin /
# $cstm_troops_end / $cstm_presentation_troop from $cstm_selected_tree and
# $cstm_selected_gender (used by the import, which runs from the picker).
	("kct_compute_tree_range", _build_compute_range_ops()),

# script_kct_export_tree_to_file - no params. Packs the current tree (selected
# via $cstm_selected_tree / $cstm_troops_begin / $cstm_troops_end) into a dict
# and saves it as <prefix>.json. The file name is derived from the tree prefix
# (the name of trp_cstm_custom_troops_end, cstm_troop_tree_prefix) so it always
# matches the name saved in the slot registry.
	("kct_export_tree_to_file",
	[
		# Name = the tree prefix (also the export file name); "Custom" if empty.
		# Keep it in s2: the pack loop below clobbers s0/s1, so the name must
		# live in a register the loop never touches.
		(str_store_troop_name, s2, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s2),
			(str_store_string, s2, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s2),
		(try_end,),

		(dict_create, "$kct_export_dict"),
		(dict_set_int, "$kct_export_dict", "@kct_version", 1),
		(dict_set_int, "$kct_export_dict", "@kct_tree", "$cstm_selected_tree"),
		(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
		(troop_get_slot, ":budget", cstm_troop_tree_prefix, ":budget_slot"),
		(dict_set_int, "$kct_export_dict", "@kct_budget", ":budget"),
		(dict_set_str, "$kct_export_dict", "@kct_prefix", s2),

		(assign, ":index", 0),
		(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),

			(assign, reg0, ":index"),
			(str_store_string, s1, "@t{reg0}_name"),
			(str_store_troop_name, s0, ":dummy"),
			(dict_set_str, "$kct_export_dict", s1, s0),

			(str_store_string, s1, "@t{reg0}_plural"),
			(str_store_troop_name_plural, s0, ":dummy"),
			(dict_set_str, "$kct_export_dict", s1, s0),

			(try_for_range, ":att", 0, 4),
				(assign, reg0, ":index"),
				(assign, reg1, ":att"),
				(str_store_string, s1, "@t{reg0}_att{reg1}"),
				(store_attribute_level, ":val", ":troop", ":att"),
				(dict_set_int, "$kct_export_dict", s1, ":val"),
			(try_end,),

			(try_for_range, ":skill", 0, 42),
				(assign, reg0, ":index"),
				(assign, reg1, ":skill"),
				(str_store_string, s1, "@t{reg0}_skl{reg1}"),
				(store_skill_level, ":val", ":skill", ":troop"),
				(dict_set_int, "$kct_export_dict", s1, ":val"),
			(try_end,),

			(try_for_range, ":wpt", 0, 7),
				(assign, reg0, ":index"),
				(assign, reg1, ":wpt"),
				(str_store_string, s1, "@t{reg0}_wpt{reg1}"),
				(store_proficiency_level, ":val", ":troop", ":wpt"),
				(dict_set_int, "$kct_export_dict", s1, ":val"),
			(try_end,),

			(try_for_range, ":slot", 0, num_equipment_kinds),
				(assign, reg0, ":index"),
				(assign, reg1, ":slot"),
				(troop_get_inventory_slot, ":item", ":troop", ":slot"),
				(troop_get_inventory_slot_modifier, ":imod", ":troop", ":slot"),
				(val_max, ":item", 0),
				(val_max, ":imod", 0),
				(str_store_string, s1, "@t{reg0}_eq_item{reg1}"),
				(dict_set_int, "$kct_export_dict", s1, ":item"),
				(str_store_string, s1, "@t{reg0}_eq_mod{reg1}"),
				(dict_set_int, "$kct_export_dict", s1, ":imod"),
			(try_end,),

			(assign, reg0, ":index"),
			(str_store_string, s1, "@t{reg0}_conf"),
			# t{i}_conf = 1 if the node is fully defined: its store Save was
			# pressed (slot 520), it carries any equipment, or any stat/skill/
			# proficiency is above the CSTM defaults (gender-aware). A blank
			# node (no gear, exactly the seeded defaults) exports 0, so the
			# bottom-up editing restriction survives an export/import round-trip
			# unless the node was actually configured.
			(assign, ":val", 0),
			(troop_get_slot, ":conf", ":troop", cstm_slot_troop_configured),
			(try_begin,),
				(eq, ":conf", 1),
				(assign, ":val", 1),
			(try_end,),
			(try_begin,),
				(eq, ":val", 0),
				(try_for_range, ":slot", 0, num_equipment_kinds),
					(troop_get_inventory_slot, ":item", ":troop", ":slot"),
					(gt, ":item", 0),
					(assign, ":val", 1),
				(try_end,),
			(try_end,),
			(try_begin,),
				(eq, ":val", 0),
				(troop_get_type, ":gender", ":troop"),
				(assign, ":def_str", CSTM_STR_START),
				(assign, ":def_agi", CSTM_AGI_START),
				(assign, ":def_int", CSTM_INT_START),
				(assign, ":def_cha", CSTM_CHA_START),
				(try_begin,),
					(eq, ":gender", 1),
					(val_add, ":def_agi", 1),
				(else_try,),
					(val_add, ":def_str", 1),
				(try_end,),
				(store_attribute_level, ":cur", ":troop", ca_strength),
				(gt, ":cur", ":def_str"),
				(assign, ":val", 1),
				(store_attribute_level, ":cur", ":troop", ca_agility),
				(gt, ":cur", ":def_agi"),
				(assign, ":val", 1),
				(store_attribute_level, ":cur", ":troop", ca_intelligence),
				(gt, ":cur", ":def_int"),
				(assign, ":val", 1),
				(store_attribute_level, ":cur", ":troop", ca_charisma),
				(gt, ":cur", ":def_cha"),
				(assign, ":val", 1),
				(store_skill_level, ":cur", skl_trade, ":troop"),
				(gt, ":cur", 2),
				(assign, ":val", 1),
				(store_skill_level, ":cur", skl_inventory_management, ":troop"),
				(gt, ":cur", 2),
				(assign, ":val", 1),
				(store_skill_level, ":cur", skl_prisoner_management, ":troop"),
				(gt, ":cur", 1),
				(assign, ":val", 1),
				(store_skill_level, ":cur", skl_leadership, ":troop"),
				(gt, ":cur", 1),
				(assign, ":val", 1),
				(try_for_range, ":proficiency", proficiencies_begin, proficiencies_end),
					(store_proficiency_level, ":cur", ":troop", ":proficiency"),
					(gt, ":cur", CSTM_WP_LEVELS_START),
					(assign, ":val", 1),
				(try_end,),
			(try_end,),
			(dict_set_int, "$kct_export_dict", s1, ":val"),

			# t{i}_eqmod = the node's "defined" state (same derivation as conf).
			# The store's Save-time propagation only writes into troops whose
			# equipment_modified slot is 0; exporting this flag lets a restored
			# imported tree carry it so an edited ancestor never overwrites an
			# already-defined node's gear. Computed at export, restored verbatim
			# at import (the import never derives it).
			(assign, reg0, ":index"),
			(str_store_string, s1, "@t{reg0}_eqmod"),
			(dict_set_int, "$kct_export_dict", s1, ":val"),

			(assign, reg0, ":index"),
			(str_store_string, s1, "@t{reg0}_cls"),
			(troop_get_slot, ":val", ":troop", cstm_slot_troop_class_override),
			(dict_set_int, "$kct_export_dict", s1, ":val"),

			(val_add, ":index", 1),
		(try_end,),

		(dict_set_int, "$kct_export_dict", "@kct_count", ":index"),
		(dict_save_json, "$kct_export_dict", s2),
		(dict_free, "$kct_export_dict"),

		(display_message, "@Tree '{s2}' exported"),
	]),

# script_kct_save_tree_to_slot - exports the current tree into the save-slot
# registry with auto-assignment: if a slot already holds a tree with the same
# name it is overwritten (rename), otherwise the first empty slot is used. If
# all kct_tree_slot_count slots are full and no name matches, nothing is saved
# and a message is shown. reg0 = 1 on success, 0 on failure.
	("kct_save_tree_to_slot",
	[
		# Name = the tree prefix (also the export file name); "Custom" if empty
		(str_store_troop_name, s0, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s0),
			(str_store_string, s0, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
		(try_end,),

		# Load the save-slot registry (create + persist it if it does not exist)
		(try_begin,),
			(gt, "$kct_tree_registry", 0),
			(array_free, "$kct_tree_registry"),
		(try_end,),
		(str_store_string, s4, kct_tree_registry_file),
		(assign, "$kct_tree_registry", 0),
		(array_load_file, "$kct_tree_registry", s4),
		(try_begin,),
			(eq, "$kct_tree_registry", 0),
			(array_create, "$kct_tree_registry", 1, kct_tree_slot_count),
			(array_save_file, "$kct_tree_registry", s4),
		(try_end,),

		# 1) find a slot that already holds this name (case-insensitive)
		(assign, ":slot", -1),
		(try_for_range, ":i", 0, kct_tree_slot_count),
			(array_get_val, s1, "$kct_tree_registry", ":i"),
			(try_begin,),
				(str_compare, ":cmp", s0, s1, 1),
				(eq, ":cmp", 0),
				(assign, ":slot", ":i"),
			(try_end,),
		(try_end,),

		# 2) else the first empty slot
		(try_begin,),
			(eq, ":slot", -1),
			(try_for_range, ":i", 0, kct_tree_slot_count),
				(array_get_val, s1, "$kct_tree_registry", ":i"),
				(try_begin,),
					(str_is_empty, s1),
					(assign, ":slot", ":i"),
				(try_end,),
			(try_end,),
		(try_end,),

		(try_begin,),
			(eq, ":slot", -1),
			(display_message, "@All slots are full - delete a tree first", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(array_set_val, "$kct_tree_registry", s0, ":slot"),
			(str_store_string, s4, kct_tree_registry_file),
			(array_save_file, "$kct_tree_registry", s4),
			(call_script, "script_kct_export_tree_to_file"),
			(assign, reg1, ":slot"),
			(val_add, reg1, 1),
			(display_message, "@Tree saved to slot {reg1}"),
			(assign, reg0, 1),
		(try_end,),
	]),

# script_kct_import_tree_from_file - param 1: template name (string register).
# Loads <name>.json, validates it against the current tree, sets the selected
# tree from the file header, applies every stored value to the tree's troops
# and syncs their dummies. reg0 = 1 on success, 0 on failure (message shown).
	("kct_import_tree_from_file",
	[
		(store_script_param, ":template", 1),
		# Snapshot the template name into s3 (a register the rest of this script
		# never touches) - the import loop below clobbers s0/s1.
		(str_store_string_reg, s3, ":template"),

		(dict_create, "$kct_import_dict"),
		(dict_load_file_json, "$kct_import_dict", s3),

		(dict_get_int, ":version", "$kct_import_dict", "@kct_version", 0),
		(try_begin,),
			(neq, ":version", 1),
			(display_message, "@Template '{s3}' not found or unsupported", 0xff0000),
			(dict_free, "$kct_import_dict"),
			(assign, reg0, 0),
		(else_try,),
			(dict_get_int, "$cstm_selected_tree", "$kct_import_dict", "@kct_tree", 0),
			(call_script, "script_kct_compute_tree_range"),

			(store_sub, ":range_count", "$cstm_troops_end", "$cstm_troops_begin"),
			(dict_get_int, ":file_count", "$kct_import_dict", "@kct_count", 0),
			(try_begin,),
				(neq, ":range_count", ":file_count"),
				(display_message, "@Template '{s3}' does not match the selected tree", 0xff0000),
				(dict_free, "$kct_import_dict"),
				(assign, reg0, 0),
			(else_try,),
				(dict_get_str, s0, "$kct_import_dict", "@kct_prefix"),
				(troop_set_name, cstm_troop_tree_prefix, s0),

				# Per-tree budget: read @kct_budget (default 3 = Auto so templates
				# without the key - exported before this feature - adapt to the
				# gear cost instead of a fixed level table).
				(dict_get_int, ":budget", "$kct_import_dict", "@kct_budget", 3),
				(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
				(troop_set_slot, cstm_troop_tree_prefix, ":budget_slot", ":budget"),

				(assign, ":index", 0),
				(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
					(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),

					(assign, reg0, ":index"),
					(str_store_string, s1, "@t{reg0}_name"),
					(dict_get_str, s0, "$kct_import_dict", s1),
					(troop_set_name, ":dummy", s0),
					(str_store_string, s1, "@t{reg0}_plural"),
					(dict_get_str, s0, "$kct_import_dict", s1),
					(troop_set_plural_name, ":dummy", s0),

					(call_script, "script_kct_troop_reset_stats", ":troop"),

					(try_for_range, ":att", 0, 4),
						(assign, reg0, ":index"),
						(assign, reg1, ":att"),
						(str_store_string, s1, "@t{reg0}_att{reg1}"),
						(dict_get_int, ":val", "$kct_import_dict", s1, 0),
						(store_attribute_level, ":cur", ":troop", ":att"),
						(store_sub, ":diff", ":val", ":cur"),
						(gt, ":diff", 0),
						(troop_raise_attribute, ":troop", ":att", ":diff"),
					(try_end,),

					(try_for_range, ":skill", 0, 42),
						(assign, reg0, ":index"),
						(assign, reg1, ":skill"),
						(str_store_string, s1, "@t{reg0}_skl{reg1}"),
						(dict_get_int, ":val", "$kct_import_dict", s1, 0),
						(store_skill_level, ":cur", ":skill", ":troop"),
						(store_sub, ":diff", ":val", ":cur"),
						(gt, ":diff", 0),
						(troop_raise_skill, ":troop", ":skill", ":diff"),
					(try_end,),

					(try_for_range, ":wpt", 0, 7),
						(assign, reg0, ":index"),
						(assign, reg1, ":wpt"),
						(str_store_string, s1, "@t{reg0}_wpt{reg1}"),
						(dict_get_int, ":val", "$kct_import_dict", s1, 0),
						(store_proficiency_level, ":cur", ":troop", ":wpt"),
						(store_sub, ":diff", ":val", ":cur"),
						(gt, ":diff", 0),
						(troop_raise_proficiency_linear, ":troop", ":wpt", ":diff"),
					(try_end,),

					(troop_clear_inventory, ":troop"),
					(try_for_range, ":slot", 0, num_equipment_kinds),
						(assign, reg0, ":index"),
						(assign, reg1, ":slot"),
						(str_store_string, s1, "@t{reg0}_eq_item{reg1}"),
						(dict_get_int, ":item", "$kct_import_dict", s1, 0),
						(str_store_string, s1, "@t{reg0}_eq_mod{reg1}"),
						(dict_get_int, ":imod", "$kct_import_dict", s1, 0),
						(gt, ":item", 0),
						(troop_set_inventory_slot, ":troop", ":slot", ":item"),
						(troop_set_inventory_slot_modifier, ":troop", ":slot", ":imod"),
					(try_end,),

					(assign, reg0, ":index"),
					(str_store_string, s1, "@t{reg0}_conf"),
					(dict_get_int, ":conf", "$kct_import_dict", s1, 0),
					(troop_set_slot, ":troop", cstm_slot_troop_configured, ":conf"),

					(assign, reg0, ":index"),
					(str_store_string, s1, "@t{reg0}_eqmod"),
					(dict_get_int, ":eqmod", "$kct_import_dict", s1, 0),
					(troop_set_slot, ":troop", cstm_slot_troop_equipment_modified, ":eqmod"),

					(assign, reg0, ":index"),
					(str_store_string, s1, "@t{reg0}_cls"),
					(dict_get_int, ":cls", "$kct_import_dict", s1, 0),
					(troop_set_slot, ":troop", cstm_slot_troop_class_override, ":cls"),

					(call_script, "script_kct_copy_custom_troop_to_dummy", ":troop"),
					(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),

					(val_add, ":index", 1),
				(try_end,),

				(dict_free, "$kct_import_dict"),
				(assign, reg0, 1),
				(display_message, "@Tree imported"),
			(try_end,),
		(try_end,),
	]),
]
