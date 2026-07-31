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


  ##diplomacy begin
  #Troop AI Spouse: Spouse thinking
  

spouse_ai_thinking_simple_triggers = [
(3,
   [
	(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	(ge, ":player_spouse", active_npcs_begin),#<-- skip the rest of the check when there is no spouse
    (try_for_parties, ":spouse_party"),
      (party_slot_eq, ":spouse_party", slot_party_type, dplmc_spt_spouse),

      (party_get_slot, ":spouse_target", ":spouse_party", slot_party_orders_object),
      (party_get_slot, ":home_center", ":spouse_party", slot_party_home_center),
      (store_distance_to_party_from_party, ":distance", ":spouse_party", ":spouse_target"),

      #Moving spouse to home village
      (try_begin),
        (le, ":distance", 1),
        (try_begin),
          (this_or_next|eq, ":spouse_target", "$g_player_court"),
		      (eq, ":spouse_target", ":home_center"),
          (remove_party, ":spouse_party"),
          (troop_set_slot, ":player_spouse", slot_troop_cur_center, ":spouse_target"),
        (else_try),
          (try_begin),
            (is_between, ":spouse_target", villages_begin, villages_end),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_elder),
          (else_try),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_merchant),
          (try_end),
          (troop_get_slot, ":amount", ":player_spouse", dplmc_slot_troop_mission_diplomacy),
          (troop_remove_items, ":cur_merchant", "itm_bread", ":amount"),
          (party_set_ai_behavior, ":spouse_party", ai_bhvr_travel_to_party),
          (try_begin),
            (gt, "$g_player_court", 0),
            (party_set_slot, ":spouse_party", slot_party_ai_object, "$g_player_court"),
            (party_set_ai_object, ":spouse_party", "$g_player_court"),
          (else_try),
            (party_set_slot, ":spouse_party", slot_party_ai_object, ":home_center"),
            (party_set_ai_object, ":spouse_party", ":home_center"),
          (try_end),

          (troop_add_items, "trp_household_possessions", "itm_bread", ":amount"),
        (try_end),
      (try_end),
    (try_end),
    ]),
]
