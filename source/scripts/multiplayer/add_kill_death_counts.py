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

add_kill_death_counts_scripts = [
("add_kill_death_counts",
   [
      (store_script_param, ":killer_agent_no", 1),
      (store_script_param, ":dead_agent_no", 2),

      (try_begin),
        (ge, ":killer_agent_no", 0),
        (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
      (else_try),
        (assign, ":killer_agent_team", -1),
      (try_end),

      (try_begin),
        (ge, ":dead_agent_no", 0),
        (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
      (else_try),
        (assign, ":dead_agent_team", -1),
      (try_end),

      #adjusting kill counts of players/bots
      (try_begin),
        (try_begin),
          (ge, ":killer_agent_no", 0),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":killer_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (neq, ":killer_agent_no", ":dead_agent_no"),

          (this_or_next|neq, ":killer_agent_team", ":dead_agent_team"),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),

          (agent_get_player_id, ":killer_agent_player", ":killer_agent_no"),
          (try_begin),
            (agent_is_non_player, ":killer_agent_no"), #if killer agent is bot then increase bot kill counts of killer agent's team by one.
            (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
            (team_get_bot_kill_count, ":killer_agent_team_bot_kill_count", ":killer_agent_team"),
            (val_add, ":killer_agent_team_bot_kill_count", 1),
            (team_set_bot_kill_count, ":killer_agent_team", ":killer_agent_team_bot_kill_count"),
          (else_try), #if killer agent is not bot then increase kill counts of killer agent's player by one.
            (player_is_active, ":killer_agent_player"),
            (player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player"),
            (val_add, ":killer_agent_player_kill_count", 1),
            (player_set_kill_count, ":killer_agent_player", ":killer_agent_player_kill_count"),
          (try_end),
        (try_end),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (try_begin),
            (agent_is_non_player, ":dead_agent_no"), #if dead agent is bot then increase bot kill counts of dead agent's team by one.
            (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
            (team_get_bot_death_count, ":dead_agent_team_bot_death_count", ":dead_agent_team"),
            (val_add, ":dead_agent_team_bot_death_count", 1),
            (team_set_bot_death_count, ":dead_agent_team", ":dead_agent_team_bot_death_count"),
          (else_try), #if dead agent is not bot then increase death counts of dead agent's player by one.
            (agent_get_player_id, ":dead_agent_player", ":dead_agent_no"),
            (player_is_active, ":dead_agent_player"),
            (player_get_death_count, ":dead_agent_player_death_count", ":dead_agent_player"),
            (val_add, ":dead_agent_player_death_count", 1),
            (player_set_death_count, ":dead_agent_player", ":dead_agent_player_death_count"),
          (try_end),

          (try_begin),
            (assign, ":continue", 0),

            (try_begin),
              (this_or_next|lt, ":killer_agent_no", 0), #if he killed himself (1a(team change) or 1b(self kill)) then decrease kill counts of killer player by one.
              (eq, ":killer_agent_no", ":dead_agent_no"),
              (assign, ":continue", 1),
            (try_end),

            (try_begin),
              (eq, ":killer_agent_team", ":dead_agent_team"), #if he killed a teammate and game mod is not deathmatch then decrease kill counts of killer player by one.
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
              (assign, ":continue", 1),
            (try_end),

            (eq, ":continue", 1),

            (try_begin),
              (ge, ":killer_agent_no", 0),
              (assign, ":responsible_agent", ":killer_agent_no"),
            (else_try),
              (assign, ":responsible_agent", ":dead_agent_no"),
            (try_end),

            (try_begin),
              (ge, ":responsible_agent", 0),
              (neg|agent_is_non_player, ":responsible_agent"),
              (agent_get_player_id, ":responsible_player", ":responsible_agent"),
              (ge, ":responsible_player", 0),
              (player_get_kill_count, ":dead_agent_player_kill_count", ":responsible_player"),
              (val_add, ":dead_agent_player_kill_count", -1),
              (player_set_kill_count, ":responsible_player", ":dead_agent_player_kill_count"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
    ])
]
