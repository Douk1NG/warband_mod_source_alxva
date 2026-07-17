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
# NATIVE MISCELLANEOUS SCRIPTS
# 
# This file contains the remaining scripts of the Native module that didn't fit neatly
# into the other domains. (Utility functions, getters, setters, presentations logic, etc).
####################################################################################################################

misc_scripts = [
  # INPUT: arg1 = slider_value
  # OUTPUT: reg0 = army_size
  ("get_army_size_from_slider_value",
    [
     (store_script_param, ":slider_value", 1),
     (assign, ":army_size", ":slider_value"),
     (try_begin),
       (gt, ":slider_value", 25),
       (store_sub, ":adder_value", ":slider_value", 25),
       (val_add, ":army_size", ":adder_value"),
       (try_begin),
         (gt, ":slider_value", 50),
         (store_sub, ":adder_value", ":slider_value", 50),
         (val_mul, ":adder_value", 3),
         (val_add, ":army_size", ":adder_value"),
       (try_end),
     (try_end),
     (assign, reg0, ":army_size"),
  ]),

  #script_spawn_quick_battle_army
  # INPUT: arg1 = initial_entry_point, arg2 = faction_no, arg3 = infantry_ratio, arg4 = archers_ratio, arg5 = cavalry_ratio, arg6 = divide_archer_entry_points, arg7 = player_team
  # OUTPUT: none
  ("spawn_quick_battle_army",
   [
     (store_script_param, ":cur_entry_point", 1),
     (store_script_param, ":faction_no", 2),
     (store_script_param, ":infantry_ratio", 3),
     (store_script_param, ":archers_ratio", 4),
     (store_script_param, ":cavalry_ratio", 5),
     (store_script_param, ":divide_archer_entry_points", 6),
     (store_script_param, ":player_team", 7),

     (try_begin),
       (eq, ":player_team", 1),
       (call_script, "script_get_army_size_from_slider_value", "$g_quick_battle_army_1_size"),
       (assign, ":army_size", reg0),
       (set_player_troop, "$g_quick_battle_troop"),
       (set_visitor, ":cur_entry_point", "$g_quick_battle_troop"),
       (try_begin),
         (eq, ":cur_entry_point", 0),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_0_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_0_banner", "mesh_banners_default_b"),
         (try_end),
       (else_try),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_1_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_1_banner", "mesh_banners_default_b"),
         (try_end),
       (try_end),
       (val_add, ":cur_entry_point", 1),

     (else_try),
       (call_script, "script_get_army_size_from_slider_value", "$g_quick_battle_army_2_size"),
       (assign, ":army_size", reg0),
       (try_begin),
         (eq, ":cur_entry_point", 0),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_0_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_0_banner", "mesh_banners_default_a"),
         (try_end),
       (else_try),
         (try_begin),
           (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
           (faction_get_slot, "$g_quick_battle_team_1_banner", ":faction_no", slot_faction_banner),
         (else_try),
           (assign, "$g_quick_battle_team_1_banner", "mesh_banners_default_a"),
         (try_end),
       (try_end),
       (val_add, ":cur_entry_point", 1),
     (try_end),

     (store_mul, ":num_infantry", ":infantry_ratio", ":army_size"),
     (val_div, ":num_infantry", 100),
     (store_mul, ":num_archers", ":archers_ratio", ":army_size"),
     (val_div, ":num_archers", 100),
     (store_mul, ":num_cavalry", ":cavalry_ratio", ":army_size"),
     (val_div, ":num_cavalry", 100),

     (try_begin),
       (store_add, ":num_total", ":num_infantry", ":num_archers"),
       (val_add, ":num_total", ":num_cavalry"),
       (neq, ":num_total", ":army_size"),
       (store_sub, ":leftover", ":army_size", ":num_total"),
       (try_begin),
         (gt, ":infantry_ratio", ":archers_ratio"),
         (gt, ":infantry_ratio", ":cavalry_ratio"),
         (val_add, ":num_infantry", ":leftover"),
       (else_try),
         (gt, ":archers_ratio", ":cavalry_ratio"),
         (val_add, ":num_archers", ":leftover"),
       (else_try),
         (val_add, ":num_cavalry", ":leftover"),
       (try_end),
     (try_end),

     (store_mul, ":rand_min", ":num_infantry", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_infantry", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_infantry", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_infantry", ":num_infantry", ":num_tier_2_infantry"),
     (store_mul, ":rand_min", ":num_archers", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_archers", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_archers", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_archers", ":num_archers", ":num_tier_2_archers"),
     (store_mul, ":rand_min", ":num_cavalry", 15),
     (val_div, ":rand_min", 100),
     (store_mul, ":rand_max", ":num_cavalry", 45),
     (val_div, ":rand_max", 100),
     (store_random_in_range, ":num_tier_2_cavalry", ":rand_min", ":rand_max"),
     (store_sub, ":num_tier_1_cavalry", ":num_cavalry", ":num_tier_2_cavalry"),

     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_infantry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_infantry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_infantry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_infantry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_cavalry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_cavalry"),
     (val_add, ":cur_entry_point", 1),
     (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_cavalry),
     (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_cavalry"),
     (val_add, ":cur_entry_point", 1),

     (try_begin),
       (eq, ":divide_archer_entry_points", 0),
       (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_archer),
       (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_2_archers"),
       (val_add, ":cur_entry_point", 1),
       (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_archer),
       (set_visitors, ":cur_entry_point", ":cur_troop", ":num_tier_1_archers"),
       (val_add, ":cur_entry_point", 1),
     (else_try),
       (assign, ":cur_entry_point", 40), #archer positions begin point
       (store_div, ":num_tier_1_archers_ceil_8", ":num_tier_1_archers", 8),
       (val_mul, ":num_tier_1_archers_ceil_8", 8),
       (try_begin),
         (neq, ":num_tier_1_archers_ceil_8", ":num_tier_1_archers"),
         (val_div, ":num_tier_1_archers_ceil_8", 8),
         (val_add, ":num_tier_1_archers_ceil_8", 1),
         (val_mul, ":num_tier_1_archers_ceil_8", 8),
       (try_end),
       (store_div, ":num_tier_2_archers_ceil_8", ":num_tier_2_archers", 8),
       (val_mul, ":num_tier_2_archers_ceil_8", 8),
       (try_begin),
         (neq, ":num_tier_2_archers_ceil_8", ":num_tier_2_archers"),
         (val_div, ":num_tier_2_archers_ceil_8", 8),
         (val_add, ":num_tier_2_archers_ceil_8", 1),
         (val_mul, ":num_tier_2_archers_ceil_8", 8),
       (try_end),
       (store_add, ":num_archers_ceil_8", ":num_tier_1_archers_ceil_8", ":num_tier_2_archers_ceil_8"),
       (store_div, ":num_archers_per_entry_point", ":num_archers_ceil_8", 8),
       (assign, ":left_tier_1_archers", ":num_tier_1_archers"),
       (assign, ":left_tier_2_archers", ":num_tier_2_archers"),
       (assign, ":end_cond", 1000),
       (try_for_range, ":unused", 0, ":end_cond"),
         (try_begin),
           (gt, ":left_tier_2_archers", 0),
           (assign, ":used_tier_2_archers", ":num_archers_per_entry_point"),
           (val_min, ":used_tier_2_archers", ":left_tier_2_archers"),
           (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_2_archer),
           (set_visitors, ":cur_entry_point", ":cur_troop", ":used_tier_2_archers"),
           (val_add, ":cur_entry_point", 1),
           (val_sub, ":left_tier_2_archers", ":used_tier_2_archers"),
         (else_try),
           (gt, ":left_tier_1_archers", 0),
           (assign, ":used_tier_1_archers", ":num_archers_per_entry_point"),
           (val_min, ":used_tier_1_archers", ":left_tier_1_archers"),
           (faction_get_slot, ":cur_troop", ":faction_no", slot_faction_quick_battle_tier_1_archer),
           (set_visitors, ":cur_entry_point", ":cur_troop", ":used_tier_1_archers"),
           (val_add, ":cur_entry_point", 1),
           (val_sub, ":left_tier_1_archers", ":used_tier_1_archers"),
         (else_try),
           (assign, ":end_cond", 0),
         (try_end),
       (try_end),
     (try_end),
     ]),

  ("player_arrived",
   [
      # (assign, ":player_faction_culture", "fac_culture_1"),
      #SB : align start faction culture
      (party_relocate_near_party, "p_main_party", "$g_starting_town", 2),
      (party_get_slot, ":player_faction_culture", "$g_starting_town", slot_center_culture),
      (faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":player_faction_culture"),
      (faction_set_slot, "fac_player_faction",  slot_faction_culture, ":player_faction_culture"),
      (party_set_morale, "p_main_party", 100),
    ]),


  #script_game_set_multiplayer_mission_end
  # INPUT: arg1 = groom_troop, arg2 = bride_troop
  # OUTPUT: none
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


  # script_game_get_troop_wage
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("add_kill_death_counts",
   [
      (store_script_param, ":killer_agent_no", 1),
      (store_script_param, ":dead_agent_no", 2),

      (try_begin),
        (ge, ":killer_agent_no", 0),
        (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
      (else_try),
        (assign, ":killer_agent_team", -1),
      (try_end),

      (try_begin),
        (ge, ":dead_agent_no", 0),
        (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
      (else_try),
        (assign, ":dead_agent_team", -1),
      (try_end),

      #adjusting kill counts of players/bots
      (try_begin),
        (try_begin),
          (ge, ":killer_agent_no", 0),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":killer_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (neq, ":killer_agent_no", ":dead_agent_no"),

          (this_or_next|neq, ":killer_agent_team", ":dead_agent_team"),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),

          (agent_get_player_id, ":killer_agent_player", ":killer_agent_no"),
          (try_begin),
            (agent_is_non_player, ":killer_agent_no"), #if killer agent is bot then increase bot kill counts of killer agent's team by one.
            (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
            (team_get_bot_kill_count, ":killer_agent_team_bot_kill_count", ":killer_agent_team"),
            (val_add, ":killer_agent_team_bot_kill_count", 1),
            (team_set_bot_kill_count, ":killer_agent_team", ":killer_agent_team_bot_kill_count"),
          (else_try), #if killer agent is not bot then increase kill counts of killer agent's player by one.
            (player_is_active, ":killer_agent_player"),
            (player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player"),
            (val_add, ":killer_agent_player_kill_count", 1),
            (player_set_kill_count, ":killer_agent_player", ":killer_agent_player_kill_count"),
          (try_end),
        (try_end),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (try_begin),
            (agent_is_non_player, ":dead_agent_no"), #if dead agent is bot then increase bot kill counts of dead agent's team by one.
            (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
            (team_get_bot_death_count, ":dead_agent_team_bot_death_count", ":dead_agent_team"),
            (val_add, ":dead_agent_team_bot_death_count", 1),
            (team_set_bot_death_count, ":dead_agent_team", ":dead_agent_team_bot_death_count"),
          (else_try), #if dead agent is not bot then increase death counts of dead agent's player by one.
            (agent_get_player_id, ":dead_agent_player", ":dead_agent_no"),
            (player_is_active, ":dead_agent_player"),
            (player_get_death_count, ":dead_agent_player_death_count", ":dead_agent_player"),
            (val_add, ":dead_agent_player_death_count", 1),
            (player_set_death_count, ":dead_agent_player", ":dead_agent_player_death_count"),
          (try_end),

          (try_begin),
            (assign, ":continue", 0),

            (try_begin),
              (this_or_next|lt, ":killer_agent_no", 0), #if he killed himself (1a(team change) or 1b(self kill)) then decrease kill counts of killer player by one.
              (eq, ":killer_agent_no", ":dead_agent_no"),
              (assign, ":continue", 1),
            (try_end),

            (try_begin),
              (eq, ":killer_agent_team", ":dead_agent_team"), #if he killed a teammate and game mod is not deathmatch then decrease kill counts of killer player by one.
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
              (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
              (assign, ":continue", 1),
            (try_end),

            (eq, ":continue", 1),

            (try_begin),
              (ge, ":killer_agent_no", 0),
              (assign, ":responsible_agent", ":killer_agent_no"),
            (else_try),
              (assign, ":responsible_agent", ":dead_agent_no"),
            (try_end),

            (try_begin),
              (ge, ":responsible_agent", 0),
              (neg|agent_is_non_player, ":responsible_agent"),
              (agent_get_player_id, ":responsible_player", ":responsible_agent"),
              (ge, ":responsible_player", 0),
              (player_get_kill_count, ":dead_agent_player_kill_count", ":responsible_player"),
              (val_add, ":dead_agent_player_kill_count", -1),
              (player_set_kill_count, ":responsible_player", ":dead_agent_player_kill_count"),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
    ]),

  #script_warn_player_about_auto_team_balance
  # INPUT: none
  # OUTPUT: none
  ("warn_player_about_auto_team_balance",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
     (start_presentation, "prsnt_multiplayer_message_2"),
     ]),

  #script_check_team_balance
  # INPUT: none
  # OUTPUT: none
  ("check_team_balance",
   [
     (try_begin),
       (multiplayer_is_server),

       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
         (player_get_team_no, ":player_team", ":cur_player"),
         (try_begin),
           (eq, ":player_team", 0),
           (val_add, ":number_of_players_at_team_1", 1),
         (else_try),
           (eq, ":player_team", 1),
           (val_add, ":number_of_players_at_team_2", 1),
         (try_end),
       (try_end),

       (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
       (assign, ":number_of_players_will_be_moved", 0),
       (try_begin),
         (try_begin),
           (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
           (le, ":difference_of_number_of_players", ":checked_value"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (assign, ":team_with_more_players", 1),
           (assign, ":team_with_less_players", 0),
         (else_try),
           (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (assign, ":team_with_more_players", 0),
           (assign, ":team_with_less_players", 1),
         (try_end),
       (try_end),
       #team balance checks are done
       (try_begin),
         (gt, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (eq, "$g_team_balance_next_round", 1), #if warning is given

           #auto team balance starts
           (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"),
             (assign, ":max_player_join_time", 0),
             (assign, ":latest_joined_player_no", -1),
             (get_max_players, ":num_players"),
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (player_get_team_no, ":player_team", ":player_no"),
               (eq, ":player_team", ":team_with_more_players"),
               (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
               (try_begin),
                 (gt, ":player_join_time", ":max_player_join_time"),
                 (assign, ":max_player_join_time", ":player_join_time"),
                 (assign, ":latest_joined_player_no", ":player_no"),
               (try_end),
             (try_end),
             (try_begin),
               (ge, ":latest_joined_player_no", 0),
               (try_begin),
                 #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                 (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"),
                 (ge, ":latest_joined_agent_id", 0),
                 (agent_is_alive, ":latest_joined_agent_id"),

                 (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                 (val_add, ":player_kill_count", 1),
                 (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                 (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                 (val_sub, ":player_death_count", 1),
                 (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                 (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                 (val_add, ":player_score", 1),
                 (player_set_score, ":latest_joined_player_no", ":player_score"),

                 (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                   (player_is_active, ":player_no"),
                   (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                 (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                 (val_add, ":player_gold", ":old_items_value"),
                 (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
               (end_try),

               (player_set_troop_id, ":latest_joined_player_no", -1),
               (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
               (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
             (try_end),
           (try_end),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------
           (get_max_players, ":num_players"),
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
           (try_end),
           (assign, "$g_team_balance_next_round", 0),
           #auto team balance done
         (else_try),
           #tutorial message (next round there will be auto team balance)
           (assign, "$g_team_balance_next_round", 1),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------
           (get_max_players, ":num_players"),
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next),
           (try_end),
         (try_end),
       (else_try),
         (assign, "$g_team_balance_next_round", 0),
       (try_end),
     (try_end),
   ]),

  #script_check_creating_ladder_dust_effect
  # INPUT: arg1 = instance_id, arg2 = remaining_time
  # OUTPUT: none
  ("check_creating_ladder_dust_effect",
   [
      (store_trigger_param_1, ":instance_id"),
      (store_trigger_param_2, ":remaining_time"),

      (try_begin),
        (lt, ":remaining_time", 15), #less then 0.15 seconds
        (gt, ":remaining_time", 3), #more than 0.03 seconds

        (scene_prop_get_slot, ":smoke_effect_done", ":instance_id", scene_prop_smoke_effect_done),
        (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

        (try_begin),
          (eq, ":smoke_effect_done", 0),
          (eq, ":opened_or_closed", 0),

          (prop_instance_get_position, pos0, ":instance_id"),

          (assign, ":smallest_dist", -1),
          (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
            (entry_point_get_position, pos1, ":entry_point_no"),
            (get_sq_distance_between_positions, ":dist", pos0, pos1),
            (this_or_next|eq, ":smallest_dist", -1),
            (lt, ":dist", ":smallest_dist"),
            (assign, ":smallest_dist", ":dist"),
            (assign, ":nearest_entry_point", ":entry_point_no"),
          (try_end),

          (try_begin),
            (set_fixed_point_multiplier, 100),

            (ge, ":smallest_dist", 0),
            (lt, ":smallest_dist", 22500), #max 15m distance

            (entry_point_get_position, pos1, ":nearest_entry_point"),
            (position_rotate_x, pos1, -90),

            (prop_instance_get_scene_prop_kind, ":scene_prop_kind", ":instance_id"),
            (try_begin),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_6m"),
              (init_position, pos2),
              (position_set_z, pos2, 300),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_6m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_6m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_8m"),
              (init_position, pos2),
              (position_set_z, pos2, 400),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_8m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_8m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_10m"),
              (init_position, pos2),
              (position_set_z, pos2, 500),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_10m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_10m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_12m"),
              (init_position, pos2),
              (position_set_z, pos2, 600),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_12m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_12m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_14m"),
              (init_position, pos2),
              (position_set_z, pos2, 700),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_14m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_14m", pos3, 100),
            (try_end),

            (scene_prop_set_slot, ":instance_id", scene_prop_smoke_effect_done, 1),
          (try_end),
        (try_end),
      (try_end),
      ]),

  #script_money_management_after_agent_death
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("money_management_after_agent_death",
   [
     (store_script_param, ":killer_agent_no", 1),
     (store_script_param, ":dead_agent_no", 2),

     (assign, ":dead_agent_player_id", -1),

     (try_begin),
       (multiplayer_is_server),
       (ge, ":killer_agent_no", 0),
       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_is_human, ":killer_agent_no"), #if killer agent is not horse
       (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
       (agent_get_team, ":dead_agent_team", ":dead_agent_no"),

       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (neq, ":killer_agent_team", ":dead_agent_team"), #if these agents are enemies

       (neq, ":dead_agent_no", ":killer_agent_no"), #if agents are different, do not remove it is needed because in deathmatch mod, self killing passes here because of this or next.

       (try_begin),
         (neg|agent_is_non_player, ":dead_agent_no"),
         (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
         (player_get_slot, ":dead_agent_equipment_value", ":dead_player_no", slot_player_total_equipment_value),
       (else_try),
         (assign, ":dead_agent_equipment_value", 0),
       (try_end),

       (assign, ":dead_agent_team_human_players_count", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),
         (player_get_team_no, ":player_team", ":player_no"),
         (eq, ":player_team", ":dead_agent_team"),
         (val_add, ":dead_agent_team_human_players_count", 1),
       (try_end),

       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),

         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
           (assign, ":one_spawn_per_round_game_type", 1),
         (else_try),
           (assign, ":one_spawn_per_round_game_type", 0),
         (try_end),

         (this_or_next|eq, ":one_spawn_per_round_game_type", 0),
         (this_or_next|player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
         (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),

         (player_get_agent_id, ":agent_no", ":player_no"),
         (try_begin),
           (eq, ":agent_no", ":dead_agent_no"), #if this agent is dead agent then get share from total loot. (20% of total equipment value)
           (player_get_gold, ":player_gold", ":player_no"),

           (assign, ":dead_agent_player_id", ":player_no"),

           #dead agent loot share (32%-48%-64%, norm : 48%)
           (store_mul, ":share_of_dead_agent", ":dead_agent_equipment_value", multi_dead_agent_loot_percentage_share),
           (val_div, ":share_of_dead_agent", 100),
           (val_mul, ":share_of_dead_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_dead_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_dead_agent", 4),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_dead_agent", 2),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_dead_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (else_try),
           (eq, ":agent_no", ":killer_agent_no"), #if this agent is killer agent then get share from total loot. (10% of total equipment value)
           (player_get_gold, ":player_gold", ":player_no"),

           #killer agent standart money (100-150-200, norm : 150)
           (assign, ":killer_agent_standard_money_addition", multi_killer_agent_standard_money_add),
           (val_mul, ":killer_agent_standard_money_addition", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":killer_agent_standard_money_addition", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":killer_agent_standard_money_addition", 4),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":killer_agent_standard_money_addition", 2),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
           (else_try),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), #(3/3x) share if current mod is siege
           (try_end),

           #killer agent loot share (8%-12%-16%, norm : 12%)
           (store_mul, ":share_of_killer_agent", ":dead_agent_equipment_value", multi_killer_agent_loot_percentage_share),
           (val_div, ":share_of_killer_agent", 100),
           (val_mul, ":share_of_killer_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_killer_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_killer_agent", 4),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_killer_agent", 2),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_killer_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),
       (try_end),
     (try_end),

     #(below lines added new at 25.11.09 after Armagan decided new money system)
     (try_begin),
       (multiplayer_is_server),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),

       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
       (ge, ":dead_agent_player_id", 0),

       (player_get_gold, ":player_gold", ":dead_agent_player_id"),
       (try_begin),
         (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
         (lt, ":player_gold", ":minimum_gold"),
         (assign, ":player_gold", ":minimum_gold"),
       (try_end),
       (player_set_gold, ":dead_agent_player_id", ":player_gold"),
     (try_end),
     #new money system addition end
     ]),

	  # INPUT: arg1 = agent_id, arg2 = instance_id
  # OUTPUT: none
  ("use_item",
   [
     (store_script_param, ":instance_id", 1),
     (store_script_param, ":user_id", 2),

     (try_begin),
       (game_in_multiplayer_mode),
       (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
       (eq, ":scene_prop_id", "spr_winch_b"),

       (multiplayer_get_my_player, ":my_player_no"),

       (this_or_next|gt, ":my_player_no", 0),
       (neg|multiplayer_is_dedicated_server),

       (ge, ":my_player_no", 0),
       (player_get_agent_id, ":my_agent_id", ":my_player_no"),
       (ge, ":my_agent_id", 0),
       (agent_is_active, ":my_agent_id"),
       (agent_get_team, ":my_team_no", ":my_agent_id"),
       (eq, ":my_team_no", 0),

       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (ge, ":user_id", 0),
       (agent_is_active, ":user_id"),
       (agent_get_player_id, ":user_player", ":user_id"),
       (str_store_player_username, s7, ":user_player"),

       (try_begin),
         (eq, ":opened_or_closed", 0),
         (display_message, "@{s7} opened the gate"),
       (else_try),
         (display_message, "@{s7} closed the gate"),
       (try_end),
     (try_end),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (assign, ":smallest_dist", -1),
     (prop_instance_get_position, pos0, ":instance_id"),
     (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
       (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions, ":dist", pos0, pos1),
       (this_or_next|eq, ":smallest_dist", -1),
       (lt, ":dist", ":smallest_dist"),
       (assign, ":smallest_dist", ":dist"),
       (assign, ":effected_object_instance_id", ":cur_instance_id"),
     (try_end),

     (try_begin),
       (ge, ":instance_id", 0),
       (ge, ":smallest_dist", 0),

       (try_begin),
         (eq, ":effected_object", "spr_portcullis"),
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0), #open gate

           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, 375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, 72000),
           (try_end),
         (else_try), #close gate
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, -375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 0),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, -72000),
           (try_end),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_6m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_8m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_10m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_12m"),
         (eq, ":effected_object", "spr_siege_ladder_move_14m"),

         (try_begin),
           (eq, ":effected_object", "spr_siege_ladder_move_6m"),
           (assign, ":animation_time_drop", 120),
           (assign, ":animation_time_elevate", 240),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_8m"),
           (assign, ":animation_time_drop", 140),
           (assign, ":animation_time_elevate", 280),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_10m"),
           (assign, ":animation_time_drop", 160),
           (assign, ":animation_time_elevate", 320),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_12m"),
           (assign, ":animation_time_drop", 190),
           (assign, ":animation_time_elevate", 360),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_14m"),
           (assign, ":animation_time_drop", 230),
           (assign, ":animation_time_elevate", 400),
         (try_end),

         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_elevate"), #3 seconds in average
           (eq, ":opened_or_closed", 0), #ladder at ground
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
           (prop_instance_enable_physics, ":effected_object_instance_id", 0),
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 300),
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try), #ladder at wall
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_drop"), #1.5 seconds in average
           (prop_instance_get_position, pos0, ":instance_id"),

           (assign, ":smallest_dist", -1),
           (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
             (entry_point_get_position, pos1, ":entry_point_no"),
             (get_sq_distance_between_positions, ":dist", pos0, pos1),
             (this_or_next|eq, ":smallest_dist", -1),
             (lt, ":dist", ":smallest_dist"),
             (assign, ":smallest_dist", ":dist"),
             (assign, ":nearest_entry_point", ":entry_point_no"),
           (try_end),

           (try_begin),
             (ge, ":smallest_dist", 0),
             (lt, ":smallest_dist", 22500), #max 15m distance
             (entry_point_get_position, pos1, ":nearest_entry_point"),
             (position_rotate_x, pos1, -90),
             (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_smoke_effect_done, 0),
             (prop_instance_enable_physics, ":effected_object_instance_id", 0),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos1, 130),
           (try_end),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_door_destructible"),
         (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
         (eq, ":scene_prop_id", "spr_castle_f_door_a"),

         (assign, ":effected_object_instance_id", ":instance_id"),
         (scene_prop_get_slot, ":opened_or_closed", ":effected_object_instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0),

           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (try_begin),
             (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
             (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),

             (position_rotate_z, pos0, -85),
           (else_try),
             (position_rotate_z, pos0, 85),
           (try_end),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try),
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (try_end),
     (try_end),
     ]),

  #script_determine_team_flags
  # INPUT: none
  # OUTPUT: none
  ("determine_team_flags",
   [
     (store_script_param, ":team_no", 1),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),

       (try_begin),
         (eq, ":team_no", 0),

         (team_get_faction, ":team_faction_no", 0),
         (try_begin),
           (eq, ":team_faction_no", "fac_kingdom_1"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_1"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_2"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_2"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_3"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_3"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_4"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_4"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_5"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_5"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_6"),
           (assign, "$team_1_flag_scene_prop", "spr_ctf_flag_kingdom_6"),
         (try_end),
       (else_try),
         (team_get_faction, ":team_faction_no", 1),
         (try_begin),
           (eq, ":team_faction_no", "fac_kingdom_1"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_1"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_2"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_2"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_3"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_3"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_4"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_4"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_5"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_5"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_6"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_6"),
         (try_end),

         (try_begin),
           (eq, "$team_1_flag_scene_prop", "$team_2_flag_scene_prop"),
           (assign, "$team_2_flag_scene_prop", "spr_ctf_flag_kingdom_7"),
         (try_end),
       (try_end),
     (else_try),
       (try_begin),
         (eq, ":team_no", 0),

         (team_get_faction, ":team_faction_no", 0),
         (try_begin),
           (eq, ":team_faction_no", "fac_kingdom_1"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_swadian"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_2"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_vaegir"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_3"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_khergit"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_4"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_nord"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_5"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_rhodok"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_6"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_sarranid"),
         (try_end),
       (else_try),
         (team_get_faction, ":team_faction_no", 1),
         (try_begin),
           (eq, ":team_faction_no", "fac_kingdom_1"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_swadian"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_2"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_vaegir"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_3"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_khergit"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_4"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_nord"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_5"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_rhodok"),
         (else_try),
           (eq, ":team_faction_no", "fac_kingdom_6"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_sarranid"),
         (try_end),

         (try_begin),
           (eq, "$team_1_flag_scene_prop", "$team_2_flag_scene_prop"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_rebel"),
         (try_end),
       (try_end),
     (try_end),
   ]),


  #script_calculate_flag_move_time
  # INPUT: arg1 = number_of_total_agents_around_flag, arg2 = dist_between_flag_and_its_pole
  # OUTPUT: reg0 = flag move time
  ("calculate_flag_move_time",
   [
     (store_script_param, ":number_of_total_agents_around_flag", 1),
     (store_script_param, ":dist_between_flag_and_its_target", 2),

     (try_begin), #(if no one is around flag it again moves to its current owner situation but 5 times slower than normal)
       (eq, ":number_of_total_agents_around_flag", 0),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 2500),#5.00 * 1.00 * (500 stable) = 2000
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 1),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 500), #1.00 * (500 stable) = 500
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 2),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 300), #0.60(0.60) * (500 stable) = 300
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 3),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 195), #0.39(0.60 * 0.65) * (500 stable) = 195
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 4),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 137), #0.273(0.60 * 0.65 * 0.70) * (500 stable) = 136.5 >rounding> 137
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 5),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 102), #0.20475(0.60 * 0.65 * 0.70 * 0.75) * (500 stable) = 102.375 >rounding> 102
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 6),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 82),  #0.1638(0.60 * 0.65 * 0.70 * 0.75 * 0.80) * (500 stable) = 81.9 >rounding> 82
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 7),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 66),  #0.13104(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85) * (500 stable) = 65.52 >rounding> 66
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 8),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 59),  #0.117936(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90) * (500 stable) = 58.968 >rounding> 59
     (else_try),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 56),  #0.1120392(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90 * 0.95) * (500 stable) = 56.0196 >rounding> 56
     (try_end),

     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":cur_player", 0, ":num_players"),
       (player_is_active, ":cur_player"),
       (val_add, ":number_of_players", 1),
     (try_end),

     (try_begin),
       (lt, ":number_of_players", 10),
       (val_mul, reg0, 50),
     (else_try),
       (lt, ":number_of_players", 35),
       (store_sub, ":number_of_players_multipication", 35, ":number_of_players"),
       (val_mul, ":number_of_players_multipication", 2),
       (store_sub, ":number_of_players_multipication", 100, ":number_of_players_multipication"),
       (val_mul, reg0, ":number_of_players_multipication"),
     (else_try),
       (val_mul, reg0, 100),
     (try_end),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (val_mul, reg0, 2),
     (try_end),

     (val_div, reg0, 10000), #100x for number of players around flag, 100x for number of players in game
     ]),

  #script_move_death_mode_flags_down
  # INPUT: none
  # OUTPUT: none
  ("move_death_mode_flags_down",
   [
     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (position_move_z, pos0, -2000),
       (prop_instance_set_position, ":pole_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (position_move_z, pos1, -2000),
       (prop_instance_set_position, ":pole_2_id", pos1),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_1_id"),
       (position_move_z, pos0, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_2_id"),
       (position_move_z, pos1, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_2_id", pos1),
     (try_end),
   ]),

  #script_move_flag
  # INPUT: arg1 = shown_flag_id, arg2 = move time in seconds, pos0 = target position
  # OUTPUT: none
  ("move_flag",
   [
     (store_script_param, ":shown_flag_id", 1),
     (store_script_param, ":shown_flag_move_time", 2),

     (try_begin),
       (multiplayer_is_server), #added after auto-animating

       (try_begin),
         (eq, ":shown_flag_move_time", 0), #stop
         (prop_instance_stop_animating, ":shown_flag_id"),
       (else_try),
         (prop_instance_animate_to_position, ":shown_flag_id", pos0, ":shown_flag_move_time"),
       (try_end),
     (try_end),
   ]),

  #script_move_headquarters_flags
  # INPUT: arg1 = current_owner, arg2 = number_of_agents_around_flag_team_1, arg3 = number_of_agents_around_flag_team_2
  # OUTPUT: none
  ("move_headquarters_flags",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":number_of_agents_around_flag_team_1", 2),
     (store_script_param, ":number_of_agents_around_flag_team_2", 3),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":current_owner", "trp_multiplayer_data", ":cur_flag_slot"),

     (scene_prop_get_num_instances, ":num_instances", "spr_headquarters_flag_gray_code_only"),
     (try_begin),
       (assign, ":visibility", 0),
       (lt, ":flag_no", ":num_instances"),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_get_visibility, ":visibility", ":flag_id"),
     (try_end),

     (try_begin),
       (eq, ":visibility", 1),
       (assign, ":shown_flag", 0),
       (assign, ":shown_flag_id", ":flag_id"),
     (else_try),
       (scene_prop_get_num_instances, ":num_instances", "$team_1_flag_scene_prop"),
       (try_begin),
         (assign, ":visibility", 0),
         (lt, ":flag_no", ":num_instances"),
         (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (scene_prop_get_visibility, ":visibility", ":flag_id"),
       (try_end),

       #(scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       #(scene_prop_get_visibility, ":visibility", ":flag_id"),
       (try_begin),
         (eq, ":visibility", 1),
         (assign, ":shown_flag", 1),
         (assign, ":shown_flag_id", ":flag_id"),
       (else_try),
         (scene_prop_get_num_instances, ":num_instances", "$team_2_flag_scene_prop"),
         (try_begin),
           (assign, ":visibility", 0),
           (lt, ":flag_no", ":num_instances"),
           (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
           (scene_prop_get_visibility, ":visibility", ":flag_id"),
         (try_end),

         #(scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         #(scene_prop_get_visibility, ":visibility", ":flag_id"),
         (try_begin),
           (eq, ":visibility", 1),
           (assign, ":shown_flag", 2),
           (assign, ":shown_flag_id", ":flag_id"),
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
     (try_end),

     (try_begin),
       (eq, ":shown_flag", ":current_owner"), #situation 1 : (current owner is equal shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),
         (assign, ":flag_movement", 0), #0:stop
       (else_try),
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", 1), #1:rise (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (eq, ":current_owner", 1),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (eq, ":current_owner", 2),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (assign, ":flag_movement", -1), #-1:drop (fast)
         (try_end),
       (try_end),
     (else_try), #situation 2 : (current owner is different than shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),
         (assign, ":flag_movement", 0), #0:stop
       (else_try),
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", -1), #-1:drop (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (try_begin),
             (eq, ":shown_flag", 1),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 1),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (try_begin),
             (eq, ":shown_flag", 2),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 2),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (try_end),
       (try_end),
     (try_end),

     (store_add, ":number_of_total_agents_around_flag", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),

     (try_begin),
       (eq, ":flag_movement", 0),
       (assign, reg0, 0),
     (else_try),
       (eq, ":flag_movement", 1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (position_move_z, pos0, multi_headquarters_pole_height),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (else_try),
       (eq, ":flag_movement", -1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (try_end),

     (call_script, "script_move_flag", ":shown_flag_id", reg0), #pos0 : target position
     ]),

  #script_set_num_agents_around_flag
  # INPUT: arg1 = flag_no, arg2 = owner_code
  # OUTPUT: none
  ("set_num_agents_around_flag",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":current_owner_code", 2),

     (store_div, ":number_of_agents_around_flag_team_1", ":current_owner_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":current_owner_code", 100),

     (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
  ]),

  #script_change_flag_owner
  # INPUT: arg1 = flag_no, arg2 = owner_code
  # OUTPUT: none
  ("change_flag_owner",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":owner_code", 2),

     (try_begin),
       (lt, ":owner_code", 0),
       (val_add, ":owner_code", 1),
       (val_mul, ":owner_code", -1),
     (try_end),

     (store_div, ":owner_team_no", ":owner_code", 100),
     (store_mod, ":shown_flag_no", ":owner_code", 100),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":older_owner_team_no", "trp_multiplayer_data", ":cur_flag_slot"),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", ":owner_team_no"),

     #senchronizing flag positions
     (try_begin),
       #(this_or_next|eq, ":initial_flags", 0), #moved after auto-animating
       (multiplayer_is_server),

       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
       (try_begin),
         (eq, ":owner_team_no", 0), #if new owner team is 0 then flags are at bottom
         (neq, ":older_owner_team_no", -1), #clients
         (assign, ":continue", 1),
         (try_begin),
           (multiplayer_is_server),
           (eq, "$g_placing_initial_flags", 1),
           (assign, ":continue", 0),
         (try_end),
         (eq, ":continue", 1),
         (prop_instance_get_position, pos0, ":pole_id"),
         (position_move_z, pos0, multi_headquarters_distance_to_change_flag),
       (else_try),
         (prop_instance_get_position, pos0, ":pole_id"), #if new owner team is not 0 then flags are at top
         (position_move_z, pos0, multi_headquarters_pole_height),
       (try_end),

       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),

       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),

       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),
     (try_end),

     #setting visibilities of flags
     (try_begin),
       (eq, ":shown_flag_no", 0),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
     (else_try),
       (eq, ":shown_flag_no", 1),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (else_try),
       (eq, ":shown_flag_no", 2),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (try_end),

     #other
     (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_get_slot, ":players_around_code", "trp_multiplayer_data", ":cur_flag_players_around_slot"),

     (store_div, ":number_of_agents_around_flag_team_1", ":players_around_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":players_around_code", 100),

     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
   ]),

  #script_move_object_to_nearest_entry_point
  # INPUT: none
  # OUTPUT: none
  ("move_object_to_nearest_entry_point",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (prop_instance_get_position, pos0, ":instance_id"),

       (assign, ":smallest_dist", -1),
       (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
         (entry_point_get_position, pos1, ":entry_point_no"),
         (get_sq_distance_between_positions, ":dist", pos0, pos1),
         (this_or_next|eq, ":smallest_dist", -1),
         (lt, ":dist", ":smallest_dist"),
         (assign, ":smallest_dist", ":dist"),
         (assign, ":nearest_entry_point", ":entry_point_no"),
       (try_end),

       (try_begin),
         (ge, ":smallest_dist", 0),
         (lt, ":smallest_dist", 22500), #max 15m distance
         (entry_point_get_position, pos1, ":nearest_entry_point"),
         (position_rotate_x, pos1, -90),
         (prop_instance_animate_to_position, ":instance_id", pos1, 1),
       (try_end),
     (try_end),
   ]),


  #script_multiplayer_server_on_agent_spawn_common
  # INPUT: none
  # OUTPUT: none
  ("move_belfries_to_their_first_entry_point",
   [
    (store_script_param, ":belfry_body_scene_prop", 1),

    (set_fixed_point_multiplier, 100),
    (scene_prop_get_num_instances, ":num_belfries", ":belfry_body_scene_prop"),

    (try_for_range, ":belfry_no", 0, ":num_belfries"),
      #belfry
      (scene_prop_get_instance, ":belfry_scene_prop_id", ":belfry_body_scene_prop", ":belfry_no"),
      (prop_instance_get_position, pos0, ":belfry_scene_prop_id"),

      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
        #belfry platform_b
        (scene_prop_get_instance, ":belfry_platform_b_scene_prop_id", "spr_belfry_platform_b", ":belfry_no"),
      (else_try),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
      (try_end),

      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),
      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_2
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_3
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),

      (store_add, ":belfry_first_entry_point_id", 11, ":belfry_no"), #belfry entry points are 110..119 and 120..129 and 130..139
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (val_add, ":belfry_first_entry_point_id", ":number_of_belfry_a"),
      (try_end),
      (val_mul, ":belfry_first_entry_point_id", 10),
      (entry_point_get_position, pos1, ":belfry_first_entry_point_id"),

      #this code block is taken from module_mission_templates.py (multiplayer_server_check_belfry_movement)
      #up down rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9),
      (position_get_distance_to_terrain, ":height_to_terrain_1", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at left part of belfry

      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, 300), #go 3.0 meters right
      (position_transform_position_to_parent, pos10, pos1, pos9),
      (position_get_distance_to_terrain, ":height_to_terrain_2", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at right part of belfry

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
      (val_mul, ":height_to_terrain", 100), #because of fixed point multiplier

      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 2 degrees. #ac sonra
      (init_position, pos20),
      (position_rotate_x_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos23, pos1, pos20),

      #right left rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_1", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_2", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
      (val_mul, ":height_to_terrain", 100), #100 is because of fixed_point_multiplier
      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 25 degrees.
      (val_mul, ":rotate_angle_of_next_entry_point", -1),

      (init_position, pos20),
      (position_rotate_y_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos22, pos23, pos20),

      (copy_position, pos1, pos22),
      #end of code block

      #belfry
      (prop_instance_stop_animating, ":belfry_scene_prop_id"),
      (prop_instance_set_position, ":belfry_scene_prop_id", pos1),

      #belfry platforms
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),

        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),

          (init_position, pos20),
          (position_rotate_x, pos20, 90),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),
        #belfry platform_b
        (prop_instance_get_position, pos6, ":belfry_platform_b_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (prop_instance_stop_animating, ":belfry_platform_b_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_b_scene_prop_id", pos8),
      (else_try),
        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),

          (init_position, pos20),
          (position_rotate_x, pos20, 50),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),
      (try_end),

      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),
      (prop_instance_get_position, pos6, ":belfry_wheel_1_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_1_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_1_scene_prop_id", pos8),
      #belfry wheel_2
      (prop_instance_get_position, pos6, ":belfry_wheel_2_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_2_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_2_scene_prop_id", pos8),
      #belfry wheel_3
      (prop_instance_get_position, pos6, ":belfry_wheel_3_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_3_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_3_scene_prop_id", pos8),
    (try_end),
    ]),

  #script_team_set_score
  # INPUT: arg1 = team_no, arg2 = score
  # OUTPUT: none
  ("team_set_score",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":score", 2),

     (team_set_score, ":team_no", ":score"),
   ]),

  #script_player_set_score
  # INPUT: arg1 = player_no, arg2 = score
  # OUTPUT: none
  ("player_set_score",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),

     (player_set_score, ":player_no", ":score"),
   ]),

  #script_player_set_kill_count
  # INPUT: arg1 = player_no, arg2 = score
  # OUTPUT: none
  ("player_set_kill_count",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),

     (player_set_kill_count, ":player_no", ":score"),
   ]),

  #script_player_set_death_count
  # INPUT: arg1 = player_no, arg2 = score
  # OUTPUT: none
  ("player_set_death_count",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),

     (player_set_death_count, ":player_no", ":score"),
   ]),

  #script_set_attached_scene_prop
  # INPUT: arg1 = agent_id, arg2 = flag_id
  # OUTPUT: none
  ("set_attached_scene_prop",
   [
     (store_script_param, ":agent_id", 1),
     (store_script_param, ":flag_id", 2),

     (try_begin), #if current mod is capture the flag and attached scene prop is flag then change flag situation of flag owner team.
       (scene_prop_get_instance, ":red_flag_id", "spr_tutorial_flag_red", 0),
       (scene_prop_get_instance, ":blue_flag_id", "spr_tutorial_flag_blue", 0),
       (assign, ":flag_owner_team", -1),
       (try_begin),
         (ge, ":red_flag_id", 0),
         (eq, ":flag_id", ":red_flag_id"),
         (assign, ":flag_owner_team", 0),
       (else_try),
         (ge, ":blue_flag_id", 0),
         (eq, ":flag_id", ":blue_flag_id"),
         (assign, ":flag_owner_team", 1),
       (try_end),
       (ge, ":flag_owner_team", 0),
       (team_set_slot, ":flag_owner_team", slot_team_flag_situation, 1), #1-stolen flag
     (try_end),

     (agent_set_attached_scene_prop, ":agent_id", ":flag_id"),
     (agent_set_attached_scene_prop_x, ":agent_id", 20),
     (agent_set_attached_scene_prop_z, ":agent_id", 50),
   ]),

  #script_set_team_flag_situation
  # INPUT: arg1 = team_no, arg2 = score
  # OUTPUT: none
  ("set_team_flag_situation",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":flag_situation", 2),

     (team_set_slot, ":team_no", slot_team_flag_situation, ":flag_situation"),
   ]),

  #script_start_death_mode
  # INPUT: none
  # OUTPUT: none
  ("start_death_mode",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_start_death_mode),
     (start_presentation, "prsnt_multiplayer_message_1"),
   ]),

  #script_calculate_new_death_waiting_time_at_death_mod
  # INPUT: none
  # OUTPUT: none
  ("calculate_new_death_waiting_time_at_death_mod",
   [
     (assign, ":num_living_players", 0), #count number of living players to find out death wait time
     (try_begin),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (val_add, ":num_living_players", 1),
       (try_end),
     (try_end),

     (val_add, ":num_living_players", multiplayer_battle_formula_value_a),
     (set_fixed_point_multiplier, 100),
     (store_mul, ":num_living_players", ":num_living_players", 100),
     (store_sqrt, ":sqrt_num_living_players", ":num_living_players"),
     (store_div, "$g_battle_waiting_seconds", multiplayer_battle_formula_value_b, ":sqrt_num_living_players"),
     (store_mission_timer_a, "$g_death_mode_part_1_start_time"),
   ]),

  #script_calculate_number_of_targets_destroyed
  # INPUT: none
  # OUTPUT: none

  ("calculate_number_of_targets_destroyed",
   [
     (assign, "$g_number_of_targets_destroyed", 0),
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),
     ]),

  #script_initialize_objects
  # INPUT: none
  # OUTPUT: reg0 = team_1_num_flags, reg1 = team_2_num_flags
  ("get_headquarters_scores",
   [
     (assign, ":team_1_num_flags", 0),
     (assign, ":team_2_num_flags", 0),
     (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
       (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
       (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
       (neq, ":cur_flag_owner", 0),
       (try_begin),
         (eq, ":cur_flag_owner", 1),
         (val_add, ":team_1_num_flags", 1),
       (else_try),
         (val_add, ":team_2_num_flags", 1),
       (try_end),
     (try_end),
     (assign, reg0, ":team_1_num_flags"),
     (assign, reg1, ":team_2_num_flags"),
     ]),


  #script_draw_this_round
  # INPUT: arg1 = value
  ("draw_this_round",
   [
    (store_script_param, ":value", 1),
    (try_begin),
      (eq, ":value", -9), #destroy mod round end
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      #(assign, "$g_multiplayer_message_value_1", -1),
      #(assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      #(start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", -1), #draw
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      (assign, "$g_multiplayer_message_value_1", -1),
      (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", 0), #defender wins
      #THIS_IS_OUR_LAND achievement
      (try_begin),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
        (multiplayer_get_my_player, ":my_player_no"),
        (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
        (player_get_agent_id, ":my_player_agent", ":my_player_no"),
        (ge, ":my_player_agent", 0),
        (agent_is_alive, ":my_player_agent"),
        (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
        (eq, ":my_player_agent_team_no", 0), #defender
        (unlock_achievement, ACHIEVEMENT_THIS_IS_OUR_LAND),
      (try_end),
      #THIS_IS_OUR_LAND achievement end
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),

      (team_get_faction, ":faction_of_winner_team", 0),
      (team_get_score, ":team_1_score", 0),
      (val_add, ":team_1_score", 1),
      (team_set_score, 0, ":team_1_score"),
      (assign, "$g_winner_team", 0),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
      (else_try),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", 1), #attacker wins
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),

      (team_get_faction, ":faction_of_winner_team", 1),
      (team_get_score, ":team_2_score", 1),
      (val_add, ":team_2_score", 1),
      (team_set_score, 1, ":team_2_score"),
      (assign, "$g_winner_team", 1),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_siege_mode),
      (else_try),
        (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    #LAST_MAN_STANDING achievement
    (try_begin),
      (is_between, ":value", 0, 2), #defender or attacker wins
      (try_begin),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (multiplayer_get_my_player, ":my_player_no"),
        (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
        (player_get_agent_id, ":my_player_agent", ":my_player_no"),
        (ge, ":my_player_agent", 0),
        (agent_is_alive, ":my_player_agent"),
        (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
        (eq, ":my_player_agent_team_no", ":value"), #winner team
        (unlock_achievement, ACHIEVEMENT_LAST_MAN_STANDING),
      (try_end),
    (try_end),
    #LAST_MAN_STANDING achievement end
    ]),

  #script_check_achievement_last_man_standing
  #INPUT: arg1 = value
  ("check_achievement_last_man_standing",
   [
   #LAST_MAN_STANDING achievement
	  (try_begin),
	    (store_script_param, ":value", 1),
		(is_between, ":value", 0, 2), #defender or attacker wins
	    (try_begin),
		  (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
		  (multiplayer_get_my_player, ":my_player_no"),
		  (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
		  (player_get_agent_id, ":my_player_agent", ":my_player_no"),
		  (ge, ":my_player_agent", 0),
		  (agent_is_alive, ":my_player_agent"),
		  (agent_get_team, ":my_player_agent_team_no", ":my_player_agent"),
		  (eq, ":my_player_agent_team_no", ":value"), #winner team
		  (unlock_achievement, ACHIEVEMENT_LAST_MAN_STANDING),
		(try_end),
	  (try_end),
    #LAST_MAN_STANDING achievement end
    ]),

  #script_find_most_suitable_bot_to_control
  # INPUT: arg1 = value
  ("find_most_suitable_bot_to_control",
   [
      (set_fixed_point_multiplier, 100),
      (store_script_param, ":player_no", 1),
      (player_get_team_no, ":player_team", ":player_no"),

      (player_get_slot, ":x_coor", ":player_no", slot_player_death_pos_x),
      (player_get_slot, ":y_coor", ":player_no", slot_player_death_pos_y),
      (player_get_slot, ":z_coor", ":player_no", slot_player_death_pos_z),

      (init_position, pos0),
      (position_set_x, pos0, ":x_coor"),
      (position_set_y, pos0, ":y_coor"),
      (position_set_z, pos0, ":z_coor"),

      (assign, ":most_suitable_bot", -1),
      (assign, ":max_bot_score", -1),

      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_non_player, ":cur_agent"),
        (agent_get_team ,":cur_team", ":cur_agent"),
        (eq, ":cur_team", ":player_team"),
        (agent_get_position, pos1, ":cur_agent"),

        #getting score for distance of agent to death point (0..3000)
        (get_distance_between_positions_in_meters, ":dist", pos0, pos1),

        (try_begin),
          (lt, ":dist", 500),
          (store_sub, ":bot_score", 500, ":dist"),
        (else_try),
          (assign, ":bot_score", 0),
        (try_end),
        (val_mul, ":bot_score", 6),

        #getting score for distance of agent to enemy & friend agents (0..300 x agents)
        (try_for_agents, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (neq, ":cur_agent", ":cur_agent_2"),
          (agent_get_team ,":cur_team_2", ":cur_agent_2"),
          (try_begin),
            (neq, ":cur_team_2", ":player_team"),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":enemy_near_score", ":dist_2"),
            (else_try),
              (assign, ":enemy_near_score", 300),
            (try_end),
            (val_add, ":bot_score", ":enemy_near_score"),
          (else_try),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":friend_near_score", 300, ":dist_2"),
            (else_try),
              (assign, ":friend_near_score", 0),
            (try_end),
            (val_add, ":bot_score", ":friend_near_score"),
          (try_end),
        (try_end),

        #getting score for health (0..200)
        (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        (val_mul, ":agent_hit_points", 2),
        (val_add, ":bot_score", ":agent_hit_points"),

        (ge, ":bot_score", ":max_bot_score"),
        (assign, ":max_bot_score", ":bot_score"),
        (assign, ":most_suitable_bot", ":cur_agent"),
      (try_end),

      (assign, reg0, ":most_suitable_bot"),
    ]),

  #script_game_receive_url_response
  # Input: none
  # Output: reg0 = 100xconstant (100..500)
  ("find_number_of_agents_constant",
   [
     (assign, ":num_dead_or_alive_agents", 0),

     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (val_add, ":num_dead_or_alive_agents", 1),
     (try_end),

     (try_begin),
       (le, ":num_dead_or_alive_agents", 2), #2
       (assign, reg0, 100),
     (else_try),
       (le, ":num_dead_or_alive_agents", 4), #2+2
       (assign, reg0, 140),
     (else_try),
       (le, ":num_dead_or_alive_agents", 7), #2+2+3
       (assign, reg0, 180),
     (else_try),
       (le, ":num_dead_or_alive_agents", 11), #2+2+3+4
       (assign, reg0, 220),
     (else_try),
       (le, ":num_dead_or_alive_agents", 17), #2+2+3+4+6
       (assign, reg0, 260),
     (else_try),
       (le, ":num_dead_or_alive_agents", 25), #2+2+3+4+6+8
       (assign, reg0, 300),
     (else_try),
       (le, ":num_dead_or_alive_agents", 36), #2+2+3+4+6+8+11
       (assign, reg0, 340),
     (else_try),
       (le, ":num_dead_or_alive_agents", 50), #2+2+3+4+6+8+11+14
       (assign, reg0, 380),
     (else_try),
       (le, ":num_dead_or_alive_agents", 68), #2+2+3+4+6+8+11+14+18
       (assign, reg0, 420),
     (else_try),
       (le, ":num_dead_or_alive_agents", 91), #2+2+3+4+6+8+11+14+18+23
       (assign, reg0, 460),
     (else_try),
       (assign, reg0, 500),
     (try_end),
     ]),

  # script_game_multiplayer_event_duel_offered
  # Input: arg1 = mission_object_id
  # Output: none
  ("send_open_close_information_of_object",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":scene_prop_no", 2),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (try_begin),
         (eq, ":opened_or_closed", 1),
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_scene_prop_open_or_close, ":instance_id"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_send_initial_information
  # Input: arg1 = party_no
  # Output: reg0: ideal size
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


  #script_game_get_party_prisoner_limit:
  # INPUT: $g_talk_troop, $g_talk_troop_relation
  ("setup_talk_info",
    [
      # ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      # (try_begin),
         # (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
         # (assign, "$character_gender", tf_female),
      # (else_try),
         # (assign, "$character_gender", tf_male),
      # (try_end),
      # ##diplomacy end+
      #SB : redo order
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      # (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      # (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, "@{!} {s61}"),
      (talk_info_set_line, 1, "str_relation_reg1"),
      (call_script, "script_describe_relation_to_s63", "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ]),

#NPC companion changes begin

  #script_update_party_creation_random_limits
  # INPUT: none
  ("update_party_creation_random_limits",
    [
      (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
  ]),

  #script_set_trade_route_between_centers
  # INPUT:
  # param1: center_no
  # param2: item_id
  # param3: production_rate (should be between -100 (for net consumption) and 100 (for net production)
  # param4: randomness (between 0-100)
  #("center_change_trade_good_production",
  #  [
#	  (display_message, "@CHANGING"),
#      (store_script_param, ":center_no", 1),
#      (store_script_param, ":item_no", 2),
#      (store_script_param, ":production_rate", 3),
#      (store_script_param, ":randomness", 4),
#      (store_random_in_range, ":random_num", 0, ":randomness"),
#      (store_random_in_range, ":random_sign", 0, 2),
#      (try_begin),
#        (eq, ":random_sign", 0),
#        (val_add, ":production_rate", ":random_num"),
#      (else_try),
#        (val_sub, ":production_rate", ":random_num"),
#      (try_end),
#      (val_sub, ":item_no", trade_goods_begin),
#      (val_add, ":item_no", slot_town_trade_good_productions_begin),
#
#      (party_get_slot, ":old_production_rate", ":center_no", ":item_no"),
#      (val_add, ":production_rate", ":old_production_rate"),
#      (party_set_slot, ":center_no", ":item_no", ":production_rate"),
#  ]),




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



  #script_average_trade_good_productions
  # INPUT: arg1 = party_no
  #Called once every 72 hours
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

    # INPUT: arg1 = item_no
  # Output: reg0: production string
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

  #script_do_merchant_town_trade
  # INPUT:
  # param1: Party-id
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




  #script_party_calculate_strength:
  # INPUT: arg1 = party_id, arg2 = exclude leader
  # OUTPUT: reg0 = strength

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


  #script_loot_player_items:
  # INPUT: arg1 = enemy_party_no
  # Output: none
  ("loot_player_items",
    [
      (store_script_param, ":enemy_party_no", 1),
	  ##diplomacy start+ some enemy lords will not loot the personal equipment of a player who surrendered
	  (assign, ":save_reg0", reg0),
	  (assign, ":extra_gold", 0),
	  #I am not sure if this is historical or not, but it gives the player a reason to
	  #surrender (rather than fight to the end) even before permanent attribute loss is
	  #a possibility (or even if it is disabled outright).
	  #
	  #This also adds another layer of interaction, and makes different lords feel
	  #different from each other.
	  #
	  #Other changes:
	  # Enemy lords will receive gold they loot from the player,
	  # Books will not be looted from the player (it turns out a bug was responsible for this being possible)
	  # The enemy leader's looting skill will affect the amount of gold lootable.
	  (assign, ":merciful", 0),
	  (assign, ":party_leader", -1),
	  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
	  (try_begin),
 	    (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
	    #Possibility the player's personal equipment will be untouched if he surrendered
  	    (ge, "$g_player_surrenders", 1),
   	    (gt, ":enemy_party_no", 0),
		(party_stack_get_troop_id, ":party_leader", ":enemy_party_no", 0),
	   #(party_slot_eq, ":enemy_party_no", slot_party_type, spt_kingdom_hero_party),
		(ge, ":party_leader", walkers_end),
		(troop_is_hero, ":party_leader"),
		(call_script, "script_troop_get_player_relation", ":party_leader"),
		(assign, ":relation", reg0),
		(assign, ":probability_modifier", 0),
		(try_begin),
			#Upstanding lords are inclined to honor deals in general, and will automatically
			#do so with honorable lords they do not extremely dislike.  However, this does not
			#extend to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
			(val_max, ":probability_modifier", 10),#set to +10 unless already higher
			#They will automatically honor deals with the honorable, if they do not
			#excessively dislike them.
			(ge, "$player_honor", 1),
			(val_add, reg0, 10),
			(val_clamp, reg0, 11, 21),
			(val_max, ":probability_modifier", reg0),#set somewhere from +11 to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Martial lords are inclined to honor deals with lords who likewise follow the rules of war,
			#and will do so as long as they are neutral or friendly towards them.  This does not extend
			#to commoners.
			(troop_slot_ge, "trp_player", slot_troop_banner_scene_prop, 1),# the player has a coat of arms
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
			(ge, "$player_honor", 1),
			(assign, reg0, "$player_honor"),
			(val_clamp, reg0, 1, 6),
			(val_max, ":probability_modifier", reg0),#set somewhere from +1 to +5 unless already higher
			(ge, ":relation", 0),
			(assign, ":merciful", 1),
		(else_try),
			#Good-natured lords are inclined to honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			#This also goes for Moralist ladies if they someone end up accepting your surrender.
			(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
			(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
			(val_max, ":probability_modifier", 21),#set to +20 unless already higher
			(ge, ":relation", -10),
			(assign, ":merciful", 1),
		(else_try),
			#Honest lords are inclined honor deals with everyone, commoner or not.
			#They will do so automatically unless they particularly dislike someone.
			(call_script, "script_dplmc_get_troop_morality_value", ":party_leader", tmt_honest),
			(assign, ":honest_val", reg0),
			(ge, ":honest_val", 1),
			(store_add, reg0, ":honest_val", 14),
			(val_max, ":probability_modifier", reg0),#set to (14 + honesty ) unless already higher
			(ge, "$player_honor", 1),
			(val_mul, reg0, -1),
			(ge, ":relation", reg0),
			(assign, ":merciful", 1),
		(else_try),
			(try_begin),
				#Penalty instead of bonus for vicious lord personalities, unless they are
				#explicitly set as honest.  (None are by default.)
				(lt, ":honest_val", 1),#Must either be negative or not given
				(this_or_next|lt, ":honest_val", 0),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
				(this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
				(troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
				(val_min, ":probability_modifier", -10),#set to -10 unless already lower
			(try_end),
			#Now store into reg0 the percent chance of mercy
			(try_begin),
				(le, ":reduce_campaign_ai", 0),#Hard: base chance 25% + relation
				(store_add, reg0, ":relation", 25),
			(else_try),
				(eq, ":reduce_campaign_ai", 1),#Medium: base chance 50% + relation
				(store_add, reg0, ":relation", 50),
			(else_try),
				(ge, ":reduce_campaign_ai", 2),#Easy: base chance 75% + relation
				(store_add, reg0, ":relation", 75),
			(try_end),
			(val_add, reg0, ":probability_modifier"),#modify the chance based on the captor's personality
			(val_max, reg0, ":probability_modifier"),#at least this much of a chance
			(val_max, reg0, 5),#at least a 5% chance
			(store_random_in_range, ":probability_modifier", 1, 101),
			(lt, reg0, ":probability_modifier"),
			(assign, ":merciful", 1),
		(try_end),
	  (else_try),
  	   (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#only use this if it is explicitly enabled
		#Surrendered to a non-hero party
		(gt, ":enemy_party_no", 0),
		(ge, "$g_player_surrenders", 1),
		(store_random_in_range, reg0, 1, 101),
		(this_or_next|lt, reg0, 25),#Hard: 25% chance
			(ge, ":reduce_campaign_ai", 1),
		(this_or_next|lt, reg0, 50),#Medium: 50% chance
			(ge, ":reduce_campaign_ai", 2),
		(lt, reg0, 75),#Easy: 75% chance
		(assign, ":merciful", 1),
	  (try_end),
	  (try_begin),
		(ge, "$cheat_mode", 1),
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#don't display when nonapplicable
		(assign, ":save_reg1", reg1),
		(assign, reg0, "$g_player_surrenders"),
		(assign, reg1, ":merciful"),
		(display_message, "@{!} DEBUG loot_player_items: g_player_surrenders = {reg0}, merciful = {reg1}"),
        (assign, reg1, ":save_reg1"),
	  (try_end),
	  ##diplomacy end+
      (troop_get_inventory_capacity, ":inv_cap", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
        (ge, ":item_id", 0),
		##diplomacy start+ looting changes
		(neg|is_between, ":item_id", books_begin, books_end),#shouldn't be necessary, but just in case
		(assign, ":randomness", 0),#properly initialize variables
		##diplomacy end+
        (troop_get_inventory_slot_modifier, ":item_modifier", "trp_player", ":i_slot"),
        (try_begin),
          (is_between, ":item_id", trade_goods_begin, trade_goods_end),
          (assign, ":randomness", 20),
        (else_try),
          (this_or_next|is_between, ":item_id", horses_begin, horses_end),
          (this_or_next|eq, ":item_id", "itm_warhorse_sarranid"),
          (eq, ":item_id", "itm_warhorse_steppe"),
          (assign, ":randomness", 15),
        (else_try),
          (this_or_next|is_between, ":item_id", weapons_begin, weapons_end),
          (is_between, ":item_id", ranged_weapons_begin, ranged_weapons_end),
          (assign, ":randomness", 5),
        (else_try),
          (this_or_next|is_between, ":item_id", armors_begin, armors_end),
		  (this_or_next|eq, ":item_id", "itm_plate_boots"), #added to the end because of not breaking the save games
          (is_between, ":item_id", shields_begin, shields_end),
          (assign, ":randomness", 5),
        (try_end),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":randomness"),
		##diplomacy start+ changes
		(try_begin),
			#If this option is enabled, personal items may be spared, and instead
			#sligthly more gold is taken (but not as much as the thing's worth).
			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
			(ge, ":merciful", 1),
			(is_between, ":i_slot", ek_item_0, dplmc_ek_alt_items_end),
			(assign, ":random_no", 101),
			#(store_item_value, reg0, ":item_id"),#don't bother with imods #don't bother with the rest of this
			#(val_div, reg0, 2),
			#(ge, reg0, 1),
			#(val_add, ":extra_gold", reg0),##disable, as it defeats the point!
		(try_end),
		(lt, ":random_no", ":randomness"),
		##diplomacy end+
        (troop_remove_item, "trp_player", ":item_id"),

        (try_begin),
          (gt, ":enemy_party_no", 0),
          (party_get_slot, ":cur_loot_slot", ":enemy_party_no", slot_party_next_looted_item_slot),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_id"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1),
          (val_add, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (party_set_slot, ":enemy_party_no", ":cur_loot_slot", ":item_modifier"),
          (val_sub, ":cur_loot_slot", slot_party_looted_item_1_modifier),
          (val_add, ":cur_loot_slot", 1),
          (val_mod, ":cur_loot_slot", num_party_loot_slots),
          (party_set_slot, ":enemy_party_no", slot_party_next_looted_item_slot, ":cur_loot_slot"),
        (try_end),
      (try_end),
      (store_troop_gold, ":cur_gold", "trp_player"),
      (store_div, ":max_lost", ":cur_gold", 5),
      (store_div, ":min_lost", ":cur_gold", 10),
      (store_random_in_range, ":lost_gold", ":min_lost", ":max_lost"),
	  ##diplomacy start+
	  (try_begin),
		#This does nothing unless the option is enabled.
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		#add extra gold from enemy's looting skill
		(gt, ":enemy_party_no", 0),
		(party_get_skill_level, reg0, ":enemy_party_no", "skl_looting"),
		(val_clamp, reg0, 0, 11),#allow range +0 to +10
		(val_add, reg0, 10),
		(val_mul, ":lost_gold", reg0),
		(val_div, ":lost_gold", 10),
		#Add any gold from items not looted.
		(val_add, ":lost_gold", ":extra_gold"),
		#gold looted can't exceed player's actual gold
		(val_min, ":lost_gold", ":cur_gold"),
		(val_max, ":lost_gold", 0),
      (try_end),
	  #diplomacy end+
      (troop_remove_gold, "trp_player", ":lost_gold"),
	  ##diplomacy start+
	  (try_begin),
	    #add looted gold to the enemy, if he's a valid hero
		(is_between, ":party_leader", heroes_begin, heroes_end),
		(troop_is_hero, ":party_leader"),
		(neq, ":party_leader", "trp_player"),
		(neq, ":party_leader", "trp_kingdom_heroes_including_player_begin"),
		(ge, ":lost_gold", 1),
		#(call_script, "script_troop_add_gold", ":party_leader", ":lost_gold"),#add looted gold to enemy
		(troop_get_slot, reg0, ":party_leader", slot_troop_wealth),
		(val_add, reg0, ":lost_gold"),
		(val_max, reg0, 0),
		(troop_set_slot, ":party_leader", slot_troop_wealth, reg0),#add looted gold to enemy
	  (try_end),
	  (assign, reg0, ":save_reg0"),#revert register
	  ##diplomacy end+
      ]),


  #script_party_calculate_loot:
  # INPUT:
  # param1: Party-id
  # Returns num looted items in reg0
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

  #script_calculate_main_party_shares:
  # INPUT:
  # Returns number of player party shares in reg0
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

  #script_party_give_xp_and_gold:
  # INPUT:
  # param1: destroyed Party-id
  # calculates and gives player paty's share of gold and xp.

  ("party_give_xp_and_gold",
    [
      (store_script_param_1, ":enemy_party"), #Party_id

      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),

      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks",":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":enemy_party",":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size",":enemy_party",":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),

      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),

      (val_min, ":total_gain", 40000), #eliminate negative results

      (assign, ":player_party_xp_gain", ":total_gain"),

      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),

      (party_add_xp, "p_main_party", ":player_party_xp_gain"),

      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),

      #add gold now
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),
  ]),


  #script_setup_troop_meeting:
  # INPUT:
  # param1: troop_id with which meeting will be made.
  # param2: troop_dna (optional)

  ("setup_troop_meeting",
    [
      (store_script_param_1, ":meeting_troop"),
      (store_script_param_2, ":troop_dna"),
      (call_script, "script_get_meeting_scene"),
      (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),
      (reset_visitors),
      (set_visitor,0,"trp_player"),
	  (try_begin),
		(gt, ":troop_dna", -1),
        (troop_set_slot, "trp_temp_array_c", 17, ":troop_dna"),
        (set_visitor,17,":meeting_troop",":troop_dna"),
	  (else_try),
        (set_visitor,17,":meeting_troop"),
	  (try_end),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),

  #script_setup_party_meeting:
  # INPUT:
  # param1: Party-id with which meeting will be made.

  ("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      (party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
      (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (set_visitor,17,":meeting_troop",":troop_dna"),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ]),

  #script_get_meeting_scene:
  # INPUT: none
  # OUTPUT: reg0 contain suitable scene_no

  ("get_meeting_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_random_scene"),
      (try_begin),
        (eq, ":terrain_type", rt_steppe),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_plain),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_meeting_scene_desert"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water),
        (assign, ":scene_to_use", "scn_sea_boarding_a_a"),

        (party_get_slot, ":ship_type", "$g_encountered_party", slot_party_ship_type),
        (try_begin),
          (eq, ":ship_type", 1),
          (assign, ":scene_to_use", "scn_sea_boarding_a_a"),
        (else_try),
          (eq, ":ship_type", 2),
          (assign, ":scene_to_use", "scn_sea_boarding_b_b"),
        (else_try),
          (eq, ":ship_type", 3),
          (assign, ":scene_to_use", "scn_sea_boarding_c_c"),
        (else_try),
          (eq, ":ship_type", 4),
          (assign, ":scene_to_use", "scn_sea_boarding_d_d"),
        (try_end),

      (else_try),
        (assign, ":scene_to_use", "scn_meeting_scene_plain"),
      (try_end),
      (assign, reg0, ":scene_to_use"),
  ]),

  #script_party_remove_all_companions:
  # INPUT:
  # param1: Party-id from which  prisoners will be removed.
  # "$g_move_heroes" : controls if heroes will also be removed.

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

  #script_party_add_party_companions:
  # INPUT:
  # param1: Party-id to add the second party
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

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

  #script_party_prisoners_add_party_companions:
  # INPUT:
  # param1: Party-id to add the second part
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

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

  # script_party_add_party:
  # INPUT:
  # param1: Party-id to add the second part
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

  ("party_add_party",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (call_script, "script_party_add_party_companions",          ":target_party", ":source_party"),
      (call_script, "script_party_prisoners_add_party_prisoners", ":target_party", ":source_party"),
  ]),


  #script_party_copy:
  # INPUT:
  # param1: Party-id to copy the second party
  # param2: Party-id which will be copied to the first one.

  ("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ]),


  #script_clear_party_group:
  # INPUT:
  # param1: Party-id of the root of the group.
  # This script will clear the root party and all parties attached to it recursively.

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


  #script_party_add_wounded_members_as_prisoners:
  # INPUT:
  # param1: Party-id to add the second party
  # param2: Party-id which will be added to the first one.
  # "$g_move_heroes" : controls if heroes will also be added.

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


  #script_get_nonempty_party_in_group:
  # INPUT:
  # param1: Party-id of the root of the group.
  # OUTPUT: reg0: nonempy party-id

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

  #script_collect_prisoners_from_empty_parties:
  # INPUT:
  # param1: Party-id of the root of the group.
  # param2: Party to collect prisoners in.
  # make sure collection party is cleared before calling this.

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

  #script_change_party_morale:
  # INPUT: party_no, morale_gained
  # OUTPUT: none

  ("change_party_morale",
   [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":morale_dif"),

      (party_get_morale, ":cur_morale", ":party_no"),
      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),
      (party_set_morale, ":party_no", ":new_morale"),
      (str_store_party_name, s1, ":party_no"),

      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
      (try_end),
  ]),

  #script_count_casualties_and_adjust_morale:
  # INPUT:
  # param1: Party_id, param2: 0 = use new line, 1 = use comma

  #OUTPUT:
  # string register 0.

  ("print_casualties_to_s0",
    [(store_script_param, ":party_no", 1),
     (store_script_param, ":use_comma", 2),
     (str_clear, s0),
     (assign, ":total_reported", 0),
     (assign, ":total_wounded", 0),
     (assign, ":total_killed", 0),
     (assign, ":total_routed", 0),
     (party_get_num_companion_stacks, ":num_stacks",":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop_id", ":party_no", ":i_stack"),
       (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
       (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":i_stack"),
       #get number of routed agent numbers
       (try_begin),
         (this_or_next|eq, ":party_no", "p_main_party"),
         (eq, ":party_no", "p_player_casualties"),
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_player_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
       (else_try),
         (party_get_attached_to, ":attached_to", ":party_no"),
         (this_or_next|eq, ":party_no", "p_ally_casualties"),
         (ge, ":attached_to", 0),
         (this_or_next|eq, ":party_no", "p_ally_casualties"),
         (eq, ":attached_to", "p_main_party"),
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_ally_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
       (else_try),
         (troop_get_slot, ":num_routed", ":stack_troop_id", slot_troop_enemy_routed_agents),
         (troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
       (try_end),
       (store_sub, ":num_killed", ":stack_size", ":num_wounded"),
       (val_sub, ":num_killed", ":num_routed"),
       (val_add, ":total_killed", ":num_killed"),
       (val_add, ":total_wounded", ":num_wounded"),
       (val_add, ":total_routed", ":num_routed"),
       (try_begin),
         (this_or_next|gt, ":num_killed", 0),
         (this_or_next|gt, ":num_wounded", 0),
         (gt, ":num_routed", 0),
         (store_add, reg3, ":num_killed", ":num_wounded"),
         (store_add, reg3, reg3, ":num_routed"),
         (str_store_troop_name_by_count, s1, ":stack_troop_id", reg3),
         (try_begin),
           (troop_is_hero, ":stack_troop_id"),
           (assign, reg3, 0),
         (try_end),
         (try_begin), #there are people who killed, wounded and routed.
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (assign, reg6, ":num_routed"),
           (str_store_string, s2, "str_reg4_killed_reg5_wounded_reg6_routed"),
         (else_try), #there are people who killed and routed.
           (gt, ":num_killed", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "str_reg4_killed_reg5_routed"),
         (else_try), #there are people who killed and wounded.
           (gt, ":num_killed", 0),
           (gt, ":num_wounded", 0),
           (assign, reg4, ":num_killed"),
           (assign, reg5, ":num_wounded"),
           (str_store_string, s2, "str_reg4_killed_reg5_wounded"),
         (else_try), #there are people who wounded and routed.
           (gt, ":num_wounded", 0),
           (gt, ":num_routed", 0),
           (assign, reg4, ":num_wounded"),
           (assign, reg5, ":num_routed"),
           (str_store_string, s2, "str_reg4_wounded_reg5_routed"),
         (else_try), #there are people who only killed.
           (gt, ":num_killed", 0),
           (assign, reg1, ":num_killed"),
           (str_store_string, s3, "@killed"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (else_try), #there are people who only wounded.
           (gt, ":num_wounded", 0),
           (assign, reg1, ":num_wounded"),
           (str_store_string, s3, "@wounded"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (else_try), #there are people who only routed.
           (assign, reg1, ":num_routed"),
           (str_store_string, s3, "str_routed"),
           (str_store_string, s2, "str_reg1_blank_s3"),
         (try_end),
         (try_begin),
           (eq, ":use_comma", 1),
           (try_begin),
             (eq, ":total_reported", 0),
             (str_store_string, s0, "@{!}{reg3?{reg3}:} {s1} ({s2})"),
           (else_try),
             (str_store_string, s0, "@{!}{s0}, {reg3?{reg3}:} {s1} ({s2})"),
           (try_end),
         (else_try),
           (str_store_string, s0, "@{!}{s0}^{reg3?{reg3}:} {s1} ({s2})"),
         (try_end),
         (val_add, ":total_reported", 1),
       (try_end),
     (try_end),
     (try_begin),
       (this_or_next|gt, ":total_killed", 0),
       (this_or_next|gt, ":total_wounded", 0),
       (gt, ":total_routed", 0),
       (store_add, ":total_agents", ":total_killed", ":total_wounded"),
       (val_add, ":total_agents", ":total_routed"),
       (assign, reg3, ":total_agents"),
       (try_begin),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (assign, reg6, ":total_routed"),
         (str_store_string, s2, "str_reg4_killed_reg5_wounded_reg6_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "str_reg4_killed_reg5_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (gt, ":total_wounded", 0),
         (assign, reg4, ":total_killed"),
         (assign, reg5, ":total_wounded"),
         (str_store_string, s2, "str_reg4_killed_reg5_wounded"),
       (else_try),
         (gt, ":total_wounded", 0),
         (gt, ":total_routed", 0),
         (assign, reg4, ":total_wounded"),
         (assign, reg5, ":total_routed"),
         (str_store_string, s2, "str_reg4_wounded_reg5_routed"),
       (else_try),
         (gt, ":total_killed", 0),
         (str_store_string, s2, "@killed"),
       (else_try),
         (gt, ":total_wounded", 0),
         (str_store_string, s2, "@wounded"),
       (else_try),
         (str_store_string, s2, "str_routed"),
       (else_try),
       (try_end),
       (str_store_string, s0, "@{s0}^TOTAL: {reg3} ({s2})"),
     (else_try),
       (try_begin),
         (eq, ":use_comma", 1),
         (str_store_string, s0, "@None"),
       (else_try),
         (str_store_string, s0, "@^None"),
       (try_end),
     (try_end),
  ]),

  #script_write_fit_party_members_to_stack_selection
  # INPUT:
  # param1: party_no, exclude_leader
  #OUTPUT:
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
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

  #script_remove_fit_party_member_from_stack_selection
  # INPUT:
  # param1: slot_index
  #OUTPUT:
  # reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
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

  #script_remove_random_fit_party_member_from_stack_selection
  # INPUT:
  # none
  #OUTPUT:
  # reg0 = troop_no
  # trp_stack_selection_amounts slots (slot 0 = number of stacks, 1 = number of men fit, 2..n = stack sizes (fit))
  # trp_stack_selection_ids slots (2..n = stack troops)
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


  #script_add_routed_party
  #INPUT: none
  #OUTPUT: none
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
    ]), #ozan
  # INPUT: none
  # OUTPUT: reg0 = weapon_1, reg1 = weapon_2
  ("get_random_melee_training_weapon",
   [
     (assign, ":weapon_1", -1),
     (assign, ":weapon_2", -1),
     (store_random_in_range, ":random_no", 0, 3),
     (try_begin),
       (eq, ":random_no", 0),
       (assign, ":weapon_1", "itm_practice_staff"),
     (else_try),
       (eq, ":random_no", 1),
       (assign, ":weapon_1", "itm_practice_sword"),
       (assign, ":weapon_2", "itm_practice_shield"),
     (else_try),
       (assign, ":weapon_1", "itm_heavy_practice_sword"),
     (try_end),
     (assign, reg0, ":weapon_1"),
     (assign, reg1, ":weapon_2"),
     ]),

  #script_start_training_at_training_ground
  # INPUT:
  # param1: Party-id

  #OUTPUT:
  # string register 0.

  ##  ("print_party_to_s0",
  ##    [
  ##      (store_script_param_1, ":party"), #Party_id
  ##      (party_get_num_companion_stacks, ":num_stacks",":party"),
  ##      (str_store_string, s50, "str_dplmc_none"),
  ##      (try_for_range, ":i_stack", 0, ":num_stacks"),
  ##        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
  ##        (party_stack_get_size,         ":stack_size",":party",":i_stack"),
  ##        (str_store_troop_name_by_count, s61, ":stack_troop", ":stack_size"),
  ##        (try_begin),
  ##          (troop_is_hero, ":stack_troop"),
  ##          (str_store_string_reg, s51, s61),
  ##        (else_try),
  ##          (assign, reg60, ":stack_size"),
  ##          (str_store_string, s63, "str_reg60_s61"),
  ##        (try_end),
  ##        (try_begin),
  ##          (eq, ":i_stack", 0),
  ##          (str_store_string_reg, s50, s51),
  ##        (else_try),
  ##          (str_store_string, s50, "str_s50_comma_s51"),
  ##        (try_end),
  ##      (try_end),
  ##      (str_store_string_reg, s0, s50),
  ##  ]),



  #script_party_count_fit_regulars:
  # Returns the number of unwounded regular companions in a party
  # INPUT:
  # param1: Party-id

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


  #script_party_count_fit_for_battle:
  # Returns the number of unwounded companions in a party
  # INPUT:
  # param1: Party-id
  # OUTPUT: reg0 = result
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


  #script_party_count_members_with_full_health
  # Returns the number of unwounded regulars, and heroes other than player with 100% hitpoints in a party
  # INPUT:
  # param1: Party-id
  # OUTPUT: reg0 = result
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


  ##  ("get_fit_stack_with_rank",
  ##    [
  ##      (store_script_param_1, ":party"), #Party_id
  ##      (store_script_param_2, ":rank"), #Rank
  ##      (party_get_num_companion_stacks, ":num_stacks",":party"),
  ##      (assign, reg0, -1),
  ##      (assign, ":num_total", 0),
  ##      (try_for_range, ":i_stack", 0, ":num_stacks"),
  ##        (eq, reg(0), -1), #continue only if we haven't found the result yet.
  ##        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
  ##        (assign, ":num_fit",0),
  ##        (try_begin),
  ##          (troop_is_hero, ":stack_troop"),
  ##          (store_troop_health, ":troop_hp", ":stack_troop"),
  ##          (try_begin),
  ##            (ge,  ":troop_hp", 20),
  ##            (assign, ":num_fit",1),
  ##          (try_end),
  ##        (else_try),
  ##          (party_stack_get_size,         ":num_fit",":party",":i_stack"),
  ##          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
  ##          (val_sub, ":num_fit", ":num_wounded"),
  ##        (try_end),
  ##        (val_add, ":num_total", ":num_fit"),
  ##        (try_begin),
  ##          (lt, ":rank", ":num_total"),
  ##          (assign, reg(0), ":i_stack"),
  ##        (try_end),
  ##      (try_end),
  ##  ]),

  #script_get_stack_with_rank:
  # Returns the stack no, containing unwounded regular companions with rank rank.
  # INPUT:
  # param1: Party-id
  # param2: rank

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

  #script_inflict_casualties_to_party:
  # INPUT:
  # param1: Party-id
  # param2: number of rounds

  #OUTPUT:
  # This script doesn't return a value but populates the parties p_temp_wounded and p_temp_killed with the wounded and killed.
  #Example:
  #  (script_inflict_casualties_to_party, "_p_main_party" ,50),
  #  Simulate 50 rounds of casualties to main_party.

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


  #script_move_members_with_ratio:
  # INPUT:
  # param1: Source Party-id
  # param2: Target Party-id
  # pin_number = ratio of members to move, multiplied by 1000

  #OUTPUT:
  # This script doesn't return a value but moves some of the members of source party to target party according to the given ratio.
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


  # script_count_parties_of_faction_and_party_type:
  ##    [
  ##      # First count num matching spawn points
  ##      (assign, reg(24), 0),
  ##      (try_for_range,reg(25), spawn_points_begin, spawn_points_end),
  ##        (store_faction_of_party, reg(23), reg(25)),
  ##        (eq, reg(23), "$pin_faction"),
  ##        (val_add, reg(24), 1),
  ##      (end_try,0),
  ##      # reg4 now holds num towns of this faction.
  ##      (gt, reg(24), 0), #Fail if there are no towns
  ##      (store_random, reg(26), reg(24)),
  ##
  ##      (assign, reg(24), 0), # reg24 = num points of this faction.
  ##      (try_for_range,reg(25), spawn_points_begin, spawn_points_end),
  ##        (store_faction_of_party, reg(23), reg(25)),
  ##        (eq, reg(23), "$pin_faction"),
  ##        (try_begin,0),
  ##          (eq, reg(24), reg(26)),
  ##          (assign, "$pout_town", reg(25)), # result is this town
  ##        (end_try,0),
  ##        (val_add, reg(24), 1),
  ##      (end_try,0),
  ##  ]),


  #script_spawn_party_at_random_town:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # and spawns a new party there.
  # INPUT:
  # $pin_faction: given_faction
  # $pin_party_template: given_party_template

  #OUTPUT:
  # This script may return false if party cannot be spawned.
  # $pout_party: id of the spawned party
  ##  ("spawn_party_at_random_town",
  ##    [
  ##      (call_script,"script_select_random_spawn_point"),
  ##      (set_spawn_radius,1),
  ##      (spawn_around_party,"$pout_town","$pin_party_template"),
  ##      (assign, "$pout_party", reg(0)),
  ##  ]),

  #script_cf_spawn_party_at_faction_town:
  # This script selects a random town in range [towns_begin, towns_end)
  # such that faction of the town is equal to given_faction
  # and spawns a new party there.
  # INPUT:
  # $pin_faction: given_faction
  # $pin_party_template: given_party_template

  #OUTPUT:
  # This script may return false if party cannot be spawned.
  # $pout_party: id of the spawned party
  ##  ("cf_spawn_party_at_faction_town",
  ##    [
  ##      (call_script,"script_cf_select_faction_spawn_point"),
  ##      (set_spawn_radius,1),
  ##      (spawn_around_party,"$pout_town","$pin_party_template"),
  ##      (assign, "$pout_party", reg(0)),
  ##  ]),

  #script_spawn_party_at_random_town_if_below_limit:
  # This script checks if number of parties
  # of specified template is less than limit,
  # If so, it selects a random town in range [towns_begin, towns_end)
  # and spawns a new party there.
  # INPUT:
  # $pin_party_template: given_party_template
  # $pin_limit: limit value

  #OUTPUT:
  # $pout_party: id of the spawned party
  # $pout_town: id of the selected faction town
  # Note:
  # This script may return false if number of parties
  # of specified template is greater or equal to limit,
  # or if party cannot be spawned.
##  ("cf_spawn_party_at_random_town_if_below_limit",
##    [
##      (store_num_parties_of_template, reg(22), "$pin_party_template"),
##      (lt,reg(22),"$pin_limit"), #check if we are below limit.
##      (call_script,"script_select_random_spawn_point"),
##      (set_spawn_radius,1),
##      (spawn_around_party,"$pout_town","$pin_party_template"),
##      (assign, "$pout_party", reg(0)),
##  ]),

  ##  #script_spawn_party_at_faction_town_if_below_limit:
  ##  # This script checks if number of parties
  ##  # of specified template is less than limit,
  ##  # If so, it selects a random town in range [towns_begin, towns_end)
  ##  # such that faction of the town is equal to given_faction
  ##  # and spawns a new party there.
  ##  # INPUT:
  ##  # $pin_faction: given_faction
  ##  # $pin_party_template: given_party_template
  ##  # $pin_limit: limit value
  ##
  ##  #OUTPUT:
  ##  # $pout_party: id of the spawned party
  ##  # $pout_town: id of the selected faction town
  ##  # Note:
  ##  # This script may return false if number of parties
  ##  # of specified template is greater or equal to limit,
  ##  # or if party cannot be spawned.
  ##  ("cf_spawn_party_at_faction_town_if_below_limit",
  ##    [
  ##      (store_num_parties_of_template, reg(22), "$pin_party_template"),
  ##      (lt,reg(22),"$pin_limit"), #check if we are below limit.
  ##      (call_script,"script_cf_select_faction_spawn_point"),
  ##      (set_spawn_radius,1),
  ##      (spawn_around_party,"$pout_town","$pin_party_template"),
  ##      (assign, "$pout_party", reg(0)),
  ##  ]),

  # script_shuffle_troop_slots:
  # Shuffles a range of slots of a given troop.
  # Used for exploiting a troop as an array.
  # Input: arg1 = troop_no, arg2 = slot_begin, arg3 = slot_end
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


  # script_get_quest - combines old get_random_quest with new get_dynamic_quest
  # Input: arg1 = troop_no,
  # Output: reg0 = enemy_troop_no (Can fail)
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


##  # script_cf_troop_get_random_enemy_troop_as_a_town_lord
##  # Input: arg1 = party_no, arg2 = kingdom_no
##  # Output: reg0 = center_no (closest)
##  ("get_closest_town_of_faction",
##    [
##      (store_script_param_1, ":party_no"),
##      (store_script_param_2, ":kingdom_no"),
##      (assign, ":min_distance", 9999999),
##      (assign, ":result", -1),
##      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##        (store_faction_of_party, ":faction_no", ":center_no"),
##        (eq, ":faction_no", ":kingdom_no"),
##        (party_slot_eq, ":center_no", slot_party_type, spt_town),
##        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
##        (lt, ":party_distance", ":min_distance"),
##        (assign, ":min_distance", ":party_distance"),
##        (assign, ":result", ":center_no"),
##      (try_end),
##      (assign, reg0, ":result"),
##  ]),


  # script_let_nearby_parties_join_current_battle
  # Input: arg1 = besiege_mode, arg2 = dont_add_friends_other_than_accompanying
  # Output: none
  ("let_nearby_parties_join_current_battle",
    [
      (store_script_param, ":besiege_mode", 1),
      (store_script_param, ":dont_add_friends_other_than_accompanying", 2),

      (store_character_level, ":player_level", "trp_player"),
      (try_for_parties, ":party_no"),
        (party_is_active, ":party_no"),
        (party_get_battle_opponent, ":opponent",":party_no"),
        (lt, ":opponent", 0), #party is not itself involved in a battle
        (party_get_attached_to, ":attached_to",":party_no"),
        (lt, ":attached_to", 0), #party is not attached to another party
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (neq, ":behavior", ai_bhvr_in_town),

        (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
        (party_get_template_id,":template_id",":party_no"),
        #SB : exclude certain templates, quest, prisoners/routers
        (neq, ":template_id", "pt_troublesome_bandits"),
        (neq, ":template_id", "pt_bandits_awaiting_ransom"),
        (neq, ":template_id", "pt_rescued_prisoners"),
        (neq, ":template_id", "pt_routed_warriors"),

        (try_begin),
          (this_or_next|is_between, ":stack_troop", "trp_looter", bandits_end),
          (is_between, ":template_id", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (assign, ":is_bandit", 1),
        (else_try),
          (assign, ":is_bandit", 0),
        (try_end),
        (game_get_reduce_campaign_ai, ":join_sub"), #easier = smaller distance bandits
        (try_begin),#Native behaviour
          (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_DISABLE),
          (try_begin),
            (eq, ":is_bandit", 1),
            (assign, ":join_distance", 5), #day/not bandit
            (try_begin),
              (is_currently_night),
              (assign, ":join_distance", 3), #nigh/not bandit
            (try_end),
          (else_try),
            (assign, ":join_distance", 3), #day/bandit
            (try_begin),
              (is_currently_night),
              (assign, ":join_distance", 2), #night/bandit
            (try_end),
          (try_end),
        (else_try), #SB : new distance calculation, based on spotting
          (party_get_skill_level, ":join_distance", ":party_no", "skl_spotting"), #Native lords have none
          (val_div, ":join_distance", 3),
          (val_add, ":join_distance", 4), #from 4 to 7
          (try_begin), #global night deduction
            (is_currently_night),
            (val_sub, ":join_distance", 2), #night/not bandit
          (try_end),
          (try_begin),
            (eq, ":is_bandit", 1),
            (val_sub, ":join_distance", 1), #day/bandit, value of 3
            (val_sub, ":join_distance", ":join_sub"), #can reduce it down to 1 on easy mode
            (is_currently_night), #night/bandit
            (val_add, ":join_distance", 1), #less sharp penalty, value of 2
          (try_end),
          #booster to patrols etc. that makes up for new base of 4
          (try_begin),
            (eq, ":template_id", "pt_patrol_party"),
            (val_add, ":join_distance", 1), #always true
            (try_begin),
              (get_party_ai_object, ":obj", ":party_no"),#just in case
              (eq, ":behavior", ai_bhvr_escort_party),
              (eq, ":obj", "p_main_party"),
              (val_add, ":join_distance", ":join_sub"),#they stray off easily
            (try_end),
          # (else_try), #other behaviour score
            # (eq, ":behavior", ai_bhvr_avoid_party), #fleeing
            # (val_sub, ":join_distance", 1),
          (else_try), #representing preparedness to join battle
            (this_or_next|eq, ":behavior", ai_bhvr_patrol_party),
            (this_or_next|eq, ":behavior", ai_bhvr_patrol_location),
            (eq, ":behavior", ai_bhvr_escort_party),
            (val_add, ":join_distance", 1),
          (try_end),
        (try_end),


		# #Quest bandits do not join battle
		# (this_or_next|neg|check_quest_active, "qst_track_down_bandits"),
			# (neg|quest_slot_eq, "qst_track_down_bandits", slot_quest_target_party, ":party_no"),
		# (this_or_next|neg|check_quest_active, "qst_troublesome_bandits"),
			# (neg|quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, ":party_no"),



        (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
        (lt, ":distance", ":join_distance"),

        (store_faction_of_party, ":faction_no", ":party_no"),
        (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
        (try_begin),
          (eq, ":faction_no", "fac_player_supporters_faction"),
          (assign, ":reln_with_player", 100),
        (else_try),
          (store_relation, ":reln_with_player", ":faction_no", "fac_player_supporters_faction"),
        (try_end),
        (try_begin),
          (eq, ":faction_no", ":enemy_faction"),
          (assign, ":reln_with_enemy", 100),
        (else_try),
          (store_relation, ":reln_with_enemy", ":faction_no", ":enemy_faction"),
        (try_end),

        (assign, ":enemy_side", 1),
        (try_begin),
          (neq, "$g_enemy_party", "$g_encountered_party"),
          (assign, ":enemy_side", 2),
        (try_end),

        (try_begin),
          (eq, ":besiege_mode", 0),
          (lt, ":reln_with_player", 0),
          (gt, ":reln_with_enemy", 0),
          ##zerilius changes begin
          ##wrong use of operation (native bug)
          #(party_get_slot, ":party_type", ":party_no"),
          (party_get_slot, ":party_type", ":party_no", slot_party_type),
          ##zerilius changes end

          (assign, ":enemy_is_bandit_party_and_level_is_greater_than_6", 0),
          (try_begin), #SB : is_bandit
            # (party_stack_get_troop_id, ":stack_troop", ":party_no", 0),
            # (is_between, ":stack_troop", "trp_looter", "trp_black_khergit_horseman"),
            (eq, ":is_bandit", 1),
            (gt, ":player_level", 6),
            (assign, ":enemy_is_bandit_party_and_level_is_greater_than_6", 1),
          (try_end),

          (this_or_next|eq, ":party_type", spt_kingdom_hero_party),
          (eq, ":enemy_is_bandit_party_and_level_is_greater_than_6", 1),

          (get_party_ai_behavior, ":ai_bhvr", ":party_no"),
          (neq, ":ai_bhvr", ai_bhvr_avoid_party),
          (party_quick_attach_to_current_battle, ":party_no", ":enemy_side"), #attach as enemy
          (str_store_party_name, s1, ":party_no"),
          #SB : colorize
          (display_message, "str_s1_joined_battle_enemy", message_negative),
        (else_try),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, "trp_player"),
            (assign, ":party_is_accompanying_player", 1),
          (else_try),
            (assign, ":party_is_accompanying_player", 0),
          (try_end),

          (this_or_next|eq, ":dont_add_friends_other_than_accompanying", 0),
          (eq, ":party_is_accompanying_player", 1),
          (gt, ":reln_with_player", 0),
          (lt, ":reln_with_enemy", 0),

          (assign, ":following_player", 0),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
            (assign, ":following_player", 1),
          (try_end),

          (assign, ":do_join", 1),
          (try_begin),
            (eq, ":besiege_mode", 1),
            (eq, ":following_player", 0),
            (assign, ":do_join", 0),
            (eq, ":faction_no", "$players_kingdom"),
            (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
            (assign, ":do_join", 1),
          (try_end),
          (eq, ":do_join", 1),

          ##zerilius changes begin
          ##wrong use of operation (native bug)
          #(party_get_slot, ":party_type", ":party_no"),
          (party_get_slot, ":party_type", ":party_no", slot_party_type),
          ##zerilius changes end
          (this_or_next|eq, ":party_type", spt_kingdom_hero_party), #dckplmc
          (eq, ":template_id", "pt_hero_party"),
          (party_stack_get_troop_id, ":leader", ":party_no", 0),
          #(troop_get_slot, ":player_relation", ":leader", slot_troop_player_relation),
          (call_script, "script_troop_get_player_relation", ":leader"),
          (assign, ":player_relation", reg0),

          (assign, ":join_even_you_do_not_like_player", 0),
          (try_begin),
            (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"), #new added, if player is marshal and if he is accompanying then join battle even lord do not like player
            (eq, ":following_player", 1),
            (assign, ":join_even_you_do_not_like_player", 1),
          ##diplomacy start+
	  #Affiliates will assist the player.
	   (else_try),
             (lt, ":player_relation", 0),
	     (call_script, "script_dplmc_is_affiliated_family_member", ":leader"),
	     (val_max, ":player_relation", reg0),
          ##diplomacy end+
          (try_end),

          (this_or_next|ge, ":player_relation", 0),
          (eq, ":join_even_you_do_not_like_player", 1),

          (party_quick_attach_to_current_battle, ":party_no", 0), #attach as friend
          (str_store_party_name, s1, ":party_no"),
          # ## SB : colorize
          # (faction_get_color, ":color", ":faction_no"),
          (display_message, "str_s1_joined_battle_friend", message_positive),

          (troop_get_slot, ":limit", "$g_player_troop", slot_troop_renown),
          (val_sub, ":limit", dplmc_command_renown_limit),
          (game_get_reduce_campaign_ai, ":bonus"),
          (val_mul, ":bonus", "$player_right_to_rule"),
          (val_add, ":limit", ":bonus"),

          (assign, ":continue", -1), #by default, not under command

          (try_begin), #under command if marshal
            (eq, ":faction_no", "$players_kingdom"),
            (troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
            (try_begin), #as marshal
               # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
               # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
               # (assign, ":continue", 0),
            # (else_try), #as ruler/pretender marshal
               # (faction_slot_eq, ":party_faction", slot_faction_state, sfs_active),
               (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
               (ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),

               (display_message, "@marshall {reg0}"),
               # (this_or_next|faction_slot_eq, ":party_faction", slot_faction_marshall, "trp_player"),
               # (faction_slot_eq, ":party_faction", slot_faction_leader, "$g_player_troop"),
               (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", -1), #If still not satisfied, check other conditions
          (else_try), #or high enough renown
            (troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":renown", ":leader", slot_troop_renown),
            (call_script, "script_troop_get_relation_with_troop", ":leader", "$g_player_troop"),
            (val_sub, ":renown", reg0), #higher relation means less renown needed.
            (le, ":renown", ":limit"),

            (assign, ":continue", 0),
          (else_try), #straggler parties - patrols, caravans, etc.
            (neg|is_between, ":leader", active_npcs_begin, active_npcs_end),

            (assign, ":continue", 0),
          (try_end),
          (party_set_slot, ":party_no", slot_party_temp_slot_1, ":continue"),
          (try_begin),
            (ge, "$cheat_mode", 1),
            (assign, reg0, ":continue"),
            # (str_store_party_name, s0, ":party_no"),
            (str_store_party_name, s0, ":party_no"),
            (faction_get_color, ":color", ":faction_no"),
            (display_message, "@{s0} will {reg0?not :}be under your command", ":color"),
          (try_end),

        (try_end),
      (try_end),
  ]),

  # script_party_wound_all_members_aux
  # Input: arg1 = party_no
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

  # script_party_wound_all_members
  # Input: arg1 = party_no
  ("party_wound_all_members",
    [
      (store_script_param_1, ":party_no"),

      (call_script, "script_party_wound_all_members_aux", ":party_no"),
  ]),



  # script_calculate_battle_advantage
  # Input: none
  # Output: none, fails when enemies are nearby
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

  # script_get_heroes_attached_to_center_aux
  # Input: arg1 = party_no_1, arg2 = party_no_2
  # Output: reg0 = relation between parties
  ("get_relation_between_parties",
    [
      (store_script_param_1, ":party_no_1"),
      (store_script_param_2, ":party_no_2"),

      (store_faction_of_party, ":party_no_1_faction", ":party_no_1"),
      (store_faction_of_party, ":party_no_2_faction", ":party_no_2"),
      (try_begin),
        (eq, ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, 100),
      (else_try),
        (store_relation, ":relation", ":party_no_1_faction", ":party_no_2_faction"),
        (assign, reg0, ":relation"),
      (try_end),
  ]),
  # script_calculate_weekly_party_wage
  # Input: arg1 = party_no
  # Output: reg0 = weekly wage
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

  # script_calculate_player_faction_wage
  # Input: arg1 = party_no,
  # Output: none
  # Adds reinforcement to party according to its type and faction
  # Called from several places, simple_triggers for centers, script_hire_men_to_kingdom_hero_party for hero parties
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

  # script_hire_men_to_kingdom_hero_party
  # Input: arg1 = value, arg2 = percentage
  # Output: none
  ("get_percentage_with_randomized_round",
    [
      (store_script_param, ":value", 1),
      (store_script_param, ":percentage", 2),

      (store_mul, ":result", ":value", ":percentage"),
      (val_div, ":result", 100),
      (store_mul, ":used_amount", ":result", 100),
      (val_div, ":used_amount", ":percentage"),
      (store_sub, ":left_amount", ":value", ":used_amount"),
      (try_begin),
        (gt, ":left_amount", 0),
        (store_mul, ":chance", ":left_amount", ":percentage"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
      ]),

  # script_create_cattle_herd
  # Input: arg1 = center_no, arg2 = amount (0 = default)
  # Output: reg0 = party_no
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

  #script_buy_cattle_from_village
  # Input: arg1 = party_no, arg2 = amount
  # Output: none (fills trp_temp_troop's inventory)
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

  # script_create_kingdom_hero_party
  # Input: arg1 = faction_no, arg2 = party_type (variables beginning with spt_)
  # Output: reg0 = party_no
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


  # script_cf_create_kingdom_party
  # Input: arg1 = faction_no, arg2 = party_type (variables beginning with spt_)
  # Output: reg0 = party_no
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

  # script_get_troop_attached_party
  # Input: arg1 = troop_no
  # Output: reg0 = party_no (-1 if troop's party is not attached to a party)
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


  # script_center_get_food_consumption
  # Input: none
  # Output: none
  #called from triggers
  ("process_alarms",
    [
      (assign, ":current_modula", "$g_alarm_modula"),
      (val_add, "$g_alarm_modula", 1),
      (try_begin),
        (eq, "$g_alarm_modula", 3),
        (assign, "$g_alarm_modula", 0),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),

        (party_set_slot, ":center_no", slot_center_last_spotted_enemy, -1),
        (party_set_slot, ":center_no", slot_center_sortie_strength, 0),
        (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, 0),

        (assign, ":spotting_range", 3),
        (try_begin),
          (is_currently_night),
          (assign, ":spotting_range", 2),
        (try_end),

        (try_begin),
          (party_slot_eq, ":center_no", slot_center_has_watch_tower, 1),
          (val_mul, ":spotting_range", 2),
        (else_try),
          (neg|is_between, ":center_no", villages_begin, villages_end),
          (val_add, ":spotting_range", 1),
          (val_mul, ":spotting_range", 2),
        (try_end),

        (store_faction_of_party, ":center_faction", ":center_no"),

        (try_for_parties, ":party_no"),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
          (eq, ":party_no", "p_main_party"),

          (store_faction_of_party, ":party_faction", ":party_no"),

          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (assign, ":party_faction", "$players_kingdom"),
          (try_end),

          (try_begin),
            (eq, ":party_faction", ":center_faction"),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
            (le, ":distance", ":spotting_range"),

            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
            (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
            (val_add, ":sortie_strength", ":cached_strength"),
            (party_set_slot, ":center_no", slot_center_sortie_strength, ":sortie_strength"),
          (else_try),
            (neq, ":party_faction", ":center_faction"),

            (store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),

			(try_begin),
				(lt, ":distance", 10),
				(store_current_hours, ":hours"),
				(store_sub, ":faction_recce_slot", ":party_faction", kingdoms_begin),
				(val_add, ":faction_recce_slot", slot_center_last_reconnoitered_by_faction_time),
				(party_set_slot, ":center_no", ":faction_recce_slot", ":hours"),

				#(eq, "$cheat_mode", 1),
				#(str_store_faction_name, s4, ":party_faction"),
				#(str_store_party_name, s5, ":center_no"),
				#(display_message, "@{!}DEBUG -- {s4} reconnoiters {s5}"),
			(try_end),

		    (store_relation, ":reln", ":center_faction", ":party_faction"),
            (lt, ":reln", 0),
			(try_begin),
	            (le, ":distance", ":spotting_range"),

	            (party_get_slot, ":cached_strength", ":party_no", slot_party_cached_strength),
	            (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),
	            (val_add, ":enemy_strength", ":cached_strength"),
	            (party_set_slot, ":center_no", slot_center_sortie_enemy_strength, ":enemy_strength"),
	            (party_set_slot, ":center_no", slot_center_last_spotted_enemy, ":party_no"),
			(try_end),

          (try_end),
        (try_end),
      (try_end),

      (try_for_range, ":center_no", centers_begin, centers_end),
        (store_mod, ":center_modula", ":center_no", 3),
        (eq, ":center_modula", ":current_modula"),

        (try_begin), #eligible units sortie out of castle
          (is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),

          (party_get_slot, ":sortie_strength", ":center_no", slot_center_sortie_strength),
          (party_get_slot, ":enemy_strength", ":center_no", slot_center_sortie_enemy_strength),

          #Below two lines are new added by ozan. While AI want to drive nearby besieging enemy parties by making sortie them, they give up current battle if they are already joining one.
          #Lets assume there is a battle inside the castle, because enemies are inside castle and they are so close to castle they will be also added to slot_center_sortie_enemy_strength
          #But in this scenario, they are not outside the castle, so searching/patrolling enemy outside the castle is useless at this point.
          #So if there is already a battle inside the center, do not sortie and search enemy outside.
          (party_get_battle_opponent, ":center_battle_opponent", ":center_no"),
          (try_begin),
		    (ge, "$cheat_mode", 1),
            (ge, ":center_battle_opponent", 0),
            (str_store_party_name, s7, ":center_no"),
            (str_store_party_name, s6, ":center_battle_opponent"),
            (display_message, "@{!}DEBUG : There are already enemies ({s6}) inside {s7}."),
          (try_end),
          (lt, ":center_battle_opponent", 0),
          #New added by ozan ended.

          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s4, ":center_no"),
            (assign, reg3, ":sortie_strength"),
            (assign, reg4, ":enemy_strength"),
            (display_message, "@{!}DEBUG -- Calculating_sortie for {s4} strength of {reg3} vs {reg4} enemies"),
          (try_end),

          (store_mul, ":enemy_strength_mul_14_div_10", ":enemy_strength", 14),
          (val_div, ":enemy_strength_mul_14_div_10", 10),
          (gt, ":sortie_strength", ":enemy_strength_mul_14_div_10"),

          (assign, ":at_least_one_party_sorties", 0),
          (try_for_parties, ":sortie_party"),
            (party_get_attached_to, ":town", ":sortie_party"),
            (eq, ":town", ":center_no"),

            (party_slot_eq, ":sortie_party", slot_party_type, spt_kingdom_hero_party),

            (party_get_slot, ":cached_strength", ":sortie_party", slot_party_cached_strength),
            (ge, ":cached_strength", 100),

            (party_detach, ":sortie_party"),
            (call_script, "script_party_set_ai_state", ":sortie_party",  spai_patrolling_around_center, ":center_no"),

            (try_begin),
              (eq, "$cheat_mode", 1),
              (str_store_party_name, s4, ":sortie_party"),
              (display_message, "str_s4_sorties"),
            (try_end),

            (eq, ":at_least_one_party_sorties", 0),
            (assign, ":at_least_one_party_sorties", ":sortie_party"),
          (try_end),

          (try_begin),
            (party_is_in_town, "p_main_party", ":center_no"),
			(eq, "$g_player_is_captive", 0),
            (gt, ":at_least_one_party_sorties", 0),
            (call_script, "script_add_notification_menu", "mnu_notification_sortie_possible", ":center_no", ":sortie_party"),
          (try_end),
		(try_end),

		(store_faction_of_party, ":center_faction", ":center_no"),

		#Send message
		(this_or_next|eq, "$cheat_mode", 1), #this is message
		(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(eq, ":center_faction", "$players_kingdom"),

		(party_get_slot, ":enemy_party", ":center_no", slot_center_last_spotted_enemy),
		(ge, ":enemy_party", 0),
		(store_distance_to_party_from_party, ":dist", "p_main_party", ":center_no"),
		(assign, ":has_messenger", 0),
		(try_begin),
		 ##diplomacy start+ Handle player is co-ruler of faction
		 (assign, ":is_coruler", 0),
		 (try_begin),
			(eq, ":center_faction", "$players_kingdom"),
			(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":is_coruler", 1),
		 (try_end),
		 (this_or_next|eq, ":is_coruler", 1),
		 ##diplomacy end+
		  (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		  (eq, ":center_faction", "fac_player_supporters_faction"),
		  (party_slot_eq, ":center_no", slot_center_has_messenger_post, 1),
		  (assign, ":has_messenger", 1),
		(try_end),

		(this_or_next|eq, "$cheat_mode", 1),
		(this_or_next|lt, ":dist", 30),
			(eq, ":has_messenger", 1),

		(str_store_party_name_link, s1, ":center_no"),
        (party_get_slot, ":exact_enemy_strength", ":center_no", slot_center_sortie_enemy_strength),

		(try_begin),
			(lt, ":exact_enemy_strength", 500),
			(display_message, "@Small bands of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 1000),
			(display_message, "@Enemy patrols spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 2000),
			(display_message, "@Medium-sized group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 4000),
			(display_message, "@Significant group of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 8000),
			(display_message, "@Army of enemies spotted near {s1}."),
		(else_try),
			(lt, ":exact_enemy_strength", 16000),
			(display_message, "@Large army of enemies spotted near {s1}."),
		(else_try),
			(display_message, "@Great host of enemies spotted near {s1}."),
		(try_end),
		#maybe do audio sound?

      (try_end),
     ]),

  # script_allow_vassals_to_join_indoor_battle
  # Input: none
  # Output: none
  ("allow_vassals_to_join_indoor_battle",
    [
     #if our commander attacks an enemy army
     ##diplomacy start+ Support promoted kingdom ladies
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
     (try_for_range, ":troop_no", heroes_begin, heroes_end),
     ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),

       (party_get_attached_to, ":party_is_attached_to", ":party_no"),
       (lt, ":party_is_attached_to", 0),

       (store_troop_faction, ":faction_no", ":troop_no"),

       (try_begin),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_enemies_around_center),
         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),

         (assign, ":besieged_center", -1),
         (try_begin),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_holding_center), #if commander is holding a center
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (center they are holding)
           (party_get_battle_opponent, ":besieger_enemy", ":commander_object"), #get this object's battle opponent
           (party_is_active, ":besieger_enemy"),
           (assign, ":besieged_center", ":commander_object"),
           (assign, ":commander_object", ":besieger_enemy"),
         (else_try),
           (party_slot_eq, ":commander_party", slot_party_ai_state, spai_engaging_army), #if commander is engaging an army
           (party_get_slot, ":commander_object", ":commander_party", slot_party_ai_object), #get commander's ai object (army which they engaded)
           (ge, ":commander_object", 0), #if commander has an object
           (neg|is_between, ":commander_object", centers_begin, centers_end), #if this object is not a center, so it is a party
           (party_is_active, ":commander_object"),
           (party_get_battle_opponent, ":besieged_center", ":commander_object"), #get this object's battle opponent
         (else_try),
           (assign, ":besieged_center", -1),
         (try_end),

         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if battle opponent of our commander's ai object is a walled center

         (party_get_attached_to, ":attached_to_party", ":commander_party"), #if commander is attached to besieged center already.
         (eq, ":attached_to_party", ":besieged_center"),

         (store_faction_of_party, ":besieged_center_faction", ":besieged_center"),#get (battle opponent of our commander's ai object)'s faction
         (eq, ":besieged_center_faction", ":faction_no"), #if battle opponent of our commander's ai object is from same faction with current party
         (party_is_active, ":commander_object"),
         #make also follow_or_not check if needed

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":commander_object"), #go and help commander

         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_party_name, s7, ":party_no"),
           (str_store_party_name, s6, ":commander_object"),
           (display_message, "@{!}DEBUG : {s7} is helping his commander by fighting with {s6}."),
         (try_end),
       (else_try),
         #(faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_attacking_center),

         (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
         (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
         (gt, ":commander_party", 0),
         (party_is_active, ":commander_party"),

         (party_get_battle_opponent, ":besieged_center", ":commander_party"), #get this object's battle opponent

         #make also follow_or_not check if needed

         (is_between, ":besieged_center", walled_centers_begin, walled_centers_end), #if this object is a center
         (party_get_attached_to, ":attached_to_party", ":party_no"),
         (neq, ":attached_to_party", ":besieged_center"),
         (party_is_active, ":besieged_center"),

         (call_script, "script_party_set_ai_state", ":party_no", spai_engaging_army, ":besieged_center"), #go and help commander

         #(try_begin),
         #  (eq, "$cheat_mode", 1),
         #  (str_store_party_name, s7, ":party_no"),
         #  (str_store_party_name, s6, ":besieged_center"),
         #  (display_message, "@{!}DEBUG : {s7} is helping his commander by attacking {s6}."),
         #(try_end),

         #(party_set_ai_behavior, ":party_no", ai_bhvr_attack_party),
         #(party_set_ai_object, ":party_no", ":besieged_center"),
         #(party_set_flags, ":party_no", pf_default_behavior, 1), #is these needed?
         #(party_set_slot, ":party_no", slot_party_ai_substate, 1), #is these needed?
       (try_end),
     (try_end),
     ]),

  # script_party_set_ai_state
  # Input: arg1 = party_no, arg2 = new_ai_state, arg3 = action_object (if necessary)
  # Output: none (Can fail)

  #Redone somewhat on Feb 18 to make sure that initative is set properly

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

  #Currently called from process_ai_state, could be called from elsewhere
    # Input: arg1 = troop_no
    # Output: reg0 = effective relation (modified by troop reputation, honor, etc.)
    ("troop_get_player_relation",
      [
        (store_script_param_1, ":troop_no"),
        (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
        (troop_get_slot, ":effective_relation", ":troop_no", slot_troop_player_relation),
        (assign, ":honor_bonus", 0),
        (try_begin),
          (eq,  ":reputation", lrep_quarrelsome),
          (val_add, ":effective_relation", -3),
        (try_end),
        (try_begin),
          (ge, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
             (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy start+
		  (else_try),
			#In general this should not apply to ladies, as they operate by different
			#reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			#it should apply.
		     (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 #Personality type that values keeping your word
			 (call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			 (ge, reg0, 1),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  ##diplomacy end+
          (try_end),
        (try_end),
        (try_begin),
          (lt, "$player_honor", 0),
          (try_begin),
            (this_or_next|eq,  ":reputation", lrep_upstanding),
            (             eq,  ":reputation", lrep_goodnatured),
            (store_div, ":honor_bonus", "$player_honor", 3),
          ##diplomacy start+
		  (else_try),
			(call_script, "script_dplmc_get_troop_morality_value", ":troop_no", tmt_honest),
			(ge, reg0, 1),#Personality type that values keeping your word
			(store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
		  	 #"My kind of scum" - a few rare individuals might actively approve.
		  	 (lt, reg0, 0),#<-- must have negative value for tmt_honest; by default this is only Rolf.
		  	 (this_or_next|eq, ":reputation", lrep_roguish),
		  	 (this_or_next|eq, ":reputation", lrep_custodian),
		  	 (this_or_next|eq, ":reputation", lrep_debauched),
		  	 (this_or_next|eq, ":reputation", lrep_ambitious),
		  		(eq, ":reputation", lrep_cunning),
		  	 (store_div, ":honor_bonus", "$player_honor", -5),
		  	 (val_clamp, ":honor_bonus", 1, 6),
          (else_try),
			#"Honorable" lords can be awful people, so no bonus with benefactors,
			#but dishonorable lords are *guaranteed* to be awful.
            (eq, ":reputation", lrep_benefactor),
            (store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			#Self-righteous lords are moralizing but hypocritical.
			(eq, ":reputation", lrep_selfrighteous),
			(store_div, ":honor_bonus", "$player_honor", 5),
		  (else_try),
			 #In general this should not apply to ladies, as they operate by different
			 #reputation rules, but if a "kingdom lady" has become a "kingdom hero" instead,
			 #it should apply.
			 (eq,  ":reputation", lrep_moralist),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 3),
		  (else_try),
			 (eq,  ":reputation", lrep_conventional),#-- verify that the lady is effectively a lord:
		     (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			 (store_div, ":honor_bonus", "$player_honor", 5),
          ##diplomacy end+
          (else_try),
            (eq,  ":reputation", lrep_martial),
            (store_div, ":honor_bonus", "$player_honor", 5),
          (try_end),
        (try_end),
        (val_add, ":effective_relation", ":honor_bonus"),
        (val_clamp, ":effective_relation", -100, 101),
        (assign, reg0, ":effective_relation"),
    ]),

  # script_change_troop_renown
  # Input: arg1 = troop_no, arg2 = relation difference
  # Output: none
  ("change_troop_renown",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":renown_change"),

      (troop_get_slot, ":old_renown", ":troop_no", slot_troop_renown),

	  (try_begin),
		(gt, ":renown_change", 0),
		(assign, reg4, ":renown_change"),

		(store_div, ":subtraction", ":old_renown", 200),
	    (val_sub, ":renown_change", ":subtraction"),
	    (val_max, ":renown_change", 0),

	    (eq, ":troop_no", "trp_player"),
	    (assign, reg5, ":renown_change"),

		(eq, "$cheat_mode", 1),
	    (display_message, "str_renown_change_of_reg4_reduced_to_reg5_because_of_high_existing_renown"),
	  (try_end),

      (store_add, ":new_renown", ":old_renown", ":renown_change"),
      (val_max, ":new_renown", 0),
      (troop_set_slot, ":troop_no", slot_troop_renown, ":new_renown"),

      (try_begin),
        (eq, ":troop_no", "trp_player"),

		(try_begin),
		  (ge, ":new_renown", 50),

          (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_TALK_OF_THE_TOWN),
          (try_end),
		(try_end),

        # (str_store_troop_name, s1, ":troop_no"),
        (assign, reg12, ":renown_change"),
        (val_abs, reg12),
        (try_begin),
         (gt, ":renown_change", 0),
         (display_message, "@You gained {reg12} renown.", message_positive),
        (else_try),
          (lt, ":renown_change", 0),
          (display_message, "@You lose {reg12} renown.", message_negative),
        (try_end),
      (try_end),
      (call_script, "script_update_troop_notes", ":troop_no"),
  ]),


  # script_change_player_relation_with_troop
  # Input: arg1 = troop_no, arg2 = relation difference
  # Output: none
  ("change_player_relation_with_troop",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (neq, ":troop_no", "trp_player"),
        (neg|is_between, ":troop_no", soldiers_begin, soldiers_end),
        ##diplomacy start+
		  (neq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
		  #(neq, ":troop_no", -1),#OLD
		  (ge, ":troop_no", 1),#NEW
        ##diplomacy end+
        (neq, ":difference", 0),
        (call_script, "script_troop_get_player_relation", ":troop_no"),
        (assign, ":old_effective_relation", reg0),
        (troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
        (val_add, ":player_relation", ":difference"),
        (val_clamp, ":player_relation", -100, 101),
        (try_begin),
          (troop_set_slot, ":troop_no", slot_troop_player_relation, ":player_relation"),

          (try_begin),
            (le, ":player_relation", -50),
            (unlock_achievement, ACHIEVEMENT_OLD_DIRTY_SCOUNDREL),
          (try_end),

          (str_store_troop_name_link, s1, ":troop_no"),
          (call_script, "script_troop_get_player_relation", ":troop_no"),
          (assign, ":new_effective_relation", reg0),
          (neq, ":old_effective_relation", ":new_effective_relation"),
          (assign, reg1, ":old_effective_relation"),
          (assign, reg2, ":new_effective_relation"),
          (try_begin),
			##diplomacy start+ Suppress this message for dead people except in cheat mode
            (lt, "$cheat_mode", 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			(neq, ":troop_no", "$g_talk_troop"),
		  (else_try),
		  ##diplomacy end+
            (gt, ":difference", 0),
            (display_message, "str_troop_relation_increased", message_positive),
          (else_try),
            (lt, ":difference", 0),
            (display_message, "str_troop_relation_detoriated", message_negative),
          (try_end),
          (try_begin),
            (eq, ":troop_no", "$g_talk_troop"),
            (assign, "$g_talk_troop_relation", ":new_effective_relation"),
            (call_script, "script_setup_talk_info"),
          (try_end),
          (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
      (try_end),
  ]),

  # script_change_player_relation_with_center
  # Input: arg1 = faction_no, arg2 = relation difference
  # Output: none
  ("make_kingdom_hostile_to_player",
    [
      (store_script_param_1, ":kingdom_no"),
      (store_script_param_2, ":difference"),

      (try_begin),
        (lt, ":difference", 0),
        (store_relation, ":player_relation", ":kingdom_no", "fac_player_supporters_faction"),
        (val_min, ":player_relation", 0),
        (val_add, ":player_relation", ":difference"),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_no", ":player_relation"),
      (try_end),
  ]),

  # script_change_player_honor
  # Input: arg1 = honor difference
  # Output: none
  ("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      ##diplomacy start+
      #Exacerbate the effect of honor losses as the player's honor increases
      (try_begin),
         (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#<-- experimental settings must be enabled
         (ge, "$player_honor", 10),
         (lt, ":honor_dif", 0),
         (store_add, ":honor_multiplier", "$player_honor", 100),
         (val_mul, ":honor_dif", ":honor_multiplier"),
         (val_sub, ":honor_dif", 50),
         (val_div, ":honor_dif", 100),
      (try_end),
      ##diplomacy end+
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour.", message_positive),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour.", message_negative),
      (try_end),

##      (val_mul, ":honor_dif", 1000),
##      (assign, ":temp_honor", 0),
##      (assign, ":num_nonlinear_steps", 10),
##      (try_begin),
##        (gt, "$player_honor", 0),
##        (lt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 0),
##      (else_try),
##        (lt, "$player_honor", 0),
##        (gt, ":honor_dif", 0),
##        (assign, ":num_nonlinear_steps", 3),
##      (try_end),
##
##      (try_begin),
##        (ge, "$player_honor", 0),
##        (assign, ":temp_honor", "$player_honor"),
##      (else_try),
##        (val_sub, ":temp_honor", "$player_honor"),
##      (try_end),
##      (try_for_range, ":unused",0,":num_nonlinear_steps"),
##        (ge, ":temp_honor", 10000),
##        (val_div, ":temp_honor", 2),
##        (val_div, ":honor_dif", 2),
##      (try_end),
##      (val_add, "$player_honor", ":honor_dif"),
  ]),

  # script_change_player_party_morale
  # Input: arg1 = morale difference
  # Output: none
  ("change_player_party_morale",
    [
      (store_script_param_1, ":morale_dif"),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (val_clamp, ":cur_morale", 0, 100),

      (store_add, ":new_morale", ":cur_morale", ":morale_dif"),
      (val_clamp, ":new_morale", 0, 100),

      (party_set_morale, "p_main_party", ":new_morale"),
      #SB : colorize message
      (try_begin),
        (lt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":cur_morale", ":new_morale"),
        (display_message, "str_party_lost_morale", message_negative),
      (else_try),
        (gt, ":new_morale", ":cur_morale"),
        (store_sub, reg1, ":new_morale", ":cur_morale"),
        (display_message, "str_party_gained_morale", message_positive),
      (try_end),
  ]),

  # script_cf_player_has_item_without_modifier
  # Input: arg1 = item_id, arg2 = modifier
  # Output: none (can_fail)
  ("cf_player_has_item_without_modifier",
    [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
      (player_has_item, ":item_id"),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", "trp_player"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
  ]),

  # script_get_player_party_morale_values
  # Output: reg0 = player_party_morale_target
  ("get_player_party_morale_values",
    [
      (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
      (assign, ":num_men", 0),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":num_men", 1), #it was 3 in "Mount&Blade", now it is 1 in Warband
        (else_try),
          (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
          (val_add, ":num_men", ":stack_size"),
        (try_end),
      (try_end),
      (assign, "$g_player_party_morale_modifier_party_size", ":num_men"),

      (store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),

      (try_begin),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (faction_get_slot, ":cur_faction_king", "$players_kingdom", slot_faction_leader),
        (eq, ":cur_faction_king", "trp_player"),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 15),
      (else_try),
        (store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", 12),
      (try_end),

      (assign, ":new_morale", "$g_player_party_morale_modifier_leadership"),
      (val_sub, ":new_morale", "$g_player_party_morale_modifier_party_size"),

      (val_add, ":new_morale", 50),

      (assign, "$g_player_party_morale_modifier_food", 0),
      (try_for_range, ":cur_edible", "itm_raw_date_fruit", food_end),
        (neq, ":cur_edible", "itm_furs"),
        (item_slot_eq, ":cur_edible", slot_item_edible, 1),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),

        (val_mul, ":food_bonus", 3),
        (val_div, ":food_bonus", 2),

        (val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
      (try_end),
      (val_add, ":new_morale", "$g_player_party_morale_modifier_food"),

      (try_begin),
        (eq, "$g_player_party_morale_modifier_food", 0),
        (assign, "$g_player_party_morale_modifier_no_food", 30),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
      (else_try),
        (assign, "$g_player_party_morale_modifier_no_food", 0),
      (try_end),

      (assign, "$g_player_party_morale_modifier_debt", 0),
      (try_begin),
        (gt, "$g_player_debt_to_party_members", 0),
        (call_script, "script_calculate_player_faction_wage"),
        (assign, ":total_wages", reg0),
        (store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
		(val_max, ":total_wages", 1),
        (val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
        (val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
        (val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
      (try_end),

      (val_clamp, ":new_morale", 0, 100),
      (assign, reg0, ":new_morale"),
      ]),

  # script_diplomacy_start_war_between_kingdoms
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("diplomacy_start_war_between_kingdoms", #sets relations between two kingdoms and their vassals.
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #1 = after start of game

	  (call_script, "script_npc_decision_checklist_peace_or_war", ":kingdom_a", ":kingdom_b", -1),
	  (assign, ":explainer_string", reg1),

	  #
    ##diplomacy begin
    (try_begin),
      (lt, ":initializing_war_peace_cond", 2),
    ##diplomacy end
	  (try_begin),
	    (eq, ":kingdom_a", "fac_player_supporters_faction"),
		(assign, ":war_event", logent_player_faction_declares_war),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_declared_war_to_control_calradia"),
		(assign, ":war_event", logent_player_faction_declares_war), #for savegame compatibility, this event stands in for the attempt to declare war on all of calradia
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_considers_s16_to_be_dangerous_and_untrustworthy_and_shehe_wants_to_bring_s16_down"),
		(assign, ":war_event", logent_faction_declares_war_out_of_personal_enmity),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_anxious_to_reclaim_old_lands_such_as_s18_now_held_by_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_regain_territory),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_faces_too_much_internal_discontent_to_feel_comfortable_ignoring_recent_provocations_by_s16s_subjects"),
		(assign, ":war_event", logent_faction_declares_war_to_respond_to_provocation),
	  (else_try),
		(eq, ":explainer_string", "str_s12s15_is_alarmed_by_the_growing_power_of_s16"),
		(assign, ":war_event", logent_faction_declares_war_to_curb_power),
	  (try_end),
	  (call_script, "script_add_log_entry", ":war_event", ":kingdom_a", 0, 0, ":kingdom_b"),



	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":kingdom_a", ":kingdom_b"),
	  (assign, ":current_diplomatic_status", reg0),
	  (try_begin), #effects of policy only after the start of the game
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", -1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
	  (else_try),
	    (eq, ":initializing_war_peace_cond", 1),
		(eq, ":current_diplomatic_status", 0),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":current_diplomatic_status", 1),
		(call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_breaks_truce),
	  (try_end),
	  ##diplomacy begin
    (else_try),
      (assign, ":war_event", logent_faction_declares_war_to_fulfil_pact),
      (call_script, "script_faction_follows_controversial_policy", ":kingdom_a", logent_policy_ruler_declares_war_with_justification),
      (assign, ":initializing_war_peace_cond", 1),
	  (try_end),
	  ##diplomacy end

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_min, ":relation", -10),
      (val_add, ":relation", -30),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_min, ":relation", -30),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),

		#Remove this -- this scrambles who declares war on whom
#        (try_begin),
 #         (store_random_in_range, ":random_no", 0, 2),
  #        (this_or_next|eq, ":kingdom_a", "fac_player_supporters_faction"),
	#		(eq, ":random_no", 0),
     #     (assign, ":local_temp", ":kingdom_a"),
      #    (assign, ":kingdom_a", ":kingdom_b"),
       #   (assign, ":kingdom_b", ":local_temp"),
        #(try_end),

        (str_store_faction_name_link, s1, ":kingdom_a"),
        #SB : don't colorize message, if it's relevant script_set_player_relation_with_faction calls will show it
        # (faction_get_color, ":color", ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} has declared war against {s2}.", message_alert),

		(store_current_hours, ":hours"),
		(faction_set_slot, ":kingdom_a", slot_faction_ai_last_decisive_event, ":hours"),
		(faction_set_slot, ":kingdom_b", slot_faction_ai_last_decisive_event, ":hours"),

		#set provocation and truce days
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_b", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_a", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_a", ":provocation_slot", 0),

		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(store_add, ":provocation_slot", ":kingdom_a", slot_faction_provocation_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		(val_sub, ":provocation_slot", kingdoms_begin),
		(faction_set_slot, ":kingdom_b", ":truce_slot", 0),
		(faction_set_slot, ":kingdom_b", ":provocation_slot", 0),

        (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":kingdom_a", ":kingdom_b"),

        (call_script, "script_update_faction_notes", ":kingdom_a"),
        (call_script, "script_update_faction_notes", ":kingdom_b"),
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
	    (neg|check_quest_succeeded, "qst_cause_provocation"),
		(this_or_next|eq, "$players_kingdom", ":kingdom_a"),
			(eq, "$players_kingdom", ":kingdom_b"),
		(call_script, "script_abort_quest", "qst_cause_provocation", 0),
	  (try_end),
    ##diplomacy begin
    #check for defensive
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_a"),
			(ge, ":cur_relation", 0), #AT PEACE

      (store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "40" with a named constant
  		#(gt, ":truce_days", 40),
  		(gt, ":truce_days", dplmc_treaty_defense_days_expire),
  		##nested diplomacy end+
  		(try_begin),
  		  (lt, ":initializing_war_peace_cond", 2), #only if war was not caused by defensive or alliance pact
  		  (call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_a", 2),
  		(try_end),
    (try_end),

    #check for alliance
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (neq, ":cur_kingdom", ":kingdom_a"),
      (neq, ":cur_kingdom", ":kingdom_b"),

      (store_relation, ":cur_relation", ":cur_kingdom", ":kingdom_b"),
			(ge, ":cur_relation", 0), #AT PEACE

  		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
  		(val_sub, ":truce_slot", kingdoms_begin),
  		(faction_get_slot, ":truce_days", ":cur_kingdom", ":truce_slot"),
  		##nested diplomacy start+ replace "60" with a named constant
  		#(gt, ":truce_days", 60),
  		(gt, ":truce_days", dplmc_treaty_alliance_days_expire),
  		##nested diplomacy end+
  		(call_script, "script_diplomacy_start_war_between_kingdoms", ":cur_kingdom", ":kingdom_b", 3),
    (try_end),
    ##diplomacy end
  ]),


  #script_diplomacy_party_attacks_neutral
  ("diplomacy_party_attacks_neutral", #called from game_menus (plundering a village, raiding a village),  from dialogs: surprise attacking a neutral lord, any attack on caravan or villagers
#Has no effect if factions are already at war
    [
      (store_script_param, ":attacker_party", 1),
      (store_script_param, ":defender_party", 2),

	  (store_faction_of_party, ":attacker_faction", ":attacker_party"),
	  (store_faction_of_party, ":defender_faction", ":defender_party"),

	  (party_stack_get_troop_id, ":attacker_leader", ":attacker_party", 0),

	  (try_begin),
		(eq, ":attacker_party", "p_main_party"),
		(neq, ":attacker_faction", "fac_player_supporters_faction"),
		(assign, ":attacker_faction", "$players_kingdom"),
	  (else_try),
		(eq, ":attacker_party", "p_main_party"),
		(eq, ":attacker_faction", "fac_player_supporters_faction"),
	  (try_end),

	  (try_begin),
	    (eq, ":attacker_party", "p_main_party"),
		(store_relation, ":relation", ":attacker_faction", ":defender_faction"),
	    (ge, ":relation", 0),
		(call_script, "script_change_player_honor", -2),
	  (try_end),


	  (try_begin),
		(check_quest_active, "qst_cause_provocation"),
		(quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, ":defender_faction"),
		(quest_get_slot, ":giver_troop", "qst_cause_provocation", slot_quest_giver_troop),
		(store_faction_of_troop, ":attacker_faction", ":giver_troop"),
		(call_script, "script_succeed_quest", "qst_cause_provocation"),
	  (try_end),

	  (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":attacker_faction", ":defender_faction"),
	  (assign, ":diplomatic_status", reg0),

	  (try_begin),
	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
		#player faction inactive, no effect
	  (else_try),
		(eq, ":diplomatic_status", -2),
	    #war, no effect
	  (else_try),

	    (eq, ":attacker_faction", "fac_player_supporters_faction"),
		(faction_slot_eq, ":attacker_faction", slot_faction_leader, "trp_player"),
		(call_script, "script_faction_follows_controversial_policy", "fac_player_supporters_faction",logent_policy_ruler_attacks_without_provocation),
	  (else_try),
		(eq, ":diplomatic_status", 1),
		#truce
		(party_stack_get_troop_id, ":defender_party_leader", ":defender_party", 0),
		(try_begin),
			##diplomacy start+ add support for promoted kingdom ladies
			#(i.e. verify not a promoted kingdom lady, since they exist)
			(this_or_next|neg|is_between, ":defender_party_leader", kingdom_ladies_begin, kingdom_ladies_end),
				(neg|troop_slot_eq, ":defender_party_leader", slot_troop_occupation, slto_kingdom_hero),
			##diplomacy end+
			(neg|is_between, ":defender_party_leader", active_npcs_begin, active_npcs_end),
			(store_faction_of_party, ":defender_party_faction", ":defender_party"),
			(faction_get_slot, ":defender_party_leader", ":defender_party_faction", slot_faction_leader),
		(try_end),

		(call_script, "script_add_log_entry", logent_border_incident_troop_breaks_truce, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (else_try),
		#truce
		(call_script, "script_add_log_entry", logent_border_incident_troop_attacks_neutral, ":attacker_leader", -1, ":defender_party_leader", ":attacker_faction"),
	  (try_end),

	  (try_begin),
	    (is_between, ":defender_party", villages_begin, villages_end),
	    (call_script, "script_add_log_entry", logent_village_raided, ":attacker_leader",  ":defender_party", -1, ":defender_faction"),
        #SB : add quest cancellation when raiding villages
        (try_begin),
          (eq, ":attacker_party", "p_main_party"),
          (party_get_slot, ":elder", ":defender_party", slot_town_elder),
          (gt, ":elder", 0),
          (try_for_range, ":quest_no", village_elder_quests_begin, village_elder_quests_end),
            (quest_slot_eq, ":quest_no", slot_quest_giver_troop, ":elder"),
            (call_script, "script_abort_quest", ":quest_no", 1),
          (try_end),
        (try_end),
	  (else_try),
	    (party_get_template_id, ":template", ":defender_party"),
	    # (neq, ":template", "pt_kingdom_hero_party"),
	    (eq, ":template", "pt_kingdom_caravan_party"), #SB: fix this to specifically apply to caravans
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_faction_name, s5, ":defender_faction"),
			(display_message, "@{!}Debug - {s5} caravan attacked"),
		(try_end),

	    (call_script, "script_add_log_entry", logent_caravan_accosted, ":attacker_leader",  -1, -1, ":defender_faction"),
	  (try_end),

	  (store_add, ":slot_truce_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_truce_days", kingdoms_begin),
	  (faction_set_slot, ":defender_faction", ":slot_truce_days", 0),

	  (store_add, ":slot_provocation_days", ":attacker_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  (try_begin),
	    (neq, ":diplomatic_status", -2),
		(faction_slot_eq, ":defender_faction", ":slot_provocation_days", 0),
		(faction_set_slot, ":defender_faction", ":slot_provocation_days", 30),
	  (try_end),
	]),

  # script_party_calculate_and_set_nearby_friend_enemy_follower_strengths
  # Input: party_no
  # Output: none
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

  # script_init_ai_calculation
  # Input: arg1 = kingdom_1, arg2 = kingdom_2, arg3 = initializing_war_peace_cond
  # Output: none
  ("diplomacy_start_peace_between_kingdoms", #sets relations between two kingdoms
    [
      (store_script_param, ":kingdom_a", 1),
      (store_script_param, ":kingdom_b", 2),
      (store_script_param, ":initializing_war_peace_cond", 3), #set to 1 if not the start of the game

      (store_relation, ":relation", ":kingdom_a", ":kingdom_b"),
      (val_max, ":relation", 0),
      (set_relation, ":kingdom_a", ":kingdom_b", ":relation"),
      (call_script, "script_exchange_prisoners_between_factions", ":kingdom_a", ":kingdom_b"),

      (try_begin),
        (eq, "$players_kingdom", ":kingdom_a"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_b"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_b", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", "fac_player_supporters_faction"), #event cancels certain quests
      (else_try),
        (eq, "$players_kingdom", ":kingdom_b"),
        (store_relation, ":relation", "fac_player_supporters_faction", ":kingdom_a"),
        (val_max, ":relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":kingdom_a", ":relation"),
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", "fac_player_supporters_faction"), #event cancels certain quests
      (try_end),

      (try_for_range, ":cur_center", centers_begin, centers_end),
        (store_faction_of_party, ":faction_no", ":cur_center"),
        (this_or_next|eq, ":faction_no", ":kingdom_a"),
        (eq, ":faction_no", ":kingdom_b"),
        (party_get_slot, ":besieger_party", ":cur_center", slot_center_is_besieged_by),
        (ge, ":besieger_party", 0), #town is under siege
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_party_faction_no", ":besieger_party"),
        (this_or_next|eq, ":besieger_party_faction_no", ":kingdom_a"),
        (eq, ":besieger_party_faction_no", ":kingdom_b"),
        (call_script, "script_lift_siege", ":cur_center", 0),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$players_kingdom", ":kingdom_a"),
        (eq, "$players_kingdom", ":kingdom_b"),

        (ge, "$g_player_besiege_town", 0),
        (party_is_active, "$g_player_besiege_town"),

        (store_faction_of_party, ":besieged_center_faction_no", "$g_player_besiege_town"),

        (this_or_next|eq, ":besieged_center_faction_no", ":kingdom_a"),
        (eq, ":besieged_center_faction_no", ":kingdom_b"),

        (call_script, "script_lift_siege", "$g_player_besiege_town", 0),
        (assign, "$g_player_besiege_town", -1),
      (try_end),

      (try_begin),
        (eq, ":initializing_war_peace_cond", 1),
        (str_store_faction_name_link, s1, ":kingdom_a"),
        (str_store_faction_name_link, s2, ":kingdom_b"),
        (display_log_message, "@{s1} and {s2} have made peace with each other.", message_alert),
        (call_script, "script_add_notification_menu", "mnu_notification_peace_declared", ":kingdom_a", ":kingdom_b"), #stability penalty for early peace is in the menu
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_a", ":kingdom_b"), #cancels quests
        (call_script, "script_event_kingdom_make_peace_with_kingdom", ":kingdom_b", ":kingdom_a"), #cancels quests
        (assign, "$g_recalculate_ais", 1),
      (try_end),

	  (try_begin), #add truce
		(store_add, ":truce_slot", ":kingdom_a", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
		##diplomacy begin
	    #(faction_set_slot, ":kingdom_b", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
#        (faction_set_slot, ":kingdom_b", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_b", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
	    ##diplomacy end
		(store_add, ":truce_slot", ":kingdom_b", slot_faction_truce_days_with_factions_begin),
		(val_sub, ":truce_slot", kingdoms_begin),
	    ##diplomacy begin
	    #(faction_set_slot, ":kingdom_a", ":truce_slot", 40),
        ##nested diplomacy start+ replace "20" with constant for truce length
        #(faction_set_slot, ":kingdom_a", ":truce_slot", 20),
        (faction_set_slot, ":kingdom_a", ":truce_slot", dplmc_treaty_truce_days_initial),
        ##nested diplomacy end+
        ##diplomacy end
		(store_add, ":slot_war_damage_inflicted_on_b", ":kingdom_b", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_b", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_a", ":kingdom_a", ":slot_war_damage_inflicted_on_b"),
		(faction_set_slot, ":kingdom_a", ":slot_war_damage_inflicted_on_b", 0),
		(store_add, ":slot_war_damage_inflicted_on_a", ":kingdom_a", slot_faction_war_damage_inflicted_on_factions_begin),
		(val_sub, ":slot_war_damage_inflicted_on_a", kingdoms_begin),
		#(faction_get_slot, ":damage_inflicted_by_b", ":kingdom_b", ":slot_war_damage_inflicted_on_a"),
		(faction_set_slot, ":kingdom_b", ":slot_war_damage_inflicted_on_a", 0),
	  (try_end),
  ]),



  ("event_kingdom_make_peace_with_kingdom",
    [
      (store_script_param_1, ":source_kingdom"),
      (store_script_param_2, ":target_kingdom"),
      (try_begin),
        (check_quest_active, "qst_capture_prisoners"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_prisoners", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_prisoners"),
        (try_end),
      (try_end),

      (try_begin),
        (check_quest_active, "qst_capture_enemy_hero"),
        (try_begin),
          (eq, "$players_kingdom", ":source_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":target_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (else_try),
          (eq, "$players_kingdom", ":target_kingdom"),
          (quest_slot_eq, "qst_capture_enemy_hero", slot_quest_target_faction, ":source_kingdom"),
          (call_script, "script_cancel_quest", "qst_capture_enemy_hero"),
        (try_end),
      (try_end),



      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (quest_get_slot, ":lord_1", "qst_persuade_lords_to_make_peace", slot_quest_target_troop),
        (quest_get_slot, ":lord_2", "qst_persuade_lords_to_make_peace", slot_quest_object_troop),

        (try_begin),
            (lt, ":lord_1", 0),
            (val_mul, ":lord_1", -1),
        (try_end),
        (try_begin),
            (lt, ":lord_2", 0),
            (val_mul, ":lord_2", -1),
        (try_end),


        (store_faction_of_troop, ":lord_1_faction", ":lord_1"),
        (store_faction_of_troop, ":lord_2_faction", ":lord_2"),

        (this_or_next|eq, ":lord_1_faction", ":source_kingdom"),
            (eq, ":lord_2_faction", ":source_kingdom"),

        (this_or_next|eq, ":lord_1_faction", ":target_kingdom"),
            (eq, ":lord_2_faction", ":target_kingdom"),

        (call_script, "script_cancel_quest", "qst_persuade_lords_to_make_peace"),

      (try_end),

      #Rescue prisoners cancelled in simple_triggers

      (try_begin),
        #SB : better checking, also adds rtr for co-ruler
        (this_or_next|eq, "$players_kingdom", ":source_kingdom"),
        (eq, "$players_kingdom", ":target_kingdom"),
        (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
        (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (call_script, "script_change_player_right_to_rule", 3),
      (try_end),

  ]),

  # script_randomly_start_war_peace
  # Input: arg1 = menu_no, arg2 = menu_var_1, arg3 = menu_var_2
  # Output: none
  ("add_notification_menu",
    [
      (try_begin),
        (eq, "$g_infinite_camping", 0),
        (store_script_param, ":menu_no", 1),
        (store_script_param, ":menu_var_1", 2),
        (store_script_param, ":menu_var_2", 3),
        (assign, ":end_cond", 1),
        (try_for_range, ":cur_slot", 0, ":end_cond"),
          (try_begin),
            (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
            (val_add, ":end_cond", 1),
          (else_try),
            (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
            (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
            (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
          (try_end),
        (try_end),
      (try_end),
      ]),

  # script_finish_quest
  # Input: arg1 = troop_no, arg2 = time (0 if present tense, 1 if past tense)
  # Output: s1 = String, reg0 = knows-or-not
  ("get_information_about_troops_position",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, reg3),
	  ##diplomacy start+
	  #(troop_get_type, reg4, ":troop_no"),
     (call_script, "script_dplmc_store_troop_is_female_reg", ":troop_no", 4),
	  ##diplomacy end+
      (str_store_troop_name, s2, ":troop_no"),

      (assign, ":found", 0),
      (troop_get_slot, ":center_no", ":troop_no", slot_troop_cur_center),
      (try_begin),
        (gt, ":center_no", 0),
        (is_between, ":center_no", centers_begin, centers_end),
        (str_store_party_name_link, s3, ":center_no"),
        (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
        (assign, ":found", 1),
      (else_try),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (gt, ":party_no", 0),
        (call_script, "script_get_troop_attached_party", ":troop_no"),
        (assign, ":center_no", reg0),
        (try_begin),
          (is_between, ":center_no", centers_begin, centers_end),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is currently} at {s3}."),
          (assign, ":found", 1),
        (else_try),
          (get_party_ai_behavior, ":ai_behavior", ":party_no"),
          (eq, ":ai_behavior", ai_bhvr_travel_to_party),
          (get_party_ai_object, ":ai_object", ":party_no"),
          (is_between, ":ai_object", centers_begin, centers_end),
		  ##diplomacy start+
		  #(call_script, "script_get_closest_center", ":party_no"),
		  (call_script, "script_dplmc_get_closest_center_or_two", ":party_no"),
		  ##diplomacy end+
          (str_store_party_name_link, s4, reg0),
          (str_store_party_name_link, s3, ":ai_object"),
          (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} close to {s4}{reg3?: at the moment}."),
          (assign, ":found", 1),
		  ##diplomacy start+
		  (try_begin),
		     (gt, reg1, -1),
			 (str_store_party_name_link, s1, reg1),
			 (str_store_string, s1, "@{s2} {reg3?was:is} travelling to {s3} and {reg4?she:he} {reg3?was:should be} between {s4} and {s1}{reg3?: at the moment}."),
		  (try_end),
		  ##diplomacy end+
        (else_try),
		  ##diplomacy start+
		  #(call_script, "script_get_closest_center", ":party_no"),
		  (call_script, "script_dplmc_get_closest_center_or_two", ":party_no"),
		  ##diplomacy end+
          (str_store_party_name_link, s3, reg0),
          (str_store_string, s1, "@{s2} {reg3?was:is} in the field and {reg4?she:he} {reg3?was:should be} close to {s3}{reg3?: at the moment}."),
          (assign, ":found", 1),
		  ##diplomacy start+
		  (try_begin),
		     (gt, reg1, -1),
			 (str_store_party_name_link, s1, reg1),
			 (str_store_string, s1, "@{s2} {reg3?was:is} in the field and {reg4?she:he} {reg3?was:should be} between {s3} and {s1}{reg3?: at the moment}."),
		  (try_end),
		  ##diplomacy end+
        (try_end),
      (else_try),
        #(troop_slot_ge, ":troop_no", slot_troop_is_prisoner, 1),
        (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
          (party_count_prisoners_of_type, ":num_prisoners", ":center_no", ":troop_no"),
          (gt, ":num_prisoners", 0),
          (assign, ":found", 1),
          (str_store_party_name_link, s3, ":center_no"),
          (str_store_string, s1, "@{s2} {reg3?was:is} being held captive at {s3}."),
        (try_end),
        (try_begin),
          (eq, ":found", 0),
          (str_store_string, s1, "@{s2} {reg3?was:has been} taken captive by {reg4?her:his} enemies."),
          (assign, ":found", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":found", 0),
        (str_store_string, s1, "@{reg3?{s2}'s location was unknown:I don't know where {s2} is}."),
      (try_end),
      (assign, reg0, ":found"),
  ]),

  # script_recruit_troop_as_companion
  # Input: arg1 = center_no, arg2 = mission_template_no
  # Output: none
  ("setup_random_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_random_scene"),
      (try_begin),
        (eq, ":terrain_type", rt_steppe),
        (assign, ":scene_to_use", "scn_random_scene_steppe"),
      (else_try),
        (eq, ":terrain_type", rt_plain),
        (assign, ":scene_to_use", "scn_random_scene_plain"),
      (else_try),
        (eq, ":terrain_type", rt_snow),
        (assign, ":scene_to_use", "scn_random_scene_snow"),
      (else_try),
        (eq, ":terrain_type", rt_desert),
        (assign, ":scene_to_use", "scn_random_scene_desert"),
      (else_try),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_random_scene_steppe_forest"),
      (else_try),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_random_scene_plain_forest"),
      (else_try),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_random_scene_snow_forest"),
      (else_try),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_random_scene_desert_forest"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water),
        (assign,  ":scene_to_use", "scn_sea_boarding_a_a"),

        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),

        (try_begin),
          (eq, "$g_joined_battle_to_help", 1),
          (party_get_slot, ":ship_type", "$g_ally_party", slot_party_ship_type),
        (try_end),

        (party_get_slot, ":enemy_ship_type", "$g_enemy_party", slot_party_ship_type),

        (assign, reg0, ":ship_type"),
        (assign, reg1, ":enemy_ship_type"),
        (display_message, "@our ship: {reg0}, enemy ship: {reg1}"),

        (try_begin),
          (eq, ":ship_type", 1),
          (assign, "$g_player_attacker", 1),
          (try_begin),
            (eq, ":enemy_ship_type", 1),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_a"),
          (else_try),
            (eq, ":enemy_ship_type", 2),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_b"),
          (else_try),
            (eq, ":enemy_ship_type", 3),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_c"),
          (else_try),
            (eq, ":enemy_ship_type", 4),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_d"),
          (try_end),
        (else_try),
          (eq,  ":ship_type", 2),
          (assign, "$g_player_attacker", 1),
          (try_begin),
            (eq, ":enemy_ship_type", 1),
            (assign, "$g_player_attacker", 0),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_b"),
          (else_try),
            (eq, ":enemy_ship_type", 2),
            (assign,  ":scene_to_use", "scn_sea_boarding_b_b"),
          (else_try),
            (eq, ":enemy_ship_type", 3),
            (assign,  ":scene_to_use", "scn_sea_boarding_b_c"),
          (else_try),
            (eq, ":enemy_ship_type", 4),
            (assign,  ":scene_to_use", "scn_sea_boarding_b_d"),
          (try_end),
        (else_try),
          (eq,  ":ship_type", 3),
          (assign, "$g_player_attacker", 1),
          (try_begin),
            (eq, ":enemy_ship_type", 1),
            (assign, "$g_player_attacker", 0),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_c"),
          (else_try),
            (eq, ":enemy_ship_type", 2),
            (assign, "$g_player_attacker", 0),
            (assign,  ":scene_to_use", "scn_sea_boarding_b_c"),
          (else_try),
            (eq, ":enemy_ship_type", 3),
            (assign,  ":scene_to_use", "scn_sea_boarding_c_c"),
          (else_try),
            (eq, ":enemy_ship_type", 4),
            (assign, "$g_player_attacker", 0), #
            (assign,  ":scene_to_use", "scn_sea_boarding_c_d"),
          (try_end),
        (else_try),
          (eq,  ":ship_type", 4),
          (assign, "$g_player_attacker", 0),
          (try_begin),
            (eq, ":enemy_ship_type", 1),
            (assign,  ":scene_to_use", "scn_sea_boarding_a_d"),
          (else_try),
            (eq, ":enemy_ship_type", 2),
            (assign,  ":scene_to_use", "scn_sea_boarding_b_d"),
          (else_try),
            (eq, ":enemy_ship_type", 3),
            (assign, "$g_player_attacker", 1), #
            (assign,  ":scene_to_use", "scn_sea_boarding_c_d"),
          (else_try),
            (eq, ":enemy_ship_type", 4),
            (assign, "$g_player_attacker", 1),
            (assign,  ":scene_to_use", "scn_sea_boarding_d_d"),
          (try_end),
        (try_end),

        (try_begin),
          (eq, "$g_joined_battle_to_help", 1),
          (set_jump_mission,"mt_ship_battle"),
        (else_try),
          (eq, "$g_player_attacker", 1),
          (set_jump_mission,"mt_ship_battle"),
        (else_try),
          (set_jump_mission,"mt_ship_battle_reversed"),
        (try_end),

       (try_for_range, ":entry_no", 0, 5),
         (mission_tpl_entry_set_override_flags, "mt_ship_battle", ":entry_no", af_override_horse),
         (mission_tpl_entry_set_override_flags, "mt_ship_battle_reversed", ":entry_no", af_override_horse),
       (try_end),
      (else_try),
        (eq, ":terrain_type", rt_bridge),
        (assign, ":scene_to_use", "scn_random_scene_plain"),
      (try_end),
      (jump_to_scene,":scene_to_use"),
  ]),

  # script_enter_dungeon
  # Input: arg1 = center_no
  # Output: none
  #other search term: setup_court
  ("enter_court",
    [
      (store_script_param_1, ":center_no"),

      (assign, "$talk_context", tc_court_talk),

      (set_jump_mission,"mt_visit_town_castle"),

      (mission_tpl_entry_clear_override_items, "mt_visit_town_castle", 0),
      #(mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_all),

      (mission_tpl_entry_set_override_flags, "mt_visit_town_castle", 0, af_override_all),
      (assign, ":dest_cloth", "itm_tabard"),
      (assign, ":have_civilian_cloth", 0),
      (assign, ":equipped_body_is_civilian", 0),
      (troop_get_inventory_slot, ":equipped_body", "trp_player", ek_body),
      (try_begin),
        (ge, ":equipped_body", 0),
        (item_has_property, ":equipped_body", itp_civilian),
        (assign, ":dest_cloth", ":equipped_body"),
        (assign, ":have_civilian_cloth", 1),
        (assign, ":equipped_body_is_civilian", 1),
      (else_try),
        (troop_get_inventory_capacity, ":inv_size", "trp_player"),
        (assign, ":end_cond", ":inv_size"),
        (try_for_range, ":i_slot", ek_head, ":end_cond"),
          (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
          (ge, ":item_id", 0),
          (item_get_type, ":i_type", ":item_id"),
          (eq, ":i_type", itp_type_body_armor),
          (item_has_property, ":item_id", itp_civilian),
          (assign, ":dest_cloth", ":item_id"),
          (assign, ":have_civilian_cloth", 1),
          (assign, ":end_cond", 0),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":equipped_body_is_civilian", 1),
      (else_try),
        (eq, ":have_civilian_cloth", 1),
        (display_message, "@You have changed into casual clothes from your inventory."),
      (else_try),
        (display_message, "@You have no casual clothes, so the castle guard provides common clothes temporarily."),
      (try_end),
      (mission_tpl_entry_add_override_item, "mt_visit_town_castle", 0, ":dest_cloth"),

      (party_get_slot, ":castle_scene", ":center_no", slot_town_castle),
      (modify_visitors_at_site,":castle_scene"),
      (reset_visitors),
      #Adding guards
      (store_faction_of_party, ":center_faction", ":center_no"),
      ##diplomacy begin
      (try_begin),
         (eq, ":center_faction", "$players_kingdom"),
         (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
         (faction_get_slot, ":guard_troop", "$g_player_culture", slot_faction_guard_troop),
	  ##nested diplomacy start+
	  (else_try),
	     #Reflect multicultural empires.
		 (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
		 (gt, ":town_lord", "trp_player"),
		 (troop_get_slot, ":lord_original_faction", ":town_lord", slot_troop_original_faction),
		 (neq, ":lord_original_faction", ":center_faction"),
		 (is_between, ":lord_original_faction", npc_kingdoms_begin, npc_kingdoms_end),
		 (this_or_next|party_slot_eq, ":center_no", slot_center_original_faction, ":lord_original_faction"),
			(troop_slot_eq, ":town_lord", slot_troop_home, ":center_no"),
		 (faction_get_slot, ":guard_troop", ":lord_original_faction", slot_faction_guard_troop),
	  ##nested diplomacy end+
      (else_try),
        (faction_get_slot, ":guard_troop", ":center_faction", slot_faction_guard_troop),
      (try_end),
      ##diplomacy end
      (try_begin),
        (le, ":guard_troop", 0),
		#diplomacy start+
		#rubik changes this in Custom Commander, and I agree: the "generic" guard
		#should be non-faction-specific.
		##OLD:
        #(assign, ":guard_troop", "trp_swadian_sergeant"),
		##NEW:
		(assign, ":guard_troop", "trp_hired_blade"),
		##diplomacy end+
      (try_end),
      (set_visitor, 6, ":guard_troop"),
      (set_visitor, 7, ":guard_troop"),

      (assign, ":cur_pos", 16),

	  (try_begin),
		(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	    (gt, ":player_spouse", 0),
		(troop_slot_eq, ":player_spouse", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_spouse"),
        (val_add,":cur_pos", 1),
	  (else_try),
		(troop_get_slot, ":player_betrothed", "trp_player", slot_troop_betrothed),
	    (gt, ":player_betrothed", 0),
		(troop_slot_eq, ":player_betrothed", slot_troop_cur_center, ":center_no"),
        (set_visitor, ":cur_pos", ":player_betrothed"),
        (val_add,":cur_pos", 1),
	  (try_end),

	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
		(gt, "$g_player_minister", 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$g_player_minister"),
        (set_visitor, ":cur_pos", "$g_player_minister"),
        (val_add,":cur_pos", 1),
	  (try_end),
    ##diplomacy begin

    # (try_begin), #dckplmc seneschals
      # (call_script, "script_assign_seneschals"),
      # (party_get_slot, ":town_seneschal", ":center_no", slot_town_seneschal),
      # (gt, ":town_seneschal", -1),
      # (set_visitor, ":cur_pos", ":town_seneschal"),
      # (val_add,":cur_pos", 1),
    # (try_end),

    (try_begin),
      (gt, "$g_player_chamberlain", 0),
      (call_script, "script_dplmc_appoint_chamberlain"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chamberlain"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_constable", 0),
      (call_script, "script_dplmc_appoint_constable"),  #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_constable"),
      (val_add,":cur_pos", 1),
    (try_end),

    (try_begin),
      (gt, "$g_player_chancellor", 0),
      (call_script, "script_dplmc_appoint_chancellor"), #fix for wrong troops after update
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (eq, ":town_lord", "trp_player"),
      (set_visitor, ":cur_pos", "$g_player_chancellor"),
      (val_add,":cur_pos", 1),
    (try_end),
    ##diplomacy end

      #Lords wishing to pledge allegiance - inactive, but part of player faction
      #SB : move down to sorted script call
	  (try_begin),
		(eq, "$g_player_court", ":center_no"),
	    (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
	    (try_for_range, ":active_npc", heroes_begin, heroes_end), #support for upgraded kingdom ladies
	      (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
	      (eq, ":active_npc_faction", "fac_player_supporters_faction"),
	      (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_inactive),
	      (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she is not prisoner in any center.
	      (neq, ":active_npc", "$g_player_minister"),
	      (set_visitor, ":cur_pos", ":active_npc"),
	      (val_add,":cur_pos", 1),
		(try_end),
	  (try_end),

      ##diplomacy start+
      #Show heroes you haven't seen recently first, to deal with crowded feast halls
      #(call_script, "script_get_heroes_attached_to_center", ":center_no", "p_temp_party"),
      (call_script, "script_dplmc_time_sorted_heroes_for_center", ":center_no", "p_temp_party"),
	  #Reserve a certain number of feast positions for ladies, both for practical
	  #reasons of courtship and for visual variety.
	  (try_begin),
		#If the player is unmarried, reserve zero to 8 slots for women
		(lt, ":player_spouse", 1),
		(store_random_in_range, ":reserved", 0, 9),
	  (else_try),
		#If the player is married, reserve zero to four slots for women
		(store_random_in_range, ":reserved", 0, 5),
	  (try_end),
	  (store_sub, ":non_lady_max", 32, ":reserved"),
      #diplomacy end+
      (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),
		##diplomacy start+
        #(lt, ":cur_pos", 32), # spawn up to entry point 32 - is it possible to add another 10 spots?
		(lt, ":cur_pos", ":non_lady_max"),#Leave some room for ladies in huge feasts
		##diplomacy end+
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add,":cur_pos", 1),
      (try_end),
      (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
        (neq, ":cur_troop", "trp_knight_1_1_wife"), #The one who should not appear in game
        #(troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
        (troop_slot_eq, ":cur_troop", slot_troop_cur_center, ":center_no"),

        (assign, ":lady_meets_visitors", 0),
		(assign, ":tribute_entertainer", 0),
        (try_begin),
            (this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":cur_troop"), #player spouse goes in position of honor
            (troop_slot_eq, "trp_player", slot_troop_betrothed, ":cur_troop"), #player spouse goes in position of honor
            (assign, ":lady_meets_visitors", 0), #She is already in the place of honor
            (try_begin), #SB : primary spouse
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (display_message, "str_s4_is_present_at_the_center_and_in_place_of_honor"),
            (try_end),
        (else_try),
            (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_spouse, "trp_player"), #player spouse goes in position of honor
            (troop_slot_eq, ":cur_troop", slot_troop_betrothed, "trp_player"),
            (assign, ":lady_meets_visitors", 1),
            (try_begin), #SB : secondary spouse, normally shadowed due to above behaviour
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (display_message, "str_s4_is_present_at_the_center_and_is_married"),
            (try_end),
        (else_try), #lady is troop
            (store_faction_of_troop, ":lady_faction", ":cur_troop"),
            (neq, ":lady_faction", ":center_faction"),

            (assign, ":lady_meets_visitors", 1),


            (try_begin),
                (eq, "$cheat_mode", 1),
                (str_store_troop_name, s4, ":cur_troop"),
                (try_begin), #SB : distinguish between refugee and prisoner
                  (troop_slot_eq, ":cur_troop", slot_troop_prisoner_of_party, ":center_no"),
                  (display_message, "@{s4} is present at the center as a prisoner"),
				  #Prisoner Entertainer
				  (assign, ":lady_meets_visitors", 1),
                (else_try),
                  (display_message, "str_s4_is_present_at_the_center_as_a_refugee"),
                (try_end),
            (try_end),

        (else_try),
            (troop_slot_ge, ":cur_troop", slot_troop_spouse, 1),

            (try_begin),
             #married ladies at a feast will not mingle - this is ahistorical, as married women and widows probably had much more freedom than unmarried ones, at least in the West, but the game needs to leave slots for them to show off their unmarried daughters
                (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
                (faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
                (assign, ":lady_meets_visitors", 0),

                (try_begin),
                    (eq, "$cheat_mode", 1),
                    (str_store_troop_name, s4, ":cur_troop"),
                    (display_message, "str_s4_is_present_at_the_center_and_not_attending_the_feast"),
                (try_end),
            (else_try),
                (assign, ":lady_meets_visitors", 1),

                (try_begin),
                    (eq, "$cheat_mode", 1),
                    (str_store_troop_name, s4, ":cur_troop"),
                    (display_message, "str_s4_is_present_at_the_center_and_is_married"),
                (try_end),
            (try_end),

		(else_try), #feast is in progress
			(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, ":center_faction", slot_faction_ai_object, ":center_no"),
			(assign, ":lady_meets_visitors", 1),

			(try_begin),
				(store_random_in_range,":r",1,8),
				(eq,":r", 3),
				(assign, ":tribute_entertainer", 1),
			(try_end),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is attending the feast"),
			(try_end),

		(else_try), #already met - awaits in private
			(troop_slot_ge, ":cur_troop", slot_troop_met, 2),
			(assign, ":lady_meets_visitors", 0),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is present at the center and is awaiting the player in private"),
			(try_end),

		(else_try),
			(call_script, "script_get_kingdom_lady_social_determinants", ":cur_troop"),
			(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", reg0, "trp_player"),
			(gt, reg0, 0),
			(assign, ":lady_meets_visitors", 1),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4} is_present_at_the_center_and_is_allowed_to_meet_the_player"),
			(try_end),

		(else_try),
			(try_begin),
				(eq, "$cheat_mode", 1),
				(str_store_troop_name, s4, ":cur_troop"),
				(display_message, "@{!}DEBUG -- {s4}is_present_at_the_center_and_is_not_allowed_to_meet_the_player"),
			(try_end),

		(try_end),

		(eq, ":lady_meets_visitors", 1),

		(try_begin),
			(eq, ":tribute_entertainer", 1),
			(try_begin),
				(eq, "$tep_entertainer1", 69),
				(assign, "$tep_entertainer1", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer2", 69),
				(assign, "$tep_entertainer2", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer3", 69),
				(assign, "$tep_entertainer3", ":cur_troop"),
			(else_try),
				(eq, "$tep_entertainer4", 69),
				(assign, "$tep_entertainer4", ":cur_troop"),
			(else_try),
				(assign, ":tribute_entertainer", 0),
		(try_end),
			#(troop_set_slot, ":cur_troop", slot_troop_entertainer, 1), Now used for permanently abused ladies
		(try_end),

        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":cur_troop"),
        (val_add,":cur_pos", 1),
      (try_end),

      (set_jump_entry, 0),

      (jump_to_scene,":castle_scene"),
      (scene_set_slot, ":castle_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),


     # Input: pos1 should hold center_position_no
  #        arg1: team_no
  #        arg2: search_radius (in meters)
  # Output: pos52 contains highest ground within <search_radius> meters of team leader
  # Destroys position registers: pos10, pos11, pos15
  ("find_high_ground_around_pos1",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":search_radius", 2),
      (val_mul, ":search_radius", 100),
      (get_scene_boundaries, pos10,pos11),
      (team_get_leader, ":ai_leader", ":team_no"),
      (agent_get_position, pos1, ":ai_leader"),
      (set_fixed_point_multiplier, 100),
      (position_get_x, ":o_x", pos1),
      (position_get_y, ":o_y", pos1),
      (store_sub, ":min_x", ":o_x", ":search_radius"),
      (store_sub, ":min_y", ":o_y", ":search_radius"),
      (store_add, ":max_x", ":o_x", ":search_radius"),
      (store_add, ":max_y", ":o_y", ":search_radius"),
      (position_get_x, ":scene_min_x", pos10),
      (position_get_x, ":scene_max_x", pos11),
      (position_get_y, ":scene_min_y", pos10),
      (position_get_y, ":scene_max_y", pos11),
      #do not find positions close to borders (20 m)
      (val_add, ":scene_min_x", 2000),
      (val_sub, ":scene_max_x", 2000),
      (val_add, ":scene_min_y", 2000),
      (val_sub, ":scene_max_y", 2000),
      (val_max, ":min_x", ":scene_min_x"),
      (val_max, ":min_y", ":scene_min_y"),
      (val_min, ":max_x", ":scene_max_x"),
      (val_min, ":max_y", ":scene_max_y"),

      (store_div, ":min_x_meters", ":min_x", 100),
      (store_div, ":min_y_meters", ":min_y", 100),
      (store_div, ":max_x_meters", ":max_x", 100),
      (store_div, ":max_y_meters", ":max_y", 100),

      (assign, ":highest_pos_z", -10000),
      (copy_position, pos52, pos1),
      (init_position, pos15),

      (try_for_range, ":i_x", ":min_x_meters", ":max_x_meters"),
        (store_mul, ":i_x_cm", ":i_x", 100),
        (try_for_range, ":i_y", ":min_y_meters", ":max_y_meters"),
          (store_mul, ":i_y_cm", ":i_y", 100),
          (position_set_x, pos15, ":i_x_cm"),
          (position_set_y, pos15, ":i_y_cm"),
          (position_set_z, pos15, 10000),
          (position_set_z_to_ground_level, pos15),
          (position_get_z, ":cur_pos_z", pos15),
          (try_begin),
            (gt, ":cur_pos_z", ":highest_pos_z"),
            (copy_position, pos52, pos15),
            (assign, ":highest_pos_z", ":cur_pos_z"),
          (try_end),
        (try_end),
      (try_end),
  ]),

  # script_select_battle_tactic
  # Input: none
  # Output: ally_power, enemy_power
  ("calculate_team_powers",
     [
       (store_script_param, ":agent_no", 1),

       (try_begin),
         (assign, ":agent_side", 0),
         (agent_is_ally, ":agent_no"),
         (assign, ":agent_side", 1),
       (try_end),

       (assign, ":ally_power", 0),
       (assign, ":enemy_power", 0),

       (try_for_agents, ":cur_agent"),
         (agent_is_human, ":cur_agent"),
         (agent_is_alive, ":cur_agent"),

         (try_begin),
           (assign, ":agent_side_cur", 0),
           (agent_is_ally, ":cur_agent"),
           (assign, ":agent_side_cur", 1),
         (try_end),

         (try_begin),
           (agent_get_horse, ":agent_horse_id", ":cur_agent"),
           (neq, ":agent_horse_id", -1),
           (assign, ":agent_power", 2), #if this agent is horseman then his power effect is 2
         (else_try),
           (assign, ":agent_power", 1), #if this agent is walker then his power effect is 1
         (try_end),

         (try_begin),
           (eq, ":agent_side", ":agent_side_cur"),
           (val_add, ":ally_power", ":agent_power"),
         (else_try),
           (val_add, ":enemy_power", ":agent_power"),
         (try_end),
       (try_end),

       (assign, reg0, ":ally_power"),
       (assign, reg1, ":enemy_power"),
  ]), #ozan

#jacobhinds Morale Code END

#jacobhinds Morale Code BEGIN
#(Native version)

  # script_decide_run_away_or_not
  # Input: none
  # Output: none
  ("decide_run_away_or_not",
    [
      (store_script_param, ":cur_agent", 1),
      (store_script_param, ":mission_time", 2),



      (assign, ":force_retreat", 0),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (agent_get_division, ":agent_division", ":cur_agent"),
      (try_begin),
        (lt, ":agent_division", 9), #static classes
        (team_get_movement_order, ":agent_movement_order", ":agent_team", ":agent_division"),
        (eq, ":agent_movement_order", mordr_retreat),
        (assign, ":force_retreat", 1),
      (try_end),

      (agent_get_slot, ":is_cur_agent_running_away", ":cur_agent", slot_agent_is_running_away),
      (try_begin),
		#(neg|agent_slot_eq, ":cur_agent", slot_agent_courage_score_bonus, -1),
        (eq, ":is_cur_agent_running_away", 0),
        (try_begin),
          (eq, ":force_retreat", 1),
          (agent_clear_scripted_mode, ":cur_agent"),	#handle scripted mode troops - motomataru
          (agent_start_running_away, ":cur_agent"),
		  #(call_script, "script_agent_remove_from_square", ":cur_agent"), #jacobhinds infantry square script (remove if you don't have the infantry square script)
          (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
		  #(agent_set_speed_limit, ":cur_agent", 60),
        (else_try),
          (ge, ":mission_time", 4), #first 4 seconds anyone does not run away whatever happens.
          (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
          (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
          (val_mul, ":agent_hit_points", 10), #was 4
         # (try_begin),
          #  (agent_is_ally, ":cur_agent"),
           # (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
         # (try_end),

#	IGNORE THIS, just rambling from several workarounds ago BEGIN

#	ratio
#	assume major battle 100(enemy) vs 100(ally)
#	20/100 = 0.2 = nigh unbreakable (for now give no negative effects)
#	100/20 = 5	= rout
#	battle ratio * 100
#	potential swing from 0-1000 courage score malus before rout
#	perhaps link to battle ai....? or unbalanced?

#	IGNORE THIS, just rambling from several workarounds ago END

		  (try_begin),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(agent_is_ally, ":cur_agent"),
			(val_add, ":agent_hit_points", "$battle_ratio"),
		  (else_try),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(val_sub, ":agent_hit_points", "$battle_ratio"),
		  (try_end),

          #(val_mul, ":agent_hit_points", 10),
          (store_sub, ":start_running_away_courage_score_limit", 1500, ":agent_hit_points"), #was 3500
          #(assign, reg11, ":agent_courage_score"),
          #(assign, reg12, ":start_running_away_courage_score_limit"),
          #(display_message, "@courage: {reg11}, limit: {reg12}"),
          (lt, ":agent_courage_score", ":start_running_away_courage_score_limit"), #if (courage score < 3500 - (agent hit points * 40)) and (agent is not running away) then start running away, average hit points : 50, average running away limit = 1500

          (agent_get_troop_id, ":troop_id", ":cur_agent"), #for now do not let heroes to run away from battle
          (neg|troop_is_hero, ":troop_id"),

		  # (try_begin), #this block is optional, delete if you don't have diplomacy or if you don't want retreating voices.
			  # (call_script, "script_dplmc_store_troop_is_female", ":troop_id"), #shout "retreat" if male
			  # (neq, reg0, 1),
			  # #(agent_play_sound, ":cur_agent", "snd_man_retreat"), #uncomment if you want retreating voices
		  # (try_end),

          (agent_clear_scripted_mode, ":cur_agent"),	#handle scripted mode troops - motomataru
          (agent_start_running_away, ":cur_agent"),
		  #(call_script, "script_agent_remove_from_square", ":cur_agent"), #jacobhinds infantry square script (remove if you don't have the infantry square script)
		  #(agent_set_speed_limit, ":cur_agent", 60),
          (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
          #(display_message, "@AGENT HAS STARTED RUNNING"),
        (try_end),


      (else_try),
		#(neg|agent_slot_eq, ":cur_agent", slot_agent_courage_score_bonus, -1),
        (neq, ":force_retreat", 1),
        (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
        (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        (val_mul, ":agent_hit_points", 10), #was 4
   #     (try_begin),
    #      (agent_is_ally, ":cur_agent"),
     #     (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
      #  (try_end),

		  (try_begin),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(agent_is_ally, ":cur_agent"),
			(val_add, ":agent_hit_points", "$battle_ratio"),
		  (else_try),
			(call_script, "script_cf_agent_can_rout", ":cur_agent"),
			(val_sub, ":agent_hit_points", "$battle_ratio"),
		  (try_end),

        #(val_mul, ":agent_hit_points", 10),
        (store_sub, ":stop_running_away_courage_score_limit", 1800, ":agent_hit_points"),#what

        #(assign, reg11, ":agent_courage_score"),
        #(assign, reg12, ":start_running_away_courage_score_limit"),
        #(display_message, "@courage: {reg11}, limit: {reg12}"),

        (ge, ":agent_courage_score", ":stop_running_away_courage_score_limit"), #if (courage score > 3700 - agent hit points) and (agent is running away) then stop running away, average hit points : 50, average running away limit = 1700
        (agent_stop_running_away, ":cur_agent"),
        (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0),
        #(display_message, "@AGENT HAS STOPPED RUNNING"),
      (try_end),
  ]), #ozan
##  # Input: none
##  # Output: none
##  ("siege_defender_tactic_apply",
##    [
##      (try_begin),
##        (eq, "$defender_team", 1),
##        (ge, "$belfry_positioned", 2),
##
##        (assign, ":enemy_too_weak", 0),
##        (try_begin),
##          (ge, "$attacker_reinforcement_stage", 2),
##          (call_script, "script_calculate_team_strength", "$defender_team"),
##          (assign, ":defender_strength", reg0),
##          (call_script, "script_calculate_team_strength", "$attacker_team"),
##          (assign, ":attacker_strength", reg0),
##          (store_mul, ":attacker_strength_multiplied", ":attacker_strength", 2),
##          (ge, ":defender_strength", ":attacker_strength_multiplied"),
##          (assign, ":enemy_too_weak", 1),
##        (try_end),
##
##        (try_begin),
##          (eq, ":enemy_too_weak", 1),
##          (neq, "$ai_battle_tactic", btactic_charge),
##          (assign, "$ai_battle_tactic", btactic_charge),
##          (team_give_order, "$defender_team", grc_infantry, mordr_charge),
##        (else_try),
##          (neq, "$ai_battle_tactic", btactic_charge),
##          (neq, "$ai_battle_tactic", btactic_hold),
##          (assign, "$ai_battle_tactic", btactic_hold),
##          (team_give_order, "$defender_team", grc_infantry, mordr_hold),
##          (team_give_order, "$defender_team", grc_heroes, mordr_hold),
##          (entry_point_get_position,pos1,10),
##          (team_set_order_position, "$defender_team", grc_infantry, pos1),
##          (team_set_order_position, "$defender_team", grc_heroes, pos1),
##        (try_end),
##      (try_end),
##  ]),


  # script_team_get_class_percentages
  # Input: arg1: team_no, arg2: try for team's enemies
  # Output: reg0: percentage infantry, reg1: percentage archers, reg2: percentage cavalry
  ("team_get_class_percentages",
    [
      (assign, ":num_infantry", 0),
      (assign, ":num_archers", 0),
      (assign, ":num_cavalry", 0),
      (assign, ":num_total", 0),
      (store_script_param, ":team_no", 1),
      (store_script_param, ":negate", 2),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (assign, ":continue", 0),
        (try_begin),
          (eq, ":negate", 1),
          (teams_are_enemies, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (else_try),
          (eq, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (val_add, ":num_total", 1),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (try_begin),
          (eq, ":agent_class", grc_infantry),
          (val_add,  ":num_infantry", 1),
        (else_try),
          (eq, ":agent_class", grc_archers),
          (val_add,  ":num_archers", 1),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (val_add,  ":num_cavalry", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq,  ":num_total", 0),
        (assign,  ":num_total", 1),
      (try_end),
      (store_mul, ":perc_infantry",":num_infantry",100),
      (val_div, ":perc_infantry",":num_total"),
      (store_mul, ":perc_archers",":num_archers",100),
      (val_div, ":perc_archers",":num_total"),
      (store_mul, ":perc_cavalry",":num_cavalry",100),
      (val_div, ":perc_cavalry",":num_total"),
      (assign, reg0, ":perc_infantry"),
      (assign, reg1, ":perc_archers"),
      (assign, reg2, ":perc_cavalry"),
  ]),

  # script_get_closest3_distance_of_enemies_at_pos1
  # Input: arg1: team_no, pos1
  # Output: reg0: distance in cms.
  ("get_closest3_distance_of_enemies_at_pos1",
    [
      (assign, ":min_distance_1", 100000),
      (assign, ":min_distance_2", 100000),
      (assign, ":min_distance_3", 100000),

      (store_script_param, ":team_no", 1),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (teams_are_enemies, ":agent_team", ":team_no"),

        (agent_get_position, pos2, ":cur_agent"),
        (get_distance_between_positions,":cur_dist",pos2,pos1),
        (try_begin),
          (lt, ":cur_dist", ":min_distance_1"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":min_distance_1"),
          (assign, ":min_distance_1", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_2"),
          (assign, ":min_distance_3", ":min_distance_2"),
          (assign, ":min_distance_2", ":cur_dist"),
        (else_try),
          (lt, ":cur_dist", ":min_distance_3"),
          (assign, ":min_distance_3", ":cur_dist"),
        (try_end),
      (try_end),

      (assign, ":total_distance", 0),
      (assign, ":total_count", 0),
      (try_begin),
        (lt, ":min_distance_1", 100000),
        (val_add, ":total_distance", ":min_distance_1"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_2", 100000),
        (val_add, ":total_distance", ":min_distance_2"),
        (val_add, ":total_count", 1),
      (try_end),
      (try_begin),
        (lt, ":min_distance_3", 100000),
        (val_add, ":total_distance", ":min_distance_3"),
        (val_add, ":total_count", 1),
      (try_end),
      (assign, ":average_distance", 100000),
      (try_begin),
        (gt, ":total_count", 0),
        (store_div, ":average_distance", ":total_distance", ":total_count"),
      (try_end),
      (assign, reg0, ":average_distance"),
      (assign, reg1, ":min_distance_1"),
      (assign, reg2, ":min_distance_2"),
      (assign, reg3, ":min_distance_3"),
  ]),

  # script_team_get_average_position_of_enemies
  # Input: arg1: team_no,
  # Output: pos0: average position.
  ("team_get_average_position_of_enemies",
    [
      (store_script_param_1, ":team_no"),
      (init_position, pos0),
      (assign, ":num_enemies", 0),
      (assign, ":accum_x", 0),
      (assign, ":accum_y", 0),
      (assign, ":accum_z", 0),
      (try_for_agents,":enemy_agent"),
        (agent_is_alive, ":enemy_agent"),
        (agent_is_human, ":enemy_agent"),
        (agent_get_team, ":enemy_team", ":enemy_agent"),
        (teams_are_enemies, ":team_no", ":enemy_team"),

        (agent_get_position, pos62, ":enemy_agent"),

        (position_get_x, ":x", pos62),
        (position_get_y, ":y", pos62),
        (position_get_z, ":z", pos62),

        (val_add, ":accum_x", ":x"),
        (val_add, ":accum_y", ":y"),
        (val_add, ":accum_z", ":z"),
        (val_add, ":num_enemies", 1),
      (try_end),

      (try_begin), #to avoid division by zeros at below division part.
        (le, ":num_enemies", 0),
        (assign, ":num_enemies", 1),
      (try_end),

      (store_div, ":average_x", ":accum_x", ":num_enemies"),
      (store_div, ":average_y", ":accum_y", ":num_enemies"),
      (store_div, ":average_z", ":accum_z", ":num_enemies"),

      (position_set_x, pos0, ":average_x"),
      (position_set_y, pos0, ":average_y"),
      (position_set_z, pos0, ":average_z"),

      (assign, reg0, ":num_enemies"),
  ]),


  # script_search_troop_prisoner_of_party
  # Input: arg1 = troop_no
  # Output: reg0 = party_no (-1 if troop is not a prisoner.)
  ("search_troop_prisoner_of_party",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":prisoner_of", -1),
      (try_for_parties, ":party_no"),
        (eq,  ":prisoner_of", -1),
        (this_or_next|eq, ":party_no", "p_main_party"),
        (ge, ":party_no", centers_begin),
        (party_count_prisoners_of_type, ":troop_found", ":party_no", ":troop_no"),
        (gt, ":troop_found", 0),
        (assign, ":prisoner_of", ":party_no"),
      (try_end),
      (assign, reg0, ":prisoner_of"),
  ]),


##  # script_clear_last_quest
##  # Input: arg1 = troop_no
##  # Output: none
##  ("clear_last_quest",
##    [
##      (store_script_param_1, ":troop_no"),
##
##      (troop_set_slot, ":troop_no",slot_troop_last_quest, 0),
##      (troop_set_slot, ":troop_no",slot_troop_last_quest_betrayed, 0)
##  ]),



  # script_change_debt_to_troop
  # Input: arg1 = troop_no, arg2 = new debt amount
  # Output: none
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




  # script_abort_quest
##  # Input: arg1 = center_no, arg2 = old_faction_no
##  # Output: none
##  ("event_center_captured",
##    [
##      #      (store_script_param_1, ":center_no"),
##      #       (store_script_param_2, ":old_faction_no"),
##      #       (store_faction_of_party, ":faction_no"),
##
##      (try_begin),
##        (check_quest_active, "qst_deliver_message"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_escort_lady"),
##        (quest_slot_eq, "qst_escort_lady", slot_quest_target_center, ":center_no"),
##        (call_script, "script_abort_quest", "qst_escort_lady"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_rescue_lady_under_siege"),
##        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_target_center, ":center_no"),
##        (quest_slot_eq, "qst_rescue_lady_under_siege", slot_quest_current_state, 0),
##        (call_script, "script_abort_quest", "qst_rescue_lady_under_siege", 1),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_lover"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_enemy_lord"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_prisoners_to_enemy"),
##        (quest_slot_eq, "qst_bring_prisoners_to_enemy", slot_quest_target_center, ":center_no"),
##        (neg|check_quest_succeeded, "qst_bring_prisoners_to_enemy"),
##        (call_script, "script_abort_quest", "qst_bring_prisoners_to_enemy"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_reinforcements_to_siege"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_supply_to_center_under_siege"),
##        (quest_slot_eq, "qst_deliver_supply_to_center_under_siege", slot_quest_target_center, ":center_no"),
##        (call_script, "script_abort_quest", "qst_deliver_supply_to_center_under_siege", 1),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_raise_troops"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_messenger"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_back_deserters"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_kill_local_merchant"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_bring_back_runaway_serfs"),
##        (quest_slot_eq, "qst_bring_back_runaway_serfs", slot_quest_object_center, ":center_no"),
##        (neg|check_quest_succeeded, "qst_bring_back_runaway_serfs"),
##        (neg|check_quest_failed, "qst_bring_back_runaway_serfs"),
##        (call_script, "script_abort_quest", "qst_bring_back_runaway_serfs"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_follow_spy"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_enemy_hero"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_lend_companion"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_conspirators"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_defend_nobles_against_peasants"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_incriminate_loyal_commander"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_hunt_down_raiders"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_capture_prisoners"),
##      (try_end),
##      #Enemy lord quests
##      (try_begin),
##        (check_quest_active, "qst_lend_surgeon"),
##      (try_end),
##      #Kingdom lady quests
##      (try_begin),
##        (check_quest_active, "qst_rescue_lord_by_replace"),
##        (quest_get_slot, ":quest_target_troop", "qst_rescue_lord_by_replace", slot_quest_target_troop),
##        (troop_slot_eq, ":quest_target_troop", slot_troop_is_prisoner, 0),
##        (neg|check_quest_succeeded, "qst_rescue_lord_by_replace"),
##        (call_script, "script_abort_quest", "qst_rescue_lord_by_replace"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
##      (try_end),
##      (try_begin),
##        (check_quest_active, "qst_duel_for_lady"),
##      (try_end),
##  ]),

  # script_cf_is_quest_troop
  # Input: arg1 = troop_no
  # Output: none (can fail)
  ("cf_is_quest_troop",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":is_quest_troop", 0),
      (try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
        (check_quest_active, ":cur_quest"),
        (quest_get_slot, ":quest_troop_1", ":cur_quest", slot_quest_target_troop),
        (quest_get_slot, ":quest_troop_2", ":cur_quest", slot_quest_object_troop),
        (quest_get_slot, ":quest_troop_3", ":cur_quest", slot_quest_giver_troop),
        (this_or_next|eq, ":quest_troop_1", ":troop_no"),
        (this_or_next|eq, ":quest_troop_2", ":troop_no"),
        (eq, ":quest_troop_3", ":troop_no"),
        (assign, ":is_quest_troop", 1),
      (try_end),
      (eq, ":is_quest_troop", 1),
  ]),


##  # script_calculate_team_strength
##  # Input: arg1 = team_no
##  # Output: strength
##  ("calculate_team_strength",
##    [
##      (store_script_param_1, ":team_no"),
##      (assign, ":total_strength", 0),
##      (try_for_agents, ":cur_agent"),
##        (agent_get_team, ":agent_team", ":cur_agent"),
##        (eq, ":team_no", ":agent_team"),
##        (agent_is_human, ":cur_agent"),
##        (agent_is_alive, ":cur_agent"),
##
##        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
##        (store_character_level, ":cur_level", ":cur_troop"),
##        (val_add, ":cur_level", 5),
##        (try_begin),
##          (troop_is_hero, ":cur_troop"),
##          (val_add, ":cur_level", 5),
##        (try_end),
##        (val_add, ":total_strength", ":cur_level"),
##      (try_end),
##      (assign, reg0, ":total_strength"),
##  ]),

  # script_check_friendly_kills
  # Input: none
  # Output: none (changes the morale of the player's party)
  ("check_friendly_kills",
    [(get_player_agent_own_troop_kill_count, ":count"),
     (try_begin),
       (neq, "$g_player_current_own_troop_kills", ":count"),
       (val_sub, ":count", "$g_player_current_own_troop_kills"),
       (val_add, "$g_player_current_own_troop_kills", ":count"),
       (val_mul, ":count", -1),
       (call_script, "script_change_player_party_morale", ":count"),
     (try_end),
   ]),

  # script_simulate_retreat
  # Input: arg1 = minimum_distance in km, arg2 = maximum_distance in km, pos1 = origin position
  # Output: pos2 = result position
  ("map_get_random_position_around_position_within_range",
    [
      (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
  ]),


  # script_get_number_of_unclaimed_centers_by_player
  # Input: arg1 = troop_no
  # Output: reg0 = number_of_enemy_troops
#  ("troop_count_number_of_enemy_troops",
#    [
#      (store_script_param_1, ":troop_no"),
#      (assign, ":enemy_count", 0),
#      (try_for_range, ":i_enemy_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
#        (troop_slot_ge, ":troop_no", ":i_enemy_slot", 1),
#        (val_add, ":enemy_count", 1),
#      (try_end),
#      (assign, reg0, ":enemy_count"),
#  ]),


  # script_cf_troop_check_troop_is_enemy
  # Input: arg1 = troop_no, arg2 = checked_troop_no
  # Output: none (Can fail)
  ("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
	  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":checked_troop_no"),
	  (lt, reg0, -10),
 ]),


  # script_troop_get_leaded_center_with_index
  # Inputs: none
  # Outputs: none

  #complete family relations removed

  # script_collect_friendly_parties
  # Fills the party p_collective_friends with the members of parties attached to main_party and ally_party_no
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

  # script_encounter_calculate_fit
  # Input: arg1 = troop_no
  # Output: fills $battle_renown_value
  ("calculate_renown_value",
   [
      ##diplomacy start+
	  #If terrain advantage is enabled, use it to avoid messing up cached
	  #strength values, but do not take it into consideration for renown
	  #granted.
	  (assign, ":main_party_strength", 1),
	  (assign, ":enemy_strength", 1),
	  (assign, ":friends_strength", 1),
	  (assign, ":terrain_code", -1),
	  (try_begin),
	     (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
	     (try_begin),
	        (encountered_party_is_attacker),
		    (call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
	     (else_try),
	        (call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
		 (try_end),
		 (assign, ":terrain_code", reg0),
		 ##Alternate option: calculate with terrain, but don't use it for renown
		 #(but do use it to update the cached strength for the party)
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code",0,1),
		 (assign, ":main_party_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code",0,1),
		 (assign, ":enemy_strength", reg1),#use non-terrain version!
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_friends", ":terrain_code",0,1),
		 (assign, ":friends_strength", reg1),#use non-terrain version!
	  (else_try),
	      ##Original option: calculate without terrain
		  (call_script, "script_party_calculate_strength", "p_main_party", 0),
		  (assign, ":main_party_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
		  (assign, ":enemy_strength", reg0),
		  (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
		  (assign, ":friends_strength", reg0),
	  (try_end),
	  ##diplomacy end+

      (val_add, ":friends_strength", 1),
      (store_mul, ":enemy_strength_ratio", ":enemy_strength", 100),
      (val_div, ":enemy_strength_ratio", ":friends_strength"),

      (assign, ":renown_val", ":enemy_strength"),
      (val_mul, ":renown_val", ":enemy_strength_ratio"),
      (val_div, ":renown_val", 100),

      (val_mul, ":renown_val", ":main_party_strength"),
      (val_div, ":renown_val",":friends_strength"),

      (store_div, "$battle_renown_value", ":renown_val", 5),
      (val_min, "$battle_renown_value", 2500),
      (convert_to_fixed_point, "$battle_renown_value"),
      (store_sqrt, "$battle_renown_value", "$battle_renown_value"),
      (convert_from_fixed_point, "$battle_renown_value"),
      (assign, reg8, "$battle_renown_value"),
      (display_message, "@Renown value for this battle is {reg8}.",0xFFFFFFFF),
  ]),


  ##  # script_calculate_weekly_wage_for_player
  ##  # Input: none
  ##  # Output: none
  ##  ("calculate_weekly_wage_for_player",
  ##    [
  ##        (call_script, "script_calculate_weekly_party_wage", "p_main_party"),
  ##        (assign, ":result", reg0),
  ##        (try_for_parties, ":party_no"),
  ##          (store_faction_of_party, ":party_faction", ":party_no"),
  ##          (eq, ":party_faction", "fac_player_supporters_faction"),
  ##          (call_script, "script_calculate_weekly_party_wage", ":party_no"),
  ##          (val_add, ":result", reg0),
  ##        (try_end),
  ##        (assign, reg0, ":result"),
  ##  ]),


  # script_get_first_agent_with_troop_id
  # Input: arg1 = troop_no
  # Output: agent_id
  ("cf_get_first_agent_with_troop_id",
    [
      (store_script_param_1, ":troop_no"),
      #      (store_script_param_2, ":agent_no_to_begin_searching_after"),
      (assign, ":result", -1),
      (try_for_agents, ":cur_agent"),
        (eq, ":result", -1),
        ##        (try_begin),
        ##          (eq, ":cur_agent", ":agent_no_to_begin_searching_after"),
        ##          (assign, ":agent_no_to_begin_searching_after", -1),
        ##        (try_end),
        ##        (eq, ":agent_no_to_begin_searching_after", -1),
        (agent_get_troop_id, ":cur_troop_no", ":cur_agent"),
        (eq, ":cur_troop_no", ":troop_no"),
        (assign, ":result", ":cur_agent"),
      (try_end),
      (assign, reg0, ":result"),
      (neq, reg0, -1),
  ]),


  # script_cf_team_get_average_position_of_agents_with_type_to_pos1
  # Input: arg1 = team_no, arg2 = class_no (grc_everyone, grc_infantry, grc_cavalry, grc_archers, grc_heroes)
  # Output: none, pos1 = average_position (0,0,0 if there are no matching agents)
  ("cf_team_get_average_position_of_agents_with_type_to_pos1",
    [
      (store_script_param_1, ":team_no"),
      (store_script_param_2, ":division_no"),
      (assign, ":total_pos_x", 0),
      (assign, ":total_pos_y", 0),
      (assign, ":total_pos_z", 0),
      (assign, ":num_agents", 0),
      (set_fixed_point_multiplier, 100),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":cur_team_no", ":cur_agent"),
        (eq, ":cur_team_no", ":team_no"),
        (agent_get_division, ":cur_agent_division", ":cur_agent"),
        (this_or_next|eq, ":division_no", grc_everyone),
        (eq, ":division_no", ":cur_agent_division"),
        (agent_get_position, pos1, ":cur_agent"),
        (position_get_x, ":cur_pos_x", pos1),
        (val_add, ":total_pos_x", ":cur_pos_x"),
        (position_get_y, ":cur_pos_y", pos1),
        (val_add, ":total_pos_y", ":cur_pos_y"),
        (position_get_z, ":cur_pos_z", pos1),
        (val_add, ":total_pos_z", ":cur_pos_z"),
        (val_add, ":num_agents", 1),
      (try_end),
      (gt, ":num_agents", 1),
      (val_div, ":total_pos_x", ":num_agents"),
      (val_div, ":total_pos_y", ":num_agents"),
      (val_div, ":total_pos_z", ":num_agents"),
      (init_position, pos1),
      (position_move_x, pos1, ":total_pos_x"),
      (position_move_y, pos1, ":total_pos_y"),
      (position_move_z, pos1, ":total_pos_z"),
  ]),

  # script_cf_turn_windmill_fans
  # Input: arg1 = instance_no (none = 0)
  # Output: none
  ("cf_turn_windmill_fans",
    [(store_script_param_1, ":instance_no"),
      (scene_prop_get_instance, ":windmill_fan_object", "spr_windmill_fan_turning", ":instance_no"),
      (ge, ":windmill_fan_object", 0),
      (prop_instance_get_position, pos1, ":windmill_fan_object"),
      (position_rotate_y, pos1, 10),
      (prop_instance_animate_to_position, ":windmill_fan_object", pos1, 100),
      (val_add, ":instance_no", 1),
      (call_script, "script_cf_turn_windmill_fans", ":instance_no"),
  ]),

  # script_print_party_members
  # Input: arg1 = party_no
  # Output: s51 = output string. "noone" if the party is empty
  ("print_party_members",
    [
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
      (assign, reg10, ":num_stacks"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop",":party_no",":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 0),
          (str_store_troop_name, s51, ":stack_troop"),
        (try_end),
        (str_store_troop_name, s52, ":stack_troop"),
        (try_begin),
          (eq, ":i_stack", 1),
          (str_store_string, s51, "str_s52_and_s51"),
        (else_try),
          (gt, ":i_stack", 1),
          (str_store_string, s51, "str_s52_comma_s51"),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":num_stacks", 0),
        (str_store_string, s51, "str_noone"),
      (try_end),
  ]),

  # script_round_value
  # Input: arg1 = value
  # Output: reg0 = rounded_value
  ("round_value",
    [
      (store_script_param_1, ":value"),
      (try_begin),
        (lt, ":value", 100),
        (neq, ":value", 0),
        (val_add, ":value", 5),
        (val_div, ":value", 10),
        (val_mul, ":value", 10),
        (try_begin),
          (eq, ":value", 0),
          (assign, ":value", 5),
        (try_end),
      (else_try),
        (lt, ":value", 300),
        (val_add, ":value", 25),
        (val_div, ":value", 50),
        (val_mul, ":value", 50),
      (else_try),
        (val_add, ":value", 50),
        (val_div, ":value", 100),
        (val_mul, ":value", 100),
      (try_end),
      (assign, reg0, ":value"),
  ]),


  # script_change_banners_and_chest
  # Input: arg1 = relation (-100 .. 100)
  # Output: none
  ("describe_relation_to_s63",
    [(store_script_param_1, ":relation"),
      (store_add, ":normalized_relation", ":relation", 100),
      (val_add, ":normalized_relation", 5),
      (store_div, ":str_offset", ":normalized_relation", 10),
      (val_clamp, ":str_offset", 0, 20),
      (store_add, ":str_id", "str_relation_mnus_100",  ":str_offset"),
      (str_store_string, s63, ":str_id"),
  ]),

  # script_describe_center_relation_to_s3
  # Input: none
  # Output: none (required for siege mission templates)
  ("siege_init_ai_and_belfry",
   [(assign, "$cur_belfry_pos", 50),
    (assign, ":cur_belfry_object_pos", slot_scene_belfry_props_begin),
    (store_current_scene, ":cur_scene"),
    #Collecting belfry objects
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (try_for_range, ":i_belfry_instance", 0, 3),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_b", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$belfry_rotating_objects_begin", ":cur_belfry_object_pos"),
    (try_for_range, ":i_belfry_instance", 0, 5),
      (scene_prop_get_instance, ":belfry_object", "spr_belfry_wheel", ":i_belfry_instance"),
      (ge, ":belfry_object", 0),
      (scene_set_slot, ":cur_scene", ":cur_belfry_object_pos", ":belfry_object"),
      (val_add, ":cur_belfry_object_pos", 1),
    (try_end),
    (assign, "$last_belfry_object_pos", ":cur_belfry_object_pos"),

    #Lifting up the platform  at the beginning
    (try_begin),
      (scene_prop_get_instance, ":belfry_object_to_rotate", "spr_belfry_platform_a", 0),
    (try_end),

    #Moving the belfry objects to their starting position
    (entry_point_get_position,pos1,55),
    (entry_point_get_position,pos3,50),
    (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
      (assign, ":pos_no", pos_belfry_begin),
      (val_add, ":pos_no", ":i_belfry_object_pos"),
      (val_sub, ":pos_no", slot_scene_belfry_props_begin),
      (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
      (prop_instance_get_position, pos2, ":cur_belfry_object"),
      (try_begin),
        (eq, ":cur_belfry_object", ":belfry_object_to_rotate"),
        (position_rotate_x, pos2, 90),
      (try_end),
      (position_transform_position_to_local, ":pos_no", pos1, pos2),
      (position_transform_position_to_parent, pos4, pos3, ":pos_no"),
      (prop_instance_animate_to_position, ":cur_belfry_object", pos4, 1),
    (try_end),
    (assign, "$belfry_positioned", 0),
    (assign, "$belfry_num_slots_positioned", 0),
    (assign, "$belfry_num_men_pushing", 0),

    (set_show_messages, 0),
    (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
    (team_give_order, "$attacker_team_2", grc_everyone, mordr_stand_ground),
    (set_show_messages, 1),
  ]),

  # script_cf_siege_move_belfry
  # Input: none
  # Output: none (required for siege mission templates)
  ("cf_siege_move_belfry",
   [(neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (entry_point_get_position,pos1,50),
    (entry_point_get_position,pos4,55),
    (get_distance_between_positions, ":total_distance", pos4, pos1),
    (store_current_scene, ":cur_scene"),
    (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
    (prop_instance_get_position, pos2, ":first_belfry_object"),
    (entry_point_get_position,pos1,"$cur_belfry_pos"),
    (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
    (position_transform_position_to_parent, pos5, pos4, pos_belfry_begin),
    (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (get_distance_between_positions, ":distance_left", pos2, pos5),
    (try_begin),
      (le, ":cur_distance", 10),
      (val_add, "$cur_belfry_pos", 1),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (position_transform_position_to_parent, pos3, pos1, pos_belfry_begin),
      (get_distance_between_positions, ":cur_distance", pos2, pos3),
    (try_end),
    (neq, "$cur_belfry_pos", 50),

    (assign, ":base_speed", 20),
    (store_div, ":slow_range", ":total_distance", 60),
    (store_sub, ":distance_moved", ":total_distance", ":distance_left"),

    (try_begin),
      (lt, ":distance_moved", ":slow_range"),
      (store_mul, ":base_speed", ":distance_moved", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (else_try),
      (lt, ":distance_left", ":slow_range"),
      (store_mul, ":base_speed", ":distance_left", -60),
      (val_div, ":base_speed", ":slow_range"),
      (val_add, ":base_speed", 80),
    (try_end),
    (store_mul, ":belfry_speed", ":cur_distance", ":base_speed"),
    (try_begin),
      (eq, "$belfry_num_men_pushing", 0),
      (assign, ":belfry_speed", 1000000),
    (else_try),
      (val_div, ":belfry_speed", "$belfry_num_men_pushing"),
    (try_end),

    (try_begin),
      (le, "$cur_belfry_pos", 55),
      (init_position, pos3),
      (position_rotate_x, pos3, ":distance_moved"),
      (scene_get_slot, ":base_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos4, ":base_belfry_object"),
      (entry_point_get_position,pos1,"$cur_belfry_pos"),
      (try_for_range, ":i_belfry_object_pos", slot_scene_belfry_props_begin, "$last_belfry_object_pos"),
        (scene_get_slot, ":cur_belfry_object", ":cur_scene", ":i_belfry_object_pos"),
        (try_begin),
          (ge, ":i_belfry_object_pos", "$belfry_rotating_objects_begin"),
          (prop_instance_get_starting_position, pos5, ":base_belfry_object"),
          (prop_instance_get_starting_position, pos6, ":cur_belfry_object"),
          (position_transform_position_to_local, pos7, pos5, pos6),
          (position_transform_position_to_parent, pos5, pos4, pos7),
          (position_transform_position_to_parent, pos6, pos5, pos3),
          (prop_instance_set_position, ":cur_belfry_object", pos6),
        (else_try),
          (assign, ":pos_no", pos_belfry_begin),
          (val_add, ":pos_no", ":i_belfry_object_pos"),
          (val_sub, ":pos_no", slot_scene_belfry_props_begin),
          (position_transform_position_to_parent, pos2, pos1, ":pos_no"),
          (prop_instance_animate_to_position, ":cur_belfry_object", pos2, ":belfry_speed"),
        (try_end),
      (try_end),
    (try_end),
    (gt, "$cur_belfry_pos", 55),
    (assign, "$belfry_positioned", 1),
  ]),

  # script_cf_siege_rotate_belfry_platform
  # Input: none
  # Output: none (required for siege mission templates)
  ("cf_siege_rotate_belfry_platform",
   [(eq, "$belfry_positioned", 1),
    (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
    (prop_instance_get_position, pos1, ":belfry_object"),
    (position_rotate_x, pos1, -90),
    (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
    (assign, "$belfry_positioned", 2),
  ]),

  # script_cf_siege_assign_men_to_belfry
  # Input: none
  # Output: none (required for siege mission templates)
  ("cf_siege_assign_men_to_belfry",
   [
##    (store_mission_timer_a, ":cur_seconds"),
    (neq, "$last_belfry_object_pos", slot_scene_belfry_props_begin),
    (assign, ":end_trigger", 0),
    (try_begin),
      (lt, "$belfry_positioned", 3),
      (get_player_agent_no, ":player_agent"),
      (store_current_scene, ":cur_scene"),
      (scene_get_slot, ":first_belfry_object", ":cur_scene", slot_scene_belfry_props_begin),
      (prop_instance_get_position, pos2, ":first_belfry_object"),
      (assign, ":slot_1_positioned", 0),
      (assign, ":slot_2_positioned", 0),
      (assign, ":slot_3_positioned", 0),
      (assign, ":slot_4_positioned", 0),
      (assign, ":slot_5_positioned", 0),
      (assign, ":slot_6_positioned", 0),
      (assign, "$belfry_num_slots_positioned", 0),
      (assign, "$belfry_num_men_pushing", 0),
      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_get_slot, ":x_pos", ":cur_agent", slot_agent_target_x_pos),
          (neq, ":x_pos", 0),
          (agent_get_slot, ":y_pos", ":cur_agent", slot_agent_target_y_pos),
          (try_begin),
            (eq, ":x_pos", -600),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_1_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_2_positioned", 1),
            (else_try),
              (assign, ":slot_3_positioned", 1),
            (try_end),
          (else_try),
            (try_begin),
              (eq, ":y_pos", 0),
              (assign, ":slot_4_positioned", 1),
            (else_try),
              (eq, ":y_pos", -200),
              (assign, ":slot_5_positioned", 1),
            (else_try),
              (assign, ":slot_6_positioned", 1),
            (try_end),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (init_position, pos1),
          (position_move_x, pos1, ":x_pos"),
          (position_move_y, pos1, ":y_pos"),
          (init_position, pos3),
          (position_move_x, pos3, ":x_pos"),
          (position_move_y, pos3, -1000),
          (position_transform_position_to_parent, pos4, pos2, pos1),
          (position_transform_position_to_parent, pos5, pos2, pos3),
          (agent_get_position, pos6, ":cur_agent"),
          (get_distance_between_positions, ":target_distance", pos6, pos4),
          (get_distance_between_positions, ":waypoint_distance", pos6, pos5),
          (try_begin),
            (this_or_next|lt, ":target_distance", ":waypoint_distance"),
            (lt, ":waypoint_distance", 600),
            (agent_set_scripted_destination, ":cur_agent", pos4, 1),
          (else_try),
            (agent_set_scripted_destination, ":cur_agent", pos5, 1),
          (try_end),
          (try_begin),
            (le, ":target_distance", 300),
            (val_add, "$belfry_num_men_pushing", 1),
          (try_end),
##        (else_try),
##          (agent_get_team, ":cur_agent_team", ":cur_agent"),
##          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
##          (             eq, "$attacker_team_2", ":cur_agent_team"),
##          (try_begin),
##            (gt, ":cur_seconds", 20),
##            (agent_get_position, pos1, ":cur_agent"),
##            (agent_set_scripted_destination, ":cur_agent", pos1, 0),
##          (else_try),
##            (try_begin),
##              (team_get_movement_order, ":order1", "$attacker_team", grc_infantry),
##              (team_get_movement_order, ":order2", "$attacker_team", grc_cavalry),
##              (team_get_movement_order, ":order3", "$attacker_team", grc_archers),
##              (this_or_next|neq, ":order1", mordr_stand_ground),
##              (this_or_next|neq, ":order2", mordr_stand_ground),
##              (neq, ":order3", mordr_stand_ground),
##              (set_show_messages, 0),
##              (team_give_order, "$attacker_team", grc_everyone, mordr_stand_ground),
##              (set_show_messages, 1),
##            (try_end),
##          (try_end),
        (try_end),
      (try_end),
      (try_begin),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_class, ":agent_class", ":cur_agent"),
          (this_or_next|eq, ":agent_class", grc_infantry),
          (eq, ":agent_class", grc_cavalry),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
      (try_begin),
        (store_mission_timer_a, ":cur_timer"),
        (gt, ":cur_timer", 20),
        (lt, "$belfry_num_slots_positioned", 6),
        (try_for_agents, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_get_team, ":cur_agent_team", ":cur_agent"),
          (this_or_next|eq, "$attacker_team", ":cur_agent_team"),
          (             eq, "$attacker_team_2", ":cur_agent_team"),
          (neq, ":player_agent", ":cur_agent"),
          (agent_get_slot, ":x_pos", ":cur_agent", 1),
          (eq, ":x_pos", 0),
          (assign, ":y_pos", 0),
          (try_begin),
            (eq, ":slot_1_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_1_positioned", 1),
          (else_try),
            (eq, ":slot_2_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_2_positioned", 1),
          (else_try),
            (eq, ":slot_3_positioned", 0),
            (assign, ":x_pos", -600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_3_positioned", 1),
          (else_try),
            (eq, ":slot_4_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", 0),
            (val_add, ":slot_4_positioned", 1),
          (else_try),
            (eq, ":slot_5_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -200),
            (val_add, ":slot_5_positioned", 1),
          (else_try),
            (eq, ":slot_6_positioned", 0),
            (assign, ":x_pos", 600),
            (assign, ":y_pos", -400),
            (val_add, ":slot_6_positioned", 1),
          (try_end),
          (val_add, "$belfry_num_slots_positioned", 1),
          (agent_set_slot, ":cur_agent", 1, ":x_pos"),
          (agent_set_slot, ":cur_agent", 2, ":y_pos"),
        (try_end),
      (try_end),
    (else_try),
      (assign, ":end_trigger", 1),
      (try_for_agents, ":cur_agent"),
        (agent_clear_scripted_mode, ":cur_agent"),
      (try_end),
      (set_show_messages, 0),
      (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
      (set_show_messages, 1),
    (try_end),
    (eq, ":end_trigger", 1),
  ]),

  # script_siege_move_archers_to_archer_positions
  # Input: arg1 = team_no, arg2 = class_no
  # Output: s1 = order_name
  ("store_weapon_usage_order_name_to_s1",
   [(store_script_param_1, ":team_no"),
    (store_script_param_2, ":class_no"),
    (team_get_weapon_usage_order, ":cur_order", ":team_no", ":class_no"),
    (team_get_hold_fire_order, ":cur_hold_fire", ":team_no", ":class_no"),
    (try_begin),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Any Weapon"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_fire_at_will),
      (str_store_string, s1, "@Blunt Weapons"),
    (else_try),
      (eq, ":cur_order", wordr_use_any_weapon),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_hold_fire"),
    (else_try),
      (eq, ":cur_order", wordr_use_blunt_weapons),
      (eq, ":cur_hold_fire", aordr_hold_your_fire),
      (str_store_string, s1, "str_blunt_hold_fire"),
    (else_try),
      (str_store_string, s1, "@N/A"),
    (try_end),
  ]),

  # script_team_give_order_from_order_panel
  # Input: arg1 = agent_no, pos2 = map_size_pos
  # Output: none
  ("update_agent_position_on_map",
   [(store_script_param_1, ":agent_no"),
    (agent_get_slot, ":agent_overlay", ":agent_no", slot_agent_map_overlay_id),

    (get_player_agent_no, ":player_agent"),
    (try_begin),
      (le, ":agent_overlay", 0),
      (set_fixed_point_multiplier, 1000),
      (try_begin),
        (eq, ":agent_no", ":player_agent"),
        (create_mesh_overlay, reg1, "mesh_player_dot"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 500),
        (overlay_set_size, reg1, pos1),
      (else_try),
        (create_mesh_overlay, reg1, "mesh_white_dot"),
        (position_set_x, pos1, 200),
        (position_set_y, pos1, 200),
        (overlay_set_size, reg1, pos1),
      (try_end),
      (overlay_set_alpha, reg1, 0x88),
      (agent_set_slot, ":agent_no", slot_agent_map_overlay_id, reg1),
      (assign, ":agent_overlay", reg1),
    (try_end),

    (try_begin),
      (neq, ":agent_no", ":player_agent"),
      (agent_get_party_id, ":agent_party", ":agent_no"),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (agent_get_division, ":agent_division", ":agent_no"),
        (try_begin),
          (eq, ":agent_division", 0),
          (overlay_set_color, ":agent_overlay", 0x8d5220),
        (else_try),
          (eq, ":agent_division", 1),
          (overlay_set_color, ":agent_overlay", 0x34c6e4),
        (else_try),
          (eq, ":agent_division", 2),
          (overlay_set_color, ":agent_overlay", 0x569619),
        (else_try),
          (eq, ":agent_division", 3),
          (overlay_set_color, ":agent_overlay", 0xFFE500),
        (else_try),
          (eq, ":agent_division", 4),
          (overlay_set_color, ":agent_overlay", 0x990099),
        (else_try),
          (eq, ":agent_division", 5),
          (overlay_set_color, ":agent_overlay", 0x99FE80),
        (else_try),
          (eq, ":agent_division", 6),
          (overlay_set_color, ":agent_overlay", 0x9DEFFE),
        (else_try),
          (eq, ":agent_division", 7),
          (overlay_set_color, ":agent_overlay", 0xFECB9D),
        (else_try),
          (eq, ":agent_division", 8),
          (overlay_set_color, ":agent_overlay", 0xB19C9C),
        (try_end),
      (else_try),
        (agent_is_ally, ":agent_no"),
        (overlay_set_color, ":agent_overlay", 0x5555FF),
      (else_try),
        (overlay_set_color, ":agent_overlay", 0xFF0000),
      (try_end),
    (try_end),

    (try_begin),
      (eq, ":agent_no", ":player_agent"),
      (agent_get_look_position, pos1, ":agent_no"),
      (position_get_rotation_around_z, ":rot", pos1),
      (init_position, pos10),
      (position_rotate_z, pos10, ":rot"),
      (overlay_set_mesh_rotation, ":agent_overlay", pos10),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (else_try),
      (agent_get_position, pos1, ":agent_no"),
      (call_script, "script_convert_3d_pos_to_map_pos"),
    (try_end),
    (overlay_set_position, ":agent_overlay", pos0),
  ]),

  # script_convert_3d_pos_to_map_pos
  # Input: pos1 = 3d_pos, pos2 = map_size_pos
  # Output: pos0 = map_pos
  ("convert_3d_pos_to_map_pos",
   [(set_fixed_point_multiplier, 1000),
    (position_transform_position_to_local, pos3, pos2, pos1),
    (position_get_x, ":agent_x_pos", pos3),
    (position_get_y, ":agent_y_pos", pos3),
    (val_div, ":agent_x_pos", "$g_battle_map_scale"),
    (val_div, ":agent_y_pos", "$g_battle_map_scale"),
    (set_fixed_point_multiplier, 1000),
    (store_sub, ":map_x", 980, "$g_battle_map_width"),
    (store_sub, ":map_y", 730, "$g_battle_map_height"),
    (val_add, ":agent_x_pos", ":map_x"),
    (val_add, ":agent_y_pos", ":map_y"),
    (position_set_x, pos0, ":agent_x_pos"),
    (position_set_y, pos0, ":agent_y_pos"),
  ]),

  # script_update_order_flags_on_map
  # Input: none
  # Output: none
  ("update_order_panel_statistics_and_map", #TODO: Call this in every battle mission template, once per second
   [(set_fixed_point_multiplier, 1000),

    (assign, ":num_us_ready_group0", 0),
    (assign, ":num_us_ready_group1", 0),
    (assign, ":num_us_ready_group2", 0),
    (assign, ":num_us_ready_group3", 0),
    (assign, ":num_us_ready_group4", 0),
    (assign, ":num_us_ready_group5", 0),
    (assign, ":num_us_ready_group6", 0),
    (assign, ":num_us_ready_group7", 0),
    (assign, ":num_us_ready_group8", 0),

    (assign, ":num_us_ready_men", 0),
    (assign, ":num_us_wounded_men", 0),
    (assign, ":num_us_routed_men", 0),
    (assign, ":num_us_dead_men", 0),
    (assign, ":num_allies_ready_men", 0),
    (assign, ":num_allies_wounded_men", 0),
    (assign, ":num_allies_routed_men", 0),
    (assign, ":num_allies_dead_men", 0),
    (assign, ":num_enemies_ready_men", 0),
    (assign, ":num_enemies_wounded_men", 0),
    (assign, ":num_enemies_routed_men", 0),
    (assign, ":num_enemies_dead_men", 0),

    (get_scene_boundaries, pos2, pos3),

    (try_for_agents,":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_get_division, ":agent_division", ":cur_agent"),
      (agent_get_party_id, ":agent_party", ":cur_agent"),
      (agent_get_slot, ":agent_overlay", ":cur_agent", slot_agent_map_overlay_id),
      (try_begin),
        (eq, ":agent_party", "p_main_party"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (try_begin),
            (eq, ":agent_division", 0),
            (val_add, ":num_us_ready_group0", 1),
            (eq, "$group0_has_troops", 1), #added to solve problem. test this.
          (else_try),
            (eq, ":agent_division", 1),
            (val_add, ":num_us_ready_group1", 1),
            (eq, "$group1_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 2),
            (val_add, ":num_us_ready_group2", 1),
            (eq, "$group2_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 3),
            (val_add, ":num_us_ready_group3", 1),
            (eq, "$group3_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 4),
            (val_add, ":num_us_ready_group4", 1),
            (eq, "$group4_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 5),
            (val_add, ":num_us_ready_group5", 1),
            (eq, "$group5_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 6),
            (val_add, ":num_us_ready_group6", 1),
            (eq, "$group6_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 7),
            (val_add, ":num_us_ready_group7", 1),
            (eq, "$group7_has_troops", 1), #added to solve problem.
          (else_try),
            (eq, ":agent_division", 8),
            (val_add, ":num_us_ready_group8", 1),
            (eq, "$group8_has_troops", 1), #added to solve problem.
          (try_end),
          (val_add, ":num_us_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_us_wounded_men", 1),
        (else_try),
          (agent_is_routed, ":cur_agent"),
          (val_add, ":num_us_routed_men", 1),
        (else_try),
          (val_add, ":num_us_dead_men", 1),
        (try_end),
      (else_try),
        (agent_is_ally, ":cur_agent"),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_allies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_allies_wounded_men", 1),
        (else_try),
          (agent_is_routed, ":cur_agent"),
          (val_add, ":num_allies_routed_men", 1),
        (else_try),
          (val_add, ":num_allies_dead_men", 1),
        (try_end),
      (else_try),
        (try_begin),
          (agent_is_alive, ":cur_agent"),
          (call_script, "script_update_agent_position_on_map", ":cur_agent"),
          (val_add, ":num_enemies_ready_men", 1),
        (else_try),
          (overlay_set_alpha, ":agent_overlay", 0),
          (agent_is_wounded, ":cur_agent"),
          (val_add, ":num_enemies_wounded_men", 1),
        (else_try),
          (agent_is_routed, ":cur_agent"),
          (val_add, ":num_enemies_routed_men", 1),
        (else_try),
          (val_add, ":num_enemies_dead_men", 1),
        (try_end),
      (try_end),
    (try_end),

    (assign, reg1, ":num_us_ready_group0"),
    (assign, reg2, ":num_us_ready_group1"),
    (assign, reg3, ":num_us_ready_group2"),
    (assign, reg4, ":num_us_ready_group3"),
    (assign, reg5, ":num_us_ready_group4"),
    (assign, reg6, ":num_us_ready_group5"),
    (assign, reg7, ":num_us_ready_group6"),
    (assign, reg8, ":num_us_ready_group7"),
    (assign, reg9, ":num_us_ready_group8"),
    (assign, reg10, ":num_us_ready_men"),
    (assign, reg11, ":num_us_wounded_men"),
    (assign, reg12, ":num_us_routed_men"),
    (assign, reg13, ":num_us_dead_men"),
    (assign, reg14, ":num_allies_ready_men"),
    (assign, reg15, ":num_allies_wounded_men"),
    (assign, reg16, ":num_allies_routed_men"),
    (assign, reg17, ":num_allies_dead_men"),
    (assign, reg18, ":num_enemies_ready_men"),
    (assign, reg19, ":num_enemies_wounded_men"),
    (assign, reg20, ":num_enemies_routed_men"),
    (assign, reg21, ":num_enemies_dead_men"),

    (try_begin),
      (eq, "$group0_has_troops", 1),
      (str_store_class_name, s1, 0),
      (overlay_set_text, "$g_presentation_obj_battle_name0", "str_s1_reg1"),
    (try_end),
    (try_begin),
      (eq, "$group1_has_troops", 1),
      (str_store_class_name, s1, 1),
      (overlay_set_text, "$g_presentation_obj_battle_name1", "str_s1_reg2"),
    (try_end),
    (try_begin),
      (eq, "$group2_has_troops", 1),
      (str_store_class_name, s1, 2),
      (overlay_set_text, "$g_presentation_obj_battle_name2", "str_s1_reg3"),
    (try_end),
    (try_begin),
      (eq, "$group3_has_troops", 1),
      (str_store_class_name, s1, 3),
      (overlay_set_text, "$g_presentation_obj_battle_name3", "str_s1_reg4"),
    (try_end),
    (try_begin),
      (eq, "$group4_has_troops", 1),
      (str_store_class_name, s1, 4),
      (overlay_set_text, "$g_presentation_obj_battle_name4", "str_s1_reg5"),
    (try_end),
    (try_begin),
      (eq, "$group5_has_troops", 1),
      (str_store_class_name, s1, 5),
      (overlay_set_text, "$g_presentation_obj_battle_name5", "str_s1_reg6"),
    (try_end),
    (try_begin),
      (eq, "$group6_has_troops", 1),
      (str_store_class_name, s1, 6),
      (overlay_set_text, "$g_presentation_obj_battle_name6", "str_s1_reg7"),
    (try_end),
    (try_begin),
      (eq, "$group7_has_troops", 1),
      (str_store_class_name, s1, 7),
      (overlay_set_text, "$g_presentation_obj_battle_name7", "str_s1_reg8"),
    (try_end),
    (try_begin),
      (eq, "$group8_has_troops", 1),
      (str_store_class_name, s1, 8),
      (overlay_set_text, "$g_presentation_obj_battle_name8", "str_s1_reg9"),
    (try_end),

    (overlay_set_text, "$g_battle_us_ready", "@{!}{reg10}"),
    (overlay_set_text, "$g_battle_us_wounded", "@{!}{reg11}"),
    (overlay_set_text, "$g_battle_us_routed", "@{!}{reg12}"),
    (overlay_set_text, "$g_battle_us_dead", "str_reg13"),
    (overlay_set_text, "$g_battle_allies_ready", "str_reg14"),
    (overlay_set_text, "$g_battle_allies_wounded", "str_reg15"),
    (overlay_set_text, "$g_battle_allies_routed", "str_reg16"),
    (overlay_set_text, "$g_battle_allies_dead", "str_reg17"),
    (overlay_set_text, "$g_battle_enemies_ready", "str_reg18"),
    (overlay_set_text, "$g_battle_enemies_wounded", "str_reg19"),
    (overlay_set_text, "$g_battle_enemies_routed", "str_reg20"),
    (overlay_set_text, "$g_battle_enemies_dead", "str_reg21"),

    (assign, ":stat_position_x", 675),
    (assign, ":stat_position_y", 280),
    (val_add, ":stat_position_x", 70),
    (val_add, ":stat_position_y", 60),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_us_ready", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_wounded", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_routed", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_us_dead", pos1),
    (val_add, ":stat_position_x", -210),
    (val_add, ":stat_position_y", -30),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_allies_ready", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_wounded", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_routed", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_allies_dead", pos1),
    (val_add, ":stat_position_x", -210),
    (val_add, ":stat_position_y", -30),
    (position_set_x, pos1, ":stat_position_x"),
    (position_set_y, pos1, ":stat_position_y"),
    (overlay_set_position, "$g_battle_enemies_ready", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_wounded", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_routed", pos1),
    (val_add, ":stat_position_x", 70),
    (position_set_x, pos1, ":stat_position_x"),
    (overlay_set_position, "$g_battle_enemies_dead", pos1),

    (call_script, "script_update_order_flags_on_map"),
  ]),

 # script_set_town_picture
  # Input: arg1: order of the food to be consumed
  # Output: none
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



  # script_calculate_troop_score_for_center
  # INPUT: arg1 = agent_no
  # OUTPUT: none
  ("agent_reassign_team",
    [
      (store_script_param, ":agent_no", 1),
      (get_player_agent_no, ":player_agent"),
      (try_begin),
        (ge, ":player_agent", 0),
        (agent_is_human, ":agent_no"),
        (agent_is_ally, ":agent_no"),
        (agent_get_party_id, ":party_no", ":agent_no"),
        #SB : pre-process this instead of calculating per agent
        (party_slot_eq, ":party_no", slot_party_temp_slot_1, -1),
        # (neq, ":party_no", "p_main_party"),
        # (assign, ":continue", 1),
        # (store_faction_of_party, ":party_faction", ":party_no"),
        # (try_begin),
          # (eq, ":party_faction", "$players_kingdom"),
          # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          # (assign, ":continue", 0),
        # (else_try),
          # (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),
          # (neg|is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end),
          # (assign, ":continue", 0),
        # (try_end),
        # (eq, ":continue", 1),
        (agent_get_team, ":player_team", ":player_agent"),
        (val_add, ":player_team", 2),
        (agent_set_team, ":agent_no", ":player_team"),
      (try_end),
      ]),

  #script_start_quest
  # INPUT: none
  # OUTPUT: none
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

  #script_update_tavern_travellers
  # INPUT: none
  # OUTPUT: none
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

  #script_update_tavern_minstels
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_notes",
    [
##      (store_script_param, ":troop_no", 1),
##     (str_store_troop_name, s54, ":troop_no"),
##     (try_begin),
##       (eq, ":troop_no", "trp_player"),
##       (this_or_next|eq, "$player_has_homage", 1),
##		(eq, "$players_kingdom", "fac_player_supporters_faction"),
##       (assign, ":troop_faction", "$players_kingdom"),
##     (else_try),
##       (store_troop_faction, ":troop_faction", ":troop_no"),
##     (try_end),
##
##	 (str_clear, s49),
##	 (try_begin),
##		(is_between, ":troop_no", lords_begin, kingdom_ladies_end),
##		(troop_get_slot, reg1, ":troop_no", slot_troop_age),
##		(str_store_string, s49, "str__age_reg1_family_"),
##
##		(try_for_range, ":aristocrat", lords_begin, kingdom_ladies_end),
##			(call_script, "script_troop_get_family_relation_to_troop", ":aristocrat", ":troop_no"),
##			(gt, reg0, 0),
##
##			(try_begin),
##				(neg|is_between, ":aristocrat", kingdom_ladies_begin, kingdom_ladies_end),
##				(str_store_troop_name_link, s12, ":aristocrat"),
##				(call_script, "script_troop_get_relation_with_troop", ":aristocrat", ":troop_no"),
##				(str_store_string, s49, "str_s49_s12_s11_rel_reg0"),
##			(else_try),
##				(str_store_troop_name, s12, ":aristocrat"),
##				(str_store_string, s49, "str_s49_s12_s11"),
##			(try_end),
##
##		(try_end),
##	 (try_end),
##
##     (try_begin),
##       (neq, ":troop_no", "trp_player"),
##       (neg|is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
##       (str_clear, s54),
##       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
###     (else_try),
###       (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
###       (str_clear, s54),
###       (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
###       (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##     (else_try),
##       (is_between, ":troop_no", pretenders_begin, pretenders_end),
##       (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##       (neq, ":troop_no", "$supported_pretender"),
##       (troop_get_slot, ":orig_faction", ":troop_no", slot_troop_original_faction),
##       (try_begin),
##         (faction_slot_eq, ":orig_faction", slot_faction_state, sfs_active),
##         (faction_slot_eq, ":orig_faction", slot_faction_has_rebellion_chance, 1),
##         (str_store_faction_name_link, s56, ":orig_faction"),
##         (add_troop_note_from_sreg, ":troop_no", 0, "@{s54} is a claimant to the throne of {s56}.", 0),
##         (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##       (else_try),
##         (str_clear, s54),
##         (add_troop_note_from_sreg, ":troop_no", 0, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 1, s54, 0),
##         (add_troop_note_from_sreg, ":troop_no", 2, s54, 0),
##       (try_end),
##     (else_try),
##       (faction_get_slot, ":faction_leader", ":troop_faction", slot_faction_leader),
##       (str_store_troop_name_link, s55, ":faction_leader"),
##       (str_store_faction_name_link, s56, ":troop_faction"),
##       (assign, ":troop_is_player_faction", 0),
##       (assign, ":troop_is_faction_leader", 0),
##       (try_begin),
##         (eq, ":troop_faction", "fac_player_faction"),
##         (assign, ":troop_is_player_faction", 1),
##       (else_try),
##         (eq, ":faction_leader", ":troop_no"),
##         (assign, ":troop_is_faction_leader", 1),
##       (try_end),
##       (assign, ":num_centers", 0),
##       (str_store_string, s58, "@nowhere"),
##       (try_for_range_backwards, ":cur_center", centers_begin, centers_end),
##         (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
##         (try_begin),
##           (eq, ":num_centers", 0),
##           (str_store_party_name_link, s58, ":cur_center"),
##         (else_try),
##           (eq, ":num_centers", 1),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{s57} and {s58}"),
##         (else_try),
##           (str_store_party_name_link, s57, ":cur_center"),
##           (str_store_string, s58, "@{!}{s57}, {s58}"),
##         (try_end),
##         (val_add, ":num_centers", 1),
##       (try_end),
##       (troop_get_type, reg3, ":troop_no"),
##       (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##       (str_clear, s59),
##       (try_begin),
###         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
##         (call_script, "script_troop_get_player_relation", ":troop_no"),
##         (assign, ":relation", reg0),
##         (store_add, ":normalized_relation", ":relation", 100),
##         (val_add, ":normalized_relation", 5),
##         (store_div, ":str_offset", ":normalized_relation", 10),
##         (val_clamp, ":str_offset", 0, 20),
##         (store_add, ":str_id", "str_relation_mnus_100_ns",  ":str_offset"),
##         (neq, ":str_id", "str_relation_plus_0_ns"),
##         (str_store_string, s60, "@{reg3?She:He}"),
##         (str_store_string, s59, ":str_id"),
##         (str_store_string, s59, "@{!}^{s59}"),
##       (try_end),
##
##	#lord recruitment changes begin
##	#This sends a bunch of political information to s47.
##
##
##
##
##	    #refresh registers
##        (assign, reg9, ":num_centers"),
##        (troop_get_type, reg3, ":troop_no"),
##        (troop_get_slot, reg5, ":troop_no", slot_troop_renown),
##		(assign, reg4, ":troop_is_faction_leader"),
##		(assign, reg6, ":troop_is_player_faction"),
##
##        (add_troop_note_from_sreg, ":troop_no", 0, "str_reg6reg4s54_is_the_ruler_of_s56_s54_is_a_vassal_of_s55_of_s56_renown_reg5_reg9reg3shehe_is_the_reg3ladylord_of_s58reg3shehe_has_no_fiefss59_s49", 0),
##	#lord recruitment changes end
##
##        (add_troop_note_tableau_mesh, ":troop_no", "tableau_troop_note_mesh"),
##     (try_end),
     ]),

  #script_update_troop_location_notes
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_location_notes",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":see_or_hear", 2),
      (try_begin),
        (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
        (neq, reg0, 0),

        (call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
        (eq, reg0, -1),
        ##diplomacy start+ use gender script
	    #(troop_get_type, reg1, ":troop_no"),
		(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
		(assign, reg1, reg0),
		##diplomacy end+
        (try_begin),
          (eq, ":see_or_hear", 0),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
        (else_try),
          (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
        (try_end),
      (try_end),
     ]),

  #script_update_troop_location_notes_prisoned
  # INPUT: troop_no
  # OUTPUT: none
  ("update_troop_location_notes_prisoned",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":capturer_faction_no", 2),
      ##diplomacy start+ use gender script
      #(troop_get_type, reg1, ":troop_no"),
	  (call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
      (assign, reg1, reg0),
	  ##diplomacy end+
      (str_store_faction_name_link, s1, ":capturer_faction_no"),

      (add_troop_note_from_sreg, ":troop_no", 2, "str_reg1shehe_is_prisoner_of_s1", 1),
    ]),

    # INPUT: none
  # OUTPUT: none
  ("update_all_notes",
    [
      (call_script, "script_update_troop_notes", "trp_player"),
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	    (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
        (call_script, "script_update_troop_notes", ":troop_no"),
      (try_end),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (call_script, "script_update_center_notes", ":center_no"),
      (try_end),
      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":faction_no"),
      (try_end),
    ]),

  #script_agent_troop_get_banner_mesh
##  # INPUT: agent_no
##  # OUTPUT: none
##  ("shield_item_set_banner",
##    [
##       (store_script_param, ":tableau_no",1),
##       (store_script_param, ":agent_no", 2),
##       (store_script_param, ":troop_no", 3),
##       (assign, ":banner_troop", -1),
##       (try_begin),
##         (lt, ":agent_no", 0),
##         (try_begin),
##           (ge, ":troop_no", 0),
##           (troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 0),
##           (assign, ":banner_troop", ":troop_no"),
##         (else_try),
##           (assign, ":banner_troop", -2),
##         (try_end),
##       (else_try),
##         (agent_get_troop_id, ":troop_id", ":agent_no"),
##         (troop_slot_ge,  ":troop_id", slot_troop_custom_banner_flag_type, 0),
##         (assign, ":banner_troop", ":troop_id"),
##       (else_try),
##         (agent_get_party_id, ":agent_party", ":agent_no"),
##         (try_begin),
##           (lt, ":agent_party", 0),
##           (is_between, ":troop_id", companions_begin, companions_end),
##           (main_party_has_troop, ":troop_id"),
##           (assign, ":agent_party", "p_main_party"),
##         (try_end),
##         (ge, ":agent_party", 0),
##         (party_get_template_id, ":party_template", ":agent_party"),
##         (try_begin),
##           (eq, ":party_template", "pt_deserters"),
##           (assign, ":banner_troop", -3),
##         (else_try),
##           (is_between, ":agent_party", centers_begin, centers_end),
##           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
##           (ge, ":town_lord", 0),
##           (assign, ":banner_troop", ":town_lord"),
##         (else_try),
##           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
##           (             eq, ":agent_party", "p_main_party"),
##           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
##           (gt, ":num_stacks", 0),
##           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
##           (troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
##           (assign, ":banner_troop", ":leader_troop_id"),
##         (try_end),
##       (else_try), #Check if we are in a tavern
##         (eq, "$talk_context", tc_tavern_talk),
##         (neq, ":troop_no", "trp_player"),
##         (assign, ":banner_troop", -4),
##       (else_try), #can't find party, this can be a town guard
##         (neq, ":troop_no", "trp_player"),
##         (is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
##         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
##         (ge, ":town_lord", 0),
##         (assign, ":banner_troop", ":town_lord"),
##       (try_end),
##       (cur_item_set_tableau_material, ":tableau_no", ":banner_troop"),
##     ]),

  #script_add_troop_to_cur_tableau
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau",
    [
       (store_script_param, ":troop_no",1),

       (cur_tableau_clear_override_items),

#       (cur_tableau_set_override_flags, af_override_fullhelm),
       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),

       (set_fixed_point_multiplier, 100),
       (assign, ":banner_mesh", -1),
       (troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
       (try_begin),
           (eq, ":banner_spr", -1),
           (try_begin),
              # (this_or_next|eq, ":troop_no", "trp_player"),
              # (is_between, ":troop_no", npcs_begin, npcs_end),
              (troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
              (ge, ":flag_icon", 0),
              (troop_get_slot, ":banner", ":troop_no", slot_troop_custom_banner_flag_type),
              (ge, ":banner", 0),
              (val_add, ":banner", "itm_banner_background1"),
              (cur_tableau_add_override_item, ":banner"),
           (try_end),
       (else_try),
           (gt, ":banner_spr", 0),
           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
           (try_begin),
             (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
             (val_sub, ":banner_spr", banner_scene_props_begin),
             (store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
           (try_end),
       (try_end),



       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":eye_height", 162),
       (store_mul, ":camera_distance", ":troop_no", 87323),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 139),
       (store_mul, ":camera_yaw", ":troop_no", 124337),
       (val_mod, ":camera_yaw", 50),
       (val_add, ":camera_yaw", -25),
       (store_mul, ":camera_pitch", ":troop_no", 98123),
       (val_mod, ":camera_pitch", 20),
       (val_add, ":camera_pitch", -14),
       (assign, ":animation", "anim_stand_man"),

##       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
##       (try_begin),
##         (gt, ":horse_item", 0),
##         (assign, ":eye_height", 210),
##         (cur_tableau_add_horse, ":horse_item", pos2, anim_horse_stand, 0),
##         (assign, ":animation", anim_ride_0),
##         (position_set_z, pos5, 125),
##         (try_begin),
##           (is_between, ":camera_yaw", -10, 10), #make sure horse head doesn't obstruct face.
##           (val_min, ":camera_pitch", -5),
##         (try_end),
##       (try_end),
       (position_set_z, pos5, ":eye_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (ge, ":banner_mesh", 0),
         (eq, "$black_jack",0),#plus blackjack 21


         (init_position, pos1),
         (position_set_z, pos1, -1500),
         (position_set_x, pos1, 265),
         (position_set_y, pos1, 400),
         (position_transform_position_to_parent, pos3, pos5, pos1),
         (cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
       (try_end),
       (cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_add_troop_to_cur_tableau_for_character
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_character",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (cur_tableau_set_override_flags, af_override_fullhelm),
##       (cur_tableau_set_override_flags, af_override_head|af_override_weapons),

       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 150),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 360),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_add_troop_to_cur_tableau_for_inventory
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_inventory",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":side", ":troop_no", 4), #side flag is inside troop_no value
       (val_div, ":troop_no", 4), #removing the flag bit
       (val_mul, ":side", 90), #to degrees

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       #SB : override appearance while disguised and buying stuff
       (try_begin),
         (gt, "$sneaked_into_town", disguise_none),
         (cur_tableau_set_override_flags, af_override_everything),
         (try_begin),
           (eq, "$sneaked_into_town", disguise_pilgrim),
           (cur_tableau_add_override_item, "itm_pilgrim_hood"),
           (cur_tableau_add_override_item, "itm_pilgrim_disguise"),
           (cur_tableau_add_override_item, "itm_wrapping_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_farmer),
           (cur_tableau_add_override_item, "itm_felt_hat"),
           (cur_tableau_add_override_item, "itm_coarse_tunic"),
           (cur_tableau_add_override_item, "itm_nomad_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_hunter),
           (cur_tableau_add_override_item, "itm_black_hood"),
           (cur_tableau_add_override_item, "itm_leather_gloves"),
           (cur_tableau_add_override_item, "itm_light_leather"),
           (cur_tableau_add_override_item, "itm_light_leather_boots"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_merchant),
           (cur_tableau_add_override_item, "itm_leather_jacket"),
           (cur_tableau_add_override_item, "itm_woolen_hose"),
           (cur_tableau_add_override_item, "itm_felt_steppe_cap"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_guard),
           (cur_tableau_add_override_item, "itm_footman_helmet"),
           (cur_tableau_add_override_item, "itm_mail_mittens"),
           (cur_tableau_add_override_item, "itm_mail_shirt"),
           (cur_tableau_add_override_item, "itm_leather_jerkin"),
           (cur_tableau_add_override_item, "itm_mail_chausses"),
         (else_try),
           (eq, "$sneaked_into_town", disguise_bard),
           (cur_tableau_add_override_item, "itm_linen_tunic"),
           (cur_tableau_add_override_item, "itm_leather_boots"),
         (try_end),
       (try_end),
       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #script_add_troop_to_cur_tableau_for_profile
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_profile",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),

       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (profile_get_banner_id, ":profile_banner"),
       (try_begin),
         (ge, ":profile_banner", 0),
         (init_position, pos2),
         (val_add, ":profile_banner", banner_meshes_begin),
         (position_set_x, pos2, -175),
         (position_set_y, pos2, -300),
         (position_set_z, pos2, 180),
         (position_rotate_x, pos2, 90),
         (position_rotate_y, pos2, -15),
         (cur_tableau_add_mesh, ":profile_banner", pos2, 0, 0),
       (try_end),

       (init_position, pos2),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),

  #SB : duplicate of script_add_troop_to_cur_tableau_for_profile for single-player kingdom heroes
  #script_add_troop_to_cur_tableau_for_presentation
  # INPUT: troop_no, kingdom hero or lady
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_presentation",
    [
        (store_script_param, ":troop_no",1),

        (set_fixed_point_multiplier, 100),

        (cur_tableau_clear_override_items),

        (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

        (init_position, pos5),
        (assign, ":cam_height", 105),
        #       (val_mod, ":camera_distance", 5),
        (assign, ":camera_distance", 380),
        (assign, ":camera_yaw", -15),
        (assign, ":camera_pitch", -18),
        #transient pose seeds
        (troop_get_xp, ":random_seed", ":troop_no"),
        (val_add, ":random_seed", ":troop_no"),
        (val_mod, ":random_seed", 5),
        (store_add, ":animation", "anim_pose_1", ":random_seed"),

        (position_set_z, pos5, ":cam_height"),

        # camera looks towards -z axis

        (position_rotate_x, pos5, -90),
        (position_rotate_z, pos5, 180),
        # now apply yaw and pitch
        (position_rotate_y, pos5, ":camera_yaw"),
        (position_rotate_x, pos5, ":camera_pitch"),
        (position_move_z, pos5, ":camera_distance", 0),
        (position_move_x, pos5, 5, 0),

        #honestly we can just draw this in the presentation
       # (troop_get_slot, ":banner", ":troop_no", slot_troop_banner_scene_prop),
       # (try_begin), #default slot val = 0, exclude placeholders since we don't want to touch their slots
         # (ge, ":banner", 0),
         # (is_between, ":troop_no", heroes_begin, heroes_end),
         # (init_position, pos2),
         # (val_sub, ":banner", banner_scene_props_begin),
         # (val_add, ":banner", banner_meshes_begin),
         # (position_set_x, pos2, -175),
         # (position_set_y, pos2, -300),
         # (position_set_z, pos2, 180),
         # (position_rotate_x, pos2, 90),
         # (position_rotate_y, pos2, -15),
         # (cur_tableau_add_mesh, ":banner", pos2, 0, 0),
       # (try_end),

       (init_position, pos2),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (try_begin), #rotate character, not flag
           (call_script, "script_cf_dplmc_troop_is_female", ":troop_no"),
           (position_rotate_z, pos2, -45),
         (try_end),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),


  #script_add_troop_to_cur_tableau_for_retirement
  # INPUT: type
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_retirement", [
    (store_script_param, ":type", 1),
    (try_begin),
      (is_between, ":type", 0, 10),
      (cur_tableau_set_override_flags, af_override_everything),
    (try_end),

    (try_begin),
      (eq, ":type", 0),
      (cur_tableau_add_override_item, "itm_pilgrim_hood"),
      (cur_tableau_add_override_item, "itm_pilgrim_disguise"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 1),
      (cur_tableau_add_override_item, "itm_pilgrim_hood"),
      (cur_tableau_add_override_item, "itm_red_tunic"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (cur_tableau_add_override_item, "itm_dagger"),
      (assign, ":animation", "anim_pose_1"),
    (else_try),
      (eq, ":type", 2),
      (cur_tableau_add_override_item, "itm_linen_tunic"),
      (cur_tableau_add_override_item, "itm_wrapping_boots"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 3),
      (cur_tableau_add_override_item, "itm_nomad_vest"),
      (cur_tableau_add_override_item, "itm_nomad_boots"),
      (assign, ":animation", "anim_pose_2"),
    (else_try),
      (eq, ":type", 4),
      (cur_tableau_add_override_item, "itm_leather_apron"),
      (cur_tableau_add_override_item, "itm_leather_boots"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 5),
      (cur_tableau_add_override_item, "itm_red_shirt"),
      (cur_tableau_add_override_item, "itm_woolen_hose"),
      (cur_tableau_add_override_item, "itm_fur_hat"),
      (assign, ":animation", "anim_pose_3"),
    (else_try),
      (eq, ":type", 6),
      (cur_tableau_add_override_item, "itm_red_gambeson"),
      (cur_tableau_add_override_item, "itm_leather_boots"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 7),
      (cur_tableau_add_override_item, "itm_nobleman_outfit"),
      (cur_tableau_add_override_item, "itm_blue_hose"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 8),
      (cur_tableau_add_override_item, "itm_courtly_outfit"),
      (cur_tableau_add_override_item, "itm_woolen_hose"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_4"),
    (else_try),
      (eq, ":type", 9),
      (cur_tableau_add_override_item, "itm_heraldic_mail_with_surcoat_for_tableau"),
      (cur_tableau_add_override_item, "itm_mail_boots_for_tableau"),
      (cur_tableau_add_override_item, "itm_sword_medieval_c"),
      (assign, ":animation", "anim_pose_5"),
    (try_end),

##    (set_fixed_point_multiplier, 100),
##    (cur_tableau_set_background_color, 0x00000000),
##    (cur_tableau_set_ambient_light, 10,11,15),

##     (init_position, pos8),
##     (position_set_x, pos8, -210),
##     (position_set_y, pos8, 200),
##     (position_set_z, pos8, 300),
##     (cur_tableau_add_point_light, pos8, 550,500,450),


    (set_fixed_point_multiplier, 100),
    (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),
    (assign, ":cam_height", 155),
    (assign, ":camera_distance", 575),
    (assign, ":camera_yaw", -5),
    (assign, ":camera_pitch", 10),

    (init_position, pos5),
    (position_set_z, pos5, ":cam_height"),
    # camera looks towards -z axis
    (position_rotate_x, pos5, -90),
    (position_rotate_z, pos5, 180),
    # now apply yaw and pitch
    (position_rotate_y, pos5, ":camera_yaw"),
    (position_rotate_x, pos5, ":camera_pitch"),
    (position_move_z, pos5, ":camera_distance", 0),
    (position_move_x, pos5, 60, 0),

    (init_position, pos2),
    (cur_tableau_add_troop, "trp_player", pos2, ":animation", 0),
    (cur_tableau_set_camera_position, pos5),

    (copy_position, pos8, pos5),
    (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
    (position_rotate_z, pos8, 30),
    (position_rotate_x, pos8, -60),
    (cur_tableau_add_sun_light, pos8, 175,150,125),
    ]),

  #script_add_troop_to_cur_tableau_for_party
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_party",
    [
       (store_script_param, ":troop_no",1),
       (store_mod, ":hide_weapons", ":troop_no", 2), #hide_weapons flag is inside troop_no value
       (val_div, ":troop_no", 2), #removing the flag bit

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       (try_begin),
         (eq, ":hide_weapons", 1),
         (cur_tableau_set_override_flags, af_override_fullhelm|af_override_head|af_override_weapons),
       (try_end),

       (init_position, pos2),
       (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 450),
       (assign, ":camera_yaw", 15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),

       (troop_get_inventory_slot, ":horse_item", ":troop_no", ek_horse),
       (try_begin),
         (gt, ":horse_item", 0),
         (eq, ":hide_weapons", 0),
         (cur_tableau_add_horse, ":horse_item", pos2, "anim_horse_stand", 0),
         (assign, ":animation", "anim_ride_0"),
         (assign, ":camera_yaw", 23),
         (assign, ":cam_height", 150),
         (assign, ":camera_distance", 550),
       (try_end),
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),


  #script_count_mission_casualties_from_agents
  # INPUT: none
  # OUTPUT: none
  ("count_mission_casualties_from_agents",
    [(party_clear, "p_player_casualties"),
     (party_clear, "p_enemy_casualties"),
     (party_clear, "p_ally_casualties"),
     (assign, "$any_allies_at_the_last_battle", 0),
     #(assign, "$num_routed_us", 0), #these should not assign to 0 here to protect routed agents to spawn again in next turns.
     #(assign, "$num_routed_allies", 0),
     #(assign, "$num_routed_enemies", 0),

     #initialize all routed counts of troops
     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (agent_get_party_id, ":agent_party", ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (troop_set_slot, ":agent_troop_id", slot_troop_player_routed_agents, 0),
       (troop_set_slot, ":agent_troop_id", slot_troop_ally_routed_agents, 0),
       (troop_set_slot, ":agent_troop_id", slot_troop_enemy_routed_agents, 0),
     (try_end),

     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (agent_get_party_id, ":agent_party", ":cur_agent"),
       (try_begin),
         (neq, ":agent_party", "p_main_party"),
         (agent_is_ally, ":cur_agent"),
         (assign, "$any_allies_at_the_last_battle", 1),
       (try_end),
       #count routed agents in player party, ally parties and enemy parties
       (try_begin),
         #(agent_is_routed, ":cur_agent"), #dckplmc
         (assign, ":continue", 0),
         (agent_get_slot, ":agent_was_running_away", ":cur_agent", slot_agent_is_running_away),
         (try_begin),
             (agent_is_routed, ":cur_agent"),
             (eq, ":agent_was_running_away", 1),
             (assign, ":continue", 1),
         (else_try),
            (agent_is_alive, ":cur_agent"),
            (eq, ":agent_was_running_away", 1),
            (assign, ":continue", 1),
         (try_end),
         (eq, ":continue", 1),
         (try_begin),
           (agent_get_troop_id, ":routed_ag_troop_id", ":cur_agent"),
           (agent_get_party_id, ":routed_ag_party_id", ":cur_agent"),
           #only enemies
           #only regulars

           (try_begin),
             (eq, ":agent_party", "p_main_party"),
             (val_add, "$num_routed_us", 1),
           (else_try),
             (agent_is_ally, ":cur_agent"),
             (val_add, "$num_routed_allies", 1),
           (else_try),
             #for now only count and include routed enemy agents in new routed party.
             (val_add, "$num_routed_enemies", 1),

             (gt, ":routed_ag_party_id", -1),
             (store_faction_of_party, ":faction_of_routed_agent_party", ":routed_ag_party_id"),

             (faction_get_slot, ":num_routed_agents_in_this_faction", ":faction_of_routed_agent_party", slot_faction_num_routed_agents),
             (val_add, ":num_routed_agents_in_this_faction", 1),
             (faction_set_slot, ":faction_of_routed_agent_party", slot_faction_num_routed_agents, ":num_routed_agents_in_this_faction"),
             (party_add_members, "p_routed_enemies", ":routed_ag_troop_id", 1),
           (try_end),
         (try_end),
         (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
         (try_begin),
           (eq, ":agent_party", "p_main_party"),
           (troop_get_slot, ":player_routed_agents", ":agent_troop_id", slot_troop_player_routed_agents),
           (val_add, ":player_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_player_routed_agents, ":player_routed_agents"),

         (else_try),
           (agent_is_ally, ":cur_agent"),
           (troop_get_slot, ":ally_routed_agents", ":agent_troop_id", slot_troop_ally_routed_agents),
           (val_add, ":ally_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_ally_routed_agents, ":ally_routed_agents"),

         (else_try),
           (troop_get_slot, ":enemy_routed_agents", ":agent_troop_id", slot_troop_enemy_routed_agents),
           (val_add, ":enemy_routed_agents", 1),
           (troop_set_slot, ":agent_troop_id", slot_troop_enemy_routed_agents, ":enemy_routed_agents"),

         (try_end),
       (try_end),
       #count and save killed agents in player party, ally parties and enemy parties
       (assign, ":continue", 0),
       (agent_get_slot, ":agent_was_running_away", ":cur_agent", slot_agent_is_running_away),
       (try_begin),
         (neg|agent_is_alive, ":cur_agent"),
         (assign, ":continue", 1),
       (else_try),
        (eq, ":agent_was_running_away", 1),
        (assign, ":continue", 1),
       (try_end),
       (eq, ":continue", 1),
       #(neg|agent_is_alive, ":cur_agent"),
       (agent_get_troop_id, ":agent_troop_id", ":cur_agent"),
       (try_begin),
         (eq, ":agent_party", "p_main_party"),
         (party_add_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_player_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (agent_is_ally, ":cur_agent"),
         (party_add_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_ally_casualties", ":agent_troop_id", 1),
         (try_end),
       (else_try),
         (party_add_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_begin),
           (agent_is_wounded, ":cur_agent"),
           (party_wound_members, "p_enemy_casualties", ":agent_troop_id", 1),
         (try_end),
       (try_end),
     (try_end),
     ]),

  #script_get_max_skill_of_player_party
  # INPUT: arg1 = skill_no
  # OUTPUT: reg0 = max_skill, reg1 = skill_owner_troop_no
  ("get_max_skill_of_player_party",
    [(store_script_param, ":skill_no", 1),
     (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
     (store_skill_level, ":max_skill", ":skill_no", "trp_player"),
     (assign, ":skill_owner", "trp_player"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (party_stack_get_troop_id, ":stack_troop","p_main_party",":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (neg|troop_is_wounded, ":stack_troop"),
       (store_skill_level, ":cur_skill", ":skill_no", ":stack_troop"),
       (gt, ":cur_skill", ":max_skill"),
       (assign, ":max_skill", ":cur_skill"),
       (assign, ":skill_owner", ":stack_troop"),
     (try_end),
     (party_get_skill_level, reg0, "p_main_party", ":skill_no"),
##     (assign, reg0, ":max_skill"),
     (assign, reg1, ":skill_owner"),
     ]),

  #script_upgrade_hero_party
  # INPUT: arg1 = improvement
  # OUTPUT: reg0 = base_cost
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

  #script_cf_troop_agent_is_alive
  # INPUT: arg1 = troop_id
  ("cf_troop_agent_is_alive",
    [(store_script_param, ":troop_no", 1),
     (assign, ":alive_count", 0),
     (try_for_agents, ":cur_agent"),
       (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
       (eq, ":troop_no", ":cur_agent_troop"),
       (agent_is_alive, ":cur_agent"),
       (val_add, ":alive_count", 1),
     (try_end),
     (gt, ":alive_count", 0),
     ]),

    # INPUT: arg1 = troop_no, arg2 = item_no
  # OUTPUT: reg0 = item_amount
  ("get_troop_item_amount",
    [(store_script_param, ":troop_no", 1),
     (store_script_param, ":item_no", 2),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (assign, ":count", 0),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
       (eq, ":cur_item", ":item_no"),
       (val_add, ":count", 1),
     (try_end),
     (assign, reg0, ":count"),
     ]),

  #script_get_name_from_dna_to_s50
  # INPUT: arg1 = dna
  # OUTPUT: s50 = name
  ("get_name_from_dna_to_s50",
    [(store_script_param, ":dna", 1),
     (store_sub, ":num_names", names_end, names_begin),
     (store_sub, ":num_surnames", surnames_end, surnames_begin),
     (assign, ":selected_name", ":dna"),
     (val_mod, ":selected_name", ":num_names"),
     (assign, ":selected_surname", ":dna"),
     (val_div, ":selected_surname", ":num_names"),
     (val_mod, ":selected_surname", ":num_surnames"),
     (val_add, ":selected_name", names_begin),
     (val_add, ":selected_surname", surnames_begin),
     (str_store_string, s50, ":selected_name"),
     (str_store_string, s50, ":selected_surname"),
     ]),

  #script_change_center_prosperity
  # INPUT: arg1 = troop_no, arg2 = amount
  # OUTPUT: none
  ("troop_add_gold",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":amount", 2),

      (troop_add_gold, ":troop_no", ":amount"),
      (try_begin),
        (eq, ":troop_no", "trp_player"),
        (play_sound, "snd_money_received"),
      (try_end),
     ]),

#NPC companion changes begin
("objectionable_action",
    [
        (store_script_param_1, ":action_type"),
        (store_script_param_2, ":action_string"),

        (assign, ":grievance_minimum", -2),
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),

###Primary morality check
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),

###Secondary morality check
            (else_try),
                (troop_slot_eq, ":npc", slot_troop_2ary_morality_type, ":action_type"),
                (troop_get_slot, ":value", ":npc", slot_troop_2ary_morality_value),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_acknowledged),
# npc is betrayed, major penalty to player honor and morale
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_mul, ":value", 2),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
                    (this_or_next|troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_dismissed),
                        (eq, "$disable_npc_complaints", 1),
# npc is quietly disappointed
                    (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                    (val_add, ":grievance", ":value"),
                    (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),
                (else_try),
# npc raises the issue for the first time
                    (troop_slot_eq, ":npc", slot_troop_2ary_morality_state, tms_no_problem),
                    (gt, ":value", ":grievance_minimum"),
                    (assign, "$npc_with_grievance", ":npc"),
                    (assign, "$npc_grievance_string", ":action_string"),
                    (assign, "$npc_grievance_slot", slot_troop_2ary_morality_state),
                    (assign, ":grievance_minimum", ":value"),
                    (assign, "$npc_praise_not_complaint", 0),
                    (try_begin),
                        (lt, ":value", 0),
                        (assign, "$npc_praise_not_complaint", 1),
                    (try_end),
                (try_end),
            (try_end),

            (try_begin),
                (gt, "$npc_with_grievance", 0),
                (eq, "$npc_praise_not_complaint", 0),
                (str_store_troop_name, 4, "$npc_with_grievance"),
                (display_message, "@{s4} looks upset.", message_alert),
            (try_end),
        (try_end),
     ]),


  ("post_battle_personality_clash_check",
[
            (try_for_range, ":npc", companions_begin, companions_end),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),

#                (store_random_in_range, ":random", 0, 3),
                (try_begin),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash2_state, 0),
                    (try_begin),
#                        (eq, ":random", 0),
                        (assign, "$npc_with_personality_clash_2", ":npc"),
                    (try_end),
                (try_end),

            (try_end),

            (try_for_range, ":npc", companions_begin, companions_end),
                (troop_slot_eq, ":npc", slot_troop_personalitymatch_state, 0),
                (eq, "$disable_npc_complaints", 0),

                (main_party_has_troop, ":npc"),
                (neg|troop_is_wounded, ":npc"),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_personalitymatch_object),
                (main_party_has_troop, ":other_npc"),
                (neg|troop_is_wounded, ":other_npc"),
                (assign, "$npc_with_personality_match", ":npc"),
            (try_end),


            (try_begin),
                (gt, "$npc_with_personality_clash_2", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(display_message, "str_personality_clash_conversation_begins"),
				(try_end),

				(try_begin),
					(main_party_has_troop, "$npc_with_personality_clash_2"),
					(assign, "$npc_map_talk_context", slot_troop_personalityclash2_state),
					(start_map_conversation, "$npc_with_personality_clash_2"),
				(else_try),
					(assign, "$npc_with_personality_clash_2", 0),
				(try_end),
            (else_try),
                (gt, "$npc_with_personality_match", 0),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(display_message, "str_personality_match_conversation_begins"),
				(try_end),

				(try_begin),
					(main_party_has_troop, "$npc_with_personality_match"),
					(assign, "$npc_map_talk_context", slot_troop_personalitymatch_state),
					(start_map_conversation, "$npc_with_personality_match"),
				(else_try),
					(assign, "$npc_with_personality_match", 0),
				(try_end),
			(try_end),
     ]),

  #script_event_player_defeated_enemy_party
  # INPUT: none
  # OUTPUT: none
  ("event_player_defeated_enemy_party",
    [(try_begin),
       (check_quest_active, "qst_raid_caravan_to_start_war"),
       (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
       (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_caravan),
       (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
       (quest_slot_eq, "qst_raid_caravan_to_start_war", slot_quest_target_faction, ":enemy_faction"),
       (quest_get_slot, ":cur_state", "qst_raid_caravan_to_start_war", slot_quest_current_state),
       (quest_get_slot, ":quest_target_amount", "qst_raid_caravan_to_start_war", slot_quest_target_amount),
       (val_add, ":cur_state", 1),
       (quest_set_slot, "qst_raid_caravan_to_start_war", slot_quest_current_state, ":cur_state"),
       (try_begin),
         (ge, ":cur_state", ":quest_target_amount"),
         (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
         (quest_get_slot, ":quest_giver_troop", "qst_raid_caravan_to_start_war", slot_quest_giver_troop),
         (store_troop_faction, ":quest_giver_faction", ":quest_giver_troop"),
         (call_script, "script_diplomacy_start_war_between_kingdoms", ":quest_target_faction", ":quest_giver_faction", 1),
         (call_script, "script_succeed_quest", "qst_raid_caravan_to_start_war"),
       (try_end),
     (try_end),

     ]),

  #script_event_player_captured_as_prisoner
  # INPUT: none
  # OUTPUT: none
  ("event_player_captured_as_prisoner",
    [
        (try_begin),
          (check_quest_active, "qst_raid_caravan_to_start_war"),
          (neg|check_quest_concluded, "qst_raid_caravan_to_start_war"),
          (quest_get_slot, ":quest_target_faction", "qst_raid_caravan_to_start_war", slot_quest_target_faction),
          (store_faction_of_party, ":capturer_faction", "$capturer_party"),
          (eq, ":quest_target_faction", ":capturer_faction"),
          (call_script, "script_fail_quest", "qst_raid_caravan_to_start_war"),
        (try_end),
        #Removing followers of the player
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),
          (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
          (party_slot_eq, ":party_no", slot_party_ai_object, "p_main_party"),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
          (assign, "$g_recalculate_ais", 1),
        (try_end),
     ]),

#NPC morale both returns a string and reg0 as the morale value

  #script_calculate_ransom_amount_for_troop
  # INPUT: arg1 = troop_no
  # OUTPUT: reg0 = ransom_amount
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

  #script_offer_ransom_amount_to_player_for_prisoners_in_party
  # INPUT: arg1 = party_no
  # OUTPUT: reg0 = result (1 = offered, 0 = not offered)
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

  # script_event_hero_taken_prisoner_by_player
  # Input: arg1 = party_no
  # Output: troop_id that has been removed (can fail)
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

  # script_place_player_banner_near_inventory
  # Input: arg1 = num_hours
  # Output: none
  ("stay_captive_for_hours",
    [
      (store_script_param, ":num_hours", 1),
      (store_current_hours, ":cur_hours"),
      (val_add, ":cur_hours", ":num_hours"),
      (val_max, "$g_check_autos_at_hour", ":cur_hours"),
      (val_add, ":num_hours", 1),
      (rest_for_hours, ":num_hours", 0, 0),
    ]),

  # script_set_parties_around_player_ignore_player
  # Input: arg1 = ignore_range, arg2 = num_hours_to_ignore
  # Output: none
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

  # script_randomly_make_prisoner_heroes_escape_from_party
  # Input: arg1 = village_no
  # Output: reg0 = max_amount
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


  # script_draw_banner_to_region
  # Input: arg1 = color_1, arg2 = color_2
  # Output: none
  ("cf_check_color_visibility",
    [
      (store_script_param, ":color_1", 1),
      (store_script_param, ":color_2", 2),
      (store_mod, ":blue_1", ":color_1", 256),
      (store_div, ":green_1", ":color_1", 256),
      (val_mod, ":green_1", 256),
      (store_div, ":red_1", ":color_1", 256 * 256),
      (val_mod, ":red_1", 256),
      (store_mod, ":blue_2", ":color_2", 256),
      (store_div, ":green_2", ":color_2", 256),
      (val_mod, ":green_2", 256),
      (store_div, ":red_2", ":color_2", 256 * 256),
      (val_mod, ":red_2", 256),
      (store_sub, ":red_dif", ":red_1", ":red_2"),
      (val_abs, ":red_dif"),
      (store_sub, ":green_dif", ":green_1", ":green_2"),
      (val_abs, ":green_dif"),
      (store_sub, ":blue_dif", ":blue_1", ":blue_2"),
      (val_abs, ":blue_dif"),
      (assign, ":max_dif", 0),
      (val_max, ":max_dif", ":red_dif"),
      (val_max, ":max_dif", ":green_dif"),
      (val_max, ":max_dif", ":blue_dif"),
      (ge, ":max_dif", 64),
     ]),

  # script_get_next_active_kingdom
  # Input: arg1 = faction_no
  # Output: reg0 = faction_no (does not choose player faction)
  ("get_next_active_kingdom",
    [
      (store_script_param, ":faction_no", 1),
      (assign, ":end_cond", kingdoms_end),
      (try_for_range, ":unused", kingdoms_begin, ":end_cond"),
        (val_add, ":faction_no", 1),
        (try_begin),
          (ge, ":faction_no", kingdoms_end),
          (assign, ":faction_no", kingdoms_begin),
        (try_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", "fac_player_supporters_faction"),
        (assign, ":end_cond", 0),
      (try_end),
      (assign, reg0, ":faction_no"),
     ]),

#  # script_store_average_center_value_per_faction
#  # Input: none
#  # Output: none (sets $g_average_center_value_per_faction)
#  ("store_average_center_value_per_faction",
#    [
#      (store_sub, ":num_towns", towns_end, towns_begin),
#      (store_sub, ":num_castles", castles_end, castles_begin),
#      (assign, ":num_factions", 0),
#      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
#        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
#        (val_add, ":num_factions", 1),
#      (try_end),
#      (val_max, ":num_factions", 1),
#      (store_mul, "$g_average_center_value_per_faction", ":num_towns", 2),
#      (val_add, "$g_average_center_value_per_faction", ":num_castles"),
#      (val_mul, "$g_average_center_value_per_faction", 10),
#      (val_div, "$g_average_center_value_per_faction", ":num_factions"),
#     ]),

  # script_remove_cattles_if_herd_is_close_to_party
  # Input: arg1 = party_no, arg2 = maximum_number_of_cattles_required
  # Output: reg0 = number_of_cattles_removed
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

  # script_get_rumor_to_s61
  # Input: rumor_id
  # Output: reg0 = 1 if rumor found, 0 otherwise; s61 will contain rumor string if found
  ("get_rumor_to_s61",
    [
     (store_script_param, ":base_rumor_id", 1), # the script returns the same rumor for the same rumor id, so that one cannot hear all rumors by
                                                # speaking to a single person.
     ##diplomacy start+ save reg4 in order to revert it at the end of the script
	 (assign, ":save_reg4", reg4),
	 ##diplomacy end+
     (store_current_hours, ":cur_hours"),
     (store_div, ":cur_day", ":cur_hours", 24),
     (assign, ":rumor_found", 0),
     (assign, ":num_tries", 3),
     (try_for_range, ":try_no", 0, ":num_tries"),
       (store_mul, ":rumor_id", ":try_no", 6781),
       (val_add, ":rumor_id", ":base_rumor_id"),
       (store_mod, ":rumor_type", ":rumor_id", 7),
       (val_add, ":rumor_id", ":cur_hours"),
       (try_begin),
         (eq,  ":rumor_type", 0),
         (try_begin),
           (store_sub, ":range", towns_end, towns_begin),
           (store_mod, ":random_center", ":rumor_id", ":range"),
           (val_add, ":random_center", towns_begin),
           (party_slot_ge, ":random_center", slot_town_has_tournament, 1),
           (neq, ":random_center", "$current_town"),
           (str_store_party_name, s62, ":random_center"),
           (str_store_string, s61, "@I heard that there will be a tournament in {s62} soon."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 1),
         (try_begin),
           (store_sub, ":range", active_npcs_end, original_kingdom_heroes_begin), #was reversed
           (store_mod, ":random_hero", ":rumor_id", ":range"),
           (val_add, ":random_hero", original_kingdom_heroes_begin),
		   (is_between, ":random_hero", active_npcs_begin, active_npcs_end),
           (troop_get_slot, ":personality", ":random_hero", slot_lord_reputation_type),
		   ##diplomacy start+ give rumors for non-noble personalities, and make pronouns gender-correct
		   (try_begin),
		      (ge, ":personality", lrep_roguish),
			  (try_begin),
			    (eq, ":personality", lrep_benefactor),#Ymira, Bunduk, Jeremus
				(assign, ":personality", lrep_goodnatured),#treats people living in his lands decently
			  (else_try),
			    (eq, ":personality", lrep_custodian),#Marnid, Artimenner, Deshavi, Katrin
				(assign, ":personality", lrep_goodnatured),#good to his followers, and rewards them if they work well
			  (else_try),
			    (call_script, "script_dplmc_get_troop_morality_value", ":random_hero", tmt_humanitarian),
				(lt, reg0, 0),#Klethi
				(assign, ":personality", lrep_debauched),#likes to torture his enemies
			  (try_end),
			  (ge, ":personality", lrep_roguish),
			  (assign, ":personality", 0),#zero out to avoid jumping to a nonsensical string
		   (try_end),
		   (call_script, "script_dplmc_store_troop_is_female_reg", ":random_hero", 4),#store gender to reg4 to make pronouns gender-correct
		   ##diplomacy end+
           (gt, ":personality", 0),
           (store_add, ":rumor_string", ":personality", "str_gossip_about_character_default"),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, ":rumor_string"),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy start+ Change the rumor string in some circumstances to avoid implying the hero is currently ruling a fief
         (try_begin),
           (neg|is_between, ":random_hero", heroes_begin, heroes_end),
         (else_try),
           #Dead
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_dead),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard some people say they don't believe {s6} is really dead."),#The doubters are wrong, like with Tupac or Elvis.
           (assign, ":rumor_found", 1),
         (else_try),
           #In exile
           (this_or_next|troop_slot_eq, ":random_hero", slot_troop_occupation, slto_retirement),
           (troop_slot_eq, ":random_hero", slot_troop_occupation, dplmc_slto_exile),
           (str_store_troop_name, s6, ":random_hero"),
           (str_store_string, s61, "@I heard a traveller say that he came across {s6} while journeying outside these lands."),
           (assign, ":rumor_found", 1),
         (else_try),
           #Inactive pretender
           (troop_slot_eq, ":random_hero", slot_troop_occupation, slto_inactive_pretender),
           (neq, ":random_hero", "$supported_pretender"),
           (troop_get_slot, reg4, ":random_hero", slot_troop_original_faction),
           (is_between, reg4, npc_kingdoms_begin, npc_kingdoms_end),
           (faction_slot_eq, reg4, slot_faction_state, sfs_active),
           (faction_get_slot, reg4, reg4, slot_faction_leader),
           (gt, reg4, -1),
           (str_store_troop_name, s61, reg4),
           (str_store_string, s6, ":random_hero"),
           (str_store_string, s61, "@I heard that {s6} intends to raise an army and seize the throne from {s61}."),
           (assign, ":rumor_found", 1),
         (try_end),
         ##diplomacy end+
       (else_try),
         (eq,  ":rumor_type", 2),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":min_price", average_price_factor, 3),
           (val_div, ":min_price", 4),
           (assign, ":min_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (lt, ":cur_price", ":min_price"),
             (assign, ":min_price", ":cur_price"),
             (assign, ":min_price_center", ":random_center"),
           (try_end),
           (ge, ":min_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":min_price_center"),
           (str_store_string, s61, "@I heard that one can buy {s62} very cheap at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (else_try),
         (eq,  ":rumor_type", 3),
         (try_begin),
           (store_sub, ":range", trade_goods_end, trade_goods_begin),
           (store_add, ":random_trade_good", ":rumor_id", ":cur_day"),
           (store_mod, ":random_trade_good", ":random_trade_good", ":range"),
           (store_add, ":random_trade_good_slot", ":random_trade_good", slot_town_trade_good_prices_begin),
           (val_add, ":random_trade_good", trade_goods_begin),
           (store_mul, ":max_price", average_price_factor, 5),
           (val_div, ":max_price", 4),
           (assign, ":max_price_center", -1),
           (try_for_range, ":sub_try_no", 0, 10),
             (store_sub, ":range", towns_end, towns_begin),
             (store_add, ":center_rumor_id", ":rumor_id", ":sub_try_no"),
             (store_mod, ":random_center", ":center_rumor_id", ":range"),
             (val_add, ":random_center", towns_begin),
             (neq, ":random_center", "$g_encountered_party"),
             (party_get_slot, ":cur_price", ":random_center", ":random_trade_good_slot"),
             (gt, ":cur_price", ":max_price"),
             (assign, ":max_price", ":cur_price"),
             (assign, ":max_price_center", ":random_center"),
           (try_end),
           (ge, ":max_price_center", 0),
           (str_store_item_name, s62, ":random_trade_good"),
           (str_store_party_name, s63, ":max_price_center"),
           (str_store_string, s61, "@I heard that they pay a very high price for {s62} at {s63}."),
           (assign, ":rumor_found", 1),
         (try_end),
       (try_end),
       (try_begin),
         (gt, ":rumor_found", 0),
         (assign, ":num_tries", 0),
       (try_end),
     (try_end),
     (assign, reg0, ":rumor_found"),
	 ##diplomacy start+ revert reg4
	 (assign, reg4, ":save_reg4"),
	 ##diplomacy end+
     ]),

  
  # script_add_log_entry
  # Input: arg1 = entry_type, arg2 = event_actor, arg3 = center_object, arg4 = troop_object, arg5 = faction_object
  # Output: none
  ("add_log_entry",
    [(store_script_param, ":entry_type", 1),
     (store_script_param, ":actor", 2),
     (store_script_param, ":center_object", 3),
     (store_script_param, ":troop_object", 4),
     (store_script_param, ":faction_object", 5),
     (assign, ":center_object_lord", -1),
     (assign, ":center_object_faction", -1),
     (assign, ":troop_object_faction", -1),

     (try_begin),
       (party_is_active, ":center_object", 0),
       (party_get_slot, ":center_object_lord", ":center_object", slot_town_lord),
       (store_faction_of_party, ":center_object_faction", ":center_object"),
	 (else_try),
	   (assign, ":center_object_lord", 0),
       (assign, ":center_object_faction", 0),
     (try_end),

     (try_begin),
       (is_between, ":troop_object", 0, "trp_local_merchant"),
       (store_troop_faction, ":troop_object_faction", ":troop_object"),
	 (else_try),
	   (assign, ":troop_object_faction", 0),
     (try_end),

     (val_add, "$num_log_entries", 1),

     (store_current_hours, ":entry_time"),
     (troop_set_slot, "trp_log_array_entry_type",            "$num_log_entries", ":entry_type"),
     (troop_set_slot, "trp_log_array_entry_time",            "$num_log_entries", ":entry_time"),
     (troop_set_slot, "trp_log_array_actor",                 "$num_log_entries", ":actor"),
     (troop_set_slot, "trp_log_array_center_object",         "$num_log_entries", ":center_object"),
     (troop_set_slot, "trp_log_array_center_object_lord",    "$num_log_entries", ":center_object_lord"),
     (troop_set_slot, "trp_log_array_center_object_faction", "$num_log_entries", ":center_object_faction"),
     (troop_set_slot, "trp_log_array_troop_object",          "$num_log_entries", ":troop_object"),
     (troop_set_slot, "trp_log_array_troop_object_faction",  "$num_log_entries", ":troop_object_faction"),
     (troop_set_slot, "trp_log_array_faction_object",        "$num_log_entries", ":faction_object"),

     (try_begin),
       (eq, "$cheat_mode", 1),
       (assign, reg3, "$num_log_entries"),
       (assign, reg4, ":entry_type"),
       (display_message, "@{!}Log entry {reg3}: type {reg4}"),
       (try_begin),
          (gt, ":center_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),
		  (party_is_active, ":center_object"), #sometimes is a troop

          (str_store_party_name, s4, ":center_object"),
          (display_message, "@{!}Center: {s4}"),
       (try_end),
       (try_begin),
          (gt, ":troop_object", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),

		  (str_store_troop_name, s4, ":troop_object"),
		  (display_message, "@{!}Troop: {s4}"),
       (try_end),
       (try_begin),
          (gt, ":center_object_lord", 0),
		  (neq, ":entry_type", logent_traveller_attacked),
		  (neq, ":entry_type", logent_party_traded),

		  (str_store_troop_name, s4, ":center_object_lord"),
          (display_message, "@{!}Lord: {s4}"),
       (try_end),
     (try_end),


     (try_begin),
	   (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
       (this_or_next|eq, ":entry_type", logent_player_participated_in_major_battle),
		(eq, ":entry_type", logent_player_participated_in_siege),

       (try_begin),
         (eq, "$cheat_mode", 1),
         (display_message, "@{!}Ally party is present"),
       (try_end),
	   ##diplomacy start+ support kingdom ladies as well
       #(try_for_range, ":hero", active_npcs_begin, active_npcs_end),
	   (try_for_range, ":hero", heroes_begin, heroes_end),
	     (this_or_next|is_between, ":hero", active_npcs_begin, active_npcs_end),
	     (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
		 (this_or_next|troop_slot_eq, ":hero", slot_troop_occupation, slto_player_companion),
		    (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_seneschal),
	   ##diplomacy end+
         (party_count_companions_of_type, ":hero_present", "p_collective_friends", ":hero"),
         (gt, ":hero_present", 0),
         (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"),
#         (store_sub, ":skip_up_to_here", "$num_log_entries", 1),
#         (troop_set_slot, ":hero", slot_troop_last_comment_slot, ":skip_up_to_here"),
         (try_begin),
           (eq, "$cheat_mode", 1),
           (str_store_troop_name, s4, ":hero"),
           (display_message, "@{!}{s4} is present at event"),
         (try_end),
       (try_end),
     (else_try), #SB : log kingdom policy changes as well
        (eq, ":entry_type", logent_player_renamed_capital),
        (party_clear, "p_temp_party"),
        (call_script, "script_get_heroes_attached_to_center", ":center_object", "p_temp_party"),
        (party_get_num_companion_stacks, ":num_stacks","p_temp_party"),
        (try_for_range, ":stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":hero", "p_temp_party", ":stack"),
          (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"), #need to check if this gets called before or after, add +1
        (try_end),
        #they can give their opinion in the feast, although comment strings aren't set up.
     (try_end),
     ]),


  # script_get_relevant_comment_for_log_entry
  # Input: arg1 = log_entry_no,
  # Output: reg0 = comment_id; reg1 = relevance
  # Notes: 50 is the default relevance.
  # A comment with relevance less than 30 will always be skipped.
  # A comment with relevance 75 or more will never be skipped.
  # A comment with relevance 50 has about 50% chance to be skipped.
  # If there is more than one comment that is not skipped, the system will randomize their relevance values, and then choose the highest one.
  # Also note that the relevance of events decreases as time passes. After three months, relevance reduces to 50%, after 6 months, 25%, etc...
  ##diplomacy start+
  ##May also set reg4 or reg3 to correspond to gender
  ##diplomac end+
  ("get_relevant_comment_for_log_entry",
    [(store_script_param, ":log_entry_no", 1),

     (troop_get_slot, ":entry_type",            "trp_log_array_entry_type",            ":log_entry_no"),
     (troop_get_slot, ":entry_time",            "trp_log_array_entry_time",            ":log_entry_no"),
     (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":log_entry_no"),
     (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":log_entry_no"),
     (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":log_entry_no"),
     (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":log_entry_no"),
     (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":log_entry_no"),
     (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":log_entry_no"),
     (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":log_entry_no"),

     (assign, ":relevance", 0),
     (assign, ":comment", -1),
     (assign, ":rejoinder", -1),
     (assign, ":suggested_relation_change", 0),

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
	 ##diplomacy start+
	 (assign, ":return_reg4", reg4),
	 #Set an initial value for ":return_reg4", although further down
	 #some specific log types override this.
	 (try_begin),
		(is_between, ":troop_object", heroes_begin, heroes_end),
		(neq, ":troop_object", "$g_talk_troop"),
		(assign, ":return_reg4", 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
			(assign, ":return_reg4", 1),
		(try_end),
	 (else_try),
		(is_between, ":actor", heroes_begin, heroes_end),
		(neq, ":actor", "$g_talk_troop"),
		(assign, ":return_reg4", 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", ":actor"),
			(assign, ":return_reg4", 1),
		(try_end),
	 (try_end),


	 #add support for commoner/lady reputations
     (troop_get_slot, ":true_reputation", "$g_talk_troop", slot_lord_reputation_type),#unmodified value
	 #(troop_get_type, ":talk_troop_gender",  "$g_talk_troop"),
	 (call_script, "script_dplmc_store_troop_is_female", "$g_talk_troop"),
	 (assign, ":talk_troop_gender", reg0),
	 (try_begin),
	    (neg|is_between, ":reputation", lrep_none, lrep_upstanding + 1),#<-- no changes are required for standard lord personalities
		(try_begin),
			(eq, ":true_reputation", lrep_ambitious),
			(assign, ":reputation", lrep_cunning),
		(else_try),
			(eq, ":true_reputation", lrep_moralist),
			(assign, ":reputation", lrep_upstanding),
		(else_try),
			(this_or_next|eq, ":true_reputation", lrep_conventional),
			   (this_or_next|eq, ":true_reputation", lrep_otherworldly),
			   (eq, ":true_reputation", lrep_benefactor),
			(assign, ":reputation", lrep_goodnatured),
		(try_end),
	 (try_end),
	 ##diplomacy end+
     (store_current_hours, ":current_time"),
     (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),

#Post 0907 changes begin
     (assign, ":players_kingdom_relation", 0), ##the below is so that lords will not congratulate player on attacking neutrals
     (try_begin),
        (gt, "$players_kingdom", 0),
        (gt, ":troop_object_faction", 0),
		(store_relation, ":players_kingdom_relation", "$players_kingdom", ":troop_object_faction"),
     (try_end),

     (try_begin),
       (eq, "$cheat_mode", -1), #temporarily disabled
       (try_begin),
         (assign, reg5, ":log_entry_no"),
         (assign, reg6, ":entry_type"),
         (assign, reg8, ":entry_time"),

         (gt, "$players_kingdom", 0),
         (try_begin),
            (gt, ":troop_object_faction", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to troop object = {reg7}"),
         (else_try),
            (gt, ":center_object_faction", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to center object faction = {reg7}"),
         (else_try),
            (gt, ":faction_object", 0),
            (assign, reg7, ":players_kingdom_relation"),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}: player's kingdom relation to faction object = {reg7}"),
         (else_try),
            (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}. No relevant kingdom relation"),
         (try_end),
       (else_try),
         (display_message, "@{!}Event #{reg5}, type {reg6}, time {reg8}. Player unaffiliated"),
       (try_end),
     (try_end),

     ##diplomacy start+
	 #In Native, it's assumed that anyone with lrep_none is a liege, but that isn't alwasys true.
	 #(For example, it's possible in a Native game for a defeated pretender to end up as the vassal
	 #of an NPC lord (!), but still talk as if they're ruling a kingdom.)
	 #  Instead of just relying on personality for this, explicily check if they're a liege.
	 (call_script, "script_dplmc_get_troop_standing_in_faction", "$g_talk_troop", "$g_talk_troop_faction"),
	 (try_begin),
		 (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		 (assign, ":speaker_is_a_liege", 1),
	 (else_try),
	     (assign, ":speaker_is_a_liege", 0),
	 (try_end),
	 ##diplomacy end+
     (try_begin),
       (eq, ":entry_type", logent_game_start),
       (eq, "$g_talk_troop_met", 0),
       (is_between, "$g_talk_troop_faction_relation", -5, 5),
       (is_between, "$g_talk_troop_relation", -5, 5),

       (assign, ":relevance", 25),
       (troop_get_slot, ":plyr_renown", "trp_player", slot_troop_renown),
		##diplomacy start+
		(try_begin),
			(lt, "$g_disable_condescending_comments", 0),#prejudice mode: high
			(call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),#bias against gender
			#80% renown
			(val_mul, ":plyr_renown", 4),
			(val_add, ":plyr_renown", 3),
			(val_div, ":plyr_renown", 5),
		(try_end),
		##diplomacy end+
#normal_banner_begin
       (troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
#custom_banner_begin
       (try_begin),
           (eq, ":banner", -1),
           (troop_get_slot, ":banner", "trp_player", slot_troop_custom_banner_flag_type),
       (try_end),
       (store_random_in_range, ":renown_check", 100, 200),
       (try_begin),
	      ##diplomacy start+
		  (gt, ":speaker_is_a_liege", 0),#Explicitly check if the speaker is a liege rather than relying solely on reputation
		  ##diplomacy end+
          (eq, ":reputation", lrep_none),
          (gt, "$players_kingdom", 0),
          (assign, ":comment", "str_comment_intro_liege_affiliated"),
		  (try_begin),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(assign, ":comment", "str_comment_intro_liege_affiliated_to_player"),
		  (try_end),
	   (else_try),
	      ##diplomacy start+
		  ##OLD:
		  #(eq, "$character_gender",tf_female),
		  ##NEW:
		  #Instead of assuming there's anti-female bias in all settings, check on a kingdom-by-kingdom basis.
		  (call_script, "script_cf_dplmc_faction_has_bias_against_gender", "$g_talk_troop_faction", "$character_gender"),
		  ##diplomacy end+

		  (call_script, "script_troop_get_romantic_chemistry_with_troop", "$g_talk_troop", "trp_player"),
		  (assign, ":attraction", reg0),
		  (store_random_in_range, ":random", 0, 2),
		  (this_or_next|eq, ":random", 0),
			  (gt, ":attraction", 10),
          ##diplomacy start+ disable remarks about women if the speaker is a woman (or visa versa, for settings with biases against men)
		  (this_or_next|gt, ":attraction", 10),
			(neq, ":talk_troop_gender", "$character_gender"),
		  ##diplomacy end+
		  (try_begin),
            (this_or_next|gt, ":plyr_renown", ":renown_check"),
			##diplomacy start+
			#	(eq, "$g_disable_condescending_comments", 1),
			    (ge, "$g_disable_condescending_comments", 1),
			##diplomacy end+
            (assign, ":comment", "str_comment_intro_female_famous_liege"),
            (val_add, ":comment", ":reputation"),
		  (else_try),
		    (ge, ":attraction", 9),
			(assign, ":comment", "str_comment_intro_female_admiring_liege"),
			(val_add, ":comment", ":reputation"),
		  (else_try),
            (gt, ":banner", 0),
			(assign, ":comment", "str_comment_intro_female_noble_liege"),
			(val_add, ":comment", ":reputation"),
		  (else_try),
			(assign, ":comment", "str_comment_intro_female_common_liege"),
			(val_add, ":comment", ":reputation"),
		  (try_end),

		  #Rejoinders for comments
		  (try_begin),
			(eq, ":comment", "str_comment_intro_female_common_badtempered"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_common_badtempered"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_noble_pitiless"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_noble_pitiless"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_common_pitiless"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_common_pitiless"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_noble_sadistic"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_noble_sadistic"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_common_sadistic"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_common_sadistic"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_common_upstanding"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_common_upstanding"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_noble_upstanding"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_noble_upstanding"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_common_martial"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_common_martial"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_sadistic_admiring"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_sadistic_admiring"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_badtempered_admiring"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_badtempered_admiring"),
		  (else_try),
			(eq, ":comment", "str_comment_intro_female_pitiless_admiring"),
			(assign, ":rejoinder", "str_rejoinder_intro_female_pitiless_admiring"),
		  (try_end),

	   (else_try),
		  #Male character or non-gendered comment
		  (try_begin),
			(gt, ":plyr_renown", ":renown_check"),
            (assign, ":comment", "str_comment_intro_famous_liege"),
            (val_add, ":comment", ":reputation"),
		  (else_try),
            (gt, ":banner", 0),
			(assign, ":comment", "str_comment_intro_noble_liege"),
			(val_add, ":comment", ":reputation"),

			(try_begin),
				(eq, ":comment", "str_comment_intro_noble_sadistic"),
				(assign, ":rejoinder", "str_rejoinder_intro_noble_sadistic"),
			(try_end),

          (else_try),
            (assign, ":comment", "str_comment_intro_common_liege"),
            (val_add, ":comment", ":reputation"),
		  (try_end),
       (try_end),
#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_village_raided),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_raided_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_raided_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_raided_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_raided_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_village_extorted),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 30),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_robbed_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_robbed_my_village_enemy"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_robbed_my_village_friendly"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_caravan_accosted),
       (eq, ":actor", "trp_player"),
       (eq, ":faction_object", "$g_talk_troop_faction"),
           (eq, ":center_object", -1),
           (eq, ":troop_object", -1),



       (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":relevance", 30),
       (assign, ":suggested_relation_change", -1),
       (assign, ":comment", "str_comment_you_accosted_my_caravan_default"),
       (try_begin),
            (lt, "$g_talk_troop_faction_relation", -5),
            (assign, ":comment", "str_comment_you_accosted_my_caravan_enemy"),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_helped_peasants),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 40),
         (assign, ":suggested_relation_change", 0),
         (try_begin),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_helped_villagers_benevolent"),
            (assign, ":suggested_relation_change", 1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_unfriendly_spiteful"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_you_helped_villagers_friendly"),
         (else_try),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_helped_villagers_cruel"),
            (assign, ":suggested_relation_change", -1),
         (else_try),
             (assign, ":comment", "str_comment_you_helped_villagers_default"),
         (try_end),
       (try_end),

###Combat events
     (else_try),
       (eq, ":entry_type", logent_castle_captured_by_player),

       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),

         (this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_debauched),

         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),

         (this_or_next|eq, ":reputation", lrep_martial),
			(eq, ":reputation", lrep_goodnatured),

         (assign, ":comment", "str_comment_you_captured_my_castle_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":center_object_lord", "$g_talk_troop"),
		 (store_faction_of_party, ":current_center_faction", ":center_object"),
		 (eq, ":current_center_faction", "$players_kingdom"),
		 (neq, "$g_talk_troop_faction", "$players_kingdom"),

         (assign, ":comment", "str_comment_you_captured_my_castle_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_friendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly_spiteful"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied_unfriendly"),
         (assign, ":relevance", 75),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_captured_a_castle_allied"),
         (assign, ":relevance", 75),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_claims_throne_1),
       (eq, "$players_kingdom", "$g_talk_troop_faction"),
	   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":comment", "str_comment_you_claimed_the_throne_1_player_liege"),
       (assign, ":relevance", 500),
       (lt, "$g_talk_troop_relation", -10),

     (else_try),
       (eq, ":entry_type", logent_player_claims_throne_2),
       (eq, "$players_kingdom", "$g_talk_troop_faction"),
	   (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
       (assign, ":comment", "str_comment_you_claimed_the_throne_2_player_liege"),
       (assign, ":relevance", 500),
       (lt, "$g_talk_troop_relation", -10),

     (else_try), #player appointed a commoner
       (eq, ":entry_type", logent_liege_grants_fief_to_vassal),
	   (eq, ":actor", "trp_player"),
           (troop_slot_ge, ":troop_object", slot_lord_reputation_type, lrep_roguish),
           ##diplomacy start+
           (neq, ":troop_object", "trp_npc13"),#Nizar isn't a commoner
		   (neg|troop_slot_ge, ":troop_object", slot_lord_reputation_type, lrep_conventional),#ladies aren't commoners
		   (assign, ":return_reg4", 0),
		   (try_begin),
			  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
			  (assign, ":return_reg4", 1),
		   (try_end),
           ##diplomacy end+
       (try_begin),
	   ##diplomacy start+
	      #Companions: make a supportive remark if the person is compatible with you
	      (is_between, "$g_talk_troop", companions_begin, companions_end),
	      (troop_slot_eq, "$g_talk_troop", slot_troop_personalitymatch_object, ":troop_object"),
	      (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
	      (assign, ":relevance", 100),
	      (assign, ":suggested_relation_change", 0),
	   (else_try),
		   #Make a supportive remark if you like the person a lot (overrides objections)
		   (call_script, "script_troop_get_relation_with_troop", ":troop_object", "$g_talk_troop"),
 	       (ge, reg0, 50),
		   (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
		   (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", 0),
	   (else_try),
	       #Make a supportive remark if you like the person and wouldn't ordinarily object
		   (ge, reg0, 20),
		   (this_or_next|is_between, ":true_reputation", lrep_roguish, lrep_conventional),
		   (this_or_next|eq, ":reputation", lrep_cunning),
		   (eq, ":reputation", lrep_goodnatured),
		   (assign, ":comment", "str_dplmc_comment_you_enfiefed_a_commoner_supportive"),
		   (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", 0),
	   (else_try),
	       #Don't complain about your own spouse.
		   (troop_slot_eq, "$g_talk_troop", ":troop_object", slot_troop_spouse),
	   (else_try),
		   #Don't complain if you aren't actually a lord.
		   (is_between, ":true_reputation", lrep_roguish, lrep_conventional),
	   (else_try),
	   ##diplomacy end+
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_nasty"),##diplomacy start+ note: this line uses reg4 from above for gender-correct pronoun ##diplomacy end+
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -3),

       (else_try),
		   (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_hesitant"),##diplomacy start+ note: next line uses reg4 from above for gender-correct pronoun ##diplomacy end+
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -2),

       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
			   (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_enfiefed_a_commoner_derisive"),##diplomacy start+ note: next line uses reg4 from above for gender-correct pronoun ##diplomacy end+
           (assign, ":relevance", 100),
		   (assign, ":suggested_relation_change", -4),

       (try_end),

#Post 0907 changes begin
     (else_try),
       (this_or_next|eq, ":entry_type", logent_lord_defeated_by_player),
            (eq, ":entry_type", logent_lord_helped_by_player),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_defeated_a_lord_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),
           (assign, ":comment", "str_comment_we_defeated_a_lord_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_defeated_a_lord_upstanding"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_defeated_a_lord_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (this_or_next|eq, ":entry_type", logent_castle_captured_by_player),
       (eq, ":entry_type", logent_player_participated_in_siege),

       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),

       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
           (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_siege_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
           (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_fought_in_siege_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),
           (assign, ":comment", "str_comment_we_fought_in_siege_quarrelsome"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_siege_upstanding"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 2),
       (else_try),
           (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
		(else_try),
           (assign, ":comment", "str_comment_we_fought_in_siege_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_castle_given_to_lord_by_player),

       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
         (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
         (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_give_castle_in_my_control"),
         (assign, ":relevance", 200),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_participated_in_major_battle),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_quarrelsome),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_cruel"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_upstanding),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_upstanding"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 2),
	   (else_try),
           (assign, ":comment", "str_comment_we_fought_in_major_battle_default"),
           (assign, ":relevance", 150),
		   (assign, ":suggested_relation_change", 1),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_suggestion_succeeded),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_player_suggestion_succeeded"),
         (assign, ":relevance", 200),
		 (assign, ":suggested_relation_change", 3),

	   (try_end),
     (else_try),
       (eq, ":entry_type", logent_player_suggestion_failed),
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_player_suggestion_failed"),
         (assign, ":relevance", 200),
		 (assign, ":suggested_relation_change", -5),

	   (try_end),

#Post 0907 changes end

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 150),
		 (assign, ":suggested_relation_change", 1),

       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_by_player),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_debauched),
             (eq, ":reputation", lrep_quarrelsome),
         (assign, ":comment", "str_comment_you_defeated_me_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_me_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_pragmatic"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_chivalrous"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy_spiteful"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, ":troop_object_faction", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_defeated_my_friend_enemy"),
         (assign, ":relevance", 85),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (faction_slot_eq, "$players_kingdom", slot_faction_leader, "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_liege"),
         (assign, ":relevance", 70),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (assign, ":comment", "str_comment_you_defeated_a_lord_allied"),
         (assign, ":relevance", 65),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_lord_helped_by_player),
       (neq, ":troop_object", "$g_talk_troop"),
       (eq, ":troop_object_faction", "$g_talk_troop_faction"),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_upstanding),
             (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly"),
         (assign, ":relevance", 0),
       (else_try),
	      ##diplomacy start+
		  (gt, ":speaker_is_a_liege", 0),#Explicitly check if the speaker is a liege rather than relying solely on reputation
		  ##diplomacy end+
         (eq, ":reputation", lrep_none),
         (assign, ":comment", "str_comment_you_helped_my_ally_liege"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 3),
       (else_try),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_unfriendly_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_helped_my_ally_spiteful"),
         (assign, ":relevance", 65),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_helped_my_ally_chivalrous"),
         (assign, ":relevance", 65),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_helped_my_ally_default"),
       (try_end),

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly_spiteful"),
           (assign, ":relevance", 150),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (assign, ":comment", "str_comment_we_were_defeated_unfriendly"),
           (assign, ":relevance", 150),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_selfrighteous),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_we_were_defeated_cruel"),
           (assign, ":relevance", 150),
       (else_try),
           (assign, ":comment", "str_comment_we_were_defeated_default"),
           (assign, ":relevance", 150),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_defeated_by_lord),
  	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_spiteful"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_chivalrous"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_benevolent"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_I_defeated_you_enemy_coldblooded"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_I_defeated_you_enemy"),
         (assign, ":relevance", 200),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (gt, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_friendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (lt, "$g_talk_troop_relation", -5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_cruel"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
         (le, "$g_talk_troop_relation", 5),
         (assign, ":comment", "str_comment_you_were_defeated_allied_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_were_defeated_allied_pitiless"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (eq, ":reputation", lrep_upstanding),
         (lt, "$g_talk_troop_relation", -15),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly_upstanding"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, "$g_talk_troop_relation", -10),
         (assign, ":comment", "str_comment_you_were_defeated_allied_unfriendly"),
         (assign, ":relevance", 65),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (assign, ":comment", "str_comment_you_were_defeated_allied"),
         (assign, ":relevance", 65),
       (try_end),
#Post 0907 changes end

#Post 0907 changes begin
     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord),
       (troop_slot_eq, "$g_talk_troop", slot_troop_present_at_event, ":log_entry_no"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":troop_object", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
       (try_begin),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_spiteful"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (eq, ":reputation", lrep_selfrighteous),
           (assign, ":comment", "str_comment_you_abandoned_us_unfriendly_pitiless"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (lt, "$g_talk_troop_relation", -5),
           (this_or_next|eq, ":reputation", lrep_quarrelsome),
               (eq, ":reputation", lrep_debauched),
           (assign, ":comment", "str_comment_you_abandoned_us_spiteful"),
           (assign, ":suggested_relation_change", -5),
       (else_try),
           (eq, ":reputation", lrep_martial),
           (assign, ":comment", "str_comment_you_abandoned_us_chivalrous"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (else_try),
           (this_or_next|eq, ":reputation", lrep_upstanding),
               (eq, ":reputation", lrep_goodnatured),
           (assign, ":comment", "str_comment_you_abandoned_us_benefitofdoubt"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -1),
       (else_try),
           (assign, ":comment", "str_comment_you_abandoned_us_default"),
           (assign, ":relevance", 150),
           (assign, ":suggested_relation_change", -2),
       (try_end),


#Post 0907 changes end

     (else_try),
       (this_or_next|eq, ":entry_type", logent_player_retreated_from_lord),
            (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),

       (eq, ":troop_object", "$g_talk_troop"),
       (try_begin),
         (eq, "$cheat_mode", 1),
         (assign, reg7, ":entry_hours_elapsed"),
         (display_message, "@{!}Elapsed hours: {reg7}"),
       (try_end),
       (gt, ":entry_hours_elapsed", 2),
       (try_begin),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_spiteful"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_chivalrous"),
         (assign, ":relevance", 25),
       (else_try),
         (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_benevolent"),
         (assign, ":relevance", 25),
       (else_try),
         (eq, ":reputation", lrep_cunning),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy_coldblooded"),
         (assign, ":relevance", 25),
       (else_try),
         (assign, ":comment", "str_comment_you_ran_from_me_enemy"),
         (assign, ":relevance", 25),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_player_retreated_from_lord_cowardly),
       ##diplomacy start+  Set reg4 for calling scripts
       (try_begin),
          (neq, ":troop_object", "$g_talk_troop"),
          (assign, ":return_reg4", 0),
          (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
          (assign, ":return_reg4", 1),
       (try_end),
       ##diplomacy end+
       (try_begin),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (eq, ":reputation", lrep_martial),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_chivalrous"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -3),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_upstanding"),
         (assign, ":relevance", 80),
         (assign, ":suggested_relation_change", -1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", 5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_ran_from_foe_allied_spiteful"),
         (assign, ":relevance", 80),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lord_defeated_but_let_go_by_player),
       ##diplomacy start+  Set reg4 for calling scripts
       (try_begin),
          (neq, ":troop_object", "$g_talk_troop"),
          (assign, ":return_reg4", 0),
          (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
          (assign, ":return_reg4", 1),
       (try_end),
       ##diplomacy end+
       (try_begin),
         (eq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_me_go_spiteful"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", -15),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (ge, "$g_talk_troop_faction_relation", 0),
         (assign, ":comment", "str_comment_you_let_me_go_default"),
         (assign, ":relevance", 300),
         (assign, ":suggested_relation_change", 2),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_upstanding),
         (assign, ":suggested_relation_change", 5),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_chivalrous"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (this_or_next|eq, ":reputation", lrep_selfrighteous),
             (eq, ":reputation", lrep_cunning),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy_coldblooded"),
       (else_try),
         (eq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_faction_relation", 0),
         (assign, ":relevance", 300),
         (assign, ":comment", "str_comment_you_let_me_go_enemy"),
         (assign, ":suggested_relation_change", 1),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_martial),
             (eq, ":reputation", lrep_goodnatured),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_chivalrous"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (eq, ":reputation", lrep_upstanding),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_upstanding"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (this_or_next|eq, ":reputation", lrep_cunning),
             (eq, ":reputation", lrep_selfrighteous),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_coldblooded"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (lt, "$g_talk_troop_relation", -5),
         (this_or_next|eq, ":reputation", lrep_quarrelsome),
             (eq, ":reputation", lrep_debauched),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied_unfriendly_spiteful"),
         (assign, ":relevance", 80),
       (else_try),
         (eq, "$players_kingdom", "$g_talk_troop_faction"),
         (lt, ":players_kingdom_relation", 0),
         (neq, ":troop_object", "$g_talk_troop"),
         (assign, ":comment", "str_comment_you_let_go_a_lord_allied"),
         (assign, ":relevance", 80),
       (try_end),

#Internal faction relations

     (else_try),
       (eq, ":entry_type", logent_pledged_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
		 (eq, ":faction_object", "$players_kingdom"), #Ie, no switch of kingdoms
         (assign, ":relevance", 200),
         (try_begin),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_martial),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_martial"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_quarrelsome),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_quarrelsome"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_selfrighteous"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_cunning"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_debauched"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_goodnatured),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_goodnatured"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding_unfriendly"),
         (else_try),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_pledged_allegiance_allied_upstanding"),
         (try_end),
       (try_end),


     (else_try),
       (eq, ":entry_type", logent_liege_grants_fief_to_vassal),
       (eq, ":troop_object", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":actor", "$g_talk_troop"),
         (eq, ":faction_object", "$players_kingdom"),
         (assign, ":relevance", 110),
         (try_begin),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cruel"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_cunning),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly_cynical"),
         (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_friendly"),
         (else_try),
            (is_between, "$g_talk_troop_relation", -5, 5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_spiteful"),
            (assign, ":suggested_relation_change", -2),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_upstanding"),
         (else_try),
            (lt, "$g_talk_troop_relation", -5),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied_unfriendly_spiteful"),
         (else_try),
            (assign, ":comment", "str_comment_our_king_granted_you_a_fief_allied"),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_renounced_allegiance),
       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":faction_object", "$g_talk_troop_faction"),
         (neq, ":troop_object", "$g_talk_troop"),
         (try_begin),
           (ge, "$g_talk_troop_faction_relation", 0),
           (neq, "$g_talk_troop_faction", "$players_kingdom"),
           (assign, ":relevance", 180),
           (try_begin),
             (gt, "$g_talk_troop_relation", 5),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
           (else_try),
             (ge, "$g_talk_troop_relation", 0),
             (eq, ":reputation", lrep_goodnatured),
             (assign, ":comment", "str_comment_you_renounced_your_alliegance_friendly"),
		   (else_try),
		     (assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
           (try_end),
         (else_try),
           (lt, "$g_talk_troop_faction_relation", 0),
           (assign, ":relevance", 300),
           (try_begin),
              (ge, "$g_talk_troop_relation", 0),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_moralizing"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (this_or_next|eq, ":reputation", lrep_goodnatured),
                (eq, ":reputation", lrep_upstanding),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy_friendly"),
           (else_try),
              (gt, "$g_talk_troop_relation", 5),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_enemy"),
           (else_try),
              (is_between, "$g_talk_troop_relation", -5, 5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
                  (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
              (assign, ":suggested_relation_change", -2),
           (else_try),
              (lt, "$g_talk_troop_relation", -5),
              (this_or_next|eq, ":reputation", lrep_quarrelsome),
              (this_or_next|eq, ":reputation", lrep_selfrighteous),
                (eq, ":reputation", lrep_debauched),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_unfriendly_spiteful"),
           (else_try),
              (assign, ":comment", "str_comment_you_renounced_your_alliegance_default"),
           (try_end),
         (try_end),
       (try_end),

     (else_try),
       (eq, ":entry_type", logent_lady_marries_lord),
	   (eq, ":troop_object", "trp_player"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":actor", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":actor"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
		  (this_or_next|eq, ":reputation", lrep_quarrelsome),
			(eq, ":reputation", lrep_debauched),
		  (lt, "$g_talk_troop_relation", -5),
          (assign, ":relevance", 200),
		  (assign, ":comment", "str_comment_marriage_normal_nasty"),
	   (else_try),
		  (call_script, "script_troop_get_family_relation_to_troop", ":actor", "$g_talk_troop"),
		  (ge, reg0, 5),
		  (assign, ":comment", "str_comment_marriage_normal_family"),
          (assign, ":relevance", 300),
		  (assign, ":suggested_relation_change", reg0),
		  (val_div, ":suggested_relation_change", 3),
	   (else_try),
		  (store_faction_of_troop, ":bride_faction", ":actor"),
		  (eq, ":bride_faction", "$g_talk_troop_faction"),
		  (assign, ":comment", "str_comment_marriage_normal"),
          (assign, ":relevance", 100),
	   (try_end),
     (else_try),
       (eq, ":entry_type", logent_lady_elopes_with_lord),
	   (eq, ":troop_object", "trp_player"),
  	   ##diplomacy start+  Set reg4 for calling scripts
	   (try_begin),
		  (neq, ":actor", "$g_talk_troop"),
		  (assign, ":return_reg4", 0),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
		  (call_script, "script_troop_get_family_relation_to_troop", ":actor", "$g_talk_troop"),
		  (ge, reg0, 5),
		  (assign, ":comment", "str_comment_marriage_elopement_family"),
          (assign, ":relevance", 300),
		  (store_sub, ":suggested_relation_change", 0, reg0),
		  (val_div, ":suggested_relation_change", 3),
	   (else_try),
		  (store_faction_of_troop, ":bride_faction", ":actor"),
		  (eq, ":bride_faction", "$g_talk_troop_faction"),
		  (faction_slot_eq, ":bride_faction", slot_faction_leader, "$g_talk_troop"),
		  (assign, ":comment", "str_comment_marriage_elopement_liege"),
          (assign, ":relevance", 300),
		  (assign, ":suggested_relation_change", -10),
	   (try_end),
     (else_try), #this is specific to quarrels with the player
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":actor", "$g_talk_troop"),
 	   (eq, ":center_object", "trp_player"),

	   (neg|troop_slot_ge, ":troop_object", slot_troop_spouse, "trp_player"),

	   (str_store_troop_name, s54, ":troop_object"),
   	   ##diplomacy start+  Set reg4 for calling scripts
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+
	   (try_begin),
	       (this_or_next|eq, ":reputation", lrep_selfrighteous),
	       (this_or_next|eq, ":reputation", lrep_quarrelsome),
				(eq, ":reputation", lrep_debauched),

	       (assign, ":comment", "str_comment_i_quarreled_with_you_over_woman_derisive"),
		   (assign, ":relevance", 200),
	       (assign, ":suggested_relation_change", -20),
	   (else_try),
	       (assign, ":comment", "str_comment_i_quarreled_with_you_over_woman_default"),
		   (assign, ":relevance", 200),
	       (assign, ":suggested_relation_change", -20),
	   (try_end),

     (else_try),
       (eq, ":entry_type", logent_border_incident_troop_breaks_truce),
 	   (eq, ":actor", "trp_player"),
 	   (faction_slot_eq, ":faction_object", slot_faction_leader, "$g_talk_troop"),
	   (eq, "$players_kingdom", ":faction_object"),

	   (assign, ":suggested_relation_change", -10),
	   (assign, ":comment", "str_comment_you_broke_truce_as_my_vassal"),
	   (assign, ":relevance", 300),

     (else_try),
       (eq, ":entry_type", logent_border_incident_troop_attacks_neutral),
 	   (eq, ":actor", "trp_player"),
 	   (faction_slot_eq, ":faction_object", slot_faction_leader, "$g_talk_troop"),
	   (eq, "$players_kingdom", ":faction_object"),

	   (assign, ":suggested_relation_change", -3),
	   (assign, ":comment", "str_comment_you_attacked_neutral_as_my_vassal"),
	   (assign, ":relevance", 200),

	 #THE FOLLOWING ARE ALL COMPLAINTS SPOKEN BY LORDS WITHIN CONVERATIONS, RATHER THAN COMMENTS WHEN THE PLAYER FIRST SPEAKS TO A LORD
	 (else_try), #these need to have the actor and object strings added because they are used outside of "script_get_relevant_comment_to_s42"
       (eq, ":entry_type", logent_ruler_intervenes_in_quarrel),
 	   (eq, ":center_object", "$g_talk_troop"), #actor is liege lord, center object is loser lord, troop object is winner lord
	   (str_store_troop_name, s50, ":actor"),
	   (str_store_troop_name, s51, ":center_object"), #s50 is actor, s51 is center object, s54 is troop object
	   (str_store_troop_name, s54, ":troop_object"), #s50 is actor, s51 is center object, s54 is troop object
       (assign, ":comment", "str_comment_lord_intervened_against_me"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lord_protests_marshall_appointment),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"), #s51 is center object (marshall), s54 is troop object (liege lord),
	   (str_store_troop_name, s54, ":troop_object"),

       (assign, ":comment", "str_comment_i_protested_marshall_appointment"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lord_blames_defeat),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"), #s51 is center object (marshall), s54 is troop object (liege lord),
	   (str_store_troop_name, s54, ":troop_object"),
	   (str_store_troop_name, s56, ":faction_object"), #faction object is unusual in this circumstance

       (assign, ":comment", "str_comment_i_blamed_defeat"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_troop_feels_cheated_by_troop_over_land),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_party_name, s51, ":center_object"),
	   (str_store_troop_name, s54, ":troop_object"),
	   (str_store_troop_name, s56, ":faction_object"), #faction object is unusual in this circumstance

       (assign, ":comment", "str_comment_i_was_entitled_to_fief"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":actor", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":center_object"),
	   (str_store_troop_name, s54, ":troop_object"),
	   ##diplomacy start+  Set reg4 and reg3 for calling scripts
	   #(assign, reg3, 0),# #Exclude reg3, since it is used for output anyway
	   #(try_begin),
	   #  (call_script, "script_cf_dplmc_troop_is_female", ":center_object"),
	   #  (assign, reg3, 1),
	   #(try_end),
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+

       (assign, ":comment", "str_comment_i_quarreled_with_troop_over_woman"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_lords_quarrel_over_woman),
 	   (eq, ":center_object", "$g_talk_troop"),

	   (str_store_troop_name, s51, ":actor"),
	   (str_store_troop_name, s54, ":troop_object"),
	   ##diplomacy start+  Set reg4 and reg3 for calling scripts
	   #(assign, reg3, 0),#Exclude reg3, since it is used for output anyway
	   #(try_begin),
	   #  (call_script, "script_cf_dplmc_troop_is_female", ":actor"),
	   #  (assign, reg3, 1),
	   #(try_end),
	   (assign, ":return_reg4", 0),
	   (try_begin),
		  (call_script, "script_cf_dplmc_troop_is_female", ":troop_object"),
		  (assign, ":return_reg4", 1),
	   (try_end),
	   ##diplomacy end+

       (assign, ":comment", "str_comment_i_quarreled_with_troop_over_woman"),
	   (assign, ":relevance", -1),

	 (else_try),
       (eq, ":entry_type", logent_player_stole_cattles_from_village),

       (eq, ":actor", "trp_player"),
       (try_begin),
         (eq, ":center_object_lord", "$g_talk_troop"),
         (assign, ":relevance", 200),
         (assign, ":suggested_relation_change", -1),
         (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_default"),
         (try_begin),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_goodnatured),
            (eq, ":reputation", lrep_upstanding),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_benevolent"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_cunning),
                (eq, ":reputation", lrep_selfrighteous),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_coldblooded"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy_spiteful"),
         (else_try),
            (lt, "$g_talk_troop_faction_relation", -3),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_enemy"),
         (else_try),
            (lt, "$g_talk_troop_relation", -3),
            (this_or_next|eq, ":reputation", lrep_quarrelsome),
                (eq, ":reputation", lrep_debauched),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_unfriendly_spiteful"),
         (else_try),
            (gt, "$g_talk_troop_relation", 6),
            (assign, ":comment", "str_comment_you_stole_cattles_from_my_village_friendly"),
         (try_end),
       (try_end),

     (try_end),

     (assign, reg0, ":comment"),
     (assign, reg1, ":relevance"),
     (assign, reg2, ":suggested_relation_change"),
     (assign, reg3, ":rejoinder"),
     ##diplomacy start+
     (assign, reg4, ":return_reg4"),
     ##diplomacy end+
    ]),

  # script_get_relevant_comment_to_s42
  # Input: none
  # Output: reg0 = 1 if comment found, 0 otherwise; s61 will contain comment string if found
  ("get_relevant_comment_to_s42",
    [

     (troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
     (try_begin),
       (eq, "$cheat_mode", 1),
       (store_add, ":rep_string", ":reputation", "str_personality_archetypes"),
       (str_store_string, s15, ":rep_string"),
       (display_message, "@{!}Reputation type: {s15}"),
     (try_end),


     (assign, ":highest_score_so_far", 50),
     (assign, ":best_comment_so_far", -1),
     (assign, ":rejoinder_to_best_comment_so_far", -1),
     (assign, ":comment_found", 0),
     (assign, ":best_log_entry", -1),
     (assign, ":comment_relation_change", 0),
     (store_current_hours, ":current_time"),
	 ##diplomacy start+
	 (assign, ":best_comment_reg4", 0),
	 ##diplomacy end+

#prevents multiple comments in conversations in same hour

#     (troop_get_slot, ":talk_troop_last_comment_time", "$g_talk_troop", slot_troop_last_comment_time),
#"$num_log_entries should also be set to one, not zero. This is included in the initialize npcs script, although could be moved to game_start
     (troop_get_slot, ":talk_troop_last_comment_slot", "$g_talk_troop", slot_troop_last_comment_slot),
     (troop_set_slot, "$g_talk_troop", slot_troop_last_comment_slot, "$num_log_entries"),

     (store_add, ":log_entries_plus_one", "$num_log_entries", 1),
     (try_for_range, ":log_entry_no", 1, ":log_entries_plus_one"),
#      It should be log entries plus one, so that the try_ sequence does not stop short of the last log entry
#      $Num_log_entries is now the number of the last log entry, which begins at "1" rather than "0"
#      This is so that (le, ":log_entry_no", ":talk_troop_last_comment_slot") works properly

       (troop_get_slot, ":entry_time",           "trp_log_array_entry_time",           ":log_entry_no"),
#      (val_max, ":entry_time", 1), #This is needed for pre-game events to be commented upon, if hours are used rather than the order of events
       (store_sub, ":entry_hours_elapsed", ":current_time", ":entry_time"),
       (try_begin),
         (le, ":log_entry_no", ":talk_troop_last_comment_slot"),
#         (le, ":entry_time", ":talk_troop_last_comment_time"),
         (try_begin),
           (eq, ":log_entry_no", ":talk_troop_last_comment_slot"),
           (eq, "$cheat_mode", 1),
           (assign, reg5, ":log_entry_no"),
           (display_message, "@{!}Entries up to #{reg5} skipped"),
         (try_end),
#       I suggest using the log entry number as opposed to time so that events in the same hour can be commented upon
#       This feels more natural, for example, if there are other lords in the court when the player pledges allegiance
       (else_try),
#         (le, ":entry_hours_elapsed", 3), #don't comment on really fresh events
#       (else_try),
         (call_script, "script_get_relevant_comment_for_log_entry", ":log_entry_no"),
         (gt, reg1, 10),
         (assign, ":score", reg1),
         (assign, ":comment", reg0),
		 #reg2 is what
		 (assign, ":rejoinder", reg3),

         (store_random_in_range, ":rand", 70, 140),
         (val_mul, ":score", ":rand"),
         (store_add, ":entry_time_score", ":entry_hours_elapsed", 500), #approx. one month
         (val_mul, ":score", 1000),
         (val_div, ":score", ":entry_time_score"), ###Relevance decreases over time - halved after one month, one-third after two, etc
         (try_begin),
           (gt, ":score", ":highest_score_so_far"),
           (assign, ":highest_score_so_far", ":score"),
           (assign, ":best_comment_so_far",  ":comment"),
           (assign, ":rejoinder_to_best_comment_so_far",  ":rejoinder"),
           (assign, ":best_log_entry", ":log_entry_no"),
           (assign, ":comment_relation_change", reg2),
		   ##diplomacy start+
		   (assign, ":best_comment_reg4", reg4),
		   ##diplomacy end+
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (gt, ":best_comment_so_far", 0),
       (assign, ":comment_found", 1), #comment found print it to s61 now.
       (troop_get_slot, ":actor",                 "trp_log_array_actor",                 ":best_log_entry"),
       (troop_get_slot, ":center_object",         "trp_log_array_center_object",         ":best_log_entry"),
       (troop_get_slot, ":center_object_lord",    "trp_log_array_center_object_lord",    ":best_log_entry"),
       (troop_get_slot, ":center_object_faction", "trp_log_array_center_object_faction", ":best_log_entry"),
       (troop_get_slot, ":troop_object",          "trp_log_array_troop_object",          ":best_log_entry"),
       (troop_get_slot, ":troop_object_faction",  "trp_log_array_troop_object_faction",  ":best_log_entry"),
       (troop_get_slot, ":faction_object",        "trp_log_array_faction_object",        ":best_log_entry"),
	   ##diplomacy start+
	   (assign, reg4, ":best_comment_reg4"),
	   ##diplomacy end+
       (try_begin),
         (ge, ":actor", 0),
         (str_store_troop_name,   s50, ":actor"),
		 ##diplomacy start+
		 (eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
		 (neq, ":actor", "$g_talk_troop"),
		 (neq, ":actor", "trp_player"),
         #SB : other script
         (call_script, "script_dplmc_store_troop_is_female_reg", ":actor", 3),
		 ##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object", 0),
		 ##diplomacy start+
		 ##OLD:
		 #(str_store_party_name,   s51, ":center_object"),
		 ##NEW:
		 #Alternate meaning (not usually called from this script, but just in case)
		 #In this case, s51 is actually a troop.  Use reg3 for the gender.
		 (try_begin),
			(eq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
			(str_store_troop_name, s51, ":center_object"),
			(neq, ":center_object", "$g_talk_troop"),
			(neq, ":center_object", "trp_player"),
			(call_script, "script_dplmc_store_troop_is_female_reg", ":center_object", 3),
		 (else_try),
		   (neq, ":best_comment_so_far", "str_comment_i_quarreled_with_troop_over_woman"),
 		   (str_store_party_name,   s51, ":center_object"),#<- old behavior
  	    (try_end),
		##diplomacy end+
       (try_end),
       (try_begin),
         (ge, ":center_object_lord", 0),
         (str_store_troop_name,   s52, ":center_object_lord"),
       (try_end),
       (try_begin),
         (ge, ":center_object_faction", 0),
         (str_store_faction_name, s53, ":center_object_faction"),
       (try_end),
       (try_begin),
         (ge, ":troop_object", 0),
         (str_store_troop_name,   s54, ":troop_object"),
       (try_end),
       (try_begin),
         (is_between, ":troop_object_faction", kingdoms_begin, kingdoms_end),
         (str_store_faction_name, s55, ":troop_object_faction"),
         (str_store_string, s55, "str_the_s55"),
	   (else_try),
		 (is_between, ":troop_object", bandits_begin, bandits_end),
         (str_store_string, s55, "str_bandits"),
	   (else_try),
	     (eq, ":troop_object_faction", "fac_deserters"),
         (str_store_string, s55, "str_deserters"),
       (else_try),
         (str_store_string, s55, "str_travellers_on_the_road"),
	   (else_try),

       (try_end),

       (try_begin),
         (ge, ":faction_object", 0),
         (str_store_faction_name, s56, ":faction_object"),
       (try_end),
	   (assign, "$g_last_comment_copied_to_s42", ":best_comment_so_far"), #maybe deprecate
	   (assign, "$g_rejoinder_to_last_comment", ":rejoinder_to_best_comment_so_far"),

       (str_store_string, s42, ":best_comment_so_far"),
     (try_end),

     (assign, reg0, ":comment_found"),

     (assign, "$log_comment_relation_change", ":comment_relation_change"),
     ]),

#
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

  ]
