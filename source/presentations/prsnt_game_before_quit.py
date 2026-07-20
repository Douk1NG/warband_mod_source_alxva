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

game_before_quit = ("game_before_quit", 0, mesh_load_window,
   [
     (ti_on_presentation_load,
      [
        (try_begin),
          (is_trial_version),
          (set_fixed_point_multiplier, 1000),
          (create_mesh_overlay, reg0, "mesh_quit_adv"),
          (position_set_x, pos1, -1),
          (position_set_y, pos1, -1),
          (overlay_set_position, reg0, pos1),
          (position_set_x, pos1, 1002),
          (position_set_y, pos1, 1002),
          (overlay_set_size, reg0, pos1),
          (assign, "$g_game_before_quit_state", 0),
          (presentation_set_duration, 999999),
        (try_end),
      ]),
     (ti_on_presentation_run,
       [
        (store_trigger_param_1, ":cur_time"),
        (gt, ":cur_time", 500),
        (try_begin),
          (this_or_next|key_clicked, key_space),
          (this_or_next|key_clicked, key_enter),
          (this_or_next|key_clicked, key_escape),
          (this_or_next|key_clicked, key_back_space),
          (this_or_next|key_clicked, key_left_mouse_button),
          (this_or_next|key_clicked, key_right_mouse_button),
          (this_or_next|key_clicked, key_xbox_ltrigger),
          (key_clicked, key_xbox_rtrigger),
          (try_begin),
            (eq, "$g_game_before_quit_state", 0),
            (val_add, "$g_game_before_quit_state", 1),
            (create_mesh_overlay, reg0, "mesh_quit_adv_b"),
            (position_set_x, pos1, -1),
            (position_set_y, pos1, -1),
            (overlay_set_position, reg0, pos1),
            (position_set_x, pos1, 1002),
            (position_set_y, pos1, 1002),
            (overlay_set_size, reg0, pos1),
          (else_try),
            (presentation_set_duration, 0),
          (try_end),
        (try_end),
        ]),
     ])
