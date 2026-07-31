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

transfer_mode_reset_triggers = [
(0,0, ti_on_switch_to_map, [],
  [
	   (troop_set_slot, "trp_temp_array_d", slot_adv_transfer_mode, 0),
  ])
]
