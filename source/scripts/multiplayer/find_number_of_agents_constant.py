# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

find_number_of_agents_constant_scripts = [
("find_number_of_agents_constant",
   [
     (assign, ":num_dead_or_alive_agents", 0),

     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (val_add, ":num_dead_or_alive_agents", 1),
     (try_end),

     (try_begin),
       (le, ":num_dead_or_alive_agents", 2), #2
       (assign, reg0, 100),
     (else_try),
       (le, ":num_dead_or_alive_agents", 4), #2+2
       (assign, reg0, 140),
     (else_try),
       (le, ":num_dead_or_alive_agents", 7), #2+2+3
       (assign, reg0, 180),
     (else_try),
       (le, ":num_dead_or_alive_agents", 11), #2+2+3+4
       (assign, reg0, 220),
     (else_try),
       (le, ":num_dead_or_alive_agents", 17), #2+2+3+4+6
       (assign, reg0, 260),
     (else_try),
       (le, ":num_dead_or_alive_agents", 25), #2+2+3+4+6+8
       (assign, reg0, 300),
     (else_try),
       (le, ":num_dead_or_alive_agents", 36), #2+2+3+4+6+8+11
       (assign, reg0, 340),
     (else_try),
       (le, ":num_dead_or_alive_agents", 50), #2+2+3+4+6+8+11+14
       (assign, reg0, 380),
     (else_try),
       (le, ":num_dead_or_alive_agents", 68), #2+2+3+4+6+8+11+14+18
       (assign, reg0, 420),
     (else_try),
       (le, ":num_dead_or_alive_agents", 91), #2+2+3+4+6+8+11+14+18+23
       (assign, reg0, 460),
     (else_try),
       (assign, reg0, 500),
     (try_end),
     ])
]
