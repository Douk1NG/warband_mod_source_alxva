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

init_death_cam_scripts = [
("init_death_cam",
      [
        (assign, "$deathcam_mouse_last_x", 5000),
        (assign, "$deathcam_mouse_last_y", 3750),
        (assign, "$deathcam_mouse_last_notmoved_x", 5000),
        (assign, "$deathcam_mouse_last_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_x", 5000), #Center screen (10k fixed pos)
        (assign, "$deathcam_mouse_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_counter", 0),

        (assign, "$deathcam_total_rotx", 0),

        (assign, "$deathcam_sensitivity_x", 200), #4:3 ratio may be best
        (assign, "$deathcam_sensitivity_y", 150), #If modified, change values in common_move_deathcam

        (assign, "$deathcam_prsnt_was_active", 0),

        (assign, "$deathcam_keyboard_rotation_x", 0),
        (assign, "$deathcam_keyboard_rotation_y", 0),

        (assign, "$g_dplmc_cam_activated", 0),
        (assign, "$dmod_current_agent", -1),
        # check if keys are not set/invalid
        (try_begin),
          (neg|is_between, "$g_dplmc_cam_default", camera_keyboard, camera_follow + 1),
          (call_script, "script_setup_camera_keys"),
          (assign, "$g_dplmc_cam_default", camera_keyboard),
        (try_end),

        (get_player_agent_no, "$g_player_agent"),
        (agent_get_team, "$g_player_team", "$g_player_agent"),
      ])
]
