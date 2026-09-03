# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_create_number_box_overlay_scripts = [
    ("prsnt_create_number_box_overlay",
    [
        (store_script_param, ":pos_x", 1),
        (store_script_param, ":pos_y", 2),
        (store_script_param, ":min_value", 3),
        (store_script_param, ":max_value", 4),

        (set_fixed_point_multiplier, 1000),
        (create_number_box_overlay, reg1, ":min_value", ":max_value"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
    ]),
]
