# ======================================================================
# SHARED DEPENDENCY
# Entity: describe_center_relation_to_s3 (script)
# Called by menus in 2 domains: town, village
# ======================================================================

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

describe_center_relation_to_s3_scripts = [
# Input: arg1 = relation (-100 .. 100)
# Output: none
("describe_center_relation_to_s3",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      (str_store_string, s3, ":str_id"),
  ])
]
