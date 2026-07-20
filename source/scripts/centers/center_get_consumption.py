# ======================================================================
# SHARED DEPENDENCY
# Entity: center_get_consumption (script)
# Called by menus in 2 domains: reports, village
# ======================================================================

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

center_get_consumption_scripts = [
("center_get_consumption",
    [
		(store_script_param_1, ":center_no"),
		(store_script_param_2, ":cur_good"),

		(assign, ":consumer_consumption", 0),
		(try_begin),
##diplomacy start+ To determine if a center should be counted as a desert center or not,
#instead of using a fixed range (which is brittle to map changes) check if the terrain
#at the center is rt_desert or rt_desert_forest.
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(is_between, ":center_no", centers_begin, centers_end),
			(party_get_current_terrain, reg0, ":center_no"),
			(this_or_next|eq, reg0, rt_desert),
			(eq, reg0, rt_desert_forest),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
#If economic changes are disabled, use the Native desert-check logic.
##diplomacy end+
			(this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),
				(ge, ":center_no", "p_village_91"),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
			(is_between, ":center_no", villages_begin, villages_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_rural_demand),
		(else_try),
			(is_between, ":center_no", towns_begin, towns_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_urban_demand),
		(try_end),


		(assign, ":raw_material_consumption", 0),
		(try_begin),
			(eq, ":cur_good", "itm_grain"),
			(party_get_slot, ":grain_for_bread", ":center_no", slot_center_mills),
			(val_mul, ":grain_for_bread", 20),

			(party_get_slot, ":grain_for_ale", ":center_no", slot_center_breweries),
			(val_mul, ":grain_for_ale", 5),

			(store_add, ":raw_material_consumption", ":grain_for_bread", ":grain_for_ale"),

		(else_try),
			(eq, ":cur_good", "itm_iron"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_smithies),
			(val_mul, ":raw_material_consumption", 3),

		(else_try),
			(eq, ":cur_good", "itm_wool"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_wool_looms),
			(val_mul, ":raw_material_consumption", 5),

		(else_try),
			(eq, ":cur_good", "itm_raw_flax"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_linen_looms),
			(val_mul, ":raw_material_consumption", 5),

		(else_try),
			(eq, ":cur_good", "itm_raw_leather"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_tanneries),
			(val_mul, ":raw_material_consumption", 20),

		(else_try),
			(eq, ":cur_good", "itm_raw_grapes"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_wine_presses),
			(val_mul, ":raw_material_consumption", 30),

		(else_try),
			(eq, ":cur_good", "itm_raw_olives"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_olive_presses),
			(val_mul, ":raw_material_consumption", 12),


		(else_try),
			(eq, ":cur_good", "itm_raw_dyes"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_silk_looms),
			(val_mul, ":raw_material_consumption", 1),
		(else_try),
			(eq, ":cur_good", "itm_raw_silk"),
			(party_get_slot, ":raw_material_consumption", ":center_no", slot_center_silk_looms),
			(val_mul, ":raw_material_consumption", 5),


		(else_try),
			(eq, ":cur_good", "itm_salt"),
			(party_get_slot, ":salt_for_beef", ":center_no", slot_center_head_cattle),
			(val_div, ":salt_for_beef", 10),

			(party_get_slot, ":salt_for_fish", ":center_no", slot_center_fishing_fleet),
			(val_div, ":salt_for_fish", 5),

			(store_add, ":raw_material_consumption", ":salt_for_beef", ":salt_for_fish"),
		(try_end),

		(try_begin), #Reduce consumption of raw materials if their cost is high
			(gt, ":raw_material_consumption", 0),
			(store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
	        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
	        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
			##diplomacy start+
			(gt, ":cur_center_price", average_price_factor),#replace the hardcoded constant 1000 with average_price_factor
			(val_mul, ":raw_material_consumption", average_price_factor),#again replace the hardcoded constant 1000 with average_price_factor
			##diplomacy end+
			(val_div, ":raw_material_consumption", ":cur_center_price"),
		(try_end),



		(store_add, ":modified_consumption", ":consumer_consumption", ":raw_material_consumption"),
		(try_begin),
			(party_get_slot, ":prosperity_plus_75", ":center_no", slot_town_prosperity),
			(val_add, ":prosperity_plus_75", 75),
			(val_mul, ":modified_consumption", ":prosperity_plus_75"),
			(val_div, ":modified_consumption", 125),
		(try_end),


	    (assign, reg0, ":modified_consumption"), #modded by prosperity
	    (assign, reg1, ":raw_material_consumption"),
	    (assign, reg2, ":consumer_consumption"),
	])
]
