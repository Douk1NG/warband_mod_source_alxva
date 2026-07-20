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

dplmc_time_sorted_heroes_for_center_aux_scripts = [
# For internal use only
# param 1: center no
# param 2: party_no_to_collect_heroes
# param 3: minimum time since last met (inclusive), or negative for no restriction
# param 4: maximum time since last met (exclusive), or negative for no restriction
("dplmc_time_sorted_heroes_for_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (store_script_param, ":min_time", 3),
      (store_script_param, ":max_time", 4),

      (store_current_hours, ":current_hours"),

      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        #get time since last talk
        (troop_get_slot, ":troop_last_talk_time", ":stack_troop", slot_troop_last_talk_time),
        (store_sub, ":time_since_last_talk", ":current_hours", ":troop_last_talk_time"),
        #add if time meets constraints
        (this_or_next|ge, ":time_since_last_talk", ":min_time"),
           (lt, ":min_time", 0),
        (this_or_next|lt, ":time_since_last_talk", ":max_time"),
           (lt, ":max_time", 0),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_dplmc_time_sorted_heroes_for_center_aux", ":attached_party", ":party_no_to_collect_heroes",":min_time",":max_time"),
      (try_end),
  ])
]
