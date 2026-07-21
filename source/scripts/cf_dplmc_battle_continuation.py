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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

cf_dplmc_battle_continuation_scripts = [
##diplomacy end+
#new camera setup scripts, setting up other calls
("cf_dplmc_battle_continuation", [
    (eq, "$g_dplmc_battle_continuation", 0),
    (assign, ":num_allies", 0),
    (try_for_agents, ":agent"),
      (agent_is_ally, ":agent"),
      (agent_is_alive, ":agent"),
      (val_add, ":num_allies", 1),
    (try_end),
    (gt, ":num_allies", 0),
    (try_begin),
      (eq, "$g_dplmc_cam_activated", 0),
      #(store_mission_timer_a, "$g_dplmc_main_hero_fallen_seconds"),
      (assign, "$g_dplmc_cam_activated", "$g_dplmc_cam_default"),

      (display_message, "@You have been knocked out by the enemy. Watch your men continue the fight without you or press Tab to retreat."),
      (store_add, ":string", "$g_dplmc_cam_activated", "str_camera_keyboard"),
      (val_sub, ":string", 1),
      (display_message, ":string"),
      # (display_message, "@To watch the fight you can use 'w, a, s, d, numpad_+/numpad_-' to move and 'numpad_1,2,3,4,6,8' to rotate the cam."),

      (try_begin), #http://forums.taleworlds.com/index.php/topic,322343.0.html
        (eq, "$g_dplmc_charge_when_dead", 1),
        (get_player_agent_no, ":player_agent"),
        (agent_get_team, ":player_team", ":player_agent"),
        (set_show_messages, 0),
        (team_give_order, ":player_team", grc_everyone, mordr_charge),
        (team_give_order, ":player_team", grc_everyone, mordr_use_any_weapon),
        (team_give_order, ":player_team", grc_everyone, mordr_fire_at_will),
        (set_show_messages, 1),
      (try_end),

      (mission_cam_get_position, pos1), #Death pos
      (position_get_rotation_around_z, ":rot_z", pos1),

      (init_position, pos47),
      (position_copy_origin, pos47, pos1), #Copy X,Y,Z pos
      (position_rotate_z, pos47, ":rot_z"), #Copying X-Rotation is likely possible, but I haven't figured it out yet

      (mission_cam_set_mode, 1, 0, 0), #Manual?

      (try_begin), #auto-assign the closest agent
        (eq, "$g_dplmc_cam_activated", camera_follow),
        (call_script, "script_dmod_closest_agent"),
      (try_end),

      (mission_cam_set_position, pos47),
    (try_end),
    ])
]
