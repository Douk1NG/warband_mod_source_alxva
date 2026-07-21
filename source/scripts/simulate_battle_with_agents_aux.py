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

simulate_battle_with_agents_aux_scripts = [
# script_simulate_battle_with_agents_aux
# For internal use only
# Input: arg1 = attacker_side (0 = ally, 1 = enemy), arg2 = damage amount
# Output: none
("simulate_battle_with_agents_aux",
    [
      (store_script_param_1, ":attacker_side"),
      (store_script_param_2, ":damage"),

      (get_player_agent_no, ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (neq, ":player_agent", ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        #do not check agent_is_alive, check slot_agent_is_alive_before_retreat instead, so that dead agents can still hit enemies
        (agent_slot_eq, ":cur_agent", slot_agent_is_alive_before_retreat, 1),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (assign, ":cur_agents_side", 0),
        (else_try),
          (assign, ":cur_agents_side", 1),
        (try_end),
        (eq, ":cur_agents_side", ":attacker_side"),
        (agent_get_position, pos2, ":cur_agent"),
        (assign, ":closest_agent", -1),
        (assign, ":min_distance", 100000),
        (try_for_agents, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (try_begin),
            (agent_is_ally, ":cur_agent_2"),
            (assign, ":cur_agents_side_2", 0),
          (else_try),
            (assign, ":cur_agents_side_2", 1),
          (try_end),
          (this_or_next|neq, ":cur_agent_2", ":player_agent"),
          (eq, "$pin_player_fallen", 0),
          (neq, ":attacker_side", ":cur_agents_side_2"),
          (agent_get_position, pos3, ":cur_agent_2"),
          (get_distance_between_positions, ":cur_distance", pos2, pos3),
          (lt, ":cur_distance", ":min_distance"),
          (assign, ":min_distance", ":cur_distance"),
          (assign, ":closest_agent", ":cur_agent_2"),
        (try_end),
        (ge, ":closest_agent", 0),
        #Fight
        (agent_get_class, ":agent_class", ":cur_agent"),
        (assign, ":agents_speed", 1),
        (assign, ":agents_additional_hit", 0),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (assign, ":agents_additional_hit", 2),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed", 2),
        (try_end),
        (agent_get_class, ":agent_class", ":closest_agent"),
        (assign, ":agents_speed_2", 1),
        (try_begin),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed_2", 2),
        (try_end),
        (assign, ":agents_hit", 18000),
        (val_add, ":min_distance", 3000),
        (val_div, ":agents_hit", ":min_distance"),
        (val_mul, ":agents_hit", 2),# max 10, min 2 hits within 150 meters

        (val_mul, ":agents_hit", ":agents_speed"),
        (val_div, ":agents_hit", ":agents_speed_2"),
        (val_add, ":agents_hit", ":agents_additional_hit"),

        (assign, ":cur_damage", ":damage"),
        (agent_get_troop_id, ":closest_troop", ":closest_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (store_character_level, ":closest_level", ":closest_troop"),
        (store_character_level, ":cur_level", ":cur_troop"),
        (store_sub, ":level_dif", ":cur_level", ":closest_level"),
        (val_div, ":level_dif", 5),
        (val_add, ":cur_damage", ":level_dif"),

        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (val_div, ":cur_damage", 2),
          (store_agent_hit_points, ":init_player_hit_points", ":player_agent", 1),
        (try_end),

        (try_for_range, ":unused", 0, ":agents_hit"),
          (store_random_in_range, ":random_damage", 0, 100),
          (lt, ":random_damage", ":cur_damage"),
          (agent_deliver_damage_to_agent, ":cur_agent", ":closest_agent"),
        (try_end),

        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (store_agent_hit_points, ":final_player_hit_points", ":player_agent", 1),
          (store_sub, ":hit_points_difference", ":init_player_hit_points", ":final_player_hit_points"),
          (val_add, "$g_last_mission_player_damage", ":hit_points_difference"),
        (try_end),

        (neg|agent_is_alive, ":closest_agent"),
        (try_begin),
          (eq, ":attacker_side", 1),
          (party_add_members, "p_temp_party", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party", ":closest_troop", 1),
          (try_end),
        (else_try),
          (party_add_members, "p_temp_party_2", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party_2", ":closest_troop", 1),
          (try_end),
        (try_end),
      (try_end),
  ])
]
