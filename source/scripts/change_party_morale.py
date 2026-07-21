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

change_party_morale_scripts = [
#ozan
("change_party_morale",
   [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":morale_dif"),

      (party_get_morale, ":cur_morale", ":party_no"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      (party_set_morale, ":party_no", ":new_morale"),
      (str_store_party_name, s1, ":party_no"),

      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
      (try_end),
  ])
]
