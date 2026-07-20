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

multiplayer_remove_destroy_mod_targets_scripts = [
#script_multiplayer_remove_destroy_mod_targets
# Input: none
# Output: none
("multiplayer_remove_destroy_mod_targets",
   [
       (replace_scene_props, "spr_catapult_destructible", "spr_empty"),
       (replace_scene_props, "spr_trebuchet_destructible", "spr_empty"),
     ])
]
