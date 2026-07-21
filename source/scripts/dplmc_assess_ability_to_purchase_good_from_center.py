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

dplmc_assess_ability_to_purchase_good_from_center_scripts = [
#script_dplmc_assess_ability_to_purchase_good_from_center
# INPUT: arg1 = good_no
#        arg2 = center_no
# OUTPUT:
#        reg0 = actual price (may be theoretical if unavailable)
#        reg1 = 1 if available, 0 if unavailable
("dplmc_assess_ability_to_purchase_good_from_center",
    [
		(store_script_param, ":good_no", 1),
		(store_script_param, ":center_no", 2),

		#This is still quite experimental.  This is a work in progress
                #rather than a finished formula.
		(assign, ":price_factor", average_price_factor),
		(assign, ":has_good", 0),

		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),

			(is_between, ":good_no", trade_goods_begin, trade_goods_end),

			(store_sub, ":item_slot_no", ":good_no", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":price_factor", ":center_no", ":item_slot_no"),

			(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":good_no", ":center_no"),
			(assign, ":has_good", reg0),
			#abort if good is found
			(lt, ":has_good", 1),

			(store_faction_of_party, ":center_faction", ":center_no"),
			(faction_get_slot, ":mercantilism", ":center_faction", dplmc_slot_faction_mercantilism),
			(val_clamp, ":mercantilism", -3, 4),

			#For towns, check trade centers.
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(is_between, ":center_no", towns_begin, towns_end),

			(store_current_hours, ":cur_hours"),
			(assign, ":best_foreign_price", maximum_price_factor),
         (assign, ":worst_price_seen", ":price_factor"),

			(try_for_range, ":trade_town_index", slot_town_trade_routes_begin, slot_town_trade_routes_end),
				(party_get_slot, ":trade_town", ":center_no", ":trade_town_index"),
            (is_between, ":trade_town", centers_begin, centers_end),

				(party_get_slot, ":price_factor_2", ":trade_town", ":item_slot_no"),
				(val_max, ":worst_price_seen", ":price_factor_2"),

            (party_slot_eq, ":trade_town", slot_party_type, spt_town),
				(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":good_no", ":trade_town"),
				#The town has or produces the item
				(ge, reg0, 1),

				#Get the number of hours since the last caravan arrival, and set the penalty accordingly.
				(assign, ":hours_since", 0),
				#The slot storing the arrival time.  This may be uninitialized for old saved games used
				#with this mod.
				(store_sub, ":arrival_slot", ":trade_town_index", slot_town_trade_routes_begin),
				(val_add, ":arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin),
				(try_begin),
					#This condition can only occur if the number of trade route slots was increased
					#but the number of trade arrival time slots was not.  Check just in case, to avoid
					#strange errors.
					(neg|is_between, ":arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
					#Set "hours-since" to one week.
					(assign, ":hours_since", 7 * 24),
				(else_try),
					#If the slot is uninitialized, give it a random plausible value.
					(party_slot_eq, ":center_no", ":arrival_slot", 0),#Uninitialzed memory!
					(store_random_in_range, ":hours_since", 1, (24 * 7 * 5) + 1),#random time in last five weeks
					(party_get_slot, ":prosperity_factor", ":center_no", slot_town_prosperity),
					(val_clamp, ":prosperity_factor", 0, 101),
					(val_add, ":prosperity_factor", 75),
					(val_mul, ":hours_since", 125),
					(val_div, ":hours_since", ":prosperity_factor"),#last arrival some time in the last five weeks, plus or minus up to 40% based on prosperity
					(store_sub, ":last_arrival", ":cur_hours", ":hours_since"),
					(party_set_slot, ":center_no", ":arrival_slot", ":last_arrival"),
				(else_try),
					(party_get_slot, ":last_arrival", ":center_no", ":arrival_slot"),
					(store_sub, ":hours_since", ":cur_hours", ":last_arrival"),
					(val_max, ":hours_since", 0),
				(try_end),


				#Base penalty is 5%.  It stays at a flat 5% for the first week, then begins rising
				#at a rate of 5% per week afterwards (incremented continuously).
				#Clamp the maximum penalty at 50%.
				(store_mul, ":penalty", ":hours_since", 5),
				(val_add, ":penalty", (24 * 7) // 2),
				(val_div, ":penalty", 24 * 7),
				(val_max, ":penalty", 5),#required for the first week
				(val_min, ":penalty", 50),#don't increase above 50%

				#Apply mercantilism
				(store_faction_of_party, ":other_faction", ":trade_town"),
				(try_begin),
					#Decrease penalty for mercantilism, increase for free trade
					(eq, ":other_faction", ":center_faction"),
					(val_sub, ":penalty", ":mercantilism"),
				(else_try),
					#Increase penalty for mercantilism, decrease for free trade
					(val_add, ":penalty", ":mercantilism"),
				(try_end),

				(try_begin),
					(ge, ":price_factor_2", average_price_factor),
					(val_mul, ":price_factor_2", ":penalty"),
					(val_add, ":price_factor_2", 50),
					(val_div, ":price_factor_2", 100),
				(else_try),
					(store_add, reg0, 100, ":penalty"),
					(val_mul, reg0, average_price_factor),
					(val_add, reg0, 50),
					(val_div, reg0, 100),
					(val_add, ":price_factor_2", reg0),
				(try_end),
				#Make use of the source
				(assign, ":has_good", 1),
				(val_min, ":best_foreign_price", ":price_factor_2"),
			(try_end),
			(try_begin),
			   (ge, ":has_good", 1),
				(val_min, ":price_factor", ":best_foreign_price"),
			(else_try),
  		      #Make it so that lack of supply will not make the price lower
			   (lt, ":has_good", 1),
			   (val_max, ":price_factor", ":worst_price_seen"),
			(try_end),
		(try_end),

		(try_begin),
			(lt, ":has_good", 1),
			(val_max, ":price_factor", average_price_factor),#don't give bargains if there is no supply
			(val_mul, ":price_factor", 8),#sixty percent penalty
			(val_div, ":price_factor", 5),
		(try_end),

		#Apply constraints at the last step
		(val_clamp, ":price_factor", minimum_price_factor, maximum_price_factor),

		(assign, reg0, ":price_factor"),
		(assign, reg1, ":has_good"),
	])
]
