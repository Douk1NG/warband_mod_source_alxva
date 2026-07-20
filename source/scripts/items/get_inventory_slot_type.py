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

get_inventory_slot_type_scripts = [
("get_inventory_slot_type",
    [
      (store_script_param, ":slot_no", 1),

      (try_begin),
        (is_between, ":slot_no", 0, ek_head),
        (assign, ":slot_type", itp_type_one_handed_wpn),
      (else_try),
        (is_between, ":slot_no", ek_head, ek_horse),
        (store_sub, ":slot_type", ":slot_no", ek_head),
        (val_add, ":slot_type", itp_type_head_armor),
      (else_try),
        (eq, ":slot_no", 8),
        (assign, ":slot_type", itp_type_horse),
      (else_try),
        (assign, ":slot_type", -1),
      (try_end),
      (assign, reg0, ":slot_type"),
    ])
]
