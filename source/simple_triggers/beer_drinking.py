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


    #-## TBS - Beer drinking
   

beer_drinking_simple_triggers = [
(1, [
	(troop_get_slot, ":last_beers_time", "trp_player", slot_last_beers_time),
	(store_current_hours, ":cur_hrs"),
	(val_sub, ":cur_hrs", ":last_beers_time"),
	(ge, ":cur_hrs", 18), # If 18 hours have passed since you drank beers
	(troop_set_slot, "trp_player", slot_beers_for_the_day, 0),
   ]),
]
