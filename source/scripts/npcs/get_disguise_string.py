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

get_disguise_string_scripts = [
("get_disguise_string", [
      (store_script_param, ":cur_val", 1),
      (store_script_param, ":sreg", 2),
      (store_add, ":end_val", "str_pilgrim_disguise", num_disguises),
      (str_clear, ":sreg"),
      (try_for_range, ":string", "str_pilgrim_disguise", ":end_val"),
        (eq, ":cur_val", 1), #
        (assign, ":end_val", -1), #loop break
        (str_store_string, ":sreg", ":string"),
      (else_try),
        (val_div, ":cur_val", 2), #divide by 2, next iteration
      (try_end),
      ])
]
