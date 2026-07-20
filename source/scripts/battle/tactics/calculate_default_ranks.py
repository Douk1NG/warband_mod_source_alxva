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

calculate_default_ranks_scripts = [
("calculate_default_ranks", [
      (store_script_param, ":bg_size", 1),

      (val_mul, ":bg_size", 20),
      (val_sub, ":bg_size", 25),
      (convert_to_fixed_point, ":bg_size"),
      (store_sqrt, reg1, ":bg_size"),
      (convert_from_fixed_point, reg1),
      (val_sub, reg1, 5),
      (val_div, reg1, 10),
      (val_add, reg1, 1),])
]
