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

multiplayer_poll_menu = ("multiplayer_poll_menu", prsntf_manual_end_only, 0, [
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
      (create_text_overlay, "$g_presentation_obj_poll_menu_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 285),
      (position_set_y, pos1, 125),
      (overlay_set_position, "$g_presentation_obj_poll_menu_container", pos1),
      (position_set_x, pos1, 405),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_poll_menu_container", pos1),
      (set_container_overlay, "$g_presentation_obj_poll_menu_container"),

      (assign, "$g_presentation_obj_poll_menu_1", -1),
      (assign, "$g_presentation_obj_poll_menu_4", -1),
      (assign, "$g_presentation_obj_poll_menu_5", -1),

      (assign, ":cur_y", 450),

      (create_text_overlay, reg0, "str_choose_a_poll_type", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (val_sub, ":cur_y", escape_menu_item_height),

      (position_set_x, pos1, 60),

      (try_begin),
        (eq, "$g_multiplayer_maps_voteable", 1),
        (create_button_overlay, "$g_presentation_obj_poll_menu_1", "str_poll_for_changing_the_map", 0),
        (overlay_set_color, "$g_presentation_obj_poll_menu_1", 0xFFFFFF),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, "$g_presentation_obj_poll_menu_1", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (try_begin),
        (eq, "$g_multiplayer_factions_voteable", 1),
        (create_button_overlay, "$g_presentation_obj_poll_menu_4", "str_poll_for_changing_the_map_and_factions", 0),
        (overlay_set_color, "$g_presentation_obj_poll_menu_4", 0xFFFFFF),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, "$g_presentation_obj_poll_menu_4", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (try_begin),
        (gt, "$g_multiplayer_num_bots_voteable", 0),
        (create_button_overlay, "$g_presentation_obj_poll_menu_5", "str_poll_for_changing_number_of_bots", 0),
        (overlay_set_color, "$g_presentation_obj_poll_menu_5", 0xFFFFFF),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, "$g_presentation_obj_poll_menu_5", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (try_begin),
        (eq, "$g_multiplayer_kick_voteable", 1),
        (create_button_overlay, "$g_presentation_obj_poll_menu_2", "str_poll_for_kicking_a_player", 0),
        (overlay_set_color, "$g_presentation_obj_poll_menu_2", 0xFFFFFF),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, "$g_presentation_obj_poll_menu_2", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (try_begin),
        (eq, "$g_multiplayer_ban_voteable", 1),
        (create_button_overlay, "$g_presentation_obj_poll_menu_3", "str_poll_for_banning_a_player", 0),
        (overlay_set_color, "$g_presentation_obj_poll_menu_3", 0xFFFFFF),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, "$g_presentation_obj_poll_menu_3", pos1),
      (try_end),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (try_begin),
        (eq, ":object", "$g_presentation_obj_poll_menu_1"),
        (presentation_set_duration, 0),
        (assign, "$g_multiplayer_maps_list_action_type", 1), #poll map
        (start_presentation, "prsnt_multiplayer_show_maps_list"),
      (else_try),
        (eq, ":object", "$g_presentation_obj_poll_menu_2"),
        (presentation_set_duration, 0),
        (assign, "$g_multiplayer_players_list_action_type", 1), #poll kick
        (start_presentation, "prsnt_multiplayer_show_players_list"),
      (else_try),
        (eq, ":object", "$g_presentation_obj_poll_menu_3"),
        (presentation_set_duration, 0),
        (assign, "$g_multiplayer_players_list_action_type", 2), #poll ban
        (start_presentation, "prsnt_multiplayer_show_players_list"),
      (else_try),
        (eq, ":object", "$g_presentation_obj_poll_menu_4"),
        (presentation_set_duration, 0),
        (assign, "$g_multiplayer_maps_list_action_type", 2), #poll map and factions
        (start_presentation, "prsnt_multiplayer_show_maps_list"),
      (else_try),
        (eq, ":object", "$g_presentation_obj_poll_menu_5"),
        (presentation_set_duration, 0),
        (assign, "$g_multiplayer_number_of_bots_list_action_type", 1), #for team 1
        (start_presentation, "prsnt_multiplayer_show_number_of_bots_list"),
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
