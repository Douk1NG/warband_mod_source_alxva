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
	# Array handles are runtime-only in WSE2 (not serialized into savegames), so
	# after loading a save the handles cached in these globals are stale/invalid.
	# Zero them so the > 0 guards in the store's code (kct_save_tree_to_slot,
	# tree_files) skip the array_free and re-create the arrays fresh instead of
	# freeing an invalid handle.
	(assign, "$kct_tree_registry", 0),
	(assign, "$kct_slot_row_texts", 0),
	(assign, "$kct_slot_checkboxes", 0),
	(try_for_range, ":troop", cstm_troops_begin, cstm_troops_end),
		(try_begin,),
			(troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
			(gt, ":dummy", 0),
			(call_script, "script_kct_replace_custom_troop_with_dummy", ":troop"),
		(try_end,),
	(try_end,),
]
for skin_id in (0, 1):
	for node_index in xrange(len(PRESET_4_UNITS)):
		real_id = "trp_" + preset_4_troop_id(skin_id, node_index)
		new_load_operations.extend([
			(try_begin),
				(troop_get_slot, ":dummy", real_id, cstm_slot_troop_dummy),
				(gt, ":dummy", 0),
				(call_script, "script_kct_replace_custom_troop_with_dummy", real_id),
			(try_end),
		])

new_simple_triggers = [
	(0, new_load_operations),
]

def modmerge(var_set):
	print "KCT_DEBUG: modmerge called for simple_triggers, pre len = %d" % len(var_set["simple_triggers"])
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
	print "KCT_DEBUG: post len = %d" % len(orig_simple_triggers)
