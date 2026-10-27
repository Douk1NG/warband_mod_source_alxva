# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from module_constants import *

prsnt_create_scrollable_container_scripts = [
    ("prsnt_create_scrollable_container",
    [
        (store_script_param, ":pos_x", 1),
        (store_script_param, ":pos_y", 2),
        (store_script_param, ":size_x", 3),
        (store_script_param, ":size_y", 4),

        (str_clear, s0),
        (call_script, "script_prsnt_create_text_overlay", "str_s0", ":pos_x", ":pos_y", 1000, ":size_x", ":size_y", tf_scrollable),
    ]),
]
