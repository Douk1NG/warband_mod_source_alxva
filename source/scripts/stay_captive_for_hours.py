# ======================================================================
# SHARED DEPENDENCY
# Entity: stay_captive_for_hours (script)
# Called by menus in 2 domains: captivity, dickplomacy
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

stay_captive_for_hours_scripts = [
("stay_captive_for_hours",
    [
      (store_script_param, ":num_hours", 1),
      (store_current_hours, ":cur_hours"),
      (val_add, ":cur_hours", ":num_hours"),
      (val_max, "$g_check_autos_at_hour", ":cur_hours"),
      (val_add, ":num_hours", 1),
      (rest_for_hours, ":num_hours", 0, 0),
    ])
]
