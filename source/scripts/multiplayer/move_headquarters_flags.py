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

move_headquarters_flags_scripts = [
("move_headquarters_flags",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":number_of_agents_around_flag_team_1", 2),
     (store_script_param, ":number_of_agents_around_flag_team_2", 3),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":current_owner", "trp_multiplayer_data", ":cur_flag_slot"),

     (scene_prop_get_num_instances, ":num_instances", "spr_headquarters_flag_gray_code_only"),
     (try_begin),
       (assign, ":visibility", 0),
       (lt, ":flag_no", ":num_instances"),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_get_visibility, ":visibility", ":flag_id"),
     (try_end),

     (try_begin),
       (eq, ":visibility", 1),
       (assign, ":shown_flag", 0),
       (assign, ":shown_flag_id", ":flag_id"),
     (else_try),
       (scene_prop_get_num_instances, ":num_instances", "$team_1_flag_scene_prop"),
       (try_begin),
         (assign, ":visibility", 0),
         (lt, ":flag_no", ":num_instances"),
         (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (scene_prop_get_visibility, ":visibility", ":flag_id"),
       (try_end),

       #(scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       #(scene_prop_get_visibility, ":visibility", ":flag_id"),
       (try_begin),
         (eq, ":visibility", 1),
         (assign, ":shown_flag", 1),
         (assign, ":shown_flag_id", ":flag_id"),
       (else_try),
         (scene_prop_get_num_instances, ":num_instances", "$team_2_flag_scene_prop"),
         (try_begin),
           (assign, ":visibility", 0),
           (lt, ":flag_no", ":num_instances"),
           (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
           (scene_prop_get_visibility, ":visibility", ":flag_id"),
         (try_end),

         #(scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         #(scene_prop_get_visibility, ":visibility", ":flag_id"),
         (try_begin),
           (eq, ":visibility", 1),
           (assign, ":shown_flag", 2),
           (assign, ":shown_flag_id", ":flag_id"),
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
     (try_end),

     (try_begin),
       (eq, ":shown_flag", ":current_owner"), #situation 1 : (current owner is equal shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),
         (assign, ":flag_movement", 0), #0:stop
       (else_try),
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", 1), #1:rise (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (eq, ":current_owner", 1),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (eq, ":current_owner", 2),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (assign, ":flag_movement", -1), #-1:drop (fast)
         (try_end),
       (try_end),
     (else_try), #situation 2 : (current owner is different than shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),
         (assign, ":flag_movement", 0), #0:stop
       (else_try),
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", -1), #-1:drop (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (try_begin),
             (eq, ":shown_flag", 1),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 1),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (try_begin),
             (eq, ":shown_flag", 2),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 2),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (try_end),
       (try_end),
     (try_end),

     (store_add, ":number_of_total_agents_around_flag", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),

     (try_begin),
       (eq, ":flag_movement", 0),
       (assign, reg0, 0),
     (else_try),
       (eq, ":flag_movement", 1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (position_move_z, pos0, multi_headquarters_pole_height),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (else_try),
       (eq, ":flag_movement", -1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (try_end),

     (call_script, "script_move_flag", ":shown_flag_id", reg0), #pos0 : target position
     ])
]
