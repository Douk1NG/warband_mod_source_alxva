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

dplmc_get_trade_penalty_scripts = [
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
  ])
]
