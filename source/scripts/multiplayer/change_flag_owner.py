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

change_flag_owner_scripts = [
("change_flag_owner",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":owner_code", 2),

     (try_begin),
       (lt, ":owner_code", 0),
       (val_add, ":owner_code", 1),
       (val_mul, ":owner_code", -1),
     (try_end),

     (store_div, ":owner_team_no", ":owner_code", 100),
     (store_mod, ":shown_flag_no", ":owner_code", 100),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":older_owner_team_no", "trp_multiplayer_data", ":cur_flag_slot"),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", ":owner_team_no"),

     #senchronizing flag positions
     (try_begin),
       #(this_or_next|eq, ":initial_flags", 0), #moved after auto-animating
       (multiplayer_is_server),

       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
       (try_begin),
         (eq, ":owner_team_no", 0), #if new owner team is 0 then flags are at bottom
         (neq, ":older_owner_team_no", -1), #clients
         (assign, ":continue", 1),
         (try_begin),
           (multiplayer_is_server),
           (eq, "$g_placing_initial_flags", 1),
           (assign, ":continue", 0),
         (try_end),
         (eq, ":continue", 1),
         (prop_instance_get_position, pos0, ":pole_id"),
         (position_move_z, pos0, multi_headquarters_distance_to_change_flag),
       (else_try),
         (prop_instance_get_position, pos0, ":pole_id"), #if new owner team is not 0 then flags are at top
         (position_move_z, pos0, multi_headquarters_pole_height),
       (try_end),

       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),

       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),

       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),
     (try_end),

     #setting visibilities of flags
     (try_begin),
       (eq, ":shown_flag_no", 0),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
     (else_try),
       (eq, ":shown_flag_no", 1),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (else_try),
       (eq, ":shown_flag_no", 2),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (try_end),

     #other
     (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_get_slot, ":players_around_code", "trp_multiplayer_data", ":cur_flag_players_around_slot"),

     (store_div, ":number_of_agents_around_flag_team_1", ":players_around_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":players_around_code", 100),

     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
   ])
]
