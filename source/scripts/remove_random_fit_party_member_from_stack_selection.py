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

remove_random_fit_party_member_from_stack_selection_scripts = [
("remove_random_fit_party_member_from_stack_selection",
   [
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (store_random_in_range, ":random_troop", 0, ":total_amount"),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (store_add, ":end_cond", ":num_slots", 2),
     (try_for_range, ":index", 2, ":end_cond"),
       (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":index"),
       (val_sub, ":random_troop", ":amount"),
       (lt, ":random_troop", 0),
       (assign, ":end_cond", 0),
       (store_sub, ":slot_index", ":index", 2),
     (try_end),
     (call_script, "script_remove_fit_party_member_from_stack_selection", ":slot_index"),
    ])
]
