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

merchant_road_info_to_s42_scripts = [
("merchant_road_info_to_s42", #also does itemss to s32
    [
	(store_script_param, ":center", 1),

	(assign, ":last_bandit_party_found", -1),
	(assign, ":last_bandit_party_origin", -1),
	(assign, ":last_bandit_party_destination", -1),
	(assign, ":last_bandit_party_hours_ago", -1),

	(str_clear, s32),

	(str_clear, s42),
	(str_clear, s47), #safe roads

	(try_for_range, ":center_to_reset", centers_begin, centers_end),
		(party_set_slot, ":center_to_reset", slot_party_temp_slot_1, 0),
	(try_end),

	(assign, ":road_attacks", 0),
	(assign, ":trades", 0),

#first mention all attacks
    (try_for_range, ":log_entry_iterator", 0, "$num_log_entries"),
		(store_sub, ":log_entry_no", "$num_log_entries", ":log_entry_iterator"),
#how long ago?
        (this_or_next|troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),

#       reference - (call_script, "script_add_log_entry", logent_traveller_attacked, ":winner_party" (actor),  ":origin" (center object), ":destination" (troop_object), ":winner_faction"),

        (troop_get_slot, ":origin",         "trp_log_array_center_object",         ":log_entry_no"),
        (troop_get_slot, ":destination",    "trp_log_array_troop_object",          ":log_entry_no"),

		(this_or_next|eq, ":origin", ":center"),
			(eq, ":destination", ":center"),


        (troop_get_slot, ":event_time",            "trp_log_array_entry_time",              ":log_entry_no"),
		(store_current_hours, ":cur_hour"),
		(store_sub, ":hours_ago", ":cur_hour", ":event_time"),
		(assign, reg3, ":hours_ago"),

		(lt, ":hours_ago", 672), #four weeks

		(try_begin),
			(eq, "$cheat_mode", 1),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(display_message, "str_attack_on_travellers_found_reg3_hours_ago"),
		(else_try),
			(eq, "$cheat_mode", 1),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
			(display_message, "str_trade_event_found_reg3_hours_ago"),
		(try_end),

		(try_begin), #possibly make script -- get_colloquial_for_time
			(lt, ":hours_ago", 24),
			(str_store_string, s46, "str_a_short_while_ago"),
		(else_try),
			(lt, ":hours_ago", 48),
			(str_store_string, s46, "str_one_day_ago"),
		(else_try),
			(lt, ":hours_ago", 72),
			(str_store_string, s46, "@two days ago"),
		(else_try),
			(lt, ":hours_ago", 154),
			(str_store_string, s46, "str_earlier_this_week"),
		(else_try),
			(lt, ":hours_ago", 240),
			(str_store_string, s46, "str_about_a_week_ago"),
		(else_try),
			(lt, ":hours_ago", 480),
			(str_store_string, s46, "str_about_two_weeks_ago"),
		(else_try),
			(str_store_string, s46, "str_several_weeks_ago"),
		(try_end),



        (troop_get_slot, ":actor", "trp_log_array_actor", ":log_entry_no"),
        (troop_get_slot, ":faction_object", "trp_log_array_faction_object", ":log_entry_no"),

		(str_store_string, s39, "str_unknown_assailants"),
		(assign, ":assailants_known", -1),
		(try_begin),
			(party_is_active, ":actor"),
			(store_faction_of_party, ":actor_faction", ":actor"),
			(eq, ":faction_object", ":actor_faction"),
			(assign, ":assailants_known", ":actor"),
			(str_store_party_name, s39, ":assailants_known"),
			(assign, "$g_bandit_party_for_bounty", -1),
			(try_begin), #possibly make script -- get_colloquial_for_faction
				(eq, ":faction_object", "fac_kingdom_1"),
				(str_store_string, s39, "str_swadians"),
			(else_try),
				(eq, ":faction_object", "fac_kingdom_2"),
				(str_store_string, s39, "str_vaegirs"),
			(else_try),
				(eq, ":faction_object", "fac_kingdom_3"),
				(str_store_string, s39, "str_khergits"),
			(else_try),
				(eq, ":faction_object", "fac_kingdom_4"),
				(str_store_string, s39, "str_nords"),
			(else_try),
				(eq, ":faction_object", "fac_kingdom_5"),
				(str_store_string, s39, "str_rhodoks"),
			(else_try),
				(eq, ":faction_object", "fac_kingdom_6"),
				(str_store_string, s39, "str_sarranids"),
			(else_try),
				(eq, ":faction_object", "fac_player_supporters_faction"),
				(str_store_string, s39, "str_your_followers"),
			(else_try), #bandits
				(assign, ":last_bandit_party_found", ":assailants_known"),
				(assign, ":last_bandit_party_origin", ":origin"),
				(assign, ":last_bandit_party_destination", ":destination"),
				(assign, ":last_bandit_party_hours_ago", ":hours_ago"),
			(try_end),
		(try_end),

		(try_begin),
			(eq, ":origin", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(party_slot_eq, ":destination", slot_party_temp_slot_1, 0),

			(party_set_slot, ":destination", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":destination"),
			(str_store_string, s44, "str_we_have_heard_that_travellers_heading_to_s40_were_attacked_on_the_road_s46_by_s39"),
			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":road_attacks", 1),
			#travellers were attacked on the road to...
		(else_try),
			(eq, ":destination", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_traveller_attacked),
			(party_slot_eq, ":origin", slot_party_temp_slot_1, 0),

			(party_set_slot, ":origin", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":origin"),
			(str_store_string, s44, "str_we_have_heard_that_travellers_coming_from_s40_were_attacked_on_the_road_s46_by_s39"),

			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":road_attacks", 1),

		#travellers from here traded at...
#		(else_try),
#			(eq, ":origin", ":center"),
#			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
#			(party_slot_eq, ":destination", slot_party_temp_slot_1, 0),

#			(party_set_slot, ":destination", slot_party_temp_slot_1, 1),
#			(str_store_party_name, s40, ":destination"),
#			(str_store_string, s44, "@Travellers headed to {s40} traded there {s46}"),
#			(str_store_string, s43, "@{s42"),
#			(str_store_string, s42, "str_s43_s44"),

			#caravan from traded at...
		(else_try),
			(eq, ":destination", ":center"),
			(troop_slot_eq, "trp_log_array_entry_type", ":log_entry_no", logent_party_traded),
			(party_slot_eq, ":origin", slot_party_temp_slot_1, 0),

			(party_set_slot, ":origin", slot_party_temp_slot_1, 1),
			(str_store_party_name, s40, ":origin"),
			(str_store_string, s44, "str_travellers_coming_from_s40_traded_here_s46"),
			(str_store_string, s43, "str_s42"),
			(str_store_string, s42, "str_s43_s44"),

			(val_add, ":trades", 1),

			#caravan from traded at...
		(try_end),

	(try_end),


	(try_begin),
		(le, ":trades", 2),
		(eq, ":road_attacks", 0),
		(store_current_hours, ":hours"),
		(lt, ":hours", 168),
		(str_store_string, s42, "str_it_is_still_early_in_the_caravan_season_so_we_have_seen_little_tradings42"),
	(else_try),
		(eq, ":trades", 0),
		(eq, ":road_attacks", 0),
		(str_store_string, s42, "str_there_has_been_very_little_trading_activity_here_recentlys42"),
	(else_try),
		(le, ":trades", 2),
		(eq, ":road_attacks", 0),
		(str_store_string, s42, "str_there_has_some_trading_activity_here_recently_but_not_enoughs42"),
	(else_try),
		(le, ":trades", 2),
		(le, ":road_attacks", 2),
		(str_store_string, s42, "str_there_has_some_trading_activity_here_recently_but_the_roads_are_dangerouss42"),
	(else_try),
		(ge, ":road_attacks", 3),
		(str_store_string, s42, "str_the_roads_around_here_are_very_dangerouss42"),
	(else_try),
		(ge, ":road_attacks", 1),
		(str_store_string, s42, "str_we_have_received_many_traders_in_town_here_although_there_is_some_danger_on_the_roadss42"),
	(else_try),
		(str_store_string, s42, "str_we_have_received_many_traders_in_town_heres42"),
	(try_end),

#do safe roads
	(assign, ":unused_trade_route_found", 0),
	(try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
		(party_get_slot, ":trade_center", ":center", ":trade_route_slot"),
		(is_between, ":trade_center", centers_begin, centers_end),

		(party_slot_eq, ":trade_center", slot_party_temp_slot_1, 0),

#		(party_get_slot, ":town_lord", ":trade_center", slot_town_lord),

		(str_store_party_name, s41, ":trade_center"),
		(try_begin),
			(eq, ":unused_trade_route_found", 1),
			(str_store_string, s44, "str_s44_s41"),
		(else_try),
			(str_store_string, s44, "str_s41"),
		(try_end),
		(assign, ":unused_trade_route_found", 1),
	(try_end),
	(try_begin),
		(eq, ":unused_trade_route_found", 1),
		(str_store_string, s47, "str_there_is_little_news_about_the_caravan_routes_to_the_towns_of_s44_and_nearby_parts_but_no_news_is_good_news_and_those_are_therefore_considered_safe"),
	(try_end),

	(assign, ":safe_village_road_found", 0),
	(try_for_range, ":village", villages_begin, villages_end),
		(party_slot_eq, ":village", slot_village_market_town, ":center"),
		(party_slot_eq, ":village", slot_party_temp_slot_1, 0),

#		(party_get_slot, ":town_lord", ":village", slot_town_lord),
		(str_store_party_name, s41, ":village"),
		(try_begin),
			(eq, ":safe_village_road_found", 1),
			(str_store_string, s44, "str_s44_s41"),
		(else_try),
			(str_store_string, s44, "str_s41"),
		(try_end),
		(assign, ":safe_village_road_found", 1),
	(try_end),

	(try_begin),
		(eq, ":safe_village_road_found", 1),
		(eq, ":unused_trade_route_found", 1),
		(str_store_string, s47, "str_s47_also_the_roads_to_the_villages_of_s44_and_other_outlying_hamlets_are_considered_safe"),
	(else_try),
		(eq, ":safe_village_road_found", 1),
		(str_store_string, s47, "str_however_the_roads_to_the_villages_of_s44_and_other_outlying_hamlets_are_considered_safe"),
	(try_end),

	(str_store_string, s33, "str_we_have_shortages_of"),
	(assign, ":some_shortages_found", 0),
	(try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
        (party_get_slot, ":price", ":center", ":cur_good_price_slot"),
		(gt, ":price", 1100),

        (str_store_item_name, s34, ":cur_good"),
        (assign, reg1, ":price"),
        (str_store_string, s33, "str_s33_s34_reg1"),

		(assign, ":some_shortages_found", 1),
	(try_end),

	(try_begin),
		(eq, ":some_shortages_found", 0),
		(str_store_string, s32, "str_we_have_adequate_stores_of_all_commodities"),
	(else_try),
		(str_store_string, s32, "str_s33_and_some_other_commodities"),
	(try_end),

	(assign, reg0, ":last_bandit_party_found"),
	(assign, reg1, ":last_bandit_party_origin"),
	(assign, reg2, ":last_bandit_party_destination"),
	(assign, reg3, ":last_bandit_party_hours_ago"),


	]
	)
]
