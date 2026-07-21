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

check_team_balance_scripts = [
("check_team_balance",
   [
     (try_begin),
       (multiplayer_is_server),

       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
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
       (assign, ":number_of_players_will_be_moved", 0),
       (try_begin),
         (try_begin),
           (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
           (le, ":difference_of_number_of_players", ":checked_value"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (assign, ":team_with_more_players", 1),
           (assign, ":team_with_less_players", 0),
         (else_try),
           (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (assign, ":team_with_more_players", 0),
           (assign, ":team_with_less_players", 1),
         (try_end),
       (try_end),
       #team balance checks are done
       (try_begin),
         (gt, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (eq, "$g_team_balance_next_round", 1), #if warning is given

           #auto team balance starts
           (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"),
             (assign, ":max_player_join_time", 0),
             (assign, ":latest_joined_player_no", -1),
             (get_max_players, ":num_players"),
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (player_get_team_no, ":player_team", ":player_no"),
               (eq, ":player_team", ":team_with_more_players"),
               (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
               (try_begin),
                 (gt, ":player_join_time", ":max_player_join_time"),
                 (assign, ":max_player_join_time", ":player_join_time"),
                 (assign, ":latest_joined_player_no", ":player_no"),
               (try_end),
             (try_end),
             (try_begin),
               (ge, ":latest_joined_player_no", 0),
               (try_begin),
                 #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                 (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"),
                 (ge, ":latest_joined_agent_id", 0),
                 (agent_is_alive, ":latest_joined_agent_id"),

                 (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                 (val_add, ":player_kill_count", 1),
                 (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                 (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                 (val_sub, ":player_death_count", 1),
                 (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                 (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                 (val_add, ":player_score", 1),
                 (player_set_score, ":latest_joined_player_no", ":player_score"),

                 (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                   (player_is_active, ":player_no"),
                   (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                 (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                 (val_add, ":player_gold", ":old_items_value"),
                 (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
               (end_try),

               (player_set_troop_id, ":latest_joined_player_no", -1),
               (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
               (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
             (try_end),
           (try_end),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------
           (get_max_players, ":num_players"),
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
           (try_end),
           (assign, "$g_team_balance_next_round", 0),
           #auto team balance done
         (else_try),
           #tutorial message (next round there will be auto team balance)
           (assign, "$g_team_balance_next_round", 1),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------
           (get_max_players, ":num_players"),
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next),
           (try_end),
         (try_end),
       (else_try),
         (assign, "$g_team_balance_next_round", 0),
       (try_end),
     (try_end),
   ])
]
