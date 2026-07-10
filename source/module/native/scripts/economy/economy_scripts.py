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
# ECONOMY & TRADE SCRIPTS
# 
# This file contains scripts that manage the global economy. It handles trade routes,
# item price calculations, trade penalties, and production normalizations.
####################################################################################################################

economy_scripts = [
  #
  # Input:
  # param1: troop_id,
  # Output: reg0

  ("get_trade_penalty",
    [
	##diplomacy start+
	##Changed to fall back to parameterized version
	##NEW:
      (store_script_param_1, ":item_kind_id"),
	  (call_script, "script_dplmc_get_trade_penalty", ":item_kind_id", "$g_encountered_party", "trp_player", "$g_talk_troop"),

	##OLD:
#	  (store_script_param_1, ":item_kind_id"),
#
#      (assign, ":penalty",0),
#
#      (party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
#      (try_begin),
#        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
#        (assign, ":penalty",15), #reduced slightly
#        (store_mul, ":skill_bonus", ":trade_skill", 1),
#        (val_sub, ":penalty", ":skill_bonus"),
#      (else_try),
#        (assign, ":penalty",100),
#        (store_mul, ":skill_bonus", ":trade_skill", 5),
#        (val_sub, ":penalty", ":skill_bonus"),
#      (try_end),
#
#	  ##diplomacy start+
#      (assign, ":penalty_multiplier", average_price_factor),#<-- replaced 1000 with average_price_factor
#	  ##diplomacy end+
###       # Apply penalty if player is hostile to merchants faction
###      (store_relation, ":merchants_reln", "fac_merchants", "fac_player_supporters_faction"),
###      (try_begin),
###        (lt, ":merchants_reln", 0),
###        (store_sub, ":merchants_reln_dif", 10, ":merchants_reln"),
###        (store_mul, ":merchants_relation_penalty", ":merchants_reln_dif", 20),
###        (val_add, ":penalty_multiplier", ":merchants_relation_penalty"),
###      (try_end),
#
#       # Apply penalty if player is on bad terms with the town
#      (try_begin),
#        (is_between, "$g_encountered_party", centers_begin, centers_end),
#        (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
#        (store_mul, ":center_relation_penalty", ":center_relation", -3),
#        (val_add, ":penalty_multiplier", ":center_relation_penalty"),
#        (try_begin),
#          (lt, ":center_relation", 0),
#          (store_sub, ":center_penalty_multiplier", 100, ":center_relation"),
#          (val_mul, ":penalty_multiplier", ":center_penalty_multiplier"),
#          (val_div, ":penalty_multiplier", 100),
#        (try_end),
#      (try_end),
#
#       # Apply penalty if player is on bad terms with the merchant (not currently used)
#      (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
#      (assign, ":troop_reln", reg0),
#      #(troop_get_slot, ":troop_reln", "$g_talk_troop", slot_troop_player_relation),
#      (try_begin),
#        (lt, ":troop_reln", 0),
#        (store_sub, ":troop_reln_dif", 0, ":troop_reln"),
#        (store_mul, ":troop_relation_penalty", ":troop_reln_dif", 20),
#        (val_add, ":penalty_multiplier", ":troop_relation_penalty"),
#      (try_end),
#
#
#	  (try_begin),
#		(is_between, "$g_encountered_party", villages_begin, villages_end),
#	    (val_mul, ":penalty", 2),
#	  (try_end),
#
#	  (try_begin),
#            (is_between, "$g_encountered_party", centers_begin, centers_end),
#	    #Double trade penalty if no local production or consumption
#	    (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
#		##diplomacy start+
#		#OPTIONAL CHANGE: Do not apply this to food
#       (this_or_next|lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
#		   (neg|is_between, ":item_kind_id", food_begin, food_end),
#		##diplomacy end+
#	    (call_script, "script_center_get_production", "$g_encountered_party", ":item_kind_id"),
#	    (eq, reg0, 0),
#	    (call_script, "script_center_get_consumption", "$g_encountered_party", ":item_kind_id"),
#	    (eq, reg0, 0),
#	    (val_mul, ":penalty", 2),
#	  (try_end),
#
#      (val_mul, ":penalty",  ":penalty_multiplier"),
#	  ##diplomacy start+
#	  (val_add, ":penalty", average_price_factor // 2),#round in the correct direction (we don't need to worry about penalty < 0)
#      (val_div, ":penalty", average_price_factor),#replace the hardcoded constant 1000 with average_price_factor
#	  ##diplomacy end+
#      (val_max, ":penalty", 1),
#      (assign, reg0, ":penalty"),
  ]),

  #script_game_event_buy_item:
("initialize_trade_routes",
	[
	  #SARGOTH - 10 routes
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_2"), #Sargoth - Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_4"), #Sargoth - Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_12"), #Sargoth - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_11"), #Sargoth - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_8"), #Sargoth - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_13"), #Sargoth - Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_7"), #Sargoth - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_9"), #Sargoth - Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_6"), #Sargoth - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_15"), #Sargoth - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_16"), #Sargoth - Dhirim

	  #TIHR- 8 Routes
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_4"), #Tihr- Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_6"), #Tihr - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_7"), #Tihr - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_15"), #Tihr - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_12"), #Tihr - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_8"), #Tihr - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_11"), #Tihr - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_16"), #Thir - Dhirim

	  #VELUCA - 8 Routes
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_7"), #Veluca- Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_5"), #Veluca - Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_15"), #Veluca - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_16"), #Veluca - Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_14"), #Veluca - Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_4"), #Veluca - Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_19"), #Veluca - Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_6"), #Veluca - Praven

	  #SUNO - 11 routes
	  #Sargoth, Tihr, Veluca
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_12"), #Suno - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_8"), #Suno - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_11"), #Suno - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_6"), #Suno - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_7"), #Suno - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_16"), #Suno - Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_5"), #Suno - Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_15"), #Suno - Yalen

	  #JELKALA - 6 ROUTES
      #Veluca, Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_15"), #Jelkala - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_6"), #Jelkala - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_7"), #Jelkala - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_19"), #Jelkala - Shariz

	  #PRAVEN - 7 ROUTES
	  #Tihr, Veluca, Suno, Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_7"), #Praven - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_15"), #Praven - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_16"), #Praven - Dhirim

	  #UXKHAL - 9 Routes
	  #Sargoth, Tihr, Suno, Jelkala, Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_15"), #Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_19"), #Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_14"), #Halmar

	  #REYVADIN - 9 Routes
	  #Suno, Sargoth
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_9"), #Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_11"), #Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_17"), #Ichamur

	  #KHUDAN - 9 Routes
	  #Sargoth, Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_11"), #Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_10"), #Tulga
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_18"), #Narra

	  #TULGA - 7 Routes
	  #Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_22"), #Bariyye
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_14"), #Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_20"), #Durquba

	  #CURAW - 9 Routes
	  #Khudan, Reyvadin, Sargoth, Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_14"), #Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_17"), #Ichamur

	  #WERCHEG - 7 Routes
	  #Sargoth, Suno, Reyvadin, Khudan, Curaw, Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_12", "p_town_13"), #Rivacheg

	  #RIVACHEG - 6 Routes
	  #Sargoth, Reyvadin, Khudan, Curaw, Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_17"), #Ichamur

	  #HALMAR- 11 Routes
	  #Veluca, Uxkhal, Tulga, Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_22"), #Bariyye
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_19"), #Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_16"), #Dhirim

	  #YALEN - 7 Routes
	  #Sargoth, Tihr, Veluca, Suno, Jelkala, Praven, Uxkhal

	  #DHIRIM - 13 Routes
	  #Sargoth, Thir, Veluca, Suno, Praven, Uxkhal, Reyvadin, Khudan, Curaw, Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_19"), #Shariz

	  #ICHAMUR - 7 Routes
      #Reyvadin, Khudan, Tulga, Curaw, Rivacheg, Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_17", "p_town_18"), #Narra

	  #NARRA - 9 Routes
      #Reyvadin, Khudan, Tulga, Halmar, Dhirim, Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_22"), #Bariyye

	  #SHARIZ - 8 Routes
      #Veluca, Jelkala, Uxkhal, Halmar, Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_22"), #Bariyye

	  #DURQUBA - 7 Routes
      #Tulga, Halmar, Dhirim, Narra, Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_22"), #Bariyye

	  #AHMERRAD - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_21", "p_town_22"), #Bariyye

	  #BARIYYE - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba, Ahmerrad

    #ZENDAR - 8 Routes
      #Sargoth, Tihr, Wercheg,Reyvadin, Curaw, Khudan, Rivacheg, Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_1"), #Zendar - Sargoth
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_2"), #Zendar - Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_12"), #Zendar - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_8"), #Zendar - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_11"), #Zendar - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_9"), #Zendar - Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_13"), #Zendar - Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_16"), #Zendar - Dhirim
	]),



      # INPUT: none (called only from game start?)
  #This is currently deprecated, as I was going to try to fine-tune production
  ("average_trade_good_productions",
    [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":center_no", towns_begin, towns_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 110),
          (store_sub, ":dist_factor", 110, ":cur_distance"),
          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_production", ":other_center", ":cur_good_slot"),
            (store_sub, ":prod_dif", ":center_production", ":other_center_production"),
            (gt, ":prod_dif", 0),
            (store_mul, ":prod_dif_change", ":prod_dif", 1),
##            (try_begin),
##              (is_between, ":center_no", towns_begin, towns_end),
##              (is_between, ":other_center", towns_begin, towns_end),
##              (val_mul, ":cur_distance", 2),
##            (try_end),
            (val_mul ,":prod_dif_change", ":dist_factor"),
            (val_div ,":prod_dif_change", 110),
            (val_add, ":other_center_production", ":prod_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_production"),
          (try_end),
        (try_end),
      (try_end),
  ]),

  #script_normalize_trade_good_productions
  #Adjusts productions according to the amount of the item produced
  # INPUT: none
  # This currently deprecated, as I was going to try to fine-tune productions
  ("normalize_trade_good_productions",
    [
      (store_sub, ":item_to_slot", slot_town_trade_good_productions_begin, trade_goods_begin),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (assign, ":total_production", 0),
        (assign, ":num_centers", 0),
        (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (val_add, ":num_centers", 1),
          (try_begin),
            (is_between, ":center_no", towns_begin, towns_end), #each town is weighted as 5 villages...
            (val_add, ":num_centers", 4),
          (try_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_add, ":total_production", ":center_production"),
        (try_end),
        (store_div, ":new_production_difference", ":total_production", ":num_centers"),
        (neq, ":new_production_difference", 0),
        (try_for_range, ":center_no", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
          (is_between, ":center_no", villages_begin, villages_end),
          (party_get_slot, ":center_production", ":center_no", ":cur_good_slot"),
          (val_sub, ":center_production", ":new_production_difference"),
          (party_set_slot, ":center_no", ":cur_good_slot", ":center_production"),
        (try_end),
      (try_end),
  ]),

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
  ]),

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

	]),




  #script_get_poorest_village_of_faction
("dplmc_get_item_buy_price_factor",
    [
	##nested diplomacy start+
    #(store_script_param_1, ":item_kind_id"),
    #(store_script_param_2, ":center_no"),
	#Add two parameters
	(store_script_param, ":item_kind_id", 1),
	(store_script_param, ":center_no", 2),
	(store_script_param, ":customer_no", 3),
	(store_script_param, ":merchant_no", 4),
	##nested diplomacy start+
    (assign, ":price_factor", 100),

	##nested diplomacy start+
    #(call_script, "script_get_trade_penalty", ":item_kind_id"),
	(call_script, "script_dplmc_get_trade_penalty", ":item_kind_id", ":center_no", ":customer_no", ":merchant_no"),
	##nested diplomacy end+
    (assign, ":trade_penalty", reg0),

    (try_begin),
	  ##nested diplomacy start+
	  (gt, ":center_no", 0),
  	  (this_or_next|is_between, ":center_no", centers_begin, centers_end),
		(party_is_active, ":center_no"),

	  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
	  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
	  ##nested diplomacy end+
      (is_between, ":center_no", centers_begin, centers_end),
      (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
      (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
      (val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
      (party_get_slot, ":price_factor", ":center_no", ":item_slot_no"),

      (try_begin),
		##nested diplomacy start+
		#OLD:
        #(is_between, ":center_no", villages_begin, villages_end),
        #(party_get_slot, ":market_town", ":center_no", slot_village_market_town),
		##NEW:
		(gt, ":center_no", 0),
		(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_village),
			(is_between, ":center_no", villages_begin, villages_end),
		(party_get_slot, ":market_town", ":center_no", slot_village_market_town),

		(ge, ":market_town", centers_begin),
		(this_or_next|party_slot_eq, ":market_town", slot_party_type, spt_town),
		(this_or_next|party_slot_eq, ":market_town", slot_party_type, spt_village),
			(is_between, ":market_town", centers_begin, centers_end),
		##nested diplomacy end+
        (party_get_slot, ":price_in_market_town", ":market_town", ":item_slot_no"),
        (val_max, ":price_factor", ":price_in_market_town"),
      (try_end),
	  ##nested diplomacy start+
	  #Enforce constraints
	  (val_clamp, ":price_factor", minimum_price_factor, maximum_price_factor + 1),
	  ##nested diplomacy end+

      #For villages, the good will be sold no cheaper than in the market town
      #This represents the absence of a permanent market -- ie, the peasants retain goods to sell on their journeys to town, and are not about to do giveaway deals with passing adventurers

      (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
      (val_div, ":price_factor", average_price_factor),
    (try_end),

    (store_add, ":penalty_factor", 100, ":trade_penalty"),

    (val_mul, ":price_factor", ":penalty_factor"),
    (val_div, ":price_factor", 100),

    (assign, reg0, ":price_factor"),
    (set_trigger_result, reg0),
  ]),

  
  # script_dplmc_get_trade_penalty
  #
  #This is similar to the old script_get_trade_penalty,
  #except it uses parameters instead of relying on global variables.
  #
  # Input:
  # param1: item_kind_id
  # param2: market center
  # param3: customer troop (-1 for a non-troop-specific answer, -2 to notify the script that this is being used to evaluate a gift)
  # param4: merchant troop (-1 for a non-troop-specific answer)
  # Output: reg0

  ("dplmc_get_trade_penalty",
    [
	  #Additions begin:
      (store_script_param, ":item_kind_id", 1),
      (store_script_param, ":market_center", 2),
      (store_script_param, ":customer_troop", 3),
      (store_script_param, ":merchant_troop", 4),
      #End Additions
      (assign, ":penalty",0),

	  ##Change this to support alternative customers
      ##(party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
	  (try_begin),
		 #Player: use skill of player party
	     (eq, ":customer_troop", "trp_player"),
		 (party_get_skill_level, ":trade_skill", "p_main_party", skl_trade),
	  (else_try),
		 #Hero leading a party: use skill of led party
	     (gt, ":customer_troop", -1),
	     (troop_is_hero, ":customer_troop"),
		 (troop_get_slot, ":customer_party", ":customer_troop", slot_troop_leaded_party),
		 (gt, ":customer_party", 0),
		 (party_is_active, ":customer_party"),
		 (party_get_skill_level, ":trade_skill", ":customer_party", skl_trade),
	  (else_try),
		 #Troop: use troop skill
		 (gt, ":customer_troop", -1),
		 (store_skill_level, ":trade_skill", ":customer_troop"),
	  (else_try),
		 (assign, ":trade_skill", 0),
	  (try_end),
	  ##End Change
      (try_begin),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (assign, ":penalty",15), #reduced slightly
        (store_mul, ":skill_bonus", ":trade_skill", 1),
        (val_sub, ":penalty", ":skill_bonus"),
      (else_try),
        (assign, ":penalty",100),
        (store_mul, ":skill_bonus", ":trade_skill", 5),
        (val_sub, ":penalty", ":skill_bonus"),
      (try_end),

      (assign, ":penalty_multiplier", average_price_factor),#<-- replaced 1000 with average_price_factor
##       # Apply penalty if player is hostile to merchants faction
##      (store_relation, ":merchants_reln", "fac_merchants", "fac_player_supporters_faction"),
##      (try_begin),
##        (lt, ":merchants_reln", 0),
##        (store_sub, ":merchants_reln_dif", 10, ":merchants_reln"),
##        (store_mul, ":merchants_relation_penalty", ":merchants_reln_dif", 20),
##        (val_add, ":penalty_multiplier", ":merchants_relation_penalty"),
##      (try_end),

       # Apply penalty if player is on bad terms with the town
      (try_begin),
		(eq, ":customer_troop", "trp_player"),#added
        (is_between, ":market_center", centers_begin, centers_end),#changed $g_encountered_party to :market_center
        (party_get_slot, ":center_relation", ":market_center", slot_center_player_relation),#changed $g_encountered_party to :market_center
        (store_mul, ":center_relation_penalty", ":center_relation", -3),
        (val_add, ":penalty_multiplier", ":center_relation_penalty"),
        (try_begin),
          (lt, ":center_relation", 0),
          (store_sub, ":center_penalty_multiplier", 100, ":center_relation"),
          (val_mul, ":penalty_multiplier", ":center_penalty_multiplier"),
          (val_div, ":penalty_multiplier", 100),
        (try_end),
      (try_end),

       # Apply penalty if player is on bad terms with the merchant (not currently used)
	   ##Begin Change
      #(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
      #(assign, ":troop_reln", reg0),
	  (try_begin),
		 (this_or_next|eq, ":merchant_troop", "trp_player"),
			(eq, ":customer_troop", "trp_player"),
		 (gt, ":merchant_troop", -1),
		 (gt, ":customer_troop", -1),
		 (call_script, "script_troop_get_player_relation", ":merchant_troop"),
		 (assign, ":troop_reln", reg0),
	  (else_try),
	    (is_between, ":merchant_troop", heroes_begin, heroes_end),
		 (is_between, ":customer_troop", heroes_begin, heroes_end),
		 (call_script, "script_troop_get_relation_with_troop", ":merchant_troop", ":customer_troop"),
		 (assign, ":troop_reln", reg0),
	  (else_try),
	     (assign, ":troop_reln", 0),
	  (try_end),
	  ##End Change
      #(troop_get_slot, ":troop_reln", "$g_talk_troop", slot_troop_player_relation),
      (try_begin),
        (lt, ":troop_reln", 0),
        (store_sub, ":troop_reln_dif", 0, ":troop_reln"),
        (store_mul, ":troop_relation_penalty", ":troop_reln_dif", 20),
        (val_add, ":penalty_multiplier", ":troop_relation_penalty"),
      (try_end),


	  (try_begin),
		##Begin Change
		#(is_between, "$g_encountered_party", villages_begin, villages_end),
		(is_between, ":market_center", centers_begin, centers_end),
		(party_slot_eq, ":market_center", slot_party_type, spt_village),
		##End Change
	    (val_mul, ":penalty", 2),
	  (try_end),

	  (try_begin),
        (is_between, ":market_center", centers_begin, centers_end),#changed $g_encountered_party to :market_center
	    #Double trade penalty if no local production or consumption
	    (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
		##Begin Change
		#(OPTIONAL CHANGE: Do not apply this to food)
		(this_or_next|eq, ":customer_troop", -2),
        (this_or_next|lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		   (neg|is_between, ":item_kind_id", food_begin, food_end),

		(assign, ":save_reg1", reg1),
		(assign, ":save_reg2", reg2),
		##End Change
	    (call_script, "script_center_get_production", ":market_center", ":item_kind_id"),#changed $g_encountered_party to :market_center
	    (eq, reg0, 0),
	    (call_script, "script_center_get_consumption", ":market_center", ":item_kind_id"),#changed $g_encountered_party to :market_center
	    (eq, reg0, 0),
	    (val_mul, ":penalty", 2),
		##Begin Change
		(assign, reg1, ":save_reg1"),
		(assign, reg2, ":save_reg2"),
		##End Change
	  (try_end),

      (val_mul, ":penalty",  ":penalty_multiplier"),
	  ##Begin Change
	  (val_add, ":penalty", average_price_factor // 2),#round in the correct direction (we don't need to worry about penalty < 0)
      (val_div, ":penalty", average_price_factor),#replace the hardcoded constant 1000 with average_price_factor
	  ##End Change
      (val_max, ":penalty", 1),
      (assign, reg0, ":penalty"),
  ]),


##"script_dplmc_print_cultural_word_to_sreg"
  # generally this is used to move the backup to the player
  # Input: arg1 = source, arg2 = destnation
  # Output: none

  ("move_inventory_and_gold",
    [
      (store_script_param, ":source", 1),
      (store_script_param, ":destination", 2),
      (store_script_param, ":move_gold", 3),
      #assume trp_temp_troop is an available placeholder

      (troop_sort_inventory, ":source"), #order them, too lazy to maintain 2 loops
      (troop_get_inventory_capacity, ":inv_cap", ":source"),
      (troop_get_inventory_capacity, ":player_cap", ":destination"),
      (assign, ":inv_slot", ek_food + 1), #start from the bottom, skip source's equipment
      (try_for_range, ":i_slot", ek_food + 1, ":player_cap"),
        (troop_get_inventory_slot, ":cur_item", ":destination", ":i_slot"),
        (eq, ":cur_item", -1), #empty slot
        (troop_get_inventory_slot, ":item", ":source", ":inv_slot"),
        (troop_set_inventory_slot, ":destination", ":i_slot", ":item"),
        #(try_begin),
          #(neq, ":cur_item", -1), #?????
          (troop_get_inventory_slot_modifier, ":imod", ":source", ":inv_slot"),
          (troop_set_inventory_slot_modifier, ":destination", ":i_slot", ":imod"),
          (try_begin),
            (troop_inventory_slot_get_item_amount, ":amount", ":source", ":inv_slot"),
            (gt, ":amount", 0),
            (troop_inventory_slot_set_item_amount, ":destination", ":i_slot", ":amount"),
          (try_end),
        #(try_end),
        (troop_set_inventory_slot, ":source", ":inv_slot", -1),
        (val_add, ":inv_slot", 1),

        (try_begin), #loop break
          (ge, ":inv_slot", ":inv_cap"),
          (assign, ":player_cap", -1),
        (try_end),
      (try_end),
      (troop_clear_inventory, ":source"), #clear off the rest if no capacity in destination
      #do gold addition
      (try_begin),
        (eq, ":move_gold", -1), #move all
        (store_troop_gold, ":cur_amount", ":source"),
        (troop_remove_gold, ":source", ":cur_amount"),
        (troop_add_gold, ":destination", ":cur_amount"),
      (else_try),
        (gt, ":move_gold", 0),  #specific amount
        (call_script, "script_troop_transfer_gold", ":source", ":destination", ":move_gold"),
      (try_end),
    ]),

   #script_get_disguise_string

#Autotrade begin
  # script_initialize_auto_trade
  ("initialize_auto_trade",
  [
    (assign, "$g_auto_trade_minimum_wealth", 1000), 
    (assign, "$g_auto_trade_items_when_leaving", 0),

    (try_for_range, ":cur_item", trade_goods_begin, trade_goods_end),
        (store_item_value, ":item_value", ":cur_item"),
        (store_mul, ":buy_price", ":item_value", 80),
        (val_div, ":buy_price", 100),
        (item_set_slot, ":cur_item", slot_item_auto_trade_buy_under_price, ":buy_price"),
        (item_set_slot, ":cur_item", slot_item_auto_trade_sell_over_price, ":item_value"),
        (item_set_slot, ":cur_item", slot_item_auto_trade_buy_enabled, 1),
        (item_set_slot, ":cur_item", slot_item_auto_trade_sell_enabled, 1),
        (item_set_slot, ":cur_item", slot_item_auto_trade_min_quantity, 0),
        (item_set_slot, ":cur_item", slot_item_auto_trade_max_quantity, 0),
    (try_end),
  ]),

  # script_auto_trade_at_center
]
