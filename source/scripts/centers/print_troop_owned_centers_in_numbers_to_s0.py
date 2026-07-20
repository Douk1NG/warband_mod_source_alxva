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

print_troop_owned_centers_in_numbers_to_s0_scripts = [
#script_party_calculate_regular_strength:
##  # INPUT:
##  # param1: stack_index
##
##  #OUTPUT:
##  # string register 0.
##  ("cf_print_troop_name_with_stack_index_to_s0",
##   [
##     (store_script_param_1, ":stack_index"),
##     (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
##     (lt, ":stack_index", ":num_stacks"),
##     (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_index"),
##     (str_store_troop_name, s0, ":stack_troop"),
##    ]),
#script_print_troop_owned_centers_in_numbers_to_s0
# INPUT:
# param1: troop_no
#OUTPUT:
# string register 0.
("print_troop_owned_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (str_store_string, s0, "@nothing"),
     (assign, ":owned_towns", 0),
     (assign, ":owned_castles", 0),
     (assign, ":owned_villages", 0),
     (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":owned_towns", 1),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":owned_castles", 1),
       (else_try),
         (val_add, ":owned_villages", 1),
       (try_end),
     (try_end),
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
