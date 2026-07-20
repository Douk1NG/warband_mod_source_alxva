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

imod_effect_hp_scripts = [
("imod_effect_hp", 
    [
      (store_script_param, ":imod", 1),
      (assign, ":imod_effect", 0),
      (try_begin),
        (eq, ":imod", imod_cracked),
        (assign, ":imod_effect", -56),
      (else_try),
        (eq, ":imod", imod_battered),
        (assign, ":imod_effect", -26),
      (else_try),
        (eq, ":imod", imod_heavy),
        (assign, ":imod_effect", 10),
      (else_try),
        (eq, ":imod", imod_thick),
        (assign, ":imod_effect", 47),
      (else_try),
        (eq, ":imod", imod_reinforced),
        (assign, ":imod_effect", 83),
      (else_try),
        (eq, ":imod", imod_lordly),
        (assign, ":imod_effect", 155),
      (else_try),
        (eq, ":imod", imod_stubborn),
        (assign, ":imod_effect", 5),
      (try_end),
      (assign, reg0, ":imod_effect"),
    ])
]
