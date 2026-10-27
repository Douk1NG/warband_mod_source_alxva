# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from ID_meshes import *
from module_constants import *

prsnt_create_mesh_overlay_scripts = [
    ("prsnt_create_mesh_overlay",
    [
        (store_script_param, ":mesh", 1),
        (store_script_param, ":pos_x", 2),
        (store_script_param, ":pos_y", 3),
        (store_script_param, ":size_x", 4),
        (store_script_param, ":size_y", 5),

        (set_fixed_point_multiplier, 1000),
        (create_mesh_overlay, reg1, ":mesh"),
        (position_set_x, pos2, ":pos_x"),
        (position_set_y, pos2, ":pos_y"),
        (overlay_set_position, reg1, pos2),
        (position_set_x, pos3, ":size_x"),
        (position_set_y, pos3, ":size_y"),
        (overlay_set_size, reg1, pos3),
    ]),
]
