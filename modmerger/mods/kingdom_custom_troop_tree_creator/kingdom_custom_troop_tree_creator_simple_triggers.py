# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_constants import *

from custom_troops_constants import cstm_troops_begin, cstm_troops_end
from kingdom_custom_troop_tree_creator_constants import *

class SimpleTrigger:
	def __init__(self, check_interval, operations = []):
		self.check_interval = check_interval
		self.operations = operations

	def convert_to_tuple(self):
		return (self.check_interval, self.operations)

# Restore the real custom troops from their dummies every time a savegame is
# loaded. The real troops are non-hero def_attrib troops, so the engine resets
# their runtime stats/equipment to the module defaults on every load, while the
# dummies are tf_hero troops whose config survives (see the comment on
# cstm_slot_troop_dummy in custom_troops_constants). This is exactly what the
# store's Save button does manually ("go to castle and click save again"); this
# trigger does it automatically on load. Idempotent: on a fresh game the dummy
# mirrors the real troop, so the copy is a no-op.
#
# Presets 1-3 (the base mod's CUSTOM_TROOP_TREES, ids "1_tier"/"2_tiers"/
# "3_tiers", real troops trp_cstm_custom_troop_*_... in [cstm_troops_begin,
# cstm_troops_end)) are customised through the same KCT store, and the base mod
# links each to its dummy at game start (custom_tree_start_slot_operations), so
# we restore every real troop in that range from its dummy - same guard-and-copy
# pattern as the preset-4 block below.
new_load_operations = [
	(try_for_range, ":troop", cstm_troops_begin, cstm_troops_end),
		(try_begin,),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
			(gt, ":dummy", 0),
			(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),
		(try_end,),
	(try_end,),
]
for tree_index, _, units in KCT_CUSTOM_PRESETS:
	index_of = {}
	for node_index, (label, _, _) in enumerate(units):
		index_of[label] = node_index
	for skin_id in (0, 1):
		for node_index in xrange(len(units)):
			real_id = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, node_index)
			dummy_id = real_id + "_dummy"
			new_load_operations.extend([
				(troop_set_type, real_id, skin_id),
				(troop_set_type, dummy_id, skin_id),
				(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
				(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
				(try_begin,),
					(troop_get_slot, ":dummy", real_id, cstm_slot_troop_dummy),
					(gt, ":dummy", 0),
					(call_script, "script_kct_replace_custom_troop_with_dummy", real_id),
				(try_end,),
			])
			for child_label in units[node_index][2]:
				child_real = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, index_of[child_label])
				new_load_operations.append((troop_set_slot, child_real, cstm_slot_troop_base_troop, real_id))

# Heal the native kingdoms' guard-site faction slots (guard, castle guard,
# prison) on every load. Earlier dev builds polluted some native kingdoms'
# slots with the tree's weakest troop, and the old gated block never healed
# them (its ge gate compared a RAW global against the ENCODED cstm_troops_begin
# constant, which is always false). script_kct_restore_native_guards is
# idempotent - on a clean save the slots already hold native values, so this is
# a no-op. The apply script is deliberately NOT called here: $cstm_selected_tree
# / $cstm_selected_gender reset to 0 on load, so it would clobber the saved
# fac_player_supporters_faction / fac_culture_player slots with the preset-1
# male tree. Those slots persist correctly in the savegame.
new_load_operations.append((call_script, "script_kct_restore_native_guards"))
# Re-apply branch-gender flips after the type resets above (custom presets set
# troop_set_type to skin_id). Persisted via slot 534 on real troops.
new_load_operations.append((call_script, "script_kct_reapply_all_genders"))
# Migrate old saves: seed default template slots if not already populated.
# Checks slot 0 directly — if kct_slot_template_occupied != 1, the defaults
# haven't been seeded. Idempotent: script_kct_seed_default_template_slots
# overwrites with the same data, and the check prevents re-running on saves
# that already have the trees.
new_load_operations.extend([
	(call_script, "script_kct_get_template_meta_troop", 0),
	(assign, ":meta", reg0),
	(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1),
	(call_script, "script_kct_seed_default_template_slots"),
	(display_message, "@Default troop tree templates restored for old save", 0x44ff44),
])

new_simple_triggers = [
	(0, new_load_operations),
]

def modmerge(var_set):
	try:
		var_name_1 = "simple_triggers"
		orig_simple_triggers = var_set[var_name_1]
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)

	orig_simple_triggers.extend(new_simple_triggers)

	simple_triggers = [SimpleTrigger(*st_tuple) for st_tuple in orig_simple_triggers]

	del orig_simple_triggers[:]
	orig_simple_triggers.extend([simple_trigger.convert_to_tuple() for simple_trigger in simple_triggers])
