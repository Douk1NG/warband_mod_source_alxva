# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

setup_camera_keys_scripts = [
("setup_camera_keys", [

      # (assign, "$g_dplmc_cam_default", camera_keyboard),
      # (assign, "$g_camera_up", key_w),
      # (assign, "$g_camera_down", key_s),
      # (assign, "$g_camera_left", key_a),
      # (assign, "$g_camera_right", key_d),

      #default custom commander y/z offsets
      (call_script, "script_setup_camera_offset"),
      #these will be retained after being changed inside missions

      #deathcam
      (assign, "$g_cam_tilt_left", key_numpad_1),
      (assign, "$g_cam_tilt_right", key_numpad_3),

      (assign, "$g_camera_adjust_add", key_numpad_plus),
      (assign, "$g_camera_adjust_sub", key_numpad_minus),

      #normally numpad swaps equipment, but we're dead so w/e
      (assign, "$g_camera_rot_up", key_numpad_8),
      (assign, "$g_camera_rot_down", key_numpad_2),
      (assign, "$g_camera_rot_left", key_numpad_4),
      (assign, "$g_camera_rot_right", key_numpad_6),
    ])
]
