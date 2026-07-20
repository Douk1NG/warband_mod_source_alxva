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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_recruit_all_prisoners_to_garrison_scripts = [
# "script_dplmc_recruit_all_prisoners_to_garrison"
#
#INPUT:
#Arg 1: center party
#Arg 2: actually recruit (positive for yes, zero or negative for no)
#OUTPUT:
#reg0: number of prisoners recruited (or would have been recruited if dry run)
("dplmc_recruit_all_prisoners_to_garrison",
   [
    (store_script_param_1, ":center_party"),
    (store_script_param_2, ":actually_recruit"),

    (assign, ":total_recruited", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", ":center_party"),
    (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":troop_no", ":center_party", ":i_stack"),
      (call_script, "script_game_check_prisoner_can_be_sold", ":troop_no"),
      (eq, reg0, 1),
      (party_prisoner_stack_get_size, ":stack_size", ":center_party", ":i_stack"),
      (val_add, ":total_recruited", ":stack_size"),
      (gt, ":actually_recruit", 0),
      (party_remove_prisoners, ":center_party", ":troop_no", ":stack_size"),
      (party_add_members, ":center_party", ":troop_no", ":stack_size"),
    (try_end),
    (assign, reg0, ":total_recruited"),
  ])
]
