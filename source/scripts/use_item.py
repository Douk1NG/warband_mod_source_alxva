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

use_item_scripts = [
("use_item",
   [
     (store_script_param, ":instance_id", 1),
     (store_script_param, ":user_id", 2),

     (try_begin),
       (game_in_multiplayer_mode),
       (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
       (eq, ":scene_prop_id", "spr_winch_b"),

       (multiplayer_get_my_player, ":my_player_no"),

       (this_or_next|gt, ":my_player_no", 0),
       (neg|multiplayer_is_dedicated_server),

       (ge, ":my_player_no", 0),
       (player_get_agent_id, ":my_agent_id", ":my_player_no"),
       (ge, ":my_agent_id", 0),
       (agent_is_active, ":my_agent_id"),
       (agent_get_team, ":my_team_no", ":my_agent_id"),
       (eq, ":my_team_no", 0),

       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (ge, ":user_id", 0),
       (agent_is_active, ":user_id"),
       (agent_get_player_id, ":user_player", ":user_id"),
       (str_store_player_username, s7, ":user_player"),

       (try_begin),
         (eq, ":opened_or_closed", 0),
         (display_message, "@{s7} opened the gate"),
       (else_try),
         (display_message, "@{s7} closed the gate"),
       (try_end),
     (try_end),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (assign, ":smallest_dist", -1),
     (prop_instance_get_position, pos0, ":instance_id"),
     (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
       (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions, ":dist", pos0, pos1),
       (this_or_next|eq, ":smallest_dist", -1),
       (lt, ":dist", ":smallest_dist"),
       (assign, ":smallest_dist", ":dist"),
       (assign, ":effected_object_instance_id", ":cur_instance_id"),
     (try_end),

     (try_begin),
       (ge, ":instance_id", 0),
       (ge, ":smallest_dist", 0),

       (try_begin),
         (eq, ":effected_object", "spr_portcullis"),
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0), #open gate

           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, 375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, 72000),
           (try_end),
         (else_try), #close gate
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, -375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 0),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, -72000),
           (try_end),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_6m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_8m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_10m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_12m"),
         (eq, ":effected_object", "spr_siege_ladder_move_14m"),

         (try_begin),
           (eq, ":effected_object", "spr_siege_ladder_move_6m"),
           (assign, ":animation_time_drop", 120),
           (assign, ":animation_time_elevate", 240),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_8m"),
           (assign, ":animation_time_drop", 140),
           (assign, ":animation_time_elevate", 280),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_10m"),
           (assign, ":animation_time_drop", 160),
           (assign, ":animation_time_elevate", 320),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_12m"),
           (assign, ":animation_time_drop", 190),
           (assign, ":animation_time_elevate", 360),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_14m"),
           (assign, ":animation_time_drop", 230),
           (assign, ":animation_time_elevate", 400),
         (try_end),

         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_elevate"), #3 seconds in average
           (eq, ":opened_or_closed", 0), #ladder at ground
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
           (prop_instance_enable_physics, ":effected_object_instance_id", 0),
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 300),
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try), #ladder at wall
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_drop"), #1.5 seconds in average
           (prop_instance_get_position, pos0, ":instance_id"),

           (assign, ":smallest_dist", -1),
           (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
             (entry_point_get_position, pos1, ":entry_point_no"),
             (get_sq_distance_between_positions, ":dist", pos0, pos1),
             (this_or_next|eq, ":smallest_dist", -1),
             (lt, ":dist", ":smallest_dist"),
             (assign, ":smallest_dist", ":dist"),
             (assign, ":nearest_entry_point", ":entry_point_no"),
           (try_end),

           (try_begin),
             (ge, ":smallest_dist", 0),
             (lt, ":smallest_dist", 22500), #max 15m distance
             (entry_point_get_position, pos1, ":nearest_entry_point"),
             (position_rotate_x, pos1, -90),
             (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_smoke_effect_done, 0),
             (prop_instance_enable_physics, ":effected_object_instance_id", 0),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos1, 130),
           (try_end),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_door_destructible"),
         (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
         (eq, ":scene_prop_id", "spr_castle_f_door_a"),

         (assign, ":effected_object_instance_id", ":instance_id"),
         (scene_prop_get_slot, ":opened_or_closed", ":effected_object_instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0),

           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (try_begin),
             (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
             (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),

             (position_rotate_z, pos0, -85),
           (else_try),
             (position_rotate_z, pos0, 85),
           (try_end),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try),
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (try_end),
     (try_end),
     ])
]
