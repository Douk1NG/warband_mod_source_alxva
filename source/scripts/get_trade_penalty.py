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

get_trade_penalty_scripts = [
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
  ])
]
