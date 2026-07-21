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

warn_player_about_auto_team_balance_scripts = [
("warn_player_about_auto_team_balance",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
     (start_presentation, "prsnt_multiplayer_message_2"),
     ])
]
