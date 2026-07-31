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



#Zaitenko's Reinforcement Script

zaitenko_reinforcements_simple_triggers = [
(0.2,  #Every 0.2 game hours will the game check if there are any reinforcements in the centers.
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_reinforcement_party),  #Find parties of the type spt_reinforcement_party
         (party_is_in_any_town, ":party_no"),  # Is the party in any town?
         (party_get_cur_town, ":cur_center", ":party_no"), #What town are they in?
         (call_script, "script_party_add_party_companions", ":cur_center", ":party_no"), #Add the party to the center, which is infact a party ;)
         (party_clear, ":party_no"), #Not sure if this cleaning up is necessary, but it's a precaution so we don't have a bundle of templates lying around.
       (try_end),
    ]),
]
