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

multiplayer_find_spawn_point_scripts = [
("multiplayer_find_spawn_point",
  [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care

     (set_fixed_point_multiplier, 100),

     (assign, ":flags", 0),

     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (val_or, ":flags", spf_examine_all_spawn_points),
     (try_end),

     (try_begin),
       (eq, ":is_horseman", 1),
       (val_or, ":flags", spf_is_horseman),
     (try_end),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (val_or, ":flags", spf_all_teams_are_enemy),
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (val_or, ":flags", spf_team_1_spawn_far_from_entry_66), #team 1 agents will not spawn 70 meters around of entry 0
       (val_or, ":flags", spf_team_0_walkers_spawn_at_high_points),
       (val_or, ":flags", spf_team_0_spawn_near_entry_66),
       (val_or, ":flags", spf_care_agent_to_agent_distances_less),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (val_or, ":flags", spf_team_1_spawn_far_from_entry_0), #team 1 agents will not spawn 70 meters around of entry 0
       (val_or, ":flags", spf_team_0_spawn_far_from_entry_32), #team 0 agents will not spawn 70 meters around of entry 32
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (assign, ":assigned_flag_count", 0),

       (store_sub, ":maximum_moved_flag_distance", multi_headquarters_pole_height, 50), #900 - 50 = 850
       (store_mul, ":maximum_moved_flag_distance_sq", ":maximum_moved_flag_distance", ":maximum_moved_flag_distance"),
       (val_div, ":maximum_moved_flag_distance_sq", 100), #dividing 100, because fixed point multiplier is 100 and it is included twice, look above line.

       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

         (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
         (prop_instance_get_position, pos0, ":pole_id"),

         (try_begin),
           (eq, ":cur_flag_owner", 1),
           (scene_prop_get_instance, ":flag_of_team_1", "$team_1_flag_scene_prop", ":flag_no"),

           (prop_instance_get_position, pos1, ":flag_of_team_1"),
           (get_sq_distance_between_positions, ":flag_height_sq", pos0, pos1),
           (ge, ":flag_height_sq", ":maximum_moved_flag_distance_sq"),

           (set_spawn_effector_scene_prop_id, ":assigned_flag_count", ":flag_of_team_1"),
           (val_add, ":assigned_flag_count", 1),
         (else_try),
           (eq, ":cur_flag_owner", 2),
           (scene_prop_get_instance, ":flag_of_team_2", "$team_2_flag_scene_prop", ":flag_no"),

           (prop_instance_get_position, pos1, ":flag_of_team_2"),
           (get_sq_distance_between_positions, ":flag_height_sq", pos0, pos1),
           (ge, ":flag_height_sq", ":maximum_moved_flag_distance_sq"),

           (set_spawn_effector_scene_prop_id, ":assigned_flag_count", ":flag_of_team_2"),
           (val_add, ":assigned_flag_count", 1),
         (try_end),
       (try_end),
       (set_spawn_effector_scene_prop_id, ":assigned_flag_count", -1),
     (try_end),

     (multiplayer_find_spawn_point, reg0, ":team_no", ":flags"),
  ])
]
