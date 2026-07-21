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

dplmc_randomize_faction_domestic_policy_scripts = [
#SB : add this to allow randomization of a single faction (see prsnt_dplmc_policy_management)
("dplmc_randomize_faction_domestic_policy",
    [
    (store_script_param, ":kingdom", 1),
    (try_for_range, ":slot", dplmc_slot_faction_centralization, dplmc_slot_faction_mercantilism + 1),
      (store_random_in_range, ":random", -3, 4),
      (faction_set_slot, ":kingdom", ":slot", ":random"),
    (try_end),
    ])
]
