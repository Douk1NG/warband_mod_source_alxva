# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_troops import *
from module_constants import *

from custom_troops_constants import cstm_troops_begin, cstm_troops_end, cstm_slot_troop_dummy, cstm_slot_troop_custom_troop, cstm_slot_troop_base_troop
from kingdom_custom_troop_tree_creator_constants import *


LOAD_RESTORE_SCRIPTS = []
load_restore_operations = [
	(store_script_param_1, ":party_no"),
	(store_script_param_2, ":force_restore"),
	(eq, ":party_no", "p_main_party"),
	(troop_get_class, ":restore_marker_class", "trp_kct_template_slot_0_meta"),
	(assign, reg0, ":restore_marker_class"),
	(assign, reg1, ":force_restore"),
	(display_debug_message, "@[KCT_DIAG] restore entered; force={reg1}, marker_class={reg0}"),
	(assign, ":should_restore", 0),
	(try_begin,),
		(eq, ":force_restore", 1),
		(assign, ":should_restore", 1),
	(else_try,),
		(neq, ":restore_marker_class", grc_archers),
		(assign, ":should_restore", 1),
	(try_end,),
	(eq, ":should_restore", 1),
	(display_message, "@[KCT] Restoring troop trees after load...", 0x44ff44),
	(assign, ":restored_troops", 0),
	(try_for_range, ":troop", cstm_troops_begin, cstm_troops_end),
		(try_begin,),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
			(gt, ":dummy", 0),
			(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),
			(val_add, ":restored_troops", 1),
		(try_end,),
	(try_end,),
]

# Restore the graph presets as well as the base CSTM custom troop range.
for tree_index, _, units in KCT_CUSTOM_PRESETS:
	index_of = {}
	for node_index, (label, _, _) in enumerate(units):
		index_of[label] = node_index
	for skin_id in (0, 1):
		for node_index in xrange(len(units)):
			real_id = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, node_index)
			dummy_id = real_id + "_dummy"
			load_restore_operations.extend([
				(troop_set_type, real_id, skin_id),
				(troop_set_type, dummy_id, skin_id),
				(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
				(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
				(try_begin,),
					(troop_get_slot, ":dummy", real_id, cstm_slot_troop_dummy),
					(gt, ":dummy", 0),
				]
			)
			load_restore_operations.extend([
					(call_script, "script_kct_replace_custom_troop_with_dummy", real_id),
				])
			load_restore_operations.extend([
					(val_add, ":restored_troops", 1),
				(try_end,),
			])
			for child_label in units[node_index][2]:
				child_real = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, index_of[child_label])
				load_restore_operations.append((troop_set_slot, child_real, cstm_slot_troop_base_troop, real_id))

# Keep migrations and repair steps ordered after the troop data has been restored.
load_restore_operations.append((call_script, "script_kct_restore_native_guards"))
load_restore_operations.append((call_script, "script_kct_reapply_all_genders"))
load_restore_operations.append((call_script, "script_kct_seed_missing_default_template_slots"))
load_restore_operations.append((call_script, "script_kct_restore_custom_tree_default_slots"))
load_restore_operations.append((call_script, "script_kct_restore_calradian_missing_troops"))
load_restore_operations.append((call_script, "script_kct_migrate_legacy_v1"))
# Use a new completion class so saves from earlier attempts (which marked the
# sentinel cavalry before Native restoration actually completed) retry once.
# The zero-interval trigger exits cheaply on later frames after this marker.
load_restore_operations.append((troop_set_class, "trp_cstm_load_check", grc_archers))
load_restore_operations.append((troop_set_class, "trp_kct_template_slot_0_meta", grc_archers))
load_restore_operations.extend([
	(assign, reg0, ":restored_troops"),
	(display_message, "@[KCT] Restore complete: {reg0} troops updated from saved data.", 0x44ff44),
])

LOAD_RESTORE_SCRIPTS.append(("kct_restore_troops_after_load", load_restore_operations))
