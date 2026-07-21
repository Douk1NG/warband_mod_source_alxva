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

store_movement_order_name_to_s1_scripts = [
# Input: arg1 = team_no, arg2 = class_no
# Output: s1 = order_name
("store_movement_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_movement_order, ":cur_order", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", mordr_hold),
      (str_store_string, s1, "@Holding"),
    (else_try),
      (eq, ":cur_order", mordr_follow),
      (str_store_string, s1, "@Following"),
    (else_try),
      (eq, ":cur_order", mordr_charge),
      (str_store_string, s1, "@Charging"),
    (else_try),
      (eq, ":cur_order", mordr_advance),
      (str_store_string, s1, "@Advancing"),
    (else_try),
      (eq, ":cur_order", mordr_fall_back),
      (str_store_string, s1, "@Falling Back"),
    (else_try),
      (eq, ":cur_order", mordr_stand_closer),
      (str_store_string, s1, "@Standing Closer"),
    (else_try),
      (eq, ":cur_order", mordr_spread_out),
      (str_store_string, s1, "@Spreading Out"),
    (else_try),
      (eq, ":cur_order", mordr_stand_ground),
      (str_store_string, s1, "@Standing"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ])
]
