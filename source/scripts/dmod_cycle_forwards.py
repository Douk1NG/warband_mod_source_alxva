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

dmod_cycle_forwards_scripts = [
("dmod_cycle_forwards",[

         (assign, ":agent_moved", 0),
         (assign, ":first_agent", -1),
         # (get_player_agent_no, ":player_agent"),
         # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_moved", 1),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            # (agent_get_team, ":cur_team", ":agent_no"),
            # (this_or_next|eq, ":cur_team", 5), #bodyguards
            # (eq, ":cur_team", ":player_team"),
            (try_begin),
              (lt, ":first_agent", 0),
              (assign, ":first_agent", ":agent_no"),
            (try_end),
            (gt, ":agent_no", "$dmod_current_agent"),
            (assign, "$dmod_current_agent", ":agent_no"),
            (assign, ":agent_moved", 1),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 0),
            (neq, ":first_agent", -1),
            (assign, "$dmod_current_agent", ":first_agent"),
            (assign, ":agent_moved", 1),
        (else_try),
            (eq, ":agent_moved", 0),
            (eq, ":first_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 1),
            (str_store_agent_name, s1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      #(assign, "$dmod_move_camera", 1),
      ])
]
