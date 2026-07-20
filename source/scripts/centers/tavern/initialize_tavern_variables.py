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

initialize_tavern_variables_scripts = [
(
   "initialize_tavern_variables",
   [
     (assign, "$g_main_attacker_agent", 0),
     (assign, "$g_attacker_drawn_weapon", 0),
     (assign, "$g_start_belligerent_drunk_fight", 0),
     (assign, "$g_start_hired_assassin_fight", 0),
     (assign, "$g_belligerent_drunk_leaving", 0),
   ])
]
