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

tutorial_show_mouse_movement = ("tutorial_show_mouse_movement",prsntf_read_only|prsntf_manual_end_only,0,[
      (ti_on_presentation_load,
       [
         (try_begin),
           (this_or_next|eq, "$g_tutorial_mouse_dir", -1),
           (eq, "$g_tutorial_mouse_click", -1),
           (presentation_set_duration, 0),
         (else_try),
           (set_fixed_point_multiplier, 1000),
           (assign, "$g_tutorial_displayed_mouse_dir", "$g_tutorial_mouse_dir"),
           (assign, "$g_tutorial_displayed_mouse_click", "$g_tutorial_mouse_click"),
           (store_add, ":arrow_mesh", "$g_tutorial_mouse_dir", "mesh_mouse_arrow_down"),
           (create_mesh_overlay, reg0, ":arrow_mesh"),
           (position_set_x, pos1, 800),
           (position_set_y, pos1, 800),
           (overlay_set_size, reg0, pos1),
           (position_set_x, pos1, 380),
           (position_set_y, pos1, 500),
           (overlay_set_position, reg0, pos1),
           (try_begin),
             (eq, "$g_tutorial_mouse_click", 0),
             (create_mesh_overlay, reg0, "mesh_mouse_left_click"),
           (else_try),
             (create_mesh_overlay, reg0, "mesh_mouse_right_click"),
           (try_end),
           (position_set_x, pos1, 800),
           (position_set_y, pos1, 800),
           (overlay_set_size, reg0, pos1),
           (position_set_x, pos1, 540),
           (position_set_y, pos1, 500),
           (overlay_set_position, reg0, pos1),
           (create_mesh_overlay, reg0, "mesh_mouse_arrow_plus"),
           (overlay_set_color, reg0, 0xFFFFFF),
           (position_set_x, pos1, 600),
           (position_set_y, pos1, 600),
           (overlay_set_size, reg0, pos1),
           (position_set_x, pos1, 470),
           (position_set_y, pos1, 510),
           (overlay_set_position, reg0, pos1),
           (presentation_set_duration, 999999),
         (try_end),
        ]),
      (ti_on_presentation_run,
       [(try_begin),
          (this_or_next|neq, "$g_tutorial_displayed_mouse_dir", "$g_tutorial_mouse_dir"),
          (neq, "$g_tutorial_displayed_mouse_click", "$g_tutorial_mouse_click"),
          (presentation_set_duration, 0),
          (try_begin),
            (ge, "$g_tutorial_mouse_dir", 0),
            (ge, "$g_tutorial_mouse_click", 0),
            (start_presentation, "prsnt_tutorial_show_mouse_movement"),
          (try_end),
        (try_end),
        ]),
      ])
