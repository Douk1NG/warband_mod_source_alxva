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

get_stack_with_rank_scripts = [
("get_stack_with_rank",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg(0), -1),
      (assign, ":num_total", 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (eq, reg(0), -1), #continue only if we haven't found the result yet.
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded,  ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, ":num_total", ":stack_size"),
        (try_begin),
          (lt, ":rank", ":num_total"),
          (assign, reg(0), ":i_stack"),
        (try_end),
      (try_end),
  ])
]
