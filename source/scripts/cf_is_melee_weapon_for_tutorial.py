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

cf_is_melee_weapon_for_tutorial_scripts = [
("cf_is_melee_weapon_for_tutorial",
    [
      (store_script_param, ":item_no", 1),
      (assign, ":result", 0),
      (try_begin),
        (this_or_next|eq, ":item_no", "itm_quarter_staff"),
        (eq, ":item_no", "itm_practice_sword"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
     ])
]
