# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

cf_multiplayer_is_item_default_for_troop_scripts = [
#script_cf_multiplayer_is_item_default_for_troop
# Input: arg1 = item_no, arg2 = troop_no
# Output: reg0: total_cost
("cf_multiplayer_is_item_default_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (assign, ":default_item", 0),
     (try_begin),
       (neg|is_between, ":item_no", horses_begin, horses_end),
       (neq, ":item_no", "itm_warhorse_sarranid"),
       (neq, ":item_no", "itm_warhorse_steppe"),

       (troop_get_inventory_capacity, ":end_cond", ":troop_no"), #troop no can come -1 here error occured at friday
       (try_for_range, ":i_slot", 0, ":end_cond"),
         (troop_get_inventory_slot, ":default_item_id", ":troop_no", ":i_slot"),
         (eq, ":item_no", ":default_item_id"),
         (assign, ":default_item", 1),
         (assign, ":end_cond", 0), #break
       (try_end),
     (try_end),
     (eq, ":default_item", 1),
     ])
]
