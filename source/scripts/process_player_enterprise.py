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

process_player_enterprise_scripts = [
("process_player_enterprise",
    #reg0: Profit per cycle
	##diplomacy start+
	#Actual documentation of original parameters and outputs.
	# INPUTS:
	#   arg1: item_type
	#   arg2: center
	# OUTPUTS:
    #   reg0:  profit_per_cycle"),
	#   reg1:  final_price_for_total_produced_goods"),
	#   reg2:  final_price_for_total_inputs"),
	#   reg3:  price_of_labor"),
	#   reg4:  final_price_for_single_produced_good"),
	#   reg5:  final_price_for_single_input"),
	#	reg10: final_price_for_secondary_input"),
	#
	# Further, if experimental changes are enabled, modify the price.
	##diplomacy end+
	[
	  (store_script_param, ":item_type", 1),
	  (store_script_param, ":center", 2),

	  (item_get_slot, ":price_of_labor", ":item_type", slot_item_overhead_per_run),

	  (item_get_slot, ":base_price", ":item_type", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":item_type", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_produced_good", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_produced_good", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_outputs_produced", ":item_type", slot_item_output_per_run),
	  (store_mul, ":final_price_for_total_produced_goods", ":number_of_outputs_produced", ":final_price_for_single_produced_good"),

	  (item_get_slot, ":primary_raw_material", ":item_type", slot_item_primary_raw_material),
	  (item_get_slot, ":base_price", ":primary_raw_material", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":primary_raw_material", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		 (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":primary_raw_material", ":center"),
		 (val_max, ":cur_price_modifier", reg0),
	  (try_end),
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_input", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_input", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_inputs_required", ":item_type", slot_item_input_number),
	  (try_begin),
	    (lt, ":number_of_inputs_required", 0),
	    (store_div, ":final_price_for_total_inputs", ":final_price_for_single_input", 2),
	  (else_try),
	    (store_mul, ":final_price_for_total_inputs", ":final_price_for_single_input", ":number_of_inputs_required"),
	  (try_end),

	  (try_begin),
	    (item_slot_ge, ":item_type", slot_item_secondary_raw_material, 1),
	    (item_get_slot, ":secondary_raw_material", ":item_type", slot_item_secondary_raw_material),
	    (item_get_slot, ":base_price", ":secondary_raw_material", slot_item_base_price),
	    (store_sub, ":cur_good_price_slot", ":secondary_raw_material", trade_goods_begin),
	    (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	    (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
		##diplomacy start+
		(try_begin),
	      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		  (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":secondary_raw_material", ":center"),
		  (val_max, ":cur_price_modifier", reg0),
	    (try_end),
	    (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
		##diplomacy end+
		(store_mul, ":final_price_for_secondary_input", ":base_price", ":cur_price_modifier"),#fixes
	    (try_begin),
	      (lt, ":number_of_inputs_required", 0),
	      (val_div, ":final_price_for_secondary_input", 2),
	    (else_try),
	      (val_mul, ":final_price_for_secondary_input", ":number_of_inputs_required"),
	    (try_end),

		##diplomacy start+
	    (val_div, ":final_price_for_secondary_input", average_price_factor),#Replaced "1000" with "average_price_factor"
		##diplomacy end+
	  (else_try),
	    (assign, ":final_price_for_secondary_input", 0),
	  (try_end),

	  #Scale production by town prosperity tier (rich towns produce more, poor towns less; overhead stays fixed)
	  (call_script, "script_get_enterprise_prosperity_numerator", ":center"),
	  (assign, ":prosperity_num", reg0),
	  (val_mul, ":final_price_for_total_produced_goods", ":prosperity_num"),
	  (val_div, ":final_price_for_total_produced_goods", 100),
	  (val_mul, ":final_price_for_total_inputs", ":prosperity_num"),
	  (val_div, ":final_price_for_total_inputs", 100),
	  (val_mul, ":final_price_for_secondary_input", ":prosperity_num"),
	  (val_div, ":final_price_for_secondary_input", 100),

	  (store_sub, ":profit_per_cycle", ":final_price_for_total_produced_goods", ":final_price_for_total_inputs"),
	  (val_sub, ":profit_per_cycle", ":price_of_labor"),
	  (val_sub, ":profit_per_cycle", ":final_price_for_secondary_input"),

	  (assign, reg0, ":profit_per_cycle"),
	  (assign, reg1, ":final_price_for_total_produced_goods"),
	  (assign, reg2, ":final_price_for_total_inputs"),
	  (assign, reg3, ":price_of_labor"),
	  (assign, reg4, ":final_price_for_single_produced_good"),
	  (assign, reg5, ":final_price_for_single_input"),
	  (assign, reg10, ":final_price_for_secondary_input"),
	])
]
