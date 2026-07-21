# ======================================================================
# SHARED DEPENDENCY
# Entity: party_remove_all_prisoners (script)
# Called by menus in 2 domains: battle, town
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

party_remove_all_prisoners_scripts = [
("party_remove_all_prisoners",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
  ])
]
