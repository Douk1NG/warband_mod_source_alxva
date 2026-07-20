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

get_center_ideal_prosperity_scripts = [
#script_get_center_ideal_prosperity
# INPUT: arg1 = center_no
# OUTPUT: reg0 = ideal_prosperity
("get_center_ideal_prosperity",
    [(store_script_param, ":center_no", 1),
     (assign, ":ideal", 65),

	 (call_script, "script_center_get_goods_availability", ":center_no"),
     (store_mul, ":hardship_index", reg0, 2),
	 (val_sub, ":ideal", ":hardship_index"),

     (try_begin),
       (is_between, ":center_no", villages_begin, villages_end),
       (party_slot_eq, ":center_no", slot_center_has_fish_pond, 1),
       (val_add, ":ideal", 5),
     (try_end),

     (val_max, ":ideal", 0),

     (assign, reg0, ":ideal"),
     ])
]
