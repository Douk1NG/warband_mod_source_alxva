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

prsnt_line_scripts = [
("prsnt_line",
    [
      (store_script_param, ":size_x", 1),
      (store_script_param, ":size_y", 2),
      (store_script_param, ":pos_x", 3),
      (store_script_param, ":pos_y", 4),
      (store_script_param, ":color", 5),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (val_mul, ":size_x", 50),
      (val_mul, ":size_y", 50),
      (position_set_x, pos0, ":size_x"),
      (position_set_y, pos0, ":size_y"),
      (overlay_set_size, reg1, pos0),
      (position_set_x, pos0, ":pos_x"),
      (position_set_y, pos0, ":pos_y"),
      (overlay_set_position, reg1, pos0),
      (overlay_set_color, reg1, ":color"),
  ])
]
