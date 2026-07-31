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



  # Exchanging hero prisoners between factions and clearing old ransom offers
  

ransom_exchange_simple_triggers = [
(72,
   [(assign, "$g_ransom_offer_rejected", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (gt, ":town_lord", 0),
      (party_get_num_prisoner_stacks, ":num_stacks", ":center_no"),
      #SB : moved to top
      (store_troop_faction, ":faction_no", ":town_lord"),
      (troop_get_slot, ":wealth", ":town_lord", slot_troop_wealth),
      (str_store_faction_name, s2, ":faction_no"),
      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
        (store_random_in_range, ":random_no", 0, 100),
        (try_begin),
          (le, ":random_no", 10),
          (call_script, "script_calculate_ransom_amount_for_troop", ":stack_troop"),
          (assign, ":ransom_amount", reg0),
          ##diplomacy start+ Remove the wealth from the stack troop
          (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":stack_troop"),
          ##diplomacy end+
          (val_add, ":wealth", ":ransom_amount"),
          
          (party_remove_prisoners, ":center_no", ":stack_troop", 1),
          (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          
          (store_troop_faction, ":troop_faction", ":stack_troop"),
          (str_store_troop_name, s1, ":stack_troop"),
          (str_store_faction_name, s2, ":faction_no"),
          (str_store_faction_name, s3, ":troop_faction"),
          #SB : colorize faction, add s2 for imprisoning faction
          (faction_get_color, ":color", ":troop_faction"),
          (display_log_message, "@{s1} of {s3} has been released from captivity by {s2}.", ":color"),
        (try_end),
        #SB : moved to bottom
        (troop_set_slot, ":town_lord", slot_troop_wealth, ":wealth"),
      (try_end),
    (try_end),
    ]),
]
