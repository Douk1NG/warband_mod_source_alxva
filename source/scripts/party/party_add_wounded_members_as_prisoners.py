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

party_add_wounded_members_as_prisoners_scripts = [
("party_add_wounded_members_as_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (ge, ":num_wounded", 1),
        (party_stack_get_troop_id, ":stack_troop", ":source_party", ":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        #(party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ])
]
