# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

get_prosperity_text_to_s50_scripts = [
#script_update_all_notes
# INPUT: center_no
# OUTPUT: none
("get_prosperity_text_to_s50",
    [(store_script_param, ":center_no", 1),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (val_div, ":prosperity", 20),
     (try_begin),
       (eq, ":prosperity", 0), #0..19
       (str_store_string, s50, "@Very Poor"),
     (else_try),
       (eq, ":prosperity", 1), #20..39
       (str_store_string, s50, "@Poor"),
     (else_try),
       (eq, ":prosperity", 2), #40..59
       (str_store_string, s50, "@Average"),
     (else_try),
       (eq, ":prosperity", 3), #60..79
       (str_store_string, s50, "@Rich"),
     (else_try),
       (str_store_string, s50, "@Very Rich"), #80..99
     (try_end),
     ])
]
