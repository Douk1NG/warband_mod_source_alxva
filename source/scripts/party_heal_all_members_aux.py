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

party_heal_all_members_aux_scripts = [
("party_heal_all_members_aux",
      [
        (store_script_param_1, ":party_no"),

        (party_get_num_companion_stacks, ":num_stacks",":party_no"),
        (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
          (try_begin),
            (neg|troop_is_hero, ":stack_troop"),
            # (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
            (party_stack_get_num_wounded, ":stack_size",":party_no",":i_stack"),
            (party_add_members, ":party_no", ":stack_troop", ":stack_size"),
            (party_remove_members_wounded_first, ":party_no", ":stack_troop", ":stack_size"),
          (else_try),
            (troop_set_health, ":stack_troop", 100),
          (try_end),
        (try_end),
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_party_heal_all_members_aux", ":attached_party"),
        (try_end),
      ]
    )
]
