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

multiplayer_set_item_available_for_troop_scripts = [
#script_multiplayer_set_item_available_for_troop
# Input: arg1 = item_no, arg2 = troop_no
# Output: none
("multiplayer_set_item_available_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),
     (item_set_slot, ":item_no", ":item_troop_slot", 1),
     ])
]
