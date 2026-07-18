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
# PARTY AI & ROUTING SCRIPTS
# 
# This file contains the logic for how non-player parties (lords, bandits, patrols) move
# on the world map. It handles target selection, pathing, fleeing, and joining sieges.
####################################################################################################################

party_ai_scripts = [
  # This script selects a random town in range [towns_begin, towns_end)
  # INPUTS:
  # none

  #OUTPUT:
  # reg0: id of the selected random town
##  ("select_random_town",
##    [
##      (assign, ":num_towns", towns_end),
##      (val_sub,":num_towns", towns_begin),
##      (store_random, ":random_town", ":num_towns"),
##      (val_add,":random_town", towns_begin),
##      (assign, reg0, ":random_town"),
##  ]),

#  ("select_random_spawn_point",
#    [
#      (assign, reg(20), spawn_points_end),
#      (val_sub,reg(20), spawn_points_begin),
#      (store_random, reg(21), reg(20)),
#      (val_add,reg(21), spawn_points_begin),
#      (assign, "$pout_town", reg(21)),
# ]),

  #script_cf_select_random_town_with_faction:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # INPUT:
  # arg1 = faction_no

  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  #script_cf_select_random_village_with_faction:
  # This script selects a random village in range [villages_begin, villages_end)
  # such that faction of the village is equal to given_faction
  # INPUT:
  # arg1 = faction_no

  #OUTPUT:
  # This script may return false if there is no matching village.
  # reg0 = village_no
  ("cf_select_random_village_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
      (try_end),
      (gt, ":no_villages", 0), #Fail if there are no villages
      (store_random_in_range, ":random_village", 0, ":no_villages"),
      (assign, ":no_villages", 0),
      (try_for_range,":cur_village", villages_begin, villages_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_village"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_villages", 1),
        (gt, ":no_villages", ":random_village"),
        (assign, ":result", ":cur_village"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


  #script_cf_select_random_walled_center_with_faction:
  # This script selects a random center in range [centers_begin, centers_end)
  # such that faction of the town is equal to given_faction
  # INPUT:
  # arg1 = faction_no
  # arg2 = preferred_center_no

  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no (Can fail)
  ("cf_select_random_walled_center_with_faction",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_centers", 1),
        (eq, ":cur_center", ":preferred_center_no"),
        (val_add, ":no_centers", 99),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


  #script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege:
  # INPUT:
  # arg1 = faction_no
  # arg2 = owner_troop_no
  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = center_no (Can fail)
  ("cf_select_random_walled_center_with_faction_and_owner_priority_no_siege",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":troop_no", 2),
      (assign, ":result", -1),
      (assign, ":no_centers", 0),

      #SB : faction active conditional
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (call_script, "script_lord_get_home_center", ":troop_no"),
      (assign, ":home_center", reg0),

      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),

        #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
        (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09

        (val_add, ":no_centers", 1000),
      (try_end),

      #if no center is available count all centers not besieged do not care its faction.
      (try_begin),
        (le, ":no_centers", 0),
        (ge, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
        (assign, "$g_there_is_no_avaliable_centers", 1),

        (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
          #SB : probably original faction
          (party_slot_eq, ":cur_center", slot_center_original_faction, ":faction_no"),
          (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
          (val_add, ":no_centers", 1),
        (try_end),
      (else_try),
        (assign, "$g_there_is_no_avaliable_centers", 0),
      (try_end),

      # (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader), #SB : only one check
      (this_or_next|eq, "$g_there_is_no_avaliable_centers", 0),
      (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"), #faction leaders cannot spawn if they have no centers.

      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (this_or_next|eq, "$g_there_is_no_avaliable_centers", 1),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          #(party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
          (eq, ":home_center", ":cur_center"), #I changed it with above line, now if lord is owner of any village its bound walled center is counted as 1000. Better this way. ozan-18.01.09
          (eq, "$g_there_is_no_avaliable_centers", 0),

          (val_sub, ":random_center", 1000),
        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


  #script_cf_select_random_walled_center_with_faction_and_less_strength_priority:
  # This script selects a random center in range [centers_begin, centers_end)
  # such that faction of the town is equal to given_faction
  # INPUT:
  # arg1 = faction_no
  # arg2 = preferred_center_no

  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no (Can fail)
  ("cf_select_random_walled_center_with_faction_and_less_strength_priority",
    [
      (store_script_param, ":faction_no", 1),
      (store_script_param, ":preferred_center_no", 2),
      (assign, ":result", -1),
      # First count num matching spawn points
      (assign, ":no_centers", 0),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_add, ":no_centers", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_add, ":no_centers", 99),
        (try_end),
##        (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##        (assign, ":strength", reg0),
##        (lt, ":strength", 80),
##        (store_sub, ":strength", 100, ":strength"),
##        (val_div, ":strength", 20),
##        (val_add, ":no_centers", ":strength"),
      (try_end),
      (gt, ":no_centers", 0), #Fail if there are no centers
      (store_random_in_range, ":random_center", 0, ":no_centers"),
      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (eq, ":cur_faction", ":faction_no"),
        (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
        (val_sub, ":random_center", 1),
        (try_begin),
          (eq, ":cur_center", ":preferred_center_no"),
          (val_sub, ":random_center", 99),
        (try_end),
##        (try_begin),
##          (call_script, "script_party_calculate_regular_strength", ":cur_center"),
##          (assign, ":strength", reg0),
##          (lt, ":strength", 80),
##          (store_sub, ":strength", 100, ":strength"),
##          (val_div, ":strength", 20),
##          (val_sub, ":random_center", ":strength"),
##        (try_end),
        (lt, ":random_center", 0),
        (assign, ":result", ":cur_center"),
      (try_end),
      (assign, reg0, ":result"),
  ]),


  #script_cf_select_random_town_at_peace_with_faction:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is friendly to given_faction
  # INPUT:
  # arg1 = faction_no

  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_at_peace_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),
      # First count num matching towns
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range,":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation,":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  #script_cf_select_random_town_at_peace_with_faction_in_trade_route
  # INPUT:
  # arg1 = town_no
  # arg2 = faction_no

  #OUTPUT:
  # This script may return false if there is no matching town.
  # reg0 = town_no
  ("cf_select_random_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
      (assign, ":result", -1),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (eq, ":result", -1),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),
        (val_sub, ":random_town", 1),
        (lt, ":random_town", 0),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),



	#the following is a very simple adjustment - it measures the difference in prices between two towns
	#all goods are weighted equally except for luxuries
	#it does not take into account the prices of the goods, nor cargo capacity
	#to do that properly, a merchant would have to virtually fill his baggage, slot by slot, for each town
	#i also found that one needed to introduce demand inelasticity -- prices should vary a lot for grain,  relatively little for iron
    ##diplomacy start+
	#
    #Added a third parameter, the caravan party, for use in distance calculations and perhaps
	#other things in the future.  This may be -1, in which case the script attempts to find a
	#general answer without referring to any specific attributes.  It may also be a town,
	#in which case its position is used for distance calculations.
	##diplomacy end+
	("cf_select_most_profitable_town_at_peace_with_faction_in_trade_route",
    [
      (store_script_param, ":town_no", 1),
      (store_script_param, ":faction_no", 2),
	  ##diplomacy start+
	  (store_script_param, ":perspective_party", 3),
	  ##diplomacy end+

      (assign, ":result", -1),
	  (assign, ":best_town_score", 0),
      (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

	  ##diplomacy start+
	  # If economics changes are enabled, the caravan may also take into account the distance
	  # to the destination or bias towards towns of its town faction.
	  (store_random_in_range, ":consider_distance", 0, 2),
	  (store_random_in_range, ":faction_bias", 0, 2),
	  (try_begin),
		(lt, ":perspective_party", 0),
		(assign, ":perspective_party", ":town_no"),
	  (try_end),
      ##diplomacy end+

      (try_for_range, ":cur_slot", slot_town_trade_routes_begin, slot_town_trade_routes_end),
        (party_get_slot, ":cur_town", ":town_no", ":cur_slot"),
        (gt, ":cur_town", 0),

        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (store_relation, ":reln", ":cur_faction", ":faction_no"),
        (ge, ":reln", 0),

		(assign, ":cur_town_score", 0),
		(try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
			(neq, ":cur_goods", "itm_butter"), #Don't count perishables
			(neq, ":cur_goods", "itm_cattle_meat"),
			(neq, ":cur_goods", "itm_chicken"),
			(neq, ":cur_goods", "itm_pork"),

            (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
			(party_get_slot, ":origin_price", ":town_no", ":cur_goods_price_slot"),
			(party_get_slot, ":destination_price", ":cur_town", ":cur_goods_price_slot"),

			(gt, ":destination_price", ":origin_price"),
			(store_sub, ":price_dif", ":destination_price", ":origin_price"),

			(try_begin), #weight luxury goods double
				(this_or_next|eq, ":cur_goods", "itm_spice"),
					(eq, ":cur_goods", "itm_velvet"),
				(val_mul, ":price_dif", 2),
			(try_end),
			(val_add, ":cur_town_score", ":price_dif"),
		(try_end),

##		(try_begin),
##			(eq, "$cheat_mode", 1),
##			(str_store_party_name, s10, ":town_no"),
##			(str_store_party_name, s11, ":cur_town"),
##			(assign, reg3, ":cur_town_score"),
##			(display_message, "str_caravan_in_s10_considers_s11_total_price_dif_=_reg3"),
##		(try_end),

        ##diplomacy start+
		(try_begin),
			#Economic changes must be enabled, or the player must have decided
			#to use mercantilism settings (which expresses a desire to see changes
			#related to that setting applied), or a trade treaty must be in effect.
			(this_or_next|neg|faction_slot_eq, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, 0),
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			#Take into account distance, or treat factions preferentially
			(try_begin),
				#Bias towards own faction
				(ge, ":faction_bias", 1),
				(neq, ":faction_no", ":cur_faction"),

				##The penalty is based on the source faction's mercantilism rating, as well as
				##the other faction's mercantilism rating.
				(faction_get_slot, ":source_mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
				(val_clamp, ":source_mercantilism", -3, 4),
				(faction_get_slot, ":dest_mercantilism", ":cur_faction", dplmc_slot_faction_mercantilism),
				(val_clamp, ":dest_mercantilism", -3, 4),
				##Default (if both factions have mercantilism 0) is a 6% reduction.  Possible range is 0% (least) to 12% (most).
				(store_sub, ":percent", 94, ":source_mercantilism"),
				(val_sub, ":percent", ":dest_mercantilism"),

				(val_mul, ":cur_town_score", ":percent"),
				(val_add, ":cur_town_score", 50),
				(val_div, ":cur_town_score", 100),
			(try_end),
			(try_begin),
				(ge, ":consider_distance", 1),#consider distance
				(store_distance_to_party_from_party, ":dist", ":perspective_party",":cur_town"),
				#Avoid asymptotic effects and undue weighting.
				#Further explanation: What we really care about is time, not distance.
				#It will take time to buy and sell once reaching our destination: halving
				#the distance doesn't double the expected profit per month.
				(val_max, ":dist", 0),
				(val_add, ":dist", 12),
				#Avoid possible problems trying to compare distant towns
				(val_mul, ":cur_town_score", 100),
				(val_div, ":cur_town_score", ":dist"),
			(try_end),
		(try_end),
		##diplomacy end+

		(gt, ":cur_town_score", ":best_town_score"),
		(assign, ":best_town_score", ":cur_town_score"),
		(assign, ":result", ":cur_town"),

	  (try_end),

      (gt, ":result", -1), #Fail if there are no towns

      (assign, reg0, ":result"),

#	  (store_current_hours, ":hour"),
#	  (party_set_slot, ":result", slot_town_caravan_last_visit, ":hour"),

##	  (try_begin),
##		(eq, "$cheat_mode", 1),
##	    (assign, reg3, ":best_town_score"),
##	    (str_store_party_name, s3, ":town_no"),
##	    (str_store_party_name, s4, ":result"),
##	    (display_message, "str_test__caravan_in_s3_selects_for_s4_trade_score_reg3"),
##	  (try_end),

  ]),


  ##  ("cf_select_faction_spawn_point",
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, reg0, ":center_no"),
      (try_end),
  ]),


  # script_get_closest_center_of_faction
  # Input: arg1 = party_no, arg2 = kingdom_no
  # Output: reg0 = center_no (closest)
  ("get_closest_center_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 99999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

  # script_get_closest_walled_center_of_faction
##  # Input: arg1 = party_no
##  # Output: reg0 = center_no
##  ("get_random_enemy_town",
##    [
##      (store_script_param_1, ":party_no"),
##
##      (assign, ":result", -1),
##      (assign, ":total_enemy_centers", 0),
##      (store_faction_of_party, ":party_faction", ":party_no"),
##
##      (try_for_range, ":center_no", towns_begin, towns_end),
##        (store_faction_of_party, ":center_faction", ":center_no"),
##        (neq, ":center_faction", ":party_faction"),
##        (val_add, ":total_enemy_centers", 1),
##      (try_end),
##
##      (try_begin),
##        (eq, ":total_enemy_centers", 0),
##      (else_try),
##        (store_random_in_range, ":random_center", 0, ":total_enemy_centers"),
##        (assign, ":total_enemy_centers", 0),
##        (try_for_range, ":center_no", towns_begin, towns_end),
##          (eq, ":result", -1),
##          (store_faction_of_party, ":center_faction", ":center_no"),
##          (neq, ":center_faction", ":party_faction"),
##          (store_relation, ":party_relation", ":center_faction", ":party_faction"),
##          (le, ":party_relation", -10),
##          (val_add, ":total_enemy_centers", 1),
##          (lt, ":random_center", ":total_enemy_centers"),
##          (assign, ":result", ":center_no"),
##        (try_end),
##      (try_end),
##      (assign, reg0, ":result"),
##  ]),



  # script_find_travel_location
  # Input: arg1 = center_no
  # Output: reg0 = new_center_no (to travel within the same faction)
  ("find_travel_location",
    [
      (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),

        (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (val_add, ":cur_distance", 1),

        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),

      (assign, reg0, -1),

      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),

          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (val_add, ":cur_distance", 1),

          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
  ]),


  # script_get_relation_between_parties
  # This is called more frequently than decide_kingdom_parties_ai
  # Input: none
  # Output: none
  #called from triggers
  ("process_kingdom_parties_ai",
    [
		##diplomacy start+ add support for promoted kingdom ladies
       (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	   ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (gt, ":party_no", 0),
         (call_script, "script_process_hero_ai", ":troop_no"),
       (try_end),
  ]),

  # script_process_hero_ai
  # This is called more frequently than script_decide_kingdom_party_ais
  #Handles sieges, raids, etc -- does not change the party's basic mission.
  # Input: none
  # Output: none
  #called from triggers
  ("process_hero_ai",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (try_begin),
        (party_is_active, ":party_no"),
        (store_faction_of_party, ":faction_no", ":party_no"),
        (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
        (try_begin),
          (eq, ":ai_state", spai_besieging_center),
          (try_begin),
            (party_slot_eq, ":ai_object", slot_center_is_besieged_by, -1),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 3),
            (try_begin),
              (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
              (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":commander_party"),
            (else_try),
              (party_set_slot, ":ai_object", slot_center_is_besieged_by, ":party_no"),
            (try_end),
            (store_current_hours, ":cur_hours"),
            (party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),


            (try_begin),
              (store_faction_of_party, ":ai_object_faction", ":ai_object"),
				 ##diplomacy start+ Handle player is co-ruler of faction
				 (assign, ":is_coruler", 0),
				 (try_begin),
					(eq, ":ai_object_faction", "$players_kingdom"),
					(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
					(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
					(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
					(assign, ":is_coruler", 1),
				 (try_end),
				 (this_or_next|eq, ":is_coruler", 1),
				 ##diplomacy end+
              (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
              (eq, ":ai_object_faction", "fac_player_supporters_faction"),
              (call_script, "script_add_notification_menu", "mnu_notification_center_under_siege", ":ai_object", ":troop_no"),
            (try_end),
            (str_store_party_name_link, s1, ":ai_object"),
            (str_store_troop_name_link, s2, ":troop_no"),
            (str_store_faction_name_link, s3, ":faction_no"),
            #SB : store color of center object
            (faction_get_color, ":color", ":ai_object_faction"),
            (display_log_message, "@{s1} has been besieged by {s2} of {s3}.", ":color"),
            (call_script, "script_village_set_state", ":ai_object", svs_under_siege),
            (assign, "$g_recalculate_ais", 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),
          (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
          (assign, ":selected_village", 0),
          (try_for_range, ":enemy_village_no", villages_begin, villages_end),
            (eq, ":selected_village", 0),
            (store_faction_of_party, ":enemy_village_faction", ":enemy_village_no"),
            (try_begin),
              (party_slot_eq, ":enemy_village_no", slot_town_lord, "trp_player"),
              (store_relation, ":reln", "fac_player_supporters_faction", ":faction_no"),
            (else_try),
              (store_relation, ":reln", ":enemy_village_faction", ":faction_no"),
            (try_end),
            (lt, ":reln", 0),
            (store_distance_to_party_from_party, ":dist", ":enemy_village_no", ":party_no"),
            (lt, ":dist", 15),
            (party_slot_eq, ":enemy_village_no", slot_village_state, svs_normal), #village is not already raided
            #CHANGE STATE TO RAID THIS VILLAGE
            (assign, ":selected_village", ":enemy_village_no"),
          (try_end),
          (try_begin),
            (eq, ":selected_village", 0),
            (is_between, ":ai_object", villages_begin, villages_end),
            (assign, ":selected_village", ":ai_object"),
          (try_end),
          (try_begin),
            (gt, ":selected_village", 0),
            #SB : minimum of 15 in raiding party, although in process_village_raids we calculate actual ratio
            (party_get_num_companions, ":num_troops", ":party_no"),
            (ge, ":num_troops", 15), #about 2 party template of reinforcements
            (call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":selected_village"),
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
              (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
              (faction_set_slot, ":faction_no", slot_faction_ai_object, ":selected_village"),
            (try_end),
            (party_get_position, pos1, ":selected_village"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":selected_village"),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_raiding_around_center),#substate is 1
          (try_begin),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 2),
            (try_begin),
              (party_slot_eq, ":ai_object", slot_village_state, svs_normal),
              (call_script, "script_village_set_state", ":ai_object", svs_being_raided),
              (party_set_slot, ":ai_object", slot_village_raided_by, ":party_no"),
              (try_begin),
                (store_faction_of_party, ":village_faction", ":ai_object"),
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
                (this_or_next|party_slot_eq, ":ai_object", slot_town_lord, "trp_player"),
                (eq, ":village_faction", "fac_player_supporters_faction"),
                (store_distance_to_party_from_party, ":dist", "p_main_party", ":ai_object"),
                (this_or_next|lt, ":dist", 30),
                (party_slot_eq, ":ai_object", slot_center_has_messenger_post, 1),
                (call_script, "script_add_notification_menu", "mnu_notification_village_raid_started", ":ai_object", ":troop_no"),
              (try_end),
            (else_try),
              (party_slot_eq, ":ai_object", slot_village_state, svs_being_raided),
            (else_try),
              #if anything other than being_raided leave
              (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_end),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_retreating_to_center),
          (try_begin),
            (party_get_battle_opponent, ":enemy_party", ":party_no"),
            (ge, ":enemy_party", 0), #we are in a battle! we may be caught in a loop!
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_patrolling_around_center),

          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":ai_object"),
            (lt, ":distance", 6),
            (party_set_slot, ":party_no", slot_party_ai_substate, 1),

	        (party_set_aggressiveness, ":party_no", 8),
	        (party_set_courage, ":party_no", 8),
	        (party_set_ai_initiative, ":party_no", 100),

            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
            (party_set_ai_object, ":party_no", ":ai_object"),
          (try_end),
        (else_try),
          (eq, ":ai_state", spai_holding_center),
        (try_end),
      (try_end),
  ]),

  # script_begin_assault_on_center
  # Input: arg1: faction_no
  # Output: none
  #called from triggers
  ("decide_faction_ai",
  #This handles political issues and faction issues
   [
    (store_script_param_1, ":faction_no"),


    (faction_get_slot, ":old_faction_ai_state", ":faction_no", slot_faction_ai_state),
    (faction_get_slot, ":old_faction_ai_object", ":faction_no", slot_faction_ai_object),
	(faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),


	#Remove marshal if he has become too controversial,, or he has defected, or has been taken prisoner
	(try_begin),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),
		(ge, ":faction_marshal", "trp_player"),

		(store_faction_of_troop, ":marshal_faction", ":faction_marshal"),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":marshal_faction", "$players_kingdom"),
		(try_end),


		(assign, ":player_marshal_is_prisoner", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(eq, "$g_player_is_captive", 1),
			(assign, ":player_marshal_is_prisoner", 1),
		(try_end),


		#High controversy level, or marshal has defected, or is prisoner
		(this_or_next|neq, ":marshal_faction", ":faction_no"),
		(this_or_next|troop_slot_ge, ":faction_marshal", slot_troop_controversy, 80),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),

		(assign, ":few_following_player_campaign", 0),
		(try_begin),
			(eq, ":faction_marshal", "trp_player"),
			(assign, ":vassals_following_player_campaign", 0),
			(gt, "$g_player_days_as_marshal", 1),
			(try_for_range, ":vassal", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":vassal", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, ":vassal_faction", ":vassal"),
				(eq, ":vassal_faction", ":faction_no"),
				(call_script, "script_npc_decision_checklist_troop_follow_or_not", ":vassal"),
				(eq, reg0, 1),
				(val_add, ":vassals_following_player_campaign", 1),
			(try_end),
			(lt, ":vassals_following_player_campaign", 4),
			(assign, ":few_following_player_campaign", 1),
		(try_end),

		#Only remove marshal for controversy if offensive campaign in progress
		(this_or_next|eq, ":old_faction_ai_state", sfai_default),
		(this_or_next|eq, ":old_faction_ai_state", sfai_feast),
		(this_or_next|neq, ":marshal_faction", ":faction_no"),
		(this_or_next|eq, ":few_following_player_campaign", 1),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),

		#No current issue on the agenda
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_political_issue, 0),
		(this_or_next|eq, ":player_marshal_is_prisoner", 1),
			(troop_slot_ge, ":faction_marshal", slot_troop_prisoner_of_party, 0),

		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal

        (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
        (try_begin),
		  (ge, ":old_marshall", 0),
		  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshal, ":old_marshall_party", 0),
        (try_end),

		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
			(call_script, "script_add_notification_menu", "mnu_notification_relieved_as_marshal", 0, 0),
		(else_try),
			(neq, ":old_marshall", "trp_player"),
			(call_script, "script_change_troop_renown", ":old_marshall", 15),
		(try_end),
		(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
		(assign, ":faction_marshal", -1),


		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),

	(else_try),	 #If marshal not present, and not already on agenda, make political issue
		(eq, ":faction_marshal", -1),
		(neg|faction_slot_ge, ":faction_no", slot_faction_political_issue, 1), #This to avoid resetting votes every time

        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(neq, ":faction_no", "fac_player_supporters_faction"),

		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal

		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),


	(else_try),	#If player is marshal, but not part of faction
		(eq, ":faction_marshal", "trp_player"),
		(neq, "$players_kingdom", ":faction_no"),

		(faction_set_slot, ":faction_no", slot_faction_political_issue, 1), #Appointment of marshal
		(store_current_hours, ":hours"),
		(val_max, ":hours", 0),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Appointment of marshal

        (faction_get_slot, ":old_marshall", ":faction_no", slot_faction_marshall),
        (try_begin),
		  (ge, ":old_marshall", 0),
		  (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshal, ":old_marshall_party", 0),
        (try_end),

		(faction_set_slot, ":faction_no", slot_faction_marshall, -1),
		(assign, ":faction_marshal", -1),

		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),

	(try_end),

	#If the faction issue is a center no longer under faction control, remove and reset
	(try_begin),
		(faction_get_slot, ":faction_political_issue", ":faction_no", slot_faction_political_issue),
		(is_between, ":faction_political_issue", centers_begin, centers_end),
		(store_faction_of_party, ":disputed_center_faction", ":faction_political_issue"),
		(neq, ":disputed_center_faction", ":faction_no"),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s4, ":faction_no"),
			(str_store_party_name, s5, ":disputed_center_faction"),
			(display_message, "@{!}DEBUG -- {s4} drops {s5} as issue as it has changed hands"),
		(try_end),

		#Reset political issue
		(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),

	(try_end),


	#Resolve the political issue on the agenda
	(try_begin),
		(faction_slot_ge, ":faction_no", slot_faction_political_issue, 1),
		(neq, ":faction_no", "fac_player_supporters_faction"),

		#Do not switch marshals during a campaign
		(this_or_next|faction_slot_ge, ":faction_no", slot_faction_political_issue, centers_begin),
		(this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_default),
			(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),


		(faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),

		(assign, ":total_lords", 0),
		(assign, ":lords_who_have_voted", 0),
		(assign, ":popular_favorite", -1),

		#Reset number of votes
		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),

		#Tabulate votes

		##diplomacy start+
		(try_begin),#count the player's vote
			(eq, "$players_kingdom", ":faction_no"),
			(ge, "$player_has_homage", 1),
			(troop_get_slot, ":lord_chosen_candidate", "trp_player", slot_troop_stance_on_faction_issue),
      			(gt, ":lord_chosen_candidate", -1),
			#You may notice that I don't count the player for "total_lords" if he was undecided.
			#This is so faction behavior will not be changed from Native if the player did not
			#support anyone.
			(val_add, ":total_lords", 1),
			(val_add, ":lords_who_have_voted", 1),
			(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, 1),
			(assign, ":popular_favorite", ":lord_chosen_candidate"),
		(try_end),
		#add support for promoted kingdom ladies
		(try_for_range, ":voting_lord", heroes_begin, heroes_end),#<- changed active_npcs_begin/end to heroes_begin/end
			(this_or_next|troop_slot_eq, ":voting_lord", slot_troop_occupation, slto_kingdom_hero),
				(is_between, ":voting_lord", active_npcs_begin, active_npcs_end),
		       	#the dead / retired / exiled do not vote
			(neg|troop_slot_ge, ":voting_lord", slot_troop_occupation, slto_retirement),
		##diplomacy end+
			(store_faction_of_troop, ":voting_lord_faction", ":voting_lord"),
			(eq, ":voting_lord_faction", ":faction_no"),
			(val_add, ":total_lords", 1),
			(troop_get_slot, ":lord_chosen_candidate", ":voting_lord", slot_troop_stance_on_faction_issue),
			(gt, ":lord_chosen_candidate", -1),
			(val_add, ":lords_who_have_voted", 1),
			(troop_get_slot, ":total_votes", ":lord_chosen_candidate", slot_troop_temp_slot),
			(val_add, ":total_votes", 1),
			(troop_set_slot, ":lord_chosen_candidate", slot_troop_temp_slot, ":total_votes"),
			(try_begin),
				(gt, ":popular_favorite", -1),
				(troop_get_slot, ":current_winner_votes", ":popular_favorite", slot_troop_temp_slot),
				(gt, ":total_votes", ":current_winner_votes"),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(else_try),
				(eq, ":popular_favorite", -1),
				(assign, ":popular_favorite", ":lord_chosen_candidate"),
			(try_end),
		(try_end),

		#Check to see if enough lords have voted
		(store_div, ":number_required_for_quorum", ":total_lords", 5),
		(val_mul, ":number_required_for_quorum", 4),
		##diplomacy start+
		#Replace number required for quorum, altering it based on the centralization
		#value.  Do the same for the minimum time left on the agenda.
		(faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
		(val_clamp, ":centralization", -3, 4),
		(try_begin),
			#Disable this for now, since NPC kingdoms set their policies randomly.
			(eq, 0, 1),
			(neq, ":centralization", 0),
			(store_sub, ":number_required_for_quorum", 15, ":centralization"),#fully centralized = 12/20 , fully decentralized = 18/20
			(try_begin),
				#If the plutocracy/aristocracy slider is negative, allow it to offset
				#a negative centralization value for the purpose of quorum, on the
				#assumption that part of the "quorum" is accounted for by the influence
				#of merchants.  They do not vote currently, although integrating guild masters
				#and/or village elders into the faction issue system is something to consider
				#for the future.
				(ge, ":number_required_for_quorum", 16),
				(faction_get_slot, ":aristocracy", ":faction_no", dplmc_slot_faction_aristocracy),
				(lt, ":aristocracy", 0),
				(val_clamp, ":aristocracy", -3, 4),
				(val_add, ":number_required_for_quorum", ":aristocracy"),
				(val_max, ":number_required_for_quorum", 15),
			(try_end),
			(val_mul, ":number_required_for_quorum", ":total_lords"),
			(val_div, ":number_required_for_quorum", 20),
		(try_end),
		##diplomacy end+

#		(gt, ":lords_who_have_voted", ":number_required_for_quorum"),

		(store_current_hours, ":hours_on_agenda"),
		(faction_get_slot, ":hours_when_put_on_agenda", ":faction_no", slot_faction_political_issue_time), #Appointment of marshal
		(val_sub, ":hours_on_agenda", ":hours_when_put_on_agenda"),

		##diplomacy start+
		#Before, the maximum number of hours on the agenda for an issue before it became
		#eligible for resolution regardless of quorum was fixed at 120 (five days).
		#Modify this by 16 hours for every point of centralization, for a minimum
		#of 3 days and a maximum of 7 days.
		(assign, ":hours_on_agenda_threshold", 120),
		(try_begin),
			#Disable this for now, since arguably all of the NPC kingdoms are
			#supposed to have fairly similar structures.  From a gameplay perspective,
			#they choose their kingdom policy at random, so enabling this is  probably
			#not going to have good effects, unless more thought is given to balancing
			#centralization/decentralization for NPC kingdoms.
			(eq, 0, 1),
			(store_mul, ":hours_on_agenda_threshold", ":centralization", 16),
			(val_add, ":hours_on_agenda_threshold", 120),
			(try_begin),
				(neq, ":centralization", 0),
			(try_end),
		(try_end),

		#(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
		#	(ge, ":hours_on_agenda", 120),

		(this_or_next|gt, ":lords_who_have_voted", ":number_required_for_quorum"),
			(ge, ":hours_on_agenda", ":hours_on_agenda_threshold"),
		##diplomacy end+

		(try_begin),
			(eq, "$cheat_mode", 1),
			(assign, reg4, ":lords_who_have_voted"),
			(assign, reg5, ":number_required_for_quorum"),
			(assign, reg7, ":hours_on_agenda"),
			(str_store_faction_name, s4, ":faction_no"),
			(display_message, "@{!}DEBUG -- Issue resolution for {s4}: {reg4} votes for a quorum of {reg5}, {reg7} hours on agenda"),
		(try_end),


		(try_begin),
		  (eq, "$cheat_mode", 1),
		  (display_message, "@{!}DEBUG -- Faction resolves political issue"),
		(try_end),


		#Resolve faction political issue
		(assign, ":winning_candidate", -1),

		##diplomacy start+
		#Change "liege overrules lords" check.  The version in Native caused relation death spirals:
		#a lord who has no fiefs becomes unhappy, and since relation is symmetrical, this can result
		#in the liege never granting him fiefs.
		#
		#OLD BEHAVIOR:
#		(else_try)
#			(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
#			(this_or_next|ge, reg0, 10),
#			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, ":popular_favorite"),
#				(troop_slot_eq, ":faction_leader", slot_troop_stance_on_faction_issue, -1),
#
#			(assign, ":winning_candidate", ":popular_favorite"),
#		(else_try),#Lord overrules lords' opinion
#			(gt, ":faction_leader", -1), #not sure why this is necessary
#			(troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
#			(ge, ":liege_choice", -1),
#
#			(assign, ":winning_candidate", ":liege_choice"),
#      (try_end),
#
#      NEW BEHAVIOR
        (troop_get_slot, ":liege_choice", ":faction_leader", slot_troop_stance_on_faction_issue),
		(assign, ":min_liege_relation", 10),#<-- Same as in default
		(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
		(try_begin),
		  (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		  #Alter the minimum for villages and castles, but not towns or the marshall.
		  (this_or_next|is_between, ":issue_on_table", villages_begin, villages_end),
		     (is_between, ":issue_on_table", castles_begin, castles_end),
		  (store_random_in_range, ":min_liege_relation", 0, 16),
		  (val_sub, ":min_liege_relation", 5),#-5 to 10
		(try_end),
		#New override check
		(try_begin),
			#When the player is co-ruler of the kingdom, his/her support for the popular
			#candidate can be sufficient to guarantee success over the opposition of the
			#king/queen.
			(ge, ":faction_leader", 1),
			(eq, "$players_kingdom", ":faction_no"),
			(this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(troop_slot_eq, "trp_player", slot_troop_stance_on_faction_issue, ":popular_favorite"),
			(assign, ":winning_candidate", ":popular_favorite"),
            (else_try),
            	#The leader may overrule a choice he disagrees with, if he dislikes the candidate
            	#sufficiently and has someone else in mind.
            	(ge, ":faction_leader", 1),
			(neq, ":liege_choice", ":popular_favorite"),
			(gt, ":liege_choice", -1),
			(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":liege_choice"),
			(val_min, ":min_liege_relation", reg0),
            	(call_script, "script_troop_get_relation_with_troop", ":faction_leader", ":popular_favorite"),
			(gt, ":min_liege_relation", reg0),
			(assign, reg0, 0),
            	(try_begin),
			   (troop_slot_ge, ":faction_leader", slot_troop_prisoner_of_party, 0),
			   (store_random_in_range, reg0, 0, 2),
			(try_end),
			(try_begin),
			    #The leader would have overruled the choice, but cannot because he is a prisoner.
            		#Print a message letting people know when this happens.
				(eq, reg0, 1),
				(gt, ":popular_favorite", -1),
            		(this_or_next|eq, "$players_kingdom", ":faction_no"),
            		(ge, "$cheat_mode", 1),
            		(str_store_faction_name, s4, ":faction_no"),
            		(str_store_troop_name, s5, ":popular_favorite"),
            		(str_store_troop_name, s0, ":faction_leader"),
            		(try_begin),
            			(eq, ":issue_on_table", 1),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to be the next marshall.  {s0} is indisposed and cannot overrule their choice."),
            		(else_try),
            			(is_between, ":issue_on_table", centers_begin, centers_end),
            			(str_store_party_name, s1, ":issue_on_table"),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to receive {s1}.  {s0} is indisposed and cannot overrule their choice."),
            		(try_end),
            	(try_end),
			(eq, reg0, 0),
			(assign, ":winning_candidate", ":liege_choice"),
			(try_begin),
				#Print a message letting people know when this happens.
				(gt, ":popular_favorite", -1),
				(this_or_next|eq, "$players_kingdom", ":faction_no"),
					(ge, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_troop_name, s5, ":popular_favorite"),
				(str_store_troop_name, s0, ":faction_leader"),
				(try_begin),
					(eq, ":issue_on_table", 1),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to be the next marshall, but {s0} overrules their choice."),
				(else_try),
					(is_between, ":issue_on_table", centers_begin, centers_end),
					(str_store_party_name, s1, ":issue_on_table"),
					(display_message, "@{s5} has the greatest support among the lords of the {s4} to receive {s1}, but {s0} overrules their choice."),
				(try_end),
			(try_end),
		(else_try),
			#No override: use popular candidate
			(assign, ":winning_candidate", ":popular_favorite"),
		(try_end),
		##diplomacy end+

		#Carry out faction decision
		(try_begin), #Nothing happens
			(eq, ":winning_candidate", -1),

		(else_try), #For player, create a menu to accept or refuse
			(eq, ":winning_candidate", "trp_player"),
			(eq, "$players_kingdom", ":faction_no"),
			(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved_for_player", 0, 0),
		(else_try),
			(eq, ":winning_candidate", "trp_player"),
			(neq, "$players_kingdom", ":faction_no"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),

			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
				(this_or_next|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),

		(else_try),	#If candidate is not of winning faction, reset lrod votes
			(store_faction_of_troop, ":winning_candidate_faction", ":winning_candidate"),
			(neq, ":winning_candidate_faction", ":faction_no"),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_faction_name, s4, ":faction_no"),
				(str_store_party_name, s5, ":winning_candidate"),
				(display_message, "@{!}DEBUG -- {s4} drops {s5} as winner, for having changed sides"),
			(try_end),
			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
				(this_or_next|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
					(is_between, ":active_npc", active_npcs_begin, active_npcs_end),
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),

		(else_try), #Honor awarded to another
			(faction_get_slot, ":issue_on_table", ":faction_no", slot_faction_political_issue),
			(try_begin), #A marshalship awarded to another
				(eq, ":issue_on_table", 1),
				(is_between, ":winning_candidate", active_npcs_begin, active_npcs_end),

				##diplomacy start+ add support for promoted kingdom ladies
				(this_or_next|is_between, ":winning_candidate", heroes_begin, heroes_end),
					(eq, "$players_kingdom", ":faction_no"),
				(this_or_next|troop_slot_eq, ":winning_candidate", slot_troop_occupation, slto_kingdom_hero),
				##diplomacy end+
				(this_or_next|is_between, ":winning_candidate", active_npcs_begin, active_npcs_end), #Prevents bug in which player given marshaldom of kingdom of which he/she is not a member
					(eq, "$players_kingdom", ":faction_no"),

				(assign, ":faction_marshal", ":winning_candidate"),
			(else_try), #A fief awarded to another
				(is_between, ":issue_on_table", centers_begin, centers_end),

				#If given to the player, resolved above
				(call_script, "script_give_center_to_lord", ":issue_on_table", ":winning_candidate", 0), #Zero means don't add garrison

				#If the player had requested a captured castle
				(try_begin),
					(eq, ":issue_on_table", "$g_castle_requested_by_player"),
					(party_slot_ge, ":issue_on_table", slot_town_lord, active_npcs_begin),
					(store_faction_of_party, ":faction_of_issue", ":issue_on_table"),
					(eq, ":faction_of_issue", "$players_kingdom"),
					(assign, "$g_center_to_give_to_player", ":issue_on_table"),
					(try_begin),
						(troop_get_slot, ":husband", "trp_player", slot_troop_spouse),
						##diplomacy start+ add support for promotede kingdom ladies
						(is_between, ":husband", heroes_begin, heroes_end),
						(this_or_next|troop_slot_eq, ":winning_candidate", slot_troop_occupation, slto_kingdom_hero),
						##diplomacy end+
						(is_between, ":husband", active_npcs_begin, active_npcs_end),
						(eq, "$g_castle_requested_for_troop", ":husband"),
						(neq, ":winning_candidate", ":husband"),
						(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
					(else_try),
						(jump_to_menu, "mnu_requested_castle_granted_to_another"),
					(try_end),
				(try_end),

			(try_end),

			(try_begin),
				(eq, ":faction_no", "$players_kingdom"),
				(call_script, "script_add_notification_menu", "mnu_notification_player_faction_political_issue_resolved", ":issue_on_table", ":winning_candidate"),
			(try_end),

		#Reset political issue
			(faction_set_slot, ":faction_no", slot_faction_political_issue, 0),
			##diplomacy start+ add support for promoted kingdom ladies
			(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
			##diplomacy end+
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":faction_no"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(try_begin),
				(eq, "$players_kingdom", ":faction_no"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),
		(try_end),
	(try_end),

	#Add fief to faction issues
	(try_begin),
		(faction_get_slot, ":faction_issue", ":faction_no", slot_faction_political_issue),
		(le, ":faction_issue", 0),

		(assign, ":landless_lords", 0),
		(assign, ":unassigned_centers", 0),
		(assign, ":first_unassigned_center_found", 0),

		(troop_set_slot, "trp_player", slot_troop_temp_slot, 0),
		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
		(try_end),

		(try_for_range, ":center", centers_begin, centers_end),
			(store_faction_of_party, ":center_faction", ":center"),
			(eq, ":center_faction", ":faction_no"),

			(party_get_slot, ":town_lord", ":center", slot_town_lord),

			(try_begin),
				(lt, ":town_lord", 0),
				(val_add, ":unassigned_centers", 1),
				(try_begin),
					(eq, ":first_unassigned_center_found", 0),
					(assign, ":first_unassigned_center_found", ":center"),
				(try_end),
			(else_try),
				(troop_set_slot, ":town_lord", slot_troop_temp_slot, 1),
			(try_end),
		(try_end),

		(store_add, ":landless_lords_plus_unassigned_centers", ":landless_lords", ":unassigned_centers"),
		(ge, ":landless_lords_plus_unassigned_centers", 2),

		(faction_set_slot, ":faction_no", slot_faction_political_issue, ":first_unassigned_center_found"),
		(store_current_hours, ":hours"),
		(faction_set_slot, ":faction_no", slot_faction_political_issue_time, ":hours"), #Fief put on agenda

		##diplomacy start+ add support for promoted kingdom ladies
		(try_for_range, ":active_npc", heroes_begin, heroes_end),#<- change active_npcs to heroes
		##diplomacy end+
			(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
			(eq, ":active_npc_faction", ":faction_no"),
			(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
		(try_end),
		(try_begin),
			(eq, "$players_kingdom", ":faction_no"),
			(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
		(try_end),
	(try_end),


    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
       #(assign, ":marshall_changed", 1),
       (eq, "$players_kingdom", ":faction_no"),
       (str_store_troop_name_link, s1, ":faction_marshal"),
       (str_store_faction_name_link, s2, ":faction_no"),
       (display_message, "@{s1} is the new marshal of {s2}."),
       (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
    (try_end),

    (try_begin), #If the marshal is changed
       (neg|faction_slot_eq, ":faction_no", slot_faction_marshall, ":faction_marshal"),
	   (gt, ":faction_marshal", -1),
       (call_script, "script_appoint_faction_marshall", ":faction_no", ":faction_marshal"),
    (try_end),

	#DO FACTION AI HERE
	(try_begin),
		(eq, ":faction_no", "$players_kingdom"),
		(eq, ":faction_marshal", "trp_player"),
	    (assign, ":faction_ai_decider", "trp_player"),
	(else_try),
		##diplomacy start+ add support for promoted kingdom ladies
		(is_between, ":faction_marshal", heroes_begin, heroes_end),
		#(this_or_next|troop_slot_eq, ":faction_marshal", slot_troop_occupation, slto_kingdom_hero),
		#(is_between, ":faction_marshal", active_npcs_begin, active_npcs_end),
		##diplomacy end+
		(assign, ":faction_ai_decider", ":faction_marshal"),
	(else_try),
		(faction_get_slot, ":faction_ai_decider", ":faction_no", slot_faction_leader),
	(try_end),

    (call_script, "script_npc_decision_checklist_faction_ai_alt",  ":faction_ai_decider"),
    (assign, ":new_strategy", reg0),
    (assign, ":new_object", reg1),

    #new ozan
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       ##diplomacy begin
       #native script error bug fix when no marshal
       (gt, ":faction_marshal", -1),
       ##diplomacy end
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
       (assign, "$g_gathering_new_started", 1),
       (call_script, "script_npc_decision_checklist_party_ai", ":faction_marshal"), #This handles AI for both marshal and other parties
       (call_script, "script_party_set_ai_state", ":marshal_party", reg0, reg1),
       (assign, "$g_gathering_new_started", 0),
    (else_try),
       #check if marshal arrived his target city during active gathering

       #for now i disabled below lines because after always/active gathering armies become very large.
       #in current style marshal makes active gathering only at first, it travels to a city and waits there.

       (eq, ":new_strategy", ":old_faction_ai_state"),
       (eq, ":new_strategy", sfai_gathering_army),
       (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
       ##diplomacy begin
       #native script error bug fix when no marshal
       (gt, ":faction_marshal", -1),
       ##diplomacy end
       (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
       ##diplomacy start+ 2011-06-08 Fix bug when the marshall leaded party is set negative!
       (gt, ":marshal_party", -1),
       ##diplomacy end+
       (party_get_slot, ":party_ai_object", ":marshal_party", slot_party_ai_object),
       (ge, ":party_ai_object", 0),
       (ge, ":marshal_party", 0),
       (party_is_active, ":marshal_party"),
       (party_is_active, ":party_ai_object"),
       (store_distance_to_party_from_party, ":dist", ":marshal_party", ":party_ai_object"),
       (le, ":dist", 5),
       (party_set_slot, ":marshal_party", slot_party_ai_object, -1),
    (try_end),
     #end ozan

     #The following logic is mostly transplanted to the new decision_checklist
     #Decision_checklist is used because I want to be able to reproduce the logic for strings
     #(call_script, "script_old_faction_ai"),
     #ozan - I collected all comment-out lines in here (faction ai script) and placed most bottom of scripts.py to avoid confusing.

    (faction_set_slot, ":faction_no", slot_faction_ai_state, ":new_strategy"),
    (faction_set_slot, ":faction_no", slot_faction_ai_object, ":new_object"),

    (call_script, "script_update_report_to_army_quest_note", ":faction_no", ":new_strategy", ":old_faction_ai_state"),


    (try_begin),
       (neq, ":old_faction_ai_state", sfai_feast),     #dckplmc
       (eq, ":new_strategy", sfai_feast),

       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_last_feast_start_time, ":hours"), #new

       (try_begin),
         (eq, "$g_player_eligible_feast_center_no", ":new_object"),
         (assign, "$g_player_eligible_feast_center_no", -1), #reset needed
       (try_end),
       (try_begin),
         (is_between, ":new_object", towns_begin, towns_end),
         (party_set_slot, ":new_object", slot_town_has_tournament, 1), #dckplmc - was 2
       (try_end),
    (try_end),

     #Change of strategy
    (try_begin),
       (neq, ":new_strategy", ":old_faction_ai_state"),

       (try_begin),
         (ge, "$cheat_mode", 1),
         (str_store_faction_name, s5, ":faction_no"),
         (display_message, "str_s5_decides_s14"),
       (try_end),

       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_ai_current_state_started, ":hours"),

       #Feast ends
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_feast),
         (call_script, "script_faction_conclude_feast", ":faction_no", ":old_faction_ai_object"),
       (try_end),


       #Feast begins
       (try_begin),
         (eq, ":new_strategy", sfai_feast),
         (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),

##         (str_store_faction_name, s1, ":faction_no"),
##         (str_store_party_name, s2, ":faction_object"),
##         (display_message, "str_lords_of_the_s1_gather_for_a_feast_at_s2"),

         (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),

         (try_begin),
           (check_quest_active, "qst_wed_betrothed"),

           (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":feast_host"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_wedding_day", ":feast_host", ":faction_object"),
		 (else_try),
           (check_quest_active, "qst_wed_betrothed_female"),

           (quest_get_slot, ":player_betrothed", "qst_wed_betrothed", slot_quest_giver_troop),
		   (store_faction_of_troop, ":player_betrothed_faction", ":player_betrothed"),
		   (eq, ":player_betrothed_faction", ":faction_no"),
           (neg|quest_slot_ge, "qst_wed_betrothed", slot_quest_expiration_days, 362),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (else_try),
           (eq, "$players_kingdom", ":faction_no"),
           (troop_slot_ge, "trp_player", slot_troop_renown, 150),


           (party_get_slot, ":feast_host", ":faction_object", slot_town_lord),
           (call_script, "script_add_notification_menu", "mnu_notification_player_kingdom_holds_feast", ":feast_host", ":faction_object"),
         (try_end),
       (try_end),


       #Offensive begins
       (try_begin),
         (eq, ":old_faction_ai_state", sfai_gathering_army),
         (is_between, ":new_strategy", sfai_attacking_center, sfai_feast),
		 (try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":faction_no"),
			(display_message, "str_s5_begins_offensive"),
		 (try_end),

         #Appoint screening party
         (try_begin),
           (assign, ":total_lords_participating", 0),
           (assign, ":best_screening_party", -1),
           (assign, ":score_to_beat", 30), #closest in size to 50
           (troop_get_slot, ":faction_marshal_party", ":faction_marshal", slot_troop_leaded_party),
           (party_is_active, ":faction_marshal_party"),

           ##diplomacy start+
    #           (try_for_range, ":screen_leader", active_npcs_begin, active_npcs_end),##OLD
           (try_for_range, ":screen_leader", heroes_begin, heroes_end),##NEW
           ##diplomacy end+
             (store_faction_of_troop, ":screen_leader_faction", ":screen_leader"),
             (eq, ":screen_leader_faction", ":faction_no"),

             (troop_get_slot, ":screening_party", ":screen_leader", slot_troop_leaded_party),
             ##diplomacy start+ Guard against things such as the party being 0 (p_main_party)
             (gt, ":screening_party", 0),
             ##diplomacy end+
             (party_is_active, ":screening_party"),
             (party_slot_eq, ":screening_party", slot_party_ai_state, spai_accompanying_army),
             (party_slot_eq, ":screening_party", slot_party_ai_object, ":faction_marshal_party"),
             (val_add, ":total_lords_participating", 1),

		     (try_begin),
			  (ge, "$cheat_mode", 1),
		      (str_store_party_name, s4, ":screening_party"),
			  (display_message, "@{!}DEBUG -- {s4} participates in offensive"),
		     (try_end),


             (store_party_size_wo_prisoners, ":screening_party_score", ":screening_party"),
             (val_sub, ":screening_party_score", 50),
             (val_abs, ":screening_party_score"),


             (lt, ":screening_party_score", ":score_to_beat"),

             #set party and score
             (assign, ":best_screening_party", ":screening_party"),
             (assign, ":score_to_beat", ":screening_party_score"),
           (try_end),

           (gt, ":total_lords_participating", 2),
           (party_is_active, ":best_screening_party"),
           (party_is_active, ":faction_marshal_party"),
           (call_script, "script_party_set_ai_state", ":best_screening_party", spai_screening_army, ":faction_marshal_party"),
           (try_begin),
             (ge, "$cheat_mode", 1),
             (str_store_party_name, s4, ":best_screening_party"),
             (display_message, "@{!}DEBUG -- {s4} chosen as screen"),
           (try_end),
           #after this - dialogs on what doing, npc_decision_checklist
         (try_end),

       #Offensive concludes
       (else_try),
	     (store_current_hours, ":hours"),
         (this_or_next|eq, ":old_faction_ai_state", sfai_gathering_army),
         (this_or_next|eq, ":old_faction_ai_state", sfai_attacking_center),
         (this_or_next|eq, ":old_faction_ai_state", sfai_raiding_village),
		 #(this_or_next|eq, ":old_faction_ai_state", sfai_attacking_enemies_around_center),
			(eq, ":old_faction_ai_state", sfai_attacking_enemy_army),

         (this_or_next|eq, ":new_strategy", sfai_default),
			(eq, ":new_strategy", sfai_feast),

         (call_script, "script_check_and_finish_active_army_quests_for_faction", ":faction_no"),
         (faction_set_slot, ":faction_no", slot_faction_last_offensive_concluded, ":hours"),
        (try_end),
    (try_end),

    (try_begin),
       (eq, "$players_kingdom", ":faction_no"),
       (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
       (check_quest_active, "qst_join_siege_with_army"),
       (call_script, "script_abort_quest", "qst_join_siege_with_army", 0),
    (try_end),

    (try_begin),
       #old condition to rest, I changed below part - ozan, to rest (a faction's old strategy should be feast or default) and (a faction's new strategy should be feast or default)
       #(this_or_next|eq, ":new_strategy", sfai_default),
       #(this_or_next|eq, ":new_strategy", sfai_feast),
       #(this_or_next|eq, ":old_faction_ai_state", sfai_default),
       #(eq, ":old_faction_ai_state", sfai_feast),

       #new condition to rest, (a faction's new strategy should be feast or default) and (":hours_at_current_state" > 20)
       (this_or_next|eq, ":new_strategy", sfai_default),
		(eq, ":new_strategy", sfai_feast),

       (store_current_hours, ":hours_at_current_state"),
       (faction_get_slot, ":current_state_started", ":faction_no", slot_faction_ai_current_state_started),
       (val_sub, ":hours_at_current_state", ":current_state_started"),
       (ge, ":hours_at_current_state", 18), #Must have at least 18 hours to reset

       (store_current_hours, ":hours"),
       (faction_set_slot, ":faction_no", slot_faction_ai_last_rest_time, ":hours"),
    (try_end),
  ]),

  # script_check_and_finish_active_army_quests_for_faction
  # Input: none
  # Output: none
  ("init_ai_calculation",
    [
      ##diplomacy start+
	  #(assign, ":real_party_strength"),
	  ##If terrain advantage is enabled, use it to calculate troop strengths.
      (try_begin),
         (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),

		 #First update all lords
		 (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
			(gt, ":cur_party", 0),
            (party_is_active, ":cur_party"),

		    (party_get_current_terrain, ":terrain_code", ":cur_party"),

			(party_get_attached_to, ":attachment", ":cur_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength
         (try_end),

		 #Then update player
		 (party_get_current_terrain, ":terrain_code", "p_main_party"),

		 (party_get_attached_to, ":attachment", "p_main_party"),
			(try_begin),
				(ge, ":attachment", 0),
				(is_between, ":attachment", centers_begin, centers_end),
				(assign, ":terrain_code", dplmc_terrain_code_siege),#siege constant defined in header_terrain_types.py
			(try_end),

		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1), #will update slot_party_cached_strength

         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
		    #Update with walled center alterations
            (call_script, "script_dplmc_party_calculate_strength_in_terrain", ":cur_center", -2, 0, 1),
         (try_end),
      (else_try),
	   #The old behavior, unchanged:
         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
            (party_is_active, ":cur_party"),
            (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
         (try_end),
         (call_script, "script_party_calculate_strength", "p_main_party", 0), #will update slot_party_cached_strength
         (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
            (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
         (try_end),
      (try_end),
      ##diplomacy end+

      (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_center"),
      (try_end),

      (try_for_range, ":cur_troop", heroes_begin, heroes_end),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (gt, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),
        (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", ":cur_troop_party"),
      (try_end),
      (call_script, "script_party_calculate_and_set_nearby_friend_enemy_follower_strengths", "p_main_party"),
      ]),


  # script_recalculate_ais
  # Input: none
  # Output: none

  #When a lord changes factions
  #When a center changes factions
  #When a center is captured
  #When a marshal is defeated
  #Every 23 hours
    ("recalculate_ais",
    [
      (call_script, "script_init_ai_calculation"),

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (assign, reg8, ":faction_no"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        #(neg|faction_slot_eq, ":faction_no",  slot_faction_marshall, "trp_player"),
        (call_script, "script_decide_faction_ai", ":faction_no"),
      (try_end),

	  ##diplomacy start+ add support for promoted kingdom ladies
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),#<- change active_npcs to heroes
	  ##diplomacy end+
        (store_troop_faction, ":faction_no", ":troop_no"),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),
    ]),

  # script_calculate_troop_ai
  # Input: troop_no
  # Output: none
  #Now called directly from scripts
  ("calculate_troop_ai",
    [
      (store_script_param, ":troop_no", 1),

      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
		(party_is_active, ":party_no"),
		##diplomacy start+
		#Testing notifications
		(party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
		#(party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
		##diplomacy end+
		(call_script, "script_npc_decision_checklist_party_ai", ":troop_no"), #This handles AI for both marshal and other parties
		(call_script, "script_party_set_ai_state", ":party_no", reg0, reg1),
		##diplomacy start+
		#Notify the player of changes to spouse and affiliates
		(party_get_slot, ":new_ai_state", ":party_no", slot_party_ai_state),
		(party_get_slot, ":new_ai_object", ":party_no", slot_party_ai_object),

		##(this_or_next|neq, ":old_ai_object", ":new_ai_object",
		(neq, ":old_ai_state", ":new_ai_state"),
		(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_LOW),
		#(assign, reg0, 0),
		#(try_begin),
		#	(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		#	(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
		#	(assign, reg0, 1),
		##(else_try),
		##	(store_faction_of_troop, ":troop_faction", ":troop_no"),
		##	(is_between,
		##(else_try),
		#	(call_script, "script_dplmc_is_affiliated_family_member", ":troop_no"),
		#(try_end),
		(call_script, "script_dplmc_store_troop_is_eligible_for_affiliate_messages", ":troop_no"),
		(gt, reg0, 0),


		#Some of these have non-obvious secondary uses.
		#xxx TODO: Later, I should go and verify all of them.
		(str_store_troop_name, s0, ":troop_no"),

		(try_begin),
			(eq, ":new_ai_state", spai_besieging_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is laying siege to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_patrolling_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is patrolling around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_raiding_around_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is raiding around {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_engaging_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is engaging {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_accompanying_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is accompanying {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_screening_army),
			(gt, ":new_ai_object", -1),
			(party_is_active, ":new_ai_object"),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is screening the advance of {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_trading_with_town),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is trading with {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_retreating_to_center),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is retreating to {s1}."),
		(else_try),
			(eq, ":new_ai_state", spai_visiting_village),
			(is_between, ":new_ai_object", centers_begin, centers_end),
			(str_store_party_name, s1, ":new_ai_object"),
			(display_message, "@{s0} is visiting {s1}."),
		(try_end),
		#Make it obvious that something went wrong if something tries to use the registers
		(str_store_string, s0, "str_ERROR_string"),
		(str_store_string, s1, "str_ERROR_string"),
		##diplomacy end+
      (try_end),
    ]),

  # script_diplomacy_start_peace_between_kingdoms
	# DECISION CHECKLISTS (OCT 14)
	# I was thinking of trying to convert as much AI decision-making as possible to the checklist format
	# While outcomes are not as nuanced and varied as a random decision using weighted chances for each outcoms,
	# the checklist has the advantage of being much more transparent, both to developers and to players
	# The checklist can yield a string (standardized to s14) which explains the rationale for the decision
	# When the script yields a yes/no/maybe result, than that is standardized from -3 to +3
    # INPUT: troop_no
    # OUTPUT: none
	("npc_decision_checklist_party_ai",
	[
	#this script can replace decide_kingdom_hero_ai and decide_kingdom_hero_ai_follow_or_not
	#However, it does not contain script_party_set_ai_state

	(store_script_param, ":troop_no", 1),

	(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
    #(party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
    #(store_div, ":min_strength_behind", ":our_strength", 2),
    #(party_get_slot, ":our_follower_strength", ":party_no", slot_party_follower_strength),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, "$g_talk_troop", ":troop_no"),
    (try_end),

    (store_troop_faction, ":faction_no", ":troop_no"),
    ##diplomacy start+
    #Get the centralization value for use below.  It should be a value in [-3,3].
    #A centralization value of 0 should not result in any behavior change.
    (try_begin),
       #If the player altered the kingdom policy, always apply its effects to
       #the AI of his kingdom's lords.
       (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
       (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
       (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
       (val_clamp, ":centralization", -3, 4),
    (else_try),
       #Currently, do not apply centralization to the AI for NPC kingdoms, since
       #NPC rulers set their policies randomly and do not gain the same monthly
       #relation bonuses/penalties from centralization that the player does.
       (assign, ":centralization", 0),
    (try_end),
    ##diplomacy end+

    (try_begin),
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_string, s15, "str__i_must_attend_to_this_matter_before_i_worry_about_the_affairs_of_the_realm"),
    (try_end),

    #find current center
    (party_get_attached_to, ":cur_center_no", ":party_no"),
    (try_begin),
      (lt, ":cur_center_no", 0),
      (party_get_cur_town, ":cur_center_no", ":party_no"),
    (try_end),
    (assign, ":besieger_party", -1),
    (try_begin),
      (neg|is_between, ":cur_center_no", centers_begin, centers_end),
      (assign, ":cur_center_no", -1),
    (else_try),
      (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
      (try_begin),
        (neg|party_is_active, ":besieger_party"),
        (assign, ":besieger_party", -1),
      (try_end),
    (try_end),

    #party_count
    (call_script, "script_party_count_fit_for_battle", ":party_no"),
    (assign, ":party_fit_for_battle", reg0),
    (call_script, "script_party_get_ideal_size", ":party_no"),
    (assign, ":ideal_size", reg0),
    (store_mul, ":party_strength_as_percentage_of_ideal", ":party_fit_for_battle", 100),
    (val_div, ":party_strength_as_percentage_of_ideal", ":ideal_size"),
    (try_begin),
      (faction_slot_eq, ":faction_no", slot_faction_num_towns, 0),
      (faction_slot_eq, ":faction_no", slot_faction_num_castles, 0),
      (assign, ":party_ratio_of_prisoners", 0), #do not let prisoners have an effect on ai calculation
    (else_try),
      (party_get_num_prisoners, ":num_prisoners", ":party_no"),
      (val_max, ":party_fit_for_battle", 1), #avoid division by zero error
      (store_div, ":party_ratio_of_prisoners", ":num_prisoners", ":party_fit_for_battle"),
    (try_end),

	(assign, ":faction_is_at_war", 0),
	(try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),
	  (store_relation, ":relation", ":faction_no", ":kingdom"),
	  (lt, ":relation", 0),
	  (assign, ":faction_is_at_war", 1),
	(try_end),

	(assign, ":operation_in_progress", 0),
	(try_begin),
	  (this_or_next|party_slot_eq, ":party_no", slot_party_ai_state, spai_raiding_around_center),
	  (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),

	  (party_get_slot, ":target_center", ":party_no", slot_party_ai_object),
	  (is_between, ":target_center", centers_begin, centers_end),

	  (store_faction_of_party, ":target_center_faction", ":target_center"),
	  (store_relation, ":relation", ":faction_no", ":target_center_faction"),
	  (lt, ":relation", 0),

	  (store_distance_to_party_from_party, ":distance", ":party_no", ":target_center"),
	  (lt, ":distance", 10),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_under_siege),
	  (this_or_next|party_slot_eq, ":target_center", slot_village_state, svs_normal),
	  (party_slot_eq, ":target_center", slot_village_state, svs_being_raided),

	  (assign, ":operation_in_progress", 1),
	(try_end),

	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),

    (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
    (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),

	(party_get_slot, ":party_cached_strength", ":party_no", slot_party_cached_strength),

	(store_current_hours, ":hours_since_last_rest"),
	(party_get_slot, ":last_rest_time", ":party_no", slot_party_last_in_any_center),
	(val_sub, ":hours_since_last_rest", ":last_rest_time"),

	(store_current_hours, ":hours_since_last_home"),
	(party_get_slot, ":last_home_time", ":party_no", slot_party_last_in_home_center),
	(val_sub, ":hours_since_last_home", ":last_home_time"),

	(store_current_hours, ":hours_since_last_combat"),
	(party_get_slot, ":last_combat_time", ":party_no", slot_party_last_in_combat),
	(val_sub, ":hours_since_last_combat", ":last_combat_time"),

	(store_current_hours, ":hours_since_last_courtship"),
	(party_get_slot, ":last_courtship_time", ":party_no", slot_party_leader_last_courted),
	(val_sub, ":hours_since_last_courtship", ":last_courtship_time"),

    (troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),
    (store_mod, ":aggressiveness", ":temp_ai_seed", 73), #To derive the
    (try_begin),
      (eq, ":troop_reputation", lrep_martial),
      (val_add, ":aggressiveness", 27),
    (else_try),
      (neq, ":troop_reputation", lrep_debauched),
      (neq, ":troop_reputation", lrep_quarrelsome),
      (val_add, ":aggressiveness", 14),
    (try_end),

    (try_begin),
      (gt, ":aggressiveness", ":hours_since_last_combat"),
      (val_add, ":aggressiveness", ":hours_since_last_combat"),
      (val_div, ":aggressiveness", 2),
    (try_end),

    (try_begin),
      (eq, "$cheat_mode", 1), #100
      (eq, ":troop_no", "$g_talk_troop"),
      (str_store_troop_name, s4, ":troop_no"),
      (assign, reg3, ":hours_since_last_rest"),
      (assign, reg4, ":hours_since_last_courtship"),
      (assign, reg5, ":hours_since_last_combat"),
      (assign, reg6, ":hours_since_last_home"),
      (assign, reg7, ":aggressiveness"),
      #(display_message, "@{!}{s4}: hours since rest {reg3}, courtship {reg4}, combat {reg5}, home {reg6}, aggressiveness {reg7}"),
    (try_end),

	##I am inspecting an estate (use slot_center_npc_volunteer_troop_amount)

	(str_store_string, s17, "str_the_other_matter_took_precedence"),

	(assign, ":do_only_collecting_rents", 0),

	#Wait in current city (dangerous to travel with less (<=10) men)
	(try_begin),
      #NOTE : I added also this condition to very top of list. Because if this condition does not exists in top then a bug happens.
      #Bug is about alone wounded lords without any troop near him travels between cities, sometimes it want to return his home city
      #to collect reinforcements, sometimes it want to patrol ext, but his party is so weak even without anyone. So we sometimes see
      #(0/1) parties in map with only one wounded lord inside. Because after wars completely defeated lords spawn again in a walled center
      #in 48 hours periods (by codes in module_simple_trigers). He spawns with only wounded himself. Then he should wait in there for
      #a time to collect new men to his (0/1) party. If a lord is the only one in his party and if he is at any walled center already then he
      #should stay where he is. He should not travel to anywhere because of any reason. If he is the only one and he is wounded and
      #he is not in any walled center this means this situation happens because of one another bug, because any lord cannot be out of
      #walled centers with wounded himself only. So I am adding this condition below.

      #SUMMARY : If lord has not got enought troops (<10 || <10%) with himself and he is currently at a walled center he should not leave
      #his current center because of any reason.

      (ge, ":cur_center_no", 0),

      (this_or_next|le, ":party_fit_for_battle", 10),
      (le, ":party_strength_as_percentage_of_ideal", 30),

      (assign, ":action", spai_holding_center),
      (assign, ":object", ":cur_center_no"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	    (str_store_string, s16, "str_i_need_to_raise_some_men_before_attempting_anything_else"),
	  (try_end),

	#Stand in a siege
	(else_try),
	  (gt, ":besieger_party", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_cannot_leave_this_fortress_now_as_it_is_under_siege"),
	    (str_store_string, s16, "str_after_all_we_are_under_siege"),
	  (try_end),

	#Continue retreat to walled center
	(else_try),
	  (eq, ":old_ai_state", spai_retreating_to_center),
	  (neg|party_is_in_any_town, ":party_no"),

	  (ge, ":old_ai_object", 0),
	  (party_is_active, ":old_ai_object"),

	  (store_faction_of_party, ":retreat_center_faction", ":old_ai_object"),
	  (eq, ":faction_no", ":retreat_center_faction"),

	  (assign, ":action", spai_retreating_to_center),
	  (assign, ":object", ":old_ai_object"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_not_strong_enough_to_face_the_enemy_out_in_the_open"),
	    (str_store_string, s16, "str_i_should_probably_seek_shelter_behind_some_stout_walls"),
	  (try_end),

	#Stand by in current center against enemies
	(else_try),
	  (is_between, ":cur_center_no", walled_centers_begin, walled_centers_end),

	  (party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  (party_get_slot, ":enemy_strength_in_area", ":cur_center_no", slot_center_sortie_enemy_strength),
	  (ge, ":enemy_strength_in_area", 50),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":cur_center_no"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_enemies_are_reported_to_be_nearby_and_we_should_stand_ready_to_either_man_the_walls_or_sortie_out_to_do_battle"),
	    (str_store_string, s16, "str_the_enemy_is_nearby"),
	  (try_end),

	#As the marshall, lead faction campaign
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (str_clear, s15), #Does not say that overrides faction orders
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),

	  (party_set_ai_initiative, ":party_no", 10),

	  #new ozan added - active gathering
	  #this code will allow marshal to travel around cities while gathering army if currently collected are less than 60%.
	  #By ratio increases travel distances become less. Travels will be only points around walled centers.
	  (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
	  (assign, ":travel_target", ":old_ai_object"),

      (call_script, "script_find_center_to_defend", ":troop_no"),
	  (assign, ":most_threatened_center", reg0),
	  (assign, ":travel_target_new_assigned", 0),

      (try_begin),
        (lt, ":old_ai_object", 0),

        (store_random_in_range, ":random_value", 0, 8), #to eanble marshal to wait sometime during active gathering
        (this_or_next|eq, "$g_gathering_new_started", 1),
        (eq, ":random_value", 0),

        (assign, ":vassals_already_assembled", 0),
        (assign, ":total_vassals", 0),
        (try_for_range, ":lord", active_npcs_begin, active_npcs_end),
          (store_faction_of_troop, ":lord_faction", ":lord"),
          (eq, ":lord_faction", ":faction_no"),
          (troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
          (party_is_active, ":led_party"),
          (val_add, ":total_vassals", 1),

          (party_slot_eq, ":led_party", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":led_party", slot_party_ai_object, ":party_no"),

          (party_is_active, ":party_no"),
          (store_distance_to_party_from_party, ":distance_to_marshal", ":led_party", ":party_no"),
          (lt, ":distance_to_marshal", 15),
          (val_add, ":vassals_already_assembled", 1),
        (try_end),

        (assign, ":ratio_of_vassals_assembled", -1),
        (try_begin),
          (gt, ":total_vassals", 0),
          (store_mul, ":ratio_of_vassals_assembled", ":vassals_already_assembled", 100),
          (val_div, ":ratio_of_vassals_assembled", ":total_vassals"),
        (try_end),

        (try_begin),
          #if more than 35% of vassals already collected do not make any more active gathering, just hold and wait last vassals to participate.
          (le, ":ratio_of_vassals_assembled", 35),

          (assign, ":best_center_to_travel", ":most_threatened_center"),

          (try_begin),
            (eq, "$g_gathering_new_started", 1),

            (assign, ":minimum_distance", 100000),
            (try_for_range, ":center_no", centers_begin, centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"), #200
              (try_begin),
                (neq, ":center_no", ":most_threatened_center"),
                (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                (lt, ":dist", ":minimum_distance"),
                (assign, ":minimum_distance", ":dist"),
                (assign, ":best_center_to_travel", ":center_no"),
              (try_end),
            (try_end),
          (else_try),
            #active gathering
            (assign, ":max_travel_distance", 150),
            (try_begin),
              (ge, ":ratio_of_vassals_assembled",15),
              (store_sub, ":max_travel_distance", 35, ":ratio_of_vassals_assembled"),
              (val_add, ":max_travel_distance", 5), #5..25
              (val_mul, ":max_travel_distance", 6), #30..150
            (try_end),

            (try_begin),
              (ge, ":most_threatened_center", 0),
              (store_distance_to_party_from_party, reg12, ":party_no", ":most_threatened_center"),
            (else_try),
              (assign, reg12, 0),
            (try_end),

            (assign, ":num_centers", 0),
            (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
              (store_faction_of_party, ":center_faction", ":center_no"),
              (eq, ":center_faction", ":faction_no"),
              (try_begin),
                #(ge, ":max_travel_distance", 0),
                (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),

                (try_begin),
                  (ge, ":most_threatened_center", 0),
                  (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                (else_try),
                  (assign, reg13, 0),
                (try_end),

                (store_sub, reg11, reg13, reg12),

                (this_or_next|ge, reg11, 40),
                (this_or_next|ge, ":dist", ":max_travel_distance"),
                (eq, ":center_no", ":most_threatened_center"),
              (else_try),
                #this center is a candidate so increase num_centers by one.
                (val_add, ":num_centers", 1),
              (try_end),
            (try_end),

            (try_begin),
              (ge, ":num_centers", 0),
              (store_random_in_range, ":random_center_no", 0, ":num_centers"),
              (val_add, ":random_center_no", 1),
              (assign, ":num_centers", 0),
              (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                (store_faction_of_party, ":center_faction", ":center_no"),
                (eq, ":center_faction", ":faction_no"),
                (try_begin),
                  (neq, ":center_no", ":most_threatened_center"),
                  (store_distance_to_party_from_party, ":dist", ":party_no", ":center_no"),
                  (lt, ":dist", ":max_travel_distance"),

                  (try_begin),
                    (ge, ":most_threatened_center", 0),
                    (store_distance_to_party_from_party, reg13, ":center_no", ":most_threatened_center"),
                  (else_try),
                    (assign, reg13, 0),
                  (try_end),

                  (store_sub, reg11, reg13, reg12),
                  (lt, reg11, 40),

                  (val_sub, ":random_center_no", 1),
                  (eq, ":random_center_no", 0),
                  (assign, ":best_center_to_travel", ":center_no"),
                (try_end),
              (try_end),
            (try_end),
          (try_end),

          (assign, ":travel_target", ":best_center_to_travel"),
          (assign, ":travel_target_new_assigned", 1),
        (try_end),
      (else_try),
        #if party has an ai object and they are close to that object while gathering army,
        #forget that ai object so they will select a new ai object next.
        (is_between, ":old_ai_object", centers_begin, centers_end),
        (party_get_position, pos1, ":party_no"),
        (party_get_position, pos2, ":old_ai_object"),
        (get_distance_between_positions, ":dist", pos1, pos2),
        (le, ":dist", 3),
        (assign, ":travel_target", -1),
      (try_end),
      #end ozan

      (try_begin),
        (eq, ":travel_target", -1),
        (assign, ":action", spai_undefined),
      (else_try),
        (assign, ":action", spai_visiting_village),
      (try_end),

      (assign, ":object", ":travel_target"),

      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (try_begin),
          (eq, ":travel_target", -1),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm"),
        (else_try),
          (try_begin),
            (eq, ":faction_no", "$players_kingdom"),
            (eq, ":travel_target_new_assigned", 1),
            (le, "$number_of_report_to_army_quest_notes", 13),
            (check_quest_active, "qst_report_to_army"),
            (str_store_party_name_link, s10, ":travel_target"),

            (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall), #300

            (str_store_troop_name_link, s11, ":faction_marshal"),
            (store_current_hours, ":hours"),
            (call_script, "script_game_get_date_text", 0, ":hours"),

            (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
            (str_store_string, s14, "@({s1}) {s11}: {s14}"),
            (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
            (val_add, "$number_of_report_to_army_quest_notes", 1),
          (try_end),

          (assign, reg0, ":travel_target"),
          (str_store_party_name, s10, ":travel_target"),
          (str_store_string, s14, "str_as_the_marshall_i_am_assembling_the_army_of_the_realm_and_travel_to_lands_near_s10_to_inform_more_vassals"),
        (try_end),
        (str_store_string, s16, "str_i_intend_to_assemble_the_army_of_the_realm"),
      (try_end),
	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_besieging_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_the_siege"),
	    (str_store_string, s16, "str_i_intend_to_begin_the_siege"),
	  (try_end),

	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":faction_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_raid"),
	    (str_store_string, s16, "str_i_intend_to_start_our_raid"),
	  (try_end),

	(else_try),
	  (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  (party_is_active, ":faction_object"),

	  #moved (party_set_ai_initiative, ":party_no", 10), #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.

	  (party_get_battle_opponent, ":besieger_party", ":faction_object"),

	  (try_begin),
	    (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),

	    (assign, ":action", spai_engaging_army),
	    (assign, ":object", ":besieger_party"),
	    (try_begin),
          (eq, ":troop_no", "$g_talk_troop"),
          (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
          (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
        (try_end),
      (else_try),
        (assign, ":action", spai_patrolling_around_center),
        (assign, ":object", ":faction_object"),
        (try_begin),
          (eq, ":troop_no", "$g_talk_troop"),
          (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_in_search_of_the_enemy"),
          (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_find_the_enemy"),
        (try_end),
      (try_end),

    (else_try),
      (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_is_active, ":faction_object"),

      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":faction_object"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_as_the_marshall_i_am_leading_our_forces_to_engage_the_enemy_in_battle"),
        (str_store_string, s16, "str_i_intend_to_lead_our_forces_out_to_engage_the_enemy"),
      (try_end),

	#Get reinforcements
	(else_try),
	  (assign, ":lowest_acceptable_strength_percentage", 30),

	  #if troop has enought gold then increase by 10%
	  #(troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
	  #(try_begin),
	  #  (ge, ":cur_wealth", 2000),
	  #  (assign, ":wealth_addition", 10),
	  #(else_try),
	  #  (store_div, ":wealth_addition", ":cur_wealth", 200),
	  #(try_end),
	  #(val_add, ":lowest_acceptable_strength_percentage", ":wealth_addition"),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),
	  (gt, ":home_center", -1),
	  (party_slot_eq, ":home_center", slot_town_lord, ":troop_no"), #newly added

	  #if troop is very close to its home center increase by 20%
	  (assign, ":distance_addition", 0),
	  (party_get_position, pos0, ":home_center"),
	  (party_get_position, pos1, ":party_no"),
	  (get_distance_between_positions, ":dist", pos0, pos1),

	  (try_begin),
	    (le, ":dist", 9000),
	    (store_div, ":distance_addition", ":dist", 600),
	    (store_sub, ":distance_addition", 15, ":distance_addition"),
	  (else_try),
	    (assign, ":distance_addition", 0),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":distance_addition"),

	  #if there is no campaign for faction increase by 35%
	  (assign, ":no_campaign_addition", 35),
	  (try_begin),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemy_army),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_raiding_village),
	    (this_or_next|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),
	    (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
	    (assign, ":no_campaign_addition", 0),

	    #If marshal is player itself and if there is a campaign then lower lowest_acceptable_strength_percentage by 10 instead of not changing it.
	    #Because players become confused when they see very less participation from AI lords to their campaigns.
	    (try_begin), #400
	      (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
	      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	      (try_begin),
	        (eq, ":reduce_campaign_ai", 0), #hard
	        (assign, ":no_campaign_addition", 0),
	      (else_try),
	        (eq, ":reduce_campaign_ai", 1), #medium
	        (assign, ":no_campaign_addition", -10),
	      (else_try),
	        (eq, ":reduce_campaign_ai", 2), #easy
	        (assign, ":no_campaign_addition", -15),
	      (try_end),
	    (try_end),
	  (try_end),
	  (val_add, ":lowest_acceptable_strength_percentage", ":no_campaign_addition"),
  	  (val_max, ":lowest_acceptable_strength_percentage", 25),

	  #max : 30%+15%+35% = 80% (happens when there is no campaign and player is near to its home center.)
	  (lt, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage"),

	  (try_begin),
	    (store_div, ":lowest_acceptable_strength_percentage_div_3", ":lowest_acceptable_strength_percentage", 3),
	    (ge, ":party_strength_as_percentage_of_ideal", ":lowest_acceptable_strength_percentage_div_3"),
	    (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
	    (le, ":troop_wealth", 1800),
	    (assign, ":do_only_collecting_rents", 1),
	  (try_end),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_dont_have_enough_troops_and_i_need_to_get_some_more"),

	    (str_store_string, s16, "str_i_am_running_low_on_troops"),
	  (try_end),

	  (eq, ":do_only_collecting_rents", 0),

	#follow player orders
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (party_slot_ge, ":party_no", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),

	  (party_get_slot, ":orders_type", ":party_no", slot_party_orders_type),
	  (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),
	  (party_get_slot, ":orders_time", ":party_no", slot_party_orders_time),

	  (ge, ":orders_object", 0),

	  (store_current_hours, ":hours_since_orders_given"),
	  (val_sub, ":hours_since_orders_given", ":orders_time"),
     ##diplomacy start+ If the player set the Centralization value, modify the
     #maximum time vassals will follow commands by a maximum of +/- 25%
     #(normally the maximum is 48 hours, so that would be +/- 12 hours).
     (store_mul, reg0, ":centralization", 4),
     (val_clamp, reg0, -12, 12),#<-- This should be unnecessary
     (val_sub, ":hours_since_orders_given", reg0),
     ##diplomacy end+

	  (party_is_active, ":orders_object"),
	  (party_get_slot, ":object_state", ":orders_object", slot_village_state),
	  (store_faction_of_party, ":object_faction", ":orders_object"),
	  (store_relation, ":relation_with_object", ":faction_no", ":object_faction"),

	  (assign, ":orders_are_appropriate", 1),
	  (try_begin),
	    (gt, ":hours_since_orders_given", 48),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_raiding_around_center),
	    (this_or_next|ge, ":relation_with_object", 0),
	    (ge, ":object_state", 2),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (eq, ":orders_type", spai_besieging_center),
	    (ge, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (else_try),
	    (this_or_next|eq, ":orders_type", spai_holding_center),
	    (this_or_next|eq, ":orders_type", spai_retreating_to_center),
	    (this_or_next|eq, ":orders_type", spai_accompanying_army),
	    (eq, ":orders_type", spai_visiting_village),
	    (le, ":relation_with_object", 0),
	    (assign, ":orders_are_appropriate", 0),
	  (try_end),

	  (eq, ":orders_are_appropriate", 1),

	  (assign, ":action", ":orders_type"),
	  (assign, ":object", ":orders_object"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_we_are_following_your_direction"),
	  (try_end),

	#Host of player wedding
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed"),
	  (quest_slot_eq, "qst_wed_betrothed", slot_quest_giver_troop, ":troop_no"),
	  (quest_get_slot, ":bride", "qst_wed_betrothed", slot_quest_target_troop),
	  (call_script, "script_get_kingdom_lady_social_determinants", ":bride"),
	  (assign, ":wedding_venue", reg1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":wedding_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_make_preparations_for_your_wedding"),
	    (str_store_string, s16, "str_after_all_i_need_to_make_preparations_for_your_wedding"),
	  (try_end),

	#Bridegroom at player wedding
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_slot_eq, "qst_wed_betrothed_female", slot_quest_giver_troop, ":troop_no"),

	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_heading_to_the_site_of_our_wedding"), #500
	    (str_store_string, s16, "str_after_all_we_are_soon_to_be_wed"),
	  (try_end),

	#Host of other feast
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
	  (party_slot_eq, ":feast_venue", slot_town_lord, ":troop_no"),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_hosting_a_feast_there"),
	    (str_store_string, s16, "str_i_have_a_feast_to_host"),
	  (try_end),

	#I am the bridegroom at a feast
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":operation_in_progress", 0),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
	  (troop_get_slot, ":troop_betrothed", ":troop_no", slot_troop_betrothed),
	  (is_between, ":troop_betrothed", kingdom_ladies_begin, kingdom_ladies_end),

	  (faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":feast_venue"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_to_be_the_bridegroom_there"),
	    (str_store_string, s16, "str_my_wedding_day_draws_near"),
	  (try_end),

	#Drop off prisoners
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (gt,  ":party_ratio_of_prisoners", 35),
	  (eq, ":operation_in_progress", 0),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),

	  (gt, ":home_center", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_too_much_loot_and_too_many_prisoners_and_need_to_secure_them"),
	    (str_store_string, s16, "str_i_should_think_of_dropping_off_some_of_my_prisoners"),
	  (try_end),

	#Reinforce a weak center
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (assign, ":center_to_reinforce", -1),
	  (assign, ":center_reinforce_score", 100),
	  (eq, ":operation_in_progress", 0),

	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (party_slot_eq, ":walled_center", slot_town_lord, ":troop_no"),
	    (party_get_slot, ":center_strength", ":walled_center", slot_party_cached_strength),
	    (lt, ":center_strength", ":center_reinforce_score"),
	    (assign, ":center_to_reinforce", ":walled_center"),
	    (assign, ":center_reinforce_score", ":center_strength"),
	  (try_end),

	  (gt, ":center_to_reinforce", -1),

	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":center_to_reinforce"),
	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_reinforce_it_as_it_is_poorly_garrisoned"),
	    (str_store_string, s16, "str_there_is_a_hole_in_our_defenses"),
	  (try_end),

	#Continue screening, if already doing so
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":old_ai_state", spai_screening_army), #566

	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),
	  (party_is_active, ":marshal_party"),

	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),

	  (assign, ":action", spai_screening_army),
	  (assign, ":object", ":marshal_party"),
	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_following_the_marshals_orders"),
	    (str_store_string, s16, "str_the_marshal_has_given_me_this_command"),
	  (try_end),

    (else_try), #special case for sfai_attacking_enemies_around_center for village raids
      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
      (is_between, ":faction_object", villages_begin, villages_end),

      (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
      (eq, reg0, 1),

      (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
      (party_get_slot, ":raider_party", ":faction_object", slot_village_raided_by),
      (party_is_active, ":raider_party"),

      #think about adding one more condition here, what if raider army is so powerfull, again lords will go and engage enemy one by one?
      (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),
      (lt, ":enemy_strength_nearby", 4000),
      #end think

      (assign, ":action", spai_engaging_army),
      (assign, ":object", ":raider_party"),
      (try_begin),
        (eq, ":troop_no", "$g_talk_troop"),
        (str_store_string, s14, "str_our_realm_needs_my_support_there_is_enemy_raiding_one_of_our_villages_which_is_not_to_far_from_here_i_am_going_there"),
        (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
      (try_end),

	#Follow the marshall's orders - if on the offensive, and the campaign has not lasted too long. Readiness is currently randomly set
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (call_script, "script_npc_decision_checklist_troop_follow_or_not", ":troop_no"),
	  (eq, reg0, 1),

	  (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshal", 0),
	  (troop_get_slot, ":marshal_party", ":faction_marshal", slot_troop_leaded_party),

	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":marshal_party"),

	  (try_begin),
	    (eq, "$g_talk_troop", ":troop_no"),
	    (str_store_string, s14, "str_i_am_answering_the_marshals_summons"),
	    (str_store_string, s16, "str_the_marshal_has_issued_a_summons"),
	  (try_end),

	#Support a nearby ally who is on the offensive
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),

	  (assign, ":party_to_support", -1),
	  (try_for_range, ":allied_hero", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":allied_hero", slot_troop_occupation, slto_kingdom_hero),
	    (store_faction_of_troop, ":allied_hero_faction", ":allied_hero"),
	    (eq, ":allied_hero_faction", ":faction_no"),

	    (neq, ":allied_hero", ":troop_no"),

	    (troop_get_slot, ":allied_hero_party", ":allied_hero", slot_troop_leaded_party),
	    (gt, ":allied_hero_party", 1),
	    (party_is_active, ":allied_hero_party"),


	    (this_or_next|party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_raiding_around_center),
			(party_slot_eq, ":allied_hero_party", slot_party_ai_state, spai_besieging_center),

	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":allied_hero"),
	    (gt, reg0, 4),

	    (troop_get_slot, ":troop_renown", ":troop_no", slot_troop_renown),
	    (troop_get_slot, ":ally_renown", ":allied_hero", slot_troop_renown),
	    (le, ":troop_renown", ":ally_renown"), #Ally to support must have higher renown

	    (store_distance_to_party_from_party, ":distance", ":party_no", ":allied_hero_party"),

	    (lt, ":distance", 5),

 	    (assign, ":party_to_support", ":allied_hero_party"),
	  (try_end),
	  (gt, ":party_to_support", 0),

	  (assign, ":action", spai_accompanying_army),
	  (assign, ":object", ":party_to_support"),
	  (try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (party_stack_get_troop_id, ":leader", ":object", 0),
		  (str_store_troop_name, s10, ":leader"),

		  (call_script, "script_troop_get_family_relation_to_troop", ":leader", "$g_talk_troop"),
		  (try_begin),
		    (eq, reg0, 0),
		    (str_store_string, s11, "str_comradeinarms"),
		  (try_end),
		  (str_store_string, s14, "str_i_am_supporting_my_s11_s10"),
		  (str_store_string, s16, "str_i_believe_that_one_of_my_comrades_is_in_need"),
	  (try_end),
    #I have decided to attack a vulnerable fortress
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),

	  (assign, ":walled_center_to_attack", -1),
	  (assign, ":walled_center_score", 50),

	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (store_faction_of_party, ":walled_center_faction", ":walled_center"),
	    (store_relation, ":relation", ":faction_no", ":walled_center_faction"),
	    (lt, ":relation", 0),

	    (party_get_slot, ":center_cached_strength", ":walled_center", slot_party_cached_strength),
	    (val_mul, ":center_cached_strength", 3),
	    (val_mul, ":center_cached_strength", 2),

	    (lt, ":center_cached_strength", ":party_cached_strength"),
	    (lt, ":center_cached_strength", 750),

	    (party_slot_eq, ":walled_center", slot_village_state, svs_normal),
	    (store_distance_to_party_from_party, ":distance", ":walled_center", ":party_no"),
	    (lt, ":distance", ":walled_center_score"),

	    (assign, ":walled_center_to_attack", ":walled_center"),
	    (assign, ":walled_center_score", ":distance"),
	  (try_end),

	  (is_between, ":walled_center_to_attack", centers_begin, centers_end),

	  (assign, ":action", spai_besieging_center),
	  (assign, ":object", ":walled_center_to_attack"),
	  (try_begin),
	    (eq, "$cheat_mode", 1),
	    (str_store_faction_name, s20, ":faction_no"),
	    (str_store_party_name, s21, ":object"),
	    (display_message, "str_s20_decided_to_attack_s21"),
	  (try_end),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_a_fortress_is_vulnerable"),
	    (str_store_string, s16, "str_i_believe_that_the_enemy_may_be_vulnerable"),
	  (try_end),

	#I am visiting an estate
	(else_try),
	  (assign, ":center_to_visit", -1),
	  (assign, ":score_to_beat", 300), #at least 300 gold to pick up
	  (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth), #average troop wealth is 2000
	  (val_div, ":troop_wealth", 10), #average troop wealth 10% is is 200
	  (val_add, ":score_to_beat", ":troop_wealth"), #average score to beat is 500
	  (eq, ":operation_in_progress", 0),

	  (try_begin),
	    (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

	    (assign, reg17, 0),
	    (try_begin),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	      (party_slot_eq, ":party_no", slot_party_ai_object, ":faction_marshal"),
	      (assign, reg17, 1),
	    (else_try),
	      (party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (assign, reg17, 1),
	    (try_end),
	    (eq, reg17, 1),

	    (try_begin),
	      (neq, ":faction_marshal", "trp_player"),
	      (neg|party_slot_eq, ":party_no", slot_party_following_player, 1),
	      (val_add, ":score_to_beat", 125),
	    (else_try),
	      (val_add, ":score_to_beat", 250),
	    (try_end),
	  (try_end),

	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

	    (assign, reg17, 0),
	    (try_begin),
	      (is_between, ":center_no", villages_begin, villages_end),
	      (party_slot_eq, ":center_no", slot_village_state, svs_normal),
	      (assign, reg17, 1),
	    (else_try),
	      (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
	      (assign, reg17, 1),
	    (try_end),
	    (eq, reg17, 1),

	    (party_get_slot, ":tariffs_available", ":center_no", slot_center_accumulated_tariffs),
	    (party_get_slot, ":rents_available", ":center_no", slot_center_accumulated_rents),
	    (store_add, ":money_available", ":rents_available", ":tariffs_available"),

	    (gt, ":money_available", ":score_to_beat"),
	    (assign, ":center_to_visit", ":center_no"),
	    (assign, ":score_to_beat", ":money_available"),
	  (try_end),

	  (is_between, ":center_to_visit", centers_begin, centers_end),

	  (try_begin),
	    (is_between, ":center_to_visit", walled_centers_begin, walled_centers_end),
	    (assign, ":action", spai_holding_center),
	    (assign, ":object", ":center_to_visit"),
	  (else_try),
        (assign, ":action", spai_visiting_village),
  	    (assign, ":object", ":center_to_visit"),
	  (try_end),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_need_to_inspect_my_properties_and_collect_my_dues"),
	    (str_store_string, s16, "str_it_has_been_too_long_since_i_have_inspected_my_estates"),
	  (try_end),

	#My men are weary, and I wish to return home
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (this_or_next|gt, ":hours_since_last_rest", 504), #Three weeks
	  (lt, ":aggressiveness", 25),
	  (gt, ":hours_since_last_rest", 168), #one week if aggressiveness < 25
	  (eq, ":operation_in_progress", 0),

	  (call_script, "script_lord_get_home_center", ":troop_no"),
	  (assign, ":home_center", reg0),

	  (gt, ":home_center", -1),
	  (assign, ":action", spai_holding_center),
	  (assign, ":object", ":home_center"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_my_men_are_weary_so_we_are_returning_home"),
	    (str_store_string, s16, "str_my_men_are_becoming_weary"),
	  (try_end),

	#I have a score to settle with the enemy
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (eq, ":operation_in_progress", 0),

	  (eq, ":faction_is_at_war", 1),
	  ##diplomacy start+ roguish lords can also do this, but humanitarian lords of any kind won't
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (eq, ":troop_reputation", lrep_quarrelsome),

	  (assign, ":target_village", -1),
	  (assign, ":score_to_beat", 0), #based on relation

	  (try_for_range, ":possible_target", villages_begin, villages_end),
	    (store_faction_of_party, ":village_faction", ":possible_target"),
	    (store_relation, ":relation", ":village_faction", ":faction_no"),
	    (lt, ":relation", 0),

	    (neg|party_slot_ge, ":possible_target", slot_village_state, svs_looted),
	    (party_get_slot, ":town_lord", ":possible_target", slot_town_lord),
	    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":town_lord"),
	    (assign, ":village_score", reg0),

	    (lt, ":village_score", ":score_to_beat"),
	    (assign, ":score_to_beat", ":village_score"),
	    (assign, ":target_village", ":possible_target"),
	  (try_end),

	  (is_between, ":target_village", centers_begin, centers_end),
	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":target_village"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_have_a_score_to_settle_with_the_lord_there"),
	    (str_store_string, s16, "str_i_am_thinking_of_settling_an_old_score"),
	  (try_end),

	#I need money, so I am raiding where the money is
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	  (eq, ":faction_is_at_war", 1),
	  (eq, ":operation_in_progress", 0),

	  (this_or_next|gt, ":hours_since_last_combat", 12),
	  (lt, ":hours_since_last_rest", 96),
	  (gt, ":aggressiveness", 40),

	  ##diplomacy start+
	  #Roguish lords can also do this.  Humanitarian companions will never
	  #do this, even if they otherwise have an eligible reputation.  Companions
	  #who actively enjoy raiding can also do this, regardless of whether they
	  #have an eligible reputation.
	  (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
	  (lt, reg0, 1),
	  (this_or_next|lt, reg0, 0),
	  (this_or_next|eq, ":troop_reputation", lrep_roguish),
	  ##diplomacy end+
	  (this_or_next|eq, ":troop_reputation", lrep_debauched),
	  (this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
	  (this_or_next|eq, ":troop_reputation", lrep_cunning),
	  (eq, ":troop_reputation", lrep_quarrelsome),

	  (troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
	  (lt, ":wealth", 500),

	  (assign, ":score_to_beat", 0),
	  (assign, ":target_village", -1),

	  (try_for_range, ":possible_target", villages_begin, villages_end),
	    (store_faction_of_party, ":village_faction", ":possible_target"),
	    (store_relation, ":relation", ":village_faction", ":faction_no"),
	    (lt, ":relation", 0),

	    (this_or_next|party_slot_eq, ":possible_target", slot_village_state, svs_normal),
	    (party_slot_eq, ":possible_target", slot_village_state, svs_being_raided),

	    (party_get_slot, reg17, ":possible_target", slot_town_prosperity),
	    (store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
	    (val_sub, reg17, ":distance"),

	    (gt, reg17, ":score_to_beat"),
	    (assign, ":score_to_beat", reg17),
	    (assign, ":target_village", ":possible_target"),
	  (try_end),

	  (gt, ":target_village", -1),

	  (assign, ":action", spai_raiding_around_center),
	  (assign, ":object", ":target_village"),

	  (try_begin),
	    (eq, ":troop_no", "$g_talk_troop"),
	    (str_store_string, s14, "str_i_am_short_of_money_and_i_hear_that_there_is_much_wealth_there"),
	    (str_store_string, s16, "str_i_need_to_refill_my_purse_preferably_with_the_enemys_money"),
	  (try_end),

	#Attacking wealthiest lands
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 65),

		(assign, ":score_to_beat", 0),
		(assign, ":target_village", -1),

		(try_for_range, ":possible_target", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":possible_target"),
			(store_relation, ":relation", ":village_faction", ":faction_no"),
			(lt, ":relation", 0),
			(neg|party_slot_eq, ":possible_target", slot_village_state, svs_looted),
			(party_get_slot, ":village_prosperity", ":possible_target", slot_town_prosperity),
			(val_mul, ":village_prosperity", 2),

			(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target"),
			(val_sub, ":village_prosperity", ":distance"),
			(gt, ":village_prosperity", ":score_to_beat"),

			(assign, ":score_to_beat", ":village_prosperity"),
			(assign, ":target_village", ":possible_target"),
		(try_end),

		##diplomacy start+ companions who hate raiding will not raid
		(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_humanitarian),
		(lt, reg0, 1),
		##diplomacy end+
		(gt, ":target_village", -1),

		(assign, ":action", spai_raiding_around_center),
		(assign, ":object", ":target_village"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_by_striking_at_the_enemys_richest_lands_perhaps_i_can_draw_them_out_to_battle"),
			(str_store_string, s16, "str_i_am_thinking_of_going_on_the_attack"),
		(try_end),

	#End the war
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
	    ##diplomacy start+
		(assign, reg0, 0),
		(try_begin),
			#A liege in service to another lord or allied with the player can do this.
			(this_or_next|eq, ":troop_reputation", lrep_none),
			(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
			(is_between, ":troop_no", pretenders_begin, pretenders_end),
			(this_or_next|neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),
			(assign, reg0, 0),
		(else_try),
			#Lords who are simulatenously Martial and tmt_honest (such as Alayen),
			#or Custodian and tmt_honest (such as Artimenner) can also do this.
			(this_or_next|eq, ":troop_reputation", lrep_martial),
			(eq, ":troop_reputation", lrep_custodian),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
		(try_end),
		(this_or_next|ge, reg0, 1),
		##diplomacy end+
		(eq, ":troop_reputation", lrep_upstanding),
		(eq, ":faction_is_at_war", 1),
		(eq, ":operation_in_progress", 0),

		(assign, ":faction_to_attack", -1),
		(try_for_range, ":possible_faction_to_attack", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_no", ":possible_faction_to_attack"),
			(lt, ":relation", 0),
			(faction_slot_eq, ":possible_faction_to_attack", slot_faction_state, sfs_active),

			(store_add, ":war_damage_inflicted_slot", ":possible_faction_to_attack", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":war_damage_inflicted_slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_inflicted", ":faction_no", ":war_damage_inflicted_slot"),

			(store_add, ":war_damage_suffered_slot", ":faction_no", slot_faction_war_damage_inflicted_on_factions_begin),
			(val_sub, ":war_damage_suffered_slot", kingdoms_begin),
			(faction_get_slot, ":war_damage_suffered", ":possible_faction_to_attack", ":war_damage_suffered_slot"),

			(gt, ":war_damage_inflicted", 80),
			(lt, ":war_damage_inflicted", ":war_damage_suffered"),
			(assign, ":faction_to_attack", ":possible_faction_to_attack"),
		(try_end),

		(gt, ":faction_to_attack", -1),

		(assign, ":target_village", -1),
		(assign, ":score_to_beat", 50),

		(try_for_range, ":possible_target_village", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":possible_target_village"),
			(eq, ":village_faction", ":faction_to_attack"),
			(neg|party_slot_eq, ":possible_target_village", slot_village_state, svs_looted),
			(store_distance_to_party_from_party, ":distance", ":party_no", ":possible_target_village"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":score_to_beat", ":distance"),
			(assign, ":target_village", ":possible_target_village"),
		(try_end),

		(gt, ":target_village", -1),

		(assign, ":action", spai_raiding_around_center),
		(assign, ":object", ":target_village"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_perhaps_if_i_strike_one_more_blow_we_may_end_this_war_on_our_terms_"),
			(str_store_string, s16, "str_we_may_be_able_to_bring_this_war_to_a_close_with_a_few_more_blows"),
		(try_end),

	#I have a feast to attend
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),
		(faction_get_slot, ":feast_venue", ":faction_no", slot_faction_ai_object),
		(party_get_slot, ":feast_host", ":feast_venue", slot_town_lord),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":feast_host"),
		(assign, ":relation_with_host", reg0),

        (ge, ":relation_with_host", 0),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":feast_venue"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_wish_to_attend_the_feast_there"),
			(str_store_string, s16, "str_there_is_a_feast_which_i_wish_to_attend"),
		(try_end),
	#A lady to court
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":troop_no"),
		(troop_slot_eq, ":troop_no", slot_troop_spouse, -1),
		(neg|is_between, ":troop_no", kings_begin, kings_end),
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),


		(gt, ":hours_since_last_courtship", 72),
		(eq, ":operation_in_progress", 0),

		(assign, ":center_to_visit", -1),
		(assign, ":score_to_beat", 150),

		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
			(is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_get_slot, ":love_interest_center", ":love_interest", slot_troop_cur_center),
			(is_between, ":love_interest_center", centers_begin, centers_end),
			(store_faction_of_party, ":love_interest_faction_no", ":love_interest_center"),
			(eq, ":faction_no", ":love_interest_faction_no"),
            #(store_relation, ":relation", ":faction_no", ":love_interest_faction_no"),
            #(ge, ":relation", 0),

			(store_distance_to_party_from_party, ":distance", ":party_no", ":love_interest_center"),

			(lt, ":distance", ":score_to_beat"),
			(assign, ":center_to_visit", ":love_interest_center"),
			(assign, ":score_to_beat", ":distance"),
        (try_end),

		(gt, ":center_to_visit", -1),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":center_to_visit"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_there_is_a_fair_lady_there_whom_i_wish_to_court"),
			(str_store_string, s16, "str_i_have_the_inclination_to_pay_court_to_a_fair_lady"),
		(try_end),

	#Patrolling an alarmed center
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(assign, ":target_center", -1),
		(assign, ":score_to_beat", 60),
		(eq, ":operation_in_progress", 0),
		(gt, ":aggressiveness", 40),

		(try_for_range, ":center_to_patrol", centers_begin, centers_end), #find closest center that has spotted enemies.
            (store_faction_of_party, ":center_faction", ":center_to_patrol"),
            (eq, ":center_faction", ":faction_no"),
			(party_slot_ge, ":center_to_patrol", slot_center_last_spotted_enemy, 0),

			#new - begin
			(party_get_slot, ":sortie_strength", ":center_to_patrol", slot_center_sortie_strength),
			(party_get_slot, ":enemy_strength", ":center_to_patrol", slot_center_sortie_enemy_strength),
			(store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
			(val_div, ":enemy_strength_mul_14_div_10", 10),
			(party_get_slot, ":party_strength", ":party_no", slot_party_cached_strength),

			(this_or_next|neg|party_is_in_town, ":party_no", ":center_to_patrol"),
			(gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),

			(ge, ":party_strength", 100),
			#new - end

			(party_get_slot, reg17, ":center_to_patrol", slot_town_lord),
			(call_script, "script_troop_get_relation_with_troop", reg17, ":troop_no"),

			(this_or_next|eq, ":troop_reputation", lrep_upstanding),
				(gt, reg0, -5),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_to_patrol"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":target_center", ":center_to_patrol"),
			(assign, ":score_to_beat", ":distance"),
		(try_end),

		(is_between, ":target_center", centers_begin, centers_end),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":target_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_we_have_heard_reports_that_the_enemy_is_in_the_area"),
			(str_store_string, s16, "str_i_have_heard_reports_of_enemy_incursions_into_our_territory"),
		(try_end),

	#Time in household
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(gt, ":hours_since_last_home", 168),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),
		(gt, ":home_center", -1),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_need_to_spend_some_time_with_my_household"),
			(str_store_string, s16, "str_it_has_been_a_long_time_since_i_have_been_able_to_spend_time_with_my_household"),
		(try_end),

	#Patrolling the borders
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":faction_is_at_war", 1),
		(gt, ":aggressiveness", 65),
		(eq, ":operation_in_progress", 0),

		(assign, ":center_to_patrol", -1),
		(assign, ":score_to_beat", 75),

		(try_for_range, ":village", villages_begin, villages_end),
			(store_faction_of_party, ":village_faction", ":village"),
			(store_relation, ":relation", ":village_faction", ":faction_no"),
			(lt, ":relation", 0),

			(store_distance_to_party_from_party, ":distance", ":village", ":party_no"),
			(lt, ":distance", ":score_to_beat"),

			(assign, ":score_to_beat", ":distance"),
			(assign, ":center_to_patrol", ":village"),
		(try_end),

		(is_between, ":center_to_patrol", villages_begin, villages_end),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":center_to_patrol"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_watching_the_borders"),
			(str_store_string, s16, "str_i_may_be_needed_to_watch_the_borders"),
		(try_end),

	#Visiting a friend - temporarily disabled
	(else_try),
		(eq, 1, 0),

	#Patrolling home
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),

		(is_between, ":home_center", centers_begin, centers_end),
		(eq, ":operation_in_progress", 0),

		(assign, ":action", spai_patrolling_around_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_will_guard_the_areas_near_my_home"),
			(str_store_string, s16, "str_i_am_perhaps_needed_most_at_home"),
		(try_end),

	#Default end
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":operation_in_progress", 0),

		(call_script, "script_lord_get_home_center", ":troop_no"),
		(assign, ":home_center", reg0),
		(is_between, ":home_center", walled_centers_begin, walled_centers_end),

		(assign, ":action", spai_holding_center),
		(assign, ":object", ":home_center"),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_cant_think_of_anything_better_to_do"),
		(try_end),
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(eq, ":operation_in_progress", 1),

		(party_get_slot, ":action", ":party_no", slot_party_ai_state),
		(party_get_slot, ":object", ":party_no", slot_party_ai_object),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_am_completing_what_i_have_already_begun"),
		(try_end),
	(else_try),
	  (eq, ":do_only_collecting_rents", 0),
		(assign, ":action", spai_undefined),
		(assign, ":object", -1),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s14, "str_i_dont_even_have_a_home_to_which_to_return"),
		(try_end),
	(try_end),

	(try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_troop_name, s10, ":troop_no"),
		(display_message, "str_debug__s10_decides_s14_faction_ai_s15"),
	(try_end),

    (assign, reg0, ":action"),
	(assign, reg1, ":object"),
	]),

	#script_npc_decision_checklist_troop_follow_or_not
  # Input: arg1 = party_no
  # Output: reg0 = center_no (closest)
  #         reg1 = center_no2 (another close center or -1)
  #
  # If reg1 is non-negative, it should make some sense to say "<party_no> is
  # between <reg0> and <reg1>".
  #
  # The way I do this is:
  #   1.  Find the closest center to the party.
  #   2.  Excluding the center from (1), find the closest center to the
  #       party which is not closer to the center from (1) than it is to
  #       the party.  (There might not be any centers matching this
  #       description.)
  #
  # If the party is much closer to center_1 than center_2, I discard
  # the second center.  (The rationale is that if I'm standing on my
  # doorstep, it is be helpful to say "I am between my house and the
  # grocery store".  It is less misleading to just say "I am near my
  # house.")
  ("dplmc_get_closest_center_or_two",
    [
      (store_script_param_1, ":party_no"),
      (call_script, "script_get_closest_center", ":party_no"),#writes closest center to reg0
      (store_distance_to_party_from_party, ":distance_to_beat", ":party_no", reg0),
      (val_mul, ":distance_to_beat", 2),
      (val_add, ":distance_to_beat", 1),

      (assign, reg1, -1),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (neq, ":center_no", reg0),
        (store_distance_to_party_from_party, ":party_to_center_distance", ":party_no", ":center_no"),
        (lt, ":party_to_center_distance", ":distance_to_beat"),
        (store_distance_to_party_from_party, ":center_to_center_distance", reg0, ":center_no"),
        (gt, ":center_to_center_distance", ":party_to_center_distance"),
        (assign, ":distance_to_beat", ":party_to_center_distance"),
        (assign, reg1, ":center_no"),
      (try_end),
  ]),


# Jrider +

(
	"npc_decision_checklist_troop_follow_or_not", [

	(store_script_param, ":troop_no", 1),
	(store_faction_of_troop, ":faction_no", ":troop_no"),
	(faction_get_slot, ":faction_ai_state", ":faction_no", slot_faction_ai_state),

	(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
	(faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
    ##diplomacy start+
    #Get the centralization value for use below.  It should be a value in [-3,3].
    #A centralization value of 0 should not result in any behavior change.
    (try_begin),
       #If the player altered the kingdom policy, always apply its effects to
       #the AI of his kingdom's lords.
       (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
       (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
       (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
       (val_clamp, ":centralization", -3, 4),
    (else_try),
       #Currently, do not apply centralization to the AI for NPC kingdoms, since
       #NPC rulers set their policies randomly and do not gain the same monthly
       #relation bonuses/penalties from centralization that the player does.
       (assign, ":centralization", 0),
    (try_end),
    ##diplomacy end+

	(assign, ":result", 0),
	(try_begin),
		##diplomacy start+ add another check
		(this_or_next|lt, ":faction_marshall", 0),
		##diplomacy end+
		(eq, ":faction_marshall", -1),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_no_marshal_is_appointed"),
		(try_end),
	(else_try),
		(troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
		(neg|party_is_active, ":faction_marshall_party"),

		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_marshal_is_currently_indisposed"),
		(try_end),
	(else_try),
		(neq, ":faction_ai_state", sfai_attacking_center),
        (neq, ":faction_ai_state", sfai_raiding_village),
        (neq, ":faction_ai_state", sfai_attacking_enemies_around_center),
        (neq, ":faction_ai_state", sfai_attacking_enemy_army),
        (neq, ":faction_ai_state", sfai_gathering_army),

		#Not doing an offensive
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_acting_independently_because_our_realm_is_currently_not_on_campaign"),
		(try_end),
	(else_try),
		(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_marshall"),
		(assign, ":relation_with_marshall", reg0),

		(try_begin),
		  (le, ":relation_with_marshall", -10),
		  (assign, ":acceptance_level", 10000),
		(else_try),
		  (store_mul, ":acceptance_level", ":relation_with_marshall", -1000),
		(try_end),

		(val_add, ":acceptance_level", 1500),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1250),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1250),
          (try_end),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_marshall, "trp_player"),
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard/player's faction
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate/player's faction
            (val_add, ":acceptance_level", -1500),
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy/player's faction
            (val_add, ":acceptance_level", -2000),
          (try_end),
		(try_end),

		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),

		(le, ":temp_ai_seed", ":acceptance_level"),

		#Very low opinion of marshall
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__i_am_not_accompanying_the_marshal_because_i_fear_that_he_may_lead_us_into_disaster"),
		(try_end),
		#Make nuanced, depending on personality type
	(else_try),
		(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall),

		(lt, ":relation_with_marshall", 0),
		(ge, ":marshal_controversy", 50),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_question_his_judgment"),
		(try_end),
	(else_try),
		(troop_get_slot, ":marshal_controversy", ":faction_marshall", slot_faction_marshall),
		(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":faction_marshall"),

		(lt, ":relation_with_marshall", 5),
		(ge, ":marshal_controversy", 80),

		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_will_be_reappointment"),
		(try_end),
	(else_try),
		#(lt, ":relation_with_marshall", 45),
		#(eq, ":faction_marshall", "trp_player"), #moved below as only effector. Search "think about this".

		(store_sub, ":relation_with_marshal_difference", 50, ":relation_with_marshall"),

		#for 50 relation with marshal ":acceptance_level" will be 0
		#for 20 relation with marshal ":acceptance_level" will be 2100
		#for 10 relation with marshal ":acceptance_level" will be 2800
		#for 0 relation with marshal ":acceptance_level" will be 3500
		#for -10 relation with marshal ":acceptance_level" will be 4200
		#average is about 2500
		(store_mul, ":acceptance_level", ":relation_with_marshal_difference", 70),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "$players_kingdom"),

          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1200),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", 1200),
          (try_end),
		(else_try),
          (eq, ":faction_marshall", "trp_player"),

          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard
            (val_add, ":acceptance_level", -1000),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate
            (val_add, ":acceptance_level", -1500),
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy
            (val_add, ":acceptance_level", -2000),
          (try_end),
		(try_end),

		(try_begin),
		  (eq, ":troop_reputation", lrep_selfrighteous),
		  (val_add, ":acceptance_level", 1500),
		(else_try),
		  (this_or_next|eq, ":troop_reputation", lrep_martial),
		  (this_or_next|eq, ":troop_reputation", lrep_roguish),
		  (eq, ":troop_reputation", lrep_quarrelsome),
		  (val_add, ":acceptance_level", 1000),
		(else_try),
		  (eq, ":troop_reputation", lrep_cunning),
		  (val_add, ":acceptance_level", 500),
		(else_try),
		  (eq, ":troop_reputation", lrep_upstanding), #neutral
		(else_try),
		  (this_or_next|eq, ":troop_reputation", lrep_benefactor), #helper
		  (eq, ":troop_reputation", lrep_goodnatured),
		  (val_add, ":acceptance_level", -500),
		(else_try),
		  (eq, ":troop_reputation", lrep_custodian), #very helper
		  (val_add, ":acceptance_level", -1000),
		(try_end),

		(try_begin),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_quarrelsome),
		  (val_add, ":acceptance_level", -750),
		(else_try),
		  (this_or_next|troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_martial),
		  (troop_slot_eq, ":faction_marshall", slot_lord_reputation_type, lrep_upstanding),
		  (val_add, ":acceptance_level", -250),
		(try_end),

		(val_add, ":acceptance_level", 2000),
		#average become 2500 + 2000 = 4500, (45% of lords will not join campaign because of this reason. (33% for hard, 57% for easy, 30% for marshal player))

      ##diplomacy start+ Apply centralization.
      #Adjusting acceptance level seems a natural place to represent this.
      (store_mul, reg0, ":centralization", 100),
      (val_clamp, reg0, -300, 301),#should be unnecessary
      (val_sub, ":acceptance_level", reg0),#adjust the chance of following the marshall by +/- 1% for every step of centralization
      ##diplomacy end+
		(troop_get_slot, ":temp_ai_seed", ":troop_no", slot_troop_temp_decision_seed),

		(le, ":temp_ai_seed", ":acceptance_level"),

		(try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (str_store_string, s15, "str_i_am_not_accompanying_the_marshal_because_i_can_do_greater_deeds"),
		(try_end),

		#(try_begin),
		#  (ge, "$cheat_mode", 1),
		#  (assign, reg7, ":acceptance_level"),
		#  (assign, reg8, ":relation_with_marshall"),
		#  (display_message, "@{!}DEBUGS : acceptance level : {reg7}, relation with marshal : {reg8}"),
		#(try_end),
	(else_try),
		(store_current_hours, ":hours_since_last_faction_rest"),
		(faction_get_slot, ":last_rest_time", ":faction_no", slot_faction_ai_last_rest_time),
		(val_sub, ":hours_since_last_faction_rest", ":last_rest_time"),

		#nine days on average, marshal will usually end after 10 days
		#ozan changed, 360 hours (15 days) in average, marshal cannot end it during a siege attack/defence anymore.
		(assign, ":troop_campaign_limit", 360),
		(store_mul, ":marshal_relation_modifier", ":relation_with_marshall", 6), #ozan changed 4 to 6.
		(val_add, ":troop_campaign_limit", ":marshal_relation_modifier"),

		(try_begin),
			(eq, ":troop_reputation", lrep_upstanding),
			(val_mul, ":troop_campaign_limit", 4),
			(val_div, ":troop_campaign_limit", 3),
		(try_end),

		(str_store_troop_name, s16, ":faction_marshall"),

		(gt, ":hours_since_last_faction_rest", ":troop_campaign_limit"),

		#Too long a campaign
		(try_begin),
			(eq, ":troop_no", "$g_talk_troop"),
			(str_store_string, s15, "str__s16_has_kept_us_on_campaign_on_far_too_long_and_there_are_other_pressing_matters_to_which_i_must_attend"),
		(try_end),
		#Also make nuanced, depending on personality type
	(else_try),
		(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		(neg|party_is_active, ":party_no"),
		#This string should not occur, as it will only happen if a lord is contemplating following the player
	(else_try),
		(troop_get_slot, ":marshal_party", ":faction_marshall", slot_troop_leaded_party),

		(assign, ":information_radius", 40),
		(try_begin),
		  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		  (assign, ":information_radius", 50),
		(try_end),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
		(try_begin),
		  (neq, ":faction_no", "fac_player_supporters_faction"),
		  (neq, ":faction_no", "$players_kingdom"),
		  ##diplomacy start+ the player may be able to become leader in other situations
		  (neg|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
		  ##diplomacy end+
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -10),
		    (else_try),
		      (val_add, ":information_radius", -8),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", -5),
		    (else_try),
		      (val_add, ":information_radius", -4),
		    (try_end),
		  (try_end),
		(else_try),
		  (try_begin),
		    (eq, ":reduce_campaign_ai", 2), #easy
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 25),
		    (else_try),
		      (val_add, ":information_radius", 20),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 1), #moderate
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 15),
		    (else_try),
		      (val_add, ":information_radius", 12),
		    (try_end),
		  (else_try),
		    (eq, ":reduce_campaign_ai", 0), #hard
		    (try_begin),
		      (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_gathering_army),
		      (val_add, ":information_radius", 5),
		    (else_try),
		      (val_add, ":information_radius", 4),
		    (try_end),
		  (try_end),
		(try_end),
      ##diplomacy start+ Apply centralization to the AI here.
      (store_add, reg0, 10, ":centralization"),
      (val_clamp, reg0, 7, 14),#should be unnecessary
      (val_mul, ":information_radius", reg0),
      (val_add, ":information_radius", 5),
      (val_div, ":information_radius", 10),#Adjust +/- 10% for every level of centralization
      ##diplomacy end+

		(faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
		(assign, reg17, 0),
		(try_begin),
		  (try_begin),
		    (neg|is_between, ":faction_object", villages_begin, villages_end),
		    (assign, reg17, 1),
		  (try_end),
		  (try_begin),
		    (neg|faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
		    (assign, reg17, 1),
		  (try_end),
		  (eq, reg17, 1),

		  (store_distance_to_party_from_party, ":distance", ":marshal_party", ":party_no"),

		  (gt, ":distance", ":information_radius"),

          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_not_participating_in_the_marshals_campaign_because_i_do_not_know_where_to_find_our_main_army"),
  		  (try_end),
		(else_try),
		  (eq, reg17, 0),

          (assign, reg17, 1),
          (try_begin),
            #if we are already accompanying marshal forget below.
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":marshal_party"),
            (assign, reg17, 0),
          (try_end),
          (eq, reg17, 1),

		  #if faction ai is "attacking enemies around a center" is then do not find and compare distance to marshal, find and compare distance to "attacked village"
		  (party_get_slot, ":enemy_strength_nearby", ":faction_object", slot_center_sortie_enemy_strength),

		  (try_begin), #changes between 70..x (as ":enemy_strength_nearby" increases, ":information_radius" increases too.),
		    (ge, ":enemy_strength_nearby", 4000),
		    (val_sub, ":enemy_strength_nearby", 4000),
		    (store_div, ":information_radius", ":enemy_strength_nearby", 200),
		    (val_add, ":information_radius", 70),
		  (else_try), #changes between 30..70
		    (store_div, ":information_radius", ":enemy_strength_nearby", 100),
		    (val_add, ":information_radius", 30),
		  (try_end),

		  (store_distance_to_party_from_party, ":distance", ":faction_object", ":party_no"),

		  (gt, ":distance", ":information_radius"),

          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (str_store_string, s15, "str__i_am_acting_independently_although_some_enemies_have_been_spotted_within_our_borders_they_havent_come_in_force_and_the_local_troops_should_be_able_to_dispatch_them"),
  		  (try_end),
		(try_end),

		(gt, ":distance", ":information_radius"),
	(else_try),
		(try_begin),
		  (eq, ":troop_no", "$g_talk_troop"),
		  (str_store_string, s15, "str__the_needs_of_the_realm_must_come_first"),
		(try_end),
		(assign, ":result", 1),
	(try_end),

	(assign, reg0, ":result"),
	]),

("party_get_ideal_size",
    [
      (store_script_param_1, ":party_no"),

      #default limit is 30 for any party
      (assign, ":limit", 30),

      (try_begin),
        (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
        (store_faction_of_party, ":faction_id", ":party_no"),

        #default limit is 10 for kingdom lords
        (assign, ":limit", 10),

        #each (leadership level) gives 5 to limit
        (store_skill_level, ":skill", "skl_leadership", ":party_leader"),
        (store_attribute_level, ":charisma", ":party_leader", ca_charisma),
        (val_mul, ":skill", 5),
        (val_add, ":limit", ":skill"),

        #each (charisma level) gives 1 to limit
        (val_add, ":limit", ":charisma"),

        #each (25 renown) gives 1 to limit
        (troop_get_slot, ":troop_renown", ":party_leader", slot_troop_renown),
        (store_div, ":renown_bonus", ":troop_renown", 25),
        (val_add, ":limit", ":renown_bonus"),

        ##diplomacy begin
        (assign, ":percent", 100),
        ##diplomacy end

		##diplomacy start+
		#Limit effects of policies for nascent kingdoms.
		(assign, ":policy_min", -3),
		(assign, ":policy_max", 4),#one greater than the maximum

		(try_begin),
			(this_or_next|eq, ":faction_id", "fac_player_supporters_faction"),
				(faction_slot_eq, ":faction_id", slot_faction_leader, "trp_player"),
			(faction_get_slot, ":policy_max", ":faction_id", slot_faction_num_towns),
			(faction_get_slot, reg0, ":faction_id", slot_faction_num_castles),
			(val_add, ":policy_max", reg0),
			(val_clamp, ":policy_max", 0, 4),#0, 1, 2, 3
			(store_mul, ":policy_min", ":policy_max", -1),
			(val_add, ":policy_max", 1),#one greater than the maximum
		(try_end),
		##diplomacy end+

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_leader, ":party_leader"),
          (val_add, ":limit", dplmc_monarch_party_bonus),
          ##diplomacy begin
          (try_begin),
            (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":centralization", 10),
            (val_add, ":percent", ":centralization"),
          (try_end),

        (else_try),
          (try_begin),
            (faction_get_slot, ":centralization", ":faction_id", dplmc_slot_faction_centralization),
            (neq, ":centralization", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":centralization", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":centralization", -3),
            (val_add, ":percent", ":centralization"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":aristocraty", ":faction_id", dplmc_slot_faction_aristocracy),
            (neq, ":aristocraty", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":aristocraty", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":aristocraty", 3),
            (val_add, ":percent", ":aristocraty"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":faction_id", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
			##diplomacy start+ Apply constraint
			(val_clamp, ":quality", ":policy_min", ":policy_max"),
			##diplomacy end+
            (val_mul, ":quality", -4),
            (val_add, ":percent", ":quality"),
          (try_end),
          ##diplomacy end
        (try_end),

        ##diplomacy begin
        (try_begin),
          (faction_get_slot, ":serfdom", ":faction_id", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
		  ##diplomacy start+ Apply constraint
		  (val_clamp, ":serfdom", ":policy_min", ":policy_max"),
		  ##diplomacy end+
          (val_mul, ":serfdom", 2), #SB : description says 1, this used to be 3
          (val_add, ":percent", ":serfdom"),
        (try_end),

        (val_mul, ":limit", ":percent"),
        ##nested diplomacy start+ Round correctly
        (val_add, ":limit", 50),
        ##nested diplomacy end+
        (val_div, ":limit", 100),
        ##diplomacy end

        (try_begin),
          (faction_slot_eq, ":faction_id", slot_faction_marshall, ":party_leader"),
          (val_add, ":limit", dplmc_marshal_party_bonus),
        (try_end),

        #party takes additional 20 limit per each castle its party leader owns
        (try_for_range, ":cur_center", castles_begin, castles_end),
          (party_slot_eq, ":cur_center", slot_town_lord, ":party_leader"),
          (val_add, ":limit", dplmc_castle_party_bonus),
        (try_end),
      ##diplomacy start+
      ##Extend this script so it will also work with garrisons
      (else_try),
         (party_slot_eq, ":party_no", slot_party_type, spt_town),
         (assign, ":limit", 380),#average starting town garrison size
      (else_try),
         (this_or_next|is_between, ":party_no", walled_centers_begin, walled_centers_end),
         (party_slot_eq, ":party_no", slot_party_type, spt_castle),
         (assign, ":limit", 142),#average starting castle garrison size
         #(store_faction_of_party, ":faction_id", ":party_no"),
      ##diplomacy end+
      (try_end),

      #if player has level of 0 then ideal limit will be exactly same, if player has level of 80 then ideal limit will be multiplied by 2 ((80 + 80) / 80)
      #below code will increase limits a little as the game progresses and player gains level
      (store_character_level, ":level", "trp_player"),
      (val_min, ":level", 80),
      (store_add, ":level_factor", 80, ":level"),
      (val_mul, ":limit", ":level_factor"),
      (val_div, ":limit", 80),
      (assign, reg0, ":limit"),
  ]),

("update_party_creation_random_limits",
    [
      (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
  ]),

("party_calculate_regular_strength",
    [
      (store_script_param_1, ":party"), #Party_id

      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_mul, ":stack_strength", ":stack_size"),
        (val_add,reg0, ":stack_strength"),
      (try_end),
  ]),

("party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id

      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party", ":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
        (val_add, ":stack_strength", 4), #new was 12 (patch 1.125)
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_mul, ":stack_strength", 2), #new (patch 1.125)
        (val_div, ":stack_strength", 100),
        (val_max, ":stack_strength", 1), #new (patch 1.125)
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero & wounded
          (assign, ":stack_strength", 0),
        (try_end),
        (val_add, reg0, ":stack_strength"),
      (try_end),
      (party_set_slot, ":party", slot_party_cached_strength, reg0),
  ]),

("party_remove_all_prisoners",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),

("party_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),

("party_prisoners_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":source_party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),

("party_add_party",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (call_script, "script_party_add_party_companions",          ":target_party", ":source_party"),
      (call_script, "script_party_prisoners_add_party_prisoners", ":target_party", ":source_party"),
  ]),

("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ]),

("clear_party_group",
    [
      (store_script_param_1, ":root_party"),

      (party_clear, ":root_party"),
      (party_get_num_attached_parties, ":num_attached_parties", ":root_party"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
        (call_script, "script_clear_party_group", ":attached_party"),
      (try_end),
  ]),

("party_add_wounded_members_as_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":source_party"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
        (ge, ":num_wounded", 1),
        (party_stack_get_troop_id, ":stack_troop", ":source_party", ":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        #(party_prisoner_stack_get_size, ":stack_size",":source_party",":stack_no"),
        (party_add_prisoners, ":target_party", ":stack_troop", ":num_wounded"),
      (try_end),
  ]),

("get_nonempty_party_in_group",
    [
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
      (try_begin),
        (gt, ":num_companion_stacks", 0),
        (assign, reg0, ":party_no"),
      (else_try),
        (assign, reg0, -1),

        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (lt, reg0, 0),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_get_nonempty_party_in_group", ":attached_party"),
        (try_end),
      (try_end),
  ]),

("collect_prisoners_from_empty_parties",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":collection_party"),

      (party_get_num_companions, ":num_companions", ":party_no"),
      (try_begin),
        (eq, ":num_companions", 0), #party is empty (has no companions). Collect its prisoners.
        (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
          (troop_is_hero, ":stack_troop"),
          (party_add_members, ":collection_party", ":stack_troop", 1),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_collect_prisoners_from_empty_parties", ":attached_party", ":collection_party"),
      (try_end),
  ]),

("write_fit_party_members_to_stack_selection",
   [
     (store_script_param, ":party_no", 1),
     (store_script_param, ":exclude_leader", 2),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":slot_index", 2),
     (assign, ":total_fit", 0),
     (try_for_range, ":stack_index", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_index"),
       (assign, ":num_fit", 0),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (try_begin),
           (neg|troop_is_wounded, ":stack_troop"),
           (this_or_next|eq, ":exclude_leader", 0),
           (neq, ":stack_index", 0),
           (assign, ":num_fit",1),
         (try_end),
       (else_try),
         (party_stack_get_size, ":num_fit", ":party_no", ":stack_index"),
         (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_index"),
         (val_sub, ":num_fit", ":num_wounded"),
       (try_end),
       (try_begin),
         (gt, ":num_fit", 0),
         (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":num_fit"),
         (troop_set_slot, "trp_stack_selection_ids", ":slot_index", ":stack_troop"),
         (val_add, ":slot_index", 1),
       (try_end),
       (val_add, ":total_fit", ":num_fit"),
     (try_end),
     (val_sub, ":slot_index", 2),
     (troop_set_slot, "trp_stack_selection_amounts", 0, ":slot_index"),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_fit"),
    ]),

("remove_fit_party_member_from_stack_selection",
   [
     (store_script_param, ":slot_index", 1),
     (val_add, ":slot_index", 2),
     (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":slot_index"),
     (troop_get_slot, ":troop_no", "trp_stack_selection_ids", ":slot_index"),
     (val_sub, ":amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", ":slot_index", ":amount"),
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (val_sub, ":total_amount", 1),
     (troop_set_slot, "trp_stack_selection_amounts", 1, ":total_amount"),
     (try_begin),
       (le, ":amount", 0),
       (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
       (store_add, ":end_cond", ":num_slots", 2),
       (store_add, ":begin_cond", ":slot_index", 1),
       (try_for_range, ":index", ":begin_cond", ":end_cond"),
         (store_sub, ":prev_index", ":index", 1),
         (troop_get_slot, ":value", "trp_stack_selection_amounts", ":index"),
         (troop_set_slot, "trp_stack_selection_amounts", ":prev_index", ":value"),
         (troop_get_slot, ":value", "trp_stack_selection_ids", ":index"),
         (troop_set_slot, "trp_stack_selection_ids", ":prev_index", ":value"),
       (try_end),
       (val_sub, ":num_slots", 1),
       (troop_set_slot, "trp_stack_selection_amounts", 0, ":num_slots"),
     (try_end),
     (assign, reg0, ":troop_no"),
    ]),

("remove_random_fit_party_member_from_stack_selection",
   [
     (troop_get_slot, ":total_amount", "trp_stack_selection_amounts", 1),
     (store_random_in_range, ":random_troop", 0, ":total_amount"),
     (troop_get_slot, ":num_slots", "trp_stack_selection_amounts", 0),
     (store_add, ":end_cond", ":num_slots", 2),
     (try_for_range, ":index", 2, ":end_cond"),
       (troop_get_slot, ":amount", "trp_stack_selection_amounts", ":index"),
       (val_sub, ":random_troop", ":amount"),
       (lt, ":random_troop", 0),
       (assign, ":end_cond", 0),
       (store_sub, ":slot_index", ":index", 2),
     (try_end),
     (call_script, "script_remove_fit_party_member_from_stack_selection", ":slot_index"),
    ]),

("add_routed_party",
   [
     (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.
     (assign, ":num_regulars", 0),
     (assign, ":deleted_stacks", 0),
     (try_for_range, ":stack_no", 0, ":num_stacks"),
       (store_sub, ":difference", ":num_stacks", ":stack_no"),
       (ge, ":difference", ":deleted_stacks"),
       (store_sub, ":stack_no_minus_deleted", ":stack_no", ":deleted_stacks"),
       (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no_minus_deleted"),
       (try_begin),
         (troop_is_hero, ":stack_troop"),
         (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no_minus_deleted"),
         (party_remove_members, "p_routed_enemies", ":stack_troop", 1),
         (try_begin),
           (le, ":stack_size", 1),
           (val_add, ":deleted_stacks", 1), #if deleted hero is the only one in his troop, now we have one less stacks
         (try_end),
       (else_try),
         (val_add, ":num_regulars", 1),
       (try_end),
     (try_end),

     #add new party to map if there is at least one routed agent. (new party name : routed_party, template : routed_warriors)
     (try_begin),
       (ge, ":num_regulars", 1),

       (set_spawn_radius, 2),
       (spawn_around_party, "p_main_party", "pt_routed_warriors"),
       (assign, ":routed_party", reg0),
       # SB : white flag
       (party_set_banner_icon, ":routed_party", "icon_white_flag"),
       (party_set_slot, ":routed_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

       (assign, ":max_routed_agents", 0),
       (assign, ":routed_party_faction", "fac_neutral"),
       (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
         (faction_get_slot, ":num_routed_agents_in_this_faction", ":cur_faction", slot_faction_num_routed_agents),
         (gt, ":num_routed_agents_in_this_faction", ":max_routed_agents"),
         (assign, ":max_routed_agents", ":num_routed_agents_in_this_faction"),
         (assign, ":routed_party_faction", ":cur_faction"),
       (try_end),

       (party_set_faction, ":routed_party", ":routed_party_faction"),

       (party_set_ai_behavior, ":routed_party", ai_bhvr_travel_to_party),

       (assign, ":minimum_distance", 1000000),
       #SB : get rid of useless range
       (store_random_in_range, ":nearest_ally_city", walled_centers_begin, walled_centers_end),
       (try_for_range, ":party_no", walled_centers_begin, walled_centers_end),
         # (party_is_active, ":party_no"),
         # (party_get_slot, ":cur_party_type", ":party_no", slot_party_type),
         # (this_or_next|eq, ":cur_party_type", spt_town),
         # (eq, ":cur_party_type", spt_castle),
         (store_faction_of_party, ":cur_faction", ":party_no"),
         (this_or_next|eq, ":routed_party_faction", "fac_neutral"),
         (eq, ":cur_faction", ":routed_party_faction"),
         (party_get_position, pos1, ":party_no"),
         (store_distance_to_party_from_party, ":dist", ":party_no", "p_main_party"),
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (assign, ":nearest_ally_city", ":party_no"),
         (try_end),
       (try_end),

       (party_get_position, pos1, "p_main_party"), #store position information of main party in pos1
       (party_get_position, pos2, ":nearest_ally_city"), #store position information of target city in pos2

       (assign, ":minimum_distance", 1000000),
       (try_for_range, ":unused", 0, 10),
         (map_get_random_position_around_position, pos3, pos1, 2), #store position of found random position (possible placing position for new routed party) around battle position in pos3
         (get_distance_between_positions, ":dist", pos2, pos3), #store distance between found position and target city in ":dist".
         (try_begin),
           (lt, ":dist", ":minimum_distance"),
           (assign, ":minimum_distance", ":dist"),
           (copy_position, pos63, pos3),
         (try_end),
       (end_try),

       (party_set_position, ":routed_party", pos63),

       (party_set_ai_object, ":routed_party", ":nearest_ally_city"),
       (party_set_flags, ":routed_party", pf_default_behavior, 1),
       #SB : add extra slot to actually merge with garrison
       (party_set_slot, ":routed_party", slot_party_type, spt_reinforcement),

       #adding party members of p_routed_enemies to routed_party
       (party_clear, ":routed_party"),
       (party_get_num_companion_stacks, ":num_stacks", "p_routed_enemies"), #question, I changed (total_enemy_casualties) with (p_routed_enemies) because this is not prisoner in p_routed_enemies party.
       (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", "p_routed_enemies", ":stack_no"),
         (try_begin),
           (neg|troop_is_hero, ":stack_troop"), #do not add routed heroes to (new created) routed party for now.

           (party_stack_get_size, ":stack_size", "p_routed_enemies", ":stack_no"),
           (party_add_members, ":routed_party", ":stack_troop", ":stack_size"),
         (try_end),
       (try_end),
     (try_end),
    ]),

("party_count_fit_regulars",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, reg0, ":stack_size"),
      (try_end),
  ]),

("party_count_fit_for_battle",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (try_begin),
            (neg|troop_is_wounded, ":stack_troop"),
            (assign, ":num_fit", 1),
          (try_end),
        (else_try),
          (party_stack_get_size, ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),

("party_count_members_with_full_health",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party",":i_stack"),
        (neq, ":stack_troop", "trp_player"),
        (assign, ":num_fit",0),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (store_troop_health, ":troop_hp", ":stack_troop"),
          (try_begin),
            (ge, ":troop_hp", 80),
            (assign, ":num_fit",1),
          (try_end),
        (else_try),
          (party_stack_get_size, ":num_fit",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":num_fit", ":num_wounded"),
          (val_max, ":num_fit", 0),
        (try_end),
        (val_add, reg0, ":num_fit"),
      (try_end),
  ]),

("get_stack_with_rank",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, reg(0), -1),
      (assign, ":num_total", 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (eq, reg(0), -1), #continue only if we haven't found the result yet.
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
        (party_stack_get_num_wounded,  ":num_wounded",":party",":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_add, ":num_total", ":stack_size"),
        (try_begin),
          (lt, ":rank", ":num_total"),
          (assign, reg(0), ":i_stack"),
        (try_end),
      (try_end),
  ]),

("inflict_casualties_to_party",
    [
      (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop",":party",":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
        (val_add, ":troop_toughness", 5),  #troop-toughness = level + 5
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 ,10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 2), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero,":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp",":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", 1), #wounded
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
  ]),

("move_members_with_ratio",
    [
      (store_script_param_1, ":source_party"), #Source Party_id
      (store_script_param_2, ":target_party"), #Target Party_id
      (party_get_num_prisoner_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_prisoner_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_prisoners, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_prisoners, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
      (party_get_num_companion_stacks, ":num_stacks",":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":source_party",":stack_no"),
        (party_stack_get_size,    ":stack_size",":source_party",":stack_no"),
        (store_mul, ":number_to_move",":stack_size","$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_members, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_members, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
  ]),

("shuffle_troop_slots",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":slots_begin", 2),
      (store_script_param, ":slots_end", 3),
      (try_for_range, ":cur_slot_no", ":slots_begin", ":slots_end"),
        (store_random_in_range, ":random_slot_no", ":slots_begin", ":slots_end"), #reg(58) = random slot. Now exchange slots reg(57) and reg(58)
        (troop_get_slot, ":cur_slot_value", ":troop_no", ":cur_slot_no"), #temporarily store the value in slot reg(57) in reg(59)
        (troop_get_slot, ":random_slot_value", ":troop_no", ":random_slot_no"), #temporarily store the value in slot reg(58) in reg(60)
        (troop_set_slot, ":troop_no", ":cur_slot_no", ":random_slot_value"), # Now exchange the two...
        (troop_set_slot, ":troop_no", ":random_slot_no", ":cur_slot_value"),
      (try_end),
  ]),

("cf_troop_get_random_enemy_troop_with_occupation",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":occupation"),

      (assign, ":result", -1),
      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"),
        (lt, reg0, -10),
        (val_add, ":count_enemies", 1),
      (try_end),

      (gt, ":count_enemies", 0),
      (store_random_in_range,":random_enemy",0,":count_enemies"),

      (assign, ":count_enemies", 0),
      (try_for_range, ":enemy_troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, ":occupation"),
        (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":enemy_troop_no"),
        (lt, reg0, -10),
        (val_add, ":count_enemies", 1),
        (eq, ":random_enemy", ":count_enemies"),
        (assign, ":result", ":enemy_troop_no"),
      (try_end),

      (neq, ":result", -1),
      (assign, reg0, ":result"),
  ]),

("party_wound_all_members_aux",
    [
      (store_script_param_1, ":party_no"),

      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
          (party_wound_members, ":party_no", ":stack_troop", ":stack_size"),
        (else_try),
          (troop_set_health, ":stack_troop", 0),
        (try_end),
      (try_end),
      (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
        (call_script, "script_party_wound_all_members_aux", ":attached_party"),
      (try_end),
  ]),

("party_wound_all_members",
    [
      (store_script_param_1, ":party_no"),

      (call_script, "script_party_wound_all_members_aux", ":party_no"),
  ]),

("cf_check_enemies_nearby",
    [
      (get_player_agent_no, ":player_agent"),
      (agent_is_alive, ":player_agent"),
      (agent_get_position, pos1, ":player_agent"),
      (assign, ":result", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents,":cur_agent"),
        (neq, ":cur_agent", ":player_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_ally, ":cur_agent"),
        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions, ":cur_distance", pos1, pos2),
        (le, ":cur_distance", 1500), #15 meters
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 0),
  ]),

("cf_reinforce_party",
    [
      (store_script_param_1, ":party_no"),

      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ The party faction may be changed for culture, but we still need the original
	  (assign, ":real_party_faction", ":party_faction"),
	  ##diplomacy end+
      (party_get_slot, ":party_type",":party_no", slot_party_type),

#Rebellion changes begin:
      (try_begin),
        (eq, ":party_type", spt_kingdom_hero_party),
        (party_stack_get_troop_id, ":leader", ":party_no"),
        (troop_get_slot, ":party_faction",  ":leader", slot_troop_original_faction),
		##diplomacy start+ Use player culture for companions and spouse (and any hypothetical non-hero mercenaries)
		(eq, ":real_party_faction", "fac_player_supporters_faction"),
		(is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		(this_or_next|is_between, ":leader", companions_begin, companions_end),
		(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":leader"),
		   (neg|is_between, ":leader", heroes_begin, heroes_end),
		(assign, ":party_faction", "$g_player_culture"),
		##diplomacy end+
      (try_end),
#Rebellion changes end

      (try_begin),
      #SB : this block checks for town lords, which is invalid for kingdom parties
        (is_between, ":party_type", spt_castle, spt_village),
        (eq, ":party_faction", "fac_player_supporters_faction"),
        (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
        (try_begin),
        ##diplomacy begin
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":party_faction", "$g_player_culture"),

          # (try_begin), #debug
            # (eq, "$cheat_mode", 1),
            # (str_store_party_name, s11, ":party_no"),
            # (display_message, "@pt in {s11}"),
          # (try_end),

        (else_try),
        ##diplomacy end
          (gt, ":town_lord", 0),
          (troop_get_slot, ":party_faction", ":town_lord", slot_troop_original_faction),
          (gt, ":party_faction", 0), ## CC
        (else_try),
          (party_get_slot, ":party_faction", ":party_no", slot_center_original_faction),
        (try_end),
      (try_end),
	  ##diplomacy start+ Player culture cleanup (do this once here, instead of separately for each type)
	  (try_begin),
	     (gt, ":real_party_faction", "fac_commoners"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_faction"),
	     (this_or_next|eq, ":real_party_faction", "fac_player_supporters_faction"),
		 (eq, ":real_party_faction", "$players_kingdom"),
		 (neg|is_between, ":party_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
		 (assign, ":party_faction", "$g_player_culture"),
	  (try_end),
	  ##diplomacy end+

      (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
      (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
      (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),

      (assign, ":party_template", 0),
      (store_random_in_range, ":rand", 0, 100),
  	  ##diplomacy start+
	  #Implement "quality vs. quantity" in a way that is visible in player battles
	  #(previously, quantity increased party size, but quality only had an effect
	  #in autocalc battles)
	  (try_begin),
		(is_between, ":real_party_faction", kingdoms_begin, kingdoms_end),
		(faction_get_slot, ":dplmc_quality", ":real_party_faction", dplmc_slot_faction_quality),
		(val_clamp, ":dplmc_quality", -3, 4),
		(val_add, ":rand", ":dplmc_quality"),
		(val_clamp, ":rand", 0, 101),
	  (try_end),
	  ##diplomacy end+
      (try_begin),
        (this_or_next|eq, ":party_type", spt_town),
        (eq, ":party_type", spt_castle),  #CASTLE OR TOWN
        (try_begin),
          (lt, ":rand", 65),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (assign, ":party_template", ":party_template_b"),
        (try_end),
      (else_try),
        (eq, ":party_type", spt_kingdom_hero_party),
        (try_begin),
          (lt, ":rand", 50),
          (assign, ":party_template", ":party_template_a"),
        (else_try),
          (lt, ":rand", 75),
          (assign, ":party_template", ":party_template_b"),
        (else_try),
          (assign, ":party_template", ":party_template_c"),
        (try_end),
      (else_try),
	  ##diplomacy start+ Reinforcements for patrols
	    (this_or_next|eq, ":party_type", spt_patrol),
	    (eq, ":party_type", spt_reinforcement), #SB : add more reinf if necessary
		(try_begin),
		   (lt, ":rand", 65),
		   (assign, ":party_template", ":party_template_a"),
		(else_try),
		   (assign, ":party_template", ":party_template_b"),
		(try_end),
	  ##diplomacy end+
      (try_end),

      (try_begin),
        (gt, ":party_template", 0),
        (party_add_template, ":party_no", ":party_template"),
      (try_end),
  ]),

("create_kingdom_party_if_below_limit",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),

      (call_script, "script_count_parties_of_faction_and_party_type", ":faction_no", ":party_type"),
      (assign, ":party_count", reg0),

      (assign, ":party_count_limit", 0),

      (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),

      (try_begin),
##        (eq, ":party_type", spt_forager),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_scout),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_patrol),
##        (assign, ":party_count_limit", 1),
##      (else_try),
##        (eq, ":party_type", spt_messenger),
##        (assign, ":party_count_limit", 1),
##      (else_try),
        (eq, ":party_type", spt_kingdom_caravan),
        (try_begin),
          (eq, ":num_towns", 0),
          (assign, ":party_count_limit", 0),
        (else_try),
          (eq, ":num_towns", 1),
          (assign, ":party_count_limit", 1),
        (else_try),
          (eq, ":num_towns", 2),
          (assign, ":party_count_limit", 3),
        (else_try),
          (assign, ":party_count_limit", 5),
        (try_end),
        ##diplomacy begin
          #overwriting party count limit MAX(2 * X - 1, 0)
        (store_mul, ":party_count_limit", ":num_towns", 2),
        (val_sub, ":party_count_limit", 1),
        (val_max, ":party_count_limit", 0),
        ##diplomacy end

##      (else_try),
##        (eq, ":party_type", spt_prisoner_train),
##        (assign, ":party_count_limit", 1),
      (try_end),

      (assign, reg0, -1),
      (try_begin),
        (lt, ":party_count", ":party_count_limit"),
        (call_script,"script_cf_create_kingdom_party", ":faction_no", ":party_type"),
      (try_end),
  ]),

("cf_create_kingdom_party",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":party_type"),

      (str_store_faction_name, s7, ":faction_no"),
      (assign, ":party_name_str", "str_no_string"),

##      (faction_get_slot, ":reinforcements_a", ":faction_no", slot_faction_reinforcements_a),
      (faction_get_slot, ":reinforcements_b", ":faction_no", slot_faction_reinforcements_b),
##      (faction_get_slot, ":reinforcements_c", ":faction_no", slot_faction_reinforcements_c),

      (try_begin),
##        (eq, ":party_type", spt_forager),
##        (assign, ":party_template", "pt_forager_party"),
#        (assign, ":party_name_str", "str_s7_foragers"),
##      (else_try),
##        (eq, ":party_type", spt_scout),
##        (assign, ":party_template", "pt_scout_party"),
#        (assign, ":party_name_str", "str_s7_scouts"),
##      (else_try),
##        (eq, ":party_type", spt_patrol),
##        (assign, ":party_template", "pt_patrol_party"),
#        (assign, ":party_name_str", "str_s7_patrol"),
##      (else_try),
        (eq, ":party_type", spt_kingdom_caravan),
        (assign, ":party_template", "pt_kingdom_caravan_party"),
#        (assign, ":party_name_str", "str_s7_caravan"),
##      (else_try),
##        (eq, ":party_type", spt_messenger),
##        (assign, ":party_template", "pt_messenger_party"),
#        (assign, ":party_name_str", "str_s7_messenger"),
##      (else_try),
##        (eq, ":party_type", spt_raider),
##        (assign, ":party_template", "pt_raider_party"),
##        (assign, ":party_name_str", "str_s7_raiders"),
##      (else_try),
##        (eq, ":party_type", spt_prisoner_train),
##        (assign, ":party_template", "pt_prisoner_train_party"),
#        (assign, ":party_name_str", "str_s7_prisoner_train"),
      (try_end),

      (assign, ":result", -1),
      (try_begin),
        (try_begin),
          (eq, ":party_type", spt_kingdom_caravan),
          (call_script,"script_cf_select_random_town_with_faction", ":faction_no", -1),
          (set_spawn_radius, 0),
        (else_try), #not used at the moment
          (call_script,"script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
          (set_spawn_radius, 1),
        (try_end),
        (assign, ":spawn_center", reg0),
        (is_between, ":spawn_center", centers_begin, centers_end),
        (spawn_around_party,":spawn_center",":party_template"),
        (assign, ":result", reg0),
        (party_set_faction, ":result", ":faction_no"),
        (try_begin),
          (eq, ":party_type", spt_kingdom_caravan),
          (party_set_slot, ":result", slot_party_home_center, ":spawn_center"),
          (party_set_slot, ":result", slot_party_last_traded_center, ":spawn_center"),
		(try_end),
        (party_set_slot, ":result", slot_party_type, ":party_type"),
        (party_set_slot, ":result", slot_party_ai_state, spai_undefined),
        (try_begin),
          (neq, ":party_name_str", "str_no_string"),
          (party_set_name, ":result", ":party_name_str"),
        (try_end),

        (try_begin),
##          (eq, ":party_type", spt_forager),
##          (party_add_template, ":result", ":reinforcements_a"),
##        (else_try),
##          (eq, ":party_type", spt_scout),
##          (party_add_template, ":result", ":reinforcements_c"),
##        (else_try),
##          (eq, ":party_type", spt_patrol),
##          (party_add_template, ":result", ":reinforcements_a"),
##          (party_add_template, ":result", ":reinforcements_b"),
##        (else_try),
          (eq, ":party_type", spt_kingdom_caravan),
          (try_begin),
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (party_get_slot, ":reinforcement_faction", ":spawn_center", slot_center_original_faction),
            (faction_get_slot, ":reinforcements_b", ":reinforcement_faction", slot_faction_reinforcements_b),
          (try_end),
          (party_add_template, ":result", ":reinforcements_b"),
          (party_add_template, ":result", ":reinforcements_b"),
          (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
          (party_set_ai_object,":result",":spawn_center"),
          (party_set_flags, ":result", pf_default_behavior, 1),
          (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
          (try_for_range, ":cur_goods", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_goods_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_set_slot, ":result", ":cur_goods_price_slot", average_price_factor),
          (try_end),
##        (else_try),
##          (eq, ":party_type", spt_messenger),
##          (faction_get_slot, ":messenger_troop", ":faction_no", slot_faction_messenger_troop),
##          (party_add_leader, ":result", ":messenger_troop"),
##          (party_set_ai_behavior,":result",ai_bhvr_travel_to_party),
##          (party_set_ai_object,":result",":spawn_center"),
##          (party_set_flags, ":result", pf_default_behavior, 0),
##        (else_try),
##          (eq, ":party_type", spt_raider),
##          (party_add_template, ":result", ":reinforcements_c"),
##          (party_add_template, ":result", ":reinforcements_b"),
##          (party_add_template, ":result", "pt_raider_captives"),
##        (else_try),
##          (eq, ":party_type", spt_prisoner_train),
##          (party_add_template, ":result", ":reinforcements_b"),
##          (party_add_template, ":result", ":reinforcements_a"),
##          (try_begin),
##            (call_script,"script_cf_faction_get_random_enemy_faction",":faction_no"),
##            (store_random_in_range,":r",0,3),
##            (try_begin),
##              (lt, ":r", 1),
##              (faction_get_slot, ":captive_reinforcements", reg0, slot_faction_reinforcements_b),
##            (else_try),
##              (faction_get_slot, ":captive_reinforcements", reg0, slot_faction_reinforcements_a),
##            (try_end),
##            (party_add_template, ":result", ":captive_reinforcements",1),
##          (else_try),
##            (party_add_template, ":result", "pt_default_prisoners"),
##          (try_end),
        (try_end),
      (try_end),
      (ge, ":result", 0),
      (assign, reg0, ":result"),
  ]),

("get_troop_attached_party",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":attached_party_no", -1),
      (try_begin),
        (ge, ":party_no", 0),
        (party_get_attached_to, ":attached_party_no", ":party_no"),
      (try_end),
      (assign, reg0, ":attached_party_no"),
  ]),

("party_set_ai_state",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":new_ai_state", 2),
      (store_script_param, ":new_ai_object", 3),

      (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
      (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),
      (party_get_attached_to, ":attached_to_party", ":party_no"),
      (assign, ":party_is_in_town", 0),
      (try_begin),
        (is_between, ":attached_to_party", centers_begin, centers_end),
        (assign, ":party_is_in_town", ":attached_to_party"),
      (try_end),

      (assign, ":commander", -1),
      (try_begin),
        (party_is_active, ":party_no"),
	    (party_stack_get_troop_id, ":commander", ":party_no", 0),
	    (store_faction_of_party, ":faction_no", ":party_no"),
	  (try_end),

	  (try_begin),
	    (lt, ":commander", 0),
        #sometimes 0 sized parties enter "party_set_ai_state" script. So only discard them
	    #(try_begin),
        #  (eq, "$cheat_mode", 1),
	    #  (str_store_troop_name, s6, ":party_no"),
        #  (party_get_num_companions, reg6, ":party_no"),
        #  (display_message, "@{!}DEBUGS : party name is : {s6}, party size is : {reg6}, new ai discarded."),
        #(try_end),
	  (else_try),
	    #Party does any business in town
	    (try_begin),
	      (is_between, ":party_is_in_town", walled_centers_begin, walled_centers_end),
	      (party_slot_eq, ":party_is_in_town", slot_center_is_besieged_by, -1),
	      (call_script, "script_troop_does_business_in_center", ":commander", ":party_is_in_town"),
	    (else_try),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_visiting_village),
	      (party_get_slot, ":party_is_in_village", ":party_no", slot_party_ai_object),
	      (is_between, ":party_is_in_village", villages_begin, villages_end),
	      #(party_slot_eq, ":party_is_in_village", slot_center_is_looted_by, -1),
          (call_script, "script_cf_village_normal_cond", ":party_is_in_village"), #SB : script condition
		  # (neg|party_slot_eq, ":party_is_in_village", slot_village_state, svs_being_raided),
		  # (neg|party_slot_eq, ":party_is_in_village", slot_village_state, svs_deserted), #SB : deserted condition
		  # (neg|party_slot_eq, ":party_is_in_village", slot_village_state, svs_looted),
	      (store_distance_to_party_from_party, ":distance", ":party_no", ":party_is_in_village"),
	      (lt, ":distance", 3),
	      (call_script, "script_troop_does_business_in_center", ":commander", ":party_is_in_village"),
	    (try_end),

	    (party_set_slot, ":party_no", slot_party_follow_me, 0),

	    (try_begin),
	      (eq, ":old_ai_state", ":new_ai_state"),
	      (eq, ":old_ai_object", ":new_ai_object"),
          #do nothing. Nothing is changed.
        (else_try),
          (assign, ":initiative", 100),
          (assign, ":aggressiveness", 8),
          (assign, ":courage", 8),

          (try_begin),
            (this_or_next|eq, ":new_ai_state", spai_accompanying_army),
            (eq, ":new_ai_state", spai_screening_army),

            (party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),

            (try_begin),
              (gt, ":party_is_in_town", 0),
              (party_detach, ":party_no"),
            (try_end),

            (try_begin),
              (eq, ":new_ai_state", spai_screening_army),
              (assign, ":aggressiveness", 9),
              (assign, ":courage", 9),
              (assign, ":initiative", 80),
            (else_try),
              (assign, ":aggressiveness", 6),
              (assign, ":courage", 9),
              (assign, ":initiative", 10),
            (try_end),
          (else_try),
            (eq, ":new_ai_state", spai_besieging_center),

            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 2),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_follow_me, 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),

            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),

            (assign, ":aggressiveness", 1),
            (assign, ":courage", 9),
            (assign, ":initiative", 20),
            #(assign, ":initiative", 100),
          (else_try),
            (eq, ":new_ai_state", spai_holding_center),

            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),

            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),

            (assign, ":aggressiveness", 7),
            (assign, ":courage", 9),
            (assign, ":initiative", 100),
            #(party_set_ai_initiative, ":party_no", 99),
          (else_try),
            (eq, ":new_ai_state", spai_patrolling_around_center),
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),

            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
              (party_set_ai_patrol_radius, ":party_no", 1), #line 100
            (else_try),
              (party_set_ai_patrol_radius, ":party_no", 5), #line 100
            (try_end),

            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_follow_me, 1),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),

            (try_begin),
              (gt, ":party_is_in_town", 0),
              (party_detach, ":party_no"),
            (try_end),

            (try_begin),
              #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.
              (ge, ":commander", 0),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	          (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),

	          (party_get_position, pos3, ":party_no"),
	          (get_distance_between_positions, ":distance_to_center", pos1, pos3),

	          (try_begin),
	            (ge, ":distance_to_center", 800), #added new (1.122)
                (assign, ":initiative", 10),
                (assign, ":aggressiveness", 1),
                (assign, ":courage", 8),
              (else_try), #below added new (1.122)
                (assign, ":initiative", 100),
                (assign, ":aggressiveness", 8),
                (assign, ":courage", 8),
              (try_end),
            (else_try),
              (assign, ":aggressiveness", 8),
              (assign, ":courage", 8),
              (assign, ":initiative", 100),
            (try_end),
          (else_try),
            (eq, ":new_ai_state", spai_visiting_village),
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 2),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_point),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
            (party_set_slot, ":party_no", slot_party_ai_substate, 0),
            (try_begin),
              (gt, ":party_is_in_town", 0),
              (neq, ":party_is_in_town", ":new_ai_object"),
              (party_detach, ":party_no"),
            (try_end),

            (assign, ":aggressiveness", 8),
            (assign, ":courage", 8),
            (assign, ":initiative", 100),
          (else_try), #0.660: this is where the 1625/1640 bugs happen with an improper ai_object
            (eq, ":new_ai_state", spai_raiding_around_center),
            (party_get_position, pos1, ":new_ai_object"),
            (map_get_random_position_around_position, pos2, pos1, 1),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
            (party_set_ai_patrol_radius, ":party_no", 10),
            (party_set_ai_target_position, ":party_no", pos2),
            (party_set_ai_object, ":party_no", ":new_ai_object"),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
	        (party_set_slot, ":party_no", slot_party_follow_me, 1),
	        (party_set_slot, ":party_no", slot_party_ai_substate, 0),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (neq, ":party_is_in_town", ":new_ai_object"),
	          (party_detach, ":party_no"),
	        (try_end),

	        (try_begin),
	          (ge, ":commander", 0),
	          (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	          (assign, ":aggressiveness", 1),
	          (assign, ":courage", 8),
	          (assign, ":initiative", 20),
	        (else_try),
	          (assign, ":aggressiveness", 7),
	          (assign, ":courage", 8),
	          (assign, ":initiative", 100),
	        (try_end),
	      (else_try),
	        (eq, ":new_ai_state", spai_engaging_army),

	        (party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
	        (party_set_ai_object, ":party_no", ":new_ai_object"),
	        (party_set_flags, ":party_no", pf_default_behavior, 0),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (party_detach, ":party_no"),
	        (try_end),

            (try_begin),
              #new to avoid losing time of marshal with attacking unimportant targets while there is a threat in our centers.
              (ge, ":commander", 0),
              (faction_slot_eq, ":faction_no", slot_faction_marshall, ":commander"),
	          (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
              (assign, ":initiative", 10),
              (assign, ":aggressiveness", 1),
              (assign, ":courage", 8),
            (else_try),
              (assign, ":aggressiveness", 8),
	          (assign, ":courage", 8),
	          (assign, ":initiative", 100),
	        (try_end),
	      (else_try),
	        (eq, ":new_ai_state", spai_retreating_to_center),
	        (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
	        (party_set_ai_object, ":party_no", ":new_ai_object"),
	        (party_set_flags, ":party_no", pf_default_behavior, 1),
	        (party_set_slot, ":party_no", slot_party_commander_party, -1),
	        (try_begin),
	          (gt, ":party_is_in_town", 0),
	          (neq, ":party_is_in_town", ":new_ai_object"),
	          (party_detach, ":party_no"),
	        (try_end),

	        (assign, ":aggressiveness", 3),
	        (assign, ":courage", 4),
	        (assign, ":initiative", 100),
	      (else_try),
	        (eq, ":new_ai_state", spai_undefined),
	        (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
	        (party_set_flags, ":party_no", pf_default_behavior, 0),
	      (try_end),

	      (try_begin),
	        (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_martial),
	        (val_add, ":aggressiveness", 2),
	        (val_add, ":courage", 2),
	      (else_try),
			  ##diplomacy start+ support lady personality types
			  (neg|troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_adventurous),
			  (this_or_next|troop_slot_ge, ":commander", slot_lord_reputation_type, dplmc_lrep_ladies_begin),
			  ##diplomacy end+
	        (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_debauched),
	        (val_sub, ":aggressiveness", 1),
	        (val_sub, ":courage", 1),
	      (try_end),

	      (party_set_slot, ":party_no", slot_party_ai_state, ":new_ai_state"),
	      (party_set_slot, ":party_no", slot_party_ai_object, ":new_ai_object"),
	      (party_set_aggressiveness, ":party_no", ":aggressiveness"),
	      (party_set_courage, ":party_no", ":courage"),
	      (party_set_ai_initiative, ":party_no", ":initiative"),
	    (try_end),
	  (try_end),

	  #Helpfulness
	  (try_begin),
	    (ge, ":commander", 0),

	    (party_set_helpfulness, ":party_no", 101),
	    (try_begin),
  	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_martial),
 	      (party_set_helpfulness, ":party_no", 200),
	    (else_try),
  	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_upstanding),
	      (party_set_helpfulness, ":party_no", 150),
	    (else_try),
	      (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
	      (party_set_helpfulness, ":party_no", 110),
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_quarrelsome),
	      (party_set_helpfulness, ":party_no", 90),
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_selfrighteous),
	      (party_set_helpfulness, ":party_no", 80),
	    (else_try),
	      (troop_slot_eq, ":commander", slot_lord_reputation_type, lrep_debauched),
	      (party_set_helpfulness, ":party_no", 50),
	    (try_end),
	  (try_end),
  ]),

("cf_party_under_player_suggestion",
    [
    (store_script_param, ":party_no", 1),

	(party_slot_eq, ":party_no", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),

	(party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
	(party_slot_eq, ":party_no", slot_party_orders_type, ":ai_state"),

	(party_get_slot, ":ai_object", ":party_no", slot_party_ai_object),
	(party_slot_eq, ":party_no", slot_party_orders_object, ":ai_object"),

	(store_current_hours, ":hours_since_orders_given"),
	(party_get_slot, ":orders_time", ":party_no", slot_party_orders_time),

	(val_sub, ":hours_since_orders_given", ":orders_time"),
	(lt, ":hours_since_orders_given", 12),
	]),

("party_calculate_and_set_nearby_friend_enemy_follower_strengths",
    [
      (store_script_param, ":party_no", 1),
      (assign, ":follower_strength", 0),
      (assign, ":friend_strength", 0),
      (assign, ":enemy_strength", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ add support for promoted kingdom ladies
      (store_add, ":end_cond", heroes_end, 1),#<- changed active_npcs to heroes
      (try_for_range, ":iteration", heroes_begin, ":end_cond"),#<- changed active_npcs to heroes
        (try_begin),
          (eq, ":iteration", heroes_end),#<- changed active_npcs to heroes
          (assign, ":cur_troop", "trp_player"),
        (else_try),
          (assign, ":cur_troop", ":iteration"),
        (try_end),
		##diplomacy end+

        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (ge, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),


        #I moved these lines here from (*1) to faster process, ozan.
        (store_troop_faction, ":army_faction", ":cur_troop"),
        (store_relation, ":relation", ":army_faction", ":party_faction"),
        (this_or_next|neq, ":relation", 0),
        (eq, ":army_faction", ":party_faction"),
        #ozan end


        (neq, ":party_no", ":cur_troop_party"),
        (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
        (try_begin),
          (neg|is_between, ":party_no", centers_begin, centers_end),
          (party_slot_eq, ":cur_troop_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":commander_party", ":cur_troop_party", slot_party_ai_object),
          (eq, ":commander_party", ":party_no"),
          (val_add, ":follower_strength", ":str"),
        (else_try),
          (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":party_no"),
          (lt, ":distance", 20),

          #(*1)

          (try_begin),
            (lt, ":distance", 5),
            (assign, ":str_divided", ":str"),
          (else_try),
            (lt, ":distance", 10),
            (store_div, ":str_divided", ":str", 2),
          (else_try),
            (lt, ":distance", 15),
            (store_div, ":str_divided", ":str", 4),
          (else_try),
            (store_div, ":str_divided", ":str", 8),
          (try_end),

          (try_begin),
            (this_or_next|eq, ":army_faction", ":party_faction"),
            (gt, ":relation", 0),
            (val_add, ":friend_strength", ":str_divided"),
          (else_try),
            (lt, ":relation", 0),
            (val_add, ":enemy_strength", ":str_divided"),
          (try_end),
        (try_end),
      (try_end),

      (party_set_slot, ":party_no", slot_party_follower_strength, ":follower_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_friend_strength, ":friend_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_enemy_strength, ":enemy_strength"),
      ]),

("collect_friendly_parties",
    [
      (party_collect_attachments_to_party, "p_main_party", "p_collective_friends"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_temp_party"),
        (assign, "$g_move_heroes", 1),
        (call_script, "script_party_add_party", "p_collective_friends", "p_temp_party"),
      (try_end),
  ]),

("consume_food",
   [(store_script_param, ":selected_food", 1),
    (troop_get_inventory_capacity, ":capacity", "trp_player"),
    (try_for_range, ":cur_slot", 0, ":capacity"),
      (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
      (is_between, ":cur_item", itm_raw_date_fruit, food_end),
      (neq, ":cur_item", "itm_furs"),
      (item_slot_eq, ":cur_item", slot_item_edible, 1),
      (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":cur_slot"),
      (neq, ":item_modifier", imod_rotten),
      #SB : TODO check for qst_deliver_wine items and prevent consumption
      (item_slot_eq, ":cur_item", slot_item_is_checked, 0),
      (item_set_slot, ":cur_item", slot_item_is_checked, 1),
      (val_sub, ":selected_food", 1),
      (lt, ":selected_food", 0),
      (assign, ":capacity", 0),
      (troop_inventory_slot_get_item_amount, ":cur_amount", "trp_player", ":cur_slot"),
      (val_sub, ":cur_amount", 1),
      (troop_inventory_slot_set_item_amount, "trp_player", ":cur_slot", ":cur_amount"),
    (try_end),
    ]),

("cf_party_remove_random_regular_troop",
    [(store_script_param_1, ":party_no"),
     (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
     (assign, ":num_troops", 0),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_add, ":num_troops", ":stack_size"),
     (try_end),
     (assign, reg0, -1),
     (gt, ":num_troops", 0),
     (store_random_in_range, ":random_troop", 0, ":num_troops"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (neg|troop_is_hero, ":stack_troop"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (val_sub, ":random_troop", ":stack_size"),
       (lt, ":random_troop", 0),
       (assign, ":num_stacks", 0), #break
       (party_remove_members, ":party_no", ":stack_troop", 1),
       (assign, reg0, ":stack_troop"),
     (try_end),
     ]),

("set_parties_around_player_ignore_player",
    [(store_script_param, ":ignore_range", 1),
     (store_script_param, ":num_hours", 2),
     (try_for_parties, ":party_no"),
       (party_is_active, ":party_no"),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":party_no"),
       (lt, ":dist", ":ignore_range"),
       (party_ignore_player, ":party_no", ":num_hours"),
     (try_end),
     ]),

("party_inflict_attrition", #parameters from dialog
	[
	(store_script_param, ":party", 1),
	(store_script_param, ":attrition_rate", 2),
#	(store_script_param, ":attrition_type", 3), #1 = desertion, 2 = sickness

    (party_clear, "p_temp_casualties"),

	(party_get_num_companion_stacks, ":num_stacks", ":party"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", ":party", ":stack"),
		(neg|troop_is_hero, ":troop_type"),
		(party_stack_get_size, ":size", ":party", ":stack"),
		(store_mul, ":casualties_x_100", ":attrition_rate", ":size"),
		(store_div, ":casualties", ":casualties_x_100", 100),
		(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),

		(store_mul, ":subtractor", ":casualties", 100),
		(store_sub, ":chance_of_additional_casualty", ":casualties_x_100", ":subtractor"),

		(try_begin),
			(gt, ":chance_of_additional_casualty", 0),
			(store_random_in_range, ":random", 0, 100),
			(lt, ":random", ":chance_of_additional_casualty"),
			(party_add_members, "p_temp_casualties", ":troop_type", ":casualties"),
		(try_end),

#		(try_begin),
#			(eq, "$cheat_mode", 1),
#			(str_store_party_name, s7, ":party"),
#           		...
#		(try_end),
	(try_end),

	#take temp casualties from main party
	(party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),

	#add to temp casualties
	(try_for_range, ":stack", 0, ":num_stacks"),
		(party_stack_get_troop_id, ":troop_type", "p_temp_casualties", ":stack"),
		(party_stack_get_size, ":size", "p_temp_casualties", ":stack"),
		(party_remove_members, ":party", ":troop_type", ":size"),

		(eq, "$cheat_mode", 1),
		(assign, reg3, ":size"),
		(str_store_troop_name, s4, ":troop_type"),
		(str_store_party_name, s5, ":party"),
#		(display_message, "str_s5_suffers_attrition_reg3_x_s4"),
		(str_store_string, s65, "str_s5_suffers_attrition_reg3_x_s4"),
		(display_message, "str_s65"),
		(try_begin),
			(eq, "$debug_message_in_queue", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, "$debug_message_in_queue", 1),
		(try_end),
	(try_end),

	]),

("party_heal_all_members_aux",
      [
        (store_script_param_1, ":party_no"),

        (party_get_num_companion_stacks, ":num_stacks",":party_no"),
        (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
          (try_begin),
            (neg|troop_is_hero, ":stack_troop"),
            # (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
            (party_stack_get_num_wounded, ":stack_size",":party_no",":i_stack"),
            (party_add_members, ":party_no", ":stack_troop", ":stack_size"),
            (party_remove_members_wounded_first, ":party_no", ":stack_troop", ":stack_size"),
          (else_try),
            (troop_set_health, ":stack_troop", 100),
          (try_end),
        (try_end),
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_party_heal_all_members_aux", ":attached_party"),
        (try_end),
      ]
    ),
]
