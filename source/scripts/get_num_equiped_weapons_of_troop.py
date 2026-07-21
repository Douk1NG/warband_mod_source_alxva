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
from module_items import items

get_num_equiped_weapons_of_troop_scripts = [
("get_num_equiped_weapons_of_troop", 
    [
      (store_script_param, ":troop_no", 1),
      
      (assign, ":num_weapons", 0),
      (try_for_range, ":cur_weapon_slot", ek_item_0, ek_head),
        (troop_get_inventory_slot, ":cur_weapon", ":troop_no", ":cur_weapon_slot"),
        (gt, ":cur_weapon", -1),
        (val_add, ":num_weapons", 1),
      (try_end),
      (assign, reg0, ":num_weapons"),
    ])
]
