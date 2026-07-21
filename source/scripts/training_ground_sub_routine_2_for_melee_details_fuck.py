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

training_ground_sub_routine_2_for_melee_details_fuck_scripts = [
#script_print_party_to_s0:
# INPUT:
# value
#OUTPUT:
# none
("training_ground_sub_routine_2_for_melee_details_fuck",
   [
     (store_script_param, ":value", 1),
     (val_sub, ":value", 1),
     (try_begin),
       (eq, ":value", -3),
	   (assign, reg0, -1),
     (else_try),
       (eq, ":value", -2),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
     (else_try),
       (call_script, "script_remove_fit_party_member_from_stack_selection", ":value"),
     (try_end),
     (assign, ":troop_id", reg0),
     (store_sub, ":slot_index", "$temp_2", 1),
     (troop_set_slot, "trp_temp_array_a", ":slot_index", ":troop_id"),
     (troop_set_slot, "trp_temp_array_b", ":slot_index", -1),
     (try_begin),
       (eq, "$temp", "$temp_2"),
       (call_script, "script_start_fucking", "$temp", "$g_training_ground_melee_training_scene"),
     (else_try),
       (val_add, "$temp_2", 1),
       (jump_to_menu, "mnu_fuck_3"),
     (try_end),
     ])
]
