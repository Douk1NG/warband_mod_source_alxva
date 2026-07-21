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

initialize_auto_trade_scripts = [
#script_get_disguise_string
#Autotrade begin
# script_initialize_auto_trade
("initialize_auto_trade",
  [
    (assign, "$g_auto_trade_minimum_wealth", 1000), 
    (assign, "$g_auto_trade_items_when_leaving", 0),

    (try_for_range, ":cur_item", trade_goods_begin, trade_goods_end),
        (store_item_value, ":item_value", ":cur_item"),
        (store_mul, ":buy_price", ":item_value", 80),
        (val_div, ":buy_price", 100),
        (item_set_slot, ":cur_item", slot_item_auto_trade_buy_under_price, ":buy_price"),
        (item_set_slot, ":cur_item", slot_item_auto_trade_sell_over_price, ":item_value"),
        (item_set_slot, ":cur_item", slot_item_auto_trade_buy_enabled, 1),
        (item_set_slot, ":cur_item", slot_item_auto_trade_sell_enabled, 1),
        (item_set_slot, ":cur_item", slot_item_auto_trade_min_quantity, 0),
        (item_set_slot, ":cur_item", slot_item_auto_trade_max_quantity, 0),
    (try_end),
  ])
]
