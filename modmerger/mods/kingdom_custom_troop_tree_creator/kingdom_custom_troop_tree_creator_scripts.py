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
from kingdom_custom_troop_tree_creator.kct_scripts.tree_io import TREE_IO_SCRIPTS
from kingdom_custom_troop_tree_creator.kct_scripts.guard_replacements import GUARD_REPLACEMENTS_SCRIPTS
from kingdom_custom_troop_tree_creator.kct_scripts.existing_troops import EXISTING_TROOPS_SCRIPTS
from kingdom_custom_troop_tree_creator.kct_scripts.gender import GENDER_SCRIPTS

new_scripts = UI_HELPER_SCRIPTS + BRANCH_DISPLAY_SCRIPTS + TROOP_EDITOR_SCRIPTS + TREE_IO_SCRIPTS + GUARD_REPLACEMENTS_SCRIPTS + EXISTING_TROOPS_SCRIPTS + GENDER_SCRIPTS

# Set the dummy/custom-troop slot links for KCTT custom graph presets at game start and seed the
# real troop with the default stats (and copy them to its dummy), mirroring
# custom_tree_start_slot_operations for the base trees (presets 1-3). Without
# this seeding the preset-4 troops keep level(troop_level)|def_attrib (STR 5,
# AGI 5, INT 4, CHA 4, 0 proficiencies, 0 skills), which does not match the
# store's point budget (level+20 based on the CSTM defaults 6/5/6/5+gender), so
# opening the store for a preset-4 troop triggers the "maximum was being set to
# X, but current value is Y" warnings that presets 1-3 never show.
new_start_operations = []
for tree_index, _, units in KCT_CUSTOM_PRESETS:
	index_of_label = {}
	for _i, (_label, _level, _children) in enumerate(units):
		index_of_label[_label] = _i
	for skin_id in (0, 1):
		for node_index in xrange(len(units)):
			real_id = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, node_index)
			dummy_id = real_id + "_dummy"
			new_start_operations.extend([
				(troop_set_type, real_id, skin_id),
				(troop_set_type, dummy_id, skin_id),
				(troop_set_slot, real_id, cstm_slot_troop_dummy, dummy_id),
				(troop_set_slot, dummy_id, cstm_slot_troop_custom_troop, real_id),
				(call_script, "script_kct_troop_set_stats_to_default", real_id),
				(call_script, "script_kct_copy_custom_troop_to_dummy", real_id),
			])
			for child_label in units[node_index][2]:
				child_index = index_of_label[child_label]
				child_real = "trp_" + kct_custom_preset_troop_id(tree_index, skin_id, child_index)
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

# Set the allocated equipment funds for each troop level (Balanced, Boosted, Cheater
# tables, matching the custom_troops save-fix trigger so boot-time and load-restore
# agree; see CSTM_TROOP_TREES_SPEC.md §5).
for i in xrange(EQUIPMENT_FUNDS_TABLE_SIZE):
	balanced, boosted, cheater = equipment_funds_available(i)
	new_start_operations.append((troop_set_slot, "trp_cstm_inventory_values", i, balanced))
	new_start_operations.append((troop_set_slot, "trp_cstm_inventory_values", i + EQUIPMENT_FUNDS_TABLE_SIZE, boosted))
	new_start_operations.append((troop_set_slot, "trp_cstm_inventory_values", i + 2 * EQUIPMENT_FUNDS_TABLE_SIZE, cheater))

# Set item types of arrays
for item_type in cstm_item_type_strings.keys():
	new_start_operations.append((troop_set_slot, "trp_" + cstm_items_array_id(item_type), cstm_slot_array_item_type, item_type))

# Seed visible default/faction import slots on new game. Existing saves are
# already updated; the old load-trigger migration is retired/commented.
new_start_operations.append((call_script, "script_kct_seed_default_template_slots"))
# Retired migration breadcrumb:
# new_start_operations.append((assign, "$kct_template_slots_preset8_rhodoks_migrated", 1))


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

	enter_court_ops = scripts["enter_court"].operations
	_guard_line = None
	for _i, _op in enumerate(enter_court_ops):
		if (isinstance(_op, tuple) and len(_op) >= 3
				and _op[0] == faction_get_slot and _op[2] == "$g_player_culture"):
			_guard_line = _i
			break
	if _guard_line is not None:
		enter_court_ops[_guard_line:_guard_line + 1] = [
			(try_begin,),
				(faction_slot_ge, ":center_faction", slot_faction_guard_troop, cstm_troops_begin),
				(faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
			(else_try,),
				(faction_get_slot, ":guard_troop", "$g_player_culture", slot_faction_guard_troop),
			(try_end,),
		]
	_b2_line = None
	for _i, _op in enumerate(enter_court_ops):
		if (isinstance(_op, tuple) and len(_op) >= 3 and _op[0] == party_get_slot
				and _op[1] == ":town_lord" and _op[2] == ":center_no"):
			_next = enter_court_ops[_i + 1] if _i + 1 < len(enter_court_ops) else None
			_nnext = enter_court_ops[_i + 2] if _i + 2 < len(enter_court_ops) else None
			if (isinstance(_next, tuple) and len(_next) >= 3 and _next[0] == gt
					and _next[1] == ":town_lord"
					and isinstance(_nnext, tuple) and len(_nnext) >= 3
					and _nnext[0] == troop_get_slot
					and _nnext[1] == ":lord_original_faction"):
				_b2_line = _i
				break
	if _b2_line is not None and enter_court_ops[_b2_line - 1] == else_try:
		enter_court_ops[_b2_line - 1:_b2_line - 1] = [
			(else_try,),
				(faction_slot_ge, ":center_faction", slot_faction_guard_troop, cstm_troops_begin),
				(faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
		]
	del orig_scripts[:]
	for script_id in scripts:
		orig_scripts.append(scripts[script_id].convert_to_tuple())
