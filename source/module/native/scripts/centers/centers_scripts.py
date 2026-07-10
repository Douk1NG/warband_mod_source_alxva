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

####################################################################################################################
# CENTER MANAGEMENT SCRIPTS
# 
# This file handles the economic and physical state of towns, castles, and villages.
# It manages prosperity, garrisons, town walkers (NPCs wandering streets), and center notes.
####################################################################################################################

centers_scripts = [
  # INPUT:
  # param1: defeated_center, param2: winner_faction
  # OUTPUT:
  # none
  ("order_best_besieger_party_to_guard_center",
    [
      (store_script_param, ":defeated_center", 1),
      (store_script_param, ":winner_faction", 2),
      (assign, ":best_party", -1),
      (assign, ":best_party_strength", 0),
      ##diplomacy start+ support for promoted kingdom ladies
      (try_for_range, ":kingdom_hero", heroes_begin, heroes_end),#<- changed to heroes
        (this_or_next|troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
           (is_between, ":kingdom_hero", active_npcs_begin, active_npcs_end),
      ##diplomacy end+
        (troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
        (gt, ":kingdom_hero_party", 0),
        (party_is_active, ":kingdom_hero_party"),
        (store_faction_of_party, ":kingdom_hero_party_faction", ":kingdom_hero_party"),
        (eq, ":winner_faction", ":kingdom_hero_party_faction"),
        (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":defeated_center"),
        (lt, ":dist", 5),
        #If marshall has captured the castle, then do not leave him behind.
        (neg|faction_slot_eq, ":winner_faction", slot_faction_marshall, ":kingdom_hero"),
        (assign, ":has_besiege_ai", 0),
        (try_begin),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (else_try),
          (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":kingdom_hero_party_commander_party", ":kingdom_hero_party", slot_party_ai_object),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_state, spai_besieging_center),
          (party_slot_eq, ":kingdom_hero_party_commander_party", slot_party_ai_object, ":defeated_center"),
          (assign, ":has_besiege_ai", 1),
        (try_end),
        (eq, ":has_besiege_ai", 1),
        (party_get_slot, ":kingdom_hero_party_strength", ":kingdom_hero_party", slot_party_cached_strength),#recently calculated
        (gt, ":kingdom_hero_party_strength", ":best_party_strength"),
        (assign, ":best_party_strength", ":kingdom_hero_party_strength"),
        (assign, ":best_party", ":kingdom_hero_party"),
      (try_end),
      (try_begin),
        (gt, ":best_party", 0),
        (call_script, "script_party_set_ai_state", ":best_party", spai_holding_center, ":defeated_center"),
        #(party_set_slot, ":best_party", slot_party_commander_party, -1),
        (party_set_flags, ":best_party", pf_default_behavior, 1),
      (try_end),
      ]),

  #script_game_get_item_buy_price_factor:
  # This script is called from the game engine when the notes of a center is needed.
  # INPUT: arg1 = center_no, arg2 = note_index
  # OUTPUT: s0 = note
  ("game_get_center_note",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":note_index"),

      (set_trigger_result, 0),
      (try_begin),
        (eq, ":note_index", 0),
        (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
        (try_begin),
          (ge, ":lord_troop", 0),
          (store_troop_faction, ":lord_faction", ":lord_troop"),
          (str_store_troop_name_link, s1, ":lord_troop"),
          (try_begin),
            (eq, ":lord_troop", "trp_player"),
            (gt, "$players_kingdom", 0),
            (str_store_faction_name_link, s2, "$players_kingdom"),
          (else_try),
            (str_store_faction_name_link, s2, ":lord_faction"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          ##diplomacy start+ Show when the city is the home of a lord or is a court
          (assign, ":bound_center", reg0),#Save reg0 to avoid having it randomly change
          (try_begin),
             (eq, "$g_player_court", ":center_no"),

             (store_and, reg1, "$players_kingdom_name_set", rename_center), #SB : specify capitals
             (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is {reg1?your capital:where you make your court}.^"),
          (else_try),
             (neq, ":lord_troop", "trp_player"),
             (neg|is_between, ":center_no", villages_begin, villages_end),
             (call_script, "script_lord_get_home_center", ":lord_troop"),
             (eq, reg0, ":center_no"),
             (call_script, "script_dplmc_get_troop_standing_in_faction", ":lord_troop", ":lord_faction"),
             (try_begin),
                (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} court.^"),
             (else_try),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} home.^"),
             (try_end),
          (else_try),#Fall through to normal behavior
          ##diplomacy end+
          (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
          ##diplomacy start+
          (try_end),
          (assign, reg0, ":bound_center"),#Revert reg0 to avoid having it randomly change
          ##diplomacy end+
        (else_try),
          (str_clear, s2),
          ##diplomacy start+ Don't hide notes for centers with no lords.
          (store_faction_of_party, ":lord_faction", ":center_no"),
          (str_store_string, s1, "str_noone"),
          (try_begin),
             (ge, ":lord_faction", 1),
             (str_store_faction_name_link, s2, ":lord_faction"),
          (else_try),
             (str_store_string, s2, "str_noone"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          (try_begin),
             (is_between, ":lord_faction", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":lord_faction", slot_faction_state, sfs_active),
             (str_store_string, s2, "@{s51} belongs to {s2} but has not yet been granted to a lord.^"),
          (else_try),
             (str_store_string, s2, "@{s51} belongs to {s2}.^"),
          (try_end),
          ##diplomacy end+
        (try_end),
        (try_begin),
          (is_between, ":center_no", villages_begin, villages_end),
          ##diplomacy start+ Show market town if it differs from the bound center
          (party_get_slot, ":market_center", ":center_no", slot_village_market_town),
          (try_begin),
             (is_between, ":market_center", centers_begin, centers_end),
             (neq, ":market_center", ":center_no"),
             (neg|party_slot_eq, ":center_no", slot_village_bound_center, ":market_center"),
             (str_store_party_name_link, s8, ":market_center"),
             (str_store_string, s2, "@{s2}Its market town is {s8}.^"),
          (try_end),
          ##diplomacy end+
        (else_try),
          (assign, ":num_villages", 0),
          (try_for_range_backwards, ":village_no", villages_begin, villages_end),
            (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
            (try_begin),
              (eq, ":num_villages", 0),
              (str_store_party_name_link, s8, ":village_no"),
            (else_try),
              (eq, ":num_villages", 1),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{s7} and {s8}"),
            (else_try),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{!}{s7}, {s8}"),
            (try_end),
            (val_add, ":num_villages", 1),
          (try_end),
          (try_begin),
            (eq, ":num_villages", 0),
            (str_store_string, s2, "@{s2}It has no villages.^"),
          (else_try),
            (store_sub, reg0, ":num_villages", 1),
            (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
          (try_end),
        (try_end),
        (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
        #(party_get_slot, reg7, ":center_no", slot_town_prosperity),
        (str_store_string, s0, "@{s2}Its prosperity is: {s50}", 0),

        (set_trigger_result, 1),
      (try_end),
     ]),

  #script_game_get_faction_note
  # INPUT:
  # param1: center_no_1
  # param1: center_no_2
  ("set_trade_route_between_centers",
    [(store_script_param, ":center_no_1", 1),
     (store_script_param, ":center_no_2", 2),
     (assign, ":center_1_added", 0),
     (assign, ":center_2_added", 0),
     (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
       (try_begin),
         (eq, ":center_1_added", 0),
         (party_slot_eq, ":center_no_1", ":cur_slot", 0),
         (party_set_slot, ":center_no_1", ":cur_slot", ":center_no_2"),
         (assign, ":center_1_added", 1),
       (try_end),
       (try_begin),
         (eq, ":center_2_added", 0),
         (party_slot_eq, ":center_no_2", ":cur_slot", 0),
         (party_set_slot, ":center_no_2", ":cur_slot", ":center_no_1"),
         (assign, ":center_2_added", 1),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":center_1_added", 0),
       (str_store_party_name, s1, ":center_no_1"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     (try_begin),
       (eq, ":center_2_added", 0),
       (str_store_party_name, s1, ":center_no_2"),
       (display_message, "@{!}DEBUG -- ERROR: More than 15 trade routes are given for {s1}."),
     (try_end),
     ]),

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

	]),

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
	]),

  #script_get_enterprise_name
  # INPUT: arg1 = party_no (of the merchant), arg2 = center_no
  ##diplomacy start+
  # If optional economic changes are enabled, the benefits are applied to both
  # the town of origin and the destination, instead of just the latter.
  ##diplomacy end+
  ("do_merchant_town_trade",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":center_no"),

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),

	  (try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_party_name, s4, ":center_no"),
		(str_store_party_name, s5, ":origin"),
		(display_message, "@{!}DEBUG -- Caravan trades in {s4}, originally from {s5}"),
	  (try_end),

	  (call_script, "script_add_log_entry", logent_party_traded, ":party_no", ":origin", ":center_no", -1),

      (call_script, "script_do_party_center_trade", ":party_no", ":center_no", 4), #it was first 10 then increased 20 then increased 30, now I decrease it to back 6. Because otherwise prices do not differiate much. Trade become useless in game.

      (assign, ":total_change", reg0),
      #Adding the earnings to the wealth (maximum changed price is the earning)
      (val_div, ":total_change", 2),
      (str_store_party_name, s1, ":party_no"),
      (str_store_party_name, s2, ":center_no"),
      (assign, reg1, ":total_change"),

      #Adding tariffs to the town
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),

	  (assign, ":tariffs_generated", ":total_change"),
      (val_mul, ":tariffs_generated", ":prosperity"),
	  ##diplomacy start+
	  #Move the next two lines further down to reduce rounding error
	  #(val_div, ":tariffs_generated", 100),
	  #(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages

	  #Re-wrote the "diplomacy" section here for greater clarity.
	  (assign, ":percent", 100),
      (try_begin), # trade agreement
        (store_faction_of_party, ":party_faction", ":party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),

        (store_add, ":truce_slot", ":party_faction", slot_faction_truce_days_with_factions_begin),
        (val_sub, ":truce_slot", kingdoms_begin),
  	    (faction_get_slot, ":truce_days", ":center_faction", ":truce_slot"),
  	    ##nested diplomacy start+ replace "20" with a named constant
  	    #(gt, ":truce_days", 20),
  	    (gt, ":truce_days", dplmc_treaty_trade_days_expire),
  	    ##nested diplomacy end+
  	    (val_add, ":percent", 30),
      (try_end),

	  #If economic changes are enabled, divide the tariffs between the source and destination.
	  (assign, ":origin_tariffs_generated", 0),#we will need this variable later, if it is set
	  (try_begin),
	    #Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		#give half the tariffs to the origin
		(ge, ":tariffs_generated", 0),
		(party_get_slot, ":origin_accumulated_tariffs", ":origin", slot_center_accumulated_tariffs),
		(store_div, ":origin_tariffs_generated", ":tariffs_generated", 2),
		(val_sub, ":tariffs_generated", ":origin_tariffs_generated"),
		#apply plutocracy/aristocracy modifier, and any modifier from a trade treaty
		(store_faction_of_party, ":origin_faction", ":center_no"),
		(faction_get_slot, ":aristocracy", ":origin_faction", dplmc_slot_faction_aristocracy),
		(val_mul, ":aristocracy", -5),
		(store_add, ":origin_percent", ":percent", ":aristocracy"),
		(val_mul, ":origin_tariffs_generated", ":origin_percent"),
		(val_add, ":origin_tariffs_generated", 50),#for rounding
		(val_div, ":origin_tariffs_generated", 100),
		#apply the delayed division from before (leaving the steps separated for clarity)
		(val_add, ":origin_tariffs_generated", 50),
		(val_div, ":origin_tariffs_generated", 100),#adjust for having been multiplied by prosperity
		(val_add, ":tariffs_generated", 5),
		(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
		#now we have the final value of origin_tariffs_generated
		(val_add, ":origin_accumulated_tariffs", ":origin_tariffs_generated"),
		(party_set_slot, ":origin", slot_center_accumulated_tariffs, ":origin_accumulated_tariffs"),
		#print economic debug message if enabled
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":origin_tariffs_generated"),
		(str_store_party_name, s4, ":origin"),
		(assign, reg5, ":origin_accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),

	  #For this town: apply the faction plutocracy/aristocracy modifier
      (faction_get_slot, ":aristocracy", ":center_faction", dplmc_slot_faction_aristocracy),
      (val_mul, ":aristocracy", -5),
      (val_add, ":percent", ":aristocracy"),
      (val_mul, ":tariffs_generated", ":percent"),
   	  (val_add, ":tariffs_generated", 50),
      (val_div, ":tariffs_generated", 100),
	  #apply the delayed division from before (leaving the steps separated for clarity)
   	  (val_add, ":tariffs_generated", 50),
 	  (val_div, ":tariffs_generated", 100),#adjust for having been multiplied by prosperity
	  (val_add, ":tariffs_generated", 5),
	  (val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
	  ##diplomacy end+
	  (val_add, ":accumulated_tariffs", ":tariffs_generated"),

	  (try_begin),
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":tariffs_generated"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg5, ":accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),

      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
      ##diplomacy start+
	  #If economic changes are enabled, 50% chance that the origin rather than
	  #the destination will receive the chance for prosperity increase.
	  (assign, ":benefit_center", ":center_no"),
	  (try_begin),
		#Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		(ge, ":tariffs_generated", 0),
		#50% chance
		(store_random_in_range, ":rand", 0, 64),
		(lt, ":rand", 32),
		(assign, ":benefit_center", ":origin"),
	  (try_end),
	  ##diplomacy end+
      #Adding 1 to center prosperity with 18% for each caravan in that center
      (try_begin),
        (store_random_in_range, ":rand", 0, 80),
		##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_center_get_goods_availability", ":benefit_center"),
		##diplomacy end+
		(assign, ":hardship_index", reg0),
		(gt, ":rand", ":hardship_index"),
      (try_begin),
        (store_random_in_range, ":rand", 0, 100),
        (gt, ":rand", 82),
		##diplomacy start+ in next line, changed center_no to benefit_center
		(call_script, "script_change_center_prosperity", ":benefit_center", 1),
		##diplomacy end+
		(val_add, "$newglob_total_prosperity_from_caravan_trade", 1),
      (try_end),
     (try_end),
  ]),

  #script_party_calculate_regular_strength:
##  # INPUT:
##  # param1: stack_index
##
##  #OUTPUT:
##  # string register 0.
##  ("cf_print_troop_name_with_stack_index_to_s0",
##   [
##     (store_script_param_1, ":stack_index"),
##     (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
##     (lt, ":stack_index", ":num_stacks"),
##     (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_index"),
##     (str_store_troop_name, s0, ":stack_troop"),
##    ]),

  #script_print_troop_owned_centers_in_numbers_to_s0
  # INPUT:
  # param1: troop_no
  #OUTPUT:
  # string register 0.
  ("print_troop_owned_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (str_store_string, s0, "@nothing"),
     (assign, ":owned_towns", 0),
     (assign, ":owned_castles", 0),
     (assign, ":owned_villages", 0),
     (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
       (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":owned_towns", 1),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":owned_castles", 1),
       (else_try),
         (val_add, ":owned_villages", 1),
       (try_end),
     (try_end),
     (assign, ":num_types", 0),
     (try_begin),
       (gt, ":owned_villages", 0),
       (assign, reg0, ":owned_villages"),
       (store_sub, reg1, reg0, 1),
       (str_store_string, s0, "@{reg0} village{reg1?s:}"),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_castles", 0),
       (assign, reg0, ":owned_castles"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} castle{reg1?s:}"),
       (else_try),
         (str_store_string, s0, "@{reg0} castle{reg1?s:} and {s0}"),
       (try_end),
       (val_add, ":num_types", 1),
     (try_end),
     (try_begin),
       (gt, ":owned_towns", 0),
       (assign, reg0, ":owned_towns"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} town{reg1?s:}"),
       (else_try),
         (eq, ":num_types", 1),
         (str_store_string, s0, "@{reg0} town{reg1?s:} and {s0}"),
       (else_try),
         (str_store_string, s0, "@{reg0} town{reg1?s:}, {s0}"),
       (try_end),
     (try_end),
     (store_add, reg0, ":owned_villages", ":owned_castles"),
     (val_add, reg0, ":owned_towns"),
     ]),

  #script_get_random_melee_training_weapon
  # Input: arg1 = party_no, arg2 = range (in kms)
  # Output: reg0 = center_no
  ("cf_get_random_enemy_center_within_range",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":range", 2),

      (assign, ":num_centers", 0),
      (store_faction_of_party, ":faction_no", ":party_no"),
      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_add, ":num_centers", 1),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":end_cond", centers_end),
      (try_for_range, ":cur_center", centers_begin, ":end_cond"),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
        (lt, ":cur_relation", 0),
        (store_distance_to_party_from_party, ":dist", ":party_no", ":cur_center"),
        (le, ":dist", ":range"),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
        (assign, ":end_cond", 0),#break
      (try_end),
      (assign, reg0, ":result"),
  ]),

  # script_cf_faction_get_random_enemy_faction
##  # Input: arg1 = troop_no
##  # Output: reg0 = enemy_troop_no (Can fail)
##  ("cf_troop_get_random_enemy_troop_as_a_town_lord",
##    [
##      (store_script_param_1, ":troop_no"),
##
##      (assign, ":result", -1),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##      (try_end),
##      (store_random_in_range,":random_enemy",0,":count_enemies"),
##      (assign, ":count_enemies", 0),
##      (try_for_range, ":cur_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
##        (eq, ":result", -1),
##        (troop_get_slot, ":cur_enemy", ":troop_no", ":cur_slot"),
##        (gt, ":cur_enemy", 0),
##        (troop_slot_eq, ":cur_enemy", slot_troop_occupation, slto_kingdom_hero),
##        (call_script, "script_get_number_of_hero_centers", ":cur_enemy"),
##        (gt, reg0, 0),
##        (val_add, ":count_enemies", 1),
##        (gt, ":count_enemies", ":random_enemy"),
##        (assign, ":result", ":cur_enemy"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),


  ##  # script_cf_get_random_enemy_with_valid_slot
  ##  # Input: arg1 = faction_no, arg2 = slot_no
  ##  # Output: reg0 = faction_no (Can fail)
  ##  ("cf_get_random_enemy_with_valid_slot",
  ##    [
  ##      (store_script_param_1, ":faction_no"),
  ##      (store_script_param_2, ":slot_no"),
  ##
  ##      (assign, ":result", -1),
  ##      (assign, ":count_factions", 0),
  ##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
  ##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
  ##        (le, ":cur_relation", -10),
  ##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
  ##        (gt, ":cur_value", 0),#Checking validity
  ##        (val_add, ":count_factions", 1),
  ##      (try_end),
  ##      (store_random_in_range,":random_faction",0,":count_factions"),
  ##      (assign, ":count_factions", 0),
  ##      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
  ##        (eq, ":result", -1),
  ##        (store_relation, ":cur_relation", ":faction_no", ":cur_faction"),
  ##        (le, ":cur_relation", -10),
  ##        (faction_get_slot, ":cur_value", ":cur_faction", ":slot_no"),
  ##        (gt, ":cur_value", 0),#Checking validity
  ##        (val_add, ":count_factions", 1),
  ##        (gt, ":count_factions", ":random_faction"),
  ##        (assign, ":result", ":cur_faction"),
  ##      (try_end),
  ##
  ##      (neq, ":result", -1),
  ##      (assign, reg0, ":result"),
  ##  ]),


##  # script_cf_get_random_kingdom_hero
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no (Can fail)
##  ("cf_get_random_kingdom_hero",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##      (try_end),
##      (store_random_in_range, ":random_hero", 0, ":count_heroes"),
##      (assign, ":result", -1),
##      (assign, ":count_heroes", 0),
##      (try_for_range, ":center_no", centers_begin, centers_end),
##        (eq, ":result", -1),
##        (store_faction_of_party, ":cur_faction", ":center_no"),
##        (eq, ":cur_faction", ":faction_no"),
##        (party_get_slot, ":cur_lord", ":center_no", slot_town_lord),
##        (is_between, ":cur_lord", heroes_begin, heroes_end),
##        (val_add, ":count_heroes", 1),
##        (lt, ":random_hero", ":count_heroes"),
##        (assign, ":result", ":cur_lord"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),


# script_cf_get_random_kingdom_hero_as_lover - removed



##  # script_cf_get_random_siege_location_with_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":center_no"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),

##  # script_cf_get_random_siege_location_with_attacker_faction
##  # Input: arg1 = faction_no
##  # Output: reg0 = center_no, Can Fail!
##  ("cf_get_random_siege_location_with_attacker_faction",
##    [
##      (store_script_param_1, ":faction_no"),
##      (assign, ":result", -1),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##      (try_end),
##      (store_random_in_range,":random_center",0,":count_sieges"),
##      (assign, ":count_sieges", 0),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (eq, ":result", -1),
##        (party_get_battle_opponent, ":besieger_party", ":center_no"),
##        (gt, ":besieger_party", 0),
##        (store_faction_of_party, ":cur_faction_no", ":besieger_party"),
##        (eq, ":cur_faction_no", ":faction_no"),
##        (val_add, ":count_sieges", 1),
##        (gt, ":count_sieges", ":random_center"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),



##  # script_cf_get_number_of_random_troops_from_party
##  # Input: arg1 = party_no, arg2 = number of troops to remove
##  # Output: reg0 = troop_no, Can fail if there are no slots having the required number of units!
##  ("cf_get_number_of_random_troops_from_party",
##    [
##      (store_script_param_1, ":party_no"),
##      (store_script_param_2, ":no_to_remove"),
##
##      (assign, ":result", -1),
##      (assign, ":count_stacks", 0),
##
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##      (try_end),
##      (store_random_in_range,":random_stack",0,":count_stacks"),
##      (assign, ":count_stacks", 0),
##      (try_for_range, ":i_stack", 0, ":num_stacks"),
##        (eq, ":result", -1),
##        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
##        (party_stack_get_num_wounded, ":num_wounded",":party_no",":i_stack"),
##        (val_sub, ":stack_size", ":num_wounded"),
##        (ge, ":stack_size", ":no_to_remove"),
##        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
##        (neg|troop_is_hero, ":stack_troop"),
##        (val_add, ":count_stacks", 1),
##        (gt, ":count_stacks", ":random_stack"),
##        (assign, ":result", ":stack_troop"),
##      (try_end),
##
##      (neq, ":result", -1),
##      (assign, reg0, ":result"),
##  ]),




  # script_cf_get_random_lord_in_a_center_with_faction
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_in_a_center_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (eq, ":faction_no", ":lord_faction_no"),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_cf_get_random_lord_except_king_with_faction
  # Input: arg1 = faction_no
  # Output: reg0 = troop_no, Can Fail!
  ("cf_get_random_lord_from_another_faction_in_a_center",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
      (try_end),
      (store_random_in_range, ":random_lord", 0, ":count_lords"),
      (assign, ":count_lords", 0),
      (try_for_range, ":lord_no", heroes_begin, heroes_end),
        (eq, ":result", -1),
        (store_troop_faction, ":lord_faction_no", ":lord_no"),
        (neq, ":lord_faction_no", ":faction_no"),
        (store_relation, ":our_relation", ":lord_faction_no", "fac_player_supporters_faction"),
        (store_relation, ":lord_relation", ":lord_faction_no", ":faction_no"),
        (lt, ":lord_relation", 0),
        (ge, ":our_relation", 0),
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        #(troop_slot_eq, ":lord_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":lord_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":lord_party", ":lord_no", slot_troop_leaded_party),
        (ge, ":lord_party", 0),
        (party_get_attached_to, ":lord_attachment", ":lord_party"),
        (is_between, ":lord_attachment", centers_begin, centers_end), #is troop in a center?
        (val_add, ":count_lords", 1),
        (lt, ":random_lord", ":count_lords"),
        (assign, ":result", ":lord_no"),
      (try_end),
      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

  # script_get_closest_walled_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),

  # script_get_closest_center
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_walled_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


##  # script_get_closest_town_of_faction
  # For internal use only
  ("get_heroes_attached_to_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),

  # script_get_heroes_attached_to_center
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_aux", ":center_no", ":party_no_to_collect_heroes"),

#rebellion changes begin -Arma
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

#     (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
#        (faction_slot_eq, ":rebel_faction", slot_faction_state, sfs_inactive_rebellion),
#        (faction_slot_eq, ":rebel_faction", slot_faction_inactive_leader_location, ":center_no"),
#        (faction_get_slot, ":pretender", ":rebel_faction", slot_faction_leader),
#        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
#     (try_end),
#rebellion changes end


  ]),


  # script_get_heroes_attached_to_center_as_prisoner_aux
  # For internal use only
  ("get_heroes_attached_to_center_as_prisoner_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_get_num_prisoner_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":attached_party", ":party_no_to_collect_heroes"),
      (try_end),
  ]),


  # script_get_heroes_attached_to_center_as_prisoner
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  ("get_heroes_attached_to_center_as_prisoner",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner_aux", ":center_no", ":party_no_to_collect_heroes"),
  ]),

##
##  # script_cf_get_party_leader
##  # Input: arg1 = party_no
##  # Output: reg0 = troop_no of the leader (Can fail)
##  ("cf_get_party_leader",
##    [
##      (store_script_param_1, ":party_no"),
##
##      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
##      (gt, ":num_stacks", 0),
##      (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
##      (troop_is_hero, ":stack_troop"),
##      (assign, reg0, ":stack_troop"),
##  ]),

  # script_give_center_to_faction
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      (try_begin),
        (eq, "$g_constable_training_center", ":center_no"),
        (assign, "$g_constable_training_center", -1),
      (try_end),
      ##diplomacy end
      (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (faction_get_slot, ":player_faction_king", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":player_faction_king", "trp_player"),

        (try_begin),
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (assign, ":number_of_walled_centers_players_kingdom_has", 1),
        (else_try),
          (assign, ":number_of_walled_centers_players_kingdom_has", 0),
        (try_end),

        (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":owner_faction_no", ":walled_center"),
          (eq, ":owner_faction_no", "fac_player_supporters_faction"),
          (val_add, ":number_of_walled_centers_players_kingdom_has", 1),
        (try_end),

        (ge, ":number_of_walled_centers_players_kingdom_has", 10),
        (unlock_achievement, ACHIEVEMENT_VICTUM_SEQUENS),
      (try_end),

      (try_begin),
        (check_quest_active, "qst_join_siege_with_army"),
        (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, ":center_no"),
        (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
        #Reactivating follow army quest
        (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
        (str_store_troop_name_link, s9, ":faction_marshall"),
        (setup_quest_text, "qst_follow_army"),
        (str_store_string, s2, "@{s9} wants you to resume following his army until further notice."),
        (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
        (assign, "$g_player_follow_army_warnings", 0),
      (try_end),

      #(store_faction_of_party, ":old_faction", ":center_no"),
      (call_script, "script_give_center_to_faction_aux", ":center_no", ":faction_no"),
      (call_script, "script_update_village_market_towns"),

      (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        (call_script, "script_faction_recalculate_strength", ":cur_faction"),
      (try_end),
      (assign, "$g_recalculate_ais", 1),

	  (try_begin),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(call_script, "script_activate_player_faction", "trp_player"),
	  (try_end),

      #(call_script, "script_activate_deactivate_player_faction", ":old_faction"),
      #(try_begin),
      #(eq, ":faction_no", "fac_player_supporters_faction"),
      #(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":center_no", "trp_player", 0),

      #check with Armagan -- what is this here for?
      #(try_for_range, ":cur_village", villages_begin, villages_end),
      #(store_faction_of_party, ":cur_village_faction", ":cur_village"),
      #(eq, ":cur_village_faction", "fac_player_supporters_faction"),
      #(neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      #(call_script, "script_give_center_to_lord", ":cur_village", "trp_player", 0),
      #(try_end),
      #(try_end),
    ]),

  # script_give_center_to_faction_aux
  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (try_begin),
          (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
          (gt, ":farmer_party", 0),
          (party_is_active, ":farmer_party"),
          (party_set_faction, ":farmer_party", ":faction_no"),
        (try_end),
        #SB : reinforcements becomes deserters
        (try_begin),
          (party_get_slot, ":reinf_party", ":center_no", slot_village_reinforcement_party),
          (gt, ":reinf_party", 0),
          (party_is_active, ":reinf_party"),
          (set_spawn_radius, 0),
          (spawn_around_party, ":reinf_party", "pt_deserters"),
          (assign, ":new_party", reg0),
          #apply move_members_with_ratio, party_inflict_attrition, party_inflict_casualties, etc based on center relations/prosperity
          (call_script, "script_party_add_party", ":new_party", ":reinf_party"),
          (party_set_slot, ":center_no", slot_village_reinforcement_party, -1),
          (party_set_ai_behavior, ":new_party", ai_bhvr_patrol_party),
          (party_set_ai_object, ":new_party", ":center_no"), #or its market town
          (party_set_ai_patrol_radius, ":new_party", 25),
          (remove_party, ":reinf_party"),
        (try_end),
      (try_end),

      (try_begin),
	    #This bit of seemingly redundant code (the neq condition) is designed to prevent a bug that occurs when a player first conquers a center -- apparently this script is called again AFTER it is handed to a lord
		#Without this line, then the player's dialog selection does not have any affect, because town_lord is set again to stl_unassigned after the player makes his or her choice
	    (neq, ":faction_no", ":old_faction"),
		##diplomacy start+
		(party_get_slot, ":old_ex_faction", ":center_no", slot_center_ex_faction),
		##diplomacy end+
        (party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
        (party_get_slot, ":old_town_lord", ":center_no", slot_town_lord),
		##diplomacy start+
		(store_current_hours, ":hours"),
		(party_get_slot, ":old_ex_lord", ":center_no", dplmc_slot_center_ex_lord),
		#(party_get_slot, ":old_last_transfer", ":center_no", dplmc_slot_center_last_transfer_time),
		(try_begin),
			#When a faction regains a lost fief, if the ex-lord is a member of that faction,
			#don't erase that information.
			(this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":faction_no"),#Handle several rapid sequential transfers
				(eq, ":old_ex_faction", ":faction_no"),
			(is_between, ":old_ex_lord", heroes_begin, heroes_end),
			(store_faction_of_troop, ":old_ex_lord_faction", ":old_ex_lord"),
			(eq, ":old_ex_lord_faction", ":faction_no"),
		(else_try),
			#Otherwise, if the center had a lord before this transfer, set the
			#ex-lord to the lord losing this.
			(neq, ":old_town_lord", stl_unassigned),
			(ge, ":old_town_lord", 0),
			(this_or_next|ge, ":old_town_lord", 1),#Don't apply to the player at the start of the game
				(gt, ":hours", 0),

			#Don't apply to fiefs lost by the faction leader, except for his "home",
			#and any fiefs with him marked as the original lord.
			(call_script, "script_dplmc_get_troop_standing_in_faction", ":old_town_lord", ":old_faction"),
			(this_or_next|lt, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(this_or_next|troop_slot_eq, ":old_faction", slot_troop_home, ":center_no"),
				(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":old_town_lord"),

			(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":old_town_lord"),
		(try_end),
        (party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":hours"),
        (party_set_slot, ":center_no", slot_town_lord, stl_unassigned),
        (party_set_banner_icon, ":center_no", 0),#Removing banner
        (call_script, "script_update_faction_notes", ":old_faction"),
        #Invalidate old lord's cached center points
        (gt, ":old_town_lord", -1),
        (troop_set_slot, ":old_town_lord", dplmc_slot_troop_center_points_plus_one, 0),
      (try_end),

      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),

      (try_begin),
        (ge, ":old_town_lord", 0),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_update_troop_notes", ":old_town_lord"),
      (try_end),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        ##diplomacy start+ Avoid infinite recursion even if some foolish modder (such as myself)
        #has set up bizarre cyclic dependencies
        (store_faction_of_party, ":other_center_faction", ":other_center"),
        ##The "this or next" is so that any weird uses of this function
        ##in Native (to change something to its own faction) will be
        ##replicated.  The reason this works is that all villages have
        ##higher ID numbers than castles or towns.
        (this_or_next|gt, ":other_center", ":center_no"),
        (neq, ":other_center_faction", ":old_faction"),
        ##diplomacy end+
        (call_script, "script_give_center_to_faction_aux", ":other_center", ":faction_no"),
      (try_end),
  ]),

  # script_change_troop_faction
  # Input: arg1 = center_no, arg2 = lord_troop, arg3 = add_garrison_to_center
  ("give_center_to_lord",
    [
      (store_script_param, ":center_no", 1),
      (store_script_param, ":lord_troop_id", 2), #-1 only in the case of a player deferring ownership of a center
      (store_script_param, ":add_garrison", 3),
      ##diplomacy begin
      (party_set_slot, ":center_no", dplmc_slot_center_taxation, 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
        (party_set_slot, ":center_no", slot_village_infested_by_bandits, 0),
      (try_end),
      ##diplomacy end

      ##diplomacy start+
      #For relation changes below, store all heroes' center points and closest fiefs.
      (call_script, "script_dplmc_prepare_hero_center_points_ignoring_center", ":center_no"),

      #(assign, ":player_declines_honor", 0),
      #(try_begin),
      #	  (gt, "$g_dont_give_fief_to_player_days", 1),
      #	  (assign, ":player_declines_honor", 1),
      #(try_end),
      ##diplomacy end+

      (try_begin),
      ##diplomacy start+ notable events like this should be logged by default
        (store_current_hours, ":hours"),
        (ge, ":hours", 1),#Don't spam the game log during world setup
        (ge, ":lord_troop_id", 0),
        (str_store_party_name_link, s4, ":center_no"),
        (str_store_troop_name_link, s5, ":lord_troop_id"),
        (store_troop_faction, ":msg_faction_no", ":lord_troop_id"),
        (faction_get_color, ":color", ":msg_faction_no"), #SB : colorize
        (str_store_faction_name_link, s7, ":msg_faction_no"),
        (try_begin),
           (faction_slot_eq, ":msg_faction_no", slot_faction_leader, ":lord_troop_id"),
           (display_log_message, "@{s5} of the {s7} has taken ownership of {s4}.", ":color"),
        (else_try),
           (display_log_message, "@{s4} has been awarded to {s5} of the {s7}.", ":color"),
        (try_end),
      (else_try),
	  ##diplomacy end+
	   (eq, "$cheat_mode", 1),
		(ge, ":lord_troop_id", 0),
		(str_store_party_name, s4, ":center_no"),
		(str_store_troop_name, s5, ":lord_troop_id"),
		(display_message, "@{!}DEBUG -- {s4} awarded to {s5}"),
	  (try_end),

	  (try_begin),
	    (eq, ":lord_troop_id", "trp_player"),
	    (unlock_achievement, ACHIEVEMENT_ROYALITY_PAYMENT),

	    (assign, ":number_of_fiefs_player_have", 1),
	    (try_for_range, ":cur_center", centers_begin, centers_end),
	      (neq, ":cur_center", ":center_no"),
	      (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
	      (val_add, ":number_of_fiefs_player_have", 1),
	    (try_end),

	    (ge, ":number_of_fiefs_player_have", 5),
	    (unlock_achievement, ACHIEVEMENT_MEDIEVAL_EMLAK),
	  (try_end),

      (party_get_slot, ":old_lord_troop_id", ":center_no", slot_town_lord),

	  (try_begin), #This script is ONLY called with lord_troop_id = -1 when it is the player faction
	  ##diplomacy start+
	  #The player can now also be co-ruler of a NPC kingdom.
         (eq, ":lord_troop_id", -1),

		 (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		 (faction_get_slot, ":players_kingdom_liege", "$players_kingdom", slot_faction_leader),
		 (gt, ":players_kingdom_liege", -1),
		 (this_or_next|eq, ":players_kingdom_liege", "trp_player"),
		 (this_or_next|troop_slot_eq, ":players_kingdom_liege", slot_troop_spouse, "trp_player"),
			(troop_slot_eq, "trp_player", slot_troop_spouse, ":players_kingdom_liege"),

		(assign, ":lord_troop_faction", "$players_kingdom"),
		(party_set_banner_icon, ":center_no", 0),#Removing banner
	  (else_try),
	  ##diplomacy end+
	    (eq, ":lord_troop_id", -1),
	    (assign, ":lord_troop_faction", "fac_player_supporters_faction"),
        (party_set_banner_icon, ":center_no", 0),#Removing banner

      (else_try),
	    (eq, ":lord_troop_id", "trp_player"),
	    (assign, ":lord_troop_faction", "$players_kingdom"), #was changed on Apr 27 from fac_plyr_sup_fac

      (else_try),
		(store_troop_faction, ":lord_troop_faction", ":lord_troop_id"),
	  (try_end),
	  (faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),

	  (try_begin),
	    (eq, ":faction_leader", "trp_player"),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_QUEEN),
        (try_end),
	  (try_end),

	  (try_begin),
		(eq, ":faction_leader", ":old_lord_troop_id"),
		(call_script, "script_add_log_entry", logent_liege_grants_fief_to_vassal, ":faction_leader", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
        (troop_set_slot, ":lord_troop_id", slot_troop_promised_fief, 0),
	  (try_end),

      (try_begin),
	    (eq, ":lord_troop_id", -1), #Lord troop ID -1 is only used when a player is deferring assignment of a fief
        (party_set_faction, ":center_no", "$players_kingdom"),
	  (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (gt, "$players_kingdom", 0),
        (party_set_faction, ":center_no", "$players_kingdom"),
      (else_try),
        (eq, ":lord_troop_id", "trp_player"),
        (neg|is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (party_set_faction, ":center_no", "fac_player_supporters_faction"),
      (else_try),
        (party_set_faction, ":center_no", ":lord_troop_faction"),
      (try_end),
      (party_set_slot, ":center_no", slot_town_lord, ":lord_troop_id"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (party_get_slot, ":farmer_party_no", ":center_no", slot_village_farmer_party),
        (gt, ":farmer_party_no", 0),
        (party_is_active, ":farmer_party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (party_set_faction, ":farmer_party_no", ":center_faction"),
      (try_end),

    (try_begin),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
		(gt, ":lord_troop_id", -1),

#normal_banner_begin
        (troop_get_slot, ":cur_banner", ":lord_troop_id", slot_troop_banner_scene_prop),
        (try_begin),
            (gt, ":cur_banner", 0),
            (val_sub, ":cur_banner", banner_scene_props_begin),
            (val_add, ":cur_banner", banner_map_icons_begin),
            (party_set_banner_icon, ":center_no", ":cur_banner"),
# custom_banner_begin
       (else_try),
           (eq, ":cur_banner", -1),
           (troop_get_slot, ":flag_icon", ":lord_troop_id", slot_troop_custom_banner_map_flag_type),

           # (assign, reg0, ":flag_icon"),
           # (str_store_troop_name, s5, ":lord_troop_id",),
           # (display_message, "@{s5} : {reg0}"),

           (ge, ":flag_icon", 0),
           (val_add, ":flag_icon", custom_banner_map_icons_begin),
           (party_set_banner_icon, ":center_no", ":flag_icon"),
       (try_end),

       (neq, ":lord_troop_id", "trp_player"),
       #free all captive ladies
       (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
           (troop_get_slot, ":prisoner_of_party", ":lady", slot_troop_prisoner_of_party),
           (neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
           (eq, ":center_no", ":prisoner_of_party"),
           (call_script, "script_remove_troop_from_prison", ":lady"),
           (store_faction_of_troop, ":lady_faction", ":lady"),
           (store_faction_of_troop, ":release_faction", ":lord_troop_id"),
           (faction_get_color, ":lady_faction_color", ":lady_faction"),
           (str_store_troop_name_link, s1, ":lady"),
           (str_store_faction_name_link, s2, ":release_faction"),
           (str_store_faction_name_link, s3, ":lady_faction"),
           (display_log_message, "@{s1} of {s3} has been released from captivity by {s2}.", ":lady_faction_color"),
       (try_end),

    (try_end),

#    (try_begin),
#		(eq, 1, 0),
 #       (eq, ":lord_troop_id", "trp_player"),
 #       (neq, ":old_lord_troop_id", "trp_player"),
 #       (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
 #       (is_between, ":center_relation", -4, 5),
 #       (call_script, "script_change_player_relation_with_center", ":center_no", 5),
 #       (gt, ":old_lord_troop_id", 0),
 #       (call_script, "script_change_player_relation_with_troop", ":old_lord_troop_id", -25),
 #   (try_end),
	(try_begin),
		(gt, ":lord_troop_id", -1),
		(call_script, "script_update_troop_notes", ":lord_troop_id"),
	(try_end),

    (call_script, "script_update_center_notes", ":center_no"),

    (try_begin),
      (gt, ":lord_troop_faction", 0),
      (call_script, "script_update_faction_notes", ":lord_troop_faction"),
    (try_end),

    (try_begin),
        (ge, ":old_lord_troop_id", 0),
        (call_script, "script_update_troop_notes", ":old_lord_troop_id"),
        (store_troop_faction, ":old_lord_troop_faction", ":old_lord_troop_id"),
        (call_script, "script_update_faction_notes", ":old_lord_troop_faction"),
    (try_end),

    (try_begin),
        (eq, ":add_garrison", 1),
        (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":garrison_strength", 3),
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (assign, ":garrison_strength", 9),
        (try_end),
        (try_for_range, ":unused", 0, ":garrison_strength"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
        (try_end),
        ## ADD some XP initially
        (try_for_range, ":unused", 0, 7),
          (store_mul, ":xp_range_min", 150, ":garrison_strength"),
          (store_mul, ":xp_range_max", 200, ":garrison_strength"),
          (store_random_in_range, ":xp", ":xp_range_min", ":xp_range_max"),
          (party_upgrade_with_xp, ":center_no", ":xp", 0),
        (try_end),
    (try_end),

	(faction_get_slot, ":faction_leader", ":lord_troop_faction", slot_faction_leader),
	(store_current_hours, ":hours"),

	#the next block handles gratitude, objections and jealousies
	(try_begin),
	  	(gt, ":hours", 0),
		(gt, ":lord_troop_id", 0),

    	(call_script, "script_troop_change_relation_with_troop", ":lord_troop_id", ":faction_leader", 10),
		(val_add, "$total_promotion_changes", 10),

		#smaller factions are more dramatically influenced by internal jealousies
		#Disabled as of NOV 2010
#		(try_begin),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 4),
#			(assign, ":faction_size_multiplier", 6),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 8),
#			(assign, ":faction_size_multiplier", 5),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 16),
#			(assign, ":faction_size_multiplier", 4),
#		(else_try),
#			(neg|faction_slot_ge, ":lord_troop_faction", slot_faction_number_of_parties, 32),
#			(assign, ":faction_size_multiplier", 3),
#		(else_try),
#			(assign, ":faction_size_multiplier", 2),
#		(try_end),

		#factional politics -- each lord in the faction adjusts his relation according to the relation with the lord receiving the faction
		##diplomacy start+ add support for kingdom ladies
		#(try_for_range, ":other_lord", active_npcs_begin, active_npcs_end),
		(try_for_range, ":other_lord", heroes_begin, heroes_end),
		##diplomacy end+
			(troop_slot_eq, ":other_lord", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":other_lord", ":lord_troop_id"),

		    (store_troop_faction, ":other_troop_faction", ":other_lord"),
		    (eq, ":lord_troop_faction", ":other_troop_faction"),

		    (neq, ":other_lord", ":faction_leader"),

	        (call_script, "script_troop_get_relation_with_troop", ":other_lord", ":lord_troop_id"),
			(assign, ":relation_with_troop", reg0),

			#relation reduction = relation/10 minus 2. So,0 = -2, 8 = -1, 16+ = no change or bonus, 24+ gain one point
		    (store_div, ":relation_with_liege_change", ":relation_with_troop", 8), #changed from 16
		    (val_sub, ":relation_with_liege_change", 2),

		    (val_clamp, ":relation_with_liege_change", -5, 3),

			(try_begin),
				#upstanding and goodnatured lords will not lose relation unless they actively dislike the other lord
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
				 ##diplomacy start+ add companion/lady personality types
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_benefactor),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_conventional),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_moralist),
				 (this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_otherworldly),
				 ##diplomacy end+
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_goodnatured),
				(ge, ":relation_with_troop", 0),
				(val_max, ":relation_with_liege_change", 0),
			(else_try),
				#penalty is increased for lords who have the more unpleasant reputation types
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
				(lt, ":relation_with_liege_change", 0),
				(val_mul, ":relation_with_liege_change", 3),
				(val_div, ":relation_with_liege_change", 2),
			(try_end),
			##diplomacy start+

			#TODO (idea for "high"): instead of being absolute, the sliding score system should be used.
			#(So you can use a score instead of using relations.)  The greater the
			#difference in score, the greater the relation loss -- so if the lord
			#was nearly indifferent between two candidates, the difference would be
			#lesser.
			(try_begin),
				(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
				(try_begin),
					#Optional change: Non-jerkish lords will not object to giving a village to
					#someone fiefless, unless they dislike him.
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_debauched),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_selfrighteous),
					(neg|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_quarrelsome),
					(lt, ":relation_with_liege_change", 0),
					(is_between, ":center_no", villages_begin, villages_end),
					(troop_slot_eq, ":lord_troop_id", slot_troop_temp_slot, 0),
					(ge, ":relation_with_troop", 0),
					(val_max, ":relation_with_liege_change", 0),
				(try_end),
				(try_begin),
					#Optional change: because taking a penalty for 'thrashing' the same fief
					#back and forth is silly, if you're giving the fief back to the lord who
					#last had it, reduce any penalty.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),
					(neq, ":lord_troop_id", 0),
					(val_add, ":relation_with_liege_change", 1),

					#If the other lord doesn't have any claim of his own on the center,
					#attenuate the penalty more.
					(lt, ":relation_with_liege_change", 0),
					(ge, ":relation_with_troop", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),
					(val_add, ":relation_with_liege_change", 1),
				(else_try),
					#Similar logic, but for "original lord" instead of most recent lord
					(lt, ":relation_with_liege_change", 0),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":lord_troop_id"),#don't apply this if the above "ex-center" check was applied
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":lord_troop_id"),
						(troop_slot_eq, ":lord_troop_id", slot_troop_home, ":center_no"),

					#Only attenuate the panelty if the other lord doesn't have any claim of his own on the center
					(ge, ":relation_with_troop", 0),
					(neg|troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					(neg|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|neg|troop_slot_ge, ":other_lord", slot_troop_stance_on_faction_issue, 0),
						(neg|party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":other_lord"),

					(val_add, ":relation_with_liege_change", 1),
				(try_end),
				(try_begin),
					#On the minus side, lords whose homes and/or original fiefs are not
					#disposed according to their wishes are that much more cross.
					(lt, ":relation_with_liege_change", 1),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":other_lord"),
					(this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":other_lord"),
					   (troop_slot_eq, ":other_lord", slot_troop_home, ":center_no"),
					(val_sub, ":relation_with_liege_change", 1),
				(else_try),
					#Optional change: martial lords are less displeased by awarding a fief to
					#the one who conquered it.
					(lt, ":relation_with_liege_change", 0),
					(party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":lord_troop_id"),
					(this_or_next|troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_upstanding),
					(troop_slot_eq, ":other_lord", slot_lord_reputation_type, lrep_martial),
					(val_add, ":relation_with_liege_change", 1),
				(try_end),
			(try_end),
			##diplomacy end+

		    (neq, ":relation_with_liege_change", 0),
			#removed Nov 2010
#		  	(val_mul, ":relation_reduction", ":faction_size_multiplier"),
#		  	(val_div, ":relation_reduction", 2),
			#removed Nov 2010

			(try_begin),
				(troop_slot_eq, ":other_lord", slot_troop_stance_on_faction_issue, ":lord_troop_id"),
				(val_add, ":relation_with_liege_change", 1),
				(val_max, ":relation_with_liege_change", 1),
			(try_end),

 	        (call_script, "script_troop_change_relation_with_troop", ":other_lord", ":faction_leader", ":relation_with_liege_change"),
			(val_add, "$total_promotion_changes", ":relation_with_liege_change"),

		    (try_begin),
				(this_or_next|le, ":relation_with_liege_change", -4), #Nov 2010 - changed from -8
				(this_or_next|troop_slot_eq, ":other_lord", slot_troop_promised_fief, 1), #1 is any fief
					(troop_slot_eq, ":other_lord", slot_troop_promised_fief, ":center_no"),
				(call_script, "script_add_log_entry", logent_troop_feels_cheated_by_troop_over_land, ":other_lord", ":center_no", ":lord_troop_id", ":lord_troop_faction"),
		    (try_end),

		(try_end),
	(try_end),

	##diplomacy start+ invalidate cached center points
	(try_begin),
		(neq, ":old_lord_troop_id", ":lord_troop_id"),
		(try_begin),
			(gt, ":old_lord_troop_id", -1),
			(troop_set_slot, ":old_lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
		(try_begin),
			(gt, ":lord_troop_id", -1),
			(troop_set_slot, ":lord_troop_id", dplmc_slot_troop_center_points_plus_one, 0),
		(try_end),
	(try_end),
	##diplomacy end+

	#Villages from another faction will also be transferred along with a fortress
    (try_begin),
		(is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (try_for_range, ":cur_village", villages_begin, villages_end),
			(party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),
			(store_faction_of_party, ":cur_village_faction", ":cur_village"),
			(neq, ":cur_village_faction", ":lord_troop_faction"),

			(call_script, "script_give_center_to_lord", ":cur_village", ":lord_troop_id", 0),
        (try_end),
    (try_end),
  ]),

##  # script_give_town_to_besiegers
##  # Input: arg1 = center_no, arg2 = besieger_party
##  ("give_town_to_besiegers",
##    [
##      (store_script_param_1, ":center_no"),
##      (store_script_param_2, ":besieger_party"),
##      (store_faction_of_party, ":besieger_faction", ":besieger_party"),
##
##      (try_begin),
##        (call_script, "script_cf_get_party_leader", ":besieger_party"),
##        (assign, ":new_leader", reg0),
##      (else_try),
##        (call_script, "script_select_kingdom_hero_for_new_center", ":besieger_faction"),
##        (assign, ":new_leader", reg0),
##      (try_end),
##
##      (call_script, "script_give_center_to_lord", ":center_no", ":new_leader"),
##
##      (try_for_parties, ":party_no"),
##        (get_party_ai_object, ":object", ":party_no"),
##        (get_party_ai_behavior, ":behavior", ":party_no"),
##        (eq, ":object", ":center_no"),
##        (this_or_next|eq, ":behavior", ai_bhvr_travel_to_party),
##        (eq, ":behavior", ai_bhvr_attack_party),
##        (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
##        (party_set_slot, ":party_no", slot_party_ai_state, spai_undefined),
##        (party_set_flags, ":party_no", pf_default_behavior, 0),
##      (try_end),
##
##      #Staying at the center for a while
##      (party_set_ai_behavior, ":besieger_party", ai_bhvr_hold),
##      (party_set_slot, ":besieger_party", slot_party_ai_state, spai_undefined),
##      (party_set_flags, ":besieger_party", pf_default_behavior, 0),
##
##      (faction_get_slot, ":reinforcement_a", ":besieger_faction", slot_faction_reinforcements_a),
##      (faction_get_slot, ":reinforcement_b", ":besieger_faction", slot_faction_reinforcements_b),
##      (party_add_template, ":center_no", ":reinforcement_a"),
##      (party_add_template, ":center_no", ":reinforcement_b"),
##  ]),
##

  # script_get_number_of_hero_centers
  # Input: arg1 = troop_no
  # Output: reg0 = number of centers that are ruled by the hero
  ("get_number_of_hero_centers",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ]),


  ##  # script_cf_get_new_center_leader_chance_for_troop
  ##  # Input: arg1 = troop_no
  ##  # Output: reg0 = chance of the troop to rule a new center
  ##  ("cf_get_new_center_leader_chance_for_troop",
  ##    [
  ##      (store_script_param_1, ":troop_no"),
  ##      (troop_get_slot, ":troop_rank", ":troop_no", slot_troop_kingdom_rank),
  ##      (try_begin),
  ##        (eq, ":troop_rank", 4),
  ##        (assign, ":troop_chance", 1000),
  ##      (else_try),
  ##        (eq, ":troop_rank", 3),
  ##        (assign, ":troop_chance", 800),
  ##      (else_try),
  ##        (eq, ":troop_rank", 2),
  ##        (assign, ":troop_chance", 400),
  ##      (else_try),
  ##        (eq, ":troop_rank", 1),
  ##        (assign, ":troop_chance", 100),
  ##      (else_try),
  ##        (assign, ":troop_chance", 10),
  ##      (try_end),
  ##
  ##      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
  ##      (assign, ":number_of_hero_centers", reg0),
  ##      (try_begin),
  ##        (gt, ":number_of_hero_centers", 0),
  ##        (val_mul, ":number_of_hero_centers", 2),
  ##        (val_mul, ":number_of_hero_centers", ":number_of_hero_centers"),
  ##        (val_div, ":troop_chance", ":number_of_hero_centers"),
  ##      (try_end),
  ##      (assign, reg0, ":troop_chance"),
  ##      (eq, reg0, 0),
  ##      (assign, reg0, 1),
  ##  ]),


##  # script_select_kingdom_hero_for_new_center
##  # Input: arg1 = faction_no
##  # Output: reg0 = troop_no as the new leader
##  ("select_kingdom_hero_for_new_center",
##    [
##      (store_script_param_1, ":kingdom"),
##
##      (assign, ":min_num_centers", -1),
##      (assign, ":min_num_centers_troop", -1),
##
##      (try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
##        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##        (store_troop_faction, ":troop_faction", ":troop_no"),
##        (eq, ":troop_faction", ":kingdom"),
##        (call_script, "script_get_number_of_hero_centers", ":troop_no"),
##        (assign, ":num_centers", reg0),
##        (try_begin),
##          (lt, ":num_centers", ":min_num_centers"),
##          (assign, ":min_num_centers", ":num_centers"),
##          (assign, ":min_num_centers_troop", ":troop_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":min_num_centers_troop"),
##  ]),


  # script_cf_get_random_enemy_center
  # Input: arg1 = party_no
  # Output: reg0 = center_no
  ("cf_get_random_enemy_center",
    [
      (store_script_param_1, ":party_no"),

      (assign, ":result", -1),
      (assign, ":total_enemy_centers", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_add, ":total_enemy_centers", 1),
      (try_end),

      (gt, ":total_enemy_centers", 0),
      (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
      (assign, ":total_enemy_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (store_relation, ":party_relation", ":center_faction", ":party_faction"),
        (lt, ":party_relation", 0),
        (val_sub, ":random_center", 1),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


##  # script_get_random_enemy_town
  # Input: arg1 = village_no, arg2 = amount, arg3 = single_cost
  # Output: reg0 = party_no
  ("buy_cattle_from_village",
    [
      (store_script_param, ":village_no", 1),
      (store_script_param, ":amount", 2),
      (store_script_param, ":single_cost", 3),

      #Changing price of the cattle
      (try_for_range, ":unused", 0, ":amount"),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
        (call_script, "script_game_event_buy_item", "itm_cattle_meat", 0),
      (try_end),

      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_sub, ":num_cattle", ":amount"),
      (party_set_slot, ":village_no", slot_village_number_of_cattle, ":num_cattle"),
      (store_mul, ":cost", ":single_cost", ":amount"),
      (troop_remove_gold, "trp_player", ":cost"),
      #SB : add gold back to elder
      (try_begin),
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
        (party_get_slot, ":elder", ":village_no", slot_town_elder),
        (gt, ":elder", 0),
        (troop_add_gold, ":elder", ":cost"),
      (try_end),

      (assign, ":continue", 1),
      (try_for_parties, ":cur_party"),
        (eq, ":continue", 1),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":village_no", ":cur_party"),
        (lt, ":dist", 6),
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        (party_add_members, ":cur_party", "trp_cattle", ":amount"),
        (assign, ":continue", 0),
        (assign, reg0, ":cur_party"),
      (try_end),
      (try_begin),
        (eq, ":continue", 1),
        (call_script, "script_create_cattle_herd", ":village_no", ":amount"),
      (try_end),
  ]),

  #script_kill_cattle_from_herd
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_consumption",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_consumption", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_consumption", 500),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_consumption", 50),
      (try_end),
      ##diplomacy start+
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 #Optional change: increase food consumption with garrison size
		 #The rationale goes like this:
		 #The average reinforcement size for a town or castle is 9.5 per round.
		 #At the start of the game:
		 #
		 #  Castles get 15 reinforcement rounds, for around 142.5 troops
		 #  Towns   get 40 reinforcement rounds, for around 380 troops
		 #
		 #Of course both the castles and the towns have other people living
		 #there as well.
		 (party_get_num_companions, ":garrison_size", ":center_no"),
		 (try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(gt, ":garrison_size", 150),
			#Assume that the garrison accounts for most of the food consumption.
			(store_div, ":food_consumption", ":garrison_size", 3),
		 (else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(gt, ":garrison_size", 380),
			#Assume that the garrison makes the same contribution to size for towns.
			(store_div, ":food_consumption", ":garrison_size", 3),#for 381, equals 127
			(val_add, ":food_consumption", 500 - 127),
		 (try_end),

		 #Optional change: increase food consumption with prosperity
		 (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (party_get_slot, reg0, ":center_no", slot_town_prosperity),
			(gt, reg0, 50),#<- increase only
         (val_add, reg0, 75),
         (val_mul, ":food_consumption", reg0),
         (val_add, ":food_consumption", 62),
         (val_div, ":food_consumption", 125),
      (try_end),
      ##diplomacy+
      (assign, reg0, ":food_consumption"),
  ]),

  # script_center_get_food_store_limit
  # Input: arg1 = center_no
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("center_get_food_store_limit",
    [
      (store_script_param_1, ":center_no"),
      (assign, ":food_store_limit", 0),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign, ":food_store_limit", 50000),
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (assign, ":food_store_limit", 1500),
      (try_end),
      (assign, reg0, ":food_store_limit"),
  ]),

  # script_refresh_village_merchant_inventory
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_merchant_inventory",
    [
      (store_script_param_1, ":village_no"),
      (party_get_slot, ":merchant_troop", ":village_no", slot_town_elder),
      (reset_item_probabilities,0),

	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),

	  (assign, ":total_probability", 0),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_good"),
		(assign, ":cur_probability", reg0),

        (call_script, "script_center_get_production", ":bound_center", ":cur_good"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),

		(val_max, ":cur_probability", 5),
		(val_add, ":total_probability", ":cur_probability"),
      (try_end),

	  (try_begin),
		(party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
		(val_div, ":prosperity", 15), #up to 6
		(store_add, ":number_of_items_in_village", ":prosperity", 1),
	  (try_end),

      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
	    (call_script, "script_center_get_production", ":village_no", ":cur_good"),
		(assign, ":cur_probability", reg0),

        (call_script, "script_center_get_production", ":bound_center", ":cur_good"),
		(val_div, reg0, 5), #also add 1/5 of bound center production to village's inventory.
		(val_add, ":cur_probability", reg0),

		(val_max, ":cur_probability", 5),
        (val_mul, ":cur_probability", ":number_of_items_in_village"),
		(val_mul, ":cur_probability", 100),
		(val_div, ":cur_probability", ":total_probability"),

        (set_item_probability_in_merchandise, ":cur_good", ":cur_probability"),
      (try_end),

      #SB : probably do something like trash item at base values
      (troop_clear_inventory, ":merchant_troop"),
      (troop_add_merchandise, ":merchant_troop", itp_type_goods, ":number_of_items_in_village"),
      (troop_ensure_inventory_space, ":merchant_troop", 80),

      #Adding 1 prosperity to the village while reducing each 3000 gold from the elder
      (store_troop_gold, ":gold",":merchant_troop"),
      (try_begin),
        (gt, ":gold", 3500),
        (store_div, ":prosperity_added", ":gold", 3000),
        (store_mul, ":gold_removed", ":prosperity_added", 3000),
        (troop_remove_gold, ":merchant_troop", ":gold_removed"),
        (call_script, "script_change_center_prosperity", ":village_no", ":prosperity_added"),
      (try_end),
  ]),

  # script_refresh_village_defenders
  # Input: arg1 = village_no
  # Output: none
  ("refresh_village_defenders",
    [
      (store_script_param_1, ":village_no"),

      (assign, ":ideal_size", 50),
      (try_begin),
        (party_get_num_companions, ":party_size", ":village_no"),
        (lt, ":party_size", ":ideal_size"),
        #SB : add restriction of not reinforcing while looted or infested
        (call_script, "script_cf_village_normal_cond", ":village_no"),
        (party_add_template, ":village_no", "pt_village_defenders"),

        (try_begin), #SB : upgrade into watchmen, each template had at least 10 farmers
          (party_slot_ge, ":village_no", slot_center_has_watch_tower, 1),
          (party_count_companions_of_type, ":count", ":village_no", "trp_watchman"),
          (lt, ":count", 10),
          (store_random_in_range, ":random_no", 2, 5),
          (party_add_members, ":village_no", "trp_watchman", ":random_no"),
          (party_remove_members, ":village_no", "trp_farmer"),
        (try_end),
        (try_begin), #SB : add messenger
          (party_slot_ge, ":village_no", slot_center_has_messenger_post, 1),
          (store_faction_of_party, ":faction_no", ":village_no"),
          (assign, ":troop", "trp_dplmc_messenger"),
          (try_begin),
            (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
            (faction_get_slot, ":troop", ":faction_no", slot_faction_messenger_troop),
          (try_end),
          (party_count_companions_of_type, ":count", ":village_no", ":troop"),
          (lt, ":count", 1),
          (party_add_members, ":village_no", ":troop", 1),
        (try_end),
      (try_end),
  ]),

  # script_village_set_state
  # Input: arg1 = center_no arg2:new_state
  # Output: reg0: food consumption (1 food item counts as 100 units)
  ("village_set_state",
    [
      (store_script_param_1, ":village_no"),
      (store_script_param_2, ":new_state"),
      ##diplomacy start+
      (store_current_hours, ":hours"),
      (party_get_slot, ":attacker_party", ":village_no", slot_village_raided_by),
      (try_begin),
        (ge, ":attacker_party", 0),
        (party_is_active, ":attacker_party"),#added 2011-06-07
        (party_stack_get_troop_id, ":attack_leader", ":attacker_party", 0),
        (ge, ":attack_leader", 0),
        (party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
        (party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":attack_leader"),


        (try_begin),
          (this_or_next|eq, ":new_state", svs_looted),
          (eq, ":new_state", svs_deserted),
          #SB : there's a fire whether real or fake, we set the bounding center to have guards investigate
          (try_begin),
            (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
            (is_between, ":bound_center", centers_begin, centers_end),
            (party_set_slot, ":bound_center", slot_town_last_nearby_fire_time, ":hours"),
          (try_end),
          #SB : quest state
          (try_begin),
            (check_quest_active, "qst_hunt_down_fugitive"),
            (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_target_center, ":village_no"),
            #if we found and knocked him out in mission template this won't fire
            (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
            (neg|check_quest_failed, "qst_hunt_down_fugitive"),
            (quest_set_slot, "qst_hunt_down_fugitive", slot_quest_current_state, 3),
            (try_begin), #conclude quest if village raided
              (neq, ":attacker_party", "p_main_party"),
              (call_script, "script_conclude_quest", "qst_hunt_down_fugitive"),
            (else_try), #player raided village for some reason
              (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
      ##diplomacy end+

      (try_begin),
        (eq, ":new_state", svs_normal),
        (party_set_extra_text, ":village_no", "str_empty_string"),
        #SB : redo village recruits immediately
        (try_begin),
          (this_or_next|le, ":attacker_party", 0),
          (neg|party_is_active, ":attacker_party"),
          (is_between, ":village_no", villages_begin, villages_end), #dckplmc
          (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
          (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
        (try_end),
        (party_set_slot, ":village_no", slot_village_raided_by, -1),
      (else_try),
        (eq, ":new_state", svs_being_raided),
        (party_set_extra_text, ":village_no", "@(Being Raided)"),
      (else_try), #SB : deserted state as alternative to full looting
        (eq, ":new_state", svs_deserted),
        (party_set_extra_text, ":village_no", "@(Deserted)"),

        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -20),
		(val_add, "$newglob_total_prosperity_from_villageloot", -20),
      (else_try),
        (eq, ":new_state", svs_looted),
        (party_set_extra_text, ":village_no", "@(Looted)"),

        (party_set_slot, ":village_no", slot_village_raided_by, -1),
        (call_script, "script_change_center_prosperity", ":village_no", -60),
		(val_add, "$newglob_total_prosperity_from_villageloot", -60),

		# (try_begin), #optional - lowers the relationship between a lord and his liege if his fief is looted
			# (eq, 5, 0),
			# (party_get_slot, ":town_lord", ":village_no", slot_town_lord),
			# (is_between, ":town_lord", active_npcs_begin, active_npcs_end),
			# (store_faction_of_troop, ":town_lord_faction", ":town_lord"),
			# (faction_get_slot, ":faction_leader", ":town_lord_faction", slot_faction_leader),
			# (call_script, "script_troop_change_relation_with_troop", ":town_lord", ":faction_leader", -1),
			# (val_add, "$total_battle_ally_changes", -1),
		# (try_end),
      (else_try),
        (eq, ":new_state", svs_under_siege),
        (party_set_extra_text, ":village_no", "@(Under Siege)"),

		#Divert all caravans heading to the center
		#Note that occasionally, no alternative center will be found. In that case, the caravan will try to run the blockade
		(try_for_parties, ":party_no"),
			(gt, ":party_no", "p_spawn_points_end"),
			(party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":village_no"),

			(party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
			(store_faction_of_party, ":merchant_faction", ":party_no"),
            ##diplomacy start+ added new third parameter, the caravan party itself
            (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":origin", ":merchant_faction",":party_no"),
			##diplomacy end+
            (assign, ":target_center", reg0),
			(is_between, ":target_center", centers_begin, centers_end),

            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":target_center"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
            (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
		(try_end),
      (try_end),
      (party_set_slot, ":village_no", slot_village_state, ":new_state"),
  ]),


  # script_process_village_raids
  # Input: none
  # Output: none
  # called from triggers every two hours
  ("process_village_raids",
    [
       ##diplomacy start+
       (store_current_hours, ":hours"),
       ##diplomacy end+
       (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB: also move to top
       (try_for_range, ":village_no", villages_begin, villages_end),
        ##CABA Fix
        (try_begin),
          # Snow Check
          (this_or_next|is_between, ":village_no", "p_village_16", "p_village_23"), #Shapeshte through Shulus (up to Ilvia)
          (this_or_next|is_between, ":village_no", "p_village_49", "p_village_51"), #Tismirr and Karindi
          (this_or_next|eq, ":village_no", "p_village_75"), #Bhulaban
          (this_or_next|is_between, ":village_no", "p_village_85", "p_village_87"), #Ismirala and Slezkh
          (eq, ":village_no", "p_village_112"),
          (assign, ":normal_village_icon", "icon_village_snow_a"),
          (assign, ":burnt_village_icon", "icon_village_snow_burnt_a"),
          (assign, ":deserted_village_icon", "icon_village_snow_deserted_a"),
        (else_try),
          # Desert Check (Exclude your new villages from the catch-all group)
          (is_between, ":village_no", "p_village_91", "p_village_111"), #Ayn Assuadi through Rushdigh
          (assign, ":normal_village_icon", "icon_village_c"),
          (assign, ":burnt_village_icon", "icon_village_burnt_c"),
          (assign, ":deserted_village_icon", "icon_village_deserted_c"),
        (else_try),
          # Catch-all Default (This now handles standard plain villages
          (assign, ":normal_village_icon", "icon_village_a"),
          (assign, ":burnt_village_icon", "icon_village_burnt_a"),
          (assign, ":deserted_village_icon", "icon_village_deserted_a"),
        (try_end),
        ##CABA Fix
         (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
         (try_begin),
           (party_slot_eq, ":village_no", slot_village_state, svs_normal), #village is normal
           (val_sub, ":village_raid_progress", 5),
           (val_max, ":village_raid_progress", 0),
           (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
           (try_begin),
             (lt, ":village_raid_progress", 50),

             (try_begin),
              (party_get_icon, ":village_icon", ":village_no"),
              (neq, ":village_icon", ":normal_village_icon"), ##CABA FIX
              (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX
             (try_end),

             (party_slot_ge, ":village_no", slot_village_smoke_added, 1),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),
           (try_end),
         (else_try),
           (party_slot_eq, ":village_no", slot_village_state, svs_being_raided), #village is being raided
           #End raid unless there is an enemy party nearby
           (assign, ":raid_ended", 1),
           (party_get_slot, ":raider_party", ":village_no", slot_village_raided_by),
           # (call_script, "script_party_count_fit_regulars", ":village_no"), #SB : calculate cur size
           # (assign, ":villager_count", reg0),
           # (party_get_num_companions, ":villager_count", ":village_no"), #SB : calculate cur size, including wounded
           (call_script, "script_party_calculate_strength", ":village_no", 0),
           (store_div, ":village_strength", reg0, 2),
           (try_begin),
             (ge, ":raider_party", 0),
             (party_is_active, ":raider_party"),
             (party_stack_get_troop_id, ":raid_leader", ":raider_party", 0), #SB : moved to top
             (this_or_next|neq, ":raider_party", "p_main_party"),
             (eq, "$g_player_is_captive", 0),
             #SB : strength conditional, player bypasses this however since they actually fought
             (call_script, "script_party_calculate_strength", ":raider_party", 0),
             (this_or_next|eq, ":raider_party", "p_main_party"), #player raiding conditions are different
             (ge, reg0, ":village_strength"),
             # (party_slot_ge, ":raider_party", slot_party_cached_strength, ":village_strength"),
             (store_distance_to_party_from_party, ":distance", ":village_no", ":raider_party"),
             (lt, ":distance", raid_distance),
             (party_get_battle_opponent, ":raid_opponent", ":raider_party"), #dckplmc
             (lt, ":raid_opponent", 0), #continue raid only if there is no opposition
             (assign, ":raid_ended", 0),
           (try_end),

           (try_begin),
             (eq, ":raid_ended", 1),
             (call_script, "script_village_set_state", ":village_no", svs_normal), #clear raid flag
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_clear_particle_systems, ":village_no"),
           (else_try),
             (assign, ":raid_progress_increase", 11),
             (party_get_slot, ":looter_party", ":village_no", slot_village_raided_by),
             (try_begin),
               (party_get_skill_level, ":looting_skill", ":looter_party", "skl_looting"),
               (val_add, ":raid_progress_increase", ":looting_skill"),
             (try_end),
             (try_begin),
               (party_slot_eq, ":village_no", slot_center_has_watch_tower, 1),
               (val_mul, ":raid_progress_increase", 2),
               (val_div, ":raid_progress_increase", 3),
             (try_end),
             (val_add, ":village_raid_progress", ":raid_progress_increase"),
             #SB : delay construction while being looted
             (try_begin),
               (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
               (party_slot_ge, ":village_no", slot_center_current_improvement, 1),
               (party_get_slot, ":cur_improvement_end_time", ":village_no", slot_center_improvement_end_hour),
               (store_div, ":delay", ":raid_progress_increase", 3),
               (try_begin),
                 (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (val_sub, ":delay", ":reduce_campaign_ai"),
               (try_end),
               (val_clamp, ":delay", 2, 8), #delayed for at least duration of raid
               (val_add, ":cur_improvement_end_time", ":delay"),
             (try_end),
             (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
             (try_begin),
               (ge, ":village_raid_progress", 50),
               (party_slot_eq, ":village_no", slot_village_smoke_added, 0),
               (party_add_particle_system, ":village_no", "psys_map_village_fire"),
               (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
               (party_set_icon, ":village_no", ":burnt_village_icon"), ##CABA FIX
               (party_set_slot, ":village_no", slot_village_smoke_added, 1),
             (try_end),
			 ##diplomacy start+ set values of slots
			 (try_begin),
				(ge, ":looter_party", 0),
				# (party_stack_get_troop_id, ":raid_leader", ":looter_party", 0),
				(ge, ":raid_leader", 0),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacked_time, ":hours"),
				(party_set_slot, ":village_no", dplmc_slot_center_last_attacker, ":raid_leader"),
			 (try_end),
             (assign, ":raid_total_captured", 0),
             (try_begin), #SB : enslavement mode
               (eq, ":looter_party", "p_main_party"),
               (party_slot_eq, ":village_no", slot_town_last_nearby_fire_time, 2), #enslavement mode

               #do some wounding first, in the first iteration all wounded from the initial encounter will be grabbed
               (store_random_in_range, ":random_no", ":reduce_campaign_ai", 4), #0 to 2 up to 3 per iteration
               (party_wound_members, ":village_no", "trp_farmer", ":random_no"),
               #(val_mul, ":random_no", 2),
               #(val_div, ":random_no", 3),
               (party_wound_members, ":village_no", "trp_peasant_woman", ":random_no"),

               #this is only effective for p_main_party anyway
               (call_script, "script_game_get_party_prisoner_limit", ":looter_party"),
               (assign, ":prisoner_limit", reg0),
               (party_get_num_prisoners, ":num_prisoners", ":looter_party"),
               (val_sub, ":prisoner_limit", ":num_prisoners"),

               (party_get_num_companion_stacks, ":num_stacks", ":village_no"),
               # (assign, ":num_wounded", 0),
               (party_get_slot, ":village_raid_progress", ":village_no", slot_village_raid_progress),
               (try_for_range_backwards, ":stack_no", 0, ":num_stacks"), #backwards to enslave women first
                 (party_stack_get_num_wounded, ":cur_wounded",":village_no",":stack_no"),
                 (gt, ":cur_wounded", 0),
                 (party_stack_get_troop_id, ":stack_troop",":village_no",":stack_no"),

                 (try_begin),
                    (lt, ":prisoner_limit", ":cur_wounded"),
                    (val_add, ":raid_total_captured", ":prisoner_limit"),
                    (party_remove_members_wounded_first, ":village_no", ":stack_troop", ":prisoner_limit"),
                    (party_add_prisoners, "p_main_party", ":stack_troop", ":prisoner_limit"),
                 (else_try),
                    (val_add, ":raid_total_captured", ":cur_wounded"),
                    (party_remove_members_wounded_first, ":village_no", ":stack_troop", ":cur_wounded"),
                    (party_add_prisoners, "p_main_party", ":stack_troop", ":cur_wounded"),
                 (try_end),

                 (try_begin),
                   (val_sub, ":prisoner_limit", ":cur_wounded"),
                   (le, ":prisoner_limit", 0),
                   (assign, ":num_stacks", 0),
                 (try_end),
               (try_end),
               (assign, reg1, ":raid_total_captured"),
               (try_begin),
                 (neq, reg1, 0),
                 (display_message, "@Captured {reg1} villagers."),
                 (val_add, "$qst_eliminate_bandits_infesting_village_num_villagers", ":raid_total_captured"),
               (try_end),
               (try_begin),
                 (party_get_num_companions, ":amount", ":village_no"),
                 (this_or_next|eq, ":amount", 0), #we have captured all
                 (eq, ":num_stacks", 0), #we have captured too many and broke the loop
                 (assign, ":raid_total_captured", -1), #mark this condition for later
               (else_try),
                 #for each three prisoner taken we move back the counter a bit
                 (store_div, ":amount", ":raid_total_captured", 3),
                 (val_sub, ":village_raid_progress", ":amount"),
                 (party_set_slot, ":village_no", slot_village_raid_progress, ":village_raid_progress"),
               (try_end),
             (try_end),
             #SB : probably spawn random refugees here as the raid progresses
             ##diplomacy end+
             #SB : add in enslavement function at around 75% completion, simulate each level taking off 0.5 hour
             #if the looting skill is too high we won't capture as many peasants
             (try_begin),
               (eq, ":looter_party", "p_main_party"),
               (party_slot_eq, ":village_no", slot_town_last_nearby_fire_time, 2), #enslavement mode
               (party_get_skill_level, ":management", ":looter_party", "skl_prisoner_management"),
               (val_mul, ":management", 5), #0 to 50 to 75
               (val_div, ":management", 3), #around 25
               (store_sub, ":threshold", 90, ":management"), #make sure this is before regular looting completes
               # (party_get_num_companions, ":amount", ":village_no"),
               # (party_get_free_prisoners_capacity, ":capacity", "p_main_party"), #or use previous calculation
               # (this_or_next|le, ":amount", 0), #we have wounded and captured all inhabitants
               # (this_or_next|le, ":capacity", 0), #we have no more room for capturing
               (this_or_next|eq, ":raid_total_captured", -1),
               (gt, ":village_raid_progress", ":threshold"),

               (str_store_party_name_link, s1, ":village_no"),
               (str_store_troop_name_link, s2, ":raid_leader"),
               (store_faction_of_party, ":village_faction", ":village_no"),
               (faction_get_color, ":color", ":village_faction"),
               (display_log_message, "@The village of {s1} has been sacked by {s2}.", ":color"),

               (try_begin),
                 (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
                 (is_between, ":village_lord", active_npcs_begin, active_npcs_end),
                 (call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
                 (val_add, "$total_battle_enemy_changes", -1),
               (try_end),
               (call_script, "script_village_set_state",  ":village_no", svs_deserted), #not svs_looted, less prosperity decrease
               # (party_set_slot, ":village_no", slot_center_accumulated_rents, 0),
               # (party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0),
               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 50), #SB : jumps directly to deserted icon, not burnt
               (party_set_slot, ":village_no", slot_village_smoke_added, 2), #to force trigger the icon

               (try_begin), #SB : this crippled lords too much
                 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_amount, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_amount, -1),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
               (store_faction_of_party, ":looter_faction", ":looter_party"), #enslavement less severe than plundering
               (call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 4),
             (else_try),
               (gt, ":village_raid_progress", 100),
               (str_store_party_name_link, s1, ":village_no"),
               # (party_stack_get_troop_id, ":raid_leader", ":looter_party", 0), #SB : move to top
               (ge, ":raid_leader", 0),
               #SB : colorize, string link
               # (str_store_party_name, s2, ":looter_party"),
               (try_begin),
                 (troop_is_hero, ":raid_leader"),
                 (str_store_troop_name_link, s2, ":raid_leader"),
               (else_try),
                 (str_store_party_name, s2, ":looter_party"),
               (try_end),
               (store_faction_of_party, ":village_faction", ":village_no"),
               (faction_get_color, ":color", ":village_faction"),
               (display_log_message, "@The village of {s1} has been looted by {s2}.", ":color"),

               #refugees
               (set_spawn_radius, 2),
               (spawn_around_party, ":village_no", "pt_refugees"),
               (assign, ":refugee_party", reg0),
               (party_add_template, ":refugee_party", "pt_village_farmers"),
               (party_add_template, ":refugee_party", "pt_village_farmers"),
               (party_set_faction, ":refugee_party", ":village_faction"),
               (assign, ":minimum_distance", 1000000),
               #SB : get rid of useless range
               (store_random_in_range, ":nearest_ally_city", walled_centers_begin, walled_centers_end),
               (try_for_range, ":party_no", walled_centers_begin, walled_centers_end),
                 (party_get_position, pos1, ":party_no"),
                 (store_distance_to_party_from_party, ":dist", ":party_no", ":village_no"),
                 (try_begin),
                   (lt, ":dist", ":minimum_distance"),
                   (assign, ":minimum_distance", ":dist"),
                   (assign, ":nearest_ally_city", ":party_no"),
                 (try_end),
               (try_end),
               (party_set_ai_behavior, ":refugee_party", ai_bhvr_travel_to_party),
               (party_set_ai_object, ":refugee_party", ":nearest_ally_city"),
               (party_set_slot, ":refugee_party", slot_party_home_center, ":village_no"),

               (try_begin),
                 (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
                 (is_between, ":village_lord", active_npcs_begin, active_npcs_end),
                 (call_script, "script_troop_change_relation_with_troop", ":raid_leader", ":village_lord", -1),
                 (val_add, "$total_battle_enemy_changes", -1),
               (try_end),

               #give loot gold to raid leader
               (troop_get_slot, ":raid_leader_gold", ":raid_leader", slot_troop_wealth),
			   ##diplomacy start+
			   #How did the next line ever work?  isn't it missing a slot number?!
               #  (party_get_slot, ":village_prosperity", ":village_no"),
			   #Replace it with the following:
			   (party_get_slot, ":village_prosperity", ":village_no", slot_town_prosperity),
			   ##diplomacy end+
               (store_mul, ":value_of_loot", ":village_prosperity", 60), #average is 3000
               (val_add, ":raid_leader_gold", ":value_of_loot"),
               (troop_set_slot, ":raid_leader", slot_troop_wealth, ":raid_leader_gold"),
			   (try_begin),
				   (eq, "$cheat_mode", 2),
				   (assign, reg2, ":raid_leader_gold"),
				   (str_store_troop_name_link, s2, ":raid_leader"),
				   (display_message, "@{s2} now has {reg2} denars from raiding"),#SB : debug
               (try_end),
               #take loot gold from village lord #new 1.126
			   ##diplomacy start+
			   #With economic changes enabled, this will first withdraw from accumulated taxes at center
               (try_begin),
				 #To support the possibility of kingdom_ladies becoming enfeoffed, changed the
				 #below line from active_npcs_begin/active_npcs_end to heroes_begin/heroes_end
                 (is_between, ":village_lord", heroes_begin, heroes_end),
				 (neq, ":village_lord", "trp_kingdom_heroes_including_player_begin"),
                 (troop_get_slot, ":village_lord_gold", ":village_lord", slot_troop_wealth),
				 (try_begin),
					#Optional behavior: subtract the looted wealth from the village's uncollected
					#rents and tariffs
					(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- check experimental changes are enabled
					(assign, ":gold_lost_by_lord", ":value_of_loot"),
					#Accumulated rents & tariffs get zeroed further down, so we don't need to worry
					#about modifying the slot's value to reflect the loss.
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					(party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
					(val_max, ":x", 0),
					(val_sub, ":gold_lost_by_lord", ":x"),
					#Only then subtract the remainder from the lord
					(val_max, ":gold_lost_by_lord", 0),
					(val_sub, ":village_lord_gold", ":gold_lost_by_lord"),
				 (else_try),
					#Unaltered behavior
					(val_sub, ":village_lord_gold", ":value_of_loot"),
				 (try_end),
				 #Apply the gold change
                 (val_max, ":village_lord_gold", 0),
                 (troop_set_slot, ":village_lord", slot_troop_wealth, ":village_lord_gold"),
                 (try_begin),
                    (eq, "$cheat_mode", 2),
                     (assign, reg2, ":village_lord_gold"),
                     (str_store_troop_name_link, s2, ":village_lord"),
                     (display_message, "@{s2} now has {reg2} denars from being raided"),#SB : debug
                 (try_end),
			   (else_try),
			      #Option: player loses gold when his fiefs are raided, just as an NPC does
				  #(default behavior in Native is the player loses no gold).  The gold is
				  #lost from the treasury, and is reduced by uncollected taxes.
				  #
				  #Only do this if the option is explicitly enabled and the player has
				  # a chamberlain.
				  (eq, ":village_lord", "trp_player"),
				  (gt, "$g_player_chamberlain", 0),#check the player has a chamberlain
			      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- check experimental changes are enabled
				  (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
				  #Do some double-checking, to avoid potential erroneous gold loss
				  #if some careless code has improperly left the "slot_town_lord"
				  #slot of the village initialized to zero.
				  (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
				  (this_or_next|eq, "fac_player_supporters_faction", ":village_faction"),
				     (eq, "$players_kingdom", ":village_faction"),
				  #Adjust the amount lost by difficulty setting.
				  (assign, ":gold_lost_by_lord", ":value_of_loot"),
				  # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"), #SB: move to top
				  (try_begin),
				    (eq, ":reduce_campaign_ai", 0),#hard, 125% loss
					(val_mul, ":gold_lost_by_lord", 5),
					(val_div, ":gold_lost_by_lord", 4),
				  (else_try),
					(eq, ":reduce_campaign_ai", 1),#medium, 100% loss
				  (else_try),
					(eq, ":reduce_campaign_ai", 2),#easy, 50% loss
					(val_div, ":gold_lost_by_lord", 2),
				  (try_end),

				  #First defray the lost gold with rents and tarriffs from the village
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_rents),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (party_get_slot, ":x", ":village_no", slot_center_accumulated_tariffs),
				  (val_max, ":x", 0),
				  (val_sub, ":gold_lost_by_lord", ":x"),
				  (val_max, ":gold_lost_by_lord", 0),
				  #Remove the remainder (if any) from the player's treasury
				  (store_troop_gold, ":x", "trp_household_possessions"),
				  (val_min, ":gold_lost_by_lord", ":x"),
				  (ge, ":gold_lost_by_lord", 1),
				  (call_script, "script_dplmc_withdraw_from_treasury", ":gold_lost_by_lord"),
               (try_end),
			   ##diplomacy end+

               (call_script, "script_village_set_state",  ":village_no", svs_looted),
               (party_set_slot, ":village_no", slot_center_accumulated_rents, 0), #new 1.126
               (party_set_slot, ":village_no", slot_center_accumulated_tariffs, 0), #new 1.126

               (party_set_slot, ":village_no", slot_village_raid_progress, 0),
               (party_set_slot, ":village_no", slot_village_recover_progress, 0),

               #SB : also get rid of recruits, technically they should have perished in the fighting
               (try_begin), #SB : this crippled lords too much
                 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_volunteer_troop_amount, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_type, -1),
                 (party_set_slot, ":village_no", slot_center_npc_volunteer_troop_amount, -1),
               (try_end),
               #finally clear the party
               # (party_clear, ":village_no"),
               (call_script, "script_party_wound_all_members", ":village_no"),
               (try_begin),
                 (store_faction_of_party, ":village_faction", ":village_no"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
 				 (try_begin),
				    (eq, ":village_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
                 (this_or_next|party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
                 (eq, ":village_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_village_raided", ":village_no", ":raid_leader"),
               (try_end),
               (call_script, "script_add_log_entry", logent_village_raided, ":raid_leader",  ":village_no", -1, -1),
               (store_faction_of_party, ":looter_faction", ":looter_party"),
               (call_script, "script_faction_inflict_war_damage_on_faction", ":looter_faction", ":village_faction", 5),
             (try_end),
           (try_end),
         (else_try),
           (this_or_next|party_slot_eq, ":village_no", slot_village_state, svs_looted), #village is looted
           (party_slot_eq, ":village_no", slot_village_state, svs_deserted), #SB : village is deserted
           (party_get_slot, ":recover_progress", ":village_no", slot_village_recover_progress),
           (val_add, ":recover_progress", 1),
           (party_set_slot, ":village_no", slot_village_recover_progress, ":recover_progress"), #village looted

           (try_begin), #SB : add some looters, around twice per lifetime
             (store_mod, ":looter_chance", ":recover_progress", 10),
             (eq, ":looter_chance", 0),
             (store_random_in_range, ":random_value", 0, 5),
             (eq, ":random_value", 0),
             (set_spawn_radius, 5),
             (spawn_around_party, ":village_no", "pt_looters"),
           (try_end),
           (try_begin),
             (ge, ":recover_progress", 10),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 1),
             (party_clear_particle_systems, ":village_no"),
             (party_add_particle_system, ":village_no", "psys_map_village_looted_smoke"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 2),
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 50),
             (party_slot_eq, ":village_no", slot_village_smoke_added, 2),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 3),
             (party_set_icon, ":village_no", ":deserted_village_icon"), ##CABA FIX
           (try_end),
           (try_begin),
             (gt, ":recover_progress", 100),
             (call_script, "script_village_set_state",  ":village_no", svs_normal),#village back to normal
             (party_set_slot, ":village_no", slot_village_recover_progress, 0),
             (party_clear_particle_systems, ":village_no"),
             (party_set_slot, ":village_no", slot_village_smoke_added, 0),
             (party_set_icon, ":village_no", ":normal_village_icon"), ##CABA FIX
           (try_end),
         (try_end),
       (try_end),
  ]),


  # script_process_sieges
  #It is used for lord to (1)Court ladies (2)Collect rents (3)Look for volunteers
  ## Upgrade equipment (by quality) and hire mercenaries (if Martial personality)
  ("troop_does_business_in_center",
  [
    (store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
	##diplomacy start+
	#Call this once and reuse below.
	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
	(assign, ":is_affiliated", reg0),
	#Also enable for the spouse, unless you're on bad terms
	(try_begin),
		(lt, ":is_affiliated", 0),
		(this_or_next|troop_slot_eq,":troop_no",slot_troop_spouse, "trp_player"),
			(troop_slot_eq,"trp_player",slot_troop_spouse, ":troop_no"),
		(call_script, "script_troop_get_player_relation", ":troop_no"),
		(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		(val_add, reg0, ":persuasion"),
		#reduce magnitude, since >= 0 succeeds
		(store_sub, ":persuasion_modifier", 20, ":persuasion"),
		(val_mul, reg0, ":persuasion_modifier"),
		(val_div, reg0, 20),
		#final number must be >= -5
		(ge, reg0, -5),
		(assign, ":is_affiliated", 1),
	(try_end),
	##diplomacy end+

    (troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
    (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), #SB : moved up
    (assign, ":initial_wealth", ":troop_wealth"), #DEBUG

    (store_current_hours, ":current_time"),
    (try_begin),
#      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"), #this was added to get lords in centers out and visiting their fiefs, but I've adjusted the decision checklist
      (is_between, ":center_no", walled_centers_begin, walled_centers_end),
      (party_set_slot, ":led_party", slot_party_last_in_any_center, ":current_time"),
      (try_begin),
        (call_script, "script_lord_get_home_center", ":troop_no"),
        (eq, ":center_no", reg0),
        (party_set_slot, ":led_party", slot_party_last_in_home_center, ":current_time"),
      (try_end),
    (try_end),

    #Collect the rents
    (try_begin),
      (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

      (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      # (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
      (val_add, ":troop_wealth", ":accumulated_rents"),
      (val_add, ":troop_wealth", ":accumulated_tariffs"),

      (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
      (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),

      ## upgrade owned centers

      (call_script, "script_calculate_improvement_limit", ":troop_no", ":center_no"),
      (assign, ":limit", reg0),

      (try_begin),
        (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
        (gt, ":troop_wealth", ":limit"), #surplus cash
        (party_slot_eq, ":center_no", slot_center_current_improvement, 0), #not already building
        (assign, ":continue", 1),
        #this randomization applies so that there is a chance of not building an improvement (1/6) or (4/6)
        (store_random_in_range, ":improvement_no", village_improvements_begin, walled_center_improvements_end),
        (party_slot_eq, ":center_no", ":improvement_no", 0), #not already built
        (try_begin), #villages
          (party_slot_eq, ":center_no", slot_party_type, spt_village),
          (ge, ":improvement_no", village_improvements_end),
          (assign, ":continue", 0),
        (else_try), #towns, castles
          (lt, ":improvement_no", walled_center_improvements_begin),
          (assign, ":continue", 0),
        (try_end),
        (eq, ":continue", 1),
        (call_script, "script_get_improvement_details", ":improvement_no"),
        (assign, ":improvement_cost", reg0), # 4000-9000
        # calculate cost offset from lord
        (store_attribute_level, ":int", ":troop_no", ca_intelligence), #10-70
        (store_skill_level, ":skill", "skl_engineer", ":troop_no"), #0 to 15
        (val_mul, ":skill", ":int"), # 0 to 105
        (store_character_level, ":level", ":troop_no"), #22-50
        (val_add, ":skill", ":level"),
        (val_sub, ":improvement_cost", ":skill"),

        #get working strength
        (party_get_num_companions, ":divider", ":center_no"), #0~300, ignoring wounded
        (party_get_num_prisoners, ":num_prisoners", ":center_no"), #possibly up to 100
        (val_min, ":num_prisoners", 100),

        #account for serfs, each level past base adds 25 effective manpower
        (store_faction_of_party, ":faction_no", ":center_no"),
        (faction_get_slot, ":serfdom", ":faction_no", dplmc_slot_faction_serfdom),
        (val_add, ":serfdom", 3),
        (val_mul, ":serfdom", 25),
        (val_add, ":divider", ":serfdom"),
        (gt, ":divider", ":num_prisoners"),

        #calculate time - manpower, prosperity, and int/level-based
        (party_get_slot, ":multiplier", ":center_no", slot_town_prosperity), #0 to 100
        (val_sub, ":multiplier", ":num_prisoners"), #feeding drags prosperity down
        (store_sub, ":multiplier", 300, ":multiplier"), #300 to 100
        (val_add, ":divider", ":skill"), #total 30~500 added from lord

        (store_mul, ":improvement_time", ":improvement_cost", ":multiplier"), #400000 - 2700000
        (val_div, ":improvement_time", 100),
        (val_div, ":improvement_time", ":divider"), #18.18~800
        (lt, ":improvement_time", 160), #feasible
        (val_max, ":improvement_time", 3), #not instantaneous

        (val_sub, ":troop_wealth", ":improvement_cost"),
        (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
        (try_begin),
          (this_or_next|eq, "$cheat_mode", 3),
          (ge, ":is_affiliated", 1),#<-- dplmc+ added
          (assign, reg6, ":improvement_time"),
          (str_store_troop_name_link, s10, ":troop_no"),
          #s0 comes from improvement_details
          (display_log_message, "@{s10} constructs a {s0} in {s4}", message_alert),
        (try_end),
        (assign, "$g_improvement_type", ":improvement_no"),
        # (assign, reg6, ":improvement_time"),
        (call_script, "script_improve_center", ":center_no", ":troop_no", ":improvement_time"),
      (try_end),
      ##
      ##diplomacy start+
      #Modify the next block to display for affiliates
      (try_begin),
        (this_or_next|ge, ":is_affiliated", 1),#<-- dplmc+ added
        (this_or_next|eq, "$cheat_mode", 1),
        (eq, "$cheat_mode", 3),
        (assign, reg1, ":troop_wealth"),
        (str_store_party_name_link, s4, ":center_no"),
        (add_troop_note_from_sreg, ":troop_no", 1, "str_current_wealth_reg1_taxes_last_collected_from_s4", 0),
        #New section, print a message for affiliates:
        (ge, ":is_affiliated", 1),
        (store_add, reg0, ":accumulated_rents", ":accumulated_tariffs"),
        (str_store_troop_name_link, s0, ":troop_no"),
        (try_begin),
           (gt, reg0, 0),
           (display_log_message, "@{s0} collects {reg0} denars from {s4}, current wealth: {reg1} denars"),
        (try_end),
      (try_end),
      ##diplomacy end+
    (try_end),

    #Recruit volunteers
    (try_begin),
        (is_between, ":center_no", villages_begin, villages_end),
        (party_get_slot, ":troop_amount", ":center_no", slot_center_npc_volunteer_troop_amount),
        (gt, ":troop_amount", 0),

        (party_get_slot, ":troop_type", ":center_no", slot_center_npc_volunteer_troop_type),
        (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, -1),
        ##diplomacy begin
        (try_begin),
          (store_faction_of_party, ":party_faction", ":led_party"),
          (eq, ":party_faction", "fac_player_supporters_faction"),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (faction_get_slot, ":troop_type", "$g_player_culture", slot_faction_tier_1_troop),
        (try_end),

        (try_begin), #debug
          ##nested diplomacy start+
          (this_or_next|ge, ":is_affiliated", 1),#<- Show for affiliates
          (eq, "$cheat_mode", 1),
          ##nested diplomacy end+
          (assign, reg2, ":troop_amount"),
          # (str_store_string, s11, "@{reg2}"),
          (str_store_troop_name, s12, ":troop_type"),
          (str_store_faction_name_link, s13, ":party_faction"),
          (str_store_party_name_link, s14, ":center_no"),
          (str_store_party_name, s10, ":led_party"),
          (display_log_message, "@ {s10} of {s13} recruits {reg2} {s12} in {s14}"),
        (try_end),

        ##diplomacy end
        (party_add_members, ":led_party", ":troop_type", ":troop_amount"),
    (else_try), ##do business in centers
      (is_between, ":center_no", towns_begin, towns_end),
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),

      (try_begin), #hiring mercenaries
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_morality_type, tmt_egalitarian),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_2ary_morality_type, tmt_egalitarian),
        (this_or_next|troop_slot_eq, ":troop_no", slot_troop_2ary_morality_type, tmt_aristocratic),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        (party_get_slot, ":mercenary_troop", ":center_no", slot_center_mercenary_troop_type),
        (gt, ":mercenary_troop", 0),
        (store_character_level, ":level", ":mercenary_troop"),
        #chance of not hiring
        (store_random_in_range, ":reduce", ":level", 100),
        (gt, ":reduce", 69), #favors high-level
        # (game_get_reduce_campaign_ai, ":reduce"), #0 to 2
        # (val_mul, ":reduce", 5), #0 to 10
        # (store_sub, ":reduce", 26, ":reduce"), #26 to 16
        # (lt, ":level", ":reduce"), #no special mercs - on hard can hire top-tier, on easy caravan guard/xbow/lower
        (party_get_slot, ":mercenary_amount", ":center_no", slot_center_mercenary_troop_amount),
        (call_script, "script_game_get_join_cost", ":mercenary_troop"),
        (assign, ":troop_cost", reg0),
        # (try_begin), #slight discount for improvement
          # (party_get_slot, ":reduce", ":center_no", slot_center_has_mercenary_hall),
          # (val_add, ":reduce", 5),
          # (val_mul, ":troop_cost", 5),
          # (val_div, ":troop_cost", ":reduce"),
        # (try_end),
        #test wealth levels - a tenth normally can be used
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (faction_get_slot, ":quality", ":faction_no", dplmc_slot_faction_quality),
        (val_add, ":quality", 10),
        #use faction quality to determine percentage of wealth used for mercenaries
        (store_div, ":divider", ":troop_wealth", ":quality"),
        (val_div, ":divider", ":troop_cost"),
        (val_min, ":divider", ":mercenary_amount"),


        #set the proper slots
        (try_begin),
          (gt, ":divider", 0),
          (party_add_members, ":led_party", ":mercenary_troop", ":divider"),
          (val_mul, ":troop_cost", ":divider"),
          (val_sub, ":troop_wealth", ":troop_cost"),
          (store_sub, ":mercenary_amount", ":mercenary_amount", ":divider"),
          (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, ":mercenary_amount"),
          (try_begin),
            (le, ":mercenary_amount", 0),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, -1),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_type, -1),
          (else_try),
            (party_set_slot, ":center_no", slot_center_mercenary_troop_amount, ":mercenary_amount"),
          (try_end),
          (try_begin), #debug
            (this_or_next|ge, ":is_affiliated", 1),#<- Show for affiliates
            (ge, "$cheat_mode", 1),
            (assign, reg2, ":divider"),
            (str_store_troop_name_by_count, s12, ":mercenary_troop", reg2),
            (display_log_message, "@{s10} hires {reg2} {s12} in {s4}"),
          (try_end),
        (try_end),
      (try_end),
      ##upgrade equipment from merchants
      (call_script, "script_calculate_equipment_limit", ":troop_no", ":center_no"),
      (assign, ":equipment_limit", reg0),
      #we assume startup gear is sufficient - only quality matters
      # (try_for_range, ":slot", ek_item_0, ek_food), #can't only check equipment, it'll reload if you visit lord's hall
      (troop_get_inventory_capacity, ":cap", ":troop_no"),
      (try_for_range, ":slot", ek_item_0, ":cap"),
        (gt, ":troop_wealth", ":equipment_limit"), #has spare cash
        (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot"),
        (neq, ":item_no", -1),
        (neg|item_has_property, ":item_no", itp_unique),
        (neg|item_has_property, ":item_no", itp_civilian), #why bother upgrading underwear
        (item_has_property, ":item_no", itp_merchandise), #can be sold, although player can drop loot off
        (troop_get_inventory_slot_modifier, ":old_imod", ":troop_no", ":slot"),
        # (item_get_slot, ":imod_mult", ":old_imod", slot_item_modifier_multiplier),
        (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":old_imod"),
        (assign, ":imod_mult", reg0),
        (try_begin),
          (is_between, ":slot", ek_item_0, ek_head),
          (assign, ":merchant", slot_town_weaponsmith),
        (else_try),
          (is_between, ":slot", ek_item_0, ek_head),
          (assign, ":merchant", slot_town_armorer),
        (else_try),
          (eq, ":slot", ek_horse),
          (assign, ":merchant", slot_town_horse_merchant),
        (try_end),
        (party_get_slot, ":merchant", ":center_no", ":merchant"),
        #valid merchant
        (is_between, ":merchant", armor_merchants_begin, mayors_begin),
        (troop_get_inventory_capacity, ":cap", ":merchant"),
        (try_for_range, ":i_slot", 10, ":cap"),
          (troop_get_inventory_slot, ":item_id", ":merchant", ":i_slot"),
          (eq, ":item_id", ":item_no"), #same item found
          (troop_get_inventory_slot_modifier, ":imod", ":merchant", ":i_slot"),
          (neq, ":imod", ":old_imod"), ## in general higher imod = upgrade

          # (is_between, ":imod", imod_balanced, imod_large_bag + 1), #eliminate bad+plain ones
          # (item_get_slot, ":imod_cost", ":imod", slot_item_modifier_multiplier),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_id", ":imod"),
          (assign, ":imod_cost", reg0),
          (gt, ":imod_cost", ":imod_mult"), #superior price not necessarily better quality
          #troop can use item
          (call_script, "script_dplmc_troop_can_use_item", ":troop_no", ":item_id", ":imod"),
          (eq, reg0, 1),
          #we go for a pure value ratio - get_trade_penalty applies to player only
          (store_item_value, ":val", ":item_no"),
          (store_sub, ":cost", ":imod_cost", ":imod_mult"),
          (val_mul, ":cost", ":val"),
          (val_div, ":cost", 100),#base
          (gt, ":troop_wealth", ":cost"),
          (try_begin), #debug
            (eq, "$cheat_mode", 2),
            #(str_store_string, s11, "@{reg2}"),

            # (str_store_party_name_link, s14, ":center_no"),
            (str_store_item_name, s11, ":item_no"),
            (str_store_troop_name_link, s10, ":troop_no"),
            (str_store_party_name_link, s4, ":center_no"),
            (store_add, ":string", ":old_imod", "str_imod_plain"),
            (str_store_string, s3, ":string"),
            (call_script, "script_game_get_money_text", ":cost"),
            (assign, reg0, ":troop_wealth"),
            (display_log_message, "@{s10} upgrades {s3}{s11} (costing {s1}) in {s4}, {reg0} denars remaining."),
          (try_end),
          (val_sub, ":troop_wealth", ":cost"),
          (troop_set_inventory_slot_modifier, ":troop_no", ":slot", ":imod"),
          (troop_set_inventory_slot_modifier, ":merchant", ":i_slot", ":old_imod"),
          (troop_add_gold, ":merchant", ":cost"),
          (assign, ":cap", 10), #one item has one upgrade at a time
        (try_end),
      (try_end),
      ##upgrade end
    (try_end),

    # SB : set wealth after tax and consumption
    (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
    #DEBUG
    (try_begin),
	  (eq, "$cheat_mode", 2),
      (neq, ":troop_wealth", ":initial_wealth"),
      (assign, reg1, ":initial_wealth"),
      (str_store_troop_name_link, s1, ":troop_no"),
      (str_store_party_name_link, s2, ":center_no"),
      (assign, reg2, ":troop_wealth"),
      (display_message, "@{s1} spends time in {s2}, {reg1} -> {reg2} denars"),
    (try_end),
    #Courtship
    (try_begin),
		(party_get_slot, ":time_of_last_courtship", ":led_party", slot_party_leader_last_courted),
		(store_sub, ":hours_since_last_courtship", ":current_time", ":time_of_last_courtship"),
		(gt, ":hours_since_last_courtship", 72),

		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		##diplomacy start+ Disable this for inappropriate types
		(neg|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),#They use the last visited slots for other purposes
		(neg|is_between, ":troop_no", kings_begin, kings_end),#They should not be participating in this system
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),#They should not be participating in this system
		##diplomacy end+
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
			(gt, ":love_interest", 0),
			(troop_get_slot, ":love_interest_town", ":love_interest", slot_troop_cur_center),
			(eq, ":center_no", ":love_interest_town"),

			(call_script, "script_courtship_event_troop_court_lady", ":troop_no", ":love_interest"),
			(party_set_slot, ":led_party", slot_party_leader_last_courted, ":current_time"),
		(try_end),
    (try_end),

    ]),

  # script_process_kingdom_parties_ai
  # Input: arg1: faction_no
  # Output: none
  #called from triggers
  ("begin_assault_on_center",
   [
     (store_script_param, ":center_no", 1),
	 ##diplomacy start+ add support for promoted kingdom ladies
     (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	 ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),

       (assign, ":continue", 0),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
         (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
         (assign, ":continue", 1),
       (else_try),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),
         (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
         (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
         (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
         (assign, ":continue", 1),
       (try_end),

       (eq, ":continue", 1),

       (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
       (party_set_ai_object, ":party_no", ":center_no"),
       (party_set_flags, ":party_no", pf_default_behavior, 1),
       (party_set_slot, ":party_no", slot_party_ai_substate, 1),
     (try_end),
   ]),

  #DEPRECATED - Using new political issue system instead
  # Input: arg1: center_no, arg2: target_faction_no
  # Output: reg0: relation
  #called from triggers
  ("get_center_faction_relation_including_player",
   [
     (store_script_param, ":center_no", 1),
     (store_script_param, ":target_faction_no", 2),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (store_relation, ":relation", ":center_faction", ":target_faction_no"),
     (try_begin),
       (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
       (store_relation, ":relation", "fac_player_supporters_faction", ":target_faction_no"),
     (try_end),
     (assign, reg0, ":relation"),
     ]),

   #script_update_report_to_army_quest_note
  # Input: arg1 = party_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":difference"),

      (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 100),
      (assign, reg2, ":player_relation"),
      (party_set_slot, ":center_no", slot_center_player_relation, ":player_relation"),

      (try_begin),
        (le, ":player_relation", -50),
        (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
      (try_end),


      (str_store_party_name_link, s1, ":center_no"),
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "@Your relation with {s1} has improved.", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "@Your relation with {s1} has deteriorated.", message_negative),
      (try_end),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        (call_script, "script_update_volunteer_troops_in_village", ":center_no"),
      (try_end),

      (try_begin),
        (this_or_next|is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
        (is_between, "$g_talk_troop", mayors_begin, mayors_end),
        ##diplomacy start+
		  #Fix potential bug: don't adjust relations except with *that* center's
		  #mayor.
		  (party_slot_eq, ":center_no", slot_town_elder, "$g_talk_troop"),
	    ##diplomacy end+
        (assign, "$g_talk_troop_relation", ":player_relation"),
        (call_script, "script_setup_talk_info"),
      (try_end),
  ]),


  # script_change_player_relation_with_faction
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("enter_dungeon",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),

      (set_jump_mission,":mission_template_no"),
      #new added...
      (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_horse),
      (try_begin),
        (gt, "$sneaked_into_town", disguise_none),
        (mission_tpl_entry_set_override_flags, ":mission_template_no", 0, af_override_everything), #boots + gloves
        # (mission_tpl_entry_clear_override_items, ":mission_template_no", 0),
        #SB : different disguises
        (call_script, "script_set_disguise_override_items", ":mission_template_no", 0, 0), #no weapons
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_pilgrim_hood"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_wrapping_boots"), #SB add boots
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_pilgrim_disguise"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_practice_staff"),
        # (mission_tpl_entry_add_override_item, ":mission_template_no", 0, "itm_throwing_daggers"),
      (try_end),
      #new added end

      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),

      (modify_visitors_at_site,":dungeon_scene"),
      (reset_visitors),
      (assign, ":cur_pos", 16),


      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      ##diplomacy start+ Allow some variation in which prisoners appear,
      #when there are too many to all fit in the jail at once.
      (try_begin),
         	(gt, ":num_stacks", 15),
            (store_random_in_range, ":offset", 0, ":num_stacks"),
      (else_try),
           	(assign, ":offset", 0),
      (try_end),
      ##diplomacy end+
      (try_for_range, ":i_stack", 0, ":num_stacks"),
      ##diplomacy start+
        (val_add, ":i_stack", ":offset"),
        (try_begin),
           (ge, ":i_stack", ":num_stacks"),
           (val_sub, ":i_stack", ":num_stacks"),
        (try_end),
      ##diplomacy end+
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),

		(assign, ":prisoner_offered_parole", 0),
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(else_try),
			(call_script, "script_cf_prisoner_offered_parole", ":stack_troop"),
			(assign, ":prisoner_offered_parole", 1),
		(else_try),
			(assign, ":prisoner_offered_parole", 0),
		(try_end),
		(eq, ":prisoner_offered_parole", 0),

        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),

#	  (set_visitor, ":cur_pos", "trp_npc3"),
#	  (troop_set_slot, "trp_npc3", slot_troop_prisoner_of_party, "$g_encountered_party"),

      (set_jump_entry, 0),
      (jump_to_scene,":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),

  # script_enter_court
  # Input: none
  # Output: reg0 = number of unclaimed centers, reg1 = last unclaimed center_no
  ("get_number_of_unclaimed_centers_by_player",
    [
      (assign, ":unclaimed_centers", 0),
      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (party_slot_eq, ":center_no", slot_town_claimed_by_player, 0),
        (party_get_num_companion_stacks, ":num_stacks", ":center_no"),
        (ge, ":num_stacks", 1), #castle is garrisoned
        (assign, reg1, ":center_no"),
        (val_add, ":unclaimed_centers", 1),
      (try_end),
      (assign, reg0, ":unclaimed_centers"),
  ]),

  # script_troop_count_number_of_enemy_troops
  # Input: arg1 = troop_no, arg2 = center index within range between zero and the number of centers that troop owns
  # Output: reg0 = center_no
  ("troop_get_leaded_center_with_index",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  # script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority
  # Input: arg1 = troop_no, arg2 = preferred_center_no
  # Output: reg0 = center_no (Can fail)
  ("cf_troop_get_random_leaded_walled_center_with_less_strength_priority",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":preferred_center_no", 2),

      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_add, ":num_centers", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_add, ":num_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":center_no"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":num_centers", ":strength"),
      (try_end),
      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":center_no", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":center_no"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  # script_cf_troop_get_random_leaded_town_or_village_except_center
  # Input: arg1 = troop_no, arg2 = except_center_no
  # Output: reg0 = center_no (Can fail)
  #SB : only called from checking qst_collect_taxes, apply condition as follows
  ## not close to arg2 (Native only checks if quest giver is inside town)
  ## not under siege/raided (arg3)
  ("cf_troop_get_random_leaded_town_or_village_except_center",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":except_center_no", 2), #unused I guess
      (store_script_param, ":center_state", 3), #pass in svs_normal

	  #SB : re-use except_center_no as a check
	  (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
	  (try_begin),
	    (le, ":party_no", 0),
		(assign, ":party_no", ":except_center_no"),
	  (try_end),
      (assign, ":num_centers", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),

	    # (party_set_slot, ":center_no", slot_party_temp_slot_1, 0),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (neq, ":center_no", ":except_center_no"),
		(assign, ":dist", 9999),
		(try_begin),
		  (gt, ":party_no", 0),
		  (store_distance_to_party_from_party, ":dist", ":center_no", ":party_no"),
		(try_end),
		(gt, ":dist", 15), #can't be within a day's travel
		(party_slot_eq, ":center_no", slot_village_state, ":center_state"),
		# (party_set_slot, ":center_no", slot_party_temp_slot_1, 1),
		(troop_set_slot, "trp_random_town_sequence", ":num_centers", ":center_no"),
        (val_add, ":num_centers", 1),
      (try_end),

      (gt, ":num_centers", 0),
      (store_random_in_range, ":random_center", 0, ":num_centers"),
	  (troop_get_slot, reg0, "trp_random_town_sequence", ":random_center"),
      # (assign, ":end_cond", centers_end),
      # (try_for_range, ":center_no", centers_begin, ":end_cond"),
        # (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        # (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        # (neq, ":center_no", ":except_center_no"),
        # (val_sub, ":random_center", 1),
        # (lt, ":random_center", 0),
        # (assign, ":target_center", ":center_no"),
        # (assign, ":end_cond", 0),
      # (try_end),
      # (assign, reg0, ":target_center"),
  ]),

  # script_troop_write_owned_centers_to_s2
  # Input: arg1 = troop_no
  # Output: none
  ("troop_write_owned_centers_to_s2",
    [
      (store_script_param_1, ":troop_no"),

      (call_script, "script_get_number_of_hero_centers", ":troop_no"),
      (assign, ":no_centers", reg0),

      (str_store_troop_name, s5, ":troop_no"),

      (try_begin),
        (gt, ":no_centers", 1),
        (try_for_range, ":i_center", 1, ":no_centers"),
          (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", ":i_center"),
          (str_store_party_name_link, s50, reg0),
          (try_begin),
            (eq, ":i_center", 1),
            (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
            (str_store_party_name_link, s51, reg0),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
        (try_end),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (eq, ":no_centers", 1),
        (call_script, "script_troop_get_leaded_center_with_index", ":troop_no", 0),
        (str_store_party_name_link, s51, reg0),
        (str_store_string, s2, "str_s5_is_the_ruler_of_s51"),
      (else_try),
        (store_troop_faction, ":faction_no", ":troop_no"),
        (str_store_faction_name_link, s6, ":faction_no"),
        ##diplomacy start+ make gender-correct
        #(troop_get_type, reg4, ":troop_no"),
        (assign, ":save_reg4", reg4),
        (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
        (str_store_string, s2, "str_s5_is_a_nobleman_of_s6"),
        (assign, reg4, ":save_reg4"),
        ##diplomacy end+
      (try_end),
  ]),

    # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_center_relation_to_s3",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_center_relation_mnus_100",  ":str_offset"),
      (str_store_string, s3, ":str_id"),
  ]),


  # script_center_ambiance_sounds
  # Input: none
  # Output: none
  # to be called every two seconds
  ("center_ambiance_sounds",
    [
        (assign, ":sound_1", -1),
        (assign, ":sound_2", -1),
        (assign, ":sound_3", -1),
        (assign, ":sound_4", -1),
        (assign, ":sound_5", -1),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_3", "snd_distant_dog_bark"),
            (assign, ":sound_3", "snd_distant_chicken"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
            (assign, ":sound_2", "snd_distant_owl"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (neg|is_currently_night),
            (assign, ":sound_1", "snd_distant_carpenter"),
            (assign, ":sound_2", "snd_distant_blacksmith"),
            (assign, ":sound_3", "snd_distant_dog_bark"),
          (else_try),
            (assign, ":sound_1", "snd_distant_dog_bark"),
          (try_end),
        (try_end),
        (try_begin),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq, ":r", 1),
            (ge, ":sound_1", 0),
            (play_sound, ":sound_1"),
          (else_try),
            (eq, ":r", 2),
            (ge, ":sound_2", 0),
            (play_sound, ":sound_2"),
          (else_try),
            (eq, ":r", 3),
            (ge, ":sound_3", 0),
            (play_sound, ":sound_3"),
          (else_try),
            (eq, ":r", 4),
            (ge, ":sound_4", 0),
            (play_sound, ":sound_4"),
          (else_try),
            (eq, ":r", 5),
            (ge, ":sound_5", 0),
            (play_sound, ":sound_5"),
          (try_end),
        (try_end),
  ]),

  # script_center_set_walker_to_type
  # Input: arg1 = center_no, arg2 = walker_no, arg3 = walker_type,
  # Output: none
  ("center_set_walker_to_type",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_no", 2),
       (store_script_param, ":walker_type", 3),
       (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
       (party_set_slot, ":center_no", ":type_slot", ":walker_type"),
       (party_get_slot, ":center_faction", ":center_no", slot_center_original_faction),
       (faction_get_slot, ":center_culture", ":center_faction", slot_faction_culture),
       (store_random_in_range, ":walker_troop_slot", 0, 2),
       (try_begin),
         (party_slot_eq, ":center_no", slot_party_type, spt_village),
         (val_add, ":walker_troop_slot", slot_faction_village_walker_male_troop),
       (else_try),
         (val_add, ":walker_troop_slot", slot_faction_town_walker_male_troop),
       (try_end),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (assign,":original_walker_slot",":walker_troop_slot"),
         (val_add,":walker_troop_slot",4), # select spy troop id slot
       (try_end),
       (faction_get_slot, ":walker_troop_id", ":center_culture", ":walker_troop_slot"),
       (try_begin),
         (eq,":walker_type", walkert_spy),
         (faction_get_slot, ":original_walker", ":center_culture", ":original_walker_slot"),
         # restore spy inventory
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (lt,":num_items",1),
            (troop_add_items,":walker_troop_id",":item_no",1),
         (try_end),
         # determine spy recognition item
         (store_random_in_range,":spy_item_type",itp_type_head_armor,itp_type_hand_armor),
         (assign,":num",0),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":walker_troop_id"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (troop_remove_items,":walker_troop_id",":item_no",":num_items"),
         (try_end),
         (store_random_in_range,":random_item",0,":num"),
         (assign,":num",-1),
         (try_for_range,":item_no","itm_horse_meat","itm_wooden_stick"),
            (store_item_kind_count,":num_items",":item_no",":original_walker"),
            (ge,":num_items",1),
            (item_get_type, ":itp", ":item_no"),
            (eq,":itp",":spy_item_type"),
            (val_add,":num",1),
            (eq,":num",":random_item"),
            (troop_add_items,":walker_troop_id",":item_no",1),
            (assign,":spy_item",":item_no"),
         (try_end),
         (assign,"$spy_item_worn",":spy_item"),
         (assign,"$spy_quest_troop",":walker_troop_id"),
         (troop_equip_items,":walker_troop_id"),
       (try_end),
       (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
       (party_set_slot, ":center_no", ":troop_slot", ":walker_troop_id"),
       (store_random_in_range, ":walker_dna", 0, 1000000),
       (store_add, ":dna_slot", slot_center_walker_0_dna, ":walker_no"),
       (party_set_slot, ":center_no", ":dna_slot", ":walker_dna"),
     ]),


  # script_cf_center_get_free_walker
  # Input: arg1 = center_no
  # Output: reg0 = walker no (can fail)
  ("cf_center_get_free_walker",
   [
       (store_script_param, ":center_no", 1),
       (assign, ":num_free_walkers", 0),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_add, ":num_free_walkers", 1),
       (try_end),
       (gt, ":num_free_walkers", 0),
       (assign, reg0, -1),
       (store_random_in_range, ":random_rank", 0, ":num_free_walkers"),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", walkert_default),
         (val_sub, ":num_free_walkers", 1),
         (eq, ":num_free_walkers", ":random_rank"),
         (assign, reg0, ":walker_no"),
       (try_end),
     ]),

  # script_center_remove_walker_type_from_walkers
  # Input: arg1 = center_no, arg2 = walker_type,
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("center_remove_walker_type_from_walkers",
   [
       (store_script_param, ":center_no", 1),
       (store_script_param, ":walker_type", 2),
       (try_for_range, ":walker_no", 0, num_town_walkers),
         (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
         (party_slot_eq, ":center_no", ":type_slot", ":walker_type"),
         (call_script, "script_center_set_walker_to_type", ":center_no", ":walker_no", walkert_default),
       (try_end),
     ]),


  # script_init_town_walkers
  # Input: none
  # Output: none
  ("init_town_walkers",
  [
    (try_begin),
      (eq, "$town_nighttime", 0),
      (try_for_range, ":walker_no", 0, num_town_walkers),
        (store_add, ":troop_slot", slot_center_walker_0_troop, ":walker_no"),
        (party_get_slot, ":walker_troop_id", "$current_town", ":troop_slot"),
        (gt, ":walker_troop_id", 0),
        (store_add, ":entry_no", town_walker_entries_start, ":walker_no"),
        (set_visitor, ":entry_no", ":walker_troop_id"),
      (try_end),
    (try_end),
  ]),


  # script_cf_enter_center_location_bandit_check
  # Input: none
  # Output: none
  ("cf_enter_center_location_bandit_check",
    [
      (neq, "$town_nighttime", 0),
      (party_slot_ge, "$current_town", slot_center_has_bandits, 1),
      (eq, "$g_defending_against_siege", 0),#Skip if the center is under siege (because of resting)
      (eq, "$sneaked_into_town", disguise_none),#Skip if sneaked
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (party_get_slot, ":cur_scene", "$current_town", slot_castle_exterior),
      (else_try),
        (party_get_slot, ":cur_scene", "$current_town", slot_town_center),
      (try_end),
      (modify_visitors_at_site, ":cur_scene"),
      (reset_visitors),
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (store_character_level, ":level", "trp_player"),

      (set_jump_mission, "mt_bandits_at_night"),
      (try_begin),
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (assign, ":spawn_amount", 2),
        (store_div, ":level_fac",  ":level", 10),
        (val_add, ":spawn_amount", ":level_fac"),
        (try_for_range, ":unused", 0, 3),
          (gt, ":level", 10),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (val_add, ":spawn_amount", 1),
        (try_end),
        (set_visitors, 4, ":bandit_troop", ":spawn_amount"),
        (assign, "$num_center_bandits", ":spawn_amount"),
        (set_jump_entry, 2),
      (else_try),
        (assign, ":spawn_amount", 1),
        (assign, "$num_center_bandits", 0),
        (try_begin),
          (gt, ":level", 15),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (set_visitors, 11, ":bandit_troop", ":spawn_amount"),
        (assign, ":spawn_amount", 1),
        (try_begin),
          (gt, ":level", 20),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":level"),
          (assign, ":spawn_amount", 2),
        (try_end),
        (set_visitors, 27, ":bandit_troop", ":spawn_amount"),
        (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_begin),
          (gt, ":level", 9),
          (assign, ":spawn_amount", 1),
          (try_begin),
            (gt, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (lt, ":random_no", ":level"),
            (assign, ":spawn_amount", 2),
          (try_end),
          (set_visitors, 28, ":bandit_troop", ":spawn_amount"),
          (val_add, "$num_center_bandits",  ":spawn_amount"),
        (try_end),
        (assign, "$town_entered", 1),
        (assign, "$all_doors_locked", 1),
      (try_end),

      (display_message, "@You have run into a trap!", message_negative),
      #SB : store actual bandit names
      (str_store_troop_name_plural, s1, ":bandit_troop"),
      (display_message, "@You are attacked by a group of {s1}!", message_negative),
      (play_sound, "snd_encounter_looters"), #more generic than bandit sounds
      (jump_to_scene, ":cur_scene"),
      (change_screen_mission),
      ]),

  # script_init_town_agent
  # Input: none
  # Output: none
  ("init_town_agent",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_troop_id, ":troop_no", ":agent_no"),
      (set_fixed_point_multiplier, 100),
      (assign, ":stand_animation", -1),
      (try_begin),
        (this_or_next|is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
        (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
        (try_begin),
          (troop_get_type, ":cur_troop_gender", ":troop_no"),
          (eq, ":cur_troop_gender", 0),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (else_try),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (end_try),
      (else_try),
        (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (assign, ":stand_animation", "anim_stand_lady"),
      (else_try),
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (assign, ":stand_animation", "anim_stand_lord"),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, soldiers_end),
        (assign, ":stand_animation", "anim_stand_townguard"),
      (try_end),
      (try_begin),
        (ge, ":stand_animation", 0),
        (agent_set_stand_animation, ":agent_no", ":stand_animation"),
        (agent_set_animation, ":agent_no", ":stand_animation"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
      ]),

  # script_init_town_walker_agents
  # Input: none
  # Output: none
  ("init_town_walker_agents",
    [(assign, ":num_walkers", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (val_add, ":num_walkers", 1),
       (agent_get_position, pos1, ":cur_agent"),
       (try_for_range, ":i_e_p", 9, 40),#Entry points
         (entry_point_get_position, pos2, ":i_e_p"),
         (get_distance_between_positions, ":distance", pos1, pos2),
         (lt, ":distance", 200),
         (agent_set_slot, ":cur_agent", 0, ":i_e_p"),
       (try_end),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),

  # script_agent_get_town_walker_details
  # This script assumes this is one of town walkers.
  # Input: agent_id
  # Output: reg0: town_walker_type, reg1: town_walker_dna
  ("agent_get_town_walker_details",
    [(store_script_param, ":agent_no", 1),
     (agent_get_entry_no, ":entry_no", ":agent_no"),
     (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

     (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
     (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
     (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
     (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
     (assign, reg0, ":walker_type"),
     (assign, reg1, ":walker_dna"),
     (assign, reg2, ":walker_no"),
  ]),


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


	]),







  # script_tick_town_walkers
  # Input: none
  # Output: none
  ("tick_town_walkers",
    [(try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_get_position, pos2, ":cur_agent"),
       (get_distance_between_positions, ":distance", pos1, pos2),
       (lt, ":distance", 400),
       (assign, ":random_no", 0),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (store_random_in_range, ":random_no", 0, 100),
       (try_end),
       (lt, ":random_no", 20),
       (call_script, "script_set_town_walker_destination", ":cur_agent"),
     (try_end),
  ]),


  # script_set_town_walker_destination
  # Input: arg1 = agent_no
  # Output: none
  ("set_town_walker_destination",
    [(store_script_param_1, ":agent_no"),
     (assign, reg0, 9),
     (assign, reg1, 10),
     (assign, reg2, 12),
     (assign, reg3, 32),
     (assign, reg4, 33),
     (assign, reg5, 34),
     (assign, reg6, 35),
     (assign, reg7, 36),
     (assign, reg8, 37),
     (assign, reg9, 38),
     (assign, reg10, 39),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_troop", ":cur_agent"),
       (is_between, ":cur_troop", walkers_begin, walkers_end),
       (agent_get_slot, ":target_entry_point", ":cur_agent", 0),
       (try_begin),
         (eq, ":target_entry_point", 9),
         (assign, reg0, 0),
       (else_try),
         (eq, ":target_entry_point", 10),
         (assign, reg1, 0),
       (else_try),
         (eq, ":target_entry_point", 12),
         (assign, reg2, 0),
       (else_try),
         (eq, ":target_entry_point", 32),
         (assign, reg3, 0),
       (else_try),
         (eq, ":target_entry_point", 33),
         (assign, reg4, 0),
       (else_try),
         (eq, ":target_entry_point", 34),
         (assign, reg5, 0),
       (else_try),
         (eq, ":target_entry_point", 35),
         (assign, reg6, 0),
       (else_try),
         (eq, ":target_entry_point", 36),
         (assign, reg7, 0),
       (else_try),
         (eq, ":target_entry_point", 37),
         (assign, reg8, 0),
       (else_try),
         (eq, ":target_entry_point", 38),
         (assign, reg9, 0),
       (else_try),
         (eq, ":target_entry_point", 39),
         (assign, reg10, 0),
       (try_end),
     (try_end),
     (assign, ":try_limit", 100),
     (assign, ":target_entry_point", 0),
     (try_for_range, ":unused", 0, ":try_limit"),
       (shuffle_range, 0, 11),
       (gt, reg0, 0),
       (assign, ":target_entry_point", reg0),
       (assign, ":try_limit", 0),
     (try_end),
     (try_begin),
       (gt, ":target_entry_point", 0),
       (agent_set_slot, ":agent_no", 0, ":target_entry_point"),
       (entry_point_get_position, pos1, ":target_entry_point"),
       (try_begin),
         (lt, ":target_entry_point", 32),
         (init_position, pos2),
         (position_set_y, pos2, 250),
         (position_transform_position_to_parent, pos1, pos1, pos2),
       (try_end),
       (agent_set_scripted_destination, ":agent_no", pos1, 0),
       (agent_set_speed_limit, ":agent_no", 5),
     (try_end),
  ]),

  # script_town_init_doors
  # Input: door_state (-1 = closed, 1 = open, 0 = use $town_nighttime)
  # Output: none (required for siege mission templates)
  ("town_init_doors",
   [(store_script_param, ":door_state", 1),
    (try_begin),
      (assign, ":continue", 0),
      (try_begin),
        (eq, ":door_state", 1),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":door_state", 0),
        (eq, "$town_nighttime", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),# open doors
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_left", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, -80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 100),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
      (assign, ":end_cond", 1),
      (try_for_range, ":i_instance", 0, ":end_cond"),
        (scene_prop_get_instance, ":object", "spr_towngate_rectangle_door_right", ":i_instance"),
        (ge, ":object", 0),
        (val_add, ":end_cond", 1),
        (prop_instance_get_position, pos1, ":object"),
        (position_rotate_z, pos1, 80),
        (prop_instance_animate_to_position, ":object", pos1, 1),
      (try_end),
    (try_end),
  ]),

  # script_siege_init_ai_and_belfry
  # Input: none
  # Output: none
  ("set_town_picture",
   [
        (try_begin),
          (party_get_current_terrain, ":cur_terrain", "$current_town"),
          (party_slot_eq,"$current_town",slot_party_type, spt_town),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_towndes"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_townsnow"),
          (else_try),
            (set_background_mesh, "mesh_pic_town1"),
          (try_end),
        (else_try),
          (party_slot_eq,"$current_town",slot_party_type, spt_castle),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_castledes"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_castlesnow"),
          (else_try),
            (set_background_mesh, "mesh_pic_castle1"),
          (try_end),
        (else_try), #SB : enable for villages
          (party_slot_eq,"$current_town",slot_party_type, spt_village),
          (try_begin),
            (this_or_next|eq, ":cur_terrain", rt_steppe),
            (this_or_next|eq, ":cur_terrain", rt_steppe_forest),
            (this_or_next|eq, ":cur_terrain", rt_desert),
            (             eq, ":cur_terrain", rt_desert_forest),
            (set_background_mesh, "mesh_pic_village_s"),
          (else_try),
            (this_or_next|eq, ":cur_terrain", rt_snow),
            (             eq, ":cur_terrain", rt_snow_forest),
            (set_background_mesh, "mesh_pic_village_w"),
          (else_try),
            (set_background_mesh, "mesh_pic_village_p"),
          (try_end),
        (try_end),
    ]),


  # script_consume_food
  # Input: arg1 = troop_no, arg2 = center_no
  # Output: reg0 = score
  ("calculate_troop_score_for_center",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":center_no", 2),
    (assign, ":num_center_points", 1),
    (try_for_range, ":cur_center", centers_begin, centers_end),
      (assign, ":center_owned", 0),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (party_slot_eq, ":cur_center", slot_town_lord, stl_reserved_for_player),
        (assign, ":center_owned", 1),
      (try_end),
      (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
      (eq, ":center_owned", 1),
      (try_begin),
        (party_slot_eq, ":cur_center", slot_party_type, spt_town),
        (val_add, ":num_center_points", 4),
      (else_try),
        (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
        (val_add, ":num_center_points", 2),
      (else_try),
        (val_add, ":num_center_points", 1),
      (try_end),
    (try_end),
    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
    (store_add, ":score", 500, ":troop_renown"),
    (val_div, ":score", ":num_center_points"),
    (store_random_in_range, ":random", 50, 100),
    (val_mul, ":score", ":random"),
    (try_begin),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_no"),
      (val_mul, ":score", 3),
      (val_div, ":score", 2),
  	##diplomacy start+
	#Take into account original/most-recent lord and home slots.
	#Fief allocations during rebellions are an example of when this would apply.
	(else_try),
	#Bonus for original owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for previous owner
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
		(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	(else_try),
	#Bonus for lord claiming the center as home
 		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
		(val_mul, ":score", 3),
		(val_div, ":score", 2),
	##diplomacy end+
    (try_end),
    (try_begin),
      (eq, ":troop_no", "trp_player"),
       ##diplomacy start+ xxx Replaced next line (slot 0 is not the faction leader slot):
      #(faction_get_slot, ":faction_leader", "$players_kingdom"),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
      ##diplomacy end+
      (call_script, "script_troop_get_player_relation", ":faction_leader"),
      (assign, ":leader_relation", reg0),
      #(troop_get_slot, ":leader_relation", ":faction_leader", slot_troop_player_relation),
      (val_mul, ":leader_relation", 2),
      (val_add, ":score", ":leader_relation"),
    (try_end),
    (assign, reg0, ":score"),
    ]),


  # script_assign_lords_to_empty_centers
  # Input: none
  # Output: none
  #Now ONLY called from the start
  ("assign_lords_to_empty_centers",
   [

    (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_assigning_lords_to_empty_centers"),
		(str_store_string, s65, "str_assign_lords_to_empty_centers_just_happened"),
		(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
    (try_end),

	(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_set_slot, ":faction", slot_faction_temp_slot, 0),
    (try_end),

	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
    (try_end),

    #Factions will keep one unassigned center in reserve, unless they have landless lords
    (try_for_range, ":cur_center", centers_begin, centers_end),
	    (party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
		(try_begin),
			(this_or_next|eq, ":center_lord", stl_unassigned),
				(eq, ":center_lord", stl_rejected_by_player),
			(store_faction_of_party, ":center_faction", ":cur_center"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_unassigned"),
			(try_end),

			(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":center_faction", slot_faction_temp_slot),
			(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
			(faction_set_slot,  ":center_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
		(else_try),
			(eq, ":center_lord", stl_reserved_for_player),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_party_name, s4, ":cur_center"),
				(str_store_faction_name, s5, ":center_faction"),
				(display_message, "str_s4_of_the_s5_is_reserved_for_player"),
			(try_end),

		(else_try),
			(ge, ":center_lord", 0),
			(troop_set_slot, ":center_lord", slot_troop_temp_slot, 1),
		(try_end),
	(try_end),

	(try_for_range, ":active_npc", 0, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|gt, ":active_npc", "trp_player"),
			(eq, "$player_has_homage", 1),

		(troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
		(store_faction_of_troop, ":npc_faction", ":active_npc"),

		(is_between, ":npc_faction", npc_kingdoms_begin, npc_kingdoms_end),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":active_npc"),
			(str_store_faction_name, s5, ":npc_faction"),
			(display_message, "str_s4_of_the_s5_has_no_fiefs"),
		(try_end),

		(faction_get_slot, ":number_of_unassigned_centers_plus_landless_lords", ":npc_faction", slot_faction_temp_slot),
		(val_add, ":number_of_unassigned_centers_plus_landless_lords", 1),
		(faction_set_slot,  ":npc_faction", slot_faction_temp_slot, ":number_of_unassigned_centers_plus_landless_lords"),
	(try_end),

   	(try_begin),
	  (eq, "$cheat_mode", 1),
 	  (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, reg4, ":faction", slot_faction_temp_slot),
		(str_store_faction_name, s4, ":faction"),
		(display_message, "str_s4_unassigned_centers_plus_landless_lords_=_reg4"),
	  (try_end),
    (try_end),

	(try_for_range, ":cur_center", centers_begin, centers_end),
		(party_get_slot, ":center_lord", ":cur_center", slot_town_lord),
        (this_or_next|eq, ":center_lord", stl_unassigned),
			(eq, ":center_lord", stl_rejected_by_player),

        (store_faction_of_party, ":center_faction", ":cur_center"),
        (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),

        (try_begin),
	      (eq, "$cheat_mode", 1),
		  (str_store_party_name, s5, ":cur_center"),
	      (try_begin),
			(neg|faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),
			(str_store_faction_name, s4, ":center_faction"),
			(display_message, "str_s4_holds_s5_in_reserve"),
		  (try_end),
        (try_end),

		(faction_slot_ge, ":center_faction", slot_faction_temp_slot, 2),

		#(display_message, "@Considering grant of {s5}"),

		(assign, ":best_lord", -1),
		(assign, ":best_lord_score", -1),
		(try_begin),
			(eq, ":center_lord", stl_unassigned),
			(try_begin),
				(eq, "$players_kingdom", ":center_faction"),
				(eq, "$player_has_homage", 1),
				(assign, ":best_lord", stl_reserved_for_player),
				(call_script, "script_calculate_troop_score_for_center", "trp_player", ":cur_center"),
				(assign, ":best_lord_score", reg0),
			(try_end),
		(try_end),

		(try_for_range, ":cur_troop", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":troop_faction", ":cur_troop"),
			(eq, ":troop_faction", ":center_faction"),

			(call_script, "script_calculate_troop_score_for_center", ":cur_troop", ":cur_center"),
			(assign, ":score", reg0),

			#This prioritizes granting of centers for troops which do not already have one
			(try_begin),
				(troop_slot_eq, ":cur_troop", slot_troop_temp_slot, 0),
				(is_between, ":cur_center", villages_begin, villages_end),
				(val_mul, ":score", 10),
			(try_end),

			(gt, ":score", ":best_lord_score"),
			(assign, ":best_lord_score", ":score"),
			(assign, ":best_lord", ":cur_troop"),
		(try_end),

	    #Adjust count of centers and lords
 		(try_begin),
			(this_or_next|ge, ":best_lord", 0),
				(eq, ":best_lord", stl_reserved_for_player),

			(faction_get_slot, ":landless_lords_plus_unassigned_centers", ":center_faction", slot_faction_temp_slot),
			(val_sub, ":landless_lords_plus_unassigned_centers", 1),

			(try_begin),
				(eq, ":best_lord", stl_reserved_for_player),
				(troop_slot_eq, "trp_player", slot_troop_temp_slot, 0),
				(troop_set_slot, "trp_player", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1),
			(else_try),
				(troop_slot_eq, ":best_lord", slot_troop_temp_slot, 0),
				(troop_set_slot, ":best_lord", slot_troop_temp_slot, 1),
				(val_sub, ":landless_lords_plus_unassigned_centers", 1),
			(try_end),

			(faction_set_slot, ":center_faction", slot_faction_temp_slot, ":landless_lords_plus_unassigned_centers"),
		(try_end),

	    #Give the center to the lord
		(try_begin),
			(ge, ":best_lord", 0),
			(call_script, "script_give_center_to_lord", ":cur_center", ":best_lord", 1),
		(else_try),
			(eq, ":best_lord", stl_reserved_for_player),
			(party_set_slot, ":cur_center", slot_town_lord, stl_reserved_for_player),
			(try_begin), #grant bound villages to player, if granting a castle
				(party_slot_eq, ":cur_center", slot_party_type, spt_castle),
#				(assign, ":give_at_least_one_village", 0),
				(try_for_range, ":cur_village", villages_begin, villages_end),
#					(eq, ":give_at_least_one_village", 0),
					(party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
					(party_slot_eq, ":cur_village", slot_town_lord, stl_unassigned),
					(party_set_slot, ":cur_village", slot_town_lord, stl_reserved_for_player),
#					(assign, ":give_at_least_one_village", 1),
				(try_end),
			(try_end),
		(try_end),
    (try_end),
    ]),


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

    ]),

  #script_do_party_center_trade
  # INPUT: arg1 = party_no, arg2 = center_no, arg3 = percentage_change_in_center
  # OUTPUT: reg0 = total_change
  ("do_party_center_trade",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":center_no", 2),
      (store_script_param, ":percentage_change", 3), #this should probably always be a constant. Currently it is 25
	  (assign, ":percentage_change", 30),
	  ##diplomacy start+
	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  #If optional economic changes are enabled, reduce the percentage change in order
	  #to make prices feel less static.
	  (try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#Only apply lessened price movements to towns.
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		#This halves the average impact as well as making it more variable.
		(val_add, ":percentage_change", 1),
		(store_random_in_range, ":percentage_change", 0, ":percentage_change"),
		#Display economics diagnostic
		(ge, "$cheat_mode", 3),
		(str_store_party_name, s3, ":origin"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg4, ":percentage_change"),
		(display_message, "@{!}DEBUG -- Trade from {s3} to {s4}: rolled random impact of {reg4}"),
	  (try_end),
	  ##diplomacy end+

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),
	  (party_set_slot, ":party_no", slot_party_last_traded_center, ":center_no"),
	  ##diplomacy start+
	  #Update the record of trade route arrival times
      (try_begin),
         (ge, ":origin", centers_begin),
    	 ##zerilius changes begin
    	 # (this_or_next|party_slot_eq, ":origin", villages_begin, villages_end),
    	 (this_or_next|party_slot_eq, ":origin", slot_party_type, spt_village),
    	 ##zerilius changes end
         (is_between, ":origin", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":origin", dplmc_slot_village_trade_last_arrived_to_market, ":cur_hours"),
      (try_end),
      (try_begin),
	     (ge, ":origin", centers_begin),
		 (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", towns_begin, towns_end),
		 (store_current_hours, ":cur_hours"),
		 (try_for_range, ":trade_route_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
            (party_slot_eq,  ":center_no", ":trade_route_slot", ":origin"),
			(store_sub, ":trade_route_arrival_slot", ":trade_route_slot", slot_town_trade_routes_begin),
			(val_add, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin),
			(is_between, ":trade_route_arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),#this will always be true unless a modder increased the number of trade route slots without increasing the number of last arrival slots
			(party_set_slot, ":center_no", ":trade_route_arrival_slot", ":cur_hours"),
         (try_end),
         (else_try),
            (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
               (is_between, ":center_no", villages_begin, villages_end),
         (store_current_hours, ":cur_hours"),
         (party_set_slot, ":center_no", dplmc_slot_village_trade_last_returned_from_market, ":cur_hours"),
	  (try_end),
      #SB : drop off prisoners
      (try_begin),
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":town_faction", ":center_no"),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":town_faction", ":party_faction"),
        (call_script, "script_party_prisoners_add_party_prisoners", ":center_no", ":party_no"),
        (call_script, "script_party_remove_all_prisoners", ":party_no"),
      (else_try), #sell off looted items
        (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
        (is_between, ":center_no", towns_begin, towns_end),
        (party_get_slot, ":num_items", ":party_no", slot_party_next_looted_item_slot),
        (is_between, ":num_items", 1, num_party_loot_slots + 1), #has any loot
         # (this_or_next|eq, ":num_items", 0),
        (party_get_slot, ":town_merchant", ":center_no", slot_town_merchant),
        (party_get_slot, ":town_weapon", ":center_no", slot_town_weaponsmith),
        (party_get_slot, ":town_armor", ":center_no", slot_town_armorer),
        (party_get_slot, ":town_horse", ":center_no", slot_town_horse_merchant),

        #apply penalty with 0 trade skill for farmer, 2 for caravan masters
        (assign, ":seller_troop", -1), #0 skill
        (try_begin),
          (party_get_slot, ":spt", ":party_no", slot_party_type),
          # (eq, ":spt", spt_village_farmer),
          # (assign, ":seller_troop", -1), #0 skill
        # (else_try),
          (eq, ":spt", spt_kingdom_caravan),
          (assign, ":seller_troop", "trp_caravan_master"), #knows_common, 2 skill
        (else_try),
          (eq, ":spt", spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":seller_troop", ":party_no", 0),
        (try_end),
        (val_add, ":num_items", slot_party_looted_item_1),
        (try_for_range, ":slot_no", slot_party_looted_item_1, ":num_items"),
          (party_get_slot, ":item_no", ":party_no", ":slot_no"),
          (gt, ":item_no", 0),
          (item_get_type, ":itp", ":item_no"),
          (store_add, ":imod_slot", ":slot_no", num_party_loot_slots),
          (party_get_slot, ":imod_no", ":party_no", ":imod_slot"),
          (item_get_type, ":itp", ":item_no"),
          (try_begin),
            (this_or_next|is_between, ":itp", itp_type_one_handed_wpn, itp_type_goods),
            (is_between, ":itp", itp_type_pistol, itp_type_animal),
            (assign, ":merchant", ":town_weapon"),
          (else_try),
            (is_between, ":itp", itp_type_head_armor, itp_type_pistol),
            (assign, ":merchant", ":town_armor"),
          (else_try),
            (eq, ":itp", itp_type_horse),
            (assign, ":merchant", ":town_horse"),
          (else_try),
            (assign, ":merchant", ":town_merchant"),
          (try_end),
          (gt, ":merchant", 0),
          (store_troop_gold, ":merchant_gold", ":merchant"),
          (call_script, "script_dplmc_get_item_value_with_imod", ":item_no", ":imod_no"),
          (store_div, ":price", reg0, 4), #or some other factor

          (call_script, "script_dplmc_get_trade_penalty", ":item_no", ":center_no", ":seller_troop", ":merchant"),
          (val_mul, ":price", reg0),
          (val_div, ":price", 100),
          (val_max, ":price", 1),
          (gt, ":merchant_gold", ":price"), #can afford
          (troop_remove_gold, ":merchant", ":price"),
          (troop_add_item, ":merchant", ":item_no", ":imod_no"),
          # (party_set_slot, ":party_no", ":slot_no", -1), #clear off later
          # (party_set_slot, ":party_no", ":imod_slot", -1),
        (try_end),

        #any unsold item at this point are cleared
        (try_for_range, ":slot_no", slot_party_next_looted_item_slot, slot_party_looted_item_1_modifier + num_party_loot_slots),
          (party_set_slot, ":party_no", ":slot_no", 0),
        (try_end),

      (try_end),
	  ##diplomacy end+

      (assign, ":total_change", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_add, ":cur_good_price_slot", ":cur_good", ":item_to_price_slot"),
        (party_get_slot, ":cur_merchant_price", ":party_no", ":cur_good_price_slot"),
        (party_get_slot, ":cur_center_price", ":center_no", ":cur_good_price_slot"),
        (store_sub, ":price_dif", ":cur_merchant_price", ":cur_center_price"),
        (assign, ":cur_change", ":price_dif"),
        (val_abs, ":cur_change"),
        (val_add, ":total_change", ":cur_change"),
        (val_mul, ":cur_change", ":percentage_change"),
        (val_div, ":cur_change", 100),

		#This is to reconvert from absolute value
        (try_begin),
          (lt, ":price_dif", 0),
          (val_mul, ":cur_change", -1),
        (try_end),

		(assign, ":initial_price", ":cur_center_price"),

		#The new price for the caravan or peasant is set before the change, so the prices in the trading town have full effect on the next center
        (party_set_slot, ":party_no", ":cur_good_price_slot", ":cur_center_price"),

        (val_add, ":cur_center_price", ":cur_change"),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":cur_center_price"),

		(try_begin),
			(eq, "$cheat_mode", 3),
			(str_store_party_name, s3, ":origin"),
			(str_store_party_name, s4, ":center_no"),
			(str_store_item_name, s5, ":cur_good"),
			(assign, reg4, ":initial_price"),
			(assign, reg5, ":cur_center_price"),
			(display_log_message, "@{!}DEBUG -- Trade of {s5} from {s3} to {s4} brings price from {reg4} to {reg5}"),
		(try_end),

      (try_end),
      (assign, reg0, ":total_change"),
  ]),

  #script_player_join_faction
##  # INPUT: arg1 = center_no
##  # OUTPUT: reg0 = mercenary_troop_type, reg1 = amount
##  ("get_available_mercenary_troop_and_amount_of_center",
##    [(store_script_param, ":center_no", 1),
##     (party_get_slot, ":mercenary_troop", ":center_no", slot_center_mercenary_troop_type),
##     (party_get_slot, ":mercenary_amount", ":center_no", slot_center_mercenary_troop_amount),
##     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
##     (val_min, ":mercenary_amount", ":free_capacity"),
##     (store_troop_gold, ":cur_gold", "trp_player"),
##     (call_script, "script_game_get_join_cost", ":mercenary_troop"),
##     (assign, ":join_cost", reg0),
##     (try_begin),
##       (gt, ":join_cost", 0),
##       (val_div, ":cur_gold", ":join_cost"),
##       (val_min, ":mercenary_amount", ":cur_gold"),
##     (try_end),
##     (assign, reg0, ":mercenary_troop"),
##     (assign, reg1, ":mercenary_amount"),
##     ]),
##

  #script_update_village_market_towns
  # INPUT: none
  # OUTPUT: none
  ("update_village_market_towns",
    [(try_for_range, ":cur_village", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":cur_village"),
       (assign, ":min_dist", 999999),
       (assign, ":min_dist_town", -1),
       (try_for_range, ":cur_town", towns_begin, towns_end),
         (store_faction_of_party, ":town_faction", ":cur_town"),
         (eq, ":town_faction", ":village_faction"),
         (store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
         (lt, ":cur_dist", ":min_dist"),
         (assign, ":min_dist", ":cur_dist"),
         (assign, ":min_dist_town", ":cur_town"),
       (try_end),

	   (try_begin),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (else_try),
		(assign, ":min_dist", 999999),
		(assign, ":min_dist_town", -1),
		(try_for_range, ":cur_town", towns_begin, towns_end),
			(store_faction_of_party, ":town_faction", ":cur_town"),
			(store_relation, ":relation", ":town_faction", ":village_faction"),
			(ge, ":relation", 0),
			(store_distance_to_party_from_party, ":cur_dist", ":cur_village", ":cur_town"),
			(lt, ":cur_dist", ":min_dist"),
			(assign, ":min_dist", ":cur_dist"),
			(assign, ":min_dist_town", ":cur_town"),
		(try_end),
		(gt, ":min_dist_town", -1),
		(party_set_slot, ":cur_village", slot_village_market_town, ":min_dist_town"),
	   (try_end),
     (try_end),
     ]),



  #script_update_mercenary_units_of_towns
  # INPUT: none
  # OUTPUT: none
  ("update_mercenary_units_of_towns",
    [(try_for_range, ":town_no", towns_begin, towns_end),
      (store_random_in_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
      (party_set_slot, ":town_no", slot_center_mercenary_troop_type, ":troop_no"),
      (store_random_in_range, ":amount", 3, 8),
	  ##diplomacy start+
	  #OPTIONAL CHANGE: The same way that lord party sizes increase as the player
	  #progresses, also increase mercenary party sizes to maintain their relevance.
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),
		 (store_character_level, ":level", "trp_player"), #increase limits a little bit as the game progresses.
		 (store_add, ":level_factor", 80, ":level"),
         (val_mul, ":amount", ":level_factor"),
         (val_div, ":amount", 80),
	  (try_end),
	  ##diplomacy end+
      (party_set_slot, ":town_no", slot_center_mercenary_troop_amount, ":amount"),
    (try_end),
     ]),

  #script_update_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  # OUTPUT: none
  ("update_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),


##	   (try_begin),
##		(eq, "$cheat_mode", 2),
##	    (str_store_party_name, s4, ":center_no"),
##	    (str_store_faction_name, s5, ":center_culture"),
##	    (display_message, "str_updating_volunteers_for_s4_faction_is_s5"),
##	   (try_end),

       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (store_div, ":tier_upgrades", ":player_relation", 10),
       (try_for_range, ":unused", 0, ":tier_upgrades"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),

       (assign, ":upper_limit", 8),
       (try_begin),
         (ge, ":player_relation", 4),
         (assign, ":upper_limit", ":player_relation"),
         (val_div, ":upper_limit", 2),
         (val_add, ":upper_limit", 6),
       (else_try),
         (lt, ":player_relation", 0),
         (assign, ":upper_limit", 0),
       (try_end),


##diplomacy begin
      (assign, ":percent", 100),
      (try_begin), #-30% if not owner
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_sub, ":percent", 30),
      (try_end),
      (try_begin), #1%/4 renown
        (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
        (val_div, ":player_renown", 4),
        (val_add, ":percent", ":player_renown"),
      (try_end),
      (try_begin), #1%/3 honour
        (assign, ":player_honour", "$player_honor"),
        (val_div, ":player_honour", 3),
        (val_add, ":percent", ":player_honour"),
      (try_end),
      (try_begin), #+5% if king
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (val_add, ":percent", 5),

        (try_begin), #-5% for each point of serfdom
          (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
          (val_mul, ":serfdom", 5),
          (val_sub, ":percent", ":serfdom"),
        (try_end),

        (try_begin),  #+5% if king of village
          (store_faction_of_party, ":faction", ":center_no"),
          (eq, ":faction", "fac_player_supporters_faction"),
          (val_add, ":percent", 5),
        (try_end),
      (try_end),

      (try_begin),
        (gt, ":upper_limit", 0),
        (val_clamp, ":percent", 0, 201),
        (val_mul, ":upper_limit", ":percent"),
        (val_div, ":upper_limit", 100),
      (try_end),

##diplomacy end


       (val_mul, ":upper_limit", 3),
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),

       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":amount"),
     ]),

  #script_update_npc_volunteer_troops_in_village
  # INPUT: arg1 = center_no
  # OUTPUT: none
  ("update_npc_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),
       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (try_for_range, ":unused", 0, 5),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),

       (assign, ":upper_limit", 12),

       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),

       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":amount"),
     ]),

  #script_update_companion_candidates_in_taverns
  # INPUT: none
  # OUTPUT: none
("update_companion_candidates_in_taverns",
    [
      (try_begin),
        (eq, "$cheat_mode", 1),
        (display_message, "str_shuffling_companion_locations"),
      (try_end),

      (try_for_range, ":troop_no", companions_begin, companions_end),
	    ##diplomacy start+ Move this *after* the checks!
        #  (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_days_on_mission, 0),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),

        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		##diplomacy start+
		(troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
		(try_begin),
			(is_between, ":town_no", towns_begin, towns_end),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			##zerilius changes begin
			##bug fix for red text
			(ge, ":town_lord", 0),
			##zerilius changes end
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		(else_try),
			#Moved from above:
			(troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
		(try_end),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
		##diplomacy end+
        (store_random_in_range, ":town_no", towns_begin, towns_end),
        (try_begin),
		  ##diplomacy start+ Remove the "you can't go home again" condition if the player owns the town
		  (assign, ":veto", 0),
		  (try_begin),
			(store_faction_of_party, ":town_faction", ":town_no"),
			(eq, ":town_faction", "fac_player_supporters_faction"),
		  (else_try),
			(party_get_slot, ":town_lord", ":town_no", slot_town_lord),
			(ge, ":town_lord", 0),
			(this_or_next|eq, ":town_lord", "trp_player"),
			(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
				(troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
		  (else_try),
			#Native veto:
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_home, ":town_no"),
				(troop_slot_eq, ":troop_no", slot_troop_first_encountered, ":town_no"),
			(assign, ":veto", 1),
		  (try_end),
		  (eq, ":veto", 0),
                  ##diplomacy end+
          (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_troop_name, 4, ":troop_no"),
            (str_store_party_name, 5, ":town_no"),
            (display_message, "@{!}{s4} is in {s5}"),
          (try_end),
        (try_end),
      (try_end),
     ]),

  #script_update_ransom_brokers
  # INPUT: none
  # OUTPUT: none
  ("update_tavern_travellers",
    [
    (try_for_range, ":town_no", towns_begin, towns_end),
      (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1), #keep in center
      (party_set_slot, ":town_no", slot_center_tavern_traveler, 0),
    (try_end),

    (try_for_range, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
      (store_random_in_range, ":town_no", towns_begin, towns_end),
      (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
      (assign, ":end_cond", 15), #default tries to set info faction slot
      (try_begin), #not landed, skip condition
        (le, ":cur_center", 0),
        (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
      (else_try),
        (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
        (neg|party_slot_ge, ":cur_center", slot_center_is_besieged_by, 1), #can't travel
        (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (neq, ":cur_faction", "$players_kingdom"),
        (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":cur_faction"),
        (assign, ":end_cond", 0), #we set this above
      (try_end),

      #info faction
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":info_faction", npc_kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":info_faction", slot_faction_state, sfs_active),
        (neq, ":info_faction", "$players_kingdom"),
        # (neq, ":info_faction", "fac_player_supporters_faction"),
        (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":info_faction"),
        (assign, ":end_cond", 0),
      (try_end),
    (try_end),

     #SB : let its own script update every 24 hours
	 # (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "p_town_1"),
     ]),

  #script_update_villages_infested_by_bandits
  # INPUT: none
  # OUTPUT: none
  ("update_villages_infested_by_bandits",
    [
    #SB : duration tweaks, remember that this is in a 72 hour slot
     (options_get_campaign_ai, ":reduce"),
     (val_add, ":reduce", 2), #default is 3
     (try_for_range, ":village_no", villages_begin, villages_end),
       (try_begin),
         (check_quest_active, "qst_eliminate_bandits_infesting_village"),
         (quest_slot_eq, "qst_eliminate_bandits_infesting_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_eliminate_bandits_infesting_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", ":reduce"),
           (quest_set_slot, "qst_eliminate_bandits_infesting_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_eliminate_bandits_infesting_village", 2),
         (try_end),
       (else_try),
         (check_quest_active, "qst_deal_with_bandits_at_lords_village"),
         (neg|check_quest_succeeded, "qst_deal_with_bandits_at_lords_village"), #prevent failing after succeeding
         (quest_slot_eq, "qst_deal_with_bandits_at_lords_village", slot_quest_target_center, ":village_no"),
         (quest_get_slot, ":cur_state", "qst_deal_with_bandits_at_lords_village", slot_quest_current_state),
         (val_add, ":cur_state", 1),
         (try_begin),
           (lt, ":cur_state", ":reduce"),
           (quest_set_slot, "qst_deal_with_bandits_at_lords_village", slot_quest_current_state, ":cur_state"),
         (else_try),
           (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
           (call_script, "script_abort_quest", "qst_deal_with_bandits_at_lords_village", 2),
         (try_end),
       (else_try),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, 0),
         #SB : prosperity linked infestation
         (try_begin),
           (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
           (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
           (val_div, ":prosperity", 2), #0 to 50
           (val_add, ":prosperity", 75), #75 to 125
           (store_random_in_range, ":random_no", 0, ":prosperity"),
         (else_try),
           (store_random_in_range, ":random_no", 0, 100),
         (try_end),
         # (assign, ":continue", 1),
         (try_begin),
           (check_quest_active, "qst_collect_taxes"),
           (quest_slot_eq, "qst_collect_taxes", slot_quest_target_center, ":village_no"),
           (assign, ":random_no", 100),
         (else_try),
           (check_quest_active, "qst_train_peasants_against_bandits"),
           (quest_slot_eq, "qst_train_peasants_against_bandits", slot_quest_target_center, ":village_no"),
           (assign, ":random_no", 100),
         (try_end),
         # (eq, ":continue", 1),
         ## SB : update bandit creation parameters
         (lt, ":random_no", 3),
         (call_script, "script_center_get_bandits", ":village_no", 0),
         (assign, ":bandit_troop", reg0),
         (party_set_slot, ":village_no", slot_village_infested_by_bandits, ":bandit_troop"),
         #Reduce prosperity of the village by 3: reduce to -1
         (call_script, "script_change_center_prosperity", ":village_no", -1),
         (val_add, "$newglob_total_prosperity_from_bandits", -1),
         (try_begin),
           (eq, "$cheat_mode", 2),
           (str_store_party_name, s1, ":village_no"),
           (display_message, "@{!}DEBUG --{s1} is infested by bandits."),
         (try_end),
       (try_end),
     (try_end),
     ]),

  #script_update_booksellers
  # INPUT: none
  # OUTPUT: none
  ("update_tavern_minstrels",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, 0),
     (try_end),

     #SB : remove restriction on travel, add preference for feasts
     (try_for_range, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (store_faction_of_party, ":faction_no", ":town_no"),
       #feasts can be in castles, we haven't added code to put minstrels in
       (try_begin),
         (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
         (faction_get_slot, ":center_no", ":faction_no", slot_faction_ai_object),
         (is_between, ":center_no", towns_begin, towns_end),
         (neg|party_slot_ge, ":center_no", slot_center_tavern_minstrel, tavern_minstrels_begin),
         (assign, ":town_no", ":center_no"),
       (try_end),
       (party_set_slot, ":town_no", slot_center_tavern_minstrel, ":troop_no"),
       (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
       (try_begin),
        (eq, "$cheat_mode", 1),
        (str_store_troop_name, s4, ":troop_no"),
        (str_store_party_name, s5, ":town_no"),

        (display_message, "str_s4_is_at_s5"),
       (try_end),
     (try_end),


     ]),

  ("update_other_taverngoers",
  [
	(store_random_in_range, ":fight_promoter_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_fight_promoter", slot_troop_cur_center, ":fight_promoter_tavern"),

	(store_random_in_range, ":belligerent_drunk_tavern", towns_begin, towns_end),
	(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, ":belligerent_drunk_tavern"),
	]),


  #script_update_faction_notes
  # INPUT: center_no
  # OUTPUT: none
  ("update_center_notes",
    [
##      (store_script_param, ":center_no", 1),
##
##     (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
##     (try_begin),
##       (ge, ":lord_troop", 0),
##       (store_troop_faction, ":lord_faction", ":lord_troop"),
##       (str_store_troop_name_link, s1, ":lord_troop"),
##       (try_begin),
##         (eq, ":lord_troop", "trp_player"),
##         (gt, "$players_kingdom", 0),
##         (str_store_faction_name_link, s2, "$players_kingdom"),
##       (else_try),
##         (str_store_faction_name_link, s2, ":lord_faction"),
##       (try_end),
##       (str_store_party_name, s50, ":center_no"),
##       (try_begin),
##         (party_slot_eq, ":center_no", slot_party_type, spt_town),
##         (str_store_string, s51, "@The town of {s50}"),
##       (else_try),
##         (party_slot_eq, ":center_no", slot_party_type, spt_village),
##         (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
##         (str_store_party_name_link, s52, ":bound_center"),
##         (str_store_string, s51, "@The village of {s50} near {s52}"),
##       (else_try),
##         (str_store_string, s51, "@{!}{s50}"),
##       (try_end),
##       (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
##     (else_try),
##       (str_clear, s2),
##     (try_end),
##     (try_begin),
##       (is_between, ":center_no", villages_begin, villages_end),
##     (else_try),
##       (assign, ":num_villages", 0),
##       (try_for_range_backwards, ":village_no", villages_begin, villages_end),
##         (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
##         (try_begin),
##           (eq, ":num_villages", 0),
##           (str_store_party_name_link, s8, ":village_no"),
##         (else_try),
##           (eq, ":num_villages", 1),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_villages", 1),
##       (try_end),
##       (try_begin),
##         (eq, ":num_villages", 0),
##         (str_store_string, s2, "@{s2}It has no villages.^"),
##       (else_try),
##         (store_sub, reg0, ":num_villages", 1),
##         (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
##       (try_end),
##     (try_end),
##     (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
##     (add_party_note_from_sreg, ":center_no", 0, "@{s2}Its prosperity is: {s50}", 0),
##     (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
     ]),


  #script_update_center_recon_notes
  # INPUT: center_no
  # OUTPUT: none
  ("update_center_recon_notes",
    [(store_script_param, ":center_no", 1),
     (try_begin),
       (this_or_next|is_between, ":center_no", towns_begin, towns_end),
       (is_between, ":center_no", castles_begin, castles_end),
       (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
       (call_script, "script_center_get_food_consumption", ":center_no"),
       (assign, ":food_consumption", reg0),
       (store_div, reg6, ":center_food_store", ":food_consumption"),
       (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
       (party_get_num_companions, reg5, "p_collective_ally"),
       (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
     (try_end),
     ]),

  #script_update_all_notes
  # INPUT: center_no
  # OUTPUT: none
  ("get_prosperity_text_to_s50",
    [(store_script_param, ":center_no", 1),
     (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
     (val_div, ":prosperity", 20),
     (try_begin),
       (eq, ":prosperity", 0), #0..19
       (str_store_string, s50, "@Very Poor"),
     (else_try),
       (eq, ":prosperity", 1), #20..39
       (str_store_string, s50, "@Poor"),
     (else_try),
       (eq, ":prosperity", 2), #40..59
       (str_store_string, s50, "@Average"),
     (else_try),
       (eq, ":prosperity", 3), #60..79
       (str_store_string, s50, "@Rich"),
     (else_try),
       (str_store_string, s50, "@Very Rich"), #80..99
     (try_end),
     ]),

  #script_spawn_bandits
("cf_village_recruit_volunteers_cond",
    [

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_checking_volunteer_availability_script"),
	 (try_end),

	 # (neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
	 # (neg|party_slot_eq, "$current_town", slot_village_state, svs_deserted),
     # (neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
     # (neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
     (call_script, "script_cf_village_normal_cond", "$current_town"),
     (store_faction_of_party, ":village_faction", "$current_town"),
     (party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
     (store_relation, ":village_faction_relation", ":village_faction", "fac_player_faction"),

     (ge, ":center_relation", 0),
	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_center_relation_at_least_zero"),
	 (try_end),




     (this_or_next|ge, ":center_relation", 5),
     (this_or_next|eq, ":village_faction", "$players_kingdom"),
     (this_or_next|ge, ":village_faction_relation", 0),
     (this_or_next|eq, ":village_faction", "$supported_pretender_old_faction"),
		(eq, "$players_kingdom", 0),

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_relationfaction_conditions_met"),
	 (try_end),


     (party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1), #SB : ge 1, not 0
     (party_slot_ge, "$current_town", slot_center_volunteer_troop_type, 1),

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_troops_available"),
	 (try_end),


     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (ge, ":free_capacity", 1),

	 (try_begin),
		(eq, "$cheat_mode", 1),
		(display_message, "str_party_has_capacity"),
	 (try_end),


     ]),

  #script_village_recruit_volunteers_recruit
  # INPUT: none
  # OUTPUT: none
  ("village_recruit_volunteers_recruit",
    [(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
     (party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
     (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
     (val_min, ":volunteer_amount", ":free_capacity"),
     (store_troop_gold, ":gold", "trp_player"),
     (store_div, ":gold_capacity", ":gold", 10),#10 denars per man
     (val_min, ":volunteer_amount", ":gold_capacity"),
     (party_add_members, "p_main_party", ":volunteer_troop", ":volunteer_amount"),
     (party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
     (store_mul, ":cost", ":volunteer_amount", 10),#10 denars per man
     (troop_remove_gold, "trp_player", ":cost"),
     ]),

  #script_get_troop_item_amount
  # INPUT: arg1 = center_no, arg2 = difference
  # OUTPUT: none
  ("change_center_prosperity",
    [(store_script_param, ":center_no", 1),
     (store_script_param, ":difference", 2),
     (party_get_slot, ":old_prosperity", ":center_no", slot_town_prosperity),
     (store_add, ":new_prosperity", ":old_prosperity", ":difference"),
     (val_clamp, ":new_prosperity", 0, 100),
     (store_div, ":old_state", ":old_prosperity", 20),
     (store_div, ":new_state", ":new_prosperity", 20),

     (try_begin),
       (neq, ":old_state", ":new_state"),
	   (neg|is_between, ":center_no", castles_begin, castles_end),

       (str_store_party_name_link, s2, ":center_no"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s3, s50),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
       (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
       (str_store_string, s4, s50),
       (try_begin),
         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (display_message, "@Prosperity of {s2} has changed from {s3} to {s4}."),
       (try_end),
       (call_script, "script_update_center_notes", ":center_no"),
     (else_try),
       (party_set_slot, ":center_no", slot_town_prosperity, ":new_prosperity"),
     (try_end),

	 (try_begin),
		(store_current_hours, ":hours"),
		(gt, ":hours", 1),
		(store_sub, ":actual_difference", ":new_prosperity", ":old_prosperity"),
		(try_begin),
			(lt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_losses", ":actual_difference"),
	    (else_try),
			(gt, ":actual_difference", 0),
			(val_add, "$newglob_total_prosperity_gains", ":actual_difference"),
		(try_end),
	 (try_end),

	 #This will add up all non-trade prosperity
	 (try_begin),
		(eq, "$cheat_mode", 3),
		(assign, reg4, "$newglob_total_prosperity_from_bandits"),
		(assign, reg5, "$newglob_total_prosperity_from_caravan_trade"),
	    (assign, reg7, "$newglob_total_prosperity_from_villageloot"),
	    (assign, reg8, "$newglob_total_prosperity_from_townloot"),
	    (assign, reg9, "$newglob_total_prosperity_from_village_trade"),
	    (assign, reg10, "$newglob_total_prosperity_from_convergence"),
	    (assign, reg11, "$newglob_total_prosperity_losses"),
	    (assign, reg12, "$newglob_total_prosperity_gains"),
		(display_message, "@{!}DEBUG: Total prosperity actual losses: {reg11}"),
		(display_message, "@{!}DEBUG: Total prosperity actual gains: {reg12}"),

		(display_message, "@{!}DEBUG: Prosperity changes from random bandits: {reg4}"),
		(display_message, "@{!}DEBUG: Prosperity changes from caravan trades: {reg5}"),
		(display_message, "@{!}DEBUG: Prosperity changes from farmer trades: {reg9}"),
		(display_message, "@{!}DEBUG: Prosperity changes from looted villages: {reg7}"),
		(display_message, "@{!}DEBUG: Prosperity changes from sieges: {reg8}"),
		(display_message, "@{!}DEBUG: Theoretical prosperity changes from convergence: {reg10}"),
	 (try_end),

     ]),

  #script_get_center_ideal_prosperity
  # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_center_ideal_prosperity",
    [(store_script_param, ":center_no", 1),
     (assign, ":ideal", 65),

	 (call_script, "script_center_get_goods_availability", ":center_no"),
     (store_mul, ":hardship_index", reg0, 2),
	 (val_sub, ":ideal", ":hardship_index"),

     (try_begin),
       (is_between, ":center_no", villages_begin, villages_end),
       (party_slot_eq, ":center_no", slot_center_has_fish_pond, 1),
       (val_add, ":ideal", 5),
     (try_end),

     (val_max, ":ideal", 0),

     (assign, reg0, ":ideal"),
     ]),

    # INPUT: arg1 = center_no
  # OUTPUT: reg0 = ideal_prosperity
  ("get_poorest_village_of_faction",
    [(store_script_param, ":faction_no", 1),
     (assign, ":min_prosperity_village", -1),
     (assign, ":min_prosperity", 101),
     (try_for_range, ":village_no", villages_begin, villages_end),
       (store_faction_of_party, ":village_faction", ":village_no"),
       (eq, ":village_faction", ":faction_no"),
       (party_get_slot, ":prosperity", ":village_no", slot_town_prosperity),
       (lt, ":prosperity", ":min_prosperity"),
       (assign, ":min_prosperity", ":prosperity"),
       (assign, ":min_prosperity_village", ":village_no"),
     (try_end),
     (assign, reg0, ":min_prosperity_village"),
     ]),

  #script_troop_add_gold
	#the current system still works very well, however
	("center_get_item_consumption",
    [
	]),

	("lord_get_home_center",
	[
      (store_script_param, ":troop_no", 1),
      (assign, ":result", -1),

		##diplomacy start+
		(assign, ":best_score", -1),
		(troop_get_slot, ":troop_original_faction", ":troop_no", slot_troop_original_faction),
		#The default script prefers towns to castles, but aside from that is
		#fairly arbitrary.  Add scores that take into account original faction
		#and so forth.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
		  (assign, ":center_score", 10),#10 for castles, 20 for towns
		  (try_begin),
		    (is_between, ":center_no", towns_begin, towns_end),
			(assign, ":center_score", 20),
		  (try_end),
		  (try_begin),
		    (troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
			(val_add, ":center_score", 6),
          (else_try),
			(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
			(val_add, ":center_score", 5),
		  (else_try),
		    (is_between, ":troop_original_faction", kingdoms_begin, kingdoms_end),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":troop_original_faction"),
			(val_add, ":center_score", 4),
		  (try_end),
		  (gt, ":center_score", ":best_score"),
          (assign, ":result", ":center_no"),
		  (assign, ":best_score", ":center_score"),
      (try_end),
		##diplomacy end+

      #SB : add loop breaks
      (try_begin),
        (eq, ":result", -1),
        (assign, ":limit", walled_centers_end),
        (try_for_range, ":center_no", walled_centers_begin, ":limit"),
          (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
          (assign, ":result", ":center_no"),
          (assign, ":limit", walled_centers_begin),
        (try_end),
      (try_end),

      #NOTE : In old code if a lord has no walled center then home city of this lord is assigning to
      #faction leader's home city. Now I changed this to assign home cities more logical and homogeneous.
      #In new code if a lord has no walled center then his home city becomes his village's border_city.
      #This means his home city becomes owner city of his village. If he has no village then as last change
      #his home city become faction leader's home city.
      (try_begin),
        (eq, ":result", -1),

        #SB : add loop breaks
        (assign, ":limit", villages_end),
        (try_for_range, ":center_no", villages_begin, ":limit"),
          (eq, ":result", -1),
          (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

          # (try_begin),
            # (neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
          (assign, ":result", ":bound_center"),
          (assign, ":limit", villages_begin),
          # (try_end),
        (try_end),
      (try_end),

      #If lord has no walled center and is player faction, then assign player court
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":player_court_faction", "$g_player_court"),
		(eq, ":player_court_faction", "fac_player_supporters_faction"),

        (assign, ":result", "$g_player_court"),
      (try_end),

      #If lord has no walled center and any not walled village then assign faction capital
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
        (neq, ":troop_no", ":faction_leader"),
        (ge, ":faction_leader", 0),#<- Fix for ticket 36.
        ##By the way, if this was Native, the following two lines would fix
        ##the weird bug where relatives of exiled lords start accumulating
        ##in the player's court:
        #(this_or_next|neq, ":faction_leader", ":troop_no"),
        #(eq, "$players_kingdom", ":faction_no"),
        ##This is unnecessary in Diplomacy, though, since I initialize slot_faction_leader to -1
        ##to distinguish factions led by the player from factions without actual leaders.
        (call_script, "script_lord_get_home_center", ":faction_leader"),
        (gt, reg0, -1),
        (assign, ":result", reg0),
      (try_end),

	  #Any center of the faction
      (try_begin),
        (eq, ":result", -1),
		(store_faction_of_troop, ":faction_no", ":troop_no"),

		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		    (eq, ":result", -1),

			(store_faction_of_party, ":center_faction", ":walled_center"),
			(eq, ":faction_no", ":center_faction"),
			(assign, ":result", ":walled_center"),
		(try_end),
      (try_end),



      (assign, reg0, ":result"),
	]),




	("setup_tavern_attacker",
	[
	  (store_script_param, ":cur_entry", 1),

	  (try_begin),
	    (neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_belligerent_drunk"),
	  (try_end),

	  (try_begin),
	    (troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),
	    (set_visitor, ":cur_entry", "trp_hired_assassin"),
	  (try_end),
	]),

	("activate_tavern_attackers",
	[
	  (set_party_battle_mode),
	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_fugitive"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	    (eq, ":cur_agent_troop", "trp_hired_assassin"),
	    (agent_set_team, ":cur_agent", 1),
	    (assign, "$g_main_attacker_agent", ":cur_agent"),
	    (agent_ai_set_aggressiveness, ":cur_agent", 199),
	  (try_end),
	]),

	("deactivate_tavern_attackers",
	[
	  (finish_party_battle_mode),
	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_fugitive"),
	    (this_or_next|eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	    (eq, ":cur_agent_troop", "trp_hired_assassin"),
	    (agent_set_team, ":cur_agent", 0),
	    (agent_ai_set_aggressiveness, ":cur_agent", 0),
	  (try_end),
	]),

	("activate_town_guard",
	[
	  (set_party_battle_mode),
	  #(get_player_agent_no, ":player_agent"),
	  #(agent_get_team, ":player_team", ":player_agent"),

	  (try_for_agents, ":cur_agent"),
	    (agent_get_troop_id, ":troop_type", ":cur_agent"),
	    (is_between, ":troop_type", soldiers_begin, soldiers_end), #dckplmc
        (agent_set_team, ":cur_agent", 1),
        #(team_give_order, 1, grc_everyone, mordr_charge), - for some reason, this freezes everyone if the player is not yet spawned
		#(try_begin),
		#	(eq, "$g_main_attacker_agent", 0),
		#	(assign, "$g_main_attacker_agent", ":cur_agent"),
		#(try_end),
	(else_try),
		(this_or_next|is_between, ":troop_type", walkers_begin, walkers_end),
		(is_between, ":troop_type", armor_merchants_begin, mayors_end),

		(agent_clear_scripted_mode, ":cur_agent"),
		#(agent_set_team, ":cur_agent", 2), #dckplmc don't want town guards to massacre townsfolk
	(try_end),
	]),


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
	]),

	("find_center_to_attack_alt",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":attack_by_faction", 2),
      (store_script_param, ":all_vassals_included", 3),

      (assign, ":result", -1),
      (assign, ":score_to_beat", 0),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack",	":troop_no", ":center_no", ":attack_by_faction", ":all_vassals_included"),
        (assign, ":score", reg0),

        (gt, ":score", ":score_to_beat"),

        (assign, ":result", ":center_no"),
        (assign, ":score_to_beat", ":score"),
      (try_end),

      (assign, reg0, ":result"),
      (assign, reg1, ":score_to_beat"),
	]),

  ("npc_decision_checklist_evaluate_enemy_center_for_attack",
    [
      #NOTES -- LAST OFFENSIVE TIME SCORE IS NOT USED

      (store_script_param, ":troop_no", 1),
      (store_script_param, ":potential_target", 2),
      (store_script_param, ":attack_by_faction", 3),
      (store_script_param, ":all_vassals_included", 4),

      (assign, ":result", -1),
      (assign, ":explainer_string", -1),
      #(assign, ":reason_is_obvious", 0),
      (assign, ":power_ratio", 0),
      #(assign, ":hours_since_last_recce", -1),

      #(assign, ":value_of_target", 0),
      #(assign, ":difficulty_of_capture", 0),
      (store_faction_of_troop, ":faction_no", ":troop_no"),

      (try_begin),
        (eq, ":attack_by_faction", 1),
        (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
        (ge, ":faction_marshal", 0), #STEVE ADDITION TO AVOID MESSAGE SPAM
        (troop_get_slot, ":party_no", ":faction_marshal", slot_troop_leaded_party),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_end),

      (assign, "$g_use_current_ai_object_as_s8", 0),
	  ##diplomacy start+ Use this if AI changes are enabled.
	  (party_get_slot, ":hours_since_capture", ":potential_target", dplmc_slot_center_last_transfer_time),
	  (try_begin),
	     #If the slot was uninitialized, set it to negative to indicate invalid.
	     (eq, ":hours_since_capture", 0),
		 (assign, ":hours_since_capture", -1),
	  (else_try),
	     (store_current_hours, reg0),
	     (val_sub, ":hours_since_capture", reg0),
	  (try_end),
	  #How recent counts as "recent" depends on the AI settings.
	  (try_begin),
	     (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
		 (assign, ":recency_maximum", 24 * 21),#The last three weeks
	  (else_try),
		 (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_MEDIUM),
		 (assign, ":recency_maximum", 24 * 14),#The last two weeks
	  (else_try),
	     (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		 (assign, ":recency_maximum", 24 * 7),#The last week
	  (else_try),
	     (assign, ":recency_maximum", 0),
	  (try_end),
	  ##diplomacy end+

      #THE FIRST BATCH OF DISQUALIFYING CONDITIONS DO NOT REQUIRE THE ATTACKING PARTY TO HAVE CURRENT INTELLIGENCE ON THE TARGET
      (try_begin),
        (neg|party_is_active, ":party_no"),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_party_not_active"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (store_faction_of_party, ":potential_target_faction", ":potential_target"),
        (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
        (ge, ":relation", 0),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_friendly"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
        (assign, ":faction_of_besieger_party", -1),
        (try_begin),
          (neg|party_slot_eq, ":potential_target", slot_center_is_besieged_by, -1),
          (party_get_slot, ":besieger_party", ":potential_target", slot_center_is_besieged_by),
          (party_is_active, ":besieger_party"),
          (store_faction_of_party, ":faction_of_besieger_party", ":besieger_party"),
        (try_end),

        (neq, ":faction_of_besieger_party", -1),
        (neq, ":faction_of_besieger_party", ":faction_no"),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_already_besieged"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", villages_begin, villages_end),
        (assign, ":village_is_looted_or_raided_already", 0),
        (try_begin),
          (party_slot_eq, ":potential_target", slot_village_state, svs_being_raided),
          (party_get_slot, ":raider_party", ":potential_target", slot_village_raided_by),
		  (party_is_active, ":raider_party"),
          (store_faction_of_party, ":raider_faction", ":raider_party"),
          (neq, ":raider_faction", ":faction_no"),
          (assign, ":raiding_by_one_other_faction", 1),
        (else_try),
          (assign, ":raiding_by_one_other_faction", 0),
        (try_end),

        (try_begin),
          (this_or_next|party_slot_eq, ":potential_target", slot_village_state, svs_looted),
          (eq, ":raiding_by_one_other_faction", 1),
          (assign, ":village_is_looted_or_raided_already", 1),
        (try_end),

        (eq, ":village_is_looted_or_raided_already", 1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_looted_or_raided_already"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
	    ##diplomacy start+ Add support for companion / lady personality types: does not want to attack innocents
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
		(this_or_next|gt, reg0, 0),
		(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
		(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_moralist),
		#diplomacy end+
        (this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),

        (is_between, ":potential_target", villages_begin, villages_end),
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_marshal_does_not_want_to_attack_innocents"),
      (else_try),
        (assign, ":distance_from_our_closest_walled_center", 1000),
        (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
           (store_faction_of_party, ":cur_center_faction", ":cur_center"),
           (eq, ":cur_center_faction", ":faction_no"),
           (store_distance_to_party_from_party, ":distance_from_cur_center", ":cur_center", ":potential_target"),
           (lt, ":distance_from_cur_center", ":distance_from_our_closest_walled_center"),
           (assign, ":distance_from_our_closest_walled_center", ":distance_from_cur_center"),
        (try_end),

        (gt, ":distance_from_our_closest_walled_center", 75),
		##diplomacy start+ Add support for companion / lady personality types: cautious
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(gt, reg0, 0),
		##Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_far_away_our_cautious_marshal_does_not_wish_to_reconnoiter"),
      #RECONNOITERING BEGINS HERE - VALUE WILL BE TEN OR LESS
      (else_try),
        (gt, ":distance_from_our_closest_walled_center", 90),
		##diplomacy start+ Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_far_away_even_for_our_aggressive_marshal_to_reconnoiter"),
        #(assign, ":reason_is_obvious", 1),
      (else_try),
        (is_between, ":potential_target", walled_centers_begin, walled_centers_end),
		##diplomacy start+ Add support for companion / lady personality types: aggessive
		##OLD:
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        #(neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(lt, reg0, 0),
		##Do not apply the check to recently-lost centers if AI changes are on.
		(this_or_next|lt, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		(this_or_next|neg|party_slot_eq,":potential_target", slot_center_ex_faction, ":faction_no"),
		(this_or_next|lt, ":hours_since_capture", 0), #i.e. invalid
		(ge, ":hours_since_capture", ":recency_maximum"),#hasn't been taken recently
		##diplomacy end+

        (assign, ":close_center_found", 0),
        (try_for_range, ":friendly_walled_center", walled_centers_begin, walled_centers_end),
          (eq, ":close_center_found", 0),
          (store_faction_of_party, ":friendly_walled_center_faction", ":friendly_walled_center"),
          (eq, ":friendly_walled_center_faction", ":faction_no"),
          (store_distance_to_party_from_party, ":distance_from_walled_center", ":potential_target", ":friendly_walled_center"),
          (lt, ":distance_from_walled_center", 60),
          (assign, ":close_center_found", 1),
        (try_end),
        (eq, ":close_center_found", 0),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_is_indefensible"),
      #(else_try),
        #For now it is removed as Armagan's decision, we can add this option in later patchs. I and Armagan accept it has good potential. But this system needs also
        #scouting quests and scouting AI added together. If we only add this then we limit AI very much, it can attack only very few of centers, this damages
        #variability of game and surprise attacks of AI. Player can predict where AI will attack and he can full garnisons of only this center.
        #We can add asking travellers about how good defended center X by paying 100 denars for example to equalize situations of AI and human player.
        #But these needs much work and detailed AI tests so Armagan decided to skip this for now.

        #(store_sub, ":faction_recce_slot", ":faction_no", kingdoms_begin),
        #(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
        #(party_get_slot, ":last_recce_time", ":potential_target", ":faction_recce_slot"),
        #(store_current_hours, ":hours_since_last_recce"),
        #(val_sub, ":hours_since_last_recce", ":last_recce_time"),

        #(this_or_next|eq, ":last_recce_time", 0),
        #(gt, ":hours_since_last_recce", 96), #Information is presumed to be accurate for four days

        #(store_sub, ":150_minus_distance_div_by_10", 150, ":distance_from_party"),
        #(val_div, ":150_minus_distance_div_by_10", 10),

        #(assign, ":result", ":150_minus_distance_div_by_10"),
        #(assign, ":explainer_string", "str_center_has_not_been_scouted"),
      #DECISIONS BASED ON ENEMY STRENGTH BEGIN HERE
      (else_try),
        (party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),
        (party_get_slot, ":follower_strength", ":party_no", slot_party_follower_strength),
        (party_get_slot, ":strength_of_nearby_friend", ":party_no", slot_party_nearby_friend_strength),

        (store_add, ":total_strength", ":party_strength", ":follower_strength"),
        (val_add, ":total_strength", ":strength_of_nearby_friend"),

        #(party_get_slot, ":potential_target_nearby_enemy_exact_strength", ":potential_target", slot_party_nearby_friend_strength),
        #(assign, ":potential_target_nearby_enemy_strength", ":potential_target_nearby_enemy_exact_strength"),
        (try_begin),
          (is_between, ":potential_target", villages_begin, villages_end),
          (assign, ":enemy_strength", 10),
        (else_try),
          (party_get_slot, ":enemy_strength", ":potential_target", slot_party_cached_strength),
          (party_get_slot, ":enemy_strength_nearby", ":potential_target", slot_party_nearby_friend_strength),
          (val_add, ":enemy_strength", ":enemy_strength_nearby"),
        (try_end),
        (val_max, ":enemy_strength", 1),
		##diplomacy start+  Add support for lady/companion personalities: aggressive
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_martial),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(lt, reg0, 0),
		###xxx yyy zzz TODO: The logic here seems backwards!
		###Later look at this and verify that it's what we want.
		##diplomacy end+

        (store_mul, ":power_ratio", ":total_strength", 100),
        (val_div, ":power_ratio", ":enemy_strength"),
        (lt, ":power_ratio", 150),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
      (else_try),
        (ge, ":enemy_strength", ":total_strength"), #if enemy is powerful

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
      (else_try),
        (store_mul, ":power_ratio", ":total_strength", 100),
        (val_div, ":power_ratio", ":enemy_strength"),
        (lt, ":power_ratio", 185),
		##diplomacy start+ Add support for companion/lady personalities: cautious
		##OLD:
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
		##NEW:
		(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
		(gt, reg0, 0),
		##diplomacy end+

        #equations here
        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
      (else_try),
        (lt, ":power_ratio", 140), #it was 140

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
      #To Steve - I moved below two if statement here from upper places, to enable in answering different different answers even
      #if we are close to an unlooted enemy village. For example now it can say "center X" is too far too while our army is
      #looting a village because of its closeness.
      (else_try),
        #if the party has already started the siege
        (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),
        (is_between, ":current_object", villages_begin, villages_end),
        (neq, ":potential_target", ":current_object"),
        (party_slot_eq, ":current_object", slot_village_state, svs_under_siege),

        (store_current_hours, ":hours_since_siege_began"),
        (party_get_slot, ":hour_that_siege_began", ":current_object", slot_center_siege_begin_hours),
        (val_sub, ":hours_since_siege_began", ":hour_that_siege_began"),
        (gt, ":hours_since_siege_began", 4),

        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":troop_no", ":current_object", ":attack_by_faction", 0),
        (gt, reg0, -1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_we_have_already_committed_too_much_time_to_our_present_siege_to_move_elsewhere"),
      (else_try),
        #If the party is close to an unlooted village
        (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
        (faction_get_slot, ":current_object", ":faction_no", slot_faction_ai_object),
        (neq, ":potential_target", ":current_object"),
        (is_between, ":current_object", villages_begin, villages_end),
        (store_distance_to_party_from_party, ":distance_to_cur_object", ":party_no", ":current_object"),
        (lt, ":distance_to_cur_object", 10),

        (call_script, "script_npc_decision_checklist_evaluate_enemy_center_for_attack", ":troop_no", ":current_object", ":attack_by_faction", 0),
        (gt, reg0, -1),

        (assign, "$g_use_current_ai_object_as_s8", 1),

        (assign, ":result", -1),
        (assign, ":explainer_string", "str_center_we_are_already_here_we_should_at_least_loot_the_village"),
      #DECISION TO ATTACK IS HERE
      #(else_try),
        #To Steve - I removed below lines, as here decided. We will use pre-function to evaluate assailability scores for centers rather than below lines to make AI
        #selecting better targets. If you want to make some marshals to select not-best options I can add that option into script_calculate_center_assailability_score,
        #for that we can need seed values for each center and for each lord, so we can add these seed values to create variability, clever marshals have seeds with less
        #standard deviation and less values and less-clever marshals have bigger seeds. Then probability of some lords to disagree marshal increases because their seed
        #values will be different from marshal's. If Steve wants it from me to implement I can add this.

        #(try_begin),
        #  (is_between, ":potential_target", villages_begin, villages_end),
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 50), #average 100
        #(else_try),
        #  (is_between, ":potential_target", castles_begin, castles_end),
        #  (assign, ":score", ":power_ratio"), #ie, at least 140
        #(else_try),
        #  (party_get_slot, ":score", ":potential_target", slot_town_prosperity),
        #  (val_add, ":score", 75),
        #  (val_mul, ":score", ":power_ratio"),
        #  (val_div, ":score", 100), #ie, at least about 200
        #(try_end),
        #
        #(val_sub, ":score", ":distance_from_party"),
        #(lt, ":score", -1),

        #(assign, ":result", -1),
        #(assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
      (else_try),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (eq, ":faction_no", "fac_kingdom_3"),
          (store_faction_of_party, ":potential_target_faction", ":potential_target"),
          (store_relation, ":relation", ":potential_target_faction", ":faction_no"),
          (lt, ":relation", 0),
        (try_end),

        (call_script, "script_calculate_center_assailability_score", ":troop_no", ":potential_target", ":all_vassals_included"),
        (assign, ":score", reg0),
        (assign, ":power_ratio", reg1),
        #(assign, ":distance_score", reg2),

        (assign, ":result", ":score"),

        (try_begin),
          (le, ":power_ratio", 100),
          (try_begin),
			##diplomacy start+ Add support for companion / lady personalities: cautious
			##OLD:
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
            #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
            #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
			##NEW:
			(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			(gt, reg0, 0),
			##diplomacy end+
            (assign, ":explainer_string", "str_center_cautious_marshal_believes_center_too_difficult_to_capture"),
          (else_try),
            (assign, ":explainer_string", "str_center_even_aggressive_marshal_believes_center_too_difficult_to_capture"),
          (try_end),
        (else_try),
          (le, ":power_ratio", 150),

          (try_begin),
			##diplomacy start+ Add support for companion / lady personalities: cautious
			##OLD
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
	        #(this_or_next|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_goodnatured),
	        #(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_cunning),
			##NEW:
			(call_script, "script_dplmc_store_troop_personality_caution_level", ":troop_no"),
			(lt, reg0, 0),
			##diplomacy end+
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_cautious"),
	      (else_try),
	        (assign, ":explainer_string", "str_center_protected_by_enemy_army_aggressive"),
	      (try_end),
	    (else_try),
	      (try_begin),
	        (le, ":score", "$g_faction_object_score"),
	        (assign, ":explainer_string", "str_center_value_outweighed_by_difficulty_of_capture"),
	      (else_try),
	        #To Steve, does not this sentence needs to explain why we are not attacking that city?
	        #This sentence says it justifies, so why we are not attacking?
	        (assign, ":explainer_string", "str_center_value_justifies_the_difficulty_of_capture"),
	      (try_end),
	    (try_end),
	  (try_end),

	  (assign, reg0, ":result"),
	  (assign, reg1, ":explainer_string"),
	  (assign, reg2, ":power_ratio"),
     ]),

 	  # Input: arg1 = center_no, arg2 = faction
  ("give_center_to_faction_while_maintaining_lord",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":faction_no"),

      (store_faction_of_party, ":old_faction", ":center_no"),
	  ##diplomacy start+
	  #If the player, previously the head of his own faction, is now joining
	  #an NPC faction, don't reset the "last taken" time or the "ex faction"
	  #slots.
	  (try_begin),
		#Friendly transfer: don't update transfer time or ex-faction
		(eq, ":old_faction", "fac_player_supporters_faction"),
		(eq, ":faction_no", "$players_kingdom"),
	  (else_try),
		#Defection: update transfer time and ex-faction
		(party_set_slot, ":center_no", slot_center_ex_faction, ":old_faction"),
		(store_current_hours, ":cur_hours"),
		(party_set_slot, ":center_no", dplmc_slot_center_last_transfer_time, ":cur_hours"),
	  (try_end),
	  ##diplomacy end+
      (party_set_faction, ":center_no", ":faction_no"),

      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_village),
        #SB : reinforcement
        (try_begin),
          (party_get_slot, ":farmer_party", ":center_no", slot_village_farmer_party),
          (gt, ":farmer_party", 0),
          (party_is_active, ":farmer_party"),
          (party_set_faction, ":farmer_party", ":faction_no"),
        (try_end),
        (try_begin),
          (party_get_slot, ":reinf_party", ":center_no", slot_village_reinforcement_party),
          (gt, ":reinf_party", 0),
          (party_is_active, ":reinf_party"),
          (party_set_faction, ":reinf_party", ":faction_no"),
        (try_end),
      (try_end),

      (call_script, "script_update_faction_notes", ":faction_no"),
      (call_script, "script_update_center_notes", ":center_no"),

      (try_for_range, ":other_center", centers_begin, centers_end),
        (party_slot_eq, ":other_center", slot_village_bound_center, ":center_no"),
        (call_script, "script_give_center_to_faction_while_maintaining_lord", ":other_center", ":faction_no"),
      (try_end),
  ]),

  # script_check_concilio_calradi_achievement
  ("refresh_center_inventories",
  [
  (set_merchandise_modifier_quality,150),
  (reset_item_probabilities,100),

  # Add trade goods to merchant inventories
  (try_for_range,":cur_center",towns_begin,towns_end),
    (party_get_slot,":cur_merchant",":cur_center",slot_town_merchant),
    (reset_item_probabilities,100),
      (assign, ":total_production", 0),
    (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
        (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

		(val_add, ":total_production", ":cur_production"),
      (try_end),

	  (party_get_slot, ":town_prosperity", ":cur_center", slot_town_prosperity),
	  (assign, ":number_of_items_in_town", 25),

	  (try_begin), #1.0x - 2.0x (50 - 100 prosperity)
	    (ge, ":town_prosperity", 50),
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_mul, ":ratio", 2),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (else_try), #0.5x - 1.0x (0 - 50 prosperity)
		(store_sub, ":ratio", ":town_prosperity", 50),
		(val_add, ":ratio", 100),
		(val_mul, ":number_of_items_in_town", ":ratio"),
		(val_div, ":number_of_items_in_town", 100),
	  (try_end),

	  (val_clamp, ":number_of_items_in_town", 10, 40),

	  (try_begin),
	    (is_between, ":cur_center", castles_begin, castles_end),
	    (val_div, ":number_of_items_in_town", 2),
      (try_end),

      (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
	  (call_script, "script_center_get_production", ":cur_center", ":cur_goods"),
		(assign, ":cur_production", reg0),

        (try_for_range, ":cur_village", villages_begin, villages_end),
		  (party_slot_eq, ":cur_village", slot_village_bound_center, ":cur_center"),
          (call_script, "script_center_get_production", ":cur_village", ":cur_goods"),
		  (val_div, reg0, 3),
		  (val_add, ":cur_production", reg0),
		(try_end),

		(val_max, ":cur_production", 1),
		(val_mul, ":cur_production", 4),

        (val_mul, ":cur_production", ":number_of_items_in_town"),
		(val_mul, ":cur_production", 100),
		(val_div, ":cur_production", ":total_production"),
        (set_item_probability_in_merchandise, ":cur_goods", ":cur_production"),
    (try_end),

	  (troop_clear_inventory, ":cur_merchant"),
      (troop_add_merchandise, ":cur_merchant", itp_type_goods, ":number_of_items_in_town"),

      (troop_ensure_inventory_space, ":cur_merchant", 20),
    (troop_sort_inventory, ":cur_merchant"),
    (store_troop_gold, ":cur_gold",":cur_merchant"),
    ##diplomacy start+
	#Option: scaling gold additions by the prosperity of the town.
	(try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
	    (party_get_slot, ":prosperity_75", ":cur_center", slot_town_prosperity),
		(val_add, ":prosperity_75", 75),
		(store_mul, ":target_gold", ":prosperity_75", 1500),
		(val_add, ":target_gold", 62),
		(val_div, ":target_gold", 125),#average 1500
		(lt, ":cur_gold", ":target_gold"),
		(store_random_in_range,":new_gold",500,1000),
		(val_mul, ":new_gold", ":prosperity_75"),
		(val_add, ":new_gold", 62),
		(val_div, ":new_gold", 125),
		(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	(else_try),
		(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	    #fall through to default behavior
	    ##diplomacy end+
    (lt,":cur_gold",1500),
    (store_random_in_range,":new_gold",500,1000),
    (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
    ##diplomacy start+
    (try_end),
	##diplomacy end+
  (try_end),
  ]),

  # script_refresh_center_armories
  ("refresh_center_armories",
  [
	  (reset_item_probabilities,100),
	  (set_merchandise_modifier_quality,150),
	  (try_for_range, ":cur_merchant", armor_merchants_begin, armor_merchants_end),
		(store_sub, ":cur_town", ":cur_merchant", armor_merchants_begin),
		(val_add, ":cur_town", towns_begin),
		(troop_clear_inventory, ":cur_merchant"),
		(party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
		(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_body_armor, 16),
		(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_head_armor, 16),
		(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_foot_armor, 8),
		(troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_hand_armor, 4),
		(try_begin), # Add extra armors
			(gt, "$g_sexual_content", 0),
			(troop_add_merchandise_with_faction, ":cur_merchant", fac_undeads, itp_type_body_armor, 3),
			(troop_add_merchandise_with_faction, ":cur_merchant", fac_undeads, itp_type_head_armor, 1),
			(troop_add_merchandise_with_faction, ":cur_merchant", fac_undeads, itp_type_foot_armor, 2),
		(try_end),
		(troop_ensure_inventory_space, ":cur_merchant", merchant_inventory_space),
		(troop_sort_inventory, ":cur_merchant"),
		(store_troop_gold, reg6, ":cur_merchant"),

	    ##diplomacy start+
		#Option: scaling gold additions by the prosperity of the town.
		(try_begin),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
		    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
			(val_add, ":prosperity_75", 75),
			(store_mul, ":target_gold", ":prosperity_75", 900),
			(val_add, ":target_gold", 62),
			(val_div, ":target_gold", 125),#average 900
			(lt, reg(6), ":target_gold"),
			(store_random_in_range,":new_gold",200,400),
			(val_mul, ":new_gold", ":prosperity_75"),
			(val_add, ":new_gold", 62),
			(val_div, ":new_gold", 125),
			(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		    #fall through to default behavior
		    ##diplomacy end+
	    (lt,reg6,1000),
	    (store_random_in_range,":new_gold",250,500),
	    (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		##diplomacy start+
		(try_end),
		##diplomacy end+
	  (end_try),
  ]),

  # script_refresh_center_weaponsmiths
  ("refresh_center_weaponsmiths",
  [
	  (reset_item_probabilities,100),
	  (set_merchandise_modifier_quality,150),
    (try_for_range, ":cur_merchant", weapon_merchants_begin, weapon_merchants_end),
	  (store_sub, ":cur_town", ":cur_merchant", weapon_merchants_begin),
	    (val_add, ":cur_town", towns_begin),
	  (troop_clear_inventory, ":cur_merchant"),
	    (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_one_handed_wpn, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_two_handed_wpn, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_polearm, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_shield, 6),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bow, 4),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_crossbow, 3),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_thrown, 5),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_arrows, 2),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bolts, 2),
      #Guns and gun related items
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_pistol, 1),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_musket, 1),
      (troop_add_merchandise_with_faction, ":cur_merchant", ":cur_faction", itp_type_bullets, 1),
      (troop_ensure_inventory_space, ":cur_merchant", merchant_inventory_space),
      (troop_sort_inventory, ":cur_merchant"),
      (store_troop_gold, reg6, ":cur_merchant"),

	    ##diplomacy start+
		#Option: scaling gold additions by the prosperity of the town.
		(try_begin),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
		    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
			(val_add, ":prosperity_75", 75),
			(store_mul, ":target_gold", ":prosperity_75", 900),
			(val_add, ":target_gold", 62),
			(val_div, ":target_gold", 125),#average 900
			(lt, reg6, ":target_gold"),
			(store_random_in_range,":new_gold",200,400),
			(val_mul, ":new_gold", ":prosperity_75"),
			(val_add, ":new_gold", 62),
			(val_div, ":new_gold", 125),
			(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
		(else_try),
			(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		    #fall through to default behavior
		    ##diplomacy end+
	    (lt,reg6,1000),
	    (store_random_in_range,":new_gold",250,500),
	  (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	  ##diplomacy start+
	  (try_end),
	  ##diplomacy end+
	  (try_end),
  ]),

  # script_refresh_center_stables
  ("refresh_center_stables",
  [
      (reset_item_probabilities,100),
      (set_merchandise_modifier_quality,150),
      (try_for_range,":cur_merchant",horse_merchants_begin,horse_merchants_end),
	  (troop_clear_inventory, ":cur_merchant"),
      (store_sub, ":cur_town", ":cur_merchant", horse_merchants_begin),
      (val_add, ":cur_town", towns_begin),
      (party_get_slot, ":cur_faction", ":cur_town", slot_center_original_faction),
      (troop_add_merchandise_with_faction,":cur_merchant", ":cur_faction",itp_type_horse,5),
      (troop_ensure_inventory_space,":cur_merchant",65),
      (troop_sort_inventory, ":cur_merchant"),
      (store_troop_gold, ":cur_gold",":cur_merchant"),
	##diplomacy start+
	#Option: scaling gold additions by the prosperity of the town.
	(try_begin),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#this must be explicitly enabled
	    (party_get_slot, ":prosperity_75", ":cur_town", slot_town_prosperity),
		(val_add, ":prosperity_75", 75),
		(store_mul, ":target_gold", ":prosperity_75", 600),
		(val_add, ":target_gold", 62),
		(val_div, ":target_gold", 125),#average 600
		(lt, ":cur_gold", ":target_gold"),
		(store_random_in_range,":new_gold",200,400),
		(val_mul, ":new_gold", ":prosperity_75"),
		(val_add, ":new_gold", 62),
		(val_div, ":new_gold", 125),
		(call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
	(else_try),
		(lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
	    #fall through to default behavior
	    ##diplomacy end+
    (lt,":cur_gold",600),
    (store_random_in_range, ":new_gold", 250, 500),
    (call_script, "script_troop_add_gold", ":cur_merchant", ":new_gold"),
    ##diplomacy start+
    (try_end),
    ##diplomacy end+
  (try_end),
  ]),

##diplomacy begin

  ("dplmc_describe_prosperity_to_s4",
    [
      (store_script_param_1, ":center_no"),

      (str_store_party_name, s60,":center_no"),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
      (str_store_string, s4, "str_empty_string"),
      (try_begin),
        (is_between, ":center_no", towns_begin, towns_end),
        (try_begin),
          (eq, ":prosperity", 0),
          (str_store_string, s4, "str_town_prosperity_0"),
        (else_try),
          (is_between, ":prosperity", 1, 11),
          (str_store_string, s4, "str_town_prosperity_10"),
        (else_try),
          (is_between, ":prosperity", 11, 21),
          (str_store_string, s4, "str_town_prosperity_20"),
        (else_try),
          (is_between, ":prosperity", 21, 31),
          (str_store_string, s4, "str_town_prosperity_30"),
        (else_try),
          (is_between, ":prosperity", 31, 41),
          (str_store_string, s4, "str_town_prosperity_40"),
        (else_try),
          (is_between, ":prosperity", 41, 51),
          (str_store_string, s4, "str_town_prosperity_50"),
        (else_try),
          (is_between, ":prosperity", 51, 61),
          (str_store_string, s4, "str_town_prosperity_60"),
        (else_try),
          (is_between, ":prosperity", 61, 71),
          (str_store_string, s4, "str_town_prosperity_70"),
        (else_try),
          (is_between, ":prosperity", 71, 81),
          (str_store_string, s4, "str_town_prosperity_80"),
        (else_try),
          (is_between, ":prosperity", 81, 91),
          (str_store_string, s4, "str_town_prosperity_90"),
        (else_try),
          (is_between, ":prosperity", 91, 101),
          (str_store_string, s4, "str_town_prosperity_100"),
        (try_end),
      (else_try),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_begin),
          (eq, ":prosperity", 0),
          (str_store_string, s4, "str_village_prosperity_0"),
        (else_try),
          (is_between, ":prosperity", 1, 11),
          (str_store_string, s4, "str_village_prosperity_10"),
        (else_try),
          (is_between, ":prosperity", 11, 21),
          (str_store_string, s4, "str_village_prosperity_20"),
        (else_try),
          (is_between, ":prosperity", 21, 31),
          (str_store_string, s4, "str_village_prosperity_30"),
        (else_try),
          (is_between, ":prosperity", 31, 41),
          (str_store_string, s4, "str_village_prosperity_40"),
        (else_try),
          (is_between, ":prosperity", 41, 51),
          (str_store_string, s4, "str_village_prosperity_50"),
        (else_try),
          (is_between, ":prosperity", 51, 61),
          (str_store_string, s4, "str_village_prosperity_60"),
        (else_try),
          (is_between, ":prosperity", 61, 71),
          (str_store_string, s4, "str_village_prosperity_70"),
        (else_try),
          (is_between, ":prosperity", 71, 81),
          (str_store_string, s4, "str_village_prosperity_80"),
        (else_try),
          (is_between, ":prosperity", 81, 91),
          (str_store_string, s4, "str_village_prosperity_90"),
        (else_try),
          (is_between, ":prosperity", 91, 101),
          (str_store_string, s4, "str_village_prosperity_100"),
        (try_end),
      (try_end),
        ]),

  ("dplmc_player_center_surrender",
  [
    (store_script_param, ":center_no", 1),

    #protect player for 24 hours
    (store_current_hours,":protected_until"),
    (val_add, ":protected_until", 48),
    (party_get_slot, ":besieger", ":center_no", slot_center_is_besieged_by),
    (store_faction_of_party, ":besieger_faction",":besieger"),
    ##nested diplomacy start+
    #In this version this variable currently isn't used for anything
    #(party_stack_get_troop_id, ":enemy_party_leader", ":besieger", 0),
    ##nested diplomacy end+

    (party_set_slot,":besieger",slot_party_ignore_player_until,":protected_until"),
    (party_ignore_player, ":besieger", 48),
	##nested diplomacy start+
	#Add support for promoted kingdom ladies
    #(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
	(try_for_range, ":lord", heroes_begin, heroes_end),
	  (this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
	  (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
	##nested diplomacy end+
      (store_faction_of_troop, ":lord_faction", ":lord"),
      (eq, ":lord_faction", ":besieger_faction"),
      (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
      (party_is_active, ":led_party"),

      (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
      (party_slot_eq, ":led_party", slot_party_ai_object, ":besieger"),

      (party_is_active, ":besieger"),
      (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":besieger"),
      (lt, ":distance_to_marshal", 20),

      (party_set_slot,":led_party",slot_party_ignore_player_until,":protected_until"),
      (party_ignore_player, ":led_party", 48),
    (try_end),

    (party_set_faction,"$current_town","fac_neutral"), #temporarily erase faction so that it is not the closest town
    (party_get_num_attached_parties, ":num_attached_parties_to_castle",":center_no"),
    (try_for_range_backwards, ":iap", 0, ":num_attached_parties_to_castle"),
      (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":iap"),
      (party_detach, ":attached_party"),
      (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
      (eq, ":attached_party_type", spt_kingdom_hero_party),
      (neq, ":attached_party_type", "p_main_party"),
      (store_faction_of_party, ":attached_party_faction", ":attached_party"),
      (call_script, "script_get_closest_walled_center_of_faction", ":attached_party", ":attached_party_faction"),
      (try_begin),
        (gt, reg0, 0),
        (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
      (else_try),
        (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, ":center_no"),
      (try_end),
    (try_end),
    (call_script, "script_party_remove_all_companions", ":center_no"),
    (change_screen_return),
    (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"), #recalculate so that
    (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"), #leaving troops will not be considered as captured

	##nested diplomacy start+
	#Anyone who lost a fief due to your surrender will be irritated
	(try_for_range, ":village_no", centers_begin, centers_end),
       (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
	   (party_get_slot, ":village_lord", ":village_no", slot_town_lord),
	   (neq, ":village_lord", "trp_player"),
	   (is_between, ":village_lord", heroes_begin, heroes_end),
	   (call_script, "script_change_player_relation_with_troop", ":village_lord", -1),
    (try_end),
	##nested diplomacy end+
    ##diplomacy
    (call_script, "script_give_center_to_faction", "$current_town", ":besieger_faction"),
    (call_script, "script_order_best_besieger_party_to_guard_center", ":center_no", ":besieger_faction"),

    #relation and controversy
    ##nested diplomacy start+, There should be no relation bonus with the enemy lord
    #(call_script, "script_change_player_relation_with_troop", ":enemy_party_leader", 2),
    ##nested diplomacy end+
    (try_begin),
      (gt, "$players_kingdom", 0),
      (neq, "$players_kingdom", "fac_player_supporters_faction"),
      (neq, "$players_kingdom", "fac_player_faction"),
      (faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
  	  ##diplomacy start+
	  ##OLD:
      #(neq, ":faction_leader", "trp_player"),
	  ##NEW:
	  #Also guard against faction leader being some invalid negative number
	  (gt, ":faction_leader", "trp_player"),
	  ##diplomacy end+
      (call_script, "script_change_player_relation_with_troop", ":faction_leader", -2),
    (try_end),

  	(troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
  	(val_add, ":controversy", 4),
  	(val_min, ":controversy", 100),
  	(troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),
    ##nested diplmacy start+ add garrison to fief
    #The average # of troops added by script_cf_reinforce_party is 11.5.
    (assign, ":garrison_strength", 3),#easy: 34.5 for a castle
    (try_begin),
       (party_slot_eq, ":center_no", slot_party_type, spt_town),
       (assign, ":garrison_strength", 9),#easy: 103.5 for a town
    (try_end),
    #Take into account campaign difficulty.
    (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
    (try_begin),
       (eq, ":reduce_campaign_ai", 0), #hard 166% + 3 waves
       (val_mul, ":garrison_strength", 5),
       (val_div, ":garrison_strength", 3),
       (val_add, ":garrison_strength", 3),
    (else_try),
       (eq, ":reduce_campaign_ai", 1), #moderate 166%
       (val_mul, ":garrison_strength", 5),
       (val_div, ":garrison_strength", 3),
    #(else_try),
    #   (eq, ":reduce_campaign_ai", 2), #easy 100%
    #   (store_mul, ":garrison_strength", 1),
    (try_end),

    (try_for_range, ":unused", 0, ":garrison_strength"),
       (call_script, "script_cf_reinforce_party", ":center_no"),
    (try_end),
    (try_for_range, ":unused", 0, 7),# ADD some XP initially
       (store_mul, ":xp_range_min", 150, ":garrison_strength"),
       (store_mul, ":xp_range_max", 200, ":garrison_strength"),
       (store_random_in_range, ":xp", ":xp_range_min", ":xp_range_max"),
       (party_upgrade_with_xp, ":center_no", ":xp", 0),
    (try_end),
    ##nested diplomacy end+
  ]),


  ("dplmc_send_gift_to_center",
    [
    (store_script_param, ":target_party", 1),
    (store_script_param, ":gift", 2),
    (store_script_param, ":amount", 3),

    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (str_store_item_name, s12, ":gift"),
      (str_store_party_name, s13, ":target_party"),
      (display_message, "@{!}DEBUG - Bring {s12} to {s13}"),
    (try_end),

    (try_begin),
       #Guard against this being called without an explicit amount
       (lt, ":amount", 1),
       (display_message, "@{!} ERROR: Bad gift amount {reg0}.  (Tell the mod writer he needs to update his code.)  Using a safe default."),
       (assign, ":amount", 300),
    (try_end),
    (assign, ":original_amount", ":amount"),#Save this here because amount gets modified below!

    (call_script, "script_dplmc_withdraw_from_treasury", 50),
    (troop_get_inventory_capacity, ":capacity", "trp_household_possessions"),
	  (try_for_range, ":inventory_slot", 0, ":capacity"),
	    (gt, ":amount", 0),
		  (troop_get_inventory_slot, ":item", "trp_household_possessions", ":inventory_slot"),
		  (eq, ":item", ":gift"),
		  (troop_inventory_slot_get_item_amount, ":tmp_amount", "trp_household_possessions", ":inventory_slot"),
		  (try_begin),
		    (le, ":tmp_amount", ":amount"),
		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", 0),
		    (val_sub, ":amount", ":tmp_amount"),
		  (else_try),
		    (val_sub, ":tmp_amount", ":amount"),
		    (troop_inventory_slot_set_item_amount, "trp_household_possessions", ":inventory_slot", ":tmp_amount"),
		    (assign, ":amount", 0),
		  (try_end),
	  (try_end),

    (set_spawn_radius, 1),
    (spawn_around_party, "$current_town", "pt_dplmc_gift_caravan"),
    (assign,":spawned_party",reg0),
    (party_set_slot, ":spawned_party", slot_party_type, dplmc_spt_gift_caravan),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_diplomacy, ":gift"),
    (party_set_slot, ":spawned_party",  slot_party_orders_object, 0),

    (party_set_ai_behavior, ":spawned_party", ai_bhvr_travel_to_party),
    (party_set_ai_object, ":spawned_party", ":target_party"),
    (party_set_slot, ":spawned_party", slot_party_ai_object, ":target_party"),
    (party_stack_get_troop_id, ":caravan_master", ":spawned_party", 0),
    (troop_set_slot, ":caravan_master", slot_troop_leaded_party, ":spawned_party"),
    (troop_set_slot, ":caravan_master", slot_troop_leaded_party, ":spawned_party"),
    (party_set_slot, ":spawned_party", dplmc_slot_party_mission_parameter_1, ":original_amount"),
    ]),

    # For internal use only
  # param 1: center no
  # param 2: party_no_to_collect_heroes
  # param 3: minimum time since last met (inclusive), or negative for no restriction
  # param 4: maximum time since last met (exclusive), or negative for no restriction
  ("dplmc_time_sorted_heroes_for_center_aux",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (store_script_param, ":min_time", 3),
      (store_script_param, ":max_time", 4),

      (store_current_hours, ":current_hours"),

      (party_get_num_companion_stacks, ":num_stacks",":center_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":center_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        #get time since last talk
        (troop_get_slot, ":troop_last_talk_time", ":stack_troop", slot_troop_last_talk_time),
        (store_sub, ":time_since_last_talk", ":current_hours", ":troop_last_talk_time"),
        #add if time meets constraints
        (this_or_next|ge, ":time_since_last_talk", ":min_time"),
           (lt, ":min_time", 0),
        (this_or_next|lt, ":time_since_last_talk", ":max_time"),
           (lt, ":max_time", 0),
        (party_add_members, ":party_no_to_collect_heroes", ":stack_troop", 1),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":center_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":center_no", ":attached_party_rank"),
        (call_script, "script_dplmc_time_sorted_heroes_for_center_aux", ":attached_party", ":party_no_to_collect_heroes",":min_time",":max_time"),
      (try_end),
  ]),

  # script_dplmc_time_sorted_heroes_for_center
  # Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
  # Output: none, adds heroes to the party_no_to_collect_heroes party
  # The catch is that it returns heroes who haven't been met in a day
  # or more before others, for greater use in feasts.
  ("dplmc_time_sorted_heroes_for_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),

      #SB: include these heroes in sorting
      (try_begin),
        (eq, "$g_player_court", ":center_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
        ##diplomacy start+
        #It's not exactly clear if this would work for kingdom ladies.  If they
        #can go from slto_kingdom_lady to slto_inactive, this could take them
        #from there to slto_kingdom_hero unintentionally.
        #
        #Because of this, don't enable this for now.  Elsewhere (where defections
        #occur) add alternate behavior for promoted kingdom ladies.
        #
        #TODO: Later, make sure that kingdom ladies are never inactive normally,
        #so this loop can be expanded to work with them.
        ##diplomacy end+
        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
          (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
          (eq, ":active_npc_faction", "fac_player_supporters_faction"),
          (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_inactive),
          (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she is not prisoner in any center.
          (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she does not have a party
          (neq, ":active_npc", "$g_player_minister"),
          (party_add_members, ":party_no_to_collect_heroes", ":active_npc"),
          # (set_visitor, ":cur_pos", ":active_npc"),
          # (val_add,":cur_pos", 1),
        (try_end),
      (try_end),

     #Non-attached pretenders (make sure they're not thrown under the bus)
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

     #Heroes you haven't spoken to in 24+ hours
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", 24, -1),

     #Heroes you haven't spoken to in 12 to 24 hours
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", 12, 24),

     #Everyone else
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", -1, 12),
  ]),

  # script_script_dplmc_faction_leader_splits_gold
  # INPUT: arg1 = faction_id
  #        arg2 = troop_1
  #        arg2 = troop_2
  #        arg3 = town_point_value (see explanation below)
  #
  # OUTPUT:
  #        reg0 = total renown / total faction points (or 0 if no centers held)
  #        reg1 = troop_1 total (not divided)
  #        reg2 = troop_2 total (not divided)
  #        reg3 = faction average lord renown (or 0 if no lords)
  #
  #In various places the game tallies center points differently.  The values of
  #villages/castles/fiefs, respectively, in some places are 1/2/2, in other
  #places are 1/2/3, and in others are 1/3/4.
  #Specifying the town point value determines which scheme will be used to
  #determine ceter points:
  #        arg3 = 2 gives 1/2/2
  #        arg3 = 3 gives 1/2/3
  #        arg3 = 4 gives 1/2/4
  #
  #If the specified town_point_value is not 2,3, or 4, the script is allowed to
  #clamp the value or substitute a default.
  ("dplmc_center_point_calc",
    [
		(store_script_param, ":faction_id", 1),
		(store_script_param, ":troop_1", 2),
		(store_script_param, ":troop_2", 3),
		(store_script_param, ":town_point_value", 4),

		(val_clamp, ":town_point_value", 2, 5),

		#The outputs
		(assign, ":faction_score", 0),
		(assign, ":troop_1_score", 0),
		(assign, ":troop_2_score", 0),
		#(assign, ":average_renown", 0),

		#Intermediate values we use for computing outputs
		(assign, ":total_renown", 0),
		(assign, ":num_lords", 0),

		#Handle the player first
		#(assign, ":player_in_faction", 0),
		(assign, ":faction_alias", ":faction_id"),
		(try_begin),
			(this_or_next|eq, ":faction_id", "$players_kingdom"),
				(eq, ":faction_id", "fac_player_supporters_faction"),
			(val_add, ":num_lords", 1),
			(troop_get_slot, ":total_renown", "trp_player", slot_troop_renown),
			#(assign, ":player_in_faction", 1),
			(assign, ":faction_alias", "fac_player_supporters_faction"),
			(eq, ":faction_id", "fac_player_supporters_faction"),
			(assign, ":faction_alias", "$players_kingdom"),
		(try_end),

		#Get lords in faction
		(try_for_range, ":troop_no", heroes_begin, heroes_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(this_or_next|eq, ":faction_no", ":faction_id"),
				(eq, ":faction_no", ":faction_alias"),

			(val_add, ":num_lords", 1),
			(troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
			(val_max, ":renown", 0),
			(val_add, ":total_renown", ":renown"),
		(try_end),

		#Get stats for centers
		(try_for_parties, ":center_no"),
			(assign, ":points", 0),
			(try_begin),
				#Towns are 2, 3, or 4 points
				(this_or_next|is_between, ":center_no", towns_begin, towns_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(assign, ":points", ":town_point_value"),
			(else_try),
				#Castles are always 2 points
				(this_or_next|is_between, ":center_no", castles_begin, castles_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(assign, ":points", 2),#castles are always 2
			(else_try),
				#Villages are always 1 point
				(this_or_next|is_between, ":center_no", villages_begin, villages_end),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(try_end),

			#Don't process parties that aren't centers.
			(ge, ":points", 1),

			#NB: We don't know for sure that troop_1 and troop_2 aren't the
			#same value, and we don't even necessarily know that they're part
			#of the specified faction.
			(try_begin),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_1"),
				(val_add, ":troop_1_score", ":points"),
			(try_end),

			(try_begin),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_2"),
				(val_add, ":troop_2_score", ":points"),
			(try_end),

			(store_faction_of_party, ":faction_no", ":center_no"),
			(this_or_next|eq, ":faction_no", ":faction_id"),
				(eq, ":faction_no", ":faction_alias"),
			(val_add, ":faction_score", ":points"),
		(try_end),

		# OUTPUT:
		#        reg0 = faction renown / faction points (or 0 if faction has no centers)
		#        reg1 = troop_1 total (not divided)
		#        reg2 = troop_2 total (not divided)
		#        reg3 = faction average lord renown (or 0 if no lords)
		(assign, reg0, 0),
		(try_begin),
			(neq, ":faction_score", 0),
			(store_div, reg0, ":total_renown", ":faction_score"),
		(try_end),
		(assign, reg1, ":troop_1_score"),
		(assign, reg2, ":troop_2_score"),
		(assign, reg3, 0),
		(try_begin),
			(neq, ":num_lords", 0),
			(store_div, reg0, ":total_renown", ":num_lords"),
		(try_end),
	]),


  #script_dplmc_good_produced_at_center_or_its_villages
  # For towns, also includes the villages that attach to it
  #
  # INPUT: arg1 = good_no
  #        arg2 = center_no
  # OUTPUT:
  #        reg0 = 0 if no, 1 if yes
  ("dplmc_good_produced_at_center_or_its_villages",
  [
	(store_script_param, ":good_no", 1),
	(store_script_param, ":center_no", 2),

	(assign, ":has_good", 0),
	(assign, ":save_reg1", reg1),
	(assign, ":save_reg2", reg2),
	(store_current_hours, ":cur_hours"),
	(store_sub, ":recent_time", ":cur_hours", 3 * 24),


	(try_begin),
		(is_between, ":good_no", trade_goods_begin, trade_goods_end),
		(ge, ":center_no", 1),
		(this_or_next|is_between, ":center_no", centers_begin, centers_end),
			(party_is_active, ":center_no"),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
			(is_between, ":center_no", centers_begin, centers_end),
		(call_script, "script_center_get_production", ":center_no", ":good_no"),
		(try_begin),
			#Positive production
			(ge, reg0, 1),
			(assign, ":has_good", 1),
		(else_try),
			#Is a town or a castle, and one of its villages has positive prodution
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(try_for_range, ":cur_village", villages_begin, villages_end),
				(eq, ":has_good", 0),
				#is bound to center
				(this_or_next|party_slot_eq, ":cur_village", slot_village_market_town, ":center_no"),
					(party_slot_eq, ":cur_village", slot_village_bound_center, ":center_no"),#for castles
               (assign, reg0, 0),
               (try_begin),
                  #If a trading party from the village reached the town recently, its goods are
				  #available.
                  (party_slot_ge, ":cur_village", dplmc_slot_village_trade_last_arrived_to_market, ":recent_time"),
                  (assign, reg0, 1),
               (else_try),
                  #If the village is not looted and this center is not under siege, the
				  #goods from the village could be acquired if they were needed.
					   (neg|party_slot_eq, ":cur_village", slot_village_state, svs_looted),
					   (neg|party_slot_eq, ":cur_village", slot_village_state, svs_deserted),
                  (neg|party_slot_eq, ":center_no", slot_village_state, svs_under_siege),
                  (assign, reg0, 1),
               (try_end),
               (eq, reg0, 1),
				#If an eligible village has positive production, set "has_good" to true.
				(call_script, "script_center_get_production", ":cur_village", ":good_no"),
				(ge, reg0, 1),
				(assign, ":has_good", 1),
			(try_end),
		(try_end),
	(try_end),

	(assign, reg0, ":has_good"),
	(assign, reg1, ":save_reg1"),
	(assign, reg2, ":save_reg2"),
  ]),

  #script_dplmc_assess_ability_to_purchase_good_from_center
  # INPUT: arg1 = good_no
  #        arg2 = center_no
  # OUTPUT:
  #        reg0 = actual price (may be theoretical if unavailable)
  #        reg1 = 1 if available, 0 if unavailable
  ("dplmc_assess_ability_to_purchase_good_from_center",
    [
		(store_script_param, ":good_no", 1),
		(store_script_param, ":center_no", 2),

		#This is still quite experimental.  This is a work in progress
                #rather than a finished formula.
		(assign, ":price_factor", average_price_factor),
		(assign, ":has_good", 0),

		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),

			(is_between, ":good_no", trade_goods_begin, trade_goods_end),

			(store_sub, ":item_slot_no", ":good_no", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":price_factor", ":center_no", ":item_slot_no"),

			(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":good_no", ":center_no"),
			(assign, ":has_good", reg0),
			#abort if good is found
			(lt, ":has_good", 1),

			(store_faction_of_party, ":center_faction", ":center_no"),
			(faction_get_slot, ":mercantilism", ":center_faction", dplmc_slot_faction_mercantilism),
			(val_clamp, ":mercantilism", -3, 4),

			#For towns, check trade centers.
			(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(is_between, ":center_no", towns_begin, towns_end),

			(store_current_hours, ":cur_hours"),
			(assign, ":best_foreign_price", maximum_price_factor),
         (assign, ":worst_price_seen", ":price_factor"),

			(try_for_range, ":trade_town_index", slot_town_trade_routes_begin, slot_town_trade_routes_end),
				(party_get_slot, ":trade_town", ":center_no", ":trade_town_index"),
            (is_between, ":trade_town", centers_begin, centers_end),

				(party_get_slot, ":price_factor_2", ":trade_town", ":item_slot_no"),
				(val_max, ":worst_price_seen", ":price_factor_2"),

            (party_slot_eq, ":trade_town", slot_party_type, spt_town),
				(call_script, "script_dplmc_good_produced_at_center_or_its_villages", ":good_no", ":trade_town"),
				#The town has or produces the item
				(ge, reg0, 1),

				#Get the number of hours since the last caravan arrival, and set the penalty accordingly.
				(assign, ":hours_since", 0),
				#The slot storing the arrival time.  This may be uninitialized for old saved games used
				#with this mod.
				(store_sub, ":arrival_slot", ":trade_town_index", slot_town_trade_routes_begin),
				(val_add, ":arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin),
				(try_begin),
					#This condition can only occur if the number of trade route slots was increased
					#but the number of trade arrival time slots was not.  Check just in case, to avoid
					#strange errors.
					(neg|is_between, ":arrival_slot", dplmc_slot_town_trade_route_last_arrivals_begin, dplmc_slot_town_trade_route_last_arrivals_end),
					#Set "hours-since" to one week.
					(assign, ":hours_since", 7 * 24),
				(else_try),
					#If the slot is uninitialized, give it a random plausible value.
					(party_slot_eq, ":center_no", ":arrival_slot", 0),#Uninitialzed memory!
					(store_random_in_range, ":hours_since", 1, (24 * 7 * 5) + 1),#random time in last five weeks
					(party_get_slot, ":prosperity_factor", ":center_no", slot_town_prosperity),
					(val_clamp, ":prosperity_factor", 0, 101),
					(val_add, ":prosperity_factor", 75),
					(val_mul, ":hours_since", 125),
					(val_div, ":hours_since", ":prosperity_factor"),#last arrival some time in the last five weeks, plus or minus up to 40% based on prosperity
					(store_sub, ":last_arrival", ":cur_hours", ":hours_since"),
					(party_set_slot, ":center_no", ":arrival_slot", ":last_arrival"),
				(else_try),
					(party_get_slot, ":last_arrival", ":center_no", ":arrival_slot"),
					(store_sub, ":hours_since", ":cur_hours", ":last_arrival"),
					(val_max, ":hours_since", 0),
				(try_end),


				#Base penalty is 5%.  It stays at a flat 5% for the first week, then begins rising
				#at a rate of 5% per week afterwards (incremented continuously).
				#Clamp the maximum penalty at 50%.
				(store_mul, ":penalty", ":hours_since", 5),
				(val_add, ":penalty", (24 * 7) // 2),
				(val_div, ":penalty", 24 * 7),
				(val_max, ":penalty", 5),#required for the first week
				(val_min, ":penalty", 50),#don't increase above 50%

				#Apply mercantilism
				(store_faction_of_party, ":other_faction", ":trade_town"),
				(try_begin),
					#Decrease penalty for mercantilism, increase for free trade
					(eq, ":other_faction", ":center_faction"),
					(val_sub, ":penalty", ":mercantilism"),
				(else_try),
					#Increase penalty for mercantilism, decrease for free trade
					(val_add, ":penalty", ":mercantilism"),
				(try_end),

				(try_begin),
					(ge, ":price_factor_2", average_price_factor),
					(val_mul, ":price_factor_2", ":penalty"),
					(val_add, ":price_factor_2", 50),
					(val_div, ":price_factor_2", 100),
				(else_try),
					(store_add, reg0, 100, ":penalty"),
					(val_mul, reg0, average_price_factor),
					(val_add, reg0, 50),
					(val_div, reg0, 100),
					(val_add, ":price_factor_2", reg0),
				(try_end),
				#Make use of the source
				(assign, ":has_good", 1),
				(val_min, ":best_foreign_price", ":price_factor_2"),
			(try_end),
			(try_begin),
			   (ge, ":has_good", 1),
				(val_max, ":price_factor", ":best_foreign_price"),
			(else_try),
  		      #Make it so that lack of supply will not make the price lower
			   (lt, ":has_good", 1),
			   (val_max, ":price_factor", ":worst_price_seen"),
			(try_end),
		(try_end),

		(try_begin),
			(lt, ":has_good", 1),
			(val_max, ":price_factor", average_price_factor),#don't give bargains if there is no supply
			(val_mul, ":price_factor", 8),#sixty percent penalty
			(val_div, ":price_factor", 5),
		(try_end),

		#Apply constraints at the last step
		(val_clamp, ":price_factor", minimum_price_factor, maximum_price_factor),

		(assign, reg0, ":price_factor"),
		(assign, reg1, ":has_good"),
	]),

	# script_dplmc_get_faction_truce_length_with_faction
  #
  #similar to script_print_troop_owned_centers_in_numbers_to_s0
  #
  #INPUT:
  #  arg1: owned_towns
  #  arg2: owned_castles
  #  arg3: owned_villages
  #
  #OUTPUT:
  #  reg0: owned_towns + owned_castles + owned_villages
  #    s0: a string describing the numbers of centers
    ("dplmc_print_centers_in_numbers_to_s0",
   [
     (store_script_param_1, ":owned_towns"),
	 (store_script_param_2, ":owned_castles"),
	 (store_script_param, ":owned_villages", 3),
     (str_store_string, s0, "@nothing"),

     (assign, ":num_types", 0),
     (try_begin),
       (gt, ":owned_villages", 0),
       (assign, reg0, ":owned_villages"),
       (store_sub, reg1, reg0, 1),
       (str_store_string, s0, "@{reg0} village{reg1?s:}"),
       (val_add, ":num_types", 1),
     (try_end),

     (try_begin),
       (gt, ":owned_castles", 0),
       (assign, reg0, ":owned_castles"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} castle{reg1?s:}"),
       (else_try),
         (str_store_string, s0, "@{reg0} castle{reg1?s:} and {s0}"),
       (try_end),
       (val_add, ":num_types", 1),
     (try_end),

     (try_begin),
       (gt, ":owned_towns", 0),
       (assign, reg0, ":owned_towns"),
       (store_sub, reg1, reg0, 1),
       (try_begin),
         (eq, ":num_types", 0),
         (str_store_string, s0, "@{reg0} town{reg1?s:}"),
       (else_try),
         (eq, ":num_types", 1),
         (str_store_string, s0, "@{reg0} town{reg1?s:} and {s0}"),
       (else_try),
         (str_store_string, s0, "@{reg0} town{reg1?s:}, {s0}"),
       (try_end),
     (try_end),

     (store_add, reg0, ":owned_villages", ":owned_castles"),
     (val_add, reg0, ":owned_towns"),
     ]),

  #"script_dplmc_distribute_gold_to_lord_and_holdings"
  #  Similar to script_calculate_troop_score_for_center
  #
  # slot_troop_temp_slot must already be loaded with center points;
  # dplmc_slot_troop_temp_slot must already be loaded with distance.
  #
  # Input: arg1 = evaluator
  #        arg2 = troop_no
  #        arg3 = center_no
  # Output: reg0 = score
  #         reg1 = explanation string
  ("dplmc_calculate_troop_score_for_center_aux",
   [(store_script_param, ":troop_1", 1),
    (store_script_param, ":troop_2", 2),
	 (store_script_param, ":center_no", 3),

	 (assign, ":explanation", "str_political_explanation_most_deserving_in_faction"),
	 (assign, ":explanation_priority", -1),

   (try_begin),
      (lt, ":troop_1", 0),
      (assign, ":relation", 0),
      (assign, ":reputation", lrep_none),
   (else_try),
      (eq, ":troop_1", ":troop_2"),
      (assign, ":relation", 50),
	   (troop_get_slot, ":reputation", ":troop_1", slot_lord_reputation_type),
   (else_try),
      (call_script, "script_troop_get_relation_with_troop", ":troop_1", ":troop_2"),
      (assign, ":relation", reg0),
      (troop_get_slot, ":reputation", ":troop_1", slot_lord_reputation_type),
   (try_end),
   (val_clamp, ":relation", -100, 101),

   (troop_get_slot, reg0, ":troop_2", slot_troop_renown),
   (val_max, reg0, 0),
   (store_add, ":score", 500, reg0),
	(troop_get_slot, ":num_center_points", ":troop_2", slot_troop_temp_slot),
	(val_max, ":num_center_points", 0),
	(val_add, ":num_center_points", 1),

	#Subtract distance from closest other fief owned, except when
	#considering the lord's original holdings.
	(try_begin),
	  (troop_slot_ge, ":troop_2", slot_troop_temp_slot, 1),
	  (neg|troop_slot_eq, ":troop_2", slot_troop_home, ":center_no"),
	  (neg|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_2"),

	  (troop_get_slot, reg0, ":troop_2", dplmc_slot_troop_temp_slot),
	  (gt, reg0, 1),
	  (val_min, reg0, 250),#upper cap on distance effect (bear in mind that this is subtracted from 500 + troop renown)
	  (val_sub, ":score", reg0),
	(try_end),

   #(store_random_in_range, ":random", 50, 100),
   #(val_mul, ":score", ":random"),
	(val_mul, ":score", 75),
   (val_div, ":score", ":num_center_points"),

	(assign, ":fiefless_bonus_used", 0),
	(try_begin),
	   #Bonus for lords with no other fiefs when a village is being considered.
      (lt, ":num_center_points", 2),
	  (party_slot_eq, ":center_no", slot_party_type, spt_village),
      (neq, ":reputation", lrep_debauched),
      (neq, ":reputation", lrep_selfrighteous),
      (neq, ":reputation", lrep_quarrelsome),
		(val_mul, ":score", 2),
		(try_begin),
		  (lt, ":explanation_priority", 100),
		  (assign, ":explanation_priority", 100),
		  (assign, ":explanation", "str_political_explanation_lord_lacks_center"),
		(try_end),
	 (assign, ":fiefless_bonus_used", 1),#because it has already been applied
	(try_end),

	(assign, ":troop_2_slot_alias", ":troop_2"),
	(try_begin),
		(eq, ":troop_2", "trp_player"),
		(assign, ":troop_2_slot_alias", "trp_kingdom_heroes_including_player_begin"),
	(try_end),

   (try_begin),
	#Bonus for conquerer
		(neq, ":reputation",  lrep_debauched),
		(this_or_next|neq, ":reputation", lrep_selfrighteous),
		   (eq, ":troop_1", ":troop_2"),
		(neq, ":reputation", lrep_cunning),
	  (neg|party_slot_eq, ":center_no", slot_party_type, spt_village),
      (party_slot_eq, ":center_no", slot_center_last_taken_by_troop, ":troop_2_slot_alias"),
	  (try_begin),
		 (lt, ":num_center_points", 2),
		 (eq, ":fiefless_bonus_used", 0),
		 (assign, reg1, 50),#50% increase
	  (else_try),
	     (this_or_next|troop_slot_eq, ":troop_2", slot_troop_home, ":center_no"),
		 (this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_2_slot_alias"),
		 (this_or_next|party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_2_slot_alias"),
			(eq, ":reputation", lrep_martial),
		 (assign, reg1, 50),#50% increase
	  (else_try),
		 (assign, reg1, 25),#25% increase
	  (try_end),
	  (store_add, reg0, 100, reg1),
	  (val_mul, ":score", reg0),
	  (val_div, ":score", 100),
		(try_begin),
		  (ge, reg1, ":explanation_priority"),
		  (assign, ":explanation_priority", reg1),
		  (assign, ":explanation", "str_political_explanation_lord_took_center"),
 		(try_end),
	(else_try),
	#Bonus for original owner
		(gt, ":troop_2", 0),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_2_slot_alias"),
		(try_begin),
			(lt, ":num_center_points", 2),
			(eq, ":fiefless_bonus_used", 0),
			(assign, reg1, 50),#50% increase
		(else_try),
			(this_or_next|eq, ":troop_2", ":troop_1"),
			(this_or_next|troop_slot_eq, ":troop_2", slot_troop_home, ":center_no"),
				(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_2_slot_alias"),
			(assign, reg1, 50),#50% increase
		(else_try),
			(assign, reg1, 25),#25% increase
		(try_end),
		(store_add, reg0, 100, reg1),
		(val_mul, ":score", reg0),
		(val_div, ":score", 100),
		(try_begin),
		  (ge, reg1, ":explanation_priority"),
		  (assign, ":explanation_priority", reg1),
        (assign, ":explanation", "str_dplmc_political_explanation_original_lord"),
 		(try_end),
	(else_try),
	#Bonus for previous owner, lord
		(gt, ":troop_2", 0),
		(party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, ":troop_2_slot_alias"),
		(try_begin),
			(lt, ":num_center_points", 2),
			(eq, ":fiefless_bonus_used", 0),
			(assign, reg1, 50),#50% increase
		(else_try),
		(troop_slot_eq, ":troop_2", slot_troop_home, ":center_no"),
			(assign, reg1, 50),
		(else_try),
			(assign, reg1, 25),#25% increase
		(try_end),
		(store_add, reg0, 100, reg1),
		(val_mul, ":score", reg0),
		(val_div, ":score", 100),
		(try_begin),
		  (ge, reg1, ":explanation_priority"),
		  (assign, ":explanation_priority", reg1),
        (assign, ":explanation", "str_dplmc_political_explanation_original_lord"),
 		(try_end),
	(else_try),
	#Bonus for lord claiming the center as home
		(troop_slot_eq, ":troop_2", slot_troop_home, ":center_no"),
		(val_mul, ":score", 5),
		(val_div, ":score", 4),
		(try_begin),
		  (ge, 25, ":explanation_priority"),
		  (assign, ":explanation_priority", 25),
        (assign, ":explanation", "str_dplmc_political_explanation_original_lord"),
 		(try_end),
	(else_try),
	#Aesthetic penalty (doesn't apply when there was a bonus)
	#To try to make the late game less mixed, have a preference towards
	#assigning lords to their own faction types.
		(troop_get_slot, reg0, ":troop_2", slot_troop_original_faction),
		(party_get_slot, reg1, ":center_no", slot_center_original_faction),
		(neq, reg0, reg1),
	#These extra checks are to avoid penalizing the player or promoted companions
	#unintentionally.
		(is_between, reg0, npc_kingdoms_begin, npc_kingdoms_end),
		(is_between, reg1, npc_kingdoms_begin, npc_kingdoms_end),
		#Take 95% of score
		(val_mul, ":score", 19),
		(val_add, ":score", 10),
		(val_div, ":score", 20),
   (try_end),

	#add 2 x relation (minus controversy) to score
   (troop_get_slot, ":controversy", ":troop_2", slot_troop_controversy),
   (val_clamp, ":controversy", 0, 101),
	(store_mul, ":relation_mod", ":relation", 2),
	(val_sub, ":relation_mod", ":controversy"),
	#this modifier will not raise the score by more than 50%
	(store_add, reg0, ":score", 1),
	(val_div, reg0, 2),
	(val_max, reg0, 1),
	(val_min, ":relation_mod", reg0),

	(store_mul, reg0, ":score", 100),#rego has pre-relationship modified score
	(val_add, ":score", ":relation_mod"),
	(val_div, reg0, ":score"),
	(store_sub, reg1, ":score", 100),#reg1 has percentage change (i.e. 1.5 times becomes 50% change) from relation/controversy

	(try_begin),
		(ge, reg1, 0),
		(ge, reg1, ":explanation_priority"),
		  (ge, ":relation", 15),
		(assign, ":explanation_priority", reg1),
		  (assign, ":explanation", "str_political_explanation_most_deserving_friend"),
	(try_end),

   (assign, reg0, ":score"),
	(assign, reg1, ":explanation"),
   ]),


  #Adapted "auto-sell" from rubik's Custom Commander
  #does not account for alternative towns
  ("cf_no_known_taverngoers",
  [
      (store_script_param_1, ":begin"),
      (store_script_param_2, ":end"),
      # (assign, ":num_towns", tavern_booksellers_end),
      (try_for_range, ":troop_no", ":begin", ":end"),
        # (neg|party_slot_eq, ":town_no", slot_center_tavern_bookseller, 0),
        # (party_get_slot, ":seller", ":town_no", slot_center_tavern_bookseller),#addition - fixed 2011-03-29
        (troop_slot_ge, ":troop_no", slot_troop_met, 1),
        (troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
        (is_between, ":town_no", walled_centers_begin, walled_centers_end),
        (assign, ":end", ":begin"), #loop break
      (try_end),
      (neq, ":begin", ":end"),
  ]),

  #script_list_known_taverngoers
  #input: starting/ending troop range, also party slot if necessary as error check
  #output: location of known tavern npcs to s11
  ("list_known_taverngoers",
  [
      (store_script_param, ":begin", 1),
      (store_script_param, ":end", 2),
      (store_script_param, ":slot_no", 3),

      (assign, ":num_towns", 0),
      (try_for_range, ":troop_no", ":begin", ":end"),
        (this_or_next|troop_slot_ge, ":troop_no", slot_troop_met, 1),
        (troop_slot_eq, ":troop_no", slot_troop_cur_center, "$current_town"),
        (troop_get_slot, ":town_no", ":troop_no", slot_troop_cur_center),
        (is_between, ":town_no", walled_centers_begin, walled_centers_end),
        # (neg|party_slot_eq, ":town_no", slot_center_ransom_broker, 0),
        (party_slot_eq, ":town_no", ":slot_no", ":troop_no"),
        (val_add, ":num_towns", 1),
        (str_store_party_name_link, s50, ":town_no"),
        (try_begin),
          (eq, ":num_towns", 1),
          (str_store_string, s51, s50),
        (else_try),
          (eq, ":num_towns", 2),
          (str_store_string, s51, "str_s50_and_s51"),
        (else_try),
          (str_store_string, s51, "str_s50_comma_s51"),
        (try_end),

        (try_begin), #list false tavern npcs
          (call_script, "script_cf_find_alternative_town_for_taverngoers", ":town_no", -9),
          (assign, ":alternative_town", reg0),
          (neg|party_slot_ge, ":alternative_town", ":slot_no", ":begin"),
          (val_add, ":num_towns", 1),
          (str_store_party_name_link, s52, ":alternative_town"),
          (try_begin), #this is at least the second town in the string
            (eq, ":num_towns", 2),
            (str_store_string, s51, "str_s52_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s52_comma_s51"),
          (try_end),
        (try_end),
        # (display_message, "@{s51}"),
      (try_end),
      (str_store_troop_name_plural, s10, ":begin"), #default titles "book_merchant" "ransom_broker" etc
      (str_store_string_reg, s11, s51),
      (display_message, "@You can find {s10}s at {s11}."),
  ]),
  #native functionality to increase tavern diversity
  ("cf_find_alternative_town_for_taverngoers",
  [
      (store_script_param_1, ":town_no"),
      (store_script_param_2, ":adder"),
      (store_add, ":alternative_town", ":town_no", ":adder"), #should really randomize this

      # (store_sub, ":num_towns", towns_end, towns_begin),
      (try_begin),
        (ge, ":alternative_town", towns_end),
        (val_sub, ":alternative_town", towns_end),
        (val_add, ":alternative_town", towns_begin),
      (else_try),
        (lt, ":alternative_town", towns_begin),
        (val_add, ":alternative_town", towns_end),
      (try_end),
      ##diplomacy start+
      #The above code makes assumptions about the number of towns that might not be true on other maps.
      #Changing it to support variable sizes would not be hard, but I'm not convinced that it is so
      #desirable in the first place.
      (is_between, ":alternative_town", towns_begin, towns_end),
      # (party_slot_eq, ":alternative_town", slot_party_type, spt_town),
      (assign, reg0, ":alternative_town"),
  ]),

  #script_calculate_ransom_contribution
  #input: center's slot no, entry points
  #used to talk to various center merchant npcs including guildmaster
  ("start_town_conversation",
	[
	  (store_script_param, ":troop_slot_no", 1),
	  (store_script_param, ":entry_no", 2),

      (assign, "$talk_context", tc_town_talk),
	  (try_begin),
		(eq, ":troop_slot_no", slot_town_merchant),
		(assign, ":scene_slot_no", slot_town_store),
	  (else_try),
		(eq, ":troop_slot_no", slot_town_tavernkeeper),
		(assign, ":scene_slot_no", slot_town_tavern),
        (assign, "$talk_context", tc_tavern_talk),
	  (else_try),
		(assign, ":scene_slot_no", slot_town_center),
	  (try_end),

	  (party_get_slot, ":conversation_scene", "$current_town", ":scene_slot_no"),
	  (modify_visitors_at_site, ":conversation_scene"),
	  (reset_visitors),
	  (set_visitor, 0, "trp_player"),

	  (try_begin),
		(gt, "$sneaked_into_town", disguise_none),
		(mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_all),
        #SB : use script call
        (call_script, "script_set_disguise_override_items", "mt_conversation_encounter", 0, 0),
	  (else_try),
		(mission_tpl_entry_set_override_flags, "mt_conversation_encounter", 0, af_override_horse),
		(mission_tpl_entry_clear_override_items, "mt_conversation_encounter", 0),
	  (try_end),
	  (party_get_slot, ":conversation_troop", "$current_town", ":troop_slot_no"),
	  (set_visitor, ":entry_no", ":conversation_troop"),
	  (set_jump_mission,"mt_conversation_encounter"),
	  (jump_to_scene, ":conversation_scene"),
	  (change_screen_map_conversation, ":conversation_troop"),
	]),
    #talking to people outside the court (neutral, tc_castle_gate)
  # INPUT: none
  # OUTPUT: none
  ("cf_village_normal_cond",
    [
    (store_script_param, ":party_no", 1),
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_looted),
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_deserted), #SB : addition here
    (neg|party_slot_eq, ":party_no", slot_village_state, svs_being_raided),
    (neg|party_slot_ge, ":party_no", slot_village_infested_by_bandits, 1),
    ]
  ),

    #script_cf_has_companion_emissary for diplomatic options
]
