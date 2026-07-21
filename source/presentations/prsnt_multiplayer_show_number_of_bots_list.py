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

multiplayer_show_number_of_bots_list = ("multiplayer_show_number_of_bots_list", prsntf_manual_end_only, 0, [
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
      (create_text_overlay, "$g_presentation_obj_show_number_of_bots_list_menu_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 285),
      (position_set_y, pos1, 125),
      (overlay_set_position, "$g_presentation_obj_show_number_of_bots_list_menu_container", pos1),
      (position_set_x, pos1, 405),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_show_number_of_bots_list_menu_container", pos1),
      (set_container_overlay, "$g_presentation_obj_show_number_of_bots_list_menu_container"),

      (assign, ":num_options", 0),
      (store_add, ":end_cond", "$g_multiplayer_num_bots_voteable", 1),
      (try_for_range, ":i_number", 0, ":end_cond"),
        (assign, ":i_number_mod_5", ":i_number"),
        (val_mod, ":i_number_mod_5", 5),
        (this_or_next|lt, ":i_number", 10),
        (eq, ":i_number_mod_5", 0),
        (val_add, ":num_options", 1),
      (try_end),

      (store_mul, ":cur_y", ":num_options", escape_menu_item_height),
      (val_add, ":cur_y", 10),

      (assign, reg0, "$g_multiplayer_number_of_bots_list_action_type"),
      (create_text_overlay, reg0, "str_choose_number_of_bots_for_team_reg0", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (val_sub, ":cur_y", escape_menu_item_height),

      (assign, ":overlay_id", -1),
      (try_for_range, ":i_number", 0, ":end_cond"),
        (assign, ":i_number_mod_5", ":i_number"),
        (val_mod, ":i_number_mod_5", 5),
        (this_or_next|lt, ":i_number", 10),
        (eq, ":i_number_mod_5", 0),
        (assign, reg0, ":i_number"),
        (str_store_string, s0, "str_reg0"),
        (create_button_overlay, ":overlay_id", s0, 0),
        (overlay_set_color, ":overlay_id", 0xFFFFFF),
        (position_set_x, pos1, 100),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, ":overlay_id", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (store_add, "$g_show_number_of_bots_list_button_list_end_index", ":overlay_id", 1),
      (store_sub, "$g_show_number_of_bots_list_button_list_first_index", "$g_show_number_of_bots_list_button_list_end_index", ":num_options"),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (try_for_range, ":i_button", "$g_show_number_of_bots_list_button_list_first_index", "$g_show_number_of_bots_list_button_list_end_index"),
        (eq, ":object", ":i_button"),
        (store_sub, ":value_index", ":object", "$g_show_number_of_bots_list_button_list_first_index"),
        (try_begin),
          (lt, ":value_index", 10),
          (assign, ":used_value", ":value_index"),
        (else_try),
          (store_sub, ":used_value", ":value_index", 8),
          (val_mul, ":used_value", 5),
        (try_end),
        (presentation_set_duration, 0),
        (try_begin),
          (eq, "$g_multiplayer_number_of_bots_list_action_type", 2), #vote for second team
          (try_begin),
            (multiplayer_get_my_player, ":my_player_no"),
            (ge, ":my_player_no", 0),
            (multiplayer_send_3_int_to_server, multiplayer_event_start_new_poll, 4, "$g_multiplayer_poll_number_of_bots_team_1", ":used_value"),
            (store_mission_timer_a, ":mission_timer"),
            (val_add, ":mission_timer", multiplayer_poll_disable_period),
            (player_set_slot, ":my_player_no", slot_player_poll_disabled_until_time, ":mission_timer"),
          (try_end),
        (else_try), #vote for first team
          (assign, "$g_multiplayer_number_of_bots_list_action_type", 2), #for team 2
          (assign, "$g_multiplayer_poll_number_of_bots_team_1", ":used_value"),
          (start_presentation, "prsnt_multiplayer_show_number_of_bots_list"),
        (try_end),
        (assign, "$g_show_number_of_bots_list_button_list_end_index", 0), #break;
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
