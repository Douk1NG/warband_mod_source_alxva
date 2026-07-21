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

cf_troop_agent_is_alive_scripts = [
("cf_troop_agent_is_alive",
    [(store_script_param, ":troop_no", 1),
     (assign, ":alive_count", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
       (eq, ":troop_no", ":cur_agent_troop"),
       (agent_is_alive, ":cur_agent"),
       (val_add, ":alive_count", 1),
     (try_end),
     (gt, ":alive_count", 0),
     ])
]
