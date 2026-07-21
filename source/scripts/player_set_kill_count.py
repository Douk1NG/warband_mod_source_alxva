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

player_set_kill_count_scripts = [
("player_set_kill_count",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),

     (player_set_kill_count, ":player_no", ":score"),
   ])
]
