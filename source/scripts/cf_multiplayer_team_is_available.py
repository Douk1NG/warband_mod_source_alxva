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

cf_multiplayer_team_is_available_scripts = [
# script_cf_multiplayer_team_is_available
# Input: arg1 = player_no, arg2 = team_no
# Output: none, true or false
("cf_multiplayer_team_is_available",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":team_no", 2),
     (assign, ":continue_change_team", 1),
     (try_begin),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (is_between, ":team_no", 0, multi_team_spectator),
       (neg|teams_are_enemies, ":team_no", ":team_no"), #checking if it is a deathmatch or not
       (assign, ":continue_change_team", 0),
       #counting number of players for team balance checks
       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
         (neq, ":cur_player", ":player_no"),
         (player_get_team_no, ":player_team", ":cur_player"),
         (try_begin),
           (eq, ":player_team", 0),
           (val_add, ":number_of_players_at_team_1", 1),
         (else_try),
           (eq, ":player_team", 1),
           (val_add, ":number_of_players_at_team_2", 1),
         (try_end),
       (try_end),
       (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),

       (try_begin),
         (ge, ":difference_of_number_of_players", 0),
         (val_add, ":difference_of_number_of_players", 1),
       (else_try),
         (val_add, ":difference_of_number_of_players", -1),
       (try_end),

       (try_begin),
         (eq, ":team_no", 0),
         (lt, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
         (assign, ":continue_change_team", 1),
       (else_try),
         (eq, ":team_no", 1),
         (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
         (gt, ":difference_of_number_of_players", ":checked_value"),
         (assign, ":continue_change_team", 1),
       (try_end),
     (try_end),
     (eq, ":continue_change_team", 1),
     ])
]
