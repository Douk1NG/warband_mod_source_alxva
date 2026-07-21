# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_send_gift_scripts = [
("dplmc_send_gift",
    [
    (store_script_param, ":target_troop", 1),
    (store_script_param, ":gift", 2),
    (store_script_param, ":amount", 3),

    (try_begin),
      (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_hero),
      (troop_get_slot, ":target_party", ":target_troop", slot_troop_leaded_party),
    (else_try),
      (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_lady),
      (troop_get_slot, ":target_party", ":target_troop", slot_troop_cur_center),
    (try_end),


    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_item_name, s12, ":gift"),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Bring {s12} to {s13}"),
    (try_end),

    (try_begin),
       #Guard against this being called without an explicit amount
       (lt, ":amount", 1),
       (display_message, "@{!} ERROR: Bad gift amount {reg0}.  (Tell the mod writer he needs to update his code.)  Using a safe default."),
       (assign, ":amount", 1),
       (troop_slot_eq, ":target_troop", slot_troop_occupation, slto_kingdom_hero),
       (assign, ":amount", 150),
    (try_end),
    (assign, ":original_amount", ":amount"),#Save this here because amount gets modified below!

    (call_script, "script_dplmc_withdraw_from_treasury", 50),
    (troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),

  	  (try_for_range, ":inventory_slot", 0, ":capacity"),
  	    (gt, ":amount", 0),
  		  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
  		  (eq, ":item", ":gift"),
  		  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
  		  (try_begin),
  		    (le, ":tmp_amount", ":amount"),
  		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", 0),
  		    (val_sub, ":amount", ":tmp_amount"),
  		  (else_try),
  		    (val_sub, ":tmp_amount", ":amount"),
  		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", ":tmp_amount"),
  		    (assign, ":amount", 0),
  		  (try_end),
  	  (try_end),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_dplmc_gift_caravan"),
    (assign,":spawned_party",reg0),
    (party_set_slot, ":spawned_party", slot_party_type, dplmc_spt_gift_caravan),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":gift"),
    (party_set_slot, ":spawned_party",  slot_party_orders_object,  ":target_troop"),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_stack_get_troop_id, ":caravan_master", ":spawned_party", 0),
    (troop_set_slot, ":caravan_master", slot_troop_leaded_party, ":spawned_party"),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_parameter_1, ":original_amount"),
    ])
]
