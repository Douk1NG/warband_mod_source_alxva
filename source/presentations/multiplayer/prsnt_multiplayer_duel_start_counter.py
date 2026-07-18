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

multiplayer_duel_start_counter = ("multiplayer_duel_start_counter", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),

      (assign, "$g_multiplayer_duel_start_counter_overlay", -1),
      (assign, "$g_multiplayer_last_duel_start_counter_value", -1),

      (str_clear, s0),
      (create_text_overlay, "$g_multiplayer_duel_start_counter_overlay", s0, tf_center_justify|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_duel_start_counter_overlay", 0xFFFFFF),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 600),
      (overlay_set_position, "$g_multiplayer_duel_start_counter_overlay", pos1),
      (position_set_x, pos1, 2000),
      (position_set_y, pos1, 2000),
      (overlay_set_size, "$g_multiplayer_duel_start_counter_overlay", pos1),

      (presentation_set_duration, 999999),
      ]),

    (ti_on_presentation_run, [
      (ge, "$g_multiplayer_duel_start_counter_overlay", 0),
      (store_mission_timer_a, ":current_time"),
      (store_sub, ":seconds_past_in_duel_start", ":current_time", "$g_multiplayer_duel_start_time"),
      (store_sub, ":seconds_left_in_duel_start", 3, ":seconds_past_in_duel_start"),
      (try_begin),
        (le, ":seconds_left_in_duel_start", 0),
        (presentation_set_duration, 0),
      (else_try),
        (neq, "$g_multiplayer_last_duel_start_counter_value", ":seconds_left_in_duel_start"),
        (assign, "$g_multiplayer_last_duel_start_counter_value", ":seconds_left_in_duel_start"),
        (assign, reg0, ":seconds_left_in_duel_start"),
        (str_store_string, s0, "str_duel_starts_in_reg0_seconds"),
        (overlay_set_text, "$g_multiplayer_duel_start_counter_overlay", s0),
      (try_end),
      ]),
    ])
