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

custom_battle_end_scripts = [
# script_calculate_renown_value
# Input: none
# Output: none
("custom_battle_end",
    [
      (assign, "$g_custom_battle_team1_death_count", 0),
      (assign, "$g_custom_battle_team2_death_count", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_alive, ":cur_agent"),
        (agent_get_team, ":cur_team", ":cur_agent"),
        (try_begin),
          (eq, ":cur_team", ":player_team"),
          (val_add, "$g_custom_battle_team1_death_count", 1),
        (else_try),
          (val_add, "$g_custom_battle_team2_death_count", 1),
        (try_end),
      (try_end),
      ])
]
