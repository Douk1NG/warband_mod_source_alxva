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

cf_party_remove_random_regular_troop_scripts = [
("cf_party_remove_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (party_remove_members, ":party_no", ":stack_troop", 1),
       (assign, reg0, ":stack_troop"),
     (try_end),
     ])
]
