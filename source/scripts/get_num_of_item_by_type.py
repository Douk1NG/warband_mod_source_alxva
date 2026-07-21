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

get_num_of_item_by_type_scripts = [
("get_num_of_item_by_type",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":item_type"),
      (assign, ":num_of_item", 0),
      (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
      (try_for_range, ":i_slot", 10, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop_no", ":i_slot"),
        (gt, ":item", -1),
        (item_get_type, ":type", ":item"),
        (eq, ":type", ":item_type"),
        (val_add, ":num_of_item", 1),
      (try_end),
      (assign, reg0, ":num_of_item"),
    ])
]
