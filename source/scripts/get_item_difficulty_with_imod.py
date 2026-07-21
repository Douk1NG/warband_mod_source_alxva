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

get_item_difficulty_with_imod_scripts = [
("get_item_difficulty_with_imod",
    [
      (store_script_param, ":item", 1),
      (store_script_param, ":imod", 2),

      (item_get_type, ":type", ":item"),
      (item_get_difficulty, ":difficulty", ":item"),
      (try_begin),
        (eq, ":difficulty", 0),
      (else_try),
        (eq, ":type", itp_type_horse),
        (try_begin), 
          (eq, ":imod", imod_stubborn),
          (val_add, ":difficulty", 1),
        (else_try),
          (eq, ":imod", imod_champion),
          (val_add, ":difficulty", 2),
        (else_try),
          (eq, ":imod", imod_timid),
          (val_sub, ":difficulty", 1),
        (try_end),
      (else_try),
        (this_or_next|is_between, ":type", itp_type_one_handed_wpn, itp_type_goods),
        (is_between, ":type", itp_type_head_armor, itp_type_animal),
        (try_begin),
          (eq, ":imod", imod_heavy),
          (val_add, ":difficulty", 1),
        (else_try),
          (eq, ":imod", imod_strong),
          (val_add, ":difficulty", 2),
        (else_try),
          (eq, ":imod", imod_masterwork),
          (val_add, ":difficulty", 4),
        (try_end),
      (try_end),
      (assign, reg0, ":difficulty"),
    ])
]
