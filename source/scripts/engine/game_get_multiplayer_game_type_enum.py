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

game_get_multiplayer_game_type_enum_scripts = [
# script_game_get_multiplayer_game_type_enum
# Input: none
# Output: reg0:first type, reg1:type count
("game_get_multiplayer_game_type_enum",
   [
     (assign, reg0, multiplayer_game_type_deathmatch),
	 (assign, reg1, multiplayer_num_game_types),
	 ])
]
