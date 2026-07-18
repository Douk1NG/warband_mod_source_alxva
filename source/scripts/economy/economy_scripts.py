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

("average_trade_good_prices", #Called from start
    [

	#This should be done by route rather than distance
      (store_sub, ":item_to_slot", slot_town_trade_good_prices_begin, trade_goods_begin),

      (try_for_range, ":center_no", towns_begin, towns_end),
        (this_or_next|is_between, ":center_no", towns_begin, towns_end),
		(is_between, ":center_no", villages_begin, villages_end),

        (try_for_range, ":other_center", centers_begin, centers_end),
          (this_or_next|is_between, ":center_no", towns_begin, towns_end),
		  (is_between, ":center_no", villages_begin, villages_end),

          (neq, ":other_center", ":center_no"),
          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":other_center"),
          (lt, ":cur_distance", 50), #Reduced from 110
          (store_sub, ":dist_factor", 50, ":cur_distance"),

          (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
            (store_add, ":cur_good_slot", ":cur_good", ":item_to_slot"),
            (party_get_slot, ":center_price", ":center_no", ":cur_good_slot"),
            (party_get_slot, ":other_center_price", ":other_center", ":cur_good_slot"),
            (store_sub, ":price_dif", ":center_price", ":other_center_price"),

            (assign, ":price_dif_change", ":price_dif"),

            (val_mul ,":price_dif_change", ":dist_factor"),
            (val_div ,":price_dif_change", 1000), #Maximum of 1/20 per center
            (val_add, ":other_center_price", ":price_dif_change"),
            (party_set_slot, ":other_center", ":cur_good_slot", ":other_center_price"),

            (val_sub, ":center_price", ":price_dif_change"),
            (party_set_slot, ":center_no", ":cur_good_slot", ":center_price"),
          (try_end),
        (try_end),
      (try_end),
  ]),

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
  ]),

("update_trade_good_price_for_party",
    [
      (store_script_param, ":center_no", 1),
      (try_for_range, ":cur_good", trade_goods_begin, trade_goods_end),
        (store_sub, ":cur_good_price_slot", ":cur_good", trade_goods_begin),
        (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
		(party_get_slot, ":cur_price", ":center_no", ":cur_good_price_slot"),

        (call_script, "script_center_get_production", ":center_no", ":cur_good"),
		(assign, ":production", reg0),

        (call_script, "script_center_get_consumption", ":center_no", ":cur_good"),
		(assign, ":consumption", reg0),

		#OZANDEBUG
		#(assign, reg1, ":production"),
		#(assign, reg2, ":consumption"),
		#(str_store_party_name, s1, ":center_no"),
		#(str_store_item_name, s2, ":cur_good"),

		(val_sub, ":production", ":consumption"),

		#Change average production x 2(1+random(2)) (was average 4, random(8)) for excess demand
        (try_begin),
		  #supply is greater than demand
          (gt, ":production", 0),
		  (store_mul, ":change_factor", ":production", 1), #price will be decreased by his factor
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),

		  #simulation starts
          (store_sub, ":final_price", ":cur_price", ":random_change"),
		  (val_clamp, ":final_price", minimum_price_factor, maximum_price_factor),
		  (try_begin), #Excess of supply decelerates over time, as low price reduces output
		    #if expected final price is 100 then it will multiply random_change by 0.308x ((100+300)/(1300) = 400/1300).
			(lt, ":final_price", 1000),
			(store_add, ":final_price_plus_300", ":final_price", 300),
			(val_mul, ":random_change", ":final_price_plus_300"),
			(val_div, ":random_change", 1300),
		  (try_end),
          (val_sub, ":cur_price", ":random_change"),
        (else_try),
          (lt, ":production", 0),
		  (store_sub, ":change_factor", 0, ":production"), #price will be increased by his factor
		  (val_mul, ":change_factor", 1),
		  (store_random_in_range, ":random_change", 0, ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
		  (val_add, ":random_change", ":change_factor"),
          (val_add, ":cur_price", ":random_change"),
        (try_end),

        #Move price towards average by 3%...
		#Equilibrium is 33 cycles, or 100 days
		#Change per cycle is Production x 4
		#Thus, max differential = -5 x 4 x 33 = -660 for -5
		(try_begin),
		  (is_between, ":center_no", villages_begin, villages_end),
        (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
        (val_div, ":price_difference", 100),
        (store_add, ":new_price", average_price_factor, ":price_difference"),
        (else_try),
          (store_sub, ":price_difference", ":cur_price", average_price_factor),
          (val_mul, ":price_difference", 96),
          (val_div, ":price_difference", 100),
          (store_add, ":new_price", average_price_factor, ":price_difference"),
        (try_end),

		#Price of manufactured goods drift towards primary raw material
		(try_begin),
			(item_get_slot, ":raw_material", ":cur_good", slot_item_primary_raw_material),
            (neq, ":raw_material", 0),
	        (store_sub, ":raw_material_price_slot", ":raw_material", trade_goods_begin),
	        (val_add, ":raw_material_price_slot", slot_town_trade_good_prices_begin),

			(party_get_slot, ":total_raw_material_price", ":center_no", ":raw_material_price_slot"),
			(val_mul, ":total_raw_material_price", 3),
            (assign, ":number_of_centers", 3),

			(try_for_range, ":village_no", villages_begin, villages_end),
			  (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
			  (party_get_slot, ":raw_material_price", ":village_no", ":raw_material_price_slot"),
			  (val_add, ":total_raw_material_price", ":raw_material_price"),
			  (val_add, ":number_of_centers", 1),
            (try_end),

			(store_div, ":average_raw_material_price", ":total_raw_material_price", ":number_of_centers"),

			(gt, ":average_raw_material_price", ":new_price"),
			(store_sub, ":raw_material_boost", ":average_raw_material_price", ":new_price"),
			(val_div, ":raw_material_boost", 10),
			(val_add, ":new_price", ":raw_material_boost"),
		(try_end),

        (val_clamp, ":new_price", minimum_price_factor, maximum_price_factor),
        (party_set_slot, ":center_no", ":cur_good_price_slot", ":new_price"),

		#(assign, reg3, ":new_price"),
		#(str_store_item_name, s2, ":cur_good"),
		#(display_log_message, "@DEBUG : {s1}-{s2}, prod:{reg1}, cons:{reg2}, price:{reg3}"),
      (try_end),
  ]),

("get_enterprise_name",
    [
		(store_script_param_1, ":item_produced"),
		(assign, ":enterprise_name", "str_bread_site"),
		(try_begin),
			(eq, ":item_produced", "itm_bread"),
			(assign, ":enterprise_name", "str_bread_site"),
		(else_try),
			(eq, ":item_produced", "itm_ale"),
			(assign, ":enterprise_name", "str_ale_site"),
		(else_try),
			(eq, ":item_produced", "itm_oil"),
			(assign, ":enterprise_name", "str_oil_site"),
		(else_try),
			(eq, ":item_produced", "itm_wine"),
			(assign, ":enterprise_name", "str_wine_site"),
		(else_try),
			(eq, ":item_produced", "itm_leatherwork"),
			(assign, ":enterprise_name", "str_leather_site"),
		(else_try),
			(eq, ":item_produced", "itm_wool_cloth"),
			(assign, ":enterprise_name", "str_wool_cloth_site"),
		(else_try),
			(eq, ":item_produced", "itm_linen"),
			(assign, ":enterprise_name", "str_linen_site"),
		(else_try),
			(eq, ":item_produced", "itm_velvet"),
			(assign, ":enterprise_name", "str_velvet_site"),
		(else_try),
			(eq, ":item_produced", "itm_tools"),
			(assign, ":enterprise_name", "str_tool_site"),
		(try_end),
		(assign, reg0, ":enterprise_name"),
	]),

("party_calculate_loot",
    [
      (store_script_param_1, ":enemy_party"), #Enemy Party_id

      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),

      (try_for_range, ":i_loot", 0, num_party_loot_slots),
        (store_add, ":cur_loot_slot", ":i_loot", slot_party_looted_item_1),
        (party_get_slot, ":item_no", "$g_enemy_party", ":cur_loot_slot"),
        (gt, ":item_no", 0),
        (party_set_slot, "$g_enemy_party", ":cur_loot_slot", 0),
        (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
        (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
        (party_get_slot, ":item_modifier", "$g_enemy_party", ":cur_loot_slot"),
        (troop_add_item, "trp_temp_troop", ":item_no", ":item_modifier"),
      (try_end),
      (party_set_slot, "$g_enemy_party", slot_party_next_looted_item_slot, 0),

      (assign, ":num_looted_items",0),
      (try_begin),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
        (this_or_next|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
        (party_slot_eq, "$g_enemy_party", slot_party_type, spt_village_farmer),
        (store_mul, ":plunder_amount", player_loot_share, 30),
        (val_mul, ":plunder_amount", "$g_strength_contribution_of_player"),
        (val_div, ":plunder_amount", 100),
        (val_div, ":plunder_amount", ":num_player_party_shares"),
        (try_begin),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
          (reset_item_probabilities, 100),
          (assign, ":range_min", trade_goods_begin),
          (assign, ":range_max", trade_goods_end),
        (else_try),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
          (val_div, ":plunder_amount", 2),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (else_try),
          (val_div, ":plunder_amount", 5),
          (reset_item_probabilities, 1),
          (assign, ":range_min", food_begin),
          (assign, ":range_max", food_end),
        (try_end),
        (store_sub, ":item_to_price_slot", slot_town_trade_good_prices_begin, trade_goods_begin),
        (try_for_range, ":cur_goods", ":range_min", ":range_max"),
          (try_begin),
            (neg|party_slot_eq, "$g_enemy_party", slot_party_type, spt_bandit_lair),
            (store_add, ":cur_price_slot", ":cur_goods", ":item_to_price_slot"),
            (party_get_slot, ":cur_price", "$g_enemy_party", ":cur_price_slot"),
          (else_try),
            (assign, ":cur_price", maximum_price_factor),
            (val_add, ":cur_price", average_price_factor),
            (val_div, ":cur_price", 3),
          (try_end),

          (assign, ":cur_probability", 100),
          (val_mul, ":cur_probability", average_price_factor),
          (val_div, ":cur_probability", ":cur_price"),
          (assign, reg0, ":cur_probability"),
          (set_item_probability_in_merchandise, ":cur_goods", ":cur_probability"),
        (try_end),
        (troop_add_merchandise, "trp_temp_troop", itp_type_goods, ":plunder_amount"),
        (val_add, ":num_looted_items", ":plunder_amount"),
      (try_end),

      #Now loot the defeated party
      (store_mul, ":loot_probability", player_loot_share, 3),
      (val_mul, ":loot_probability", "$g_strength_contribution_of_player"),
      (party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
      (val_add, ":player_party_looting", 10),
      (val_mul, ":loot_probability", ":player_party_looting"),
      (val_div, ":loot_probability", 10),
      (val_div, ":loot_probability", ":num_player_party_shares"),

      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      ###(((sort troops of enemy_party by level
      (assign, ":last_stack", ":num_stacks"),
      (try_for_range, ":unused", 0, ":num_stacks"),
        (assign, ":best_stack", -1),
        (assign, ":best_level", -999999),
        (try_for_range, ":cur_stack", 0, ":last_stack"),
          (party_stack_get_troop_id, ":cur_troop", ":enemy_party", ":cur_stack"),
          (neg|troop_is_hero, ":cur_troop"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (gt, ":cur_level", ":best_level"),
          (assign, ":best_level", ":cur_level"),
          (assign, ":best_stack", ":cur_stack"),
        (try_end),
        (gt, ":best_stack", -1),
        (party_stack_get_troop_id, ":stack_troop", ":enemy_party", ":best_stack"),
        (party_stack_get_size, ":stack_size", ":enemy_party", ":best_stack"),
        (party_remove_members, ":enemy_party", ":stack_troop", ":stack_size"),
        (party_add_members, ":enemy_party", ":stack_troop", ":stack_size"),
        (val_sub, ":last_stack", 1),
      (try_end),
      ###)))
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (try_for_range, ":unused", 0, ":stack_size"),
          (troop_loot_troop, "trp_temp_troop", ":stack_troop", ":loot_probability"),
        (try_end),
      (try_end),

      #(troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      #(try_for_range, ":i_slot", 0, ":inv_cap"),
      #  (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
      #  (is_between, ":item_id", horses_begin, horses_end),
      #  (troop_set_inventory_slot, "trp_temp_troop", ":i_slot", -1),
      #(try_end),

      (troop_get_inventory_capacity, ":inv_cap", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (ge, ":item_id", 0),
        (val_add, ":num_looted_items", 1),
      (try_end),

      (assign, reg0, ":num_looted_items"),
  ]),

("calculate_main_party_shares",
    [
      (assign, ":num_player_party_shares", player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),

      (assign, reg0, ":num_player_party_shares"),
  ]),

("calculate_weekly_party_wage",
    [
      (store_script_param_1, ":party_no"),

      (assign, ":result", 0),
      (party_get_num_companion_stacks, ":num_stacks",":party_no"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (party_stack_get_size, ":stack_size",":party_no",":i_stack"),
        (call_script, "script_npc_get_troop_wage", ":stack_troop", ":party_no"),
        (assign, ":cur_wage", reg0),
        (val_mul, ":cur_wage", ":stack_size"),
        (val_add, ":result", ":cur_wage"),
      (try_end),
      (assign, reg0, ":result"),
  ]),

("create_cattle_herd",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":amount"),

      (assign, ":herd_party", -1),
      (set_spawn_radius,1),

      (spawn_around_party,":center_no", "pt_cattle_herd"),
      (assign, ":herd_party", reg0),
      (party_get_position, pos1, ":center_no"),
      (call_script, "script_map_get_random_position_around_position_within_range", 1, 2),
      (party_set_position, ":herd_party", pos2),

      (party_set_slot, ":herd_party", slot_party_type, spt_cattle_herd),
      (party_set_slot, ":herd_party", slot_party_ai_state, spai_undefined),
      (party_set_ai_behavior, ":herd_party", ai_bhvr_hold),

      (party_set_slot, ":herd_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      (try_begin),
        (gt, ":amount", 0),
        (party_clear, ":herd_party"),
        (party_add_members, ":herd_party", "trp_cattle", ":amount"),
      (try_end),

      (assign, reg0, ":herd_party"),
  ]),

("kill_cattle_from_herd",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":amount"),

      (troop_clear_inventory, "trp_temp_troop"),
      (store_mul, ":meat_amount", ":amount", 2),
      (troop_add_items, "trp_temp_troop", "itm_cattle_meat", ":meat_amount"),

      (troop_get_inventory_capacity, ":inv_size", "trp_temp_troop"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":item_id", "trp_temp_troop", ":i_slot"),
        (eq, ":item_id", "itm_cattle_meat"),
        (troop_set_inventory_slot_modifier, "trp_temp_troop", ":i_slot", imod_fresh),
      (try_end),

      (party_get_num_companions, ":num_cattle", ":party_no"),
      (try_begin),
        (ge, ":amount", ":num_cattle"),
        (remove_party, ":party_no"),
      (else_try),
        (party_remove_members, ":party_no", "trp_cattle", ":amount"),
      (try_end),
      ]),

("change_debt_to_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":new_debt"),

      (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),
      (assign, reg1, ":cur_debt"),
      (val_add, ":cur_debt", ":new_debt"),
      (assign, reg2, ":cur_debt"),
      (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (try_begin), #SB : display only if > 0
        (gt, ":cur_debt", 0),
        (str_store_troop_name_link, s1, ":troop_no"),
        (display_message, "@You now owe {reg2} denars to {s1}.", message_negative),
      (try_end),
  ]),

("update_ransom_brokers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, 0),
     (try_end),

     (try_for_range, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
       #SB : random-brokers prefer towns with actual prisoners
       (assign, ":limit", 20),
       (try_for_range, ":unused", 0, ":limit"), #also exclude Tihr since it has Ramun
          (store_random_in_range, ":town_no", towns_begin, towns_end),
          (neq, ":town_no", "p_town_2"),
          (neq, ":town_no", "p_town_19"),
          #also exclude centers under siege
          (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1),
          (party_get_num_prisoners, ":prisoner_count", ":town_no"),
          (gt, ":prisoner_count", 0),
          (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
          (assign, ":limit", 0), #loop breaker
       (try_end),
       (eq, ":limit", 20), #none found
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_ransom_broker, ":troop_no"),
     (try_end),

     (party_set_slot,"p_town_2",slot_center_ransom_broker,"trp_ramun_the_slave_trader"),
     (party_set_slot,"p_town_19",slot_center_ransom_broker,"trp_galeas"),
     ]),

("update_booksellers",
    [(try_for_range, ":town_no", towns_begin, towns_end),
       (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1), #keep them there
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, 0),
     (try_end),

     (try_for_range, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
       (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
       (neg|party_slot_ge, ":cur_center", slot_center_is_besieged_by, 1), #can't travel
       (store_random_in_range, ":town_no", towns_begin, towns_end),
       (party_set_slot, ":town_no", slot_center_tavern_bookseller, ":troop_no"),
       (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
     (try_end),



     ]),

("get_improvement_details",
    [(store_script_param, ":improvement_no", 1),
     (try_begin),
       (eq, ":improvement_no", slot_center_has_manor),
       (str_store_string, s0, "@Manor"),
       (str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you rest."),
       (assign, reg0, 8000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_fish_pond),
       (str_store_string, s0, "@Mill"),
       (str_store_string, s1, "@A mill increases village prosperity by 5%."),
       (assign, reg0, 6000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_watch_tower),
       (str_store_string, s0, "@Watch Tower"),
       (str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for enemies to loot the village increases by 50%."),
       (assign, reg0, 5000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_school),
       (str_store_string, s0, "@School"),
       (str_store_string, s1, "@A shool increases the loyality of the villagers to you by +1 every month."),
       (assign, reg0, 9000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_messenger_post),
       (str_store_string, s0, "@Messenger Post"),
       (str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are nearby, even if you are far away from here."),
       (assign, reg0, 4000),
     (else_try),
       (eq, ":improvement_no", slot_center_has_prisoner_tower),
       (str_store_string, s0, "@Prison Tower"),
       (str_store_string, s1, "@A prison tower reduces the chance of captives held here running away successfully."),
       (assign, reg0, 7000),
     (try_end),
     ]),

("calculate_ransom_amount_for_troop",
    [(store_script_param, ":troop_no", 1),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (assign, ":ransom_amount", 400),

	 (assign, ":male_relative", -9), #for kingdom ladies, otherwise a number otherwise unused in slot_town_lord
     (try_begin),
       (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
       (val_add, ":ransom_amount", 4000),
	 (else_try),
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
       (val_add, ":ransom_amount", 2500), #as though a renown of 1250 -- therefore significantly higher than for roughly equivalent lords
	   (call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
	   (assign, ":male_relative", reg0),
     (try_end),

     (assign, ":num_center_points", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
		 (party_slot_eq, ":cur_center", slot_town_lord, ":male_relative"),
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
     (val_mul, ":num_center_points", 500),
     (val_add, ":ransom_amount", ":num_center_points"),
     (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
     (val_mul, ":renown", 2),
     (val_add, ":ransom_amount", ":renown"),
     (store_mul, ":ransom_max_amount", ":ransom_amount", 3),
     (val_div, ":ransom_max_amount", 2),
     (store_random_in_range, ":random_ransom_amount", ":ransom_amount", ":ransom_max_amount"),
     (val_div, ":random_ransom_amount", 100),
     (val_mul, ":random_ransom_amount", 100),
     (assign, reg0, ":random_ransom_amount"),
     ]),

("offer_ransom_amount_to_player_for_prisoners_in_party",
    [(store_script_param, ":party_no", 1),
     (assign, ":result", 0),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (eq, ":result", 0),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (this_or_next|troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_lady),
       (store_troop_faction, ":stack_troop_faction", ":stack_troop"),
       (store_random_in_range, ":random_no", 0, 100),
       (try_begin),
         (faction_slot_eq, ":stack_troop_faction", slot_faction_state, sfs_active),
         (le, ":random_no", 5),
         (neq, "$g_ransom_offer_rejected", 1),
         (assign, ":num_stacks", 0), #break
         (assign, ":result", 1),
         (assign, "$g_ransom_offer_troop", ":stack_troop"),
         (assign, "$g_ransom_offer_party", ":party_no"),
         (jump_to_menu, "mnu_enemy_offer_ransom_for_prisoner"),
       (try_end),
     (try_end),

     #SB : offer ransom for kingdom ladies as per conditions in dialogues
     (try_begin),
       (is_between, ":party_no", walled_centers_begin, walled_centers_end),
       (assign, ":end", kingdom_ladies_end),
       (store_faction_of_party, ":faction_no", ":party_no"),
       (try_for_range, ":heroes", kingdom_ladies_begin, ":end"),
         (troop_slot_eq, ":heroes", slot_troop_cur_center, ":party_no"),
         (troop_slot_eq, ":heroes", slot_troop_prisoner_of_party, ":party_no"),
         (troop_slot_eq, ":heroes", slot_troop_occupation, slto_kingdom_lady),
         (store_faction_of_troop, ":lady_faction", ":heroes"),
         (neq, ":lady_faction", ":faction_no"),
         (faction_slot_eq, ":lady_faction", slot_faction_state, sfs_active),
         (store_random_in_range, ":random_no", 0, 100),
         (le, ":random_no", 5),
         (neq, "$g_ransom_offer_rejected", 1),
         (assign, ":end", 0), #break
         (assign, ":result", 1),
         (assign, "$g_ransom_offer_troop", ":heroes"),
         (assign, "$g_ransom_offer_party", ":party_no"),
         (jump_to_menu, "mnu_enemy_offer_ransom_for_prisoner"),
       (try_end),
     (try_end),
     (assign, reg0, ":result"),
     ]),

("calculate_amount_of_cattle_can_be_stolen",
    [
      (store_script_param, ":village_no", 1),
      (call_script, "script_get_max_skill_of_player_party", "skl_looting"),
      (assign, ":max_skill", reg0),
      (store_mul, ":can_steal", ":max_skill", 2),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
      (store_add, ":num_men_effect", reg0, 10),
      (val_div, ":num_men_effect", 10),
      (val_add, ":can_steal", ":num_men_effect"),
      (party_get_slot, ":num_cattle", ":village_no", slot_village_number_of_cattle),
      (val_min, ":can_steal", ":num_cattle"),
      (assign, reg0, ":can_steal"),
     ]),

("remove_cattles_if_herd_is_close_to_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":max_req", 2),
      (assign, ":cur_req", ":max_req"),
      (try_for_parties, ":cur_party"),
        (gt, ":cur_req", 0),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":cur_party", ":party_no"),
        (lt, ":dist", 3),

        #Do not use the quest herd for "move cattle herd"
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        #Do not use the quest herd for "move cattle herd" ends

        (party_count_companions_of_type, ":num_cattle", ":cur_party", "trp_cattle"),
        (try_begin),
          (le, ":num_cattle", ":cur_req"),
          (assign, ":num_added", ":num_cattle"),
          (remove_party, ":cur_party"),
        (else_try),
          (assign, ":num_added", ":cur_req"),
          (party_remove_members, ":cur_party", "trp_cattle", ":cur_req"),
        (try_end),
        (val_sub, ":cur_req", ":num_added"),


        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_village),
          (party_get_slot, ":village_cattle_amount", ":party_no", slot_village_number_of_cattle),
          (val_add, ":village_cattle_amount", ":num_added"),
          (party_set_slot, ":party_no", slot_village_number_of_cattle, ":village_cattle_amount"),
        (try_end),

        (assign, reg3, ":num_added"),
        (str_store_party_name_link, s1, ":party_no"),
        (display_message, "@You brought {reg3} heads of cattle to {s1}."),
		(try_begin),
			(gt, "$cheat_mode", 0),
			(assign, reg4, ":village_cattle_amount"),
			(display_message, "@{!}Village now has {reg4}"),
		(try_end),
      (try_end),
      (store_sub, reg0, ":max_req", ":cur_req"),
     ]),

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
	),

("process_player_enterprise",
    #reg0: Profit per cycle
	##diplomacy start+
	#Actual documentation of original parameters and outputs.
	# INPUTS:
	#   arg1: item_type
	#   arg2: center
	# OUTPUTS:
    #   reg0:  profit_per_cycle"),
	#   reg1:  final_price_for_total_produced_goods"),
	#   reg2:  final_price_for_total_inputs"),
	#   reg3:  price_of_labor"),
	#   reg4:  final_price_for_single_produced_good"),
	#   reg5:  final_price_for_single_input"),
	#	reg10: final_price_for_secondary_input"),
	#
	# Further, if experimental changes are enabled, modify the price.
	##diplomacy end+
	[
	  (store_script_param, ":item_type", 1),
	  (store_script_param, ":center", 2),

	  (item_get_slot, ":price_of_labor", ":item_type", slot_item_overhead_per_run),

	  (item_get_slot, ":base_price", ":item_type", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":item_type", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_produced_good", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_produced_good", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_outputs_produced", ":item_type", slot_item_output_per_run),
	  (store_mul, ":final_price_for_total_produced_goods", ":number_of_outputs_produced", ":final_price_for_single_produced_good"),

	  (item_get_slot, ":primary_raw_material", ":item_type", slot_item_primary_raw_material),
	  (item_get_slot, ":base_price", ":primary_raw_material", slot_item_base_price),
	  (store_sub, ":cur_good_price_slot", ":primary_raw_material", trade_goods_begin),
	  (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	  (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
	  ##diplomacy start+
	  (try_begin),
	     (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		 (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":primary_raw_material", ":center"),
		 (val_max, ":cur_price_modifier", reg0),
	  (try_end),
	  (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
	  (store_mul, ":final_price_for_single_input", ":base_price", ":cur_price_modifier"),#<- (Unchanged)
	  (val_div, ":final_price_for_single_input", average_price_factor),#Replaced "1000" with "average_price_factor"
	  ##diplomacy end+
	  (item_get_slot, ":number_of_inputs_required", ":item_type", slot_item_input_number),
	  (try_begin),
	    (lt, ":number_of_inputs_required", 0),
	    (store_div, ":final_price_for_total_inputs", ":final_price_for_single_input", 2),
	  (else_try),
	    (store_mul, ":final_price_for_total_inputs", ":final_price_for_single_input", ":number_of_inputs_required"),
	  (try_end),

	  (try_begin),
	    (item_slot_ge, ":item_type", slot_item_secondary_raw_material, 1),
	    (item_get_slot, ":secondary_raw_material", ":item_type", slot_item_secondary_raw_material),
	    (item_get_slot, ":base_price", ":secondary_raw_material", slot_item_base_price),
	    (store_sub, ":cur_good_price_slot", ":secondary_raw_material", trade_goods_begin),
	    (val_add, ":cur_good_price_slot", slot_town_trade_good_prices_begin),
	    (party_get_slot, ":cur_price_modifier", ":center", ":cur_good_price_slot"),
		##diplomacy start+
		(try_begin),
	      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),#<-- experimental changes must be enabled
		  (call_script, "script_dplmc_assess_ability_to_purchase_good_from_center", ":secondary_raw_material", ":center"),
		  (val_max, ":cur_price_modifier", reg0),
	    (try_end),
	    (val_clamp, ":cur_price_modifier", minimum_price_factor, maximum_price_factor + 1),#Added enforcement of minimum/maximum
		##diplomacy end+
		(store_mul, ":final_price_for_secondary_input", ":base_price", ":cur_price_modifier"),#fixes
	    (try_begin),
	      (lt, ":number_of_inputs_required", 0),
	      (val_div, ":final_price_for_secondary_input", 2),
	    (else_try),
	      (val_mul, ":final_price_for_secondary_input", ":number_of_inputs_required"),
	    (try_end),

		##diplomacy start+
	    (val_div, ":final_price_for_secondary_input", average_price_factor),#Replaced "1000" with "average_price_factor"
		##diplomacy end+
	  (else_try),
	    (assign, ":final_price_for_secondary_input", 0),
	  (try_end),

	  (store_sub, ":profit_per_cycle", ":final_price_for_total_produced_goods", ":final_price_for_total_inputs"),
	  (val_sub, ":profit_per_cycle", ":price_of_labor"),
	  (val_sub, ":profit_per_cycle", ":final_price_for_secondary_input"),

	  (assign, reg0, ":profit_per_cycle"),
	  (assign, reg1, ":final_price_for_total_produced_goods"),
	  (assign, reg2, ":final_price_for_total_inputs"),
	  (assign, reg3, ":price_of_labor"),
	  (assign, reg4, ":final_price_for_single_produced_good"),
	  (assign, reg5, ":final_price_for_single_input"),
	  (assign, reg10, ":final_price_for_secondary_input"),
	]),

("get_troop_of_merchant",
  [
        (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
        (store_sub, ":troop_of_merchant", ":starting_town_faction", npc_kingdoms_begin),
        (val_add, ":troop_of_merchant", startup_merchants_begin),
        (assign, reg0, ":troop_of_merchant"),
  ]),

("calculate_ransom_contribution", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (store_script_param_2, ":ransom_size"), #2000 from quest giver, up to 125*strength for other relatives
    #because kingdom ladies aren't landholders, they give it without consequence of debt if quest fails (also less dialogue to write)
    (assign, ":ransom_amount", 0),

    (try_begin),
      (check_quest_active, "qst_rescue_prisoner"),
      (quest_get_slot, ":prisoner", "qst_rescue_prisoner", slot_quest_target_troop),
      (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
      (try_begin),
        #each +-2 relation has 1% effect on calculation to the effect of 50%/150% initial value
        (call_script, "script_troop_get_relation_with_troop", ":lord_no", ":prisoner"),
        (store_div, ":relation", reg0, 2),
        (val_add, ":relation", 100),
        (val_mul, ":ransom_amount", ":relation"),
        (val_div, ":ransom_amount", 100),
      (try_end),
      # problem is this script has variance in output, we can use the cached slot_quest_target_amount
      (call_script, "script_calculate_ransom_amount_for_troop", ":prisoner"),
      (assign, ":ransom", reg0), #original amount
      (val_add, ":ransom_size", ":cur_ransom"),
      (try_begin), #contributed too much, get remainder before arbitrary cap
        (gt, ":ransom_size", ":ransom"),
        (store_sub, ":ransom_amount", ":ransom", ":cur_ransom"),
      (else_try), #give full amount
        (store_sub, ":ransom_amount", ":ransom_size", ":cur_ransom"), #undo adding existing ransom
      (try_end),

      (try_begin), #active npcs have wealth
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_wealth", ":lord_no", slot_troop_wealth),
        (val_div, ":cur_wealth", 2), #at most half for contributing
        (val_min, ":cur_wealth", ":ransom"),
        (val_min, ":ransom_amount", ":cur_wealth"), #actual amount the lord can give
      (try_end),
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),
    (assign, reg0, ":ransom_amount"),
    ]
  ),

("lend_money_for_ransom", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (try_begin),
      (troop_get_slot, ":ransom_amount", ":lord_no", slot_troop_player_debt),
      (le, ":ransom_amount", 0),
      (store_script_param_2, ":ransom_amount"),
    (try_end),
    (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
    (val_add, ":cur_ransom", ":ransom_amount"), #actual amount to give

    #set up quests
    (quest_set_slot, "qst_rescue_prisoner", slot_quest_target_state, ":cur_ransom"),
    (assign, reg0, ":cur_ransom"),
    #the amount calculated at the start, will differ from expected ransom
    (quest_get_slot, reg1, "qst_rescue_prisoner", slot_quest_target_amount),
    (str_store_string, s1, "@You have raised {reg0}/{reg1} denars for the ransom"),
    (add_quest_note_from_sreg, "qst_rescue_prisoner", 4, s1, 1), #0:date, 1:giver, 2:desc 3:time

    #move actual gold
    (troop_add_gold, "trp_player", ":ransom_amount"),
    (try_begin),
      (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
      (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":lord_no"),
      (val_add, ":ransom_amount", dplmc_ransom_debt_mask), #masking this from "real" debt
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),

    ]
  ),

("troop_transfer_gold",
    [
      (store_script_param, ":source", 1),
      (store_script_param, ":destination", 2),
      (store_script_param, ":amount", 3),
      (store_troop_gold, ":cur_amount", ":source"),
      (try_begin),
        (gt, ":amount", 0), #0 means move all
        (val_min, ":cur_amount", ":amount"),
      (try_end),
      (troop_remove_gold, ":source", ":cur_amount"),
      # (troop_add_gold, ":destination", ":cur_amount"),
      (call_script, "script_troop_add_gold", ":destination", ":cur_amount"),
      (assign, reg0, ":cur_amount"),
    ]),

("auto_trade_at_center", [
    (store_script_param, ":center_no", 1),
    (try_begin),
      #For Towns:
      (is_between, ":center_no", towns_begin, towns_end),
      (try_begin),
        #Sell to non-trade good merchants first so player has plenty of cash and inventory space when dealing with goods merchant
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_weaponsmith),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_armorer),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_horse_merchant),
        (ge, ":merchant_troop", 1),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
      (try_begin),
        (party_get_slot, ":merchant_troop", ":center_no", slot_town_merchant),
        (ge, ":merchant_troop", 1),
        #Player should be in a good position to buy after selling to other merchants
        (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
        (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
      (try_end),
    (else_try),
      #For Villages:
      (is_between, ":center_no", villages_begin, villages_end),
      (party_get_slot, ":merchant_troop", ":center_no", slot_town_elder),
      (ge, ":merchant_troop", 1),
      #Villages tend to not have much coin, so we buy first to make sure they can afford the player's goods
      (call_script, "script_auto_trade_buy_from_merchant", ":merchant_troop"),
      (call_script, "script_auto_trade_sell_to_merchant", ":merchant_troop"),
    (try_end),
  ]),

("auto_trade_sell_to_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_sold", 0),
    (assign, ":gold_gained", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":customer"),
    (set_show_messages, 0),

    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":customer", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":customer", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":customer", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      #Don't sell if player has disabled auto selling for this item
      (item_get_slot, ":sell_enabled", ":item", slot_item_auto_trade_sell_enabled),
      (gt, ":sell_enabled", 0),

      #Don't sell if the current amount is less than or equal to the player's minimum quantity
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (item_get_slot, ":min_qty", ":item", slot_item_auto_trade_min_quantity),
      (gt, ":item_count", ":min_qty"),

      (call_script, "script_game_get_item_sell_price_factor", ":item"),
      (assign, ":sell_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":sell_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score", 1),

      (item_get_slot, ":sell_price", ":item", slot_item_auto_trade_sell_over_price),
      (gt, ":score", ":sell_price"),

      (troop_set_inventory_slot, ":customer", ":i_slot", -1),
      (troop_add_gold, ":customer", ":score"),
      (call_script, "script_game_event_sell_item", ":item", 0),
      (val_add, ":items_sold", 1),
      (val_add, ":gold_gained", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_sold", 1),
      (assign, reg0, ":gold_gained"),
      (assign, reg1, ":items_sold"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You sold {reg1} {reg3?items:item} to {s0} and gained {reg0} {reg3?denars:denar}."),
    (try_end),
  ]),

("auto_trade_buy_from_merchant", [
    (store_script_param, ":merchant_troop", 1),
    (assign, ":customer", "trp_player"),

    (assign, ":items_bought", 0),
    (assign, ":gold_spent", 0),
    (troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
    (set_show_messages, 0),
    (try_for_range, ":i_slot", 10, ":inv_cap"),
      (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
      (gt, ":item", -1),
      (is_between, ":item", trade_goods_begin, trade_goods_end),
      (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
      (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
      (eq, ":amount", ":max_amount"),

      (store_free_inventory_capacity, ":free_inv_cap", ":customer"),
      (gt, ":free_inv_cap", 0),

      #Don't buy if player has disabled auto buying for this item
      (item_get_slot, ":buy_enabled", ":item", slot_item_auto_trade_buy_enabled),
      (gt, ":buy_enabled", 0),

      #Don't buy if the quantity would exceed player's max quantity
      #Since there is a separate option to enable/disable, a max quantity of 0 is treated as no max
      (store_item_kind_count, ":item_count", ":item", ":customer"),
      (assign, ":qty_valid", 1),
      (try_begin),
        (item_get_slot, ":max_qty", ":item", slot_item_auto_trade_max_quantity),
        (gt, ":max_qty", 0),
        (ge, ":item_count", ":max_qty"),
        (assign, ":qty_valid", 0),
      (try_end),
      (eq, ":qty_valid", 1),

      (call_script, "script_game_get_item_buy_price_factor", ":item"),
      (assign, ":buy_price_factor", reg0),
      (store_item_value,":score",":item"),
      (val_mul, ":score", ":buy_price_factor"),
      (val_div, ":score", 100),
      (val_max, ":score",1),
      (store_troop_gold, ":customer_gold", ":customer"),
      (val_sub, ":customer_gold", "$g_auto_trade_minimum_wealth"),
      (ge, ":customer_gold", ":score"),

      (item_get_slot, ":buy_price", ":item", slot_item_auto_trade_buy_under_price),
      (lt, ":score", ":buy_price"),

      (troop_add_item, ":customer", ":item"),
      (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
      (troop_remove_gold, ":customer", ":score"),
      (troop_add_gold, ":merchant_troop", ":score"),
      (call_script, "script_game_event_buy_item", ":item", 0),
      (val_add, ":items_bought", 1),
      (val_add, ":gold_spent", ":score"),
    (try_end),
    (set_show_messages, 1),

    #Print a message if appropriate
    (try_begin),
      (ge, ":items_bought", 1),
      (assign, reg0, ":gold_spent"),
      (assign, reg1, ":items_bought"),
      (store_sub, reg3, reg1, 1),
      (str_store_troop_name, s0, ":merchant_troop"),
      (display_message, "@You bought {reg1} {reg3?items:item} from {s0} for {reg0} {reg3?denars:denar}."),
    (try_end),
  ]),

("initialize_exchange_screen_extensions", [
	(store_script_param, ":troop_id", 1),

	(try_begin), #MASS PRISONER TRANSFER AFTER BATTLE
		(key_is_down, key_left_control), (key_is_down, key_a),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 10),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_temp_party"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_prisoner_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(ge, ":player_prisoner_capacity", ":stack_size"),
				(party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
			(else_try),	
				(party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_prisoner_capacity"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_prisoner_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_prisoners, "p_temp_party", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_prisoners, "p_temp_party", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ MASS TRANSFER OF RESCUED PRISONERS AFTER BATTLE
	(try_begin), 
		(key_is_down, key_left_control), (key_is_down, key_s),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 10),
		(party_get_num_companion_stacks, ":num_companion_stacks","p_temp_party"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(try_begin),
				(ge, ":player_companion_capacity", ":stack_size"),
				(party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
				(party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
			(else_try),	
				(party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_companion_capacity"),
				(val_add, ":stack_no_wounded", ":player_companion_capacity"),
				(store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
				(val_max, ":excess", 0),
				(party_wound_members, "p_main_party", ":stack_troop", ":excess"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_companion_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_members, "p_temp_party", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_members, "p_temp_party", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ SORTING GARRISONS
	(try_begin), #ARROW UP
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_up),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", 0), #key_up can't be used with stack 0
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(store_sub, ":key_stack_minus_one", ":key_stack", 1),
		(store_add, ":key_stack_plus_one", ":key_stack", 1),
		(try_for_range, ":stack_no", 0, ":key_stack_minus_one"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack_minus_one"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack_minus_one"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack_minus_one"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_for_range, ":stack_no", ":key_stack_plus_one", ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1), #restoring the balance in town
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #ARROW DOWN
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_down),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(store_add, ":key_stack_plus_one", ":key_stack", 1),
		(store_add, ":key_stack_plus_two", ":key_stack", 2),
		(try_for_range, ":stack_no", 0, ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack_plus_one"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack_plus_one"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack_plus_one"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(try_for_range, ":stack_no", ":key_stack_plus_two", ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #PAGE UP
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_page_up),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", 0), #key_page_up can't be used with stack 0
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(neq, ":stack_no", ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	
	(try_begin), #PAGE DOWN
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(troop_slot_eq, "trp_temp_array_d", slot_last_requested_troop, ":troop_id"),
		(key_is_down, key_page_down),
		(party_clear, "p_temp_party"),
		(call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
		(party_get_num_companion_stacks, ":num_stacks","$current_town"),
		(store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
		(assign, ":key_stack", -1),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(try_begin),
				(eq, ":stack_troop", ":troop_id"),
				(neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
				(assign, ":key_stack", ":stack_no"),
			(try_end),
		(try_end),
		(neq, ":key_stack", -1),
		(try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(neq, ":stack_no", ":key_stack"),
			(party_stack_get_troop_id, ":stack_troop","p_temp_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_temp_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(party_stack_get_troop_id, ":stack_troop","p_temp_party",":key_stack"),
		(party_stack_get_size, ":stack_size","p_temp_party",":key_stack"),
		(party_stack_get_num_wounded, ":stack_no_wounded","p_temp_party",":key_stack"),
		(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
		(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
		(try_begin),
			(ge, ":stack_no_wounded", 1),
			(assign, ":first_party_member_was_wounded", 1),
		(try_end),
		(party_get_num_companion_stacks, ":num_stacks_in_main_party","p_main_party"),
		(try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
			(party_stack_get_troop_id, ":stack_troop_in_main_party","p_main_party",":stack_in_main_party"),
			(eq, ":stack_troop_in_main_party", ":troop_id"),
			(party_stack_get_size, ":stack_size_in_main_party","p_main_party",":stack_in_main_party"),
			(party_stack_get_num_wounded, ":stack_no_wounded_in_main_party","p_main_party",":stack_in_main_party"),
			(try_begin),
				(eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
				(gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
				(store_sub, ":stack_size_in_main_party_minus_1" ,":stack_size_in_main_party", 1),
				(store_sub, ":stack_no_wounded_in_main_party_minus_2" ,":stack_no_wounded_in_main_party", 2),
				(party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
				(party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
			(else_try),	
				(eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
				(assign, ":first_party_member_was_wounded", 1),
			(try_end),	
		(try_end),
		(party_remove_members, "p_main_party", ":troop_id", 1),
		(party_add_members, "$current_town", ":troop_id", 1),
		(try_begin),
			(eq, ":first_party_member_was_wounded", 1),
			(party_wound_members, "$current_town", ":troop_id", 1),
		(try_end),
	(try_end),
	#++++++++++++++++++++++++++++++++++++++++++++++++ MASSIVE TRANSFERS TO/FROM GARRISON
	(try_begin), #TROOPS FROM GARRISON TO PLAYER'S PARTY
		(key_is_down, key_right_control), (key_is_down, key_right),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_companion_stacks, ":num_companion_stacks","$current_town"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","$current_town",":stack_no"),
			(try_begin),
				(ge, ":player_companion_capacity", ":stack_size"),
				(party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
				(party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
			(else_try),	
				(party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_companion_capacity"),
				(val_add, ":stack_no_wounded", ":player_companion_capacity"),
				(store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
				(val_max, ":excess", 0),
				(party_wound_members, "p_main_party", ":stack_troop", ":excess"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_companion_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(party_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_members, "$current_town", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	
	(try_begin), #TROOPS FROM PLAYER'S PARTY TO GARRISON
		(key_is_down, key_right_control), (key_is_down, key_left),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_companion_stacks, ":num_companion_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_companion_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_stack_get_num_wounded, ":stack_no_wounded","p_main_party",":stack_no"),
			(party_add_members, "$current_town", ":stack_troop", ":stack_size"),
			(party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
			(party_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_remove_members, "p_main_party", ":stack_troop", ":stack_size"),
		(try_end),
	(try_end),
	
	(try_begin), #PRISONERS FROM GARRISON TO PLAYER'S PARTY
		(key_is_down, key_left_control), (key_is_down, key_a),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","$current_town"),
		(assign, ":stop_stack", -1),
		(assign, ":stop_no", -1),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(eq, ":stop_stack", -1),
			(party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(ge, ":player_prisoner_capacity", ":stack_size"),
				(party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
			(else_try),	
				(party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
				(assign, ":stop_stack", ":stack_no"),
				(assign, ":stop_no", ":player_prisoner_capacity"),
			(try_end),
		(try_end),
		(try_begin),
			(neq, ":stop_stack", -1),
			(store_add, ":stop_stack_plus_one", ":stop_stack", 1),
		(else_try),	
			(assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","$current_town",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","$current_town",":stack_no"),
			(try_begin),
				(neq, ":stop_no", -1),
				(eq, ":stack_no", ":stop_stack"),
				(party_remove_prisoners, "$current_town", ":stack_troop", ":stop_no"),
			(else_try),	
				(party_remove_prisoners, "$current_town", ":stack_troop", ":stack_size"),
			(try_end),
		(try_end),
	(try_end),
	
	(try_begin), #PRISONERS FROM PLAYER'S PARTY TO GARRISON
		(key_is_down, key_left_control), (key_is_down, key_d),
		(troop_slot_eq, "trp_temp_array_d", slot_adv_transfer_mode, 12),
		(party_get_num_prisoner_stacks, ":num_prisoner_stacks","p_main_party"),
		(try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_add_prisoners, "$current_town", ":stack_troop", ":stack_size"),
		(try_end),
		(try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
			(party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
			(neg|troop_is_hero, ":stack_troop"),
			(party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(party_remove_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
		(try_end),
	(try_end),
    ]
  ),
]
