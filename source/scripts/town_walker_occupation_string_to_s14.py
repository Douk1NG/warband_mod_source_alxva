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

town_walker_occupation_string_to_s14_scripts = [
##diplomacy start+
##WARNING: this will also clobber s0 now
##diplomacy end+
("town_walker_occupation_string_to_s14",
    [
	(store_script_param, ":agent_no", 1),

	#Cairo, approx 1799:
	#adult males = 114,000
	#military, 10,400
	#civil, including religious 5,000
	#commerce 3,500
	#merchants 4,500
	#coffee shops, 1,500 (maybe broaden to inns and taverns)
	#artisans 21,800
	#workmen 4,300
	#itinerants 8,600
	#servants (inc water carriers) 26,400
	(assign, ":check_for_good_price", 0),
    ##diplomacy start+ escalate "sir/madame" to "my lord/lady" or "your highness" if appropriate
    (call_script, "script_dplmc_print_subordinate_says_sir_madame_to_s0"),
    ##diplomacy end+
	(str_store_string, s14, "str_i_take_what_work_i_can_sirmadame_i_carry_water_or_help_the_merchants_with_their_loads_or_help_build_things_if_theres_things_to_be_built"),

	(call_script, "script_agent_get_town_walker_details", ":agent_no"),
	(assign, ":type", reg0),
	(assign, ":walker_dna", reg1),

	(assign, ":item", -1),
	(assign, ":total_item_production", 0),
	(try_for_range, ":trade_good", trade_goods_begin, trade_goods_end),
		(call_script, "script_center_get_production", "$g_encountered_party", ":trade_good"),
		(val_add, ":total_item_production", reg0),
	(try_end),

	(val_max, ":total_item_production", 1),

	(store_mod, ":semi_random_number", ":walker_dna", ":total_item_production"),


	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":walker_dna"),
		(assign, reg5, ":total_item_production"),
		(assign, reg7, ":semi_random_number"),
		(display_message, "str_dna_reg4_total_production_reg5_modula_reg7"),
	(try_end),

    (try_for_range, ":trade_good", trade_goods_begin, trade_goods_end),
        (gt, ":semi_random_number", -1),
        (call_script, "script_center_get_production", "$g_encountered_party", ":trade_good"),
        (val_sub, ":semi_random_number", reg0),
        (lt, ":semi_random_number", 0),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_item_name, s9, ":trade_good"),
          (display_message, "str_agent_produces_s9"),
        (try_end),
        (assign, ":item", ":trade_good"),
    (try_end),


	(try_begin),
		(eq, ":type", walkert_needs_money),
		(is_between, "$g_encountered_party", towns_begin, towns_end),
		(str_store_string, s14, "str_im_not_doing_anything_sirmadame_theres_no_work_to_be_had_around_here_these_days"),
	(else_try),
		(eq, ":type", walkert_needs_money),
		(str_store_string, s14, "str_im_not_doing_anything_sirmadame_i_have_no_land_of_my_own_and_theres_no_work_to_be_had_around_here_these_days"),
	(else_try),
		(eq, ":type", walkert_needs_money_helped),
		(str_store_string, s14, "str_why_im_still_living_off_of_your_kindness_and_goodness_sirmadame_hopefully_there_will_be_work_shortly"),
	(else_try),
		(eq, ":item", "itm_grain"),
        #SB : refactor
        (try_begin),
		  (is_between, "$g_encountered_party", towns_begin, towns_end),
		  (str_store_string, s14, "str_i_work_in_the_fields_just_outside_the_walls_where_they_grow_grain_we_dont_quite_grow_enough_to_meet_our_needs_though_and_have_to_import_grain_from_the_surrounding_countryside"),
		(else_try),
		  (str_store_string, s14, "str_i_work_mostly_in_the_fields_growing_grain_in_the_town_they_grind_it_to_make_bread_or_ale_and_we_can_also_boil_it_as_a_porridge"),
        (try_end),
		(assign, ":check_for_good_price", 1),
	(else_try),
		(eq, ":item", "itm_ale"),
		(str_store_string, s14, "str_i_work_in_the_breweries_making_ale_the_poor_folk_drink_a_lot_of_it_as_its_cheaper_than_wine_we_make_it_with_grain_brought_in_from_the_countryside"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_bread"),
		(str_store_string, s14, "str_i_work_in_a_mill_grinding_flour_to_make_bread_bread_is_cheap_keeps_well_and_fills_the_stomach"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_dried_meat"),
		(str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk"),
		(assign, ":check_for_good_price", 1),

	(else_try),  #SB : combine two strings
		(this_or_next|eq, ":item", "itm_cheese"),
		(eq, ":item", "itm_butter"),
		# (str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk_so_it_doesnt_spoil"),
		# (assign, ":check_for_good_price", 1),

	# (else_try),
		(str_store_string, s14, "str_i_tend_cattle_we_dry_and_salt_meat_to_preserve_it_and_make_cheese_from_the_milk_so_it_doesnt_spoil"),
		(assign, ":check_for_good_price", 1),

	(else_try), #SB : combine two strings
		(this_or_next|eq, ":item", "itm_wool"),
		(eq, ":item", "itm_sausages"),
		# (str_store_string, s14, "str_i_tend_sheep_we_send_the_wool_to_the_cities_to_be_woven_into_cloth_and_make_mutton_sausage_when_we_cull_the_herds"),
		# (assign, ":check_for_good_price", 1),

	# (else_try),
		# (eq, ":item", "itm_sausages"),
		(str_store_string, s14, "str_i_tend_sheep_we_send_the_wool_to_the_cities_to_be_woven_into_cloth_and_make_mutton_sausage_when_we_cull_the_herds"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_wool_cloth"),
		(str_store_string, s14, "str_i_work_at_a_loom_spinning_cloth_from_wool_wool_is_some_of_the_cheapest_cloth_you_can_buy_but_it_will_still_keep_you_warm"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_smoked_fish"),
		(str_store_string, s14, "str_i_crew_a_fishing_boat_we_salt_and_smoke_the_flesh_to_sell_it_far_inland"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_salt"),
		(str_store_string, s14, "str_i_sift_salt_from_a_nearby_flat_they_need_salt_everywhere_to_preserve_meat_and_fish"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_iron"),
		(str_store_string, s14, "str_i_mine_iron_from_a_vein_in_a_nearby_cliffside_they_use_it_to_make_tools_arms_and_other_goods"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_pottery"),
		(str_store_string, s14, "str_i_make_pottery_which_people_use_to_store_grain_and_carry_water"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_tools"),
		(str_store_string, s14, "str_trade_explanation_tools"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_oil"),
		(str_store_string, s14, "str_trade_explanation_oil"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_linen"),
		(str_store_string, s14, "str_trade_explanation_linen"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_velvet"),
		(str_store_string, s14, "str_trade_explanation_velvet"),
		(assign, ":check_for_good_price", 1),

	(else_try),
		(eq, ":item", "itm_spice"),
		(str_store_string, s14, "str_trade_explanation_spice"),
		(assign, ":check_for_good_price", 1),
    #SB : add missing explanation strings
	(else_try),
		(eq, ":item", "itm_apples"),
		(str_store_string, s14, "str_trade_explanation_apples"),
		(assign, ":check_for_good_price", 1),
    (else_try),
        (eq, ":item", "itm_raw_grapes"),
        (str_store_string, s14, "str_trade_explanation_grapes"),
        (assign, ":check_for_good_price", 1),
	(else_try),
		(eq, ":item", "itm_raw_dyes"),
		(str_store_string, s14, "str_trade_explanation_dyes"),
		(assign, ":check_for_good_price", 1),
    (else_try),
        (this_or_next|eq, ":item", "itm_raw_leather"),
        (eq, ":item", "itm_leatherwork"),
        (str_store_string, s14, "str_trade_explanation_leatherwork"),
        (assign, ":check_for_good_price", 1),
    (else_try),
        (eq, ":item", "itm_raw_flax"),
        (str_store_string, s14, "str_trade_explanation_flax"),
        (assign, ":check_for_good_price", 1),
    (else_try),
        (eq, ":item", "itm_raw_date_fruit"),
        (try_begin),
          (is_between, "$g_encountered_party", towns_begin, towns_end),
          (str_store_string, s14, "str_trade_explanation_dates_town"),
        (else_try),
          (str_store_string, s14, "str_trade_explanation_dates_village"),
        (try_end),
        (assign, ":check_for_good_price", 1),
    (else_try),
        (eq, ":item", "itm_raw_olives"),
        (str_store_string, s14, "str_trade_explanation_olives"),
        (assign, ":check_for_good_price", 1),
	(try_end),


	(try_begin),
		(eq, ":check_for_good_price", 1),

		(assign, ":trade_destination", -1),
		(store_skill_level, ":trade_skill", "skl_trade", "trp_player"),

		(try_begin),
			(is_between, "$g_encountered_party", villages_begin, villages_end),
			(party_get_slot, ":trade_town", "$g_encountered_party", slot_village_market_town),
		(else_try),
			(assign, ":trade_town", "$g_encountered_party"),
		(try_end),

		(store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
		(store_add, ":cur_good_price_slot", ":item", ":item_to_price_slot"),
		(party_get_slot, ":score_to_beat", ":trade_town", ":cur_good_price_slot"),
		(val_add, ":score_to_beat", 400),
		(store_mul, ":deduction_for_trade_skill", ":trade_skill", 35),
		(try_begin),
			(is_between, "$g_encountered_party", villages_begin, villages_end),
			(val_add, ":score_to_beat", 200),
		(try_end),
		(val_sub, ":score_to_beat", ":deduction_for_trade_skill"),

		(try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
			(party_get_slot, ":other_town", ":trade_town", ":trade_route_slot"),
			(is_between, ":other_town", towns_begin, towns_end), #SB: add condition for valid town
			(party_get_slot, ":price_in_other_town", ":other_town", ":cur_good_price_slot"),


			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg4, ":price_in_other_town"),
				(assign, reg5, ":score_to_beat"),
				(str_store_party_name, s10, ":other_town"),
				(display_message, "str_s10_has_reg4_needs_reg5"),
			(try_end),

			(gt, ":price_in_other_town", ":score_to_beat"),

			(assign, ":trade_destination", ":other_town"),
			(assign, ":score_to_beat", ":price_in_other_town"),
		(try_end),

		(is_between, ":trade_destination", centers_begin, centers_end),

		(str_store_party_name, s15, ":trade_destination"),
		(str_store_string, s14, "str_s14_i_hear_that_you_can_find_a_good_price_for_it_in_s15"),

		#Reasons -- raw material
		#Reason -- road cut
		#Reason -- villages looted

	(try_end),


	])
]
