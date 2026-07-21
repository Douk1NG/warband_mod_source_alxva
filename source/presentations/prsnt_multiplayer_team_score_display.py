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

multiplayer_team_score_display = ("multiplayer_team_score_display", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),
      (assign, "$g_multiplayer_team_1_last_displayed_score", -1),
      (assign, "$g_multiplayer_team_2_last_displayed_score", -1),
      (str_clear, s0),
      (create_text_overlay, "$g_multiplayer_team_1_score_display_overlay", s0, tf_left_align|tf_single_line|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_team_1_score_display_overlay", 0xFFFFFF),
      (position_set_x, pos1, 40),
      (position_set_y, pos1, 700),
      (overlay_set_position, "$g_multiplayer_team_1_score_display_overlay", pos1),
      (position_set_x, pos1, 1500),
      (position_set_y, pos1, 1500),
      (overlay_set_size, "$g_multiplayer_team_1_score_display_overlay", pos1),
      (create_text_overlay, "$g_multiplayer_team_2_score_display_overlay", s0, tf_left_align|tf_single_line|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_team_2_score_display_overlay", 0xFFFFFF),
      (position_set_x, pos1, 40),
      (position_set_y, pos1, 645),
      (overlay_set_position, "$g_multiplayer_team_2_score_display_overlay", pos1),
      (position_set_x, pos1, 1500),
      (position_set_y, pos1, 1500),
      (overlay_set_size, "$g_multiplayer_team_2_score_display_overlay", pos1),

      (try_begin),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_4"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_1"),
      (else_try),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_2"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_2"),
      (else_try),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_3"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_3"),
      (else_try),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_5"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_4"),
      (else_try),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_6"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_5"),
      (else_try),
        (eq, "$g_multiplayer_team_1_faction", "fac_kingdom_1"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_6"),
      (try_end),

      (position_set_x, pos3, 25),
      (position_set_y, pos3, 715),
      (overlay_set_position, reg0, pos3),
      (position_set_x, pos1, 50),
      (position_set_y, pos1, 50),
      (overlay_set_size, reg0, pos1),

      (try_begin),
        (eq, "$g_multiplayer_team_1_faction", "$g_multiplayer_team_2_faction"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_7"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_4"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_1"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_2"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_2"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_3"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_3"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_5"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_4"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_6"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_5"),
      (else_try),
        (eq, "$g_multiplayer_team_2_faction", "fac_kingdom_1"),
        (create_mesh_overlay, reg0, "mesh_ui_kingdom_shield_6"),
      (try_end),

      (position_set_x, pos3, 25),
      (position_set_y, pos3, 660),
      (overlay_set_position, reg0, pos3),
      (position_set_x, pos1, 50),
      (position_set_y, pos1, 50),
      (overlay_set_size, reg0, pos1),

      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_run, [
      (team_get_score, ":team_1_score", 0),
      (team_get_score, ":team_2_score", 1),
      (try_begin),
        (this_or_next|neq, ":team_1_score", "$g_multiplayer_team_1_last_displayed_score"),
        (neq, ":team_2_score", "$g_multiplayer_team_2_last_displayed_score"),
        (assign, "$g_multiplayer_team_1_last_displayed_score", ":team_1_score"),
        (assign, "$g_multiplayer_team_2_last_displayed_score", ":team_2_score"),

        (str_store_faction_name, s0, "$g_multiplayer_team_1_faction"),
        (assign, reg0, ":team_1_score"),
        (overlay_set_text, "$g_multiplayer_team_1_score_display_overlay", "str_reg0"),
        (str_store_faction_name, s0, "$g_multiplayer_team_2_faction"),
        (assign, reg0, ":team_2_score"),
        (overlay_set_text, "$g_multiplayer_team_2_score_display_overlay", "str_reg0"),

##        (str_store_faction_name, s0, "$g_multiplayer_team_1_faction"),
##        (assign, reg0, ":team_1_score"),
##        (overlay_set_text, "$g_multiplayer_team_1_score_display_overlay", "str_s0_dd_reg0"),
##        (str_store_faction_name, s0, "$g_multiplayer_team_2_faction"),
##        (assign, reg0, ":team_2_score"),
##        (overlay_set_text, "$g_multiplayer_team_2_score_display_overlay", "str_s0_dd_reg0"),
      (try_end),
      ]),
    ])
