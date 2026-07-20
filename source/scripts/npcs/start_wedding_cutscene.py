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

start_wedding_cutscene_scripts = [
("start_wedding_cutscene",
   [
     (store_script_param, "$g_wedding_groom_troop", 1),
     (store_script_param, "$g_wedding_bride_troop", 2),
     ##diplomacy start+
	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg1", reg1),


     #To prevent a ridiculous cutscene, reverse genders if the bride is male.
	 (call_script, "script_dplmc_store_is_female_troop_1_troop_2", "$g_wedding_groom_troop", "$g_wedding_bride_troop"),
	 (assign, ":groom_is_woman", reg0),
	 (assign, ":bride_is_woman", reg1),

     (try_begin),
       (eq, ":bride_is_woman", 0),
       (neq, ":groom_is_woman", 0),#Don't bother reversing if both are male
       (assign, reg0, "$g_wedding_bride_troop"),
       (assign, "$g_wedding_bride_troop", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_groom_troop", reg0),
	 (else_try),
	   #If it's a same-sex wedding, put the player in the role of the groom.
	   (eq, ":bride_is_woman", ":groom_is_woman"),
	   (eq, "$g_wedding_bride_troop", "trp_player"),
	   (assign, "$g_wedding_bride_troop", "$g_wedding_groom_troop"),
	   (assign, "$g_wedding_groom_troop", "trp_player"),
     (try_end),
     #diplomacy end+
     (assign, "$g_wedding_bishop_troop", "trp_temporary_minister"),
     (try_begin),
       (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
       (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_wedding_groom_troop"),
       (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_wedding_bride_troop"),
       (faction_get_slot, ":players_king", "$players_kingdom", slot_faction_leader),
	   ##diplomacy start+
	   (neq, ":players_king", "$g_wedding_bride_troop"),#necessary now that marrying monarchs can occur
	   (neq, ":players_king", "$g_wedding_groom_troop"),
	   #Changed the gender requirement (used to be required male)
       #(troop_get_type, ":troop_type", ":players_king"),
       #(eq, ":troop_type", 0), #male
	   (call_script, "script_dplmc_store_troop_is_female", ":players_king"),
	   (this_or_next|eq, reg0, 0),
	   (this_or_next|eq, ":groom_is_woman", ":bride_is_woman"),
	      (ge, "$g_disable_condescending_comments", 2),
       (neq, ":players_king", "$g_wedding_bride_troop"),
       (neg|troop_slot_eq, "$g_wedding_bride_troop", slot_troop_father, ":players_king"),
	   (neg|troop_slot_eq, "$g_wedding_bride_troop", slot_troop_mother, ":players_king"),
       ##diplomacy end+
       (neq, ":players_king", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_bishop_troop", ":players_king"),
     (else_try),
       (eq, "$players_kingdom", "fac_player_supporters_faction"),
       (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
       (gt, "$g_player_minister", 0),
	   ##diplomacy start+
       #(troop_get_type, ":troop_type", "$g_player_minister"),
	   #(eq, ":troop_type", 0), #male
	   (call_script, "script_dplmc_store_troop_is_female", "$g_player_minister"),
	   (this_or_next|eq, reg0, 0),
	   (this_or_next|eq, ":groom_is_woman", ":bride_is_woman"),
	      (ge, "$g_disable_condescending_comments", 2),
	   ##diplomacy end+
       (neq, "$g_player_minister", "$g_wedding_groom_troop"),
       (assign, "$g_wedding_bishop_troop", "$g_player_minister"),
     (try_end),

     (assign, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
     (try_begin),
       (neq, "$g_wedding_bride_troop", "trp_player"),
       (try_begin),
         (troop_get_slot, ":father", "$g_wedding_bride_troop", slot_troop_father),
         (gt, ":father", 0),
         ##diplomacy start+
         (neg|troop_slot_ge, ":father", slot_troop_occupation, slto_retirement),
         #(troop_get_type, ":troop_type", ":father"), #just to make sure #<- dplmc+ replaced
		 (call_script, "script_dplmc_store_troop_is_female", ":father"),
		 (this_or_next|eq, ":bride_is_woman", 0),
			(eq, reg0, 0), #male
		 ##diplomacy end+
         (neq, ":father", "$g_wedding_groom_troop"), #this might be 0 due to an error
         (neq, ":father", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":father"),
       (else_try),
         (troop_get_slot, ":guardian", "$g_wedding_bride_troop", slot_troop_guardian),
         (gt, ":guardian", 0),
         ##diplomacy start+
         (neg|troop_slot_ge, ":guardian", slot_troop_occupation, slto_retirement),
         #(troop_get_type, ":troop_type", ":guardian"), #just to make sure #<- dplmc+ replaced
		 (call_script, "script_dplmc_store_troop_is_female", ":guardian"),
		 (this_or_next|eq, ":bride_is_woman", 0),
			(eq, reg0, 0), #male
		 (call_script, "script_dplmc_store_troop_is_female", ":guardian"),
		 ##diplomacy end+
         (neq, ":guardian", "$g_wedding_groom_troop"), #this might be 0 due to an error
         (neq, ":guardian", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":guardian"),
       ##diplomacy start+
	   #mother might be appropriate
	   (else_try),
		  (troop_get_slot, ":mother", "$g_wedding_bride_troop", slot_troop_mother),
	      (gt, ":mother", 0),
	      (neg|troop_slot_ge, ":mother", slot_troop_occupation, slto_retirement),

		  (neq, ":mother", "$g_wedding_groom_troop"),
		  (neq, ":mother", "$g_wedding_bride_troop"),
		  (neq, ":mother", "$g_wedding_bishop_troop"),

	      (assign, "$g_wedding_brides_dad_troop", ":mother"),
	   #we can get here, since male players can marry female lords
       (else_try),
          (is_between, "$g_wedding_bride_troop", companions_begin, companions_end),
          (troop_get_slot, ":cur_npc", "$g_wedding_bride_troop", slot_troop_personalitymatch_object),
          (ge, ":cur_npc", heroes_begin),
          (troop_slot_ge, ":cur_npc", slot_troop_met, 1),
		  (neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
		  (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_seneschal),
		     (troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),

		  (neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),
		  (neq, ":cur_npc", "$g_wedding_groom_troop"),
	      (neq, ":cur_npc", "$g_wedding_bride_troop"),
	      (neq, ":cur_npc", "$g_wedding_bishop_troop"),

		  (this_or_next|neg|troop_slot_ge, ":cur_npc", slot_lord_reputation_type, lrep_roguish),
		  (this_or_next|troop_slot_ge, ":cur_npc", slot_lord_reputation_type, lrep_conventional),

          (assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
	   (else_try),
	      #any other companion or lord that is favorable
		  (assign, ":best_score", 0),#must be at least positive
		  (try_for_range, ":cur_npc", heroes_begin, heroes_end),
			(neq, ":cur_npc", "$g_wedding_groom_troop"),
	        (neq, ":cur_npc", "$g_wedding_bride_troop"),
	        (neq, ":cur_npc", "$g_wedding_bishop_troop"),
			(neq, ":cur_npc", "trp_knight_1_1_wife"),
			(neq, ":cur_npc", "trp_kingdom_heroes_including_player_begin"),

			(neg|troop_slot_ge, ":cur_npc", slot_troop_occupation, slto_retirement),

			(call_script, "script_troop_get_relation_with_troop", ":cur_npc", "$g_wedding_bride_troop"),
			(assign, ":relation", reg0),
			#(call_script, "script_troop_get_family_relation_to_troop", ":cur_npc", "$g_wedding_bride_troop"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_npc",  "$g_wedding_bride_troop"),
			(assign, ":family_relation", reg0),

			(store_add, ":score", ":relation", ":family_relation"),

			(gt, ":score", ":best_score"),#score better than current best
			(assign, ":best_score", ":score"),
			(assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
		  (try_end),
       ##diplomacy end+
       (try_end),
     (else_try),
       (try_for_range, ":cur_companion", companions_begin, companions_end),
         (this_or_next|troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
         (troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_kingdom_hero),
		 ##diplomacy start+
         #(troop_get_type, ":troop_type", ":cur_companion"), #just to make sure
         #(eq, ":troop_type", 0), #male
		 (call_script, "script_dplmc_store_troop_is_female", ":cur_companion"),
		 (this_or_next|eq, reg0, 0),
			(eq, ":bride_is_woman", 0),
		 ##diplomacy end+
         (neq, ":cur_companion", "$g_wedding_groom_troop"),
         (neq, ":cur_companion", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_companion"),
       (try_end),
       ##diplomacy start+ try again with female companions if no male companions available
       (eq, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
       (try_for_range, ":cur_companion", companions_begin, companions_end),
         (this_or_next|troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_player_companion),
			(troop_slot_eq, ":cur_companion", slot_troop_occupation, slto_kingdom_hero),
         (neq, ":cur_companion", "$g_wedding_groom_troop"),
         (neq, ":cur_companion", "$g_wedding_bishop_troop"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_companion"),
       (try_end),
	   #try again with all lords if no female companions available
	   (eq, "$g_wedding_brides_dad_troop", "trp_temporary_minister"),
	   (assign, ":best_score", -100),#best score
       (try_for_range, ":cur_npc", heroes_begin, heroes_end),
	     (neg|troop_slot_eq, ":cur_npc", slot_troop_met, 0),

 	     (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_seneschal),
         (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
		 (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),
			(troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),

         (neq, ":cur_npc", "$g_wedding_groom_troop"),
         (neq, ":cur_npc", "$g_wedding_bishop_troop"),
		 (neq, ":cur_npc", "trp_knight_1_1_wife"),
	 	 (neq, ":cur_npc", "trp_kingdom_heroes_including_player_begin"),

		 (call_script, "script_troop_get_player_relation", ":cur_npc"),
		 (assign, ":score", reg0),
		 (ge, ":score", 0),
		 (call_script, "script_dplmc_is_affiliated_family_member", ":cur_npc"),
		 (this_or_next|ge, ":score", 20),
			(ge, reg0, 1),
		 (gt, ":score", ":best_score"),
		 (assign, ":best_score", ":score"),
         (assign, "$g_wedding_brides_dad_troop", ":cur_npc"),
       (try_end),
       ##diplomacy end+
     (try_end),

     (modify_visitors_at_site,"scn_wedding"),
     (reset_visitors,0),
     (set_visitor, 0, "$g_wedding_groom_troop"),
     (set_visitor, 1, "$g_wedding_bride_troop"),
     (set_visitor, 2, "$g_wedding_brides_dad_troop"),
     (set_visitor, 3, "$g_wedding_bishop_troop"),
     (assign, ":num_visitors", 4),
     (assign, ":num_male_visitors", 0),
	 ##diplomacy start+
	 (store_troop_faction, ":groom_faction", "$g_wedding_groom_troop"),
	 (store_troop_faction, ":bride_faction", "$g_wedding_bride_troop"),
	 ##diplomacy end+
     (try_for_range, ":cur_npc", active_npcs_begin, kingdom_ladies_end),
       (lt, ":num_visitors", 32),
       (neq, ":cur_npc", "$g_wedding_groom_troop"),
       (neq, ":cur_npc", "$g_wedding_bride_troop"),
       (neq, ":cur_npc", "$g_wedding_brides_dad_troop"),
       (neq, ":cur_npc", "$g_wedding_bishop_troop"),
       (store_troop_faction, ":npc_faction", ":cur_npc"),
	   ##diplomacy start+
       #(is_between, ":npc_faction", kingdoms_begin, kingdoms_end),
       #(eq, ":npc_faction", "$players_kingdom"),
	   (this_or_next|eq, ":groom_faction", ":npc_faction"),
	      (eq, ":bride_faction", ":npc_faction"),
       ##diplomacy end+
       (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_player_companion),
       (this_or_next|troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_hero),
       (troop_slot_eq, ":cur_npc", slot_troop_occupation, slto_kingdom_lady),
	   ##diplomacy start+
       #(troop_get_type, ":troop_type", ":cur_npc"),
	   (call_script, "script_dplmc_store_troop_is_female", ":cur_npc"),
	   (assign, ":troop_type", reg0),
	   ##diplomacy end+
       (assign, ":continue_adding", 1),
       (try_begin),
         (eq, ":troop_type", 0),
         (assign, ":continue_adding", 0),
         (lt, ":num_male_visitors", 16), #limit number of male visitors
         (assign, ":continue_adding", 1),
         (val_add, ":num_male_visitors", 1),
       (try_end),
       (eq, ":continue_adding", 1),
       (set_visitor, ":num_visitors", ":cur_npc"),
       (val_add, ":num_visitors", 1),
     (try_end),
	 ##diplomacy start+
	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
	 ##diplomacy end+
     (set_jump_mission,"mt_wedding"),
     (jump_to_scene,"scn_wedding"),
     (change_screen_mission),
    ])
]
