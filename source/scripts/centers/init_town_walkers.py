# ======================================================================
# SHARED DEPENDENCY
# Entity: init_town_walkers (script)
# Called by menus in 2 domains: town, village
# ======================================================================

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

init_town_walkers_scripts = [
# script_init_town_walkers
# Input: none
# Output: none
("init_town_walkers",
  [
    (try_begin),
      (eq, "$town_nighttime", 0),
      (try_for_range, ":walker_no", 0, num_town_walkers),
        (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
        (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
        (gt, ":walker_troop_id", 0),
        (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
        (set_visitor, ":entry_no", ":walker_troop_id"),
      (try_end),
    (try_end),
  ])
]
