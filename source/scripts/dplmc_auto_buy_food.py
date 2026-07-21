# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_auto_buy_food (script)
# Called by menus in 3 domains: diplomacy, town, village
# ======================================================================

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

dplmc_auto_buy_food_scripts = [
##Adapted Auto-Buy-Food from rubik's Custom Commander
#Changed to parameterize merchant and customer, but did not finish expanding
#the script to work with non-player arguments.  (There is currently no need,
#but I can imagine using it for NPCs sent on item-purchasing missions, or if
#NPC parties had to buy food.)
#
##OLD: Overwrites: reg1, reg2, reg3, reg4
##NEW: Overwrite reg0
#
#INPUT:
#      arg1 :customer
#      arg2 :merchant_troop
("dplmc_auto_buy_food", [
    (store_script_param, ":customer", 1),
    (store_script_param, ":merchant_troop", 2),
    ##added section begin, preserve registers
    (assign, ":save_reg1", reg1),
    (assign, ":save_reg2", reg2),
    (assign, ":save_reg3", reg3),
    (assign, ":save_reg4", reg4),
    ##added section end

    (assign, ":customer_in_player_party", 0),#Always assumed true... re-write if you need to use for others

    (store_troop_gold, ":begin_gold", ":customer"),
    (store_free_inventory_capacity, ":begin_space", ":customer"),
    (troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", itm_raw_date_fruit, food_end),
      (neq, ":item", "itm_furs"),
      (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
      ##dplmc+: The next line required making a change to header_operations.py
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      (item_get_slot, ":food_portion", ":item", dplmc_slot_item_food_portion),
      (val_max, ":food_portion", 0),#dplmc+ added
      (store_item_kind_count, ":food_count", ":item", ":customer"),
      (lt, ":food_count", ":food_portion"),
      (store_free_inventory_capacity, ":free_inv_cap", ":customer"),
      (gt, ":free_inv_cap", 0),

      (call_script, "script_game_get_item_buy_price_factor", ":item"),
      (assign, ":buy_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":buy_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":customer_gold", ":customer"),
      (ge, ":customer_gold", ":score"),

      (troop_add_item, ":customer", ":item"),
      (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
      (troop_remove_gold, ":customer", ":score"),
      (troop_add_gold, ":merchant_troop", ":score"),
    (try_end),
    (set_show_messages, 1),
    (store_troop_gold, ":end_gold", ":customer"),
    (store_free_inventory_capacity, ":end_space", ":customer"),
    (try_begin),
      (neq, ":end_gold", ":begin_gold"),
      (store_sub, reg1, ":begin_gold", ":end_gold"),
      (store_sub, reg2, ":begin_space", ":end_space"),
      (store_sub, reg3, reg1, 1),
      (store_sub, reg4, reg2, 1),
      (eq, ":customer_in_player_party", 1),#<- added
      (display_message, "@You have bought {reg2} {reg4?kinds:kind} of food and lost {reg1} {reg3?denars:denar}."),
    (try_end),

    # sell rotten food
    (store_troop_gold, ":begin_gold", ":customer"),
    (store_free_inventory_capacity, ":begin_space", ":customer"),
    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", food_begin, food_end),
      (troop_get_inventory_slot_modifier, ":imod", ":customer", ":i_slot"),
      (eq, ":imod", imod_rotten),
      (store_free_inventory_capacity, ":free_inv_cap", ":merchant_troop"),
      (gt, ":free_inv_cap", 0),

      (call_script, "script_dplmc_get_item_value_with_imod", ":item", ":imod"),
      (assign, ":score", reg0),
      (val_div, ":score", 100),
      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (val_mul, ":score", ":sell_price_factor"),
      (troop_inventory_slot_get_item_amount, ":amount", ":customer", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":customer", ":i_slot"),
      (val_mul, ":score", ":amount"),
      (val_div, ":score", ":max_amount"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":merchant_gold", ":merchant_troop"),
      (ge, ":merchant_gold", ":score"),

      #(troop_add_item, ":merchant_troop", ":item", ":imod"),
      (troop_set_inventory_slot, ":customer", ":i_slot", -1),
      (troop_remove_gold, ":merchant_troop", ":score"),
      (troop_add_gold, ":customer", ":score"),
    (try_end),
    (set_show_messages, 1),
    (store_troop_gold, ":end_gold", ":customer"),
    (store_free_inventory_capacity, ":end_space", ":customer"),
    (try_begin),
      (neq, ":end_gold", ":begin_gold"),
      (store_sub, reg1, ":end_gold", ":begin_gold"),
      (store_sub, reg2, ":end_space", ":begin_space"),
      (store_sub, reg3, reg1, 1),
      (store_sub, reg4, reg2, 1),
      (eq, ":customer_in_player_party", 1), #<- added
      (display_message, "@You sold {reg2} {reg4?kinds:kind} of rotten food and gained {reg1} {reg3?denars:denar}."),
    (try_end),
    ##added section begin, preserve registers
    (assign, reg1, ":save_reg1"),
    (assign, reg2, ":save_reg2"),
    (assign, reg3, ":save_reg3"),
    (assign, reg4, ":save_reg4"),
    ##added section end
  ])
]
