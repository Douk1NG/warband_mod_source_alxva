# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

multiplayer_init_mission_variables_scripts = [
#script_multiplayer_init_mission_variables
("multiplayer_init_mission_variables",
   [
     (assign, "$g_multiplayer_team_1_first_spawn", 1),
     (assign, "$g_multiplayer_team_2_first_spawn", 1),
     (assign, "$g_multiplayer_poll_running", 0),
##     (assign, "$g_multiplayer_show_poll_when_suitable", 0),
     (assign, "$g_waiting_for_confirmation_to_terminate", 0),
     (assign, "$g_confirmation_result", 0),
     (assign, "$g_team_balance_next_round", 0),
     (team_get_faction, "$g_multiplayer_team_1_faction", 0),
     (team_get_faction, "$g_multiplayer_team_2_faction", 1),
     (assign, "$g_multiplayer_next_team_1_faction", "$g_multiplayer_team_1_faction"),
     (assign, "$g_multiplayer_next_team_2_faction", "$g_multiplayer_team_2_faction"),

     (assign, "$g_multiplayer_bot_type_1_wanted", 0),
     (assign, "$g_multiplayer_bot_type_2_wanted", 0),
     (assign, "$g_multiplayer_bot_type_3_wanted", 0),
     (assign, "$g_multiplayer_bot_type_4_wanted", 0),

     (call_script, "script_music_set_situation_with_culture", mtf_sit_multiplayer_fight),
     ])
]
