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

multiplayer_stats_chart_deathmatch = ("multiplayer_stats_chart_deathmatch", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load,
     [(set_fixed_point_multiplier, 1000),

      (create_mesh_overlay, reg0, "mesh_mp_score_a"),
      (position_set_x, pos1, 295),
      (position_set_y, pos1, 115),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 1000),
      (position_set_y, pos1, 1000),
      (overlay_set_size, reg0, pos1),

      (assign, ":team_rows", 0),
      (assign, ":spectator_rows", 0),
      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 0, ":num_players"),
        (store_add, ":slot_index", ":player_no", multi_data_player_index_list_begin),
        (try_begin),
          (player_is_active, ":player_no"),
          (troop_set_slot, "trp_multiplayer_data", ":slot_index", 1),
          (player_get_team_no, ":player_team", ":player_no"),
          (try_begin),
            (this_or_next|eq, ":player_team", 0),
            (eq, ":player_team", 1),
            (val_add, ":team_rows", 1),
          (else_try),
            (eq, ":player_team", multi_team_spectator),
            (val_add, ":spectator_rows", 1),
          (try_end),
        (else_try),
          (troop_set_slot, "trp_multiplayer_data", ":slot_index", 0),
        (try_end),
      (try_end),
      (try_begin),
        (this_or_next|gt, "$g_multiplayer_num_bots_team_1", 0),
        (gt, "$g_multiplayer_num_bots_team_2", 0),
        (val_add, ":team_rows", 1),
      (try_end),

      (store_add, ":total_rows", ":team_rows", ":spectator_rows"),

      (str_clear, s0),
      (create_text_overlay, "$g_presentation_obj_stats_chart_deathmatch_container", s0, tf_scrollable_style_2),
      (position_set_x, pos1, 300),
      (position_set_y, pos1, 140),
      (overlay_set_position, "$g_presentation_obj_stats_chart_deathmatch_container", pos1),
      (position_set_x, pos1, 346),
      (position_set_y, pos1, 530),
      (overlay_set_area_size, "$g_presentation_obj_stats_chart_deathmatch_container", pos1),
      (set_container_overlay, "$g_presentation_obj_stats_chart_deathmatch_container"),

      (store_mul, ":y_needed", ":total_rows", 20),
      (val_add, ":y_needed", 80),
      (try_begin),
        (gt, ":spectator_rows", 0),
        (val_add, ":y_needed", 70),
      (try_end),

      (try_begin),
        (ge, ":total_rows", 17),
        (assign, "$g_stats_chart_update_period", 10),
      (else_try),
        (assign, "$g_stats_chart_update_period", 1),
      (try_end),

      (multiplayer_get_my_player, ":my_player_no"),

      #assuming only 2 teams in scene
      (assign, ":cur_y", ":y_needed"),
      (assign, ":cur_x", 42),

      (create_text_overlay, reg0, "str_player_name", 0),
      (overlay_set_color, reg0, 0xFFFFFF),
      (position_set_x, pos1, ":cur_x"),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 750),
      (position_set_y, pos1, 750),
      (overlay_set_size, reg0, pos1),

      (create_text_overlay, reg0, "str_kills", tf_center_justify),
      (overlay_set_color, reg0, 0xFFFFFF),
      (store_add, ":sub_cur_x", ":cur_x", 179), #164
      (position_set_x, pos1, ":sub_cur_x"),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 750),
      (position_set_y, pos1, 750),
      (overlay_set_size, reg0, pos1),

      (create_text_overlay, reg0, "str_deaths", tf_center_justify),
      (overlay_set_color, reg0, 0xFFFFFF),
      (store_add, ":sub_cur_x", ":cur_x", 233), #205
      (position_set_x, pos1, ":sub_cur_x"),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 750),
      (position_set_y, pos1, 750),
      (overlay_set_size, reg0, pos1),

      (create_text_overlay, reg0, "str_ping", tf_center_justify),
      (overlay_set_color, reg0, 0xFFFFFF),
      (store_add, ":sub_cur_x", ":cur_x", 282), #264
      (position_set_x, pos1, ":sub_cur_x"),
      (position_set_y, pos1, ":cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 750),
      (position_set_y, pos1, 750),
      (overlay_set_size, reg0, pos1),

      (create_mesh_overlay, reg0, "mesh_white_plane"),
      (overlay_set_color, reg0, 0xFFFFFF),
      (overlay_set_alpha, reg0, 0xD0),
      (store_add, ":sub_cur_x", ":cur_x", 0),
      (position_set_x, pos1, ":sub_cur_x"),
      (store_add, ":sub_cur_y", ":cur_y", -10),
      (position_set_y, pos1, ":sub_cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 15250),
      (position_set_y, pos1, 50),
      (overlay_set_size, reg0, pos1),

      (val_sub, ":cur_y", 35),

      (store_add, ":end_cond", ":num_players", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (assign, ":max_score_plus_death", -30030),
        (assign, ":max_kills_player_no", -1),
        (try_for_range, ":player_no", 0, ":num_players"),
          (store_add, ":slot_index", ":player_no", multi_data_player_index_list_begin),
          (troop_slot_eq, "trp_multiplayer_data", ":slot_index", 1),
          (player_get_team_no, ":player_team", ":player_no"),
          (this_or_next|eq, ":player_team", 0),
          (eq, ":player_team", 1),

          (player_get_kill_count, ":kill_count", ":player_no"),
          (player_get_death_count, ":death_count", ":player_no"), #get_death_count
          (store_mul, ":player_score_plus_death", ":kill_count", 1000),
          (val_sub, ":player_score_plus_death", ":death_count"),

          (this_or_next|gt, ":player_score_plus_death", ":max_score_plus_death"),
          (eq, ":player_score_plus_death", -30030),

          (assign, ":max_score_plus_death", ":player_score_plus_death"),
          (assign, ":max_kills_player_no", ":player_no"),
        (try_end),
        (try_begin),
          (ge, ":max_kills_player_no", 0),
          (store_add, ":slot_index", ":max_kills_player_no", multi_data_player_index_list_begin),
          (troop_set_slot, "trp_multiplayer_data", ":slot_index", 0),
          (str_store_player_username, s1, ":max_kills_player_no"),

          (try_begin),
            (eq, ":my_player_no", ":max_kills_player_no"),
            (create_mesh_overlay, reg0, "mesh_white_plane"),
            (overlay_set_color, reg0, 0xFFFFFF),
            (overlay_set_alpha, reg0, 0x35),
            (store_add, ":sub_cur_x", ":cur_x", 0),
            (position_set_x, pos1, ":sub_cur_x"),
            (store_add, ":sub_cur_y", ":cur_y", 0),
            (position_set_y, pos1, ":sub_cur_y"),
            (overlay_set_position, reg0, pos1),
            (position_set_x, pos1, 16000),
            (position_set_y, pos1, 1000),
            (overlay_set_size, reg0, pos1),
          (try_end),

          (create_text_overlay, reg0, s1, 0),
          (overlay_set_color, reg0, 0xFFFFFF),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (position_set_x, pos1, ":cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (player_get_kill_count, reg0, ":max_kills_player_no"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, 0xFFFFFF),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 188), #173
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (player_get_death_count, reg0, ":max_kills_player_no"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, 0xFFFFFF),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 238), #223
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (player_get_ping, reg0, ":max_kills_player_no"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, 0xFFFFFF),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 288), #273
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),
          (val_sub, ":cur_y", 20),
        (else_try),
          (store_add, ":number_of_bots", "$g_multiplayer_num_bots_team_1", "$g_multiplayer_num_bots_team_2"),
          (ge, ":number_of_bots", 1),

          (try_begin),
            (gt, ":number_of_bots", 1),
            (assign, reg0, ":number_of_bots"),
            (create_text_overlay, reg0, "str_bots_reg0_agents", 0),
          (else_try),
            (create_text_overlay, reg0, "str_bot_1_agent", 0),
          (try_end),

          (overlay_set_color, reg0, 0xD0D0D0),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (position_set_x, pos1, ":cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (team_get_bot_kill_count, reg0, 0),
          (assign, ":bot_kill_count", reg0),
          (team_get_bot_kill_count, reg0, 1),
          (val_add, ":bot_kill_count", reg0),
          (assign, reg0, ":bot_kill_count"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, 0xD0D0D0),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 188), #173
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (team_get_bot_death_count, reg0, 0),
          (assign, ":bot_death_count", reg0),
          (team_get_bot_death_count, reg0, 1),
          (val_add, ":bot_death_count", reg0),
          (assign, reg0, ":bot_death_count"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, 0xD0D0D0),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 238), #223
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),
          (val_sub, ":cur_y", 20),

          (assign, ":end_cond", 0), #all players are written, break
        (else_try),
          (assign, ":end_cond", 0), #all players are written, break
        (try_end),
      (try_end),

      (assign, ":cur_x", 42),

      #white line between playing players and spectators
      (create_mesh_overlay, reg0, "mesh_white_plane"),
      (overlay_set_color, reg0, 0xFFFFFF),
      (overlay_set_alpha, reg0, 0xD0),
      (store_add, ":sub_cur_x", ":cur_x", 0),
      (position_set_x, pos1, ":sub_cur_x"),
      (store_add, ":sub_cur_y", ":cur_y", 10),
      (position_set_y, pos1, ":sub_cur_y"),
      (overlay_set_position, reg0, pos1),
      (position_set_x, pos1, 15250),
      (position_set_y, pos1, 50),
      (overlay_set_size, reg0, pos1),

      (try_begin),
        (gt, ":spectator_rows", 0),

        (assign, ":cur_x", 75),
        (val_sub, ":cur_y", 50),

        #"spectators" text
        (create_text_overlay, reg0, "str_spectators", 0),
        (overlay_set_color, reg0, 0xFFFFFF),
        (position_set_x, pos1, ":cur_x"),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 1000),
        (position_set_y, pos1, 1000),
        (overlay_set_size, reg0, pos1),

        (create_text_overlay, reg0, "str_ping", tf_center_justify),
        (overlay_set_color, reg0, 0xFFFFFF),
        (store_add, ":sub_cur_x", ":cur_x", 218), #200
        (position_set_x, pos1, ":sub_cur_x"),
        (position_set_y, pos1, ":cur_y"),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg0, pos1),

        #white line for spectators list
        (create_mesh_overlay, reg0, "mesh_white_plane"),
        (overlay_set_color, reg0, 0xFFFFFF),
        (overlay_set_alpha, reg0, 0xD0),
        (store_add, ":sub_cur_x", ":cur_x", 0),
        (position_set_x, pos1, ":sub_cur_x"),
        (store_add, ":sub_cur_y", ":cur_y", -10),
        (position_set_y, pos1, ":sub_cur_y"),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 12000),
        (position_set_y, pos1, 50),
        (overlay_set_size, reg0, pos1),

        (val_sub, ":cur_y", 30),

        (assign, ":font_color", 0xC0C0C0),

        (store_add, ":end_cond", ":num_players", 1),
        (try_for_range, ":player_no", 0, ":end_cond"),
          (store_add, ":slot_index", ":player_no", multi_data_player_index_list_begin),
          (troop_slot_eq, "trp_multiplayer_data", ":slot_index", 1),

          (player_get_team_no, ":player_team", ":player_no"),
          (eq, ":player_team", multi_team_spectator), #to not to allow dedicated server to pass below, dedicated servers have -1 for team_no not 2(multi_team_spectator).

          (troop_set_slot, "trp_multiplayer_data", ":slot_index", 1),

          (try_begin),
            (eq, ":my_player_no", ":player_no"),
            (create_mesh_overlay, reg0, "mesh_white_plane"),
            (overlay_set_color, reg0, 0xFFFFFF),
            (overlay_set_alpha, reg0, 0x35),
            (store_add, ":sub_cur_x", ":cur_x", 0),
            (position_set_x, pos1, ":sub_cur_x"),
            (store_add, ":sub_cur_y", ":cur_y", 0),
            (position_set_y, pos1, ":sub_cur_y"),
            (overlay_set_position, reg0, pos1),
            (position_set_x, pos1, 12000), #16500
            (position_set_y, pos1, 1000),
            (overlay_set_size, reg0, pos1),
          (try_end),

          (str_store_player_username, s1, ":player_no"),
          (create_text_overlay, reg0, s1, 0),
          (overlay_set_color, reg0, ":font_color"),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (position_set_x, pos1, ":cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),

          (player_get_ping, reg0, ":player_no"),
          (create_text_overlay, reg0, "str_reg0", tf_right_align),
          (overlay_set_color, reg0, ":font_color"),
          (position_set_x, pos1, 750),
          (position_set_y, pos1, 750),
          (overlay_set_size, reg0, pos1),
          (store_add, ":sub_cur_x", ":cur_x", 215), #200
          (position_set_x, pos1, ":sub_cur_x"),
          (position_set_y, pos1, ":cur_y"),
          (overlay_set_position, reg0, pos1),
          (val_sub, ":cur_y", 20),
        (try_end),
      (try_end),

      (omit_key_once, key_mouse_scroll_up),
      (omit_key_once, key_mouse_scroll_down),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_run,
     [(store_trigger_param_1, ":cur_time"),
      (try_begin),
        (this_or_next|key_clicked, key_mouse_scroll_up),
        (key_clicked, key_mouse_scroll_down),
        (omit_key_once, key_mouse_scroll_up),
        (omit_key_once, key_mouse_scroll_down),
      (try_end),
      (try_begin),
        (eq, "$g_multiplayer_stats_chart_opened_manually", 1),
        (neg|game_key_is_down, gk_leave),
        (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
        (clear_omitted_keys),
        (presentation_set_duration, 0),
      (try_end),
      (try_begin),
        (store_mul, ":update_period_time_limit", "$g_stats_chart_update_period", 1000),
        (gt, ":cur_time", ":update_period_time_limit"),
        (clear_omitted_keys),
        (presentation_set_duration, 0),
        (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
      (try_end),
      ]),
    ])
