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

get_num_backup_weapons_of_troop_scripts = [
("get_num_backup_weapons_of_troop", 
    [
      (store_script_param, ":troop_no", 1),
      
      (assign, ":num_backup_weapons", 0),
      (try_for_range, ":cur_2nd_weapon_slot", slot_2nd_weapons_1, slot_2nd_weapons_4+1),
        (troop_get_slot, ":cur_2nd_weapon_with_modifier", ":troop_no", ":cur_2nd_weapon_slot"),
        (gt, ":cur_2nd_weapon_with_modifier", 0),
        (val_add, ":num_backup_weapons", 1),
      (try_end),
      (assign, reg0, ":num_backup_weapons"),
    ])
]
