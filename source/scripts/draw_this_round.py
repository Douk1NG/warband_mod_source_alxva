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

draw_this_round_scripts = [
("draw_this_round",
   [
    (store_script_param, ":value", 1),
    (try_begin),
      (eq, ":value", -9), #destroy mod round end
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      #(assign, "$g_multiplayer_message_value_1", -1),
      #(assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      #(start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", -1), #draw
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      (assign, "$g_multiplayer_message_value_1", -1),
      (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", 0), #defender wins
      #THIS_IS_OUR_LAND achievement
      (try_begin),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        (multiplayer_get_my_player, ":my_player_no"),
        (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
        (player_get_agent_id, ":my_player_agent", ":my_player_no"),
        (ge, ":my_player_agent", 0),
        (agent_is_alive, ":my_player_agent"),
        (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
        (eq, ":my_player_agent_team_no", 0), #defender
        (unlock_achievement, ACHIEVEMENT_THIS_IS_OUR_LAND),
      (try_end),
      #THIS_IS_OUR_LAND achievement end
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),

      (team_get_faction, ":faction_of_winner_team", 0),
      (team_get_score, ":team_1_score", 0),
      (val_add, ":team_1_score", 1),
      (team_set_score, 0, ":team_1_score"),
      (assign, "$g_winner_team", 0),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
      (else_try),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", 1), #attacker wins
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),

      (team_get_faction, ":faction_of_winner_team", 1),
      (team_get_score, ":team_2_score", 1),
      (val_add, ":team_2_score", 1),
      (team_set_score, 1, ":team_2_score"),
      (assign, "$g_winner_team", 1),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
      (else_try),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    #LAST_MAN_STANDING achievement
    (try_begin),
      (is_between, ":value", 0, 2), #defender or attacker wins
      (try_begin),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (multiplayer_get_my_player, ":my_player_no"),
        (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
        (player_get_agent_id, ":my_player_agent", ":my_player_no"),
        (ge, ":my_player_agent", 0),
        (agent_is_alive, ":my_player_agent"),
        (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
        (eq, ":my_player_agent_team_no", ":value"), #winner team
        (unlock_achievement, ACHIEVEMENT_LAST_MAN_STANDING),
      (try_end),
    (try_end),
    #LAST_MAN_STANDING achievement end
    ])
]
