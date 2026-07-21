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

cf_multiplayer_evaluate_poll_scripts = [
#script_get_headquarters_scores
# Input: none
# Output: none (can fail)
("cf_multiplayer_evaluate_poll",
   [
     (assign, ":result", 0),
     (assign, "$g_multiplayer_poll_ended", 1),
     (store_add, ":total_votes", "$g_multiplayer_poll_yes_count", "$g_multiplayer_poll_no_count"),
     (store_sub, ":abstain_votes", "$g_multiplayer_poll_num_sent", ":total_votes"),
     (store_mul, ":nos_from_abstains", 3, ":abstain_votes"),
     (val_div, ":nos_from_abstains", 10), #30% of abstains are counted as no
     (val_add, ":total_votes", ":nos_from_abstains"),
     (val_max, ":total_votes", 1), #if someone votes and only 1-3 abstain occurs?
     (store_mul, ":vote_ratio", 100, "$g_multiplayer_poll_yes_count"),
     (val_div, ":vote_ratio", ":total_votes"),
     (try_begin),
       (ge, ":vote_ratio", "$g_multiplayer_valid_vote_ratio"),
       (assign, ":result", 1),
       (try_begin),
         (eq, "$g_multiplayer_poll_to_show", 1), #kick player
         (try_begin),
           (player_is_active, "$g_multiplayer_poll_value_to_show"),
           (kick_player, "$g_multiplayer_poll_value_to_show"),
         (try_end),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 2), #ban player
         (ban_player_using_saved_ban_info), #already loaded at the beginning of the poll
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
         (team_set_faction, 0, "$g_multiplayer_poll_value_2_to_show"),
         (team_set_faction, 1, "$g_multiplayer_poll_value_3_to_show"),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 4), #change number of bots
         (assign, "$g_multiplayer_num_bots_team_1", "$g_multiplayer_poll_value_to_show"),
         (assign, "$g_multiplayer_num_bots_team_2", "$g_multiplayer_poll_value_2_to_show"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
         (try_end),
       (try_end),
     (else_try),
       (assign, "$g_multiplayer_poll_running", 0), #end immediately if poll fails. but end after some time if poll succeeds (apply the results first)
     (try_end),
     (get_max_players, ":num_players"),
     #for only server itself-----------------------------------------------------------------------------------------------
     (call_script, "script_show_multiplayer_message", multiplayer_message_type_poll_result, ":result"), #0 is useless here
     #for only server itself-----------------------------------------------------------------------------------------------
     (try_for_range, ":cur_player", 1, ":num_players"),
       (player_is_active, ":cur_player"),
       (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_show_multiplayer_message, multiplayer_message_type_poll_result, ":result"),
     (try_end),
     (eq, ":result", 1),
     ])
]
