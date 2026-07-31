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



        #SB : change this block
    

escort_caravan_simple_triggers = [
(1,
    [
      # #escort caravan quest auto dialog trigger, moved to menu while auto-entering towns
      # (try_begin),
        # (eq, "$caravan_escort_state", 1),
        # (party_is_active, "$caravan_escort_party_id"),

        # (store_distance_to_party_from_party, ":caravan_distance_to_destination","$caravan_escort_destination_town","$caravan_escort_party_id"),
        # (lt, ":caravan_distance_to_destination", 2),

        # (store_distance_to_party_from_party, ":caravan_distance_to_player","p_main_party","$caravan_escort_party_id"),
        # (lt, ":caravan_distance_to_player", 5),

        # (assign, "$talk_context", tc_party_encounter),
        # (assign, "$g_encountered_party", "$caravan_escort_party_id"),
        # (party_stack_get_troop_id, ":caravan_leader", "$caravan_escort_party_id", 0),
        # (party_stack_get_troop_dna, ":caravan_leader_dna", "$caravan_escort_party_id", 0),

        # (start_map_conversation, ":caravan_leader", ":caravan_leader_dna"),
      # (try_end),
      #SB : debug block
      (try_begin),
        (eq, "$cheat_mode", 2),
        (troop_is_hero, "$g_talk_troop"),
        (str_store_troop_name, s17, "$g_talk_troop"),
        (troop_get_slot, reg17, "$g_talk_troop", slot_troop_wealth),
        (try_begin),
          (neq, reg17, "$demanded_money"),
          (display_message, "@{s17} has {reg17} denars"),
        (try_end),
        (assign, "$demanded_money", reg17),
      (try_end),

      (try_begin),
        (gt, "$g_reset_mission_participation", 1),

        (try_for_range, ":troop", active_npcs_begin, kingdom_ladies_end),
          (troop_set_slot, ":troop", slot_troop_mission_participation, 0),
        (try_end),
      (try_end),
    ]),
]
