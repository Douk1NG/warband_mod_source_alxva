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

good_price_affects_good_production_scripts = [
#script_update_trade_good_price_for_party
("good_price_affects_good_production",
	[
	(store_script_param, ":center", 1),
	(store_script_param, ":input_item_no", 2),
	(store_script_param, ":production", 3),
	(store_script_param, ":impact_divisor", 4),

	(assign, reg4, ":production"),

	(try_begin),
		(gt, ":production", 0), #let's take -20 as the zero production rate, although in actuality production can go lower, representing increased demand

		(store_sub, ":input_good_price_slot", ":input_item_no", trade_goods_begin),
		(val_add, ":input_good_price_slot", slot_town_trade_good_prices_begin),
		(party_get_slot, ":input_price", ":center", ":input_good_price_slot"),

		(try_begin),
		  (is_between, ":center", towns_begin, towns_end),

		  (val_mul, ":input_price", 4),
		  (assign, ":number_of_villages", 4),
		  (try_for_range, ":village_no", villages_begin, villages_end),
		    (party_slot_eq, ":village_no", slot_village_bound_center, ":center"),
		    (party_get_slot, ":input_price_at_village", ":village_no", ":input_good_price_slot"),
			(val_add, ":input_price", ":input_price_at_village"),
			(val_add, ":number_of_villages", 1),
		  (try_end),

		  (val_div, ":input_price", ":number_of_villages"),
		(try_end),

		(try_begin), #1/2 impact for low prices
			##diplomacy start+
			(lt, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			##diplomacy end+
			(val_mul, ":impact_divisor", 2),
		(try_end),

		(try_begin),
			(gt, ":impact_divisor", 1),
			##diplomacy start+
			(val_sub, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			(val_div, ":input_price", ":impact_divisor"),#<- unchanged
			(val_add, ":input_price", average_price_factor),#Replace 1000 with average_price_factor
			##diplomacy end+
		(try_end),

		##diplomacy start+
		(val_mul, ":production", average_price_factor),#Replace 1000 with average_price_factor
		##diplomacy end+
		(val_div, ":production", ":input_price"),

#		(assign, reg5, ":production"),
		#(assign, reg3, ":input_price"),
#		(str_store_item_name, s4, ":input_item_no"),
#		(display_message, "@{s4} price of {reg3} reduces production from {reg4} to {reg5}"),

	(try_end),


	(assign, reg0, ":production"),

	])
]
