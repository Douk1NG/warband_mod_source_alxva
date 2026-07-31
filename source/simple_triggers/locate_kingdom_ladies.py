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

locate_kingdom_ladies_simple_triggers = [
(4, #Locate kingdom ladies
    [
      #change location for all ladies
      (try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
        ##diplomacy start+ do not set the troop's center when the troop is leading a party
        (troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_lady),
        (troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),
		(try_begin),
			(gt, ":leaded_party", 0),
			(neg|party_is_active, ":leaded_party"),
			(assign, ":leaded_party", -1),
		(try_end),
        (lt, ":leaded_party", 1),#if the value is 0, it's a bug, so overlook it
        ##diplomacy end+
        
        #do not change location if under siege
        (assign, ":continue", 1),
        (try_begin),
            (troop_get_slot, ":location", ":troop_id",  slot_troop_cur_center ),
            (gt, ":location", -1),
            (party_slot_eq, ":location", slot_village_state, svs_under_siege),
            (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        
        (neg|troop_slot_ge, ":troop_id", slot_troop_prisoner_of_party, 0),
        (call_script, "script_get_kingdom_lady_social_determinants", ":troop_id"),
        (assign, ":location", reg1),
        (troop_set_slot, ":troop_id", slot_troop_cur_center, ":location"),
      (try_end),
	]),
]
