# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *

prsnt_get_grid_position_scripts = [
    ("prsnt_get_grid_position",
    [
        (store_script_param, ":index", 1),
        (store_script_param, ":num_items", 2),
        (store_script_param, ":num_cols", 3),
        (store_script_param, ":col_width", 4),
        (store_script_param, ":col_height", 5),

        (store_mod, ":x", ":index", ":num_cols"),
        (store_mul, ":pos_x", ":x", ":col_width"),

        (store_sub, ":row", ":index", ":x"),
        (val_div, ":row", ":num_cols"),
        (val_sub, ":num_items", 1),
        (store_div, ":num_rows", ":num_items", ":num_cols"),
        (val_add, ":num_rows", 1),
        (store_sub, ":pos_y", ":num_rows", ":row"),
        (val_sub, ":pos_y", 1),
        (val_mul, ":pos_y", ":col_height"),

        (assign, reg0, ":pos_x"),
        (assign, reg1, ":pos_y"),
    ]),
]
