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

calculate_team_powers_scripts = [
("calculate_team_powers",
     [
       (store_script_param, ":agent_no", 1),

       (try_begin),
         (assign, ":agent_side", 0),
         (agent_is_ally, ":agent_no"),
         (assign, ":agent_side", 1),
       (try_end),

       (assign, ":ally_power", 0),
       (assign, ":enemy_power", 0),

       (try_for_agents, ":cur_agent"),
         (agent_is_human, ":cur_agent"),
         (agent_is_alive, ":cur_agent"),

         (try_begin),
           (assign, ":agent_side_cur", 0),
           (agent_is_ally, ":cur_agent"),
           (assign, ":agent_side_cur", 1),
         (try_end),

         (try_begin),
           (agent_get_horse, ":agent_horse_id", ":cur_agent"),
           (neq, ":agent_horse_id", -1),
           (assign, ":agent_power", 2), #if this agent is horseman then his power effect is 2
         (else_try),
           (assign, ":agent_power", 1), #if this agent is walker then his power effect is 1
         (try_end),

         (try_begin),
           (eq, ":agent_side", ":agent_side_cur"),
           (val_add, ":ally_power", ":agent_power"),
         (else_try),
           (val_add, ":enemy_power", ":agent_power"),
         (try_end),
       (try_end),

       (assign, reg0, ":ally_power"),
       (assign, reg1, ":enemy_power"),
  ])
]
