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

game_get_scene_name_scripts = [
#script_game_get_scene_name
# This script is called from the game engine when a name for the scene is needed.
# INPUT: arg1 = scene_no
# OUTPUT: s0 = name
("game_get_scene_name",
    [
      (store_script_param, ":scene_no", 1),
      (try_begin),
        (is_between, ":scene_no", multiplayer_scenes_begin, multiplayer_scenes_end),
        (store_sub, ":string_id", ":scene_no", multiplayer_scenes_begin),
        (val_add, ":string_id", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_id"),
      (try_end),
     ])
]
