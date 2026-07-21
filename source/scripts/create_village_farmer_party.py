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

create_village_farmer_party_scripts = [
# script_create_village_farmer_party
# Input: arg1 = village_no
# Output: reg0 = party_no
("create_village_farmer_party",
   [(store_script_param, ":village_no", 1),
    (party_get_slot, ":town_no", ":village_no", slot_village_market_town),
    (store_faction_of_party, ":party_faction", ":town_no"),


#    (store_faction_of_party, ":town_faction", ":town_no"),
#    (try_begin),
#		(neq, ":town_faction", ":party_faction"),
#		(assign, ":town_no", -1),
#		(assign, ":score_to_beat", 9999),
#		(try_for_range, ":other_town", towns_begin, towns_end),
#			(store_faction_of_party, ":other_town_faction", ":town_no"),
#			(store_relation, ":relation", ":other_town_faction", ":party_faction"),
#			(ge, ":relation", 0),

#			(store_distance_to_party_from_party, ":distance", ":village_no", ":other_town"),
#			(lt, ":distance", ":score_to_beat"),
#			(assign, ":town_no", ":other_town"),
#			(assign, ":score_to_beat", ":distance"),
#		(try_end),
#	(try_end),

	(try_begin),
		(is_between, ":town_no", towns_begin, towns_end),
	    (set_spawn_radius, 0),
	    (spawn_around_party, ":village_no", "pt_village_farmers"),
	    (assign, ":new_party", reg0),

	    (party_set_faction, ":new_party", ":party_faction"),
	    (party_set_slot, ":new_party", slot_party_home_center, ":village_no"),
	    (party_set_slot, ":new_party", slot_party_last_traded_center, ":village_no"),

	    (party_set_slot, ":new_party", slot_party_type, spt_village_farmer),
	    (party_set_slot, ":new_party", slot_party_ai_state, spai_trading_with_town),
	    (party_set_slot, ":new_party", slot_party_ai_object, ":town_no"),
	    (party_set_ai_behavior, ":new_party", ai_bhvr_travel_to_party),
	    (party_set_ai_object, ":new_party", ":town_no"),
	    (party_set_flags, ":new_party", pf_default_behavior, 0),
	    (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
	    (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	      (store_add, ":cur_good_price_slot", ":cur_goods", ":item_to_price_slot"),
	      (party_get_slot, ":cur_village_price", ":village_no", ":cur_good_price_slot"),
	      (party_set_slot, ":new_party", ":cur_good_price_slot", ":cur_village_price"),
	    (try_end),
	    (assign, reg0, ":new_party"),
	(try_end),

    ])
]
