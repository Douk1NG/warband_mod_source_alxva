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



  # Taking denars from player while resting in not owned centers
  

resting_denars_simple_triggers = [
(1,
   [(neg|map_free),
    (is_currently_night),
#    (ge, "$g_last_rest_center", 0),
    (is_between, "$g_last_rest_center", centers_begin, centers_end),
    (neg|party_slot_eq, "$g_last_rest_center", slot_town_lord, "trp_player"),

##diplomacy begin
    (party_get_slot, ":town_lord", "$g_last_rest_center", slot_town_lord),
    (assign, reg0, 0),
    (try_begin),
      (is_between, ":town_lord", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":town_lord"),
      (try_begin),
        (neq, reg0, 0),
        (display_message, "@You are within the walls of an affiliated family member and don't have to pay for accommodation."),
      (try_end),
    (try_end),
    (eq, reg0, 0),
##diplomacy end

    (store_faction_of_party, ":last_rest_center_faction", "$g_last_rest_center"),
    (neq, ":last_rest_center_faction", "fac_player_supporters_faction"),
    (store_current_hours, ":cur_hours"),
    (ge, ":cur_hours", "$g_last_rest_payment_until"),
    (store_add, "$g_last_rest_payment_until", ":cur_hours", 24),
    (store_troop_gold, ":gold", "trp_player"),
    (party_get_num_companions, ":num_men", "p_main_party"),
    (store_div, ":total_cost", ":num_men", 4),
    (val_add, ":total_cost", 1),
    (try_begin),
      (ge, ":gold", ":total_cost"),
      (display_message, "@You pay for accommodation."),
      (troop_remove_gold, "trp_player", ":total_cost"),
      (try_begin), #SB : faction troop morale
        (party_get_slot, ":old_faction", "$g_last_rest_center", slot_center_original_faction),
        (party_get_slot, ":relation", "$g_last_rest_center", slot_center_player_relation),
        (store_random_in_range, ":relation", ":relation", 1100), #spread of 1200 or 1000
        (ge, ":relation", 900),
        (val_sub, ":relation", ":total_cost"), #around 800
        (val_div, ":relation", 100),
        (val_max, ":relation", 1),
        (call_script, "script_change_faction_troop_morale", ":old_faction", ":relation", 0),
      (try_end),
    (else_try),
      (gt, ":gold", 0),
      (troop_remove_gold, "trp_player", ":gold"),
      #SB : stop resting
      (display_message, "@You are unable to pay for accommodation!", message_alert),
      (play_sound, "snd_encounter_nobleman"),
      # (val_mul, ":total_cost", -1),
      # (call_script, "script_change_player_party_morale", ":total_cost"),
      (val_div, ":total_cost", -10),
      (call_script, "script_change_player_relation_with_center", "$g_last_rest_center" ":total_cost"),
      (rest_for_hours, 0, 0, 0),
    (try_end),
    ]),
]
