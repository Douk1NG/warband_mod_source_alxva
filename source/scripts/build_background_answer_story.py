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

build_background_answer_story_scripts = [
("build_background_answer_story", [
        (store_script_param_1, ":sreg"),
        (assign, reg11, "$character_gender"),
        (store_sub, ":string", "$background_answer_4", cb4_revenge),
        (val_add, ":string", "str_story_reason_revenge"),
        (str_store_string, s13, ":string"),
        (store_sub, ":string", "$background_answer_3", dplmc_cb3_bravo),
        (val_add, ":string", "str_story_job_bravo"),
        (str_store_string, s12, ":string"),
        (store_sub, ":string", "$background_answer_2", cb2_page), #values for this start from 0
        (val_add, ":string", "str_story_childhood_page"),
        (str_store_string, s11, ":string"),
        (store_sub, ":string", "$background_type", cb_noble),
        (val_add, ":string", "str_story_parent_noble"),
        (str_store_string, s10, ":string"),
        (str_store_string, ":sreg", "str_story_all"),
    ])
]
