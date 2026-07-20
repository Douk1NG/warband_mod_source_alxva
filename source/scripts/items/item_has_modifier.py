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

item_has_modifier_scripts = [
("item_has_modifier",
    [
      (store_script_param, ":item", 1),
      (store_script_param, ":imod", 2),

      (assign, ":has", 0),
      (try_begin),
        (item_has_modifier, ":item", ":imod"),
        (assign, ":has", 1),
      (else_try),
        ## horse-only modifiers: valid only for actual horses, not by item-id range
        (item_get_type, ":type", ":item"),
        (eq, ":type", itp_type_horse),
        (this_or_next|eq, ":imod", imod_stubborn),
        (this_or_next|eq, ":imod", imod_spirited),
        (eq, ":imod", imod_champion),
        (assign, ":has", 1),
      (try_end),

      (assign, reg0, ":has"),
    ])
]
