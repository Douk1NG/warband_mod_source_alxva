# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

dplmc_init_domestic_policy_scripts = [
("dplmc_init_domestic_policy",
  [
    (try_for_range, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      (try_begin),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_centralization, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_aristocracy, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_quality, ":random"),
        (store_random_in_range, ":random", -3, 4),
        (faction_set_slot, ":kingdom", dplmc_slot_faction_serfdom, ":random"),
      (try_end),
    (try_end),
  ])
]
