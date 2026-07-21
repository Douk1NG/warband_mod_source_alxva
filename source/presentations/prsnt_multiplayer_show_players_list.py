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

multiplayer_show_players_list = ("multiplayer_show_players_list", prsntf_manual_end_only, 0, [
    (ti_on_presentation_load,
     [(set_fixed_point_multiplier, 1000),

      (create_mesh_overlay, reg0, "mesh_mp_ingame_menu"),
      (position_set_x, pos1, 250),
      (position_set_y, pos1, 80),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 1000),
      (position_set_y, pos1, 1000),
      (overlay_set_size, reg0, pos1),

      (str_clear, s0),
      (create_text_overlay, "$g_presentation_obj_show_players_1", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 285),
      (position_set_y, pos1, 125),
      (overlay_set_position, "$g_presentation_obj_show_players_1", pos1),
      (position_set_x, pos1, 405),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_show_players_1", pos1),
      (set_container_overlay, "$g_presentation_obj_show_players_1"),

      #(assign, ":cur_y", 450),
      (multiplayer_get_my_player, ":my_player_no"),

      (assign, ":cur_y", 10),
      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 1, ":num_players"), #0 is server no need to write it
        (player_is_active, ":player_no"),

        (assign, ":continue", 0),
        (try_begin),
          (neq, "$g_multiplayer_players_list_action_type", 5),
          (neq, "$g_multiplayer_players_list_action_type", 6),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 5),
          (neq, ":player_no", ":my_player_no"),
          (player_get_is_muted, ":is_muted", ":player_no"),
          (eq, ":is_muted", 0),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 6),
          (neq, ":player_no", ":my_player_no"),
          (player_get_is_muted, ":is_muted", ":player_no"),
          (eq, ":is_muted", 1),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),

        (val_add, ":cur_y", escape_menu_item_height),
      (try_end),

      (create_text_overlay, reg0, "str_choose_a_player", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (val_sub, ":cur_y", escape_menu_item_height),

      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 1, ":num_players"), #0 is server no need to write it
        (player_is_active, ":player_no"),
        (player_set_slot, ":player_no", slot_player_button_index, -1),

        (assign, ":continue", 0),
        (try_begin),
          (neq, "$g_multiplayer_players_list_action_type", 5),
          (neq, "$g_multiplayer_players_list_action_type", 6),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 5),
          (neq, ":player_no", ":my_player_no"),
          (player_get_is_muted, ":is_muted", ":player_no"),
          (eq, ":is_muted", 0),
          (assign, ":continue", 1),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 6),
          (neq, ":player_no", ":my_player_no"),
          (player_get_is_muted, ":is_muted", ":player_no"),
          (eq, ":is_muted", 1),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (str_store_player_username, s0, ":player_no"),

        (create_button_overlay, ":overlay_id", s0, 0),
        (overlay_set_color, ":overlay_id", 0xFFFFFF),
        (position_set_x, pos1, 130),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, ":overlay_id", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
        (player_set_slot, ":player_no", slot_player_button_index, ":overlay_id"),
      (try_end),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 1, ":num_players"), #0 is server no need to write it
        (player_is_active, ":player_no"),
        (player_slot_eq, ":player_no", slot_player_button_index, ":object"),
        (try_begin),
          (is_between, "$g_multiplayer_players_list_action_type", 1, 3), #poll kick or poll ban
          (try_begin),
            (multiplayer_get_my_player, ":my_player_no"),
            (ge, ":my_player_no", 0),
            (multiplayer_send_2_int_to_server, multiplayer_event_start_new_poll, "$g_multiplayer_players_list_action_type", ":player_no"),
            (store_mission_timer_a, ":mission_timer"),
            (val_add, ":mission_timer", multiplayer_poll_disable_period),
            (player_set_slot, ":my_player_no", slot_player_poll_disabled_until_time, ":mission_timer"),
          (try_end),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 3), #admin kick
          (multiplayer_send_int_to_server, multiplayer_event_admin_kick_player, ":player_no"),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 4), #admin ban
          (multiplayer_send_int_to_server, multiplayer_event_admin_ban_player, ":player_no"),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 5), #mute player
          (player_set_is_muted, ":player_no", 1),
        (else_try),
          (eq, "$g_multiplayer_players_list_action_type", 6), #unmute player
          (player_set_is_muted, ":player_no", 0),
        (try_end),
        (assign, ":num_players", 0), #break
        (presentation_set_duration, 0),
      (try_end),
      ]),
    (ti_on_presentation_run,
     [(store_trigger_param_1, ":cur_time"),
      (try_begin),
        (this_or_next|key_clicked, key_escape),
		(key_clicked, key_xbox_start),
        (gt, ":cur_time", 200),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ])
