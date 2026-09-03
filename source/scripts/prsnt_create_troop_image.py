# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from header_troops import *
from ID_troops import *
from module_constants import *

prsnt_create_troop_image_scripts = [
    ("prsnt_create_troop_image",
    [
        (store_script_param, ":troop_no", 1),
        (store_script_param, ":pos_x", 2),
        (store_script_param, ":pos_y", 3),
        (store_script_param, ":size", 4),

        (set_fixed_point_multiplier, 1000),
        (store_mul, ":cur_troop", ":troop_no", 2),
        (create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
        (position_set_x, pos2, ":pos_x"),
        (position_set_y, pos2, ":pos_y"),
        (overlay_set_position, reg1, pos2),
        (position_set_x, pos3, ":size"),
        (position_set_y, pos3, ":size"),
        (overlay_set_size, reg1, pos3),
    ]),
]
