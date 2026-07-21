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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_item_buy_price_factor_scripts = [
#script_order_best_besieger_party_to_guard_center:
# This script is called from the game engine for calculating the buying price of any item.
# INPUT:
# param1: item_kind_id
# OUTPUT:
# trigger_result and reg0 = price_factor
("game_get_item_buy_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
      (assign, ":price_factor", 100),

      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price_factor", "$g_encountered_party", ":item_slot_no"),

		#new
		#(try_begin),
		#	(is_between, "$g_encountered_party", villages_begin, villages_end),
		#	(party_get_slot, ":market_town", "$g_encountered_party", slot_village_market_town),
		#	(party_get_slot, ":price_in_market_town", ":market_town", ":item_slot_no"),
		#	(val_max, ":price_factor", ":price_in_market_town"),
		#(try_end),

		#For villages, the good will be sold no cheaper than in the market town
		#This represents the absence of a permanent market -- ie, the peasants retain goods to sell on their journeys to town, and are not about to do giveaway deals with passing adventurers


        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),

      (store_add, ":penalty_factor", 100, ":trade_penalty"),

      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ])
]
