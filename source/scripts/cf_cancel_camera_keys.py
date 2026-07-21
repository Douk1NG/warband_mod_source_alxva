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

cf_cancel_camera_keys_scripts = [
("cf_cancel_camera_keys", [
      (this_or_next|game_key_is_down, gk_view_char),
      (this_or_next|game_key_is_down, gk_zoom),
      (game_key_is_down, gk_cam_toggle),
      (mission_cam_set_mode, 0),
    ])
]
