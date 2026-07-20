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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_on_disembark_scripts = [
#script_game_on_disembark:
# This script is called from the game engine when the player reaches the shore with a ship.
# INPUT: pos0 = disembark position
# OUTPUT: none
("game_on_disembark",
   [(jump_to_menu, "mnu_disembark"),
  ])
]
