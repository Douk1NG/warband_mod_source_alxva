# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_prsnt_lines_to_scripts = [
    ("prsnt_prsnt_lines_to",
    [
        (store_script_param, ":pos_x1", 1),
        (store_script_param, ":pos_y1", 2),
        (store_script_param, ":pos_x2", 3),
        (store_script_param, ":pos_y2", 4),
        (store_script_param, ":color", 5),

        (try_begin),
            (eq, ":pos_x1", ":pos_x2"),
            (store_sub, ":size", ":pos_y1", ":pos_y2"),
            (val_abs, ":size"),
            (val_min, ":pos_y1", ":pos_y2"),
            (call_script, "script_prsnt_prsnt_lines", 4, ":size", ":pos_x1", ":pos_y1", ":color"),
        (else_try),
            (eq, ":pos_y1", ":pos_y2"),
            (store_sub, ":size", ":pos_x1", ":pos_x2"),
            (val_abs, ":size"),
            (val_min, ":pos_x1", ":pos_x2"),
            (call_script, "script_prsnt_prsnt_lines", ":size", 5, ":pos_x1", ":pos_y1", ":color"),
        (else_try),
            (call_script, "script_prsnt_prsnt_lines_to", ":pos_x1", ":pos_y1", ":pos_x1", ":pos_y2", ":color"),
            (call_script, "script_prsnt_prsnt_lines_to", ":pos_x1", ":pos_y2", ":pos_x2", ":pos_y2", ":color"),
        (try_end),
    ]),
]
