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

game_get_item_sell_price_factor_scripts = [
#script_game_get_item_sell_price_factor:
# This script is called from the game engine for calculating the selling price of any item.
# INPUT:
# param1: item_kind_id
# OUTPUT:
# trigger_result and reg0 = price_factor
("game_get_item_sell_price_factor",
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
        (val_mul, ":price_factor", 100),#normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (else_try),
        #increase trade penalty while selling weapons, armor, and horses
        (val_mul, ":trade_penalty", 4),
      (try_end),

	  ##diplomacy start+
	  #If economic changes are enabled, use a lesser trade penalty when selling
 	  #to the correct merchant in town.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(gt, "$g_talk_troop", "trp_player"),
		(try_begin),
			#Selling weapons to the weaponsmith
			(party_slot_eq, "$g_encountered_party", slot_town_weaponsmith, "$g_talk_troop"),
			(this_or_next|is_between, ":item_kind_id", weapons_begin, weapons_end),
			(this_or_next|is_between, ":item_kind_id", shields_begin, shields_end),
				(is_between, ":item_kind_id", ranged_weapons_begin, ranged_weapons_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling armor to the armorer
			(party_slot_eq, "$g_encountered_party", slot_town_armorer, "$g_talk_troop"),
			(is_between, ":item_kind_id", armors_begin, armors_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(else_try),
			#Selling horses to the horse merchant
			(party_slot_eq, "$g_encountered_party", slot_town_horse_merchant, "$g_talk_troop"),
			(is_between, ":item_kind_id", horses_begin, horses_end),
			(val_mul, ":trade_penalty", 9),
			(val_div, ":trade_penalty", 10),
		(try_end),
	  (try_end),

	  #If economic changes are enabled, increase food prices in a town under siege.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		(is_between, "$g_encountered_party", centers_begin, centers_end),
		#Check selling food
		(is_between, ":item_kind_id", food_begin, food_end),
		#Check at a town or castle under siege for at least 48 hours
		(this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
		(party_slot_eq, "$g_encountered_party", slot_village_state, svs_under_siege),

		(party_slot_ge, "$g_encountered_party", slot_center_is_besieged_by, 1),
		(party_get_slot, ":siege_start", "$g_encountered_party", slot_center_siege_begin_hours),
		(store_current_hours, ":cur_hours"),
		(store_sub, reg0, ":cur_hours", ":siege_start"),
		(ge, reg0, 48),
		#Check last caravan or village trading party arrival (default to eight weeks ago)
		(store_sub, ":last_arrival", ":cur_hours", 8 * 7 * 24),
		(val_min, ":last_arrival", ":siege_start"),
		(try_for_range, ":village_no", villages_begin, villages_end),
			(party_slot_eq, ":village_no", slot_village_market_town, "$g_encountered_party"),
			(party_get_slot, reg0, ":village_no", dplmc_slot_village_trade_last_arrived_to_market),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		(try_for_range, ":slot_no", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
			#Not all of these slots correspond to towns, but that doesn't
			#matter since their arrival times won't update after the start
			#of the game.
			(party_get_slot, reg0, "$g_encountered_party", ":slot_no"),
			(val_min, reg0, ":cur_hours"),
			(val_max, ":last_arrival", reg0),
		(try_end),
		##Increase food prices by 10% for every 3 days the siege has been going on,
		#or a minimum of 5%.
		#TODO: Make use of the last caravan arrival time.
		(store_sub, ":hours_since", ":cur_hours", ":siege_start"),
		(store_mul, ":siege_percent", ":hours_since", 10),
		(val_add, ":siege_percent", (3 * 24) // 2),
		(val_div, ":siege_percent", 3 * 24),
		(val_max, ":siege_percent", 5),
		(val_add, ":siege_percent", 100),
		(val_mul, ":price_factor", ":siege_percent"),
		(val_add, ":price_factor", 50),
		(val_div, ":price_factor", 100),
	  (try_end),
	  ##diplomacy end+

      (store_add, ":penalty_divisor", 100, ":trade_penalty"),

      (val_mul, ":price_factor", 100),
	  ##diplomacy start+
	  (try_begin),
		(gt, ":penalty_divisor", 0),
		(store_div, reg0, ":penalty_divisor", 2),
		(val_add, ":price_factor", reg0),#round correctly
	  (try_end),
	  ##diplomacy end+
      (val_div, ":price_factor", ":penalty_divisor"),

      (assign, reg0, ":price_factor"),
      (set_trigger_result, reg0),
  ])
]
