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

cf_has_companion_emissary_scripts = [
#script_build_background_answer_story
("cf_has_companion_emissary",
    [
    (assign, ":companion_found", companions_end),
    (try_for_range, ":emissary", companions_begin, companions_end),
      (main_party_has_troop, ":emissary"),
      (assign, ":companion_found", companions_begin),
    (try_end),
    (neq, ":companion_found", companions_end),
    ])
]
