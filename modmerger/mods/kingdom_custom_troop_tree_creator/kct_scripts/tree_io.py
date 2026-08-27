# -*- coding: cp1254 -*-
import json
import os

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

# Import/export of the current custom troop tree into vanilla savegame-backed
# hidden template troops. The whole tree round-trips: per-troop name/plural,
# attributes, skills, proficiencies, equipment with modifiers, configured flag,
# equipment-modified flag, class override, tree index, gender, budget, and tree
# prefix. Source of truth = the real custom troop for stats/equipment/slots; the
# dummy troop supplies display names, matching the store's Save split.

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
	for tree_index, _, units in KCT_CUSTOM_PRESETS:
		ops.append((else_try,))
		ops.append((eq, "$cstm_selected_tree", tree_index - 1))
		ops.append((assign, "$cstm_num_tiers", len(set([unit_level for _, unit_level, _ in units]))))
		for s in (0, 1):
			ops.append((try_begin,) if s == 0 else (else_try,))
			ops.append((eq, "$cstm_selected_gender", s))
			begin = "trp_" + kct_custom_preset_troop_id(tree_index, s, 0)
			end = "trp_" + (kct_custom_preset_troop_id(tree_index, 1, 0) if s == 0 else "cstm_custom_troop_%d_end" % tree_index)
			ops.append((assign, "$cstm_troops_begin", begin))
			ops.append((assign, "$cstm_troops_end", end))
			ops.append((assign, "$cstm_presentation_troop", "trp_cstm_presentation_troop_%d" % s))
		ops.append((try_end,))
	ops.append((try_end,))
	return ops

def _build_template_meta_resolver_ops():
	ops = [(store_script_param, ":slot", 1), (assign, reg0, 0)]
	for slot_index in xrange(kct_template_storage_slot_count):
		ops.extend([
			(try_begin,),
				(eq, ":slot", slot_index),
				(assign, reg0, "trp_" + kct_template_meta_troop_id(slot_index)),
			(try_end,),
		])
	return ops

def _build_template_node_resolver_ops():
	ops = [
		(store_script_param, ":slot", 1),
		(store_script_param, ":node", 2),
		(assign, reg0, 0),
	]
	for slot_index in xrange(kct_template_storage_slot_count):
		ops.append((try_begin,) if slot_index == 0 else (else_try,))
		ops.append((eq, ":slot", slot_index))
		for node_index in xrange(kct_template_nodes_per_slot):
			ops.extend([
				(try_begin,),
					(eq, ":node", node_index),
					(assign, reg0, "trp_" + kct_template_node_troop_id(slot_index, node_index)),
				(try_end,),
			])
	ops.append((try_end,))
	return ops

def _copy_troop_record_ops(source, name_source, destination):
	return [
		(str_store_troop_name, s0, name_source),
		(troop_set_name, destination, s0),
		(str_store_troop_name_plural, s0, name_source),
		(troop_set_plural_name, destination, s0),

		(call_script, "script_kct_troop_reset_stats", destination),
		(try_for_range, ":att", 0, 4),
			(store_attribute_level, ":val", source, ":att"),
			(troop_raise_attribute, destination, ":att", ":val"),
		(try_end,),
		(try_for_range, ":skill", 0, 42),
			(store_skill_level, ":val", ":skill", source),
			(troop_raise_skill, destination, ":skill", ":val"),
		(try_end,),
		(try_for_range, ":wpt", 0, 7),
			(store_proficiency_level, ":val", source, ":wpt"),
			(troop_raise_proficiency_linear, destination, ":wpt", ":val"),
		(try_end,),

		(troop_clear_inventory, destination),
		(try_for_range, ":slot_no", 0, num_equipment_kinds),
			(troop_get_inventory_slot, ":item", source, ":slot_no"),
			(troop_get_inventory_slot_modifier, ":imod", source, ":slot_no"),
			(gt, ":item", 0),
			(troop_set_inventory_slot, destination, ":slot_no", ":item"),
			(troop_set_inventory_slot_modifier, destination, ":slot_no", ":imod"),
		(try_end,),

		(troop_get_slot, ":val", source, cstm_slot_troop_configured),
		(troop_set_slot, destination, cstm_slot_troop_configured, ":val"),
		(troop_get_slot, ":val", source, cstm_slot_troop_equipment_modified),
		(troop_set_slot, destination, cstm_slot_troop_equipment_modified, ":val"),
		(troop_get_slot, ":val", source, cstm_slot_troop_class_override),
		(troop_set_slot, destination, cstm_slot_troop_class_override, ":val"),
		(troop_get_slot, ":val", source, cstm_slot_troop_gender),
		(troop_set_slot, destination, cstm_slot_troop_gender, ":val"),
	]

def _template_data_path(file_name):
	return os.path.join(os.path.dirname(os.path.dirname(__file__)), "kct_data", file_name)

def _template_text(value):
	try:
		return value.encode("cp1254")
	except AttributeError:
		return value

def _load_wse_json_template(file_name):
	with open(_template_data_path(file_name), "r") as template_file:
		data = json.load(template_file)
	count = int(data["kct count"])
	records = []
	for troop_index in xrange(count):
		prefix = "t%d" % troop_index
		records.append((
			_template_text(data[prefix + " name"]),
			_template_text(data[prefix + " plural"]),
			[int(data[prefix + " att%d" % i]) for i in xrange(4)],
			[int(data[prefix + " skl%d" % i]) for i in xrange(42)],
			[int(data[prefix + " wpt%d" % i]) for i in xrange(7)],
			[int(data.get(prefix + " eq item%d" % i, 0)) for i in xrange(num_equipment_kinds)],
			[int(data.get(prefix + " eq mod%d" % i, 0)) for i in xrange(num_equipment_kinds)],
			int(data.get(prefix + " conf", 0)),
			int(data.get(prefix + " eqmod", 0)),
			int(data.get(prefix + " cls", 0)),
		))
	return (
		_template_text(data["kct prefix"]),
		int(data["kct tree"]),
		int(data.get("kct budget", 3)),
		records,
	)

def _apply_template_record_ops(destination, record):
	name, plural, attributes, skills, proficiencies, items, modifiers, configured, equipment_modified, class_override = record
	ops = [
		(str_store_string, s0, "@" + name),
		(troop_set_name, destination, s0),
		(str_store_string, s0, "@" + plural),
		(troop_set_plural_name, destination, s0),
		(call_script, "script_kct_troop_reset_stats", destination),
	]
	for index, value in enumerate(attributes):
		ops.append((troop_raise_attribute, destination, index, value))
	for index, value in enumerate(skills):
		ops.append((troop_raise_skill, destination, index, value))
	for index, value in enumerate(proficiencies):
		ops.append((troop_raise_proficiency_linear, destination, index, value))
	ops.append((troop_clear_inventory, destination))
	for slot_no, item_id in enumerate(items):
		if item_id > 0:
			ops.extend([
				(troop_set_inventory_slot, destination, slot_no, item_id),
				(troop_set_inventory_slot_modifier, destination, slot_no, modifiers[slot_no]),
			])
	ops.extend([
		(troop_set_slot, destination, cstm_slot_troop_configured, configured),
		(troop_set_slot, destination, cstm_slot_troop_equipment_modified, equipment_modified),
		(troop_set_slot, destination, cstm_slot_troop_class_override, class_override),
		(troop_set_slot, destination, cstm_slot_troop_gender, 0),
	])
	return ops

def _kct_wse_filename(slot_index):
	return "@" + kct_wse_slot_filename(slot_index)

def _build_wse_export_ops():
	ops = [
		(store_script_param, ":slot", 1),
		(dict_create, ":dict"),
		(str_store_troop_name, s2, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s2),
			(str_store_string, s2, "@Custom"),
		(try_end,),
		(dict_set_str, ":dict", "@kct prefix", s2),
		(store_sub, ":count", "$cstm_troops_end", "$cstm_troops_begin"),
		(dict_set_int, ":dict", "@kct count", ":count"),
		(dict_set_int, ":dict", "@kct tree", "$cstm_selected_tree"),
		(dict_set_int, ":dict", "@kct gender", "$cstm_selected_gender"),
		(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
		(troop_get_slot, ":budget", cstm_troop_tree_prefix, ":budget_slot"),
		(dict_set_int, ":dict", "@kct budget", ":budget"),
		(dict_set_int, ":dict", "@kct version", kct_template_version),
		(assign, ":index", 0),
		(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
	]
	for idx in xrange(kct_template_nodes_per_slot):
		ops.append((try_begin,) if idx == 0 else (else_try,))
		ops.append((eq, ":index", idx))
		ops.append((str_store_troop_name, s0, ":dummy"))
		ops.append((dict_set_str, ":dict", "@t%d name" % idx, s0))
		ops.append((str_store_troop_name_plural, s0, ":dummy"))
		ops.append((dict_set_str, ":dict", "@t%d plural" % idx, s0))
		for att in xrange(4):
			ops.extend([(store_attribute_level, ":val", ":troop", att), (dict_set_int, ":dict", "@t%d att%d" % (idx, att), ":val")])
		for skl in xrange(42):
			ops.extend([(store_skill_level, ":val", skl, ":troop"), (dict_set_int, ":dict", "@t%d skl%d" % (idx, skl), ":val")])
		for wpt in xrange(7):
			ops.extend([(store_proficiency_level, ":val", ":troop", wpt), (dict_set_int, ":dict", "@t%d wpt%d" % (idx, wpt), ":val")])
		for eq_idx in xrange(num_equipment_kinds):
			ops.extend([(troop_get_inventory_slot, ":item", ":troop", eq_idx), (troop_get_inventory_slot_modifier, ":imod", ":troop", eq_idx), (dict_set_int, ":dict", "@t%d eq item%d" % (idx, eq_idx), ":item"), (dict_set_int, ":dict", "@t%d eq mod%d" % (idx, eq_idx), ":imod")])
		for slot_id, key in [(cstm_slot_troop_configured, "@t%d conf" % idx), (cstm_slot_troop_equipment_modified, "@t%d eqmod" % idx), (cstm_slot_troop_class_override, "@t%d cls" % idx), (cstm_slot_troop_gender, "@t%d gender" % idx)]:
			ops.extend([(troop_get_slot, ":val", ":troop", slot_id), (dict_set_int, ":dict", key, ":val")])
	ops.append((try_end,))
	ops.extend([
			(val_add, ":index", 1),
		(try_end,),
	])
	for s_idx in xrange(kct_seeded_template_slot_count, kct_template_slot_count):
		ops.append((try_begin,) if s_idx == kct_seeded_template_slot_count else (else_try,))
		ops.append((eq, ":slot", s_idx))
		ops.append((dict_save_json, ":dict", _kct_wse_filename(s_idx)))
	ops.append((try_end,))
	ops.extend([(dict_free, ":dict"), (assign, reg0, 1)])
	return ops

def _build_wse_import_ops():
	ops = [
		(store_script_param, ":slot", 1),
		(dict_create, ":dict"),
	]
	for s_idx in xrange(kct_seeded_template_slot_count, kct_template_slot_count):
		ops.append((try_begin,) if s_idx == kct_seeded_template_slot_count else (else_try,))
		ops.append((eq, ":slot", s_idx))
		ops.append((dict_load_file_json, ":dict", _kct_wse_filename(s_idx)))
	ops.append((try_end,))
	ops.extend([
		(try_begin,),
			(dict_is_empty, ":dict"),
			(dict_free, ":dict"),
			(display_message, "@This slot is empty", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(dict_get_int, ":version", ":dict", "@kct version", 0),
			(neq, ":version", kct_template_version),
			(dict_free, ":dict"),
			(display_message, "@Template slot version is unsupported", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(try_begin,),
				(eq, "$kct_manage_from_picker", 1),
				(eq, "$kct_import_preview_active", 1),
				(call_script, "script_kct_restore_import_preview_backup"),
				(assign, "$kct_manage_from_picker", 1),
			(try_end,),
			(dict_get_int, "$cstm_selected_tree", ":dict", "@kct tree", 0),
			(call_script, "script_kct_compute_tree_range"),
			(store_sub, ":range_count", "$cstm_troops_end", "$cstm_troops_begin"),
			(dict_get_int, ":file_count", ":dict", "@kct count", 0),
			(neq, ":range_count", ":file_count"),
			(dict_free, ":dict"),
			(display_message, "@Template slot does not match the selected tree", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(try_begin,),
				(eq, "$kct_manage_from_picker", 1),
				(neq, "$kct_import_preview_active", 1),
				(call_script, "script_kct_export_tree_to_slot_quiet", kct_import_preview_backup_slot),
				(assign, "$kct_import_preview_active", 1),
			(try_end,),
			(dict_get_str, s0, ":dict", "@kct prefix", "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
			(dict_get_int, ":budget", ":dict", "@kct budget", 3),
			(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
			(troop_set_slot, cstm_troop_tree_prefix, ":budget_slot", ":budget"),
			(assign, ":index", 0),
			(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
				(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
	])
	for idx in xrange(kct_template_nodes_per_slot):
		ops.append((try_begin,) if idx == 0 else (else_try,))
		ops.append((eq, ":index", idx))
		ops.append((dict_get_str, s0, ":dict", "@t%d name" % idx, "@Unit"))
		ops.append((troop_set_name, ":troop", s0))
		ops.append((troop_set_name, ":dummy", s0))
		ops.append((dict_get_str, s0, ":dict", "@t%d plural" % idx, "@Units"))
		ops.append((troop_set_plural_name, ":troop", s0))
		ops.append((troop_set_plural_name, ":dummy", s0))
		ops.append((call_script, "script_kct_troop_reset_stats", ":troop"))
		for att in xrange(4):
			ops.extend([(dict_get_int, ":val", ":dict", "@t%d att%d" % (idx, att), 0), (troop_raise_attribute, ":troop", att, ":val")])
		for skl in xrange(42):
			ops.extend([(dict_get_int, ":val", ":dict", "@t%d skl%d" % (idx, skl), 0), (troop_raise_skill, ":troop", skl, ":val")])
		for wpt in xrange(7):
			ops.extend([(dict_get_int, ":val", ":dict", "@t%d wpt%d" % (idx, wpt), 0), (troop_raise_proficiency_linear, ":troop", wpt, ":val")])
		ops.append((troop_clear_inventory, ":troop"))
		for eq_idx in xrange(num_equipment_kinds):
			ops.extend([(dict_get_int, ":item", ":dict", "@t%d eq item%d" % (idx, eq_idx), 0), (dict_get_int, ":imod", ":dict", "@t%d eq mod%d" % (idx, eq_idx), 0), (try_begin,), (gt, ":item", 0), (troop_set_inventory_slot, ":troop", eq_idx, ":item"), (troop_set_inventory_slot_modifier, ":troop", eq_idx, ":imod"), (try_end,)])
		for slot_id, key in [(cstm_slot_troop_configured, "@t%d conf" % idx), (cstm_slot_troop_equipment_modified, "@t%d eqmod" % idx), (cstm_slot_troop_class_override, "@t%d cls" % idx), (cstm_slot_troop_gender, "@t%d gender" % idx)]:
			ops.extend([(dict_get_int, ":val", ":dict", key, 0), (troop_set_slot, ":troop", slot_id, ":val")])
		ops.extend([(call_script, "script_kct_copy_custom_troop_to_dummy", ":troop"), (call_script, "script_kct_replace_custom_troop_with_dummy", ":troop")])
	ops.append((try_end,))
	ops.extend([
				(val_add, ":index", 1),
			(try_end,),
			(call_script, "script_kct_reapply_all_genders"),
			(dict_free, ":dict"),
			(assign, reg0, 1),
			(display_message, "@Tree imported"),
		(try_end,),
	])
	return ops

def _build_wse_is_occupied_ops():
	ops = [(store_script_param, ":slot", 1), (assign, reg0, 0), (dict_create, ":dict")]
	for s_idx in xrange(kct_seeded_template_slot_count, kct_template_slot_count):
		ops.append((try_begin,) if s_idx == kct_seeded_template_slot_count else (else_try,))
		ops.append((eq, ":slot", s_idx))
		ops.append((dict_load_file_json, ":dict", _kct_wse_filename(s_idx)))
	ops.append((try_end,))
	ops.extend([
		(try_begin,),
			(neg|dict_is_empty, ":dict"),
			(assign, reg0, 1),
		(try_end,),
		(dict_free, ":dict"),
	])
	return ops

def _build_wse_clear_ops():
	ops = [(store_script_param, ":slot", 1)]
	for s_idx in xrange(kct_seeded_template_slot_count, kct_template_slot_count):
		ops.append((try_begin,) if s_idx == kct_seeded_template_slot_count else (else_try,))
		ops.append((eq, ":slot", s_idx))
		ops.append((dict_delete_file_json, _kct_wse_filename(s_idx)))
	ops.append((try_end,))
	ops.append((assign, reg0, 1))
	return ops

def _build_wse_get_name_ops():
	ops = [(store_script_param, ":slot", 1), (dict_create, ":dict")]
	for s_idx in xrange(kct_seeded_template_slot_count, kct_template_slot_count):
		ops.append((try_begin,) if s_idx == kct_seeded_template_slot_count else (else_try,))
		ops.append((eq, ":slot", s_idx))
		ops.append((dict_load_file_json, ":dict", _kct_wse_filename(s_idx)))
	ops.append((try_end,))
	ops.extend([(dict_get_str, s0, ":dict", "@kct prefix"), (dict_free, ":dict")])
	return ops

NATIVE_DEFAULT_SLOT_TEMPLATES = [
	("Swadia", 4, [
		"trp_swadian_recruit",
		"trp_swadian_militia",
		"trp_swadian_footman",
		"trp_swadian_skirmisher",
		"trp_swadian_man_at_arms",
		"trp_swadian_infantry",
		"trp_swadian_crossbowman",
		"trp_swadian_knight",
		"trp_swadian_sergeant",
		"trp_swadian_sharpshooter",
	]),
	("Vaegirs", 4, [
		"trp_vaegir_recruit",
		"trp_vaegir_footman",
		"trp_vaegir_veteran",
		"trp_vaegir_skirmisher",
		"trp_vaegir_horseman",
		"trp_vaegir_infantry",
		"trp_vaegir_archer",
		"trp_vaegir_knight",
		"trp_vaegir_guard",
		"trp_vaegir_marksman",
	]),
	("Khergit Khanate", 5, [
		"trp_khergit_tribesman",
		"trp_khergit_skirmisher",
		"trp_khergit_horseman",
		"trp_khergit_horse_archer",
		"trp_khergit_lancer",
		"trp_khergit_veteran_horse_archer",
	]),
	("Nords", 6, [
		"trp_nord_recruit",
		"trp_nord_footman",
		"trp_nord_huntsman",
		"trp_nord_trained_footman",
		"trp_nord_archer",
		"trp_nord_warrior",
		"trp_nord_veteran_archer",
		"trp_nord_veteran",
		"trp_nord_champion",
	]),
	("Rhodoks", 7, [
		"trp_rhodok_tribesman",
		"trp_rhodok_spearman",
		"trp_rhodok_crossbowman",
		"trp_rhodok_trained_spearman",
		"trp_rhodok_trained_crossbowman",
		"trp_rhodok_veteran_spearman",
		"trp_rhodok_veteran_crossbowman",
		"trp_rhodok_sergeant",
		"trp_rhodok_sharpshooter",
	]),
	("Sarranid Sultanate", 4, [
		"trp_sarranid_recruit",
		"trp_sarranid_footman",
		"trp_sarranid_veteran_footman",
		"trp_sarranid_skirmisher",
		"trp_sarranid_horseman",
		"trp_sarranid_infantry",
		"trp_sarranid_archer",
		"trp_sarranid_mamluke",
		"trp_sarranid_guard",
		"trp_sarranid_master_archer",
	]),
]

WSE_DEFAULT_SLOT_TEMPLATES = [
	_load_wse_json_template("Falcon.json"),
	_load_wse_json_template("Calradian.json"),
]

DEFAULT_SLOT_TEMPLATES = NATIVE_DEFAULT_SLOT_TEMPLATES + WSE_DEFAULT_SLOT_TEMPLATES

def _seed_default_slot_ops(slot_index, name, selected_tree, budget, source_troops):
	ops = [
		(call_script, "script_kct_get_template_meta_troop", slot_index),
		(assign, ":meta", reg0),
		(str_store_string, s0, "@" + name),
		(troop_set_name, ":meta", s0),
		(troop_set_plural_name, ":meta", s0),
		(troop_set_slot, ":meta", kct_slot_template_occupied, 1),
		(troop_set_slot, ":meta", kct_slot_template_tree, selected_tree),
		(troop_set_slot, ":meta", kct_slot_template_gender, 0),
		(troop_set_slot, ":meta", kct_slot_template_count, len(source_troops)),
		(troop_set_slot, ":meta", kct_slot_template_budget, budget),
		(troop_set_slot, ":meta", kct_slot_template_version, kct_template_version),
	]
	for node_index, source in enumerate(source_troops):
		ops.extend([
			(call_script, "script_kct_get_template_node_troop", slot_index, node_index),
			(assign, ":template", reg0),
		])
		if isinstance(source, tuple):
			ops.extend(_apply_template_record_ops(":template", source))
		else:
			ops.extend(_copy_troop_record_ops(source, source, ":template"))
			ops.extend([
				(troop_set_slot, ":template", cstm_slot_troop_configured, 1),
				(troop_set_slot, ":template", cstm_slot_troop_equipment_modified, 1),
				(troop_set_slot, ":template", cstm_slot_troop_class_override, 0),
			])
	return ops

def _build_seed_default_slots_ops():
	ops = []
	for slot_index, template in enumerate(DEFAULT_SLOT_TEMPLATES):
		if len(template) == 3:
			name, selected_tree, source_troops = template
			budget = 3
		else:
			name, selected_tree, budget, source_troops = template
		ops.extend(_seed_default_slot_ops(slot_index, name, selected_tree, budget, source_troops))
	return ops

TREE_IO_SCRIPTS = [
# script_kct_compute_tree_range - sets $cstm_num_tiers / $cstm_troops_begin /
# $cstm_troops_end / $cstm_presentation_troop from $cstm_selected_tree and
# $cstm_selected_gender (used by the import, which runs from the picker).
	("kct_compute_tree_range", _build_compute_range_ops()),

	("kct_get_template_meta_troop", _build_template_meta_resolver_ops()),
	("kct_get_template_node_troop", _build_template_node_resolver_ops()),
	("kct_seed_default_template_slots", _build_seed_default_slots_ops()),

# script_kct_export_tree_to_slot_quiet - same storage copy as export, but
# without UI messages. Used for hidden import-preview backups.
	("kct_export_tree_to_slot_quiet",
	[
		(store_script_param, ":slot", 1),
		(call_script, "script_kct_get_template_meta_troop", ":slot"),
		(assign, ":meta", reg0),

		(str_store_troop_name, s2, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s2),
			(str_store_string, s2, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s2),
		(try_end,),
		(troop_set_name, ":meta", s2),
		(troop_set_plural_name, ":meta", s2),

		(store_sub, ":count", "$cstm_troops_end", "$cstm_troops_begin"),
		(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
		(troop_get_slot, ":budget", cstm_troop_tree_prefix, ":budget_slot"),
		(troop_set_slot, ":meta", kct_slot_template_occupied, 1),
		(troop_set_slot, ":meta", kct_slot_template_tree, "$cstm_selected_tree"),
		(troop_set_slot, ":meta", kct_slot_template_gender, "$cstm_selected_gender"),
		(troop_set_slot, ":meta", kct_slot_template_count, ":count"),
		(troop_set_slot, ":meta", kct_slot_template_budget, ":budget"),
		(troop_set_slot, ":meta", kct_slot_template_version, kct_template_version),

		(assign, ":index", 0),
		(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
			(call_script, "script_kct_get_template_node_troop", ":slot", ":index"),
			(assign, ":template", reg0),
	] + _copy_troop_record_ops(":troop", ":dummy", ":template") + [
			(val_add, ":index", 1),
		(try_end,),

		(assign, reg0, 1),
	]),

# script_kct_export_tree_to_slot - param 1: save slot index. Copies the current
# KCTT tree into vanilla hidden template troops. This replaces the WSE JSON file
# backend while keeping the same player-facing save/load workflow.
	("kct_export_tree_to_slot",
	[
		(store_script_param, ":slot", 1),
		(call_script, "script_kct_get_template_meta_troop", ":slot"),
		(assign, ":meta", reg0),

		(str_store_troop_name, s2, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s2),
			(str_store_string, s2, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s2),
		(try_end,),
		(troop_set_name, ":meta", s2),
		(troop_set_plural_name, ":meta", s2),

		(store_sub, ":count", "$cstm_troops_end", "$cstm_troops_begin"),
		(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
		(troop_get_slot, ":budget", cstm_troop_tree_prefix, ":budget_slot"),
		(troop_set_slot, ":meta", kct_slot_template_occupied, 1),
		(troop_set_slot, ":meta", kct_slot_template_tree, "$cstm_selected_tree"),
		(troop_set_slot, ":meta", kct_slot_template_gender, "$cstm_selected_gender"),
		(troop_set_slot, ":meta", kct_slot_template_count, ":count"),
		(troop_set_slot, ":meta", kct_slot_template_budget, ":budget"),
		(troop_set_slot, ":meta", kct_slot_template_version, kct_template_version),

		(assign, ":index", 0),
		(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
			(call_script, "script_kct_get_template_node_troop", ":slot", ":index"),
			(assign, ":template", reg0),
	] + _copy_troop_record_ops(":troop", ":dummy", ":template") + [
			(val_add, ":index", 1),
		(try_end,),

		(display_message, "@Tree '{s2}' saved to template slot"),
		(assign, reg0, 1),
	]),

# Compatibility wrapper for older call sites/comments. With the vanilla backend
# this no longer writes an external file; it writes to $kct_selected_slot.
	("kct_export_tree_to_file",
	[
		(call_script, "script_kct_export_tree_to_slot", "$kct_selected_slot"),
	]),

# script_kct_save_tree_to_slot - auto-assigns a vanilla in-save template slot.
# Same name overwrites; otherwise the first empty slot is used.
	("kct_save_tree_to_slot",
	[
		(str_store_troop_name, s0, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s0),
			(str_store_string, s0, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
		(try_end,),

		(assign, ":slot", -1),
		(try_for_range, ":i", 0, kct_template_slot_count),
			(eq, ":slot", -1),
			(ge, ":i", kct_seeded_template_slot_count),
			(call_script, "script_kct_get_template_meta_troop", ":i"),
			(assign, ":meta", reg0),
			(troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
			(str_store_troop_name, s1, ":meta"),
			(str_compare, ":cmp", s0, s1, 1),
			(eq, ":cmp", 0),
			(assign, ":slot", ":i"),
		(try_end,),

		(try_begin,),
			(eq, ":slot", -1),
			(try_for_range, ":i", kct_seeded_template_slot_count, kct_template_slot_count),
				(eq, ":slot", -1),
				(call_script, "script_kct_get_template_meta_troop", ":i"),
				(assign, ":meta", reg0),
				(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
				(assign, ":slot", ":i"),
			(try_end,),
		(try_end,),

		(try_begin,),
			(eq, ":slot", -1),
			(display_message, "@All slots are full - delete a tree first", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(assign, "$kct_selected_slot", ":slot"),
			(call_script, "script_kct_export_tree_to_slot", ":slot"),
			(assign, reg1, ":slot"),
			(val_add, reg1, 1),
			(display_message, "@Tree saved to slot {reg1}"),
			(assign, reg0, 1),
		(try_end,),
	]),

# script_kct_import_tree_from_slot - param 1: save slot index. Loads a vanilla
# in-save template slot back into the live KCTT tree.
	("kct_import_tree_from_slot",
	[
		(store_script_param, ":slot", 1),
		(call_script, "script_kct_get_template_meta_troop", ":slot"),
		(assign, ":meta", reg0),

		(try_begin,),
			(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
			(display_message, "@This slot is empty", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(troop_get_slot, ":version", ":meta", kct_slot_template_version),
			(neq, ":version", kct_template_version),
			(display_message, "@Template slot version is unsupported", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(try_begin,),
				(eq, "$kct_manage_from_picker", 1),
				(eq, "$kct_import_preview_active", 1),
				(call_script, "script_kct_restore_import_preview_backup"),
				(assign, "$kct_manage_from_picker", 1),
			(try_end,),
			(troop_get_slot, "$cstm_selected_tree", ":meta", kct_slot_template_tree),
			(call_script, "script_kct_compute_tree_range"),
			(store_sub, ":range_count", "$cstm_troops_end", "$cstm_troops_begin"),
			(troop_get_slot, ":file_count", ":meta", kct_slot_template_count),
			(neq, ":range_count", ":file_count"),
			(display_message, "@Template slot does not match the selected tree", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(try_begin,),
				(eq, "$kct_manage_from_picker", 1),
				(neq, "$kct_import_preview_active", 1),
				(call_script, "script_kct_export_tree_to_slot_quiet", kct_import_preview_backup_slot),
				(assign, "$kct_import_preview_active", 1),
			(try_end,),

			(str_store_troop_name, s0, ":meta"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
			(troop_get_slot, ":budget", ":meta", kct_slot_template_budget),
			(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
			(troop_set_slot, cstm_troop_tree_prefix, ":budget_slot", ":budget"),

			(assign, ":index", 0),
			(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
				(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
				(call_script, "script_kct_get_template_node_troop", ":slot", ":index"),
				(assign, ":template", reg0),
	] + _copy_troop_record_ops(":template", ":template", ":troop") + [
				(str_store_troop_name, s0, ":template"),
				(troop_set_name, ":dummy", s0),
				(str_store_troop_name_plural, s0, ":template"),
				(troop_set_plural_name, ":dummy", s0),
				(call_script, "script_kct_copy_custom_troop_to_dummy", ":troop"),
				(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),
				(val_add, ":index", 1),
			(try_end,),
			(call_script, "script_kct_reapply_all_genders"),
			(assign, reg0, 1),
			(display_message, "@Tree imported"),
		(try_end,),
	]),

	("kct_import_tree_from_file",
	[
		(store_script_param, ":slot", 1),
		(call_script, "script_kct_import_tree_from_slot", ":slot"),
	]),

	("kct_restore_import_preview_backup",
	[
		(try_begin,),
			(eq, "$kct_import_preview_active", 1),
			(call_script, "script_kct_get_template_meta_troop", kct_import_preview_backup_slot),
			(assign, ":meta", reg0),
			(troop_slot_eq, ":meta", kct_slot_template_occupied, 1),

			(troop_get_slot, "$cstm_selected_tree", ":meta", kct_slot_template_tree),
			(troop_get_slot, "$cstm_selected_gender", ":meta", kct_slot_template_gender),
			(call_script, "script_kct_compute_tree_range"),
			(store_sub, ":range_count", "$cstm_troops_end", "$cstm_troops_begin"),
			(troop_get_slot, ":file_count", ":meta", kct_slot_template_count),
			(eq, ":range_count", ":file_count"),

			(str_store_troop_name, s0, ":meta"),
			(troop_set_name, cstm_troop_tree_prefix, s0),
			(troop_get_slot, ":budget", ":meta", kct_slot_template_budget),
			(store_add, ":budget_slot", cstm_slot_tree_budget_begin, "$cstm_selected_tree"),
			(troop_set_slot, cstm_troop_tree_prefix, ":budget_slot", ":budget"),

			(assign, ":index", 0),
			(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
				(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
				(call_script, "script_kct_get_template_node_troop", kct_import_preview_backup_slot, ":index"),
				(assign, ":template", reg0),
	] + _copy_troop_record_ops(":template", ":template", ":troop") + [
				(str_store_troop_name, s0, ":template"),
				(troop_set_name, ":dummy", s0),
				(str_store_troop_name_plural, s0, ":template"),
				(troop_set_plural_name, ":dummy", s0),
				(call_script, "script_kct_copy_custom_troop_to_dummy", ":troop"),
				(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),
				(val_add, ":index", 1),
			(try_end,),
			(call_script, "script_kct_reapply_all_genders"),
		(try_end,),
		(assign, "$kct_import_preview_active", 0),
		(call_script, "script_kct_clear_template_slot", kct_import_preview_backup_slot),
	]),

	("kct_clear_template_slot",
	[
		(store_script_param, ":slot", 1),
		(call_script, "script_kct_get_template_meta_troop", ":slot"),
		(assign, ":meta", reg0),
		(str_clear, s0),
		(troop_set_name, ":meta", s0),
		(troop_set_plural_name, ":meta", s0),
		(troop_set_slot, ":meta", kct_slot_template_occupied, 0),
		(troop_set_slot, ":meta", kct_slot_template_tree, 0),
		(troop_set_slot, ":meta", kct_slot_template_gender, 0),
		(troop_set_slot, ":meta", kct_slot_template_count, 0),
		(troop_set_slot, ":meta", kct_slot_template_budget, 0),
		(troop_set_slot, ":meta", kct_slot_template_version, kct_template_version),
	]),

	# WSE backend (optional, cross-save). Same 4 user slots 8-11 but stored in
	# WSE managed JSON files kct_slot_8..11 - survives across saves.
	("kct_wse_export_tree_to_slot", _build_wse_export_ops()),
	("kct_wse_import_tree_from_slot", _build_wse_import_ops()),
	("kct_wse_is_occupied", _build_wse_is_occupied_ops()),
	("kct_wse_clear_slot", _build_wse_clear_ops()),
	("kct_wse_get_name", _build_wse_get_name_ops()),

	# Conditional wrappers - same 4 indices use WSE when available, vanilla otherwise.
	# WSE detection: (neg|is_vanilla_warband) succeeds only on WSE.
	("kct_slot_is_occupied",
	[
		(store_script_param, ":slot", 1),
		(try_begin,),
			(neg|is_vanilla_warband),
			(ge, ":slot", kct_seeded_template_slot_count),
			(call_script, "script_kct_wse_is_occupied", ":slot"),
			(assign, reg0, reg0),
		(else_try,),
			(call_script, "script_kct_get_template_meta_troop", ":slot"),
			(troop_slot_eq, reg0, kct_slot_template_occupied, 1),
			(assign, reg0, 1),
		(else_try,),
			(assign, reg0, 0),
		(try_end,),
	]),
	("kct_slot_get_name",
	[
		(store_script_param, ":slot", 1),
		(try_begin,),
			(neg|is_vanilla_warband),
			(ge, ":slot", kct_seeded_template_slot_count),
			(call_script, "script_kct_wse_get_name", ":slot"),
		(else_try,),
			(call_script, "script_kct_get_template_meta_troop", ":slot"),
			(str_store_troop_name, s0, reg0),
		(try_end,),
	]),
	("kct_slot_export_tree",
	[
		(store_script_param, ":slot", 1),
		(try_begin,),
			(neg|is_vanilla_warband),
			(ge, ":slot", kct_seeded_template_slot_count),
			(call_script, "script_kct_wse_export_tree_to_slot", ":slot"),
		(else_try,),
			(call_script, "script_kct_export_tree_to_slot", ":slot"),
		(try_end,),
	]),
	("kct_slot_import_tree",
	[
		(store_script_param, ":slot", 1),
		(try_begin,),
			(neg|is_vanilla_warband),
			(ge, ":slot", kct_seeded_template_slot_count),
			(call_script, "script_kct_wse_import_tree_from_slot", ":slot"),
		(else_try,),
			(call_script, "script_kct_import_tree_from_slot", ":slot"),
		(try_end,),
	]),
	("kct_slot_clear",
	[
		(store_script_param, ":slot", 1),
		(try_begin,),
			(neg|is_vanilla_warband),
			(ge, ":slot", kct_seeded_template_slot_count),
			(call_script, "script_kct_wse_clear_slot", ":slot"),
		(else_try,),
			(call_script, "script_kct_clear_template_slot", ":slot"),
		(try_end,),
	]),
	("kct_slot_save_tree_auto",
	[
		(str_store_troop_name, s1, cstm_troop_tree_prefix),
		(try_begin,),
			(str_is_empty, s1),
			(str_store_string, s1, "@Custom"),
			(troop_set_name, cstm_troop_tree_prefix, s1),
		(try_end,),
		(assign, ":slot", -1),
		(try_for_range, ":i", kct_seeded_template_slot_count, kct_template_slot_count),
			(eq, ":slot", -1),
			(call_script, "script_kct_slot_is_occupied", ":i"),
			(eq, reg0, 1),
			(call_script, "script_kct_slot_get_name", ":i"),
			(str_compare, ":cmp", s0, s1, 1),
			(eq, ":cmp", 0),
			(assign, ":slot", ":i"),
		(try_end,),
		(try_begin,),
			(eq, ":slot", -1),
			(try_for_range, ":i", kct_seeded_template_slot_count, kct_template_slot_count),
				(eq, ":slot", -1),
				(call_script, "script_kct_slot_is_occupied", ":i"),
				(eq, reg0, 0),
				(assign, ":slot", ":i"),
			(try_end,),
		(try_end,),
		(try_begin,),
			(eq, ":slot", -1),
			(display_message, "@All slots are full - delete a tree first", 0xff0000),
			(assign, reg0, 0),
		(else_try,),
			(assign, "$kct_selected_slot", ":slot"),
			(call_script, "script_kct_slot_export_tree", ":slot"),
			(assign, reg1, ":slot"),
			(val_add, reg1, 1),
			(display_message, "@Tree saved to slot {reg1}"),
			(assign, reg0, 1),
		(try_end,),
	]),
]
