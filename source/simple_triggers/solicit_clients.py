# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

solicit_clients_simple_triggers = [
(6, [ # Solicit Clients
       (gt,"$g_currently_soliciting",0),
       (rest_for_hours, 0, 0, 0), #stop resting
       (assign, "$auto_enter_town", "$g_currently_soliciting"),
       (assign, "$quest_auto_menu", "mnu_town_tavern_prostitution"),
       ]
   ),
]
