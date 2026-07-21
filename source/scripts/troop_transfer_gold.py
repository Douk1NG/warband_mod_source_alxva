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

troop_transfer_gold_scripts = [
("troop_transfer_gold",
    [
      (store_script_param, ":source", 1),
      (store_script_param, ":destination", 2),
      (store_script_param, ":amount", 3),
      (store_troop_gold, ":cur_amount", ":source"),
      (try_begin),
        (gt, ":amount", 0), #0 means move all
        (val_min, ":cur_amount", ":amount"),
      (try_end),
      (troop_remove_gold, ":source", ":cur_amount"),
      # (troop_add_gold, ":destination", ":cur_amount"),
      (call_script, "script_troop_add_gold", ":destination", ":cur_amount"),
      (assign, reg0, ":cur_amount"),
    ])
]
