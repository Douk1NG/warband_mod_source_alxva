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


#-## TBS - Beer drinking end

  ###(((travel_to_player_court
  

beer_drinking_rest_simple_triggers = [
(1,
    [
      (faction_get_slot, ":players_leader", "$players_kingdom", slot_faction_leader),
      (eq, ":players_leader", "trp_player"),
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),

        (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":troop_party_no", 1),
        (party_is_active, ":troop_party_no"),
        (party_set_ai_behavior, ":troop_party_no", ai_bhvr_travel_to_party),
        (party_set_ai_object, ":troop_party_no", "$g_player_court"),
      (try_end),
    ]),
]
