# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

multiplayer_respawn_time_counter = ("multiplayer_respawn_time_counter", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),

      (assign, "$g_multiplayer_respawn_counter_overlay", -1),
      (assign, "$g_multiplayer_respawn_remained_overlay", -1),

      (assign, ":do_not_show_respawn_counter", 0),
      (try_begin),
        (eq, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
        (this_or_next|eq, "$g_round_ended", 1),
        (eq, "$g_flag_is_not_ready", 1),
        (assign, ":do_not_show_respawn_counter", 1),
      (try_end),
      (eq, ":do_not_show_respawn_counter", 0),

      (assign, "$g_multiplayer_last_respawn_counter_value", -1),
      (str_clear, s0),
      (create_text_overlay, "$g_multiplayer_respawn_counter_overlay", s0, tf_center_justify|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_respawn_counter_overlay", 0xFFFFFF),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 600),
      (overlay_set_position, "$g_multiplayer_respawn_counter_overlay", pos1),
      (position_set_x, pos1, 2000),
      (position_set_y, pos1, 2000),
      (overlay_set_size, "$g_multiplayer_respawn_counter_overlay", pos1),

      (str_clear, s0),
      (create_text_overlay, "$g_multiplayer_respawn_remained_overlay", s0, tf_center_justify|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_respawn_remained_overlay", 0xFFFFFF),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 570),
      (overlay_set_position, "$g_multiplayer_respawn_remained_overlay", pos1),
      (position_set_x, pos1, 1400),
      (position_set_y, pos1, 1400),
      (overlay_set_size, "$g_multiplayer_respawn_remained_overlay", pos1),

      #(store_mission_timer_a, "$g_multiplayer_respawn_start_time"),
      (presentation_set_duration, 999999),
      ]),

    (ti_on_presentation_run, [
      (ge, "$g_multiplayer_respawn_counter_overlay", 0),
      (multiplayer_get_my_player, ":my_player_no"),
      (try_begin),
        (ge, ":my_player_no", 0),
        (player_get_team_no, ":player_team", ":my_player_no"),
        (try_begin),
          (eq, ":player_team", multi_team_spectator),
          (presentation_set_duration, 0),
        (else_try),
          (store_mission_timer_a, ":current_time"),
          (store_sub, ":seconds_past_in_respawn", ":current_time", "$g_multiplayer_respawn_start_time"),
          (try_begin),
            (eq, "$g_show_no_more_respawns_remained", 0),
            (assign, ":total_respawn_time", "$g_multiplayer_respawn_period"),
            (try_begin),
              (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
              (player_get_team_no, ":player_team", ":my_player_no"),
              (eq, ":player_team", 0),
              (val_add, ":total_respawn_time", multiplayer_siege_mod_defender_team_extra_respawn_time),
            (try_end),
          (else_try),
            (assign, ":total_respawn_time", 6),
          (try_end),
          (store_sub, ":seconds_left_in_respawn", ":total_respawn_time", ":seconds_past_in_respawn"),
          (try_begin),
            (le, ":seconds_left_in_respawn", 0),
            (presentation_set_duration, 0),
          (else_try),
            (neq, "$g_multiplayer_last_respawn_counter_value", ":seconds_left_in_respawn"),
            (assign, "$g_multiplayer_last_respawn_counter_value", ":seconds_left_in_respawn"),
            (try_begin),
              (eq, "$g_show_no_more_respawns_remained", 0),
              (assign, reg0, ":seconds_left_in_respawn"),
              (str_store_string, s0, "str_respawning_in_reg0_seconds"),
              (try_begin),
                (gt, "$g_multiplayer_number_of_respawn_count", 0),
                (store_sub, reg0, "$g_multiplayer_number_of_respawn_count", "$g_my_spawn_count"),

                (multiplayer_get_my_player, ":my_player_no"),
                (player_get_team_no, ":my_player_team", ":my_player_no"),
                (eq, ":my_player_team", 0),

                (try_begin),
                  (gt, reg0, 1),
                  (str_store_string, s1, "str_reg0_respawns_remained"),
                (else_try),
                  (str_store_string, s1, "str_this_is_your_last_respawn"),
                (try_end),
              (else_try),
                (str_clear, s1),
              (try_end),
            (else_try),
              (eq, "$g_show_no_more_respawns_remained", 1),
              ##(assign, "$g_informed_about_no_more_respawns_remained", 1),
              (str_store_string, s0, "str_no_more_respawns_remained_this_round"),
              (str_clear, s1),
              (str_store_string, s1, "str_wait_next_round"),
            (try_end),
            (overlay_set_text, "$g_multiplayer_respawn_counter_overlay", s0),
            (overlay_set_text, "$g_multiplayer_respawn_remained_overlay", s1),
          (try_end),
        (try_end),
      (else_try),
        (presentation_set_duration, 0),
      (try_end),

      (try_begin),
        (eq, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
        (this_or_next|eq, "$g_round_ended", 1),
        (eq, "$g_flag_is_not_ready", 1),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ])
