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

multiplayer_show_maps_list = ("multiplayer_show_maps_list", prsntf_manual_end_only, 0, [
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
      (create_text_overlay, "$g_presentation_obj_show_maps_list_menu_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 285),
      (position_set_y, pos1, 125),
      (overlay_set_position, "$g_presentation_obj_show_maps_list_menu_container", pos1),
      (position_set_x, pos1, 405),
      (position_set_y, pos1, 500),
      (overlay_set_area_size, "$g_presentation_obj_show_maps_list_menu_container", pos1),
      (set_container_overlay, "$g_presentation_obj_show_maps_list_menu_container"),

      (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
      (assign, ":num_maps", reg0),
      (store_mul, ":cur_y", ":num_maps", escape_menu_item_height),
      (val_add, ":cur_y", 10),

      (create_text_overlay, reg0, "str_choose_a_map", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, 0),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (val_sub, ":cur_y", escape_menu_item_height),

      (assign, ":overlay_id", -1),
      (try_for_range, ":i_map", 0, ":num_maps"),
        (store_add, ":map_slot", ":i_map", multi_data_maps_for_game_type_begin),
        (troop_get_slot, ":map_no", "trp_multiplayer_data", ":map_slot"),
        (store_sub, ":string_index", ":map_no", multiplayer_scenes_begin),
        (val_add, ":string_index", multiplayer_scene_names_begin),
        (str_store_string, s0, ":string_index"),

        (create_button_overlay, ":overlay_id", s0, 0),
        (overlay_set_color, ":overlay_id", 0xFFFFFF),
        (position_set_x, pos1, 100),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, ":overlay_id", pos1),
        (val_sub, ":cur_y", escape_menu_item_height),
      (try_end),
      (store_add, "$g_show_maps_list_button_list_end_index", ":overlay_id", 1),
      (store_sub, "$g_show_maps_list_button_list_first_index", "$g_show_maps_list_button_list_end_index", ":num_maps"),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_event_state_change,
     [(store_trigger_param_1, ":object"),
      (try_for_range, ":i_button", "$g_show_maps_list_button_list_first_index", "$g_show_maps_list_button_list_end_index"),
        (eq, ":object", ":i_button"),
        (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
        (store_sub, ":map_slot", ":object", "$g_show_maps_list_button_list_first_index"),
        (val_add, ":map_slot", multi_data_maps_for_game_type_begin),
        (troop_get_slot, ":scene_id", "trp_multiplayer_data", ":map_slot"),
        (presentation_set_duration, 0),
        (try_begin),
          (eq, "$g_multiplayer_maps_list_action_type", 1), #vote for map
          (try_begin),
            (multiplayer_get_my_player, ":my_player_no"),
            (ge, ":my_player_no", 0),
            (multiplayer_send_2_int_to_server, multiplayer_event_start_new_poll, 0, ":scene_id"),
            (store_mission_timer_a, ":mission_timer"),
            (val_add, ":mission_timer", multiplayer_poll_disable_period),
            (player_set_slot, ":my_player_no", slot_player_poll_disabled_until_time, ":mission_timer"),
          (try_end),
        (else_try), #vote for map and factions
          (assign, "$g_multiplayer_factions_list_action_type", 1), #for team 1
          (assign, "$g_multiplayer_poll_for_map_and_faction_data_map", ":scene_id"),
          (start_presentation, "prsnt_multiplayer_show_factions_list"),
        (try_end),
        (assign, "$g_show_maps_list_button_list_end_index", 0), #break;
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
