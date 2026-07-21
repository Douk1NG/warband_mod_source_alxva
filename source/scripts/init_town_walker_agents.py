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

init_town_walker_agents_scripts = [
# script_init_town_walker_agents
# Input: none
# Output: none
("init_town_walker_agents",
    [(assign, ":num_walkers", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (val_add, ":num_walkers", 1),
       (agent_get_position, pos1, ":cur_agent"),
       (try_for_range, ":i_e_p", 9, 40),#Entry points
         (entry_point_get_position, pos2, ":i_e_p"),
         (get_distance_between_positions, ":distance", pos1, pos2),
         (lt, ":distance", 200),
         (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
       (try_end),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ])
]
