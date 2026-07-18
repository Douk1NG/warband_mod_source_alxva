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

multiplayer_message_2 = ("multiplayer_message_2", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_done),
        (assign, ":text_font_color", 0xFFFFFFFF),
        (str_store_string, s0, "str_auto_team_balance_done"),
        (create_text_overlay, "$g_multiplayer_message_2", s0, tf_center_justify|tf_with_outline),
        (overlay_set_color, "$g_multiplayer_message_2", ":text_font_color"),
        (position_set_x, pos1, 375),
        (position_set_x, pos1, 500), #new
        (position_set_y, pos1, 550),
        (overlay_set_position, "$g_multiplayer_message_2", pos1),
        (position_set_x, pos1, 2000),
        (position_set_y, pos1, 2000),
        (overlay_set_size, "$g_multiplayer_message_2", pos1),
        (presentation_set_duration, 300),
      (else_try),
        (eq, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
        (assign, ":text_font_color", 0xFFFFFFFF),

        (try_begin),
          (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
          (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
          (str_store_string, s0, "str_auto_team_balance_in_20_seconds"),
          (position_set_x, pos1, 375),
        (else_try),
          (str_store_string, s0, "str_auto_team_balance_next_round"),
          (position_set_x, pos1, 375),
        (try_end),

        (create_text_overlay, "$g_multiplayer_message_2", s0, tf_center_justify|tf_with_outline),
        (overlay_set_color, "$g_multiplayer_message_2", ":text_font_color"),
        (position_set_y, pos1, 550),
        (position_set_x, pos1, 500), #new
        (overlay_set_position, "$g_multiplayer_message_2", pos1),
        (position_set_x, pos1, 2000),
        (position_set_y, pos1, 2000),
        (overlay_set_size, "$g_multiplayer_message_2", pos1),
        (presentation_set_duration, 300),
      (try_end),
      ]),
    (ti_on_presentation_run,
     [
       ]),
     ])
