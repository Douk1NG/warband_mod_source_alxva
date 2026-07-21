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

average_trade_good_prices_2_scripts = [
("average_trade_good_prices_2", #Called from start
    [

	#This should be done by route rather than distance
      (store_sub, ":item_to_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

      (try_for_range, ":center_no", towns_begin, towns_end),
        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":other_center", towns_begin, towns_end),
			(is_between, ":other_center", villages_begin, villages_end),

		  (this_or_next|party_slot_eq, ":other_center", slot_village_market_town, ":center_no"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_1, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_2, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_3, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_4, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_5, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_6, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_7, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_8, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_9, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_10, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_11, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_12, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_13, ":other_center"),
		  (this_or_next|party_slot_eq, ":center_no", slot_town_trade_route_14, ":other_center"),
			(party_slot_eq, ":center_no", slot_town_trade_route_15, ":other_center"),

#          (neq, ":other_center", ":center_no"),
#          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
#          (lt, ":cur_distance", 50), #Reduced from 110
#          (store_sub, ":dist_factor", 50, ":cur_distance"),

          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_price", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_price", ":other_center", ":cur_good_slot"),
            (store_sub, ":price_dif", ":center_price", ":other_center_price"),

			(store_div, ":price_dif_change", ":price_dif", 5), #this is done twice, reduced from 4
#            (assign, ":price_dif_change", ":price_dif"),

#            (val_mul ,":price_dif_change", ":dist_factor"),
#            (val_div ,":price_dif_change", 500), #Maximum of 1/10 per center
            (val_add, ":other_center_price", ":price_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_price"),

            (val_sub, ":center_price", ":price_dif_change"),
            (party_set_slot, ":center_no", ":cur_good_slot", ":center_price"),

          (try_end),
        (try_end),
      (try_end),
  ])
]
