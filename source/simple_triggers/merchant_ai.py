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




  #Troop AI: Merchants thinking
  

merchant_ai_simple_triggers = [
(8,
   [
       (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB : moved this up top
       (val_sub, ":reduce_campaign_ai", 1),
       (val_mul, ":reduce_campaign_ai", 10), #pre-calculate amount
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
         (party_is_in_any_town, ":party_no"),

         (store_faction_of_party, ":merchant_faction", ":party_no"),
         (faction_get_slot, ":num_towns", ":merchant_faction", slot_faction_num_towns),
         (try_begin),
           (le, ":num_towns", 0),
           (remove_party, ":party_no"),
         (else_try),
           (party_get_cur_town, ":cur_center", ":party_no"),

           (store_random_in_range, ":random_no", 0, 100),
           (assign, ":tariff_succeed_limit", 45), #SB : base amount for medium
           (try_begin),
             (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
             (eq, ":merchant_faction", "$players_kingdom"),
             (val_add, ":tariff_succeed_limit", ":reduce_campaign_ai"),
           (try_end),
           # (try_begin),
             # (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),

             # # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             # (try_begin),
               # (eq, ":reduce_campaign_ai", 0), #hard (less money from tariffs)
               # (assign, ":tariff_succeed_limit", 35),
             # (else_try),
               # (eq, ":reduce_campaign_ai", 1), #medium (normal money from tariffs)
               # (assign, ":tariff_succeed_limit", 45),
             # (else_try),
               # (eq, ":reduce_campaign_ai", 2), #easy (more money from tariffs)
               # (assign, ":tariff_succeed_limit", 60),
             # (try_end),
           # (else_try),
             # (assign, ":tariff_succeed_limit", 45),
           # (try_end),

           (lt, ":random_no", ":tariff_succeed_limit"),

           #SB : todo queue caravans so they don't blob together, obvious if same destination
           (assign, ":can_leave", 1),
           (try_begin),
             (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
             (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
             (assign, ":can_leave", 0),
           (try_end),
           (eq, ":can_leave", 1),

           (assign, ":do_trade", 0),
           (try_begin),
             (party_get_slot, ":cur_ai_state", ":party_no", slot_party_ai_state),
             (eq, ":cur_ai_state", spai_trading_with_town),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),
             (assign, ":do_trade", 1),
           (try_end),

           (assign, ":target_center", -1),

           (try_begin), #Make sure escorted caravan continues to its original destination.
             (eq, "$caravan_escort_state", 1),
             (eq, "$caravan_escort_party_id", ":party_no"), #SB : redo globals here
             (assign, ":caravan_distance_to_player", 9999),
             (try_begin), #code from triggers
               (eq, "$caravan_escort_state", 1),
               (eq, ":cur_center", "$caravan_escort_destination_town"), 
               #arrived, check if player is nearby to prompt conversation (unless player triggered dialog first)
               (store_distance_to_party_from_party, ":caravan_distance_to_player","p_main_party","$caravan_escort_party_id"),
               (lt, ":caravan_distance_to_player", 5),
               (map_free), #in case player is fighting?
               (start_encounter, "$caravan_escort_party_id"),
             (else_try),
               (ge, ":caravan_distance_to_player", 5), #cancel quest
               (assign, "$caravan_escort_state", 0),
             (else_try),
               # (neg|party_is_in_town, ":party_no", "$caravan_escort_destination_town"),
               (neq, ":cur_center", "$caravan_escort_destination_town"),
               (assign, ":target_center", "$caravan_escort_destination_town"),
             (try_end),
           (else_try),
            ##diplomacy start+ added third parameter "-1" to use the town's location
             (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":cur_center", ":merchant_faction", -1),
            ##diplomacy end+
             (assign, ":target_center", reg0),
           (try_end),
           (is_between, ":target_center", towns_begin, towns_end),
           (neg|party_is_in_town, ":party_no", ":target_center"),

           (try_begin),
             (eq, ":do_trade", 1),
             (str_store_party_name, s7, ":cur_center"),
             (call_script, "script_do_merchant_town_trade", ":party_no", ":cur_center"),
           (try_end),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":target_center"),
           (party_set_flags, ":party_no", pf_default_behavior, 0),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
         (try_end),
       (try_end),
    ]),
]
