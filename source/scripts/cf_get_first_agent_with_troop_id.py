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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

cf_get_first_agent_with_troop_id_scripts = [
("cf_get_first_agent_with_troop_id",
    [
      (store_script_param_1, ":troop_no"),
      #      (store_script_param_2, ":agent_no_to_begin_searching_after"),
      (assign, ":result", -1),
      (try_for_agents, ":cur_agent"),
        (eq, ":result", -1),
        ##        (try_begin),
        ##          (eq, ":cur_agent", ":agent_no_to_begin_searching_after"),
        ##          (assign, ":agent_no_to_begin_searching_after", -1),
        ##        (try_end),
        ##        (eq, ":agent_no_to_begin_searching_after", -1),
        (agent_get_troop_id, ":cur_troop_no", ":cur_agent"),
        (eq, ":cur_troop_no", ":troop_no"),
        (assign, ":result", ":cur_agent"),
      (try_end),
      (assign, reg0, ":result"),
      (neq, reg0, -1),
  ])
]
