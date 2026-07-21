# ======================================================================
# SHARED DEPENDENCY
# Entity: cf_training_ground_sub_routine_1_for_melee_details (script)
# Called by menus in 2 domains: dickplomacy, training
# ======================================================================

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

cf_training_ground_sub_routine_1_for_melee_details_scripts = [
#script_cf_training_ground_sub_routine_1_for_melee_details
# INPUT:
# value
#OUTPUT:
# none
("cf_training_ground_sub_routine_1_for_melee_details",
   [
     (store_script_param, ":value", 1),
     (ge, "$temp_3", ":value"),
     (val_add, ":value", 1),
     (troop_get_slot, ":troop_id", "trp_stack_selection_ids", ":value"),
     (str_store_troop_name, s0, ":troop_id"),
     ])
]
