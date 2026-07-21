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

show_multiplayer_message_scripts = [
#script_move_belfries_to_their_first_entry_point
# INPUT: arg1 = multiplayer_message_type
# OUTPUT: none
("show_multiplayer_message",
   [
    (store_script_param, ":multiplayer_message_type", 1),
    (store_script_param, ":value", 2),

    (assign, "$g_multiplayer_message_type", ":multiplayer_message_type"),

    (try_begin),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),

      (try_begin), #end of round in clients
        (neg|multiplayer_is_server),
        (assign, "$g_battle_death_mode_started", 0),
      (try_end),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_done),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_2"),
      (assign, "$g_team_balance_next_round", 0),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
      (assign, "$g_team_balance_next_round", 1),
      (call_script, "script_warn_player_about_auto_team_balance"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_no_need),
      (assign, "$g_team_balance_next_round", 0),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_score),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_returned_home),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_stole),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_poll_result),
      (assign, "$g_multiplayer_message_value_3", ":value"),
      (start_presentation, "prsnt_multiplayer_message_3"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_neutralized),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_captured),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_is_pulling),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_target_destroyed),

      (try_begin), #destroy score (condition : a target destroyed)
        (eq, "$g_defender_team", 0),
        (assign, ":attacker_team_no", 1),
      (else_try),
        (assign, ":attacker_team_no", 0),
      (try_end),

      (team_get_score, ":team_score", ":attacker_team_no"),
      (val_add, ":team_score", 1),
      (call_script, "script_team_set_score", ":attacker_team_no", ":team_score"), #destroy score end

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_defenders_saved_n_targets),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_attackers_won_the_round),
      (try_begin),
        (eq, "$g_defender_team", 0),
        (assign, "$g_multiplayer_message_value_1", 1),
      (else_try),
        (assign, "$g_multiplayer_message_value_1", 0),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    ])
]
