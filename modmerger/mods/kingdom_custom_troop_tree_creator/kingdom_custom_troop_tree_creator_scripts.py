# -*- coding: cp1254 -*-
import collections
import math

from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from header_skills import *
from header_troops import *
from ID_items import *
from ID_meshes import *
from module_constants import *

# Reuse (not re-declare) the custom_troops mod's slot/string/array constants,
# item-type strings and stat ranges - custom_troops is active and mandatory.
from custom_troops_constants import *

from kingdom_custom_troop_tree_creator_constants import *

from kingdom_custom_troop_tree_creator.kct_scripts.ui_helpers import UI_HELPER_SCRIPTS
from kingdom_custom_troop_tree_creator.kct_scripts.branch_display import BRANCH_DISPLAY_SCRIPTS
from kingdom_custom_troop_tree_creator.kct_scripts.troop_editor import TROOP_EDITOR_SCRIPTS

new_scripts = UI_HELPER_SCRIPTS + BRANCH_DISPLAY_SCRIPTS + TROOP_EDITOR_SCRIPTS

# Set the dummy/custom-troop slot links for preset 4 at game start and seed the
# real troop with the default stats (and copy them to its dummy), mirroring
# custom_tree_start_slot_operations for the base trees (presets 1-3). Without
# this seeding the preset-4 troops keep level(troop_level)|def_attrib (STR 5,
# AGI 5, INT 4, CHA 4, 0 proficiencies, 0 skills), which does not match the
# store's point budget (level+20 based on the CSTM defaults 6/5/6/5+gender), so
# opening the store for a preset-4 troop triggers the "maximum was being set to
# X, but current value is Y" warnings that presets 1-3 never show.
# Label -> index lookup for PRESET_4_UNITS (used for the parent links below).
preset_4_index_of_label = {}
for _i, (_label, _level, _children) in enumerate(PRESET_4_UNITS):
	preset_4_index_of_label[_label] = _i

new_start_operations = []
for skin_id in (0, 1):
	for node_index in xrange(len(PRESET_4_UNITS)):
		real_id = "trp_" + preset_4_troop_id(skin_id, node_index)
		dummy_id = real_id + "_dummy"
		new_start_operations.extend([
			(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
			(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
			(call_script, "script_kct_troop_set_stats_to_default", real_id),
			(call_script, "script_kct_copy_custom_troop_to_dummy", real_id),
		])
		# Parent (upgrade) links for the bottom-up editing restriction (spec §7),
		# mirroring the base mod's loop for presets 1-3: each child's base_troop
		# is this node, so a node unlocks only after its parent is configured.
		# Also activates the min_from_tree stat minimums for preset 4.
		for child_label in PRESET_4_UNITS[node_index][2]:
			child_index = preset_4_index_of_label[child_label]
			child_real = "trp_" + preset_4_troop_id(skin_id, child_index)
			new_start_operations.append((troop_set_slot, child_real, cstm_slot_troop_base_troop, real_id))
# Populate the item arrays + funds/proficiency tables the kct store needs
# (self-contained copies of the custom_troops game-start ops).
new_start_operations.append((assign, "$cstm_items_array", cstm_items_arrays_begin))
new_start_operations.append((call_script, "script_kct_setup_item_arrays"))

# Record the required points for each proficiency level
previous_requirement = 0
for i in xrange(max(cstm_proficiency_requirements.keys()) + 1):
	requirement = previous_requirement
	if i in cstm_proficiency_requirements:
		requirement = cstm_proficiency_requirements[i]
		previous_requirement = requirement
	new_start_operations.append((troop_set_slot, "trp_cstm_proficiency_requirements", i, requirement))

# Set the allocated equipment funds for each troop level (unified at 1.5x to match
# the custom_troops save-fix trigger, so boot-time and load-restore agree; see
# CSTM_TROOP_TREES_SPEC.md §5).
for i in xrange(64):
	inventory_value = equipment_funds_available(i)
	inventory_value = int(round(inventory_value * 1.5))
	new_start_operations.append((troop_set_slot, "trp_cstm_inventory_values", i, inventory_value))

# Set item types of arrays
for item_type in cstm_item_type_strings.keys():
	new_start_operations.append((troop_set_slot, "trp_" + cstm_items_array_id(item_type), cstm_slot_array_item_type, item_type))


class Script:
	def __init__(self, id, operations):
		self.id = id
		self.operations = operations

	def convert_to_tuple(self):
		return (self.id, self.operations)

def modmerge(var_set):
	try:
		orig_scripts = var_set["scripts"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"scripts\".")

	orig_scripts.extend(new_scripts)

	scripts = collections.OrderedDict()
	for script_tuple in orig_scripts:
		scripts[script_tuple[0]] = Script(*script_tuple)

	scripts["game_start"].operations.extend(new_start_operations)

	del orig_scripts[:]
	for script_id in scripts:
		orig_scripts.append(scripts[script_id].convert_to_tuple())
