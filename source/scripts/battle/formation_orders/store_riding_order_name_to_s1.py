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

store_riding_order_name_to_s1_scripts = [
# script_store_riding_order_name_to_s1
# Input: arg1 = team_no, arg2 = class_no
# Output: s1 = order_name
("store_riding_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_riding_order, ":cur_order", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", rordr_free),
      (str_store_string, s1, "@Free"),
    (else_try),
      (eq, ":cur_order", rordr_mount),
      (str_store_string, s1, "@Mount"),
    (else_try),
      (eq, ":cur_order", rordr_dismount),
      (str_store_string, s1, "@Dismount"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ])
]
