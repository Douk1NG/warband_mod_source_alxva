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

collect_prisoners_from_empty_parties_scripts = [
("collect_prisoners_from_empty_parties",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":collection_party"),

      (party_get_num_companions, ":num_companions", ":party_no"),
      (try_begin),
        (eq, ":num_companions", 0), #party is empty (has no companions). Collect its prisoners.
        (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
          (troop_is_hero, ":stack_troop"),
          (party_add_members, ":collection_party", ":stack_troop", 1),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_collect_prisoners_from_empty_parties", ":attached_party", ":collection_party"),
      (try_end),
  ])
]
