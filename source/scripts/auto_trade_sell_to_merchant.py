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

auto_trade_sell_to_merchant_scripts = [
("auto_trade_sell_to_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_sold", 0),
    (assign, ":gold_gained", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (set_show_messages, 0),

    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":customer", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":customer", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      #Don't sell if player has disabled auto selling for this item
      (item_get_slot, ":sell_enabled", ":item", slot_item_auto_trade_sell_enabled),
      (gt, ":sell_enabled", 0),

      #Don't sell if the current amount is less than or equal to the player's minimum quantity
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (item_get_slot, ":min_qty", ":item", slot_item_auto_trade_min_quantity),
      (gt, ":item_count", ":min_qty"),

      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":sell_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score", 1),

      (item_get_slot, ":sell_price", ":item", slot_item_auto_trade_sell_over_price),
      (gt, ":score", ":sell_price"),

      (troop_set_inventory_slot, ":customer", ":i_slot", -1),
      (troop_add_gold, ":customer", ":score"),
      (call_script, "script_game_event_sell_item", ":item", 0),
      (val_add, ":items_sold", 1),
      (val_add, ":gold_gained", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_sold", 1),
      (assign, reg0, ":gold_gained"),
      (assign, reg1, ":items_sold"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You sold {reg1} {reg3?items:item} to {s0} and gained {reg0} {reg3?denars:denar}."),
    (try_end),
  ])
]
