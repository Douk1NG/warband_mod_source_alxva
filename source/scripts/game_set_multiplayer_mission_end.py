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

game_set_multiplayer_mission_end_scripts = [
# This script is called from the game engine when a multiplayer map is ended in clients (not in server).
# INPUT:
# none
# OUTPUT:
# none
("game_set_multiplayer_mission_end",
    [
      (assign, "$g_multiplayer_mission_end_screen", 1),
  ])
]
