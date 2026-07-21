# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

imod_effect_speed_scripts = [
("imod_effect_speed", 
    [
      (store_script_param, ":imod", 1),
      (assign, ":imod_effect", 0),
      (try_begin),
        (eq, ":imod", imod_bent),
        (assign, ":imod_effect", -3),
      (else_try),
        (eq, ":imod", imod_balanced),
        (assign, ":imod_effect", 3),
      (else_try),
        (eq, ":imod", imod_masterwork),
        (assign, ":imod_effect", 1),
      (else_try),
        (eq, ":imod", imod_heavy),
        (assign, ":imod_effect", -2),
      (else_try),
        (eq, ":imod", imod_strong),
        (assign, ":imod_effect", -3),
      (try_end),
      (assign, reg0, ":imod_effect"),
    ])
]
