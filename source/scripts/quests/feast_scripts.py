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

feast_scripts = [

("internal_politics_rate_feast_to_s9",
	[
	(store_script_param, ":householder", 1),
	(store_script_param, ":num_servings", 2),
#	(store_script_param, ":faction", 3),
	(store_script_param, ":consume_items", 4),

	(val_max, ":num_servings", 1),

	(try_for_range, ":item", trade_goods_begin, trade_goods_end),
		(item_set_slot, ":item", slot_item_amount_available, 0), #had no "item"
	(try_end),

	(troop_get_inventory_capacity, ":capacity", ":householder"),
	(try_for_range, ":inventory_slot", ek_food + 1, ":capacity"), #SB : skip equipment
		(troop_get_inventory_slot, ":item", ":householder", ":inventory_slot"),
		(is_between, ":item", trade_goods_begin, trade_goods_end),
	    (troop_inventory_slot_get_item_amount, ":slot_amount", ":householder", ":inventory_slot"),
        #SB : TODO : evaluate quality of food, for now just make sure it's not rotten
        (troop_get_inventory_slot_modifier, ":imod", ":householder", ":inventory_slot"),
        (neq, ":imod", imod_rotten),
		(item_get_slot, ":item_amount", ":item", slot_item_amount_available),
		(val_add, ":item_amount", ":slot_amount"),
		(item_set_slot, ":item", slot_item_amount_available, ":item_amount"),
	(try_end),
	#food
	(assign, ":food_amount", 0),
	(assign, ":food_variety", 0),

	(store_div, ":servings_div_by_12", ":num_servings", 12),
	(try_for_range, ":food_item", food_begin, food_end),
		(item_get_slot, ":food_in_slot", ":food_item", slot_item_amount_available),
		(val_add, ":food_amount", ":food_in_slot"),


##		(str_store_item_name, s4, ":food_item"),
##		(assign, reg3, ":food_in_slot"),
##		(assign, reg5, ":servings_div_by_12"),
##		(display_message, "str_reg3_units_of_s4_for_reg5_guests_and_retinue"),


		(ge, ":food_in_slot", ":servings_div_by_12"),
		(val_add, ":food_variety", 1),
	(try_end),

	(val_mul, ":food_amount", 100),
	(val_div, ":food_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":food_amount", 100),

	(val_mul, ":food_variety", 85), #1 to 100 for each
	(val_div, ":food_variety", 10),
	(val_min, ":food_variety", 100),

	#drink
	(assign, ":drink_amount", 0),
	(assign, ":drink_variety", 0),
	(store_div, ":servings_div_by_4", ":num_servings", 4),
	(try_for_range, ":drink_iterator", "itm_wine", "itm_smoked_fish"),
		(assign, ":drink_item", ":drink_iterator"),
		(item_get_slot, ":drink_in_slot", ":drink_item", slot_item_amount_available),

		(val_add, ":drink_amount", ":drink_in_slot"),

		(ge, ":drink_in_slot", ":servings_div_by_4"),
		(val_add, ":drink_variety", 1),
	(try_end),

	(val_mul, ":drink_amount", 200), #amount needed is 50% of the number of guests
	(val_max, ":num_servings", 1),

	(val_div, ":drink_amount", ":num_servings"), #1 to 100 for each
	(val_min, ":drink_amount", 100),
	(val_mul, ":drink_variety", 50), #1 to 100 for each

	#in the future, it might be worthwhile to add different varieties of spices
	(item_get_slot, ":spice_amount", "itm_spice", slot_item_amount_available),
	(store_mul, ":spice_percentage", ":spice_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":spice_amount", ":servings_div_by_12"),
	(val_min, ":spice_percentage", 100),
##	(assign, reg3, ":spice_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":spice_percentage"),
##	(display_message, "str_reg3_units_of_spice_of_reg5_to_be_consumed"),

	#oil availability. In the future, this may become an "atmospherics" category, including incenses
	(item_get_slot, ":oil_amount", "itm_oil", slot_item_amount_available),
	(store_mul, ":oil_percentage", ":oil_amount", 100),
	(val_max, ":servings_div_by_12", 1),
	(val_div, ":oil_amount", ":servings_div_by_12"),
	(val_min, ":oil_percentage", 100),
##	(assign, reg3, ":oil_amount"),
##	(assign, reg5, ":servings_div_by_12"),
##	(assign, reg6, ":oil_percentage"),
##	(display_message, "str_reg3_units_of_oil_of_reg5_to_be_consumed"),

    #SB : salt + date fruit probably useful too
	(store_div, ":food_amount_string", ":food_amount", 20),
	(val_add, ":food_amount_string", "str_feast_description"),
	(str_store_string, s8, ":food_amount_string"),
	(str_store_string, s9, "str_of_food_which_must_come_before_everything_else_the_amount_is_s8"),

	(store_div, ":food_variety_string", ":food_variety", 20),
	(val_add, ":food_variety_string", "str_feast_description"),
	(str_store_string, s8, ":food_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),

	(store_div, ":drink_amount_string", ":drink_amount", 20),
	(val_add, ":drink_amount_string", "str_feast_description"),
	(str_store_string, s8, ":drink_amount_string"),
	(str_store_string, s9, "str_s9_of_drink_which_guests_will_expect_in_great_abundance_the_amount_is_s8"),

	(store_div, ":drink_variety_string", ":drink_variety", 20),
	(val_add, ":drink_variety_string", "str_feast_description"),
	(str_store_string, s8, ":drink_variety_string"),
	(str_store_string, s9, "str_s9_and_the_variety_is_s8_"),

	(store_div, ":spice_string", ":spice_percentage", 20),
	(val_add, ":spice_string", "str_feast_description"),
	(str_store_string, s8, ":spice_string"),
	(str_store_string, s9, "str_s9_of_spice_which_is_essential_to_demonstrate_that_we_spare_no_expense_as_hosts_the_amount_is_s8_"),

	(store_div, ":oil_string", ":oil_percentage", 20),
	(val_add, ":oil_string", "str_feast_description"),
	(str_store_string, s8, ":oil_string"),
	(str_store_string, s9, "str_s9_of_oil_which_we_shall_require_to_light_the_lamps_the_amount_is_s8"),

	(store_mul, ":food_amount_cap", ":food_amount", 8),
	(store_add, ":total", ":food_amount", ":food_variety"),
	(val_mul, ":total", 2), #x4
	(val_add, ":total", ":drink_variety"),
	(val_add, ":total", ":drink_amount"), #x6
	(val_add, ":total", ":spice_amount"), #x7
	(val_add, ":total", ":oil_amount"), #x8
	(val_min, ":total", ":food_amount_cap"),
	(val_div, ":total", 8),
	(val_clamp, ":total", 1, 101),
	(store_div, ":total_string", ":total", 20),
	(val_add, ":total_string", "str_feast_description"),
	(str_store_string, s8, ":total_string"),
	(str_store_string, s9, "str_s9_overall_our_table_will_be_considered_s8"),

	(assign, reg0, ":total"), #zero to 100



	(try_begin),
		(eq, ":consume_items", 1),

		(assign, ":num_of_servings_to_serve", ":num_servings"),
		(try_for_range, ":unused", 0, 1999),
			(gt, ":num_of_servings_to_serve", 0),

			(try_for_range, ":item", trade_goods_begin, trade_goods_end),
				(item_set_slot, ":item", slot_item_is_checked, 0),
			(try_end),

			(troop_get_inventory_capacity, ":inv_size", ":householder"),
			(try_for_range, ":i_slot", 0, ":inv_size"),
				(troop_get_inventory_slot, ":item", ":householder", ":i_slot"),
				(this_or_next|eq, ":item", "itm_spice"),
				(this_or_next|eq, ":item", "itm_oil"),
				(this_or_next|eq, ":item", "itm_wine"),
				(this_or_next|eq, ":item", "itm_ale"),
					(is_between, ":item",  food_begin, food_end),
				(item_slot_eq, ":item", slot_item_is_checked, 0),
				(troop_inventory_slot_get_item_amount, ":cur_amount", ":householder", ":i_slot"),
				(gt, ":cur_amount", 0),

				(val_sub, ":cur_amount", 1),
				(troop_inventory_slot_set_item_amount, ":householder", ":i_slot", ":cur_amount"),
				(val_sub, ":num_of_servings_to_serve", 1),
				(item_set_slot, ":item", slot_item_is_checked, 1),
			(try_end),
                ##diplomacy start+ Fix Native bug: "try_begin" to "try_end"
		#(try_begin),
                (try_end),
                ##diplomacy end+
	(try_end),
	]),
]