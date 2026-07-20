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

assign_seneschals_scripts = [
("assign_seneschals",
		[
          #seneschals - dckplmc
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (store_sub, ":offset", ":center_no", walled_centers_begin),
            (store_add, ":cur_object_no", "trp_town_1_seneschal", ":offset"),
            (troop_set_slot, ":cur_object_no", slot_troop_occupation, slto_kingdom_seneschal),
            (party_set_slot,":center_no", slot_town_seneschal, ":cur_object_no"),
          (try_end),
		])
]
