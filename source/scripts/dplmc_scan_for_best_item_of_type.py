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

dplmc_scan_for_best_item_of_type_scripts = [
#######################
# Search for the most expensive item of a specified type
##diplomacy start+
#"script_dplmc_scan_for_best_item_of_type"
#
#INPUT:
#   arg1 :troop
#   arg2 :item_type
#   arg3 :troop_using
#
#OUTPUT:
#   reg0 index of best item (-1 if not found)
##diplomacy end+
("dplmc_scan_for_best_item_of_type", [
	(store_script_param, ":troop",1),
	(store_script_param, ":item_type",2),
	(store_script_param, ":troop_using", 3),


    #SB : parse damage type and meta type (if any)
    # (store_div, ":dmg_type", ":item_type", meta_dmg_mask),
    (store_mod, ":meta_type", ":item_type", meta_dmg_mask), #use this instead
    (store_mod, ":item_type", ":meta_type", meta_itp_mask), #base type

    (assign, ":best_slot", -1),
    (assign, ":best_value", -1),
    # iterate through the list of items
    (troop_get_inventory_capacity, ":inv_cap", ":troop"),
    (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
        (ge, ":item", 0),
        (troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
        #(item_get_type, ":this_item_type", ":item"),  use the following instead

        # #### Autoloot improved by rubik begin
        # (try_begin),
            # # (item_slot_eq, ":item", dplmc_slot_two_handed_one_handed, 1),
            # (item_has_property, ":item", itp_type_two_handed_wpn),
            # (neg|item_has_property, ":item", itp_two_handed),
            # (assign, ":this_item_type", 11), # type 11 = two-handed/one-handed
        # (else_try),
            # (item_get_type, ":this_item_type", ":item"),
        # (try_end),
        # #### Autoloot improved by rubik end
        (call_script, "script_item_get_type_aux", ":item"), #SB : compare metatype
        (eq, ":meta_type", reg0), # it's one of the kind we're looking for (meta-type holds itp if none exists)
        (call_script, "script_dplmc_troop_can_use_item", ":troop_using", ":item", ":imod"),
        (eq, reg0, 1), # can use
        #(call_script, "script_get_item_value_with_imod", ":item", ":imod"),  # use the following instead

        #### Autoloot improved by rubik begin
        # get item_score instead of price
        (call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
        #### Autoloot improved by rubik end
        (assign, ":cur_value", reg0),
        #SB : adjust value here for damage preference
        # (try_begin),
          # (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
          # (item_get_swing_damage, ":swing_damage", ":item"),
          # (item_get_thrust_damage, ":thrust_damage", ":item"),
          # (try_begin),
            # (ge, ":swing_damage", ":thrust_damage"),
            # (item_get_swing_damage_type, ":item_dmg_type", ":item"),
          # (else_try),
            # (lt, ":swing_damage", ":thrust_damage"),
            # (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
          # (try_end),
          # #check if it matches preference
          # (eq, ":dmg_type", ":item_dmg_type"),
          # (val_mul, ":cur_value", 3),
        # (try_end),
        (gt, ":cur_value", ":best_value"), # best one we've seen yet
        (assign, ":best_slot", ":i_slot"),
        (assign, ":best_value", ":cur_value"),
    (try_end),



    # return the slot of the best one
    (assign, reg0, ":best_slot"),
])
]
