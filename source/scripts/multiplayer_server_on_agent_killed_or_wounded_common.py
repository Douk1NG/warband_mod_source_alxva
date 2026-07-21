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

multiplayer_server_on_agent_killed_or_wounded_common_scripts = [
#script_multiplayer_server_on_agent_killed_or_wounded_common
# INPUT: arg1 = dead_agent_no, arg2 = killer_agent_no
# OUTPUT: none
("multiplayer_server_on_agent_killed_or_wounded_common",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),

     (call_script, "script_multiplayer_event_agent_killed_or_wounded", ":dead_agent_no", ":killer_agent_no"),
     #adding 1 score points to agent which kills enemy agent at server
     (try_begin),
       (multiplayer_is_server),
       (try_begin), #killing myself because of some reason (friend hit, fall, team change)
         (lt, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (neg|agent_is_non_player, ":dead_agent_no"),
         (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
         (player_is_active, ":dead_agent_player_id"),
         (player_get_score, ":dead_agent_player_score", ":dead_agent_player_id"),
         (val_add, ":dead_agent_player_score", -1),
         (player_set_score, ":dead_agent_player_id", ":dead_agent_player_score"),
       (else_try), #killing teammate
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_get_team, ":killer_team_no", ":killer_agent_no"),
         (agent_get_team, ":dead_team_no", ":dead_agent_no"),
         (eq, ":killer_team_no", ":dead_team_no"),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (val_add, ":killer_agent_player_score", -1),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
         #(player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player_id"),
         #(val_add, ":killer_agent_player_kill_count", -2),
         #(player_set_kill_count, ":killer_agent_player_id", ":killer_agent_player_kill_count"),
       (else_try), #killing enemy
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_human, ":killer_agent_no"),
         (try_begin),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (try_begin),
             (eq, "$g_battle_death_mode_started", 1),
             (neq, ":dead_agent_no", ":killer_agent_no"),
             (call_script, "script_calculate_new_death_waiting_time_at_death_mod"),
           (try_end),
         (try_end),
         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
           (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
           (try_begin),
             (ge, ":dead_player_no", 0),
             (player_is_active, ":dead_player_no"),
             (neg|agent_is_non_player, ":dead_agent_no"),
             (try_for_agents, ":cur_agent"),
               (agent_is_non_player, ":cur_agent"),
               (agent_is_human, ":cur_agent"),
               (agent_is_alive, ":cur_agent"),
               (agent_get_group, ":agent_group", ":cur_agent"),
               (try_begin),
                 (eq, ":dead_player_no", ":agent_group"),
                 (agent_set_group, ":cur_agent", -1),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
         (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
         (try_begin),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (val_add, ":killer_agent_player_score", 1),
         (else_try),
           (val_add, ":killer_agent_player_score", -1),
         (try_end),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
       (try_end),
     (try_end),

     (call_script, "script_add_kill_death_counts", ":killer_agent_no", ":dead_agent_no"),
     #money management
     (call_script, "script_money_management_after_agent_death", ":killer_agent_no", ":dead_agent_no"),
     ])
]
