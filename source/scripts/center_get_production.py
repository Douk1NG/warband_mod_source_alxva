# ======================================================================
# SHARED DEPENDENCY
# Entity: center_get_production (script)
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

center_get_production_scripts = [
#script_center_change_trade_good_production
("center_get_production",
    [
	#Actually, this could be reset somewhat to yield supply and demand as raw numbers
	#Demand could be set values for rural and urban
	#Supply could be based on capital goods -- head of cattle, head of sheep, fish ponds, fishing fleets, acres of grain fields, olive orchards, olive presses, wine presses, mills, smithies, salt pans, potters' kilns, etc
	#Prosperity would increase both demand and supply
		(store_script_param_1, ":center_no"),
		(store_script_param_2, ":cur_good"),

		(assign, ":base_production", 0),

		#Grain products
		(try_begin),
			(eq, ":cur_good", "itm_bread"), #Demand = 3000 across Calradia
			(party_get_slot, ":base_production", ":center_no", slot_center_mills),
			(val_mul, ":base_production", 20), #one mills per village, five mills per town = 160 mills
		(else_try),
			(eq, ":cur_good", "itm_grain"), #Demand =  3200+, 1600 to mills, 1500 on its own, extra to breweries
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_grain),
			(val_div, ":base_production", 125), #10000 acres is the average across Calradia, extra in Swadia, less in snows and steppes, a bit from towns
		(else_try),
			(eq, ":cur_good", "itm_ale"), #
			(party_get_slot, ":base_production", ":center_no", slot_center_breweries),
			(val_mul, ":base_production", 25),

		(else_try),
			(eq, ":cur_good", "itm_smoked_fish"), #Demand = 20
			(party_get_slot, ":base_production", ":center_no", slot_center_fishing_fleet),
			(val_mul, ":base_production", 4), #was originally 5
		(else_try),
			(eq, ":cur_good", "itm_salt"),
			(party_get_slot, ":base_production", ":center_no", slot_center_salt_pans),
			(val_mul, ":base_production", 35),

		#Cattle products
		(else_try),
			(eq, ":cur_good", "itm_cattle_meat"), #Demand = 5
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(val_div, ":base_production", 4), #was 9
		(else_try),
			(eq, ":cur_good", "itm_dried_meat"), #Demand = 15
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(val_div, ":base_production", 2), #was 3
		(else_try),
			(eq, ":cur_good", "itm_cheese"), 	 #Demand = 10
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(party_get_slot, ":sheep_addition", ":center_no", slot_center_head_sheep),
			(val_div, ":sheep_addition", 2),
			(val_add, ":base_production", ":sheep_addition"),
			(party_get_slot, ":gardens", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", ":gardens"),
			(val_div, ":base_production", 10),
		(else_try),
			(eq, ":cur_good", "itm_butter"), 	 #Demand = 2
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(party_get_slot, ":gardens", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", ":gardens"),
			(val_div, ":base_production", 15),

		(else_try),
			(eq, ":cur_good", "itm_raw_leather"), 	 #Demand = ??
			(party_get_slot, ":base_production", ":center_no", slot_center_head_cattle),
			(val_div, ":base_production", 6),
			(party_get_slot, ":sheep_addition", ":center_no", slot_center_head_sheep),
			(val_div, ":sheep_addition", 12),
			(val_add, ":base_production", ":sheep_addition"),

		(else_try),
			(eq, ":cur_good", "itm_leatherwork"), 	 #Demand = ??
			(party_get_slot, ":base_production", ":center_no", slot_center_tanneries),
			(val_mul, ":base_production", 20),

		(else_try),
			(eq, ":cur_good", "itm_honey"), 	 #Demand = 5
			(party_get_slot, ":base_production", ":center_no", slot_center_apiaries),
			(val_mul, ":base_production", 6),
		(else_try),
			(eq, ":cur_good", "itm_cabbages"), 	 #Demand = 7
			(party_get_slot, ":base_production", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", 10),
		(else_try),
			(eq, ":cur_good", "itm_apples"), 	 #Demand = 7
			(party_get_slot, ":base_production", ":center_no", slot_center_household_gardens),
			(val_mul, ":base_production", 10),

		#Sheep products
		(else_try),
			(eq, ":cur_good", "itm_sausages"), 	 #Demand = 5
			(party_get_slot, ":base_production", ":center_no", slot_center_head_sheep), #average of 90 sheep
			(val_div, ":base_production", 15),
		(else_try),
			(eq, ":cur_good", "itm_wool"), 	 #(Demand = 0, but 15 averaged out perhaps)
			(party_get_slot, ":base_production", ":center_no", slot_center_head_sheep), #average of 90 sheep
			(val_div, ":base_production", 5),
		(else_try),
			(eq, ":cur_good", "itm_wool_cloth"), 	 #(Demand = 1500 across Calradia)
			(party_get_slot, ":base_production", ":center_no", slot_center_wool_looms),
			(val_mul, ":base_production", 5), #300 across Calradia

		(else_try),
			(this_or_next|eq, ":cur_good", "itm_pork"),
			(eq, ":cur_good", "itm_chicken"),
			(try_begin),
			  (is_between, ":center_no", villages_begin, villages_end),
			  (assign, ":base_production", 30),
			(else_try),
			  (assign, ":base_production", 0),
			(try_end),

		(else_try),
			(eq, ":cur_good", "itm_iron"), 	 #Demand = 5, one supplies three smithies
			(party_get_slot, ":base_production", ":center_no", slot_center_iron_deposits),
			(val_mul, ":base_production", 10),
		(else_try),
			(eq, ":cur_good", "itm_tools"), 	 #Demand = 560 across Calradia
			(party_get_slot, ":base_production", ":center_no", slot_center_smithies),
			(val_mul, ":base_production", 3),

		#Other artisanal goods
		(else_try),
			(eq, ":cur_good", "itm_pottery"), #560 is total demand
			(party_get_slot, ":base_production", ":center_no", slot_center_pottery_kilns),
			(val_mul, ":base_production", 5),

		(else_try),
			(eq, ":cur_good", "itm_raw_grapes"),
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_vineyard),
			(val_div, ":base_production", 100),
		(else_try),
			(eq, ":cur_good", "itm_wine"),
			(party_get_slot, ":base_production", ":center_no", slot_center_wine_presses),
			(val_mul, ":base_production", 25),
		(else_try),
			(eq, ":cur_good", "itm_raw_olives"),
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_olives),
			(val_div, ":base_production", 150),
		(else_try),
			(eq, ":cur_good", "itm_oil"),
			(party_get_slot, ":base_production", ":center_no", slot_center_olive_presses),
			(val_mul, ":base_production", 12),

		#Flax and linen
		(else_try),
			(eq, ":cur_good", "itm_linen"),
			(party_get_slot, ":base_production", ":center_no", slot_center_linen_looms),
			(val_mul, ":base_production", 5),
		(else_try),
			(eq, ":cur_good", "itm_raw_flax"),
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_flax),
			(val_div, ":base_production", 80),
		(else_try),
			(eq, ":cur_good", "itm_velvet"),
			(party_get_slot, ":base_production", ":center_no", slot_center_silk_looms),
			(val_mul, ":base_production", 5),
		(else_try),
			(eq, ":cur_good", "itm_raw_silk"),
			(party_get_slot, ":base_production", ":center_no", slot_center_silk_farms),
			(val_div, ":base_production", 20),
		(else_try),
			(eq, ":cur_good", "itm_raw_dyes"),
			(party_get_slot, ":base_production", ":center_no", slot_center_kirmiz_farms),
			(val_div, ":base_production", 20),
		(else_try),
			(eq, ":cur_good", "itm_raw_date_fruit"),
			(party_get_slot, ":base_production", ":center_no", slot_center_acres_dates),
			(val_div, ":base_production", 120),
		(else_try),
			(eq, ":cur_good", "itm_furs"), 	 #Demand = 90 across Calradia
			(party_get_slot, ":base_production", ":center_no", slot_center_fur_traps),
			(val_mul, ":base_production", 25),
		(else_try),
			(eq, ":cur_good", "itm_spice"),
			(try_begin),
				(eq, ":center_no", "p_town_10"), #Tulga
				(assign, ":base_production", 100),
			(else_try),
				(eq, ":center_no", "p_town_17"), #Ichamur
				(assign, ":base_production", 50),
			(else_try),
				(eq, ":center_no", "p_town_19"), #Shariz
				(assign, ":base_production", 50),
			(else_try),
				(eq, ":center_no", "p_town_22"), #Bariyye
				(assign, ":base_production", 50),
			(else_try),
				(this_or_next|eq, ":center_no", "p_village_11"), #Dusturil (village of Tulga)
				(eq, ":center_no", "p_village_25"), #Dashbigha (village of Tulga)
				(assign, ":base_production", 50),
			(else_try),
				(this_or_next|eq, ":center_no", "p_village_37"), #Ada Kulun (village of Ichlamur)
				(this_or_next|eq, ":center_no", "p_village_42"), #Dirigh Aban (village of Ichlamur)
				(this_or_next|eq, ":center_no", "p_village_99"), #Fishara (village of Bariyye)
				(eq, ":center_no", "p_village_100"), #Iqbayl (village of Bariyye)
				(assign, ":base_production", 25),
			(try_end),
		(try_end),

		#Modify production by other goods
		(assign, ":modified_production", ":base_production"),
		(try_begin),
			(eq, ":cur_good", "itm_bread"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_grain", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_ale"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_grain", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_dried_meat"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_salt", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_smoked_fish"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_salt", ":base_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_tools"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_iron", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_wool_cloth"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_wool", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_wine"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_grapes", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_oil"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_olives", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_velvet"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_silk", ":base_production", 1),
			(assign, ":initially_modified_production", reg0),

			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_dyes", ":initially_modified_production", 2),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_leatherwork"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_leather", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(else_try),
			(eq, ":cur_good", "itm_linen"),
			(call_script, "script_good_price_affects_good_production", ":center_no", "itm_raw_flax", ":base_production", 1),
			(assign, ":modified_production", reg0),
		(try_end),


		(assign, ":base_production_modded_by_raw_materials", ":modified_production"), #this is just logged for the report screen

	    #Increase both positive and negative production by the center's prosperity
		#Richer towns have more people and consume more, but also produce more
		(try_begin),
			(party_get_slot, ":prosperity_plus_75", ":center_no", slot_town_prosperity),
			(val_add, ":prosperity_plus_75", 75),
			(val_mul, ":modified_production", ":prosperity_plus_75"),
			(val_div, ":modified_production", 125),
		(try_end),

		(try_begin),
		    (this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
		    (this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_deserted), #SB : deserted village
		        (party_slot_eq, ":center_no", slot_village_state, svs_looted),
		    (assign, ":modified_production", 0),
		(try_end),

	    (assign, reg0, ":modified_production"), #modded by prosperity
	    (assign, reg1, ":base_production_modded_by_raw_materials"),
	    (assign, reg2, ":base_production"),

	])
]
