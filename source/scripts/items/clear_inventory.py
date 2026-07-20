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

clear_inventory_scripts = [
("clear_inventory",
   [(store_script_param_1, ":troop_id"),
    (troop_clear_inventory,":troop_id"),
    (try_for_range, ":item", 0, 10),
       (troop_set_inventory_slot, ":troop_id", ":item",  -1),
    (try_end),])
]
