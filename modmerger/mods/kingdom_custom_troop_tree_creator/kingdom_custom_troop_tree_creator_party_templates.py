# -*- coding: cp1254 -*-
from header_common import *
from header_parties import *
from header_troops import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *
from module_constants import *

from module_troops import troops

from kingdom_custom_troop_tree_creator_constants import PRESET_4_UNITS, preset_4_troop_id

import math

party_templates = []

# Preset 4 has 6 quality tiers (levels 4, 10, 18, 26, 34, 40). Mirror the base
# mod's reinforcement template distribution (custom_troops_party_templates.py):
#   _a -> tier 1 (5-10) + tier 2 (2-4)
#   _b -> tier 3 (5-10)
#   _c -> tier 4 (3-5)
# so AI lords/garrisons recruit the low and mid tiers of the custom tree.
def _tier_node_indexes(level):
	return [node_index for node_index, (_, unit_level, _) in enumerate(PRESET_4_UNITS) if unit_level == level]

def _stacks(skin_id, level, min_count, max_count):
	node_indexes = _tier_node_indexes(level)
	num = len(node_indexes)
	return [(find_troop(troops, preset_4_troop_id(skin_id, node_index)), int(math.ceil(min_count * 1.0 / num)), int(math.ceil(max_count * 1.0 / num))) for node_index in node_indexes]

for skin_id in (0, 1):
	id = "cstm_kingdom_player_4_%d_reinforcements" % skin_id
	party_templates.extend([
		(id + "_a", "{!}" + id + "_a", 0, 0, fac_commoners, 0, _stacks(skin_id, 4, 5, 10) + _stacks(skin_id, 10, 2, 4)),
		(id + "_b", "{!}" + id + "_b", 0, 0, fac_commoners, 0, _stacks(skin_id, 18, 5, 10)),
		(id + "_c", "{!}" + id + "_c", 0, 0, fac_commoners, 0, _stacks(skin_id, 26, 3, 5)),
	])
