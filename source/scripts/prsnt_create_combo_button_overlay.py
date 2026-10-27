# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_create_combo_button_overlay_scripts = [
    ("prsnt_create_combo_button_overlay",
    [
        (store_script_param, ":pos_x", 1),
        (store_script_param, ":pos_y", 2),

        (set_fixed_point_multiplier, 1000),
        (create_combo_button_overlay, reg1),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
    ]),
]
