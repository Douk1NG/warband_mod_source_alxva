# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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
# TRAINING GROUND SCRIPTS
# 
# This file contains scripts for the various mini-games and tutorials available at Training Grounds. 
# It handles the setup, difficulty, weapon selection, and combat logic for sparring and melee training.
####################################################################################################################

training_ground_scripts = [


  #script_cf_training_ground_sub_routine_1_for_melee_details
  # INPUT:
  # value
  #OUTPUT:
  # none
  ("cf_training_ground_sub_routine_1_for_melee_details",
   [
     (store_script_param, ":value", 1),
     (ge, "$temp_3", ":value"),
     (val_add, ":value", 1),
     (troop_get_slot, ":troop_id", "trp_stack_selection_ids", ":value"),
     (str_store_troop_name, s0, ":troop_id"),
     ]),

  #script_training_ground_sub_routine_2_for_melee_details
  # INPUT:
  # value
  #OUTPUT:
  # none
  ("training_ground_sub_routine_2_for_melee_details",
   [
     (store_script_param, ":value", 1),
     (val_sub, ":value", 1),
     (try_begin),
       (lt, ":value", 0),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
     (else_try),
       (call_script, "script_remove_fit_party_member_from_stack_selection", ":value"),
     (try_end),
     (assign, ":troop_id", reg0),
     (store_sub, ":slot_index", "$temp_2", 1),
     (troop_set_slot, "trp_temp_array_a", ":slot_index", ":troop_id"),
     (try_begin),
       (eq, "$temp", "$temp_2"),
       (call_script, "script_start_training_at_training_ground", -1, "$temp"),
     (else_try),
       (val_add, "$temp_2", 1),
       (jump_to_menu, "mnu_training_ground_selection_details_melee_2"),
     (try_end),
     ]),

  #script_cf_training_ground_sub_routine_for_training_result
  # INPUT:
  # arg1: troop_id, arg2: stack_no, arg3: troop_count, arg4: xp_ratio_to_add
  #OUTPUT:
  # none
  ("cf_training_ground_sub_routine_for_training_result",
   [
     (store_script_param, ":troop_id", 1),
     (store_script_param, ":stack_no", 2),
     (store_script_param, ":amount", 3),
     (store_script_param, ":xp_ratio_to_add", 4),

     (store_character_level, ":level", ":troop_id"),
     (store_add, ":level_added", ":level", 5),
     (store_mul, ":min_hardness", ":level_added", 3),
     (val_min, ":min_hardness", 100),
     (store_sub, ":hardness_dif", ":min_hardness", "$g_training_ground_training_hardness"),
     (val_max, ":hardness_dif", 0),
     (store_sub, ":hardness_dif", 100, ":hardness_dif"),
     (val_mul, ":hardness_dif", ":hardness_dif"),
     (val_div, ":hardness_dif", 10), # value over 1000
##     (assign, reg0, ":hardness_dif"),
##     (display_message, "@Hardness difference: {reg0}/1000"),
     (store_mul, ":xp_ratio_to_add_for_stack", ":xp_ratio_to_add", ":hardness_dif"),
     (val_div, ":xp_ratio_to_add_for_stack", 1000),
     (try_begin),
       (eq, ":troop_id", "trp_player"),
       (val_mul, ":xp_ratio_to_add_for_stack", 1),
     (else_try),
       (try_begin),
         (eq, "$g_mt_mode", ctm_melee),
         (try_begin),
           (this_or_next|troop_is_guarantee_ranged, ":troop_id"),
           (troop_is_guarantee_horse, ":troop_id"),
           (val_div, ":xp_ratio_to_add_for_stack", 4),
         (try_end),
       (else_try),
         (eq, "$g_mt_mode", ctm_mounted),
         (try_begin),
           (neg|troop_is_guarantee_horse, ":troop_id"),
           (assign, ":xp_ratio_to_add_for_stack", 0),
         (try_end),
       (else_try),
         (neg|troop_is_guarantee_ranged, ":troop_id"),
         (assign, ":xp_ratio_to_add_for_stack", 0),
       (try_end),
     (try_end),
     (val_add,  ":level", 1),
     (store_mul, ":xp_to_add", 100, ":level"),
     (val_mul, ":xp_to_add", ":amount"),
     (val_div, ":xp_to_add", 20),
     (val_mul, ":xp_to_add", ":xp_ratio_to_add_for_stack"),
     (val_div, ":xp_to_add", 1000),
     (store_mul, ":max_xp_to_add", ":xp_to_add", 3),
     (val_div, ":max_xp_to_add", 2),
     (store_div, ":min_xp_to_add", ":xp_to_add", 2),
     (store_random_in_range, ":random_xp_to_add", ":min_xp_to_add", ":max_xp_to_add"),
     (gt, ":random_xp_to_add", 0),
     (try_begin),
       (troop_is_hero, ":troop_id"),
       (add_xp_to_troop, ":random_xp_to_add", ":troop_id"),
       (store_div, ":proficiency_to_add", ":random_xp_to_add", 50),
       (try_begin),
         (gt, ":proficiency_to_add", 0),
         (troop_raise_proficiency, ":troop_id", "$g_training_ground_used_weapon_proficiency", ":proficiency_to_add"),
       (try_end),
     (else_try),
       (party_add_xp_to_stack, "p_main_party", ":stack_no", ":random_xp_to_add"),
     (try_end),
     (assign, reg0, ":random_xp_to_add"),
     ]),


##  #script_cf_print_troop_name_with_stack_index_to_s0
  # INPUT:
  # param1: training_weapon_type, param2: training_param
  ("start_training_at_training_ground",
   [
     # (val_add, "$g_training_ground_training_count", 1),
     (store_script_param, ":mission_weapon_type", 1),
     (store_script_param, ":training_param", 2),

     (set_jump_mission, "mt_training_ground_training"),
     #SB : increment sparring count
     (party_get_slot, ":count", "$g_encountered_party", slot_grounds_count),
     (party_get_slot, ":trainer_troop", "$g_encountered_party", slot_grounds_trainer),
     (val_add, ":count", 1),
     (party_set_slot, "$g_encountered_party", slot_grounds_count, ":count"),


     (assign, ":training_default_weapon_1", -1),
     (assign, ":training_default_weapon_2", -1),
     (assign, ":training_default_weapon_3", -1),
     (assign, "$scene_num_total_gourds_destroyed", 0),
     (try_begin),
       (eq, ":mission_weapon_type", itp_type_bow),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_archery),
       (assign, ":training_default_weapon_1", "itm_practice_bow"),
       (try_begin),
         (eq, "$g_mt_mode", ctm_mounted),
         (assign, ":training_default_weapon_2", "itm_practice_arrows_100_amount"),
       (else_try),
         (assign, ":training_default_weapon_2", "itm_practice_arrows_10_amount"),
       (try_end),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_crossbow),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_crossbow),
       (assign, ":training_default_weapon_1", "itm_practice_crossbow"),
       (assign, ":training_default_weapon_2", "itm_practice_bolts_9_amount"),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_thrown),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_throwing),
       (try_begin),
         (eq, "$g_mt_mode", ctm_mounted),
         (assign, ":training_default_weapon_2", "itm_practice_throwing_daggers_100_amount"),
       (else_try),
         (assign, ":training_default_weapon_2", "itm_practice_throwing_daggers"),
       (try_end),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_one_handed_wpn),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_one_handed_weapon),
       (assign, ":training_default_weapon_1", "itm_practice_sword"),
     (else_try),
       (eq, ":mission_weapon_type", itp_type_polearm),
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_polearm),
       (assign, ":training_default_weapon_1", "itm_practice_lance"),
     (else_try),
       #weapon_type comes as -1 when melee training is selected
       (assign, "$g_training_ground_used_weapon_proficiency", wpt_one_handed_weapon),
       # (call_script, "script_get_random_melee_training_weapon"),
       (try_begin),
         (gt, ":trainer_troop", 0),
         (troop_slot_ge, ":trainer_troop", slot_troop_trainer_training_difficulty, 4),
         (call_script, "script_get_proficient_melee_training_weapon", "$g_player_troop"),
         (try_begin), #sword and board
           (eq, reg0, "itm_practice_sword"),
           (assign, reg1, "itm_practice_shield"),
         (try_end),
       (else_try),
         (call_script, "script_get_random_melee_training_weapon"),
       (try_end),
       (assign, ":training_default_weapon_1", reg0),
       (assign, ":training_default_weapon_2", reg1),
     (try_end),

##     (assign, "$g_training_ground_training_troop_stack_index", ":stack_index"),
     (try_begin),
       (eq, "$g_mt_mode", ctm_mounted),
       (assign, ":training_default_weapon_3", "itm_practice_horse"),
       #SB : use slot
       (party_get_slot, "$g_training_ground_training_scene", "$g_encountered_party", slot_grounds_track),
     (else_try),
       #SB : use slot
       (party_get_slot, "$g_training_ground_training_scene", "$g_encountered_party", slot_grounds_melee),
       # (store_add, "$g_training_ground_training_scene", "scn_training_ground_ranged_melee_1", "$g_encountered_party"),
       # (val_sub, "$g_training_ground_training_scene", training_grounds_begin),
     (try_end),

     (modify_visitors_at_site, "$g_training_ground_training_scene"),
     (reset_visitors),
     (set_visitor, 0, "trp_player"),

     (assign, ":selected_weapon", -1),
     (try_for_range, ":cur_slot", ek_item_0, ek_head),#equipment slots
       (troop_get_inventory_slot, ":cur_item", "trp_player", ":cur_slot"),
       (ge, ":cur_item", 0),
       (item_get_type, ":item_type", ":cur_item"),
       (try_begin),
         (eq, ":item_type", ":mission_weapon_type"),
         (eq, ":selected_weapon", -1),
         (assign, ":selected_weapon", ":cur_item"),
       (try_end),
     (try_end),
     (mission_tpl_entry_clear_override_items, "mt_training_ground_training", 0),
     (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, "itm_practice_boots"),
     (try_begin),
       (ge, ":training_default_weapon_1", 0),
       (try_begin),
         (ge, ":selected_weapon", 0),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":selected_weapon"),
       (else_try),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_1"),
       (try_end),
     (try_end),
     (try_begin),
       (ge, ":training_default_weapon_2", 0),
       (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_2"),
     (try_end),
     (try_begin),
       (ge, ":training_default_weapon_3", 0),
       (mission_tpl_entry_add_override_item, "mt_training_ground_training", 0, ":training_default_weapon_3"),
     (try_end),

     (assign, ":cur_visitor_point", 5),
     (troop_get_slot, ":num_fit", "trp_stack_selection_amounts", 1),
     (store_add, ":end_cond", 5, ":num_fit"),
     (val_min, ":end_cond", 13),
     (try_for_range, ":cur_visitor_point", 5, ":end_cond"),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
       (set_visitor, ":cur_visitor_point", reg0),
       (val_add, ":cur_visitor_point", 1),
     (try_end),
     (try_begin),
       (eq, "$g_mt_mode", ctm_melee),
       (assign, ":total_difficulty", 0),
       (assign, ":cur_entry_point", 1),
       (try_for_range, ":i", 0, ":training_param"),
         (troop_get_slot, ":cur_troop", "trp_temp_array_a", ":i"),
         # (store_add, ":cur_entry_point", ":i", 1),
         (set_visitor, ":cur_entry_point", ":cur_troop"),
         (mission_tpl_entry_clear_override_items, "mt_training_ground_training", ":cur_entry_point"),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", "itm_practice_boots"),
         (call_script, "script_get_random_melee_training_weapon"),
         (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", reg0),
         (try_begin),
           (ge, reg1, 0),
           (mission_tpl_entry_add_override_item, "mt_training_ground_training", ":cur_entry_point", reg1),
         (try_end),
         (val_add, ":cur_entry_point", 1),
         (store_character_level, ":cur_troop_level", ":cur_troop"),
         (val_add, ":cur_troop_level", 10),
         (val_mul, ":cur_troop_level", ":cur_troop_level"),
         (val_add, ":total_difficulty", ":cur_troop_level"),
       (try_end),

       (assign, "$g_training_ground_training_num_enemies", ":training_param"),
       (assign, "$g_training_ground_training_hardness",  ":total_difficulty"),
       (store_add, ":number_multiplier", "$g_training_ground_training_num_enemies", 4),
       (val_mul, "$g_training_ground_training_hardness", ":number_multiplier"),
       (val_div, "$g_training_ground_training_hardness", 2400),
       #SB : store by count
       # (str_store_string, s0, "@Your opponents are ready for the fight."),
     (else_try),
       (eq, "$g_mt_mode", ctm_mounted),
       (try_begin),
         (eq, ":mission_weapon_type", itp_type_bow),
         (assign, "$g_training_ground_training_hardness", 350),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 30),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_thrown),
         (assign, "$g_training_ground_training_hardness", 400),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 30),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_one_handed_wpn),
         (assign, "$g_training_ground_training_hardness", 200),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 45),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_polearm),
         (assign, "$g_training_ground_training_hardness", 280),
         (assign, "$g_training_ground_training_num_gourds_to_destroy", 35),
       (try_end),
       # (str_store_string, s0, "@Try to destroy as many targets as you can. You have two and a half minutes to clear the track."),
     (else_try),
       (eq, "$g_mt_mode", ctm_ranged),
       (store_mul, "$g_training_ground_ranged_distance", ":training_param", 100),
       (assign, ":hardness_modifier", ":training_param"),
       (val_mul, ":hardness_modifier", ":hardness_modifier"),
       (try_begin),
         (eq, ":mission_weapon_type", itp_type_bow),
         (val_mul, ":hardness_modifier", 3),
         (val_div, ":hardness_modifier", 2),
       (else_try),
         (eq, ":mission_weapon_type", itp_type_thrown),
         (val_mul, ":hardness_modifier", 5),
         (val_div, ":hardness_modifier", 2),
         (val_mul, ":hardness_modifier", ":training_param"),
         (val_div, ":hardness_modifier", 2),
       (try_end),
       (store_mul, "$g_training_ground_training_hardness", 100, ":hardness_modifier"),
       (val_div, "$g_training_ground_training_hardness", 6000),
       # (str_store_string, s0, "@Stay behind the line on the ground and shoot the targets. Try not to waste any shots."),
     (try_end),
     (jump_to_menu, "mnu_training_ground_description"),
     ]),


  #script_print_party_to_s0:
  # INPUT:
  # value
  #OUTPUT:
  # none
  ("training_ground_sub_routine_2_for_melee_details_fuck",
   [
     (store_script_param, ":value", 1),
     (val_sub, ":value", 1),
     (try_begin),
       (eq, ":value", -3),
	   (assign, reg0, -1),
     (else_try),
       (eq, ":value", -2),
       (call_script, "script_remove_random_fit_party_member_from_stack_selection"),
     (else_try),
       (call_script, "script_remove_fit_party_member_from_stack_selection", ":value"),
     (try_end),
     (assign, ":troop_id", reg0),
     (store_sub, ":slot_index", "$temp_2", 1),
     (troop_set_slot, "trp_temp_array_a", ":slot_index", ":troop_id"),
     (troop_set_slot, "trp_temp_array_b", ":slot_index", -1),
     (try_begin),
       (eq, "$temp", "$temp_2"),
       (call_script, "script_start_fucking", "$temp", "$g_training_ground_melee_training_scene"),
     (else_try),
       (val_add, "$temp_2", 1),
       (jump_to_menu, "mnu_fuck_3"),
     (try_end),
     ]),

  #script_start_fucking

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

("cf_is_melee_weapon_for_tutorial",
    [
      (store_script_param, ":item_no", 1),
      (assign, ":result", 0),
      (try_begin),
        (this_or_next|eq, ":item_no", "itm_quarter_staff"),
        (eq, ":item_no", "itm_practice_sword"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
     ]),

("agents_cheer_during_training", [
      (party_get_morale, ":cur_morale", "p_main_party"),
      (assign, ":boundary", 150),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        # (agent_get_troop_id, ":troop_no", ":agent_no"), #a spectator
        (neg|agent_has_item_equipped, ":agent_no", "itm_practice_boots"),
        (store_random_in_range, ":random_no", ":cur_morale", 250),
        (gt, ":random_no", ":boundary"),
        (val_add, ":boundary", 15),
        (agent_set_animation, ":agent_no", "anim_cheer"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
    ]),

("troop_set_training_health_from_agent", [
      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        # (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":troop_no", ":agent_no"),
        (troop_is_hero, ":troop_no"),
        (store_troop_health, ":health", ":troop_no", 0), #this is not yet deducted
        (store_agent_hit_points, ":hp", ":agent_no", 0),
        (val_sub, ":hp", ":health"), #this is the difference
        (try_begin),
          (agent_is_alive, ":agent_no"),
          (store_skill_level, ":skill", "skl_first_aid", ":troop_no"),
          (val_add, ":skill", ":first_aid"),
        (else_try),
          (assign, ":skill", ":first_aid"),
        (try_end),
        (val_mul, ":skill", -5),  #as per skill description
        (val_add, ":skill", 100), # 100 - skill effect
        #apply skill effect and set health
        (val_mul, ":hp", ":skill"),
        (val_div, ":hp", 100),
        (val_add, ":hp", ":health"), #subtract modified difference
        (troop_set_health, ":troop_no", ":hp", 0),
      (try_end),
    ]),

("agent_apply_training_health", [
      (store_script_param_1, ":agent_no"),
      # (store_script_param_2, "$current_town"),

      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
      (party_get_slot, ":relation", "$current_town", slot_center_player_relation), #range from -100 to 100
      (store_sub, ":relation", 200, ":relation"), #300 to 100

      (store_troop_health, ":health", "trp_player", 0), #this is not yet deducted
      (store_agent_hit_points, ":hp", ":agent_no", 0),

      (val_sub, ":hp", ":health"), #this is the difference (non-positive)
      (try_begin),
        (agent_is_alive, ":agent_no"),
        (store_skill_level, ":skill", "skl_first_aid", "trp_player"),
      (else_try),
        (assign, ":skill", 0),
      (try_end),
      (val_add, ":skill", ":first_aid"),
      (val_mul, ":skill", -5),  #as per skill description
      (val_add, ":skill", 100), # 100 - skill effect
      #apply skill effect, relation effect and set health
      (val_mul, ":hp", ":skill"),
      (val_div, ":hp", 100),
      (val_mul, ":hp", ":relation"),
      (val_div, ":hp", 200),
      (val_add, ":health", ":hp"), #subtract modified difference
      (val_max, ":health", 5),
      (troop_set_health, "trp_player", ":health", 0),
    ]),

("get_proficient_melee_training_weapon",
    [
        (store_script_param, ":troop_no", 1),
        (store_proficiency_level, ":onehands", ":troop_no", wpt_one_handed_weapon),
        (store_proficiency_level, ":twohands", ":troop_no", wpt_two_handed_weapon),
        (store_proficiency_level, ":polearms", ":troop_no", wpt_polearm),

        (assign, ":item_no", -1),
        (try_begin), #practice shield will be added automatically
          (ge, ":onehands", ":twohands"),
          (ge, ":onehands", ":polearms"),
          # (agent_equip_item, ":agent_no", "itm_practice_shield"),
          (assign, ":item_no", "itm_practice_sword"),
        (else_try),
          (ge, ":twohands", ":onehands"),
          (ge, ":twohands", ":polearms"),
          (assign, ":item_no", "itm_heavy_practice_sword"),
        (else_try),
          (ge, ":polearms", ":onehands"),
          (ge, ":polearms", ":twohands"),
          (assign, ":item_no", "itm_practice_staff"),
        (try_end),
        (assign, reg0, ":item_no"),
    ]),
]
