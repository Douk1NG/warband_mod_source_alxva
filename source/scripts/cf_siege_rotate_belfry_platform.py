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

cf_siege_rotate_belfry_platform_scripts = [
("cf_siege_rotate_belfry_platform",
   [(eq, "$belfry_positioned", 1),
    (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
    (prop_instance_get_position, pos1, ":belfry_object"),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
    (assign, "$belfry_positioned", 2),
  ])
]
