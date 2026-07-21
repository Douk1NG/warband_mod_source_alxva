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

update_trade_good_prices_scripts = [
#script_update_trade_good_prices
# INPUT: none
("update_trade_good_prices",
    [
      (try_for_range, ":center_no", centers_begin, centers_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (call_script, "script_update_trade_good_price_for_party", ":center_no"),
      (try_end),

      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (assign, ":total_price", 0),
		(assign, ":total_constants", 0),

	    (try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),

          (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
          (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
          (party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

		  (try_begin),
		    (is_between, ":center_no", towns_begin, towns_end),
			(assign, ":constant", 5),
          (else_try),
		    (assign, ":constant", 1),
		  (try_end),

		  (val_mul, ":cur_price", ":constant"),

		  (val_add, ":total_price", ":cur_price"),
		  (val_add, ":total_constants", ":constant"),
		(try_end),

		(try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),

          (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
          (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
          (party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

		  (val_mul, ":cur_price", 1000),
		  (val_mul, ":cur_price", ":total_constants"),
		  (val_div, ":cur_price", ":total_price"),

		  (val_clamp, ":cur_price", minimum_price_factor, maximum_price_factor),
		  (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_price"),
		(try_end),
      (try_end),
  ])
]
