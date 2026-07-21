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

remove_fit_party_member_from_stack_selection_scripts = [
("remove_fit_party_member_from_stack_selection",
   [
     (store_script_param, ":slot_index", 1),
     (val_add, ":slot_index", 2),
     (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":slot_index"),
     (troop_get_slot, ":troop_no", "trp_stack_selection_ids", ":slot_index"),
     (val_sub, ":amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":amount"),
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (val_sub, ":total_amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_amount"),
     (try_begin),
       (le, ":amount", 0),
       (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
       (store_add, ":end_cond", ":num_slots", 2),
       (store_add, ":begin_cond", ":slot_index", 1),
       (try_for_range, ":index", ":begin_cond", ":end_cond"),
         (store_sub, ":prev_index", ":index", 1),
         (troop_get_slot, ":value", "trp_stack_selection_amounts", ":index"),
         (troop_set_slot, "trp_stack_selection_amounts", ":prev_index", ":value"),
         (troop_get_slot, ":value", "trp_stack_selection_ids", ":index"),
         (troop_set_slot, "trp_stack_selection_ids", ":prev_index", ":value"),
       (try_end),
       (val_sub, ":num_slots", 1),
       (troop_set_slot, "trp_stack_selection_amounts", 0, ":num_slots"),
     (try_end),
     (assign, reg0, ":troop_no"),
    ])
]
