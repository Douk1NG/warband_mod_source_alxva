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

multiplayer_poll = ("multiplayer_poll", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load,
     [(set_fixed_point_multiplier, 1000),

      (create_mesh_overlay, reg0, "mesh_white_plane"),
      (overlay_set_color, reg0, 0x000000),
      (overlay_set_alpha, reg0, 0x44),
      (position_set_x, pos1, 50),
      (position_set_y, pos1, 50),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 37500),
      (position_set_y, pos1, 4500),
      (overlay_set_size, reg0, pos1),

      (try_begin),
        (eq, "$g_multiplayer_poll_to_show", 0),
        (store_sub, ":string_index", "$g_multiplayer_poll_value_to_show", multiplayer_scenes_begin),
        (val_add, ":string_index", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_index"),
        (create_text_overlay, reg0, "str_poll_change_map", tf_center_justify),
      (else_try),
        (eq, "$g_multiplayer_poll_to_show", 1),
        (str_store_player_username, s0, "$g_multiplayer_poll_value_to_show"),
        (create_text_overlay, reg0, "str_poll_kick_player", tf_center_justify),
      (else_try),
        (eq, "$g_multiplayer_poll_to_show", 2),
        (str_store_player_username, s0, "$g_multiplayer_poll_value_to_show"),
        (create_text_overlay, reg0, "str_poll_ban_player", tf_center_justify),
      (else_try),
        (eq, "$g_multiplayer_poll_to_show", 3),
        (store_sub, ":string_index", "$g_multiplayer_poll_value_to_show", multiplayer_scenes_begin),
        (val_add, ":string_index", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_index"),
        (str_store_faction_name, s1, "$g_multiplayer_poll_value_2_to_show"),
        (str_store_faction_name, s2, "$g_multiplayer_poll_value_3_to_show"),
        (create_text_overlay, reg0, "str_poll_change_map_with_faction", tf_center_justify|tf_scrollable_style_2),
      (else_try),
        (assign, reg0, "$g_multiplayer_poll_value_to_show"),
        (assign, reg1, "$g_multiplayer_poll_value_2_to_show"),
        (str_store_faction_name, s0, "$g_multiplayer_team_1_faction"),
        (str_store_faction_name, s1, "$g_multiplayer_team_2_faction"),
        (create_text_overlay, reg0, "str_poll_change_number_of_bots", tf_center_justify|tf_scrollable_style_2),
      (try_end),
      (overlay_set_color, reg0, 0xFFFFFF),
      (try_begin),
        (neq, "$g_multiplayer_poll_to_show", 3),
        (neq, "$g_multiplayer_poll_to_show", 4),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),
      (else_try),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 70),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 60),
        (overlay_set_area_size, reg0, pos1),
      (try_end),

      (store_mission_timer_a, ":mission_timer"),
      (store_sub, "$g_multiplayer_poll_last_written_seconds_left", "$g_multiplayer_poll_client_end_time", ":mission_timer"),
      (assign, reg0, "$g_multiplayer_poll_last_written_seconds_left"),

      (create_text_overlay, "$g_presentation_obj_poll_1", "str_poll_time_left", tf_right_align|tf_single_line),
      (overlay_set_color, "$g_presentation_obj_poll_1", 0xFFFFFF),
      (position_set_x, pos1, 790),
      (position_set_y, pos1, 60),
      (overlay_set_position, "$g_presentation_obj_poll_1", pos1),

      (omit_key_once, key_1),
      (omit_key_once, key_2),
      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_run,
     [(store_trigger_param_1, ":cur_time"),
      (try_begin),
        (this_or_next|key_clicked, key_escape),
		(this_or_next|key_clicked, key_xbox_start),
        (key_clicked, key_2),
        (gt, ":cur_time", 500),
        (multiplayer_send_int_to_server, multiplayer_event_answer_to_poll, 0),
        (clear_omitted_keys),
        (presentation_set_duration, 0),
      (else_try),
        (key_clicked, key_1),
        (gt, ":cur_time", 500),
        (multiplayer_send_int_to_server, multiplayer_event_answer_to_poll, 1),
        (clear_omitted_keys),
        (presentation_set_duration, 0),
      (try_end),
      (store_mission_timer_a, ":mission_timer"),
      (store_sub, ":time_left", "$g_multiplayer_poll_client_end_time", ":mission_timer"),
      (try_begin),
        (neq, ":time_left", "$g_multiplayer_poll_last_written_seconds_left"),
        (try_begin),
          (lt, ":time_left", 0),
          (clear_omitted_keys),
          (presentation_set_duration, 0),
        (else_try),
          (assign, "$g_multiplayer_poll_last_written_seconds_left", ":time_left"),
          (assign, reg0, "$g_multiplayer_poll_last_written_seconds_left"),
          (overlay_set_text, "$g_presentation_obj_poll_1", "str_poll_time_left"),
        (try_end),
      (try_end),
      ]),
    ])
