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

center_remove_walker_type_from_walkers_scripts = [
# script_center_remove_walker_type_from_walkers
# Input: arg1 = center_no, arg2 = walker_type,
# Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
("center_remove_walker_type_from_walkers",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_type", 2),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
         (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
       (try_end),
     ])
]
