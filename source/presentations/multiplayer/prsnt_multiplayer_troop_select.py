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

multiplayer_troop_select = ("multiplayer_troop_select", prsntf_manual_end_only, 0, [
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
      (create_text_overlay, "$g_presentation_obj_troop_select_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 285),
      (position_set_y, pos1, 125),
      (overlay_set_position, "$g_presentation_obj_troop_select_container", pos1),
      (position_set_x, pos1, 405),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_troop_select_container", pos1),
      (set_container_overlay, "$g_presentation_obj_troop_select_container"),

      (assign, ":cur_y", 450),

      (create_text_overlay, reg0, "str_choose_a_troop", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (val_sub, ":cur_y", escape_menu_item_height),
      (position_set_y, pos1, ":cur_y"),
      (position_set_x, pos1, 100),

      (multiplayer_get_my_player, ":my_player_no"),
      (player_get_team_no, ":my_team_no", ":my_player_no"),
      (team_get_faction, ":my_faction_no", ":my_team_no"),
      (try_for_range, ":i_multi", multi_data_troop_button_indices_begin, multi_data_troop_button_indices_end),
        (troop_set_slot, "trp_multiplayer_data", ":i_multi", -1),
      (try_end),

      (assign, ":cur_troop_index", 0),
      (try_for_range, ":troop_no", multiplayer_troops_begin, multiplayer_troops_end),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":my_faction_no"),
        (str_store_troop_name, s1, ":troop_no"),
        (create_button_overlay, reg0, s1, 0),
        (overlay_set_color, reg0, 0xFFFFFF),
        (store_add, ":button_index_slot", ":cur_troop_index", multi_data_troop_button_indices_begin),
        (troop_set_slot, "trp_multiplayer_data", ":button_index_slot", reg0),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg0, pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
        (position_set_y, pos1, ":cur_y"),
        (val_add, ":cur_troop_index", 1),
      (try_end),
      (presentation_set_duration, 999999),
      ]),

    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (multiplayer_get_my_player, ":my_player_no"),
      (player_get_team_no, ":my_team_no", ":my_player_no"),
      (team_get_faction, ":my_faction_no", ":my_team_no"),
      (assign, ":selected_troop_no", -1),
      (assign, ":end_cond", multi_data_troop_button_indices_end),
      (try_for_range, ":i_button", multi_data_troop_button_indices_begin, ":end_cond"),
        (troop_slot_eq, "trp_multiplayer_data", ":i_button", ":object"),
        (store_sub, ":selected_troop_index", ":i_button", multi_data_troop_button_indices_begin),
        (assign, ":end_cond_2", multiplayer_troops_end),
        (try_for_range, ":troop_no", multiplayer_troops_begin, ":end_cond_2"),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (eq, ":troop_faction", ":my_faction_no"),
          (val_sub, ":selected_troop_index", 1),
          (lt, ":selected_troop_index", 0),
          (assign, ":selected_troop_no", ":troop_no"),
          (assign, ":end_cond_2", 0), #break
        (try_end),
        (try_begin),
          (multiplayer_get_my_troop, ":troop_no"),
          (neq, ":troop_no", ":selected_troop_no"),
          (player_set_troop_id, ":my_player_no", ":selected_troop_no"),
          (multiplayer_send_int_to_server, multiplayer_event_change_troop_id, ":selected_troop_no"),
          (call_script, "script_multiplayer_set_default_item_selections_for_troop", ":selected_troop_no"),
          (call_script, "script_multiplayer_send_item_selections"),
        (try_end),
        (presentation_set_duration, 0),
        (assign, "$g_presentation_state", 0),
        (start_presentation, "prsnt_multiplayer_item_select"),
        (assign, ":end_cond", 0), #break
      (try_end),
      ]),
    (ti_on_presentation_run,
     [
      (try_begin),
        (this_or_next|key_clicked, key_escape),
		(key_clicked, key_xbox_start),
        (multiplayer_get_my_player, ":my_player_no"),
        (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
        (multiplayer_get_my_troop, ":my_troop"),
        (try_begin),
          (neg|is_between, ":my_troop", multiplayer_troops_begin, multiplayer_troops_end),
          (player_set_troop_id, ":my_player_no", -1),
          (multiplayer_send_int_to_server, multiplayer_event_change_troop_id, -1),
          (multiplayer_send_int_to_server, multiplayer_event_change_team_no, multi_team_spectator),
          (player_set_team_no, ":my_player_no", multi_team_spectator),
        (try_end),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ])
