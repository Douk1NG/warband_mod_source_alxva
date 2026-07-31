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



#This trigger makes sure that no village is left reserved forever.

village_reservation_simple_triggers = [
(12,
   [
   (try_for_range, ":village", villages_begin, villages_end),
      (party_set_slot, ":village", dplmc_slot_village_reserved_by_recruiter, 0),
   (try_end),
   ]),
]
