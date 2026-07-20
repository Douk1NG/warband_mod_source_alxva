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

dmod_closest_agent_scripts = [
("dmod_closest_agent", [
          (assign, ":cur_agent", -1),
          (assign, ":distance", 999999),
          (mission_cam_get_position, pos11),
          (position_set_z_to_ground_level, pos11),
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            #position on the ground
            (agent_get_position, pos13, ":agent_no"),
            # (position_get_screen_projection, pos14, pos13),
            # (get_distance_between_positions, ":cur_distance", pos12, pos14),
            (get_distance_between_positions, ":cur_distance", pos11, pos13),
            (lt, ":cur_distance", ":distance"),
            (assign, ":distance", ":cur_distance"),
            (assign, ":cur_agent", ":agent_no"),
          (try_end),
          (try_begin),
            (neq, ":cur_agent", 1),
            (assign, "$dmod_current_agent", ":cur_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
          (try_end),

      ]
    )
]
