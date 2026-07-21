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

multiplayer_send_initial_information_scripts = [
#script_send_open_close_information_of_object
# Input: arg1 = player_no
# Output: none
("multiplayer_send_initial_information",
   [
     (store_script_param, ":player_no", 1),

     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_auto_team_balance_limit, "$g_multiplayer_auto_team_balance_limit"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_num_bots_voteable, "$g_multiplayer_num_bots_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_factions_voteable, "$g_multiplayer_factions_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_maps_voteable, "$g_multiplayer_maps_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_kick_voteable, "$g_multiplayer_kick_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ban_voteable, "$g_multiplayer_ban_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_allow_player_banners, "$g_multiplayer_allow_player_banners"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_force_default_armor, "$g_multiplayer_force_default_armor"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_disallow_ranged_weapons, "$g_multiplayer_disallow_ranged_weapons"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_type, "$g_multiplayer_game_type"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),

     (store_mission_timer_a, ":mission_timer"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_server_mission_timer_while_player_joined, ":mission_timer"),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_count, "$g_multiplayer_number_of_respawn_count"),
     (try_end),

     (try_for_agents, ":cur_agent"), #send if any agent is carrying any scene object
       (agent_is_human, ":cur_agent"),
       (agent_get_attached_scene_prop, ":attached_scene_prop", ":cur_agent"),
       (ge, ":attached_scene_prop", 0),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":cur_agent", ":attached_scene_prop"),
     (try_end),

     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_6m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_8m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_10m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_12m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_14m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_winch_b"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_e_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_left"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_right"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_door_destructible"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_b"),

     (try_begin),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

       (store_mission_timer_a, ":current_time"),
       (val_sub, ":current_time", "$g_round_start_time"),
       (val_mul, ":current_time", -1),

       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, ":current_time"),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       #if game type is capture the flag send current flag situations to each player.
       (team_get_slot, ":flag_situation_team_1", 0, slot_team_flag_situation),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, 0, ":flag_situation_team_1"),
       (team_get_slot, ":flag_situation_team_2", 1, slot_team_flag_situation),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, 1, ":flag_situation_team_2"),
     (else_try),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       #if game type is headquarters send number of agents placed around each pole's around to player.
       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (assign, ":number_of_agents_around_flag_team_1", 0),
         (assign, ":number_of_agents_around_flag_team_2", 0),

         (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
         (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.

         (try_for_agents, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (agent_is_alive, ":cur_agent"),
           (neg|agent_is_non_player, ":cur_agent"),
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
           (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
           (get_sq_distance_between_position_heights, ":squared_height_dist", pos0, pos1),
           (val_add, ":squared_dist", ":squared_height_dist"),
           (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
           (try_begin),
             (eq, ":cur_agent_team", 0),
             (val_add, ":number_of_agents_around_flag_team_1", 1),
           (else_try),
             (eq, ":cur_agent_team", 1),
             (val_add, ":number_of_agents_around_flag_team_2", 1),
           (try_end),
         (try_end),

         (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
         (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),
         (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
       (try_end),

       #if game type is headquarters send owners of each pole to player.
       (assign, "$g_placing_initial_flags", 1),
       (try_for_range, ":cur_flag", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":cur_flag"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_slot"),
         (store_mul, ":cur_flag_owner_code", ":cur_flag_owner", 100),
         (val_add, ":cur_flag_owner_code", ":cur_flag_owner"),
         (val_add, ":cur_flag_owner_code", 1),
         (val_mul, ":cur_flag_owner_code", -1),
         (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":cur_flag", ":cur_flag_owner_code"),
       (try_end),
       (assign, "$g_placing_initial_flags", 0),
     (try_end),

     #(multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_day_time, "$g_round_day_time"),
    ])
]
