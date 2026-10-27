# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_prsnt_lines_scripts = [
    ("prsnt_prsnt_lines",
    [
        (store_script_param, ":size_x", 1),
        (store_script_param, ":size_y", 2),
        (store_script_param, ":pos_x", 3),
        (store_script_param, ":pos_y", 4),
        (store_script_param, ":color", 5),

        (val_mul, ":size_x", 50),
        (val_mul, ":size_y", 50),
        (call_script, "script_prsnt_create_mesh_overlay", "mesh_white_plane", ":pos_x", ":pos_y", ":size_x", ":size_y"),
        (overlay_set_color, reg1, ":color"),
    ]),
]
