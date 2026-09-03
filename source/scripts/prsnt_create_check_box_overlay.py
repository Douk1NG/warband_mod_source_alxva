# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from ID_meshes import *
from module_constants import *

prsnt_create_check_box_overlay_scripts = [
    ("prsnt_create_check_box_overlay",
    [
        (store_script_param, ":pos_x", 1),
        (store_script_param, ":pos_y", 2),
        (store_script_param, ":size", 3),

        (set_fixed_point_multiplier, 1000),
        (create_check_box_overlay, reg1, "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
        (try_begin),
            (gt, ":size", 0),
            (position_set_x, pos1, ":size"),
            (position_set_y, pos1, ":size"),
            (overlay_set_size, reg1, pos1),
        (try_end),
    ]),
]
