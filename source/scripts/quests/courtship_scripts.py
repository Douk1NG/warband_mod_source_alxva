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

courtship_scripts = [

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
    ]),

("troop_get_romantic_chemistry_with_troop", #source is lady, target is man
    [
      ##diplomacy start+ (players of either gender may marry opposite-gender lords)
      #Note: the above is misleading even in Native, since when target_lord is the player,
      #target_lord can be female and source_lady can be male.
	  (assign, ":save_reg1", reg1),
      ##diplomacy end+
      (store_script_param, ":source_lady", 1),
      (store_script_param, ":target_lord", 2),

      (store_add, ":chemistry_sum", ":source_lady", ":target_lord"),
      (val_add, ":chemistry_sum", "$romantic_attraction_seed"),

      #This calculates (modula ^ 2) * 3
      (store_mod, ":chemistry_remainder", ":chemistry_sum", 5),
      (val_mul, ":chemistry_remainder", ":chemistry_remainder"), #0, 1, 4, 9, 16
      (val_mul, ":chemistry_remainder", 3), #0, 3, 12, 27, 48

      (store_attribute_level, ":romantic_chemistry", ":target_lord", ca_charisma),
      (val_sub, ":romantic_chemistry", ":chemistry_remainder"),

      (val_mul, ":romantic_chemistry", 2),
      ##diplomacy start+ ensure companion compatability
      (try_begin),
         (is_between, ":source_lady", companions_begin, companions_end),
         (troop_slot_eq, ":source_lady", slot_troop_personalitymatch_object, ":target_lord"),
         (val_max, ":romantic_chemistry", 15),
      (else_try),
         (is_between, ":target_lord", companions_begin, companions_end),
         (troop_slot_eq, ":target_lord", slot_troop_personalitymatch_object, ":source_lady"),
         (val_max, ":romantic_chemistry", 15),
	  #...and companion incompatibility.
	  (else_try),
  	     (is_between, ":source_lady", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":source_lady", slot_troop_personalityclash_object, ":target_lord"),
			(troop_slot_eq, ":source_lady", slot_troop_personalityclash2_object, ":target_lord"),
		 (val_min, ":romantic_chemistry", -15),
  	  (else_try),
  	     (is_between, ":target_lord", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":target_lord", slot_troop_personalityclash_object, ":source_lady"),
			(troop_slot_eq, ":target_lord", slot_troop_personalityclash2_object, ":source_lady"),
		(val_min, ":romantic_chemistry", -15),
	  #Prevent glitches.  This can be enabled explicitly if intentional.
      (else_try),
	     (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
         (eq, reg0, reg1),#different genders
         #(val_min, ":romantic_chemistry", -15), #dckplmc
      (try_end),
	  (assign, reg1, ":save_reg1"),
      ##diplomacy end+
      (assign, reg0, ":romantic_chemistry"),

      #examples :
      #For a charisma of 18, yields (18 - 0) * 2 = 36, (18 - 3) * 2 = 30, (18 - 12) * 2 = 12, (18 - 27) * 2 = -18, (18 - 48) * 2 = -60
      #For a charisma of 10, yields (10 - 0) * 2 = 20, (10 - 3) * 2 = 14, (10 - 12) * 2 = -4, (10 - 27) * 2 = -34, (10 - 48) * 2 = -76
      #For a charisma of 7, yields  (7 - 0) * 2 = 14,  (7 - 3) * 2 = 8,   (7 - 12) * 2 = -10, (7 - 27) * 2 = -40,  (7 - 48) * 2 = -82

      #15 is high attraction, 0 is moderate attraction, -76 is lowest attraction
	]),

("cf_troop_get_romantic_attraction_to_troop", #source is lady, target is man
    [

	(store_script_param, ":source_lady", 1),
	(store_script_param, ":target_lord", 2),

	(assign, ":weighted_romantic_assessment", 0),
    ##diplomacy start+
	(assign, ":save_reg1", reg1),
	#Use gender script
	#(troop_get_type, ":source_is_female", ":source_lady"),
	#(eq, ":source_is_female", 1),
	#(troop_get_type, ":target_is_female", ":target_lord"),
	#(eq, ":target_is_female", 0),
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
	(assign, ":source_is_female", reg0),
	(assign, ":target_is_female", reg1),
	(assign, reg1, ":save_reg1"),
    #(assign, reg0, -15), #dckplmc
	(neq, ":source_is_female", ":target_is_female"),
	##diplomacy end+

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":source_lady", ":target_lord"),
	(assign, ":romantic_chemistry", reg0),


	#objective attraction - average renown
	(troop_get_slot, ":modified_renown", ":target_lord", slot_troop_renown),
	(assign, ":lady_status", 60),
   ##diplomacy start+ adjust status based on who they are
	(try_begin),
      #The renown bonus is decreased the more important the lady's relatives are.
      (ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
      (troop_get_slot, ":best_renown", ":source_lady", slot_troop_renown),
      (try_begin),
        (troop_get_slot, ":relative", ":source_lady", slot_troop_father),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_guardian),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (troop_get_slot, ":relative", ":source_lady", slot_troop_mother),
        (ge, ":relative", 0),
        (troop_get_slot, ":other_renown", ":relative", slot_troop_renown),
        (val_max, ":best_renown", ":other_renown"),
   	(try_end),
   	(try_begin),
		  (ge, ":best_renown", 600),
        (store_div, ":lady_status", ":best_renown", 10),
   	(else_try),
		  (lt, ":best_renown", 400),
        (store_div, ":lady_status", ":best_renown", 10),
		  (val_add, ":lady_status", 20),
   	(try_end),
   	(val_clamp, ":lady_status", 30, 90),
   (try_end),
   ##diplomacy end+
	(val_div, ":modified_renown", 5),
	(val_sub, ":modified_renown", ":lady_status"),
	(val_min, ":modified_renown", 60),



	#weight values
	(try_begin),
		(assign, ":personality_match", 0),
		(call_script, "script_cf_test_lord_incompatibility_to_s17", ":source_lady", ":target_lord"),
		(store_sub, ":personality_match", 0, reg0),
	(try_end),

	(troop_get_slot, ":lady_reputation", ":source_lady", slot_lord_reputation_type),
	(try_begin),
		(eq, ":lady_reputation", lrep_ambitious),
		(val_mul, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_otherworldly),
		(val_div, ":modified_renown", 2),
		(val_mul, ":romantic_chemistry", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_adventurous),
		(val_div, ":modified_renown", 2),
	(else_try),
		(eq, ":lady_reputation", lrep_moralist),
		(val_div, ":modified_renown", 2),
		(val_div, ":romantic_chemistry", 2),
	(try_end),

	(val_add, ":weighted_romantic_assessment", ":romantic_chemistry"),
	(val_add, ":weighted_romantic_assessment", ":personality_match"),
	(val_add, ":weighted_romantic_assessment", ":modified_renown"),

	(assign, reg0, ":weighted_romantic_assessment"),

	]),

("assign_troop_love_interests", #Called at the beginning, or whenever a lord is spurned
    [
	(store_script_param, ":cur_troop", 1),
    ##diplomacy start+
	#wrap the entire thing in a try-statement: do nothing when called erroneously
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(try_begin),
	(this_or_next|is_between, ":cur_troop", lords_begin, lords_end),
	(this_or_next|is_between, ":cur_troop", companions_begin, companions_end),
	(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),#kingdom heroes only
	(troop_slot_eq, ":cur_troop", slot_troop_spouse, -1),#not married, engaged
	(troop_slot_eq, ":cur_troop", slot_troop_betrothed, -1),

	#avoid unintentional erroneous pairings (intentional exceptions can be added)
	#(troop_get_type, ":troop_type", ":cur_troop"),
	(call_script, "script_dplmc_store_troop_is_female", ":cur_troop"),
	(assign, ":troop_type", reg0),

	(try_begin),
	    #Certain personality types don't care about flouting convention.
		(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_debauched),
        (this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_roguish),
        (troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_adventurous),
		(assign, ":troop_type", abs(tf_male) + abs(tf_female) + 1),#guaranteed not to equal tf_male or tf_female
	(try_end),
	(store_faction_of_troop, ":troop_faction", ":cur_troop"),
	#assign default initial courtships for companions
	(try_begin),
		(is_between, ":cur_troop", companions_begin, companions_end),
        (troop_get_slot, ":cur_lady", ":cur_troop", slot_troop_personalitymatch_object),
        (is_between, ":cur_lady", heroes_begin, heroes_end),

		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		#(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		(lt, reg0, 2),#check not a close relative
        #(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),
		(ge, reg0, 0), #do not develop love interest if already spurned (but DO allow re-courting)

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_begin),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
		    (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
    (try_end),
    ##diplomacy end+
	(try_for_range, ":unused", 0, 50),
		(store_random_in_range, ":cur_lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":cur_lady", slot_troop_spouse, -1),
		(store_faction_of_troop, ":lady_faction", ":cur_lady"),
		(eq, ":troop_faction", ":lady_faction"),
		##diplomacy start+
		##(call_script, "script_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
        (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":cur_troop", ":cur_lady"),
		#(eq, reg0, 0),
		#right now nothing gives a value of 1, but change this check in case more distant relations are reported
		(lt, reg0, 2),#check not a close relative
		#(troop_get_type, reg0, ":cur_lady"),
		(call_script, "script_dplmc_store_troop_is_female", ":cur_lady"),
        (neq, ":troop_type", reg0),#check gender compatability
		(neq, ":cur_lady", ":cur_troop"),#check not yourself
		(neg|troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_retirement),#check in the game and not retired, exiled, dead, etc.
		(troop_slot_ge, ":cur_lady", slot_troop_occupation, slto_kingdom_hero),
        ##diplomacy end+
		(call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":cur_lady"),

		(eq, reg0, 0), #do not develop love interest if already spurned or courted

		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(neg|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
	##diplomacy start+ also allow -1 to signify no-one courted
		(try_begin),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_1, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_1, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_2, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_2, ":cur_lady"),
		(else_try),
			(this_or_next|troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, -1),#< added
			(troop_slot_eq, ":cur_troop", slot_troop_love_interest_3, 0),
			(troop_set_slot, ":cur_troop", slot_troop_love_interest_3, ":cur_lady"),
		(try_end),
	(try_end),
        (try_end),
	(assign, reg1, ":save_reg1"),
	(assign, reg0, ":save_reg0"),#revert register
	##diplomacy end+
	]),

("courtship_event_lady_break_relation_with_suitor", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":suitor", 2),

	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_slot_eq, ":suitor", ":love_interest_slot", ":lady"),
		##diplomacy start+ set to -1 instead, since 0 is the player (how annoying)
		#(troop_set_slot, ":suitor", ":love_interest_slot", 0),
		(troop_set_slot, ":suitor", ":love_interest_slot", -1),
		##diplomacy end+
	(try_end),
	(call_script, "script_assign_troop_love_interests", ":suitor"),

	(try_begin),
		(troop_slot_eq, ":lady", slot_troop_betrothed, ":suitor"),


		(troop_set_slot, ":lady", slot_troop_betrothed, -1),
	##diplomacy start+ perform the same check for the suitor that was done,
	#for the lady, so this script has no unfortunate consequences even if
	#called inappropriately.
	(try_end),
	(try_begin),
		(troop_slot_eq, ":suitor", slot_troop_betrothed, ":lady"),
		(troop_set_slot, ":suitor", slot_troop_betrothed, -1),
	##diplomacy end+
	(try_end),


	]),

("courtship_event_bride_marry_groom", #parameters from dialog or scripts
	[
	(store_script_param, ":bride", 1),
	(store_script_param, ":groom", 2),
	(store_script_param, ":elopement", 3),

	(try_begin),
		(eq, ":bride", "trp_player"),
		(assign, ":venue", "$g_encountered_party"),
	(else_try),
		(troop_get_slot, ":venue", ":bride", slot_troop_cur_center),
		##diplomacy start+
		#Ensure there is a venue.
		(lt, ":venue", 1),
		(troop_get_slot, ":venue", ":groom", slot_troop_cur_center),
		##diplomacy end+
	(try_end),

	(store_faction_of_troop, ":groom_faction", ":groom"),


	(try_begin),
		(eq, ":elopement", 0),
		(call_script, "script_add_log_entry", logent_lady_marries_suitor, ":bride", ":venue", ":groom", 0),
	(else_try),
		(call_script, "script_add_log_entry", logent_lady_elopes_with_lord, ":bride", ":venue", ":groom", 0),
	(try_end),

	(str_store_troop_name, s3, ":bride"),
	(str_store_troop_name, s4, ":groom"),
	(str_store_party_name, s5, ":venue"),

	(try_begin),
	##diplomacy start+ this should be globally-visible for notable personages
	#    (this_or_next|is_between, ":groom_faction", kingdoms_begin, kingdoms_end),
	#    (this_or_next|troop_slot_ge, ":groom", slot_troop_met, 1),
	#    (troop_slot_ge, ":bride", slot_troop_met, 1),
		(display_log_message, "str_s3_marries_s4_at_s5"),
	#(else_try),
    #    (eq, "$cheat_mode", 1),
	#    (display_message, "str_s3_marries_s4_at_s5"),
	##diplomacy end+
    (try_end),

	(troop_set_slot, ":bride", slot_troop_spouse, ":groom"),
	(troop_set_slot, ":groom", slot_troop_spouse, ":bride"),

	#Break groom's romantic relations
	(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
		(troop_set_slot, ":groom", ":love_interest_slot", 0),
	(try_end),

	#Break bride's romantic relations
	(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_slot_eq, ":active_npc", ":love_interest_slot", ":bride"),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":bride", ":active_npc"),
		(try_end),
	(try_end),



	(troop_set_slot, ":bride", slot_troop_betrothed, -1),
	(troop_set_slot, ":groom", slot_troop_betrothed, -1),



    #change relations with family
	##diplomacy start+ Include kingdom ladies
	#(try_for_range, ":family_member", lords_begin, lords_end),
	(try_for_range, ":family_member", heroes_begin, heroes_end),
		(neq, ":family_member", ":bride"),
		(neq, ":family_member", ":groom"),
	##diplomacy end+
		(call_script, "script_troop_get_family_relation_to_troop", ":bride", ":family_member"),
		(gt, reg0, 0),
		(store_div, ":family_relation_boost", reg0, 3),
		(try_begin),
			(eq, ":elopement", 1),
			(val_mul, ":family_relation_boost", -2),
		(try_end),
		##diplomacy start+ Fix error!  Change relation between groom and family member, not groom and bride.
		#(call_script, "script_troop_change_relation_with_troop", ":groom", ":bride", ":family_relation_boost"),
			(call_script, "script_troop_change_relation_with_troop", ":groom", ":family_member", ":family_relation_boost"),
		##diplomacy end+
		(val_add, "$total_courtship_quarrel_changes", ":family_relation_boost"),
	(try_end),

	(try_begin),
		(this_or_next|eq, ":groom", "trp_player"),
			(eq, ":bride", "trp_player"),
		##diplomacy start+ fix bug where player didn't get right to rule
		(call_script, "script_change_player_right_to_rule", 15),##one argument, not two
		##diplomacy end+
	(try_end),


	(try_begin),
		(eq, ":groom", "trp_player"),
		(check_quest_active, "qst_wed_betrothed"),
		(call_script, "script_succeed_quest", "qst_wed_betrothed"),
		(call_script, "script_end_quest", "qst_wed_betrothed"),
	(try_end),


	(try_begin),
		(check_quest_active, "qst_visit_lady"),
		(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, ":bride"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),


	(try_begin),
		(eq, ":groom", "trp_player"),
		(neq, "$g_polygamy", 1),
		(check_quest_active, "qst_visit_lady"),
		(call_script, "script_abort_quest", "qst_visit_lady", 0),
	(try_end),
	(try_begin),
		(eq, ":groom", "trp_player"),
		(neq, "$g_polygamy", 1),
		(check_quest_active, "qst_duel_courtship_rival"),
		(call_script, "script_abort_quest", "qst_duel_courtship_rival", 0),
	(try_end),


	(try_begin),
		(eq, ":bride", "trp_player"),
	    (call_script, "script_player_join_faction", ":groom_faction"),
		(assign, "$player_has_homage", 1),
	(else_try),
		(eq, ":groom", "trp_player"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!} DEBUG - {s4} faction change in marriage case 5"),
		(try_end),
		(troop_set_faction, ":bride", "$players_kingdom"),
        (call_script, "script_troop_set_title_according_to_faction", ":bride", "$players_kingdom"),
	(else_try),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":bride"),
			(display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 6"),
		(try_end),

		(troop_set_faction, ":bride", ":groom_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":bride", ":groom_faction"),
	(try_end),

    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),
        (unlock_achievement, ACHIEVEMENT_HAPPILY_EVER_AFTER),
		(try_begin),
			(eq, ":elopement", 1),
			(unlock_achievement, ACHIEVEMENT_HEART_BREAKER),
		(try_end),
    (try_end),



    (try_begin),
        (this_or_next|eq, ":groom", "trp_player"),
           (eq, ":bride", "trp_player"),

        (try_begin),
            (eq, ":elopement", 0),
            (call_script, "script_start_wedding_cutscene", ":groom", ":bride"),
        (else_try), #dckplmc: elope
             (assign, "$g_wedding_groom_troop", ":groom"),
             (assign, "$g_wedding_bride_troop", ":bride"),
             (assign, "$g_wedding_brides_dad_troop", "trp_nurse_for_lady"),
             (assign, "$g_wedding_bishop_troop", "trp_temporary_minister"),

             (modify_visitors_at_site,"scn_wedding"),
             (reset_visitors,0),
             (set_visitor, 0, ":groom"),
             (set_visitor, 1, ":bride"),
             (set_visitor, 2, "trp_nurse_for_lady"),
             (set_visitor, 3, "trp_temporary_minister"),
             (set_jump_mission,"mt_wedding"),
             (jump_to_scene,"scn_wedding"),
             (change_screen_mission),
         (try_end),
    (try_end),
	]),

("npc_decision_checklist_male_guardian_assess_suitor", #parameters from dialog
	[
	(store_script_param, ":lord", 1),
	(store_script_param, ":suitor", 2),

	(troop_get_slot, ":lord_reputation", ":lord", slot_lord_reputation_type),
	(store_faction_of_troop, ":lord_faction", ":lord"),

	(try_begin),
		(eq, ":suitor", "trp_player"),
		(assign, ":suitor_faction", "$players_kingdom"),
	(else_try),
		(store_faction_of_troop, ":suitor_faction", ":suitor"),
	(try_end),
	(store_relation, ":faction_relation_with_suitor", ":lord_faction", ":suitor_faction"),

	(call_script, "script_troop_get_relation_with_troop", ":lord", ":suitor"),
	(assign, ":lord_suitor_relation", reg0),



	(troop_get_slot, ":suitor_renown", ":suitor", slot_troop_renown),


	(assign, ":competitor_found", -1),

	(try_begin),
		(eq, ":suitor", "trp_player"),
		(gt, "$marriage_candidate", 0),

		(try_for_range, ":competitor", lords_begin, lords_end),
			(store_faction_of_troop, ":competitor_faction", ":competitor"),
			(eq, ":competitor_faction", ":lord_faction"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_1, "$marriage_candidate"),
			(this_or_next|troop_slot_eq, ":competitor", slot_troop_love_interest_2, "$marriage_candidate"),
				(troop_slot_eq, ":competitor", slot_troop_love_interest_3, "$marriage_candidate"),

			(call_script, "script_troop_get_relation_with_troop", ":competitor", ":lord"),
			(gt, reg0, 5),

			(troop_slot_ge, ":competitor", slot_troop_renown, ":suitor_renown"),  #higher renown than player

			(assign, ":competitor_found", ":competitor"),
			(str_store_troop_name, s14, ":competitor"),
			(str_store_troop_name, s16, "$marriage_candidate"),
		(try_end),
	(try_end),

	#renown
	(try_begin),
		(lt, ":suitor_renown", 50),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_quarrelsome),
		(this_or_next|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
			(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_selfrighteous),
		(assign, ":explainer_string", "str_excuse_me_how_can_you_possibly_imagine_yourself_worthy_to_marry_into_our_family"),
		(assign, ":result", -3),
	(else_try),
		(lt, ":suitor_renown", 50),
		(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),

		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction_fight_hard_count_your_dinars_and_perhaps_some_day_in_the_future_we_may_speak_of_such_things_my_good_man"),
		(assign, ":result", -1),
	(else_try),
		(lt, ":suitor_renown", 50),

		(assign, ":explainer_string", "str_em_with_regard_to_her_ladyship_we_were_looking_specifically_for_a_groom_of_some_distinction"),
		(assign, ":result", -2),

	(else_try),
		(lt, ":suitor_renown", 200),
		(neg|troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_goodnatured),
		(assign, ":explainer_string", "str_it_is_too_early_for_you_to_be_speaking_of_such_things_you_are_still_making_your_mark_in_the_world"),

		(assign, ":result", -1),

	(else_try), #wrong faction
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(str_store_faction_name, s4, ":lord_faction"),
		(this_or_next|eq, ":lord_reputation", lrep_quarrelsome),
			(eq, ":lord_reputation", lrep_debauched),
		(assign, ":explainer_string", "str_you_dont_serve_the_s4_so_id_say_no_one_day_we_may_be_at_war_and_i_prefer_not_to_have_to_kill_my_inlaws_if_at_all_possible"),

		(assign, ":result", -1),

	(else_try),
		(eq, ":suitor", "trp_player"),
		(neq, ":suitor_faction", "$players_kingdom"),
		(neq, ":lord_reputation", lrep_goodnatured),
		(neq, ":lord_reputation", lrep_cunning),

		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),

		(assign, ":result", -1),
	(else_try),
		(eq, ":suitor", "trp_player"),
		(lt, ":faction_relation_with_suitor", 0),

		(assign, ":explainer_string", "str_as_you_are_not_a_vassal_of_the_s4_i_must_decline_your_request_the_twists_of_fate_may_mean_that_we_will_one_day_cross_swords_and_i_would_hope_not_to_make_a_widow_of_a_lady_whom_i_am_obligated_to_protect"),

		(assign, ":result", -1),

	(else_try),
		(eq, ":suitor", "trp_player"),
		(neq, "$player_has_homage", 1),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),

		(assign, ":explainer_string", "str_as_you_are_not_a_pledged_vassal_of_our_liege_with_the_right_to_hold_land_i_must_refuse_your_request_to_marry_into_our_family"),

		(assign, ":result", -1),
	(else_try),
		(gt, ":competitor_found", -1),

		(this_or_next|eq, ":lord_reputation", lrep_selfrighteous),
		(this_or_next|eq, ":lord_reputation", lrep_debauched),
		(this_or_next|eq, ":lord_reputation", lrep_martial),
			(eq, ":lord_reputation", lrep_quarrelsome),

		(assign, ":explainer_string",	"str_look_here_lad__the_young_s14_has_been_paying_court_to_s16_and_youll_have_to_admit__hes_a_finer_catch_for_her_than_you_so_lets_have_no_more_of_this_talk_shall_we"),
		(assign, ":result", -1),

	(else_try),
		(lt, ":lord_suitor_relation", -4),



		(assign, ":explainer_string", "str_i_do_not_care_for_you_sir_and_i_consider_it_my_duty_to_protect_the_ladies_of_my_household_from_undesirable_suitors"),
		(assign, ":result", -3),
	(else_try),
		(lt, ":lord_suitor_relation", 5),

		(assign, ":explainer_string",	"str_hmm_young_girls_may_easily_be_led_astray_so_out_of_a_sense_of_duty_to_the_ladies_of_my_household_i_think_i_would_like_to_get_to_know_you_a_bit_better_we_may_speak_of_this_at_a_later_date"),
		(assign, ":result", -1),
	(else_try),

		(assign, ":explainer_string",	"str_you_may_indeed_make_a_fine_match_for_the_young_mistress"),
		(assign, ":result", 1),
	(try_end),

	(assign, reg0, ":result"),
	(assign, reg1, ":explainer_string"),

	]),

("npc_decision_checklist_marry_female_pc", #
	[
	(store_script_param, ":npc", 1),
    #diplomacy start+ (players of either gender may marry opposite-gender lords)
    #  Note that many of the strings used here have been altered to change based on the player's gender.
	#  Also, it should be mention that reason is written to s14.
	(assign, ":save_reg1", reg1),
	#Use gender script
	(call_script, "script_dplmc_store_is_female_troop_1_troop_2", "trp_player", ":npc"),
	(assign, ":is_female", reg0),
	(assign, ":npc_female", reg1),
    #diplomacy end+

	(troop_get_slot, ":npc_reputation_type", ":npc", slot_lord_reputation_type),

	(call_script, "script_troop_get_romantic_chemistry_with_troop", ":npc", "trp_player"),
	(assign, ":romantic_chemistry", reg0),

	(call_script, "script_troop_get_relation_with_troop", ":npc", "trp_player"),
	(assign, ":relation_with_player", reg0),

	(assign, ":competitor", -1),
	(try_for_range, ":competitor_candidate", kingdom_ladies_begin, kingdom_ladies_end),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_1, ":competitor_candidate"),
		(this_or_next|troop_slot_eq, ":npc", slot_troop_love_interest_2, ":competitor_candidate"),
			(troop_slot_eq, ":npc", slot_troop_love_interest_3, ":competitor_candidate"),
		(call_script, "script_troop_get_relation_with_troop", ":npc", ":competitor"),
		(assign, ":competitor_relation", reg0),

		(gt, ":competitor_relation", ":relation_with_player"),
		(assign, ":competitor", ":competitor_candidate"),
	(try_end),

	(assign, ":player_possessions", 0),
	(try_for_range, ":center", centers_begin, centers_end),
		(troop_slot_eq, ":center", slot_town_lord, "trp_player"),
		(val_add, ":player_possessions", 1),
	(try_end),

	(assign, ":lord_agrees", 0),
	#reasons for refusal
	(try_begin),
		(troop_slot_ge, "trp_player", slot_troop_betrothed, active_npcs_begin),
		(neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":npc"),

		(str_store_string, s14, "str_my_lady_engaged_to_another"),
	(else_try),
		#bad relationship - minor
		(lt, ":relation_with_player", -3),
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
		(this_or_next|eq, ":npc_reputation_type", lrep_cunning),
		##diplomacy start+ also test commoner types
		(this_or_next|eq, ":npc_reputation_type", lrep_roguish),
		(this_or_next|eq, ":npc_reputation_type", lrep_custodian),
		(this_or_next|eq, ":npc_reputation_type", lrep_benefactor),
		#And certain lady types?
		(this_or_next|eq, ":npc_reputation_type", lrep_ambitious),
		(this_or_next|eq, ":npc_reputation_type", lrep_moralist),
		##diplomacy end+
			(eq, ":npc_reputation_type", lrep_goodnatured),

		(str_store_string, s14, "str_madame__given_our_relations_in_the_past_this_proposal_is_most_surprising_i_do_not_think_that_you_are_the_kind_of_woman_who_can_be_bent_to_a_hushands_will_and_i_would_prefer_not_to_have_our_married_life_be_a_source_of_constant_acrimony"),

	(else_try), #really bad relationship
		(lt, ":relation_with_player", -10),

		(this_or_next|eq, ":npc_reputation_type", lrep_quarrelsome),
		(this_or_next|eq, ":npc_reputation_type", lrep_debauched),
			(eq, ":npc_reputation_type", lrep_selfrighteous),

		(str_store_string, s14, "str_i_would_prefer_to_marry_a_proper_maiden_who_will_obey_her_husband_and_is_not_likely_to_split_his_head_with_a_sword"),
	(else_try),
		(lt, ":romantic_chemistry", 5),

		(str_store_string, s14, "str_my_lady_not_sufficient_chemistry"),

	(else_try), #would prefer someone more ladylike
		(this_or_next|eq, ":npc_reputation_type", lrep_upstanding),
			(eq, ":npc_reputation_type", lrep_martial),
        #diplomacy start+ (players of either gender may marry opposite-gender lords)
        #I tried to keep this as symmetric as possible, but this sentence is ridiculous with reversed genders
		(neq, ":npc_female", 1),
        (eq, ":is_female", 1),
		#To reduce annoyance, I've changed this away from an absolute prohibition.
		(troop_get_slot, ":veto", ":npc", slot_troop_set_decision_seed),
		(val_add, ":veto", "$romantic_attraction_seed"),
		(val_mod, ":veto", 5),#4 out of 5 will still automatically refuse
		(try_begin),#make an exception for companions
			(is_between, ":npc", companions_begin, companions_end),
			(assign, ":veto", 0),
		(else_try),
			#On diminished prejudice mode, get rid of the "80% automatically refuse" condition.
			(ge, "$g_disable_condescending_comments", 2),
			(assign, ":veto", 0),
		(try_end),
		(try_begin),
			#Skip the subsequent checks if there's no way for them to pass
			(neq, ":veto", 0),
		(else_try),
			#Requires high chemistry, high relation, and positive honor
			(this_or_next|lt, ":romantic_chemistry", 15),
			(this_or_next|lt, ":relation_with_player", 30),
				(lt, "$player_honor", 10),
			(assign, ":veto", 1),
		(else_try),
			#Relation must be above some arbitrary threshold (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_sub, reg0, 100, ":romantic_chemistry"),
			(lt, ":relation_with_player", reg0),
			(assign, ":veto", 1),
		(else_try),
			#The lord's level must not be less than 75% of the player's (only if prejudice settings are not "low")
			(lt, "$g_disable_condescending_comments", 2),
			(store_character_level, reg0, "trp_player"),
			(val_mul, reg0, 3),
			(val_div, reg0, 4),
			(store_character_level, reg1, ":npc"),
			(lt, reg1, reg0),
			(assign, ":veto", 1),
		(else_try),
			#One of the lord's female relatives must like the player, if any such lords exist.
			(lt, "$g_disable_condescending_comments", 2),
			(troop_get_slot, ":npc_mother", ":npc", slot_troop_mother),
			(assign, reg1, 0),#3 = some disapproved, 2 = some approved, 1 = some existed and had no opinion, 0 = there were none
			(try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_ge, ":kingdom_lady", slot_troop_occupation, slto_retirement),
				(assign, reg0, 0),
				(try_begin),
					(troop_slot_eq, ":kingdom_lady", slot_troop_guardian, ":npc"),
					(assign, reg0, 1),
				(else_try),
					(is_between, ":npc_mother", heroes_begin, heroes_end),
					(this_or_next|eq, ":kingdom_lady", ":npc_mother"),
						(troop_slot_eq, ":kingdom_lady", slot_troop_mother, ":npc_mother"),
					(assign, reg0, 1),
				(try_end),
				(neq, reg0, 0),
				(call_script, "script_troop_get_player_relation", ":kingdom_lady"),
				(try_begin),#some were found and like the player
					(ge, reg0, 1),
					(val_max, reg1, 2),
				(else_try),#some were found and have no opinion
					(eq, reg0, 0),
					(val_max, reg1, 1),
				(else_try),#some were found and dislike the player
					(val_max, reg1, 3),
				(try_end),
			(try_end),
			(neq, reg0, 0),
			(neq, reg0, 2),
			(assign, ":veto", 1),
		(try_end),
		#Check if the veto holds
		(neq, ":veto", 0),
        #diplomacy end+

		(str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	(else_try),
		(eq, ":npc_reputation_type", lrep_quarrelsome),
		(lt, ":romantic_chemistry", 15),

		(str_store_string, s14, "str_nah_i_want_a_woman_wholl_keep_quiet_and_do_what_shes_told_i_dont_think_thats_you"),
	(else_try), #no properties
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),

		(ge, ":romantic_chemistry", 10),
		(eq, ":player_possessions", 0),

		(str_store_string, s14, "str_my_lady_you_are_possessed_of_great_charms_but_no_properties_until_you_obtain_some_to_marry_you_would_be_an_act_of_ingratitude_towards_my_ancestors_and_my_lineage"),

	(else_try), #you're a nobody - I can do better
		(this_or_next|eq, ":npc_reputation_type", lrep_selfrighteous),
			(eq, ":npc_reputation_type", lrep_debauched),

		(eq, ":player_possessions", 0),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_no_known_family_of_no_possessions__in_short_a_nobody_do_you_think_that_you_are_fit_to_marry_into_may_family"),
	(else_try), #just not that into you
		(lt, ":romantic_chemistry", 5),
		(lt, ":relation_with_player", 20),

		(neq, ":npc_reputation_type", lrep_debauched),
		(neq, ":npc_reputation_type", lrep_selfrighteous),

		(str_store_string, s14, "str_my_lady__forgive_me__the_quality_of_our_bond_is_not_of_the_sort_which_the_poets_tell_us_is_necessary_to_sustain_a_happy_marriage"),

	(else_try), #you're a liability, given your relation with the liege
		(eq, ":npc_reputation_type", lrep_cunning),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		(str_store_troop_name, s4, ":leader"),
		(call_script, "script_troop_get_relation_with_troop", ":leader", "trp_player"),
		(lt, reg0, -10),

		(str_store_string, s14, "str_um_i_think_that_if_i_want_to_stay_on_s4s_good_side_id_best_not_marry_you"),
	(else_try),	#part of another faction
		(gt, "$players_kingdom", 0),
		(neq, "$players_kingdom", "$g_talk_troop_faction"),
		(faction_get_slot, ":leader", slot_faction_leader, "$g_talk_troop_faction"),
		##diplomacy start+ use gender script
		#(troop_get_type, reg4, ":leader"),
		(call_script, "script_dplmc_store_troop_is_female_reg", ":leader", 4),
		##diplomacy end+

		(str_store_string, s14, "str_you_serve_another_realm_i_dont_see_s4_granting_reg4herhis_blessing_to_our_union"),
	(else_try), #there's a competitor
		(gt, ":competitor", -1),
		(str_store_troop_name, s4, ":competitor"),

		(str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
    ##diplomacy start+
	#By default these should not be reachable, but future changes may expose them
	#unintentionally.
	(else_try),#redundant: shouldn't be called for betrothed lords
	   (troop_slot_ge, ":npc", slot_troop_betrothed, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_betrothed),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for married lords
	   (troop_slot_ge, ":npc", slot_troop_spouse, 1),
	   (troop_get_slot, ":competitor", ":npc", slot_troop_spouse),
	   (str_store_troop_name, s4, ":competitor"),
	   (str_store_string, s14, "str_madame_my_heart_currently_belongs_to_s4"),
	(else_try),#redundant: shouldn't be called for claimants or kings
	   (this_or_next|is_between, ":npc", kings_begin, kings_end),
	      (is_between, ":npc", pretenders_begin, pretenders_end),
	   #This probably wouldn't ever occur, but put a string here just in case.
	   #The male version is ridiculous.
	   (str_store_string, s14, "str_my_lady_while_i_admire_your_valor_you_will_forgive_me_if_i_tell_you_that_a_woman_like_you_does_not_uphold_to_my_ideal_of_the_feminine_of_the_delicate_and_of_the_pure"),
	##diplomacy end+
	(else_try),
		(lt, ":relation_with_player", 10),
		(assign, ":lord_agrees", 2),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_shall_give_your_proposal_consideration"),
	(else_try),
		(assign, ":lord_agrees", 1),

		(str_store_string, s14, "str_my_lady_you_are_a_woman_of_great_spirit_and_bravery_possessed_of_beauty_grace_and_wit_i_would_be_most_honored_were_you_to_become_my_wife"),
	(try_end),

    ##diplomacy start+ revert register
	(assign, reg1, ":save_reg1"),
	##diplomacy end+
	(assign, reg0, ":lord_agrees"),

	]
	),

("courtship_poem_reactions", #parameters from dialog
	[
	(store_script_param, ":lady", 1),
	(store_script_param, ":poem", 2),

	(troop_get_slot, ":lady_reputation", ":lady", slot_lord_reputation_type),

	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":poem"),
		(assign, reg5, ":lady_reputation"),
		(display_message, "str_poem_choice_reg4_lady_rep_reg5"),
	(try_end),

	(try_begin), #conventional ++, ambitious -, adventurous -
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_ah__kais_and_layali__such_a_sad_tale_many_a_time_has_it_been_recounted_for_my_family_by_the_wandering_poets_who_come_to_our_home_and_it_has_never_failed_to_bring_tears_to_our_eyes"),
		(assign, ":result", 5),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_kais_and_layali_three_hundred_stanzas_of_pathetic_sniveling_if_you_ask_me_if_kais_wanted_to_escape_heartbreak_he_should_have_learned_to_live_within_his_station_and_not_yearn_for_what_he_cannot_have"),
		(assign, ":result", 0),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_kais_and_layali_no_one_should_ever_have_written_such_a_sad_poem_if_it_was_the_destiny_of_kais_and_layali_to_be_together_than_their_love_should_have_conquered_all_obstacles"),
		(assign, ":result", 1),
	(else_try),
		(eq, ":poem", courtship_poem_tragic),
#		moralizing and adventurous
		(str_store_string, s11, "str_ah_kais_and_layali_a_very_old_standby_but_moving_in_its_way"),
		(assign, ":result", 3),
	#Heroic
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_such_happy_times_in_which_our_ancestors_lived_women_like_kara_could_venture_out_into_the_world_like_men_win_a_name_for_themselves_and_not_linger_in_their_husbands_shadow"),
		(assign, ":result", 5),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_ah_the_saga_of_helgered_and_kara_now_there_was_a_lady_who_knew_what_she_wanted_and_was_not_afraid_to_obtain_it"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_a_terrible_tale__but_it_speaks_of_a_very_great_love_if_she_were_willing_to_make_war_on_her_own_family"),
		(assign, ":result", 2),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_as_i_recall_kara_valued_her_own_base_passions_over_duty_to_her_family_that_she_made_war_on_her_own_father_i_have_no_time_for_a_poem_which_praises_such_a_woman"),
		(assign, ":result", 0),
	(else_try), #adventurous ++, conventional -1, moralizing -1
		(eq, ":poem", courtship_poem_heroic),
		(eq, ":lady_reputation", lrep_conventional),
		(str_store_string, s11, "str_the_saga_of_helgered_and_kara_how_could_a_woman_don_armor_and_carry_a_sword_how_could_a_man_love_so_ungentle_a_creature"),
		(assign, ":result", 0),
	#Comic
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_conversation_in_the_garden_i_cannot_understand_the_lady_in_that_poem_if_she_loves_the_man_why_does_she_tease_him_so"),
		(assign, ":result", 0),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_conversation_in_the_garden_let_us_see__it_is_morally_unedifying_it_exalts_deception_it_ends_with_a_maiden_surrendering_to_her_base_passions_and_yet_i_cannot_help_but_find_it_charming_perhaps_because_it_tells_us_that_love_need_not_be_tragic_to_be_memorable"),
		(assign, ":result", 1),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_conversation_in_the_garden_now_that_is_a_tale_every_lady_should_know_by_heart_to_learn_the_subtleties_of_the_politics_she_must_practice"),
		(assign, ":result", 5),
	(else_try), #ambitious ++, romantic -, moralizing 0
		(eq, ":poem", courtship_poem_comic),
		#adventurous, conventional
		(str_store_string, s11, "str_a_conversation_in_the_garden_it_is_droll_i_suppose__although_there_is_nothing_there_that_truly_stirs_my_soul"),
		(assign, ":result", 3),

	#Allegoric
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_adventurous),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_the_lady_sits_within_doing_nothing_while_the_man_is_the_one_who_strives_and_achieves_i_have_enough_of_that_in_my_daily_life_why_listen_to_poems_about_it"),
		(assign, ":result", 0),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(this_or_next|eq, ":lady_reputation", lrep_conventional),
			(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_an_uplifting_tribute_to_the_separate_virtues_of_man_and_woman"),
		(assign, ":result", 3),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_yes_but_although_it_is_a_fine_tale_of_virtues_it_speaks_nothing_of_passion"),
		(assign, ":result", 1),
	(else_try), #moralizing ++, adventurous -, romantic -
		(eq, ":poem", courtship_poem_allegoric),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_storming_the_fortress_of_love_ah_a_sermon_dressed_up_as_a_love_poem_if_you_ask_me"),
		(assign, ":result", 1),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_otherworldly),
		(str_store_string, s11, "str_a_hearts_desire_ah_such_a_beautiful_account_of_the_perfect_perfect_love_to_love_like_that_must_be_to_truly_know_rapture"),
		(assign, ":result", 4),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_ambitious),
		(str_store_string, s11, "str_a_hearts_desire_silly_if_you_ask_me_if_the_poet_desires_a_lady_then_he_should_endeavor_to_win_her__and_not_dress_up_his_desire_with_a_pretense_of_piety"),
		(assign, ":result", 0),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(eq, ":lady_reputation", lrep_moralist),
		(str_store_string, s11, "str_a_hearts_desire_hmm__it_is_an_interesting_exploration_of_earthly_and_divine_love_it_does_speak_of_the_spiritual_quest_which_brings_out_the_best_in_man_but_i_wonder_if_the_poet_has_not_confused_his_yearning_for_higher_things_with_his_baser_passions"),
		(assign, ":result", 2),

	(else_try), #romantic ++, moralizing 0, ambitious -
		(eq, ":poem", courtship_poem_mystic),
		(str_store_string, s11, "str_a_hearts_desire_oh_yes__it_is_very_worthy_and_philosophical_but_if_i_am_to_listen_to_a_bard_strum_a_lute_for_three_hours_i_personally_prefer_there_to_be_a_bit_of_a_story"),
		(assign, ":result", 1),
	(try_end),


	(try_begin),
		(eq, "$cheat_mode", 1),
		(assign, reg4, ":result"),
		(display_message, "str_result_reg4_string_s11"),
	(try_end),


	(assign, reg0, ":result"),

	]),

("character_can_wed_character", #empty now, but might want to add mid-game
	[
	]),

("test_player_for_career_and_marriage_incompatability", #empty now, but might want to add mid-game
	[
	#Married to a lord of one faction, while fighting for another
	#Married to one lord while holding a stipend from the king
	]),
]