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

get_troop_relation_to_player_string_scripts = [
("get_troop_relation_to_player_string",
     [
         (store_script_param, ":target_string", 1),
         (store_script_param, ":troop_no", 2),

         (call_script, "script_troop_get_player_relation", ":troop_no"),
         (assign, ":relation", reg0),
         (str_clear, s61),

         (store_add, ":normalized_relation", ":relation", 100),
         (val_add, ":normalized_relation", 5),
         (store_div, ":str_offset", ":normalized_relation", 10),
         (val_clamp, ":str_offset", 0, 20),
         (store_add, ":str_rel_id", "str_relation_mnus_100_ns",  ":str_offset"),

         ## Make something if troop has relation but not strong enought to warrant a string
         (try_begin),
           (neq, ":str_rel_id", "str_relation_plus_0_ns"),
           (str_store_string, s61, ":str_rel_id"),
         (else_try),
           (neg|eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ knows of you."),
         (else_try),
           (eq, reg0, 0),
           (str_is_empty, s61),
           (str_store_string, s61, "@ has no opinion about you."),
         (try_end),

         ## copy result string to target string
         (str_store_string_reg, ":target_string", s61),
     ])
]
