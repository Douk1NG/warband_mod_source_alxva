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

get_heroes_attached_to_center_aux_scripts = [
##  # script_get_closest_town_of_faction
# For internal use only
("get_heroes_attached_to_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ])
]
