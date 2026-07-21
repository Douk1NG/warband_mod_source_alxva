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

update_trade_good_price_for_party_scripts = [
("update_trade_good_price_for_party",
    [
      (store_script_param, ":center_no", 1),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
		(party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

        (call_script, "script_center_get_production", ":center_no", ":cur_good"),
		(assign, ":production", reg0),

        (call_script, "script_center_get_consumption", ":center_no", ":cur_good"),
		(assign, ":consumption", reg0),

		#OZANDEBUG
		#(assign, reg1, ":production"),
		#(assign, reg2, ":consumption"),
		#(str_store_party_name, s1, ":center_no"),
		#(str_store_item_name, s2, ":cur_good"),

		(val_sub, ":production", ":consumption"),

		#Change average production x 2(1+random(2)) (was average 4, random(8)) for excess demand
        (try_begin),
		  #supply is greater than demand
          (gt, ":production", 0),
		  (store_mul, ":change_factor", ":production", 1), #price will be decreased by his factor
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),

		  #simulation starts
          (store_sub, ":final_price", ":cur_price", ":random_change"),
		  (val_clamp, ":final_price", minimum_price_factor, maximum_price_factor),
		  (try_begin), #Excess of supply decelerates over time, as low price reduces output
		    #if expected final price is 100 then it will multiply random_change by 0.308x ((100+300)/(1300) = 400/1300).
			(lt, ":final_price", 1000),
			(store_add, ":final_price_plus_300", ":final_price", 300),
			(val_mul, ":random_change", ":final_price_plus_300"),
			(val_div, ":random_change", 1300),
		  (try_end),
          (val_sub, ":cur_price", ":random_change"),
        (else_try),
          (lt, ":production", 0),
		  (store_sub, ":change_factor", 0, ":production"), #price will be increased by his factor
		  (val_mul, ":change_factor", 1),
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
          (val_add, ":cur_price", ":random_change"),
        (try_end),

        #Move price towards average by 3%...
		#Equilibrium is 33 cycles, or 100 days
		#Change per cycle is Production x 4
		#Thus, max differential = -5 x 4 x 33 = -660 for -5
		(try_begin),
		  (is_between, ":center_no", villages_begin, villages_end),
        (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
        (val_div, ":price_difference", 100),
        (store_add, ":new_price", average_price_factor, ":price_difference"),
        (else_try),
          (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
          (val_div, ":price_difference", 100),
          (store_add, ":new_price", average_price_factor, ":price_difference"),
        (try_end),

		#Price of manufactured goods drift towards primary raw material
		(try_begin),
			(item_get_slot, ":raw_material", ":cur_good", slot_item_primary_raw_material),
            (neq, ":raw_material", 0),
	        (store_sub, ":raw_material_price_slot", ":raw_material", trade_goods_begin),
	        (val_add, ":raw_material_price_slot", slot_town_trade_good_prices_begin),

			(party_get_slot, ":total_raw_material_price", ":center_no", ":raw_material_price_slot"),
			(val_mul, ":total_raw_material_price", 3),
            (assign, ":number_of_centers", 3),

			(try_for_range, ":village_no", villages_begin, villages_end),
			  (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
			  (party_get_slot, ":raw_material_price", ":village_no", ":raw_material_price_slot"),
			  (val_add, ":total_raw_material_price", ":raw_material_price"),
			  (val_add, ":number_of_centers", 1),
            (try_end),

			(store_div, ":average_raw_material_price", ":total_raw_material_price", ":number_of_centers"),

			(gt, ":average_raw_material_price", ":new_price"),
			(store_sub, ":raw_material_boost", ":average_raw_material_price", ":new_price"),
			(val_div, ":raw_material_boost", 10),
			(val_add, ":new_price", ":raw_material_boost"),
		(try_end),

        (val_clamp, ":new_price", minimum_price_factor, maximum_price_factor),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":new_price"),

		#(assign, reg3, ":new_price"),
		#(str_store_item_name, s2, ":cur_good"),
		#(display_log_message, "@DEBUG : {s1}-{s2}, prod:{reg1}, cons:{reg2}, price:{reg3}"),
      (try_end),
  ])
]
