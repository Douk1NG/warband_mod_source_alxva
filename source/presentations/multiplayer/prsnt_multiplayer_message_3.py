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

multiplayer_message_3 = ("multiplayer_message_3", prsntf_read_only|prsntf_manual_end_only, 0, [
    (ti_on_presentation_load, [
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, "$g_multiplayer_message_type", multiplayer_message_type_poll_result),

        (assign, ":text_font_color", 0xFFFFFFFF),
        (try_begin),
          (eq, "$g_multiplayer_message_value_3", 1),
          (str_store_string, s0, "str_poll_result_yes"),
        (else_try),
          (str_store_string, s0, "str_poll_result_no"),
        (try_end),
        (create_text_overlay, "$g_multiplayer_message_3", s0, tf_center_justify|tf_with_outline),
        (overlay_set_color, "$g_multiplayer_message_3", ":text_font_color"),
        (position_set_x, pos1, 380),
        (position_set_x, pos1, 500), #new
        (position_set_y, pos1, 475),
        (overlay_set_position, "$g_multiplayer_message_3", pos1),
        (position_set_x, pos1, 2000),
        (position_set_y, pos1, 2000),
        (overlay_set_size, "$g_multiplayer_message_3", pos1),
        (presentation_set_duration, 400),
      (try_end),
      ]),
    (ti_on_presentation_run,
     [
       ]),
     ])
