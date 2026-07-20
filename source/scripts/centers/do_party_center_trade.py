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

do_party_center_trade_scripts = [
#script_do_party_center_trade
# INPUT: arg1 = party_no, arg2 = center_no, arg3 = percentage_change_in_center
# OUTPUT: reg0 = total_change
("do_party_center_trade",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":center_no", 2),
      (store_script_param, ":percentage_change", 3), #this should probably always be a constant. Currently it is 25
	  (assign, ":percentage_change", 30),
	  ##diplomacy start+
	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  #If optional economic changes are enabled, reduce the percentage change in order
	  #to make prices feel less static.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#Only apply lessened price movements to towns.
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		#This halves the average impact as well as making it more variable.
		(val_add, ":percentage_change", 1),
		(store_random_in_range, ":percentage_change", 0, ":percentage_change"),
		#Display economics diagnostic
		(ge, "$cheat_mode", 3),
		(str_store_party_name, s3, ":origin"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg4, ":percentage_change"),
		(display_message, "@{!}DEBUG -- Trade from {s3} to {s4}: rolled random impact of {reg4}"),
	  (try_end),
	  ##diplomacy end+

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  (party_set_slot, ":party_no", slot_party_last_traded_center, ":center_no"),
	  ##diplomacy start+
	  #Update the record of trade route arrival times
      (try_begin),
         (ge, ":origin", centers_begin),
    	 ##zerilius changes begin
    	 # (this_or_next|party_slot_eq, ":origin", villages_begin, villages_end),
    	 (this_or_next|party_slot_eq, ":origin", slot_party_type, spt_village),
    	 ##zerilius changes end
         (is_between, ":origin", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":origin", dplmc_slot_village_trade_last_arrived_to_market, ":cur_hours"),
      (try_end),
      (try_begin),
	     (ge, ":origin", centers_begin),
		 (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		 (store_current_hours, ":cur_hours"),
		 (try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
            (party_slot_eq,  ":center_no", ":trade_route_slot", ":origin"),
			(store_sub, ":trade_route_arrival_slot", ":trade_route_slot", slot_town_trade_routes_begin),
			(val_add, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin),
			(is_between, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),#this will always be true unless a modder increased the number of trade route slots without increasing the number of last arrival slots
			(party_set_slot, ":center_no", ":trade_route_arrival_slot", ":cur_hours"),
         (try_end),
         (else_try),
            (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
               (is_between, ":center_no", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":center_no", dplmc_slot_village_trade_last_returned_from_market, ":cur_hours"),
	  (try_end),
      #SB : drop off prisoners
      (try_begin),
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":town_faction", ":center_no"),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":town_faction", ":party_faction"),
        (call_script, "script_party_prisoners_add_party_prisoners", ":center_no", ":party_no"),
        (call_script, "script_party_remove_all_prisoners", ":party_no"),
      (else_try), #sell off looted items
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
        (is_between, ":center_no", towns_begin, towns_end),
        (party_get_slot, ":num_items", ":party_no", slot_party_next_looted_item_slot),
        (is_between, ":num_items", 1, num_party_loot_slots + 1), #has any loot
         # (this_or_next|eq, ":num_items", 0),
        (party_get_slot, ":town_merchant", ":center_no", slot_town_merchant),
        (party_get_slot, ":town_weapon", ":center_no", slot_town_weaponsmith),
        (party_get_slot, ":town_armor", ":center_no", slot_town_armorer),
        (party_get_slot, ":town_horse", ":center_no", slot_town_horse_merchant),

        #apply penalty with 0 trade skill for farmer, 2 for caravan masters
        (assign, ":seller_troop", -1), #0 skill
        (try_begin),
          (party_get_slot, ":spt", ":party_no", slot_party_type),
          # (eq, ":spt", spt_village_farmer),
          # (assign, ":seller_troop", -1), #0 skill
        # (else_try),
          (eq, ":spt", spt_kingdom_caravan),
          (assign, ":seller_troop", "trp_caravan_master"), #knows_common, 2 skill
        (else_try),
          (eq, ":spt", spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":seller_troop", ":party_no", 0),
        (try_end),
        (val_add, ":num_items", slot_party_looted_item_1),
        (try_for_range, ":slot_no", slot_party_looted_item_1, ":num_items"),
          (party_get_slot, ":item_no", ":party_no", ":slot_no"),
          (gt, ":item_no", 0),
          (item_get_type, ":itp", ":item_no"),
          (store_add, ":imod_slot", ":slot_no", num_party_loot_slots),
          (party_get_slot, ":imod_no", ":party_no", ":imod_slot"),
          (item_get_type, ":itp", ":item_no"),
          (try_begin),
            (this_or_next|is_between, ":itp", itp_type_one_handed_wpn, itp_type_goods),
            (is_between, ":itp", itp_type_pistol, itp_type_animal),
            (assign, ":merchant", ":town_weapon"),
          (else_try),
            (is_between, ":itp", itp_type_head_armor, itp_type_pistol),
            (assign, ":merchant", ":town_armor"),
          (else_try),
            (eq, ":itp", itp_type_horse),
            (assign, ":merchant", ":town_horse"),
          (else_try),
            (assign, ":merchant", ":town_merchant"),
          (try_end),
          (gt, ":merchant", 0),
          (store_troop_gold, ":merchant_gold", ":merchant"),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":imod_no"),
          (store_div, ":price", reg0, 4), #or some other factor

          (call_script, "script_dplmc_get_trade_penalty", ":item_no", ":center_no", ":seller_troop", ":merchant"),
          (val_mul, ":price", reg0),
          (val_div, ":price", 100),
          (val_max, ":price", 1),
          (gt, ":merchant_gold", ":price"), #can afford
          (troop_remove_gold, ":merchant", ":price"),
          (troop_add_item, ":merchant", ":item_no", ":imod_no"),
          # (party_set_slot, ":party_no", ":slot_no", -1), #clear off later
          # (party_set_slot, ":party_no", ":imod_slot", -1),
        (try_end),

        #any unsold item at this point are cleared
        (try_for_range, ":slot_no", slot_party_next_looted_item_slot, slot_party_looted_item_1_modifier + num_party_loot_slots),
          (party_set_slot, ":party_no", ":slot_no", 0),
        (try_end),

      (try_end),
	  ##diplomacy end+

      (assign, ":total_change", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
        (party_get_slot, ":cur_merchant_price", ":party_no", ":cur_good_price_slot"),
        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
        (store_sub, ":price_dif", ":cur_merchant_price", ":cur_center_price"),
        (assign, ":cur_change", ":price_dif"),
        (val_abs, ":cur_change"),
        (val_add, ":total_change", ":cur_change"),
        (val_mul, ":cur_change", ":percentage_change"),
        (val_div, ":cur_change", 100),

		#This is to reconvert from absolute value
        (try_begin),
          (lt, ":price_dif", 0),
          (val_mul, ":cur_change", -1),
        (try_end),

		(assign, ":initial_price", ":cur_center_price"),

		#The new price for the caravan or peasant is set before the change, so the prices in the trading town have full effect on the next center
        (party_set_slot, ":party_no", ":cur_good_price_slot", ":cur_center_price"),

        (val_add, ":cur_center_price", ":cur_change"),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_center_price"),

		(try_begin),
			(eq, "$cheat_mode", 3),
			(str_store_party_name, s3, ":origin"),
			(str_store_party_name, s4, ":center_no"),
			(str_store_item_name, s5, ":cur_good"),
			(assign, reg4, ":initial_price"),
			(assign, reg5, ":cur_center_price"),
			(display_log_message, "@{!}DEBUG -- Trade of {s5} from {s3} to {s4} brings price from {reg4} to {reg5}"),
		(try_end),

      (try_end),
      (assign, reg0, ":total_change"),
  ])
]
