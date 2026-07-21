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

multiplayer_count_players_bots_scripts = [
# script_multiplayer_count_players_bots
# Input: none
# Output: none
("multiplayer_count_players_bots",
    [
      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (player_is_active, ":cur_player"),
        (player_set_slot, ":cur_player", slot_player_last_bot_count, 0),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_get_player_id, ":agent_player", ":cur_agent"),
        (lt, ":agent_player", 0), #not a player
        (agent_get_group, ":agent_group", ":cur_agent"),
        (player_is_active, ":agent_group"),
        (player_get_slot, ":bot_count", ":agent_group", slot_player_last_bot_count),
        (val_add, ":bot_count", 1),
        (player_set_slot, ":agent_group", slot_player_last_bot_count, ":bot_count"),
      (try_end),
      ])
]
