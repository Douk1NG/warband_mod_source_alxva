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

multiplayer_destructible_targets_display = ("multiplayer_destructible_targets_display", prsntf_read_only|prsntf_manual_end_only, 0, [ #this is for search and destroy death mode flags.
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),

      (try_begin),
        (eq, "$g_defender_team", 0),
        (store_sub, ":flag_mesh", "$g_multiplayer_team_1_faction", npc_kingdoms_begin),
      (else_try),
        (store_sub, ":flag_mesh", "$g_multiplayer_team_2_faction", npc_kingdoms_begin),
      (try_end),

      (val_add, ":flag_mesh", multiplayer_flag_projections_begin),
      (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_1", ":flag_mesh"),
      (create_mesh_overlay, "$g_presentation_obj_flag_projection_display_2", ":flag_mesh"),

      (position_set_x, pos1, 250),
      (position_set_y, pos1, 250),

      (overlay_set_size, "$g_presentation_obj_flag_projection_display_1", pos1),
      (overlay_set_size, "$g_presentation_obj_flag_projection_display_2", pos1),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 0),
      (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_run, [
      (try_begin),
        (eq, "$g_round_ended", 0),
        (set_fixed_point_multiplier, 1000),
        (scene_prop_get_instance, ":target_1_id", "$g_destructible_target_1", 0),
        (prop_instance_get_position, pos1, ":target_1_id"),
        (prop_instance_get_position, pos1, ":target_1_id"),
        (position_move_z, pos1, 250, 1),
        (scene_prop_get_instance, ":target_2_id", "$g_destructible_target_2", 0),
        (prop_instance_get_position, pos2, ":target_2_id"),
        (prop_instance_get_position, pos2, ":target_2_id"),
        (position_move_z, pos2, 250, 1),

        (position_get_screen_projection, pos3, pos1),
        (position_get_x, ":x_pos", pos3),
        (position_get_y, ":y_pos", pos3),
        (position_set_y, pos3, ":y_pos"),
        (try_begin),
          (is_between, ":x_pos", -100, 1100),
          (is_between, ":y_pos", -100, 850),

          (prop_instance_get_starting_position, pos0, ":target_1_id"),
          (prop_instance_get_position, pos1, ":target_1_id"),
          (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
          (le, ":dist", 2), #this can be 0 or 1 too.

          (overlay_set_position, "$g_presentation_obj_flag_projection_display_1", pos3),
          (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 1),
        (else_try),
          (overlay_set_display, "$g_presentation_obj_flag_projection_display_1", 0),
        (try_end),

        (position_get_screen_projection, pos3, pos2),
        (position_get_x, ":x_pos", pos3),
        (position_get_y, ":y_pos", pos3),
        (position_set_y, pos3, ":y_pos"),
        (try_begin),
          (is_between, ":x_pos", -100, 1100),
          (is_between, ":y_pos", -100, 850),

          (prop_instance_get_starting_position, pos0, ":target_2_id"),
          (prop_instance_get_position, pos1, ":target_2_id"),
          (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
          (le, ":dist", 2), #this can be 0 or 1 too.

          (overlay_set_position, "$g_presentation_obj_flag_projection_display_2", pos3),
          (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 1),
        (else_try),
          (overlay_set_display, "$g_presentation_obj_flag_projection_display_2", 0),
        (try_end),
      (else_try),
        (presentation_set_duration, 0),
      (try_end),
      ]),
    ])
