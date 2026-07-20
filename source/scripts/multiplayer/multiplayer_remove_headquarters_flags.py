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

multiplayer_remove_headquarters_flags_scripts = [
#script_multiplayer_remove_headquarters_flags
# Input: none
# Output: none
("multiplayer_remove_headquarters_flags",
   [
     (store_add, ":end_cond", "spr_headquarters_flag_gray", 1),
     (try_for_range, ":headquarters_flag_no", "spr_headquarters_flag_red", ":end_cond"),
       (replace_scene_props, ":headquarters_flag_no", "spr_empty"),
     (try_end),
     ])
]
