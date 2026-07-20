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

calculate_weekly_party_wage_scripts = [
("calculate_weekly_party_wage",
    [
      (store_script_param_1, ":party_no"),

      (assign, ":result", 0),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
        (call_script, "script_npc_get_troop_wage", ":stack_troop", ":party_no"),
        (assign, ":cur_wage", reg0),
        (val_mul, ":cur_wage", ":stack_size"),
        (val_add, ":result", ":cur_wage"),
      (try_end),
      (assign, reg0, ":result"),
  ])
]
