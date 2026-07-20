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

dmod_cycle_backwards_scripts = [
("dmod_cycle_backwards",[

        (assign, ":new_agent", -1),
        (assign, ":last_agent", -1),
        # (get_player_agent_no, ":player_agent"),
        # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
        # (agent_get_team, ":cur_team", ":agent_no"),
        # (this_or_next|eq, ":cur_team", 5), #bodyguards
        # (eq, ":cur_team", ":player_team"),
            (assign, ":last_agent", ":agent_no"),
            (lt, ":agent_no", "$dmod_current_agent"),
            (assign, ":new_agent", ":agent_no"),
        (try_end),

        (try_begin),
            (eq, ":new_agent", -1),
            (neq, ":last_agent", -1),
            (assign, ":new_agent", ":last_agent"),
        (else_try),
            (eq, ":new_agent", -1),
            (eq, ":last_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (neq, ":new_agent", -1),
            (assign, "$dmod_current_agent", ":new_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      ])
]
