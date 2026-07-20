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

get_random_melee_training_weapon_scripts = [
#script_start_fucking
("get_random_melee_training_weapon",
   [
     (assign, ":weapon_1", -1),
     (assign, ":weapon_2", -1),
     (store_random_in_range, ":random_no", 0, 3),
     (try_begin),
       (eq, ":random_no", 0),
       (assign, ":weapon_1", "itm_practice_staff"),
     (else_try),
       (eq, ":random_no", 1),
       (assign, ":weapon_1", "itm_practice_sword"),
       (assign, ":weapon_2", "itm_practice_shield"),
     (else_try),
       (assign, ":weapon_1", "itm_heavy_practice_sword"),
     (try_end),
     (assign, reg0, ":weapon_1"),
     (assign, reg1, ":weapon_2"),
     ])
]
