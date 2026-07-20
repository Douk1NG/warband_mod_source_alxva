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

center_get_goods_availability_scripts = [
#this determines whether or not a lord is thrown into a dungeon by his captor, or is kept out on parole
("center_get_goods_availability",
	[
	(store_script_param, ":center_no", 1),

	(str_store_party_name, s4, ":center_no"),
	##diplomacy start+ Determine whether the center should use "desert" consumption values.
  	#Native uses the following logic:
	#  (this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),
	#  (ge, ":center_no", "p_village_91"),
	##This is very vulnerable to map changes, though, so I would prefer to check the terrain type.
	(party_get_current_terrain, ":terrain_type", ":center_no"),
	(try_begin),
	   (eq, reg0, rt_desert_forest),
	   (assign, ":terrain_type", rt_desert),
	(try_end),
	(try_begin),
	   (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	   #To be consistent with script_center_get_consumption and script_initialize_economic_information
	   #use the Native desert-determination scheme when economic changes are disabled.
	   (assign, ":terrain_type", rt_plain),
  	   (this_or_next|is_between, ":center_no", "p_town_19", "p_castle_1"),
	   (ge, ":center_no", "p_village_91"),
	   (assign, ":terrain_type", rt_desert),
	(try_end),
	##diplomacy end+

	(assign, ":hardship_index", 0),
	(try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),

		#Must have consumption of at least 4 to be relevant
		#This prevents perishables and raw materials from having a major impact
		(try_begin),
		##diplomacy start+ Use the "desert" slot when applicable
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(eq, ":terrain_type", rt_desert),
			(item_slot_ge, ":cur_good", slot_item_desert_demand, 0), #Otherwise use rural or urban
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_desert_demand),
		(else_try),
		##diplomacy end+
			(is_between, ":center_no", villages_begin, villages_end),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_rural_demand),
		(else_try),
			(item_get_slot, ":consumer_consumption", ":cur_good", slot_item_urban_demand),
		(try_end),
		(gt, ":consumer_consumption", 2),

		(store_div, ":max_impact", ":consumer_consumption", 4), #was 4, dropped 3 again 4 now

		#High-demand items like grain tend to have much more dramatic price differentiation, so they yield substantially higher results than low-demand items

        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price", ":center_no", ":cur_good_price_slot"),

		(store_sub, ":price_differential", ":price", 1000),
		(gt, ":price_differential", 200), #was 100

		(val_div, ":price_differential", 200),
		(val_min, ":price_differential", ":max_impact"),

		(val_add, ":hardship_index", ":price_differential"),
	(try_end),

	(assign, reg0, ":hardship_index"),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "@{!}DEBUG -- hardship index for {s4} = {reg0}"),
	(try_end),
	])
]
