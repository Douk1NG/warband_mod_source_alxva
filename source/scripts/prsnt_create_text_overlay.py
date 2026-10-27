# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_create_text_overlay_scripts = [
    ("prsnt_create_text_overlay",
    [
        (store_script_param, ":string", 1),
        (store_script_param, ":pos_x", 2),
        (store_script_param, ":pos_y", 3),
        (store_script_param, ":text_size", 4),
        (store_script_param, ":size_x", 5),
        (store_script_param, ":size_y", 6),
        (store_script_param, ":flags", 7),

        (set_fixed_point_multiplier, 1000),
        (create_text_overlay, reg1, ":string", ":flags"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, ":text_size"),
        (position_set_y, pos1, ":text_size"),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, ":size_x"),
        (position_set_y, pos1, ":size_y"),
        (overlay_set_area_size, reg1, pos1),
        (overlay_set_text, reg1, ":string"),
    ]),
]
