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

dplmc_print_centers_in_numbers_to_s0_scripts = [
# script_dplmc_get_faction_truce_length_with_faction
#
#similar to script_print_troop_owned_centers_in_numbers_to_s0
#
#INPUT:
#  arg1: owned_towns
#  arg2: owned_castles
#  arg3: owned_villages
#
#OUTPUT:
#  reg0: owned_towns + owned_castles + owned_villages
#    s0: a string describing the numbers of centers
("dplmc_print_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":owned_towns"),
	 (store_script_param_2, ":owned_castles"),
	 (store_script_param, ":owned_villages", 3),
     (str_store_string, s0, "@nothing"),

     (assign, ":num_types", 0),
     (try_begin),
       (gt, ":owned_villages", 0),
       (assign, reg0, ":owned_villages"),
       (store_sub, reg1, reg0, 1),
       (str_store_string, s0, "@{reg0} village{reg1?s:}"),
       (val_add, ":num_types", 1),
     (try_end),

     (try_begin),
       (gt, ":owned_castles", 0),
       (assign, reg0, ":owned_castles"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} castle{reg1?s:}"),
       (else_try),
         (str_store_string, s0, "@{reg0} castle{reg1?s:} and {s0}"),
       (try_end),
       (val_add, ":num_types", 1),
     (try_end),

     (try_begin),
       (gt, ":owned_towns", 0),
       (assign, reg0, ":owned_towns"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} town{reg1?s:}"),
       (else_try),
         (eq, ":num_types", 1),
         (str_store_string, s0, "@{reg0} town{reg1?s:} and {s0}"),
       (else_try),
         (str_store_string, s0, "@{reg0} town{reg1?s:}, {s0}"),
       (try_end),
     (try_end),

     (store_add, reg0, ":owned_villages", ":owned_castles"),
     (val_add, reg0, ":owned_towns"),
     ])
]
