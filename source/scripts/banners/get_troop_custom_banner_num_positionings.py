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

get_troop_custom_banner_num_positionings_scripts = [
# script_get_troop_custom_banner_num_positionings
# Input: arg1 = troop_no
# Output: reg0 = num_positionings
("get_troop_custom_banner_num_positionings",
    [
      (store_script_param, ":troop_no", 1),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (try_begin),
        (eq, ":num_charges", 1),
        (assign, ":num_positionings", 2),
      (else_try),
        (eq, ":num_charges", 2),
        (assign, ":num_positionings", 4),
      (else_try),
        (eq, ":num_charges", 3),
        (assign, ":num_positionings", 6),
      (else_try),
        (assign, ":num_positionings", 2),
      (try_end),
      (assign, reg0, ":num_positionings"),
     ])
]
