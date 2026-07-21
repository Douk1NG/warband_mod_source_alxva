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

convert_3d_pos_to_map_pos_scripts = [
("convert_3d_pos_to_map_pos",
   [(set_fixed_point_multiplier, 1000),
    (position_transform_position_to_local, pos3, pos2, pos1),
    (position_get_x, ":agent_x_pos", pos3),
    (position_get_y, ":agent_y_pos", pos3),
    (val_div, ":agent_x_pos", "$g_battle_map_scale"),
    (val_div, ":agent_y_pos", "$g_battle_map_scale"),
    (set_fixed_point_multiplier, 1000),
    (store_sub, ":map_x", 980, "$g_battle_map_width"),
    (store_sub, ":map_y", 730, "$g_battle_map_height"),
    (val_add, ":agent_x_pos", ":map_x"),
    (val_add, ":agent_y_pos", ":map_y"),
    (position_set_x, pos0, ":agent_x_pos"),
    (position_set_y, pos0, ":agent_y_pos"),
  ])
]
