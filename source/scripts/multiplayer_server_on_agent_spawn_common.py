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

multiplayer_server_on_agent_spawn_common_scripts = [
#script_game_enable_cheat_menu
# INPUT: arg1 = agent_no
# OUTPUT: none
("multiplayer_server_on_agent_spawn_common",
   [
     (store_script_param, ":agent_no", 1),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, -1),
     (try_begin),
       (agent_is_non_player, ":agent_no"),
       (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
     (try_end),
     ])
]
