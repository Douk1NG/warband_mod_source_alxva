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

multiplayer_flag_projection_display = ("multiplayer_flag_projection_display", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load,
    [
      (set_fixed_point_multiplier, 1000),

      (store_sub, ":flag_mesh", "$g_multiplayer_team_1_faction", npc_kingdoms_begin),
      (val_add, ":flag_mesh", multiplayer_flag_projections_begin),
      (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_1", ":flag_mesh"),
      (val_sub, ":flag_mesh", multiplayer_flag_projections_begin),
      (val_add, ":flag_mesh", multiplayer_flag_taken_projections_begin),
      (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_2", ":flag_mesh"),

      (try_begin),
        (neq, "$g_multiplayer_team_1_faction", "$g_multiplayer_team_2_faction"),
        (store_sub, ":flag_mesh", "$g_multiplayer_team_2_faction", npc_kingdoms_begin),
        (val_add, ":flag_mesh", multiplayer_flag_projections_begin),
        (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_3", ":flag_mesh"),
        (val_sub, ":flag_mesh", multiplayer_flag_projections_begin),
        (val_add, ":flag_mesh", multiplayer_flag_taken_projections_begin),
        (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_4", ":flag_mesh"),
      (else_try),
        (assign, ":flag_mesh", "mesh_flag_project_rb"),
        (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_3", ":flag_mesh"),
        (assign, ":flag_mesh", "mesh_flag_project_rb_miss"),
        (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_4", ":flag_mesh"),
      (try_end),

      (position_set_x, pos1, 250),
      (position_set_y, pos1, 250),
      (overlay_set_size, "$g_presentation_obj_flag_projection_display_1", pos1),
      (overlay_set_size, "$g_presentation_obj_flag_projection_display_2", pos1),
      (overlay_set_size, "$g_presentation_obj_flag_projection_display_3", pos1),
      (overlay_set_size, "$g_presentation_obj_flag_projection_display_4", pos1),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 0),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_3", 0),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_4", 0),
      (presentation_set_duration, 999999),
      ]),

    (ti_on_presentation_run,
    [
      (set_fixed_point_multiplier, 1000),

      (scene_prop_get_instance, ":flag_red_id", "$team_1_flag_scene_prop", 0),
      (team_get_slot, ":team_0_flag_situation", 0, slot_team_flag_situation),
      (try_begin),
        (neq, ":team_0_flag_situation", 1),
        (prop_instance_get_position, pos1, ":flag_red_id"), #hold position of flag of team 1 (red flag) at pos1
      (else_try),
        (entry_point_get_position, pos1, multi_base_point_team_1), #moved from above to here after auto-set position
      (try_end),
      (position_move_z, pos1, 200, 1),

      (scene_prop_get_instance, ":flag_blue_id", "$team_2_flag_scene_prop", 0),
      (team_get_slot, ":team_1_flag_situation", 1, slot_team_flag_situation),
      (try_begin),
        (neq, ":team_1_flag_situation", 1),
        (prop_instance_get_position, pos2, ":flag_blue_id"), #hold position of flag of team 1 (red flag) at pos1
      (else_try),
        (entry_point_get_position, pos2, multi_base_point_team_2), #moved from above to here after auto-set position
      (try_end),
      (position_move_z, pos2, 200, 1),

      (position_get_screen_projection, pos3, pos1),
      (position_get_x, ":x_pos", pos3),
      (position_get_y, ":y_pos", pos3),
      (position_set_y, pos3, ":y_pos"),
      (try_begin),
        (is_between, ":x_pos", -100, 1100),
        (is_between, ":y_pos", -100, 850),

        (multiplayer_get_my_player, ":my_player_number"),
        (try_begin),
          (ge, ":my_player_number", 0),
          (player_get_team_no, ":my_player_team", ":my_player_number"),
        (else_try),
          (assign, ":my_player_team", multi_team_spectator),
        (try_end),

        (try_begin),
          (neq, ":my_player_team", 1), #if I am at team 0 or spectator
          (try_begin),
            (neq, ":team_0_flag_situation", 1), #if our flag is not stolen
            (overlay_set_position, "$g_presentation_obj_flag_projection_display_1", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
          (else_try), #if our flag is stolen
            (try_begin),
              (eq, ":my_player_team", 0),
              (assign, ":our_base_entry_id", multi_base_point_team_1),
            (else_try),
              (assign, ":our_base_entry_id", multi_base_point_team_2),
            (try_end),

            (entry_point_get_position, pos5, ":our_base_entry_id"), #moved from above to here after auto-set position
            (position_get_screen_projection, pos3, pos5),

            (overlay_set_position, "$g_presentation_obj_flag_projection_display_2", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 0),
          (try_end),
        (else_try),
          (try_begin),
            (neq, ":team_0_flag_situation", 1),
            (overlay_set_position, "$g_presentation_obj_flag_projection_display_1", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
          (try_end),
        (try_end),
      (else_try),
        (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 0),
        (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
      (try_end),

      (position_get_screen_projection, pos3, pos2),
      (position_get_x, ":x_pos", pos3),
      (position_get_y, ":y_pos", pos3),
      (position_set_y, pos3, ":y_pos"),
      (try_begin),
        (is_between, ":x_pos", -100, 1100),
        (is_between, ":y_pos", -100, 850),

        (team_get_slot, ":team_1_flag_situation", 1, slot_team_flag_situation),

        (multiplayer_get_my_player, ":my_player_number"),
        (try_begin),
          (ge, ":my_player_number", 0),
          (player_get_team_no, ":my_player_team", ":my_player_number"),
        (else_try),
          (assign, ":my_player_team", multi_team_spectator),
        (try_end),

        (try_begin),
          (neq, ":my_player_team", 0), #if I am at team 0 or spectator
          (try_begin),
            (neq, ":team_1_flag_situation", 1), #if our flag is not stolen
            (overlay_set_position, "$g_presentation_obj_flag_projection_display_3", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_3", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_4", 0),
          (else_try), #if our flag is stolen
            (try_begin),
              (eq, ":my_player_team", 0),
              (assign, ":our_base_entry_id", multi_base_point_team_1),
            (else_try),
              (assign, ":our_base_entry_id", multi_base_point_team_2),
            (try_end),

            (entry_point_get_position, pos5, ":our_base_entry_id"), #moved from above to here after auto-set position
            (position_get_screen_projection, pos3, pos5),

            (overlay_set_position, "$g_presentation_obj_flag_projection_display_4", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_4", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_3", 0),
          (try_end),
        (else_try),
          (try_begin),
            (neq, ":team_1_flag_situation", 1),
            (overlay_set_position, "$g_presentation_obj_flag_projection_display_3", pos3),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_3", 1),
            (overlay_set_display, "$g_presentation_obj_flag_projection_display_4", 0),
          (try_end),
        (try_end),
      (else_try),
        (overlay_set_display, "$g_presentation_obj_flag_projection_display_3", 0),
        (overlay_set_display, "$g_presentation_obj_flag_projection_display_4", 0),
      (try_end),
      ]),
    ])
