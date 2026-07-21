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

auto_trade_buy_from_merchant_scripts = [
("auto_trade_buy_from_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_bought", 0),
    (assign, ":gold_spent", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      (store_free_inventory_capacity, ":free_inv_cap", ":customer"),
      (gt, ":free_inv_cap", 0),

      #Don't buy if player has disabled auto buying for this item
      (item_get_slot, ":buy_enabled", ":item", slot_item_auto_trade_buy_enabled),
      (gt, ":buy_enabled", 0),

      #Don't buy if the quantity would exceed player's max quantity
      #Since there is a separate option to enable/disable, a max quantity of 0 is treated as no max
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (assign, ":qty_valid", 1),
      (try_begin),
        (item_get_slot, ":max_qty", ":item", slot_item_auto_trade_max_quantity),
        (gt, ":max_qty", 0),
        (ge, ":item_count", ":max_qty"),
        (assign, ":qty_valid", 0),
      (try_end),
      (eq, ":qty_valid", 1),

      (call_script, "script_game_get_item_buy_price_factor", ":item"),
      (assign, ":buy_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":buy_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":customer_gold", ":customer"),
      (val_sub, ":customer_gold", "$g_auto_trade_minimum_wealth"),
      (ge, ":customer_gold", ":score"),

      (item_get_slot, ":buy_price", ":item", slot_item_auto_trade_buy_under_price),
      (lt, ":score", ":buy_price"),

      (troop_add_item, ":customer", ":item"),
      (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
      (troop_remove_gold, ":customer", ":score"),
      (troop_add_gold, ":merchant_troop", ":score"),
      (call_script, "script_game_event_buy_item", ":item", 0),
      (val_add, ":items_bought", 1),
      (val_add, ":gold_spent", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_bought", 1),
      (assign, reg0, ":gold_spent"),
      (assign, reg1, ":items_bought"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You bought {reg1} {reg3?items:item} from {s0} for {reg0} {reg3?denars:denar}."),
    (try_end),
  ])
]
