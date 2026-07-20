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

store_weapon_usage_order_name_to_s1_scripts = [
("store_weapon_usage_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_weapon_usage_order, ":cur_order", ":team_no", ":class_no"),
    (team_get_hold_fire_order, ":cur_hold_fire", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Any Weapon"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Blunt Weapons"),
    (else_try),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_hold_fire"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_blunt_hold_fire"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ])
]
