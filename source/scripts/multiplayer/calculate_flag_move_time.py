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

calculate_flag_move_time_scripts = [
("calculate_flag_move_time",
   [
     (store_script_param, ":number_of_total_agents_around_flag", 1),
     (store_script_param, ":dist_between_flag_and_its_target", 2),

     (try_begin), #(if no one is around flag it again moves to its current owner situation but 5 times slower than normal)
       (eq, ":number_of_total_agents_around_flag", 0),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 2500),#5.00 * 1.00 * (500 stable) = 2000
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 1),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 500), #1.00 * (500 stable) = 500
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 2),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 300), #0.60(0.60) * (500 stable) = 300
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 3),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 195), #0.39(0.60 * 0.65) * (500 stable) = 195
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 4),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 137), #0.273(0.60 * 0.65 * 0.70) * (500 stable) = 136.5 >rounding> 137
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 5),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 102), #0.20475(0.60 * 0.65 * 0.70 * 0.75) * (500 stable) = 102.375 >rounding> 102
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 6),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 82),  #0.1638(0.60 * 0.65 * 0.70 * 0.75 * 0.80) * (500 stable) = 81.9 >rounding> 82
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 7),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 66),  #0.13104(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85) * (500 stable) = 65.52 >rounding> 66
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 8),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 59),  #0.117936(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90) * (500 stable) = 58.968 >rounding> 59
     (else_try),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 56),  #0.1120392(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90 * 0.95) * (500 stable) = 56.0196 >rounding> 56
     (try_end),

     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":cur_player", 0, ":num_players"),
       (player_is_active, ":cur_player"),
       (val_add, ":number_of_players", 1),
     (try_end),

     (try_begin),
       (lt, ":number_of_players", 10),
       (val_mul, reg0, 50),
     (else_try),
       (lt, ":number_of_players", 35),
       (store_sub, ":number_of_players_multipication", 35, ":number_of_players"),
       (val_mul, ":number_of_players_multipication", 2),
       (store_sub, ":number_of_players_multipication", 100, ":number_of_players_multipication"),
       (val_mul, reg0, ":number_of_players_multipication"),
     (else_try),
       (val_mul, reg0, 100),
     (try_end),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (val_mul, reg0, 2),
     (try_end),

     (val_div, reg0, 10000), #100x for number of players around flag, 100x for number of players in game
     ])
]
