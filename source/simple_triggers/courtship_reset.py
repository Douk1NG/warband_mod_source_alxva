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



  # Reducing luck by 1 in every 180 hours
  #(180,
   #[
     #(val_sub, "$g_player_luck", 1),
     #(val_max, "$g_player_luck", 0),
    #]),

	#courtship reset
  

courtship_reset_simple_triggers = [
(72,
   [
     (assign, "$lady_flirtation_location", 0),
    ]),
]
