# -*- coding: cp1254 -*-
from header_common import *
from header_parties import *
from header_troops import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *
from module_constants import *

from module_troops import troops

from kingdom_custom_troop_tree_creator_constants import KCT_CUSTOM_PRESETS, kct_custom_preset_troop_id

import math

party_templates = []

# KCTT custom graph presets mirror the base mod's reinforcement distribution:
#   _a -> tier 1 (5-10) + tier 2 (2-4)
#   _b -> tier 3 (5-10)
#   _c -> tier 4 (3-5)
# so AI lords/garrisons recruit the low and mid tiers of the custom tree.
def _tier_node_indexes(units, level):
	return [node_index for node_index, (_, unit_level, _) in enumerate(units) if unit_level == level]

def _stacks(tree_index, units, skin_id, level, min_count, max_count):
	node_indexes = _tier_node_indexes(units, level)
	num = len(node_indexes)
	return [(find_troop(troops, kct_custom_preset_troop_id(tree_index, skin_id, node_index)), int(math.ceil(min_count * 1.0 / num)), int(math.ceil(max_count * 1.0 / num))) for node_index in node_indexes]

for tree_index, _, units in KCT_CUSTOM_PRESETS:
	levels = sorted(set([unit_level for _, unit_level, _ in units]))
	for skin_id in (0, 1):
		id = "cstm_kingdom_player_%d_%d_reinforcements" % (tree_index, skin_id)
		party_templates.extend([
			(id + "_a", "{!}" + id + "_a", 0, 0, fac_commoners, 0, _stacks(tree_index, units, skin_id, levels[0], 5, 10) + _stacks(tree_index, units, skin_id, levels[min(1, len(levels) - 1)], 2, 4)),
			(id + "_b", "{!}" + id + "_b", 0, 0, fac_commoners, 0, _stacks(tree_index, units, skin_id, levels[min(2, len(levels) - 1)], 5, 10)),
			(id + "_c", "{!}" + id + "_c", 0, 0, fac_commoners, 0, _stacks(tree_index, units, skin_id, levels[min(3, len(levels) - 1)], 3, 5)),
		])
