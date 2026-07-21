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

dplmc_calculate_troop_score_for_center_aux_scripts = [
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
   ])
]
