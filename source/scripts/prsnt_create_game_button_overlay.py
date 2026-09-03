# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_create_game_button_overlay_scripts = [
    ("prsnt_create_game_button_overlay",
    [
        (store_script_param, ":string", 1),
        (store_script_param, ":pos_x", 2),
        (store_script_param, ":pos_y", 3),

        (set_fixed_point_multiplier, 1000),
        (create_game_button_overlay, reg1, ":string"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
        (overlay_set_text, reg1, ":string"),
    ]),
]
