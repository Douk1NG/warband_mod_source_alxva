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




#####!!!!!

# Village upgrade triggers

# School
  

village_school_relation_simple_triggers = [
(30 * 24,
   [(try_for_range, ":cur_village", villages_begin, villages_end),
      # (party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      (party_get_slot, ":town_lord", ":cur_village", slot_town_lord),
      #SB : also handle the case where player hands out villages
      (store_faction_of_party, ":faction_no", ":cur_village"),
      (try_begin),
        (eq, ":faction_no", "$players_kingdom"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
        (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (assign, ":town_lord", "trp_player"),
      (try_end),
      (eq, ":town_lord", "trp_player"),
      
      (party_slot_eq, ":cur_village", slot_center_has_school, 1),
      (party_get_slot, ":cur_relation", ":cur_village", slot_center_player_relation),
      (val_add, ":cur_relation", 1),
      (val_min, ":cur_relation", 100),
      (party_set_slot, ":cur_village", slot_center_player_relation, ":cur_relation"),
    (try_end),
    ]),
]
