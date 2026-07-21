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

check_friendly_kills_scripts = [
("check_friendly_kills",
    [(get_player_agent_own_troop_kill_count, ":count"),
     (try_begin),
       (neq, "$g_player_current_own_troop_kills", ":count"),
       (val_sub, ":count", "$g_player_current_own_troop_kills"),
       (val_add, "$g_player_current_own_troop_kills", ":count"),
       (val_mul, ":count", -1),
       (call_script, "script_change_player_party_morale", ":count"),
     (try_end),
   ])
]
