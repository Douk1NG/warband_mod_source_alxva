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

find_most_suitable_bot_to_control_scripts = [
("find_most_suitable_bot_to_control",
   [
      (set_fixed_point_multiplier, 100),
      (store_script_param, ":player_no", 1),
      (player_get_team_no, ":player_team", ":player_no"),

      (player_get_slot, ":x_coor", ":player_no", slot_player_death_pos_x),
      (player_get_slot, ":y_coor", ":player_no", slot_player_death_pos_y),
      (player_get_slot, ":z_coor", ":player_no", slot_player_death_pos_z),

      (init_position, pos0),
      (position_set_x, pos0, ":x_coor"),
      (position_set_y, pos0, ":y_coor"),
      (position_set_z, pos0, ":z_coor"),

      (assign, ":most_suitable_bot", -1),
      (assign, ":max_bot_score", -1),

      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_non_player, ":cur_agent"),
        (agent_get_team ,":cur_team", ":cur_agent"),
        (eq, ":cur_team", ":player_team"),
        (agent_get_position, pos1, ":cur_agent"),

        #getting score for distance of agent to death point (0..3000)
        (get_distance_between_positions_in_meters, ":dist", pos0, pos1),

        (try_begin),
          (lt, ":dist", 500),
          (store_sub, ":bot_score", 500, ":dist"),
        (else_try),
          (assign, ":bot_score", 0),
        (try_end),
        (val_mul, ":bot_score", 6),

        #getting score for distance of agent to enemy & friend agents (0..300 x agents)
        (try_for_agents, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (neq, ":cur_agent", ":cur_agent_2"),
          (agent_get_team ,":cur_team_2", ":cur_agent_2"),
          (try_begin),
            (neq, ":cur_team_2", ":player_team"),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":enemy_near_score", ":dist_2"),
            (else_try),
              (assign, ":enemy_near_score", 300),
            (try_end),
            (val_add, ":bot_score", ":enemy_near_score"),
          (else_try),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":friend_near_score", 300, ":dist_2"),
            (else_try),
              (assign, ":friend_near_score", 0),
            (try_end),
            (val_add, ":bot_score", ":friend_near_score"),
          (try_end),
        (try_end),

        #getting score for health (0..200)
        (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        (val_mul, ":agent_hit_points", 2),
        (val_add, ":bot_score", ":agent_hit_points"),

        (ge, ":bot_score", ":max_bot_score"),
        (assign, ":max_bot_score", ":bot_score"),
        (assign, ":most_suitable_bot", ":cur_agent"),
      (try_end),

      (assign, reg0, ":most_suitable_bot"),
    ])
]
