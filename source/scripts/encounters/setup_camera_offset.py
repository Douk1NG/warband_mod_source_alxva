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

setup_camera_offset_scripts = [
("setup_camera_offset",
      [
      (assign, "$g_camera_z", 200),
      (assign, "$g_camera_y", -175),
      (assign, "$g_camera_rotate_x", 0),
      (assign, "$g_camera_rotate_y", 0),
      (assign, "$g_camera_rotate_z", 0),

      ])
]
