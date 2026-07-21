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

dplmc_get_item_buy_price_factor_scripts = [
#script_get_poorest_village_of_faction
("dplmc_get_item_buy_price_factor",
    [
	##nested diplomacy start+
    #(store_script_param_1, ":item_kind_id"),
    #(store_script_param_2, ":center_no"),
	#Add two parameters
	(store_script_param, ":item_kind_id", 1),
	(store_script_param, ":center_no", 2),
	(store_script_param, ":customer_no", 3),
	(store_script_param, ":merchant_no", 4),
	##nested diplomacy start+
    (assign, ":price_factor", 100),

	##nested diplomacy start+
    #(call_script, "script_get_trade_penalty", ":item_kind_id"),
	(call_script, "script_dplmc_get_trade_penalty", ":item_kind_id", ":center_no", ":customer_no", ":merchant_no"),
	##nested diplomacy end+
    (assign, ":trade_penalty", reg0),

    (try_begin),
	  ##nested diplomacy start+
	  (gt, ":center_no", 0),
  	  (this_or_next|is_between, ":center_no", centers_begin, centers_end),
		(party_is_active, ":center_no"),

	  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
	  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
	  ##nested diplomacy end+
      (is_between, ":center_no", centers_begin, centers_end),
      (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
      (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
      (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
      (party_get_slot, ":price_factor", ":center_no", ":item_slot_no"),

      (try_begin),
		##nested diplomacy start+
		#OLD:
        #(is_between, ":center_no", villages_begin, villages_end),
        #(party_get_slot, ":market_town", ":center_no", slot_village_market_town),
		##NEW:
		(gt, ":center_no", 0),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
			(is_between, ":center_no", villages_begin, villages_end),
		(party_get_slot, ":market_town", ":center_no", slot_village_market_town),

		(ge, ":market_town", centers_begin),
		(this_or_next|party_slot_eq, ":market_town", slot_party_type, spt_town),
		(this_or_next|party_slot_eq, ":market_town", slot_party_type, spt_village),
			(is_between, ":market_town", centers_begin, centers_end),
		##nested diplomacy end+
        (party_get_slot, ":price_in_market_town", ":market_town", ":item_slot_no"),
        (val_max, ":price_factor", ":price_in_market_town"),
      (try_end),
	  ##nested diplomacy start+
	  #Enforce constraints
	  (val_clamp, ":price_factor", minimum_price_factor, maximum_price_factor + 1),
	  ##nested diplomacy end+

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
