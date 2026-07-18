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

multiplayer_round_time_counter = ("multiplayer_round_time_counter", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),
      (assign, "$g_multiplayer_last_round_time_counter_value", -1),
      (str_clear, s0),
      (create_text_overlay, "$g_multiplayer_round_time_counter_overlay", s0, tf_left_align|tf_single_line|tf_with_outline),
      (overlay_set_color, "$g_multiplayer_round_time_counter_overlay", 0xFFFFFF),
      (position_set_x, pos1, 900),
      (position_set_y, pos1, 690),
      (overlay_set_position, "$g_multiplayer_round_time_counter_overlay", pos1),
      (position_set_x, pos1, 2000),
      (position_set_y, pos1, 2000),
      (overlay_set_size, "$g_multiplayer_round_time_counter_overlay", pos1),
      (presentation_set_duration, 999999),
      ]),
    (ti_on_presentation_run,
     [(store_mission_timer_a, ":current_time"),
      (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
      (store_sub, ":seconds_left_in_round", "$g_multiplayer_round_max_seconds", ":seconds_past_in_round"),
      (val_max, ":seconds_left_in_round", 0),
      (try_begin),
        (neq, "$g_multiplayer_last_round_time_counter_value", ":seconds_left_in_round"),
        (assign, "$g_multiplayer_last_round_time_counter_value", ":seconds_left_in_round"),
        (store_div, reg0, ":seconds_left_in_round", 60),
        (store_div, reg1, ":seconds_left_in_round", 10),
        (val_mod, reg1, 6),
        (assign, reg2, ":seconds_left_in_round"),
        (val_mod, reg2, 10),
        (str_store_string, s0, "str_reg0_dd_reg1reg2"),
        (overlay_set_text, "$g_multiplayer_round_time_counter_overlay", s0),
      (try_end),
      ]),
    ])
