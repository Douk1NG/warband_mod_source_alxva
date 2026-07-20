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

cf_is_weapon_ranged_scripts = [
("cf_is_weapon_ranged", [
      (store_script_param, ":weapon", 1),
      (store_script_param, ":include_thrown", 2),

      (assign, ":test_val", 0),
      (try_begin),
        (ge, ":weapon", 0),
        (item_get_type, ":type", ":weapon"),
        (try_begin),
          (this_or_next | eq, ":type", itp_type_bow),
          (this_or_next | eq, ":type", itp_type_crossbow),
          (this_or_next | eq, ":type", itp_type_pistol),
          (eq, ":type", itp_type_musket),
          (assign, ":test_val", 1),
        (else_try),
          (eq, ":type", itp_type_thrown),
          (neq, ":include_thrown", 0),
          (assign, ":test_val", 1),
        (try_end),
      (try_end),

      (neq, ":test_val", 0),])
]
