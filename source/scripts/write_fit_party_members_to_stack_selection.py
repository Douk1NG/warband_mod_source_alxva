# ======================================================================
# SHARED DEPENDENCY
# Entity: write_fit_party_members_to_stack_selection (script)
# Called by menus in 2 domains: dickplomacy, training
# ======================================================================

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

write_fit_party_members_to_stack_selection_scripts = [
("write_fit_party_members_to_stack_selection",
   [
     (store_script_param, ":party_no", 1),
     (store_script_param, ":exclude_leader", 2),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":slot_index", 2),
     (assign, ":total_fit", 0),
     (try_for_range, ":stack_index", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_index"),
       (assign, ":num_fit", 0),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (try_begin),
           (neg|troop_is_wounded, ":stack_troop"),
           (this_or_next|eq, ":exclude_leader", 0),
           (neq, ":stack_index", 0),
           (assign, ":num_fit",1),
         (try_end),
       (else_try),
         (party_stack_get_size, ":num_fit", ":party_no", ":stack_index"),
         (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_index"),
         (val_sub, ":num_fit", ":num_wounded"),
       (try_end),
       (try_begin),
         (gt, ":num_fit", 0),
         (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":num_fit"),
         (troop_set_slot, "trp_stack_selection_ids", ":slot_index", ":stack_troop"),
         (val_add, ":slot_index", 1),
       (try_end),
       (val_add, ":total_fit", ":num_fit"),
     (try_end),
     (val_sub, ":slot_index", 2),
     (troop_set_slot, "trp_stack_selection_amounts", 0, ":slot_index"),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_fit"),
    ])
]
