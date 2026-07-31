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



    # Decide faction ais
    

process_siege_ai_simple_triggers = [
(6, #it was 23
    [
      (assign, "$g_recalculate_ais", 1),
    ]),
]
