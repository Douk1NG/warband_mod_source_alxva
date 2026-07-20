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

cf_center_get_free_walker_scripts = [
# script_cf_center_get_free_walker
# Input: arg1 = center_no
# Output: reg0 = walker no (can fail)
("cf_center_get_free_walker",
   [
       (store_script_param, ":center_no", 1),
       (assign, ":num_free_walkers", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_add, ":num_free_walkers", 1),
       (try_end),
       (gt, ":num_free_walkers", 0),
       (assign, reg0, -1),
       (store_random_in_range, ":random_rank", 0, ":num_free_walkers"),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_sub, ":num_free_walkers", 1),
         (eq, ":num_free_walkers", ":random_rank"),
         (assign, reg0, ":walker_no"),
       (try_end),
     ])
]
