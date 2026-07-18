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
# MORALE & COURAGE SCRIPTS
# 
# This file contains the logic for calculating party morale and individual troop courage
# based on casualties and other battlefield effects.
####################################################################################################################

morale_scripts = [
  # INPUT: none
  # OUTPUT: none

  ("count_casualties_and_adjust_morale",
   [
    (call_script, "script_calculate_main_party_shares"),
    (assign, ":num_player_party_shares", reg0),

    (assign, ":our_loss_score", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_player_casualties"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_player_casualties", ":i_stack"),
      (party_stack_get_size, ":stack_size", "p_player_casualties", ":i_stack"),

      (party_stack_get_num_wounded, ":num_wounded", "p_player_casualties", ":i_stack"),
      (store_mul, ":stack_size_mul_2", ":stack_size", 2),
      ##diplomacy start+ Fix what appears to be a mistake in Native
      #(store_sub, ":stack_size_mul_2_sub_wounded", ":num_wounded"),##OLD
      (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),##NEW
      ##diplomacy end+

      (store_character_level, ":level", ":stack_troop"),
      (store_add, ":gain", ":level", 3),

      #if died/wounded troop is player troop then give its level +30 while calculating troop die effect on morale
      (try_begin),
        (eq, ":stack_troop", "trp_player"),
        (val_add, ":level", 75),
      (else_try),
        (troop_is_hero, ":stack_troop"),
        (val_add, ":level", 50),
      (try_end),

      (val_mul, ":gain", ":gain"),
      (val_div, ":gain", 10),
      (assign, reg0, ":gain"),
      (val_mul, ":gain", ":stack_size"),

      (try_begin),
        (neg|troop_is_hero, ":stack_troop"),
        (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
        (val_div, ":gain", ":stack_size_mul_2"),
      (try_end),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg1, ":stack_size"),
        (assign, reg2, ":gain"),
        (display_message, "str_our_per_person__reg0_num_people__reg1_total_gain__reg2"),
      (try_end),
      (val_add, ":our_loss_score", ":gain"),
    (try_end),

    (assign, ":died_enemy_population", 0),
    (assign, ":enemy_loss_score", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_enemy_casualties"),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_troop_id, ":stack_troop", "p_enemy_casualties", ":i_stack"),
      (party_stack_get_size, ":stack_size", "p_enemy_casualties", ":i_stack"),

      (party_stack_get_num_wounded, ":num_wounded", "p_enemy_casualties", ":i_stack"),
      (store_mul, ":stack_size_mul_2", ":stack_size", 2),
      (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),

      (store_character_level, ":level", ":stack_troop"),
      (store_add, ":gain", ":level", 3),

      #if troop is hero give extra +15 level while calculating troop die effect on morale
      (try_begin),
        (troop_is_hero, ":stack_troop"),
        (val_add, ":level", 50),
      (try_end),

      (val_mul, ":gain", ":gain"),
      (val_div, ":gain", 10),
      (assign, reg0, ":gain"),
      (val_mul, ":gain", ":stack_size"),

      (try_begin),
        (neg|troop_is_hero, ":stack_troop"),
        (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
        (val_div, ":gain", ":stack_size_mul_2"),
      (try_end),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg1, ":stack_size"),
        (assign, reg2, ":gain"),
        (display_message, "str_ene_per_person__reg0_num_people__reg1_total_gain__reg2"),
      (try_end),
      (val_add, ":enemy_loss_score", ":gain"),
      (val_add, ":died_enemy_population", ":stack_size"),
    (try_end),

    (assign, ":ally_loss_score", 0),
    (try_begin),
      (eq, "$any_allies_at_the_last_battle", 1),
      (party_get_num_companion_stacks, ":num_stacks","p_ally_casualties"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_ally_casualties", ":i_stack"),
        (party_stack_get_size, ":stack_size", "p_ally_casualties", ":i_stack"),

        (party_stack_get_num_wounded, ":num_wounded", "p_ally_casualties", ":i_stack"),
        (store_mul, ":stack_size_mul_2", ":stack_size", 2),
        ##diplomacy start+ Fix what appears to be a mistake in Native
        #(store_sub, ":stack_size_mul_2_sub_wounded", ":num_wounded"),##OLD
        (store_sub, ":stack_size_mul_2_sub_wounded", ":stack_size_mul_2", ":num_wounded"),##NEW
        ##diplomacy end+

        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 3),

        #if troop is hero give extra +15 level while calculating troop die effect on morale
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (val_add, ":level", 50),
        (try_end),

        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (assign, reg0, ":gain"),
        (val_mul, ":gain", ":stack_size"),

        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (val_mul, ":gain", ":stack_size_mul_2_sub_wounded"),
          (val_div, ":gain", ":stack_size_mul_2"),
        (try_end),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (assign, reg1, ":stack_size"),
          (assign, reg2, ":gain"),
          (display_message, "str_all_per_person__reg0_num_people__reg1_total_gain__reg2"),
        (try_end),
        (val_add, ":ally_loss_score", ":gain"),
      (try_end),
    (try_end),

    (store_add, ":our_losses", ":our_loss_score", ":ally_loss_score"),
    (assign, ":enemy_losses", ":enemy_loss_score"),
    (val_mul, ":our_losses", 100),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":enemy_losses"),
      (display_message, "@{!}DEBUGS : enemy_loses : {reg0}"),
    (try_end),

    (try_begin),
      (gt, ":enemy_losses", 0),
      (store_div, ":loss_ratio", ":our_losses", ":enemy_losses"),
    (else_try),
      (assign, ":loss_ratio", 1000),
    (try_end),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg1, ":loss_ratio"),
      (display_message, "str_loss_ratio_is_reg1"),
    (try_end),

    (try_begin),
      (neg|is_between, "$g_enemy_party", centers_begin, centers_end),
      (store_sub, ":total_gain", 60, ":loss_ratio"),
    (else_try),
      (store_sub, ":total_gain", 100, ":loss_ratio"),
    (try_end),

    (try_begin),
      (lt, ":total_gain", 0),
      (val_div, ":total_gain", 2),
    (try_end),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":total_gain"),
      (display_message, "@{!}DEBUGS1 : total_gain : {reg0}"),
    (try_end),

    (val_max, ":total_gain", -60), #total gain changes between -60(1.8+ loss ratio) and 60(0 loss ratio). We assumed average loss ratio is 0.6
    (val_mul, ":total_gain", ":enemy_losses"),
    (val_div, ":total_gain", 100),

    (store_mul, ":total_enemy_morale_gain", ":total_gain", -1), #enemies get totally negative of the morale we get
    (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
    (val_div, ":total_gain", 100),

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":total_gain"),
      (display_message, "@{!}DEBUGS2 : total_gain : {reg0}"),
    (try_end),

    (try_begin),
      (party_is_active, "$g_enemy_party"), #change enemy morale if and only if there is a valid enemy party

      #main enemy party
      (assign, ":total_enemy_population", 0),
      (val_add, ":total_enemy_population", 10), #every part effect total population by number of agents they have plus 10
      (party_get_num_companion_stacks, ":num_stacks", "$g_enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$g_enemy_party", ":i_stack"),
        (party_stack_get_size, ":stack_size", "$g_enemy_party", ":i_stack"),
        (val_add, ":total_enemy_population", ":stack_size"),
      (try_end),
      (assign, ":main_enemy_party_population", ":total_enemy_population"),

      #enemy attachers
      (party_get_num_attached_parties, ":num_attached_parties", "$g_enemy_party"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (val_add, ":total_enemy_population", 10), #every part effect total population by number of agents they have plus 10
        (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
        (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":attached_party", ":i_stack"),
          (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
          (val_add, ":total_enemy_population", ":stack_size"),
        (try_end),
      (try_end),

      #(assign, reg3, ":total_enemy_population"),
      #(assign, reg4, ":died_enemy_population"),
      #(store_sub, ":remaining_enemy_population", ":total_enemy_population", ":died_enemy_population"),
      #(val_add, ":remaining_enemy_population", 10),
      #(assign, reg5, ":remaining_enemy_population"),
      #(display_message, "@total : {reg3}, died : {reg4}, remaining : {reg5}"),

      #remaining enemy population has 10+remaining soldiers in enemy party
      (assign, ":remaining_enemy_population", ":total_enemy_population"),

      (assign, reg5, ":remaining_enemy_population"),
      (assign, reg6, ":total_enemy_morale_gain"),

      (set_fixed_point_multiplier, 100),
      (val_mul, ":remaining_enemy_population", 100),
      (store_sqrt, ":sqrt_remaining_enemy_population", ":remaining_enemy_population"),
      (val_div, ":sqrt_remaining_enemy_population", 100),
      (val_div, ":total_enemy_morale_gain", ":sqrt_remaining_enemy_population"),
      (val_div, ":total_enemy_morale_gain", 4),

      (try_begin),
        (eq, "$cheat_mode", 1),
        (assign, reg7, ":total_enemy_morale_gain"),
        (display_message, "str_total_enemy_morale_gain__reg6_last_total_enemy_morale_gain__reg7_remaining_enemy_population__reg5"),
      (try_end),

      (store_mul, ":party_morale_gain", ":total_enemy_morale_gain", ":main_enemy_party_population"),
      (val_div, ":party_morale_gain", ":total_enemy_population"),

      (try_begin),
        (party_is_active, "$g_enemy_party"),

        (call_script, "script_change_party_morale", "$g_enemy_party", ":party_morale_gain"),

        (party_get_num_attached_parties, ":num_attached_parties", "$g_enemy_party"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", "$g_enemy_party", ":attached_party_rank"),
          (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
          (assign, ":party_population", 0),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":attached_party", ":i_stack"),
            (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
            (val_add, ":party_population", ":stack_size"),
          (try_end),
          #(store_div, ":party_ratio", ":total_enemy_population_multiplied_by_100", ":party_population"), #party ratio changes between 0..100, shows population ratio of that party among all enemy parties
          (store_mul, ":party_morale_gain", ":total_enemy_morale_gain", ":party_population"),
          (val_div, ":party_morale_gain", ":total_enemy_population"),
          (call_script, "script_change_party_morale", ":attached_party", ":party_morale_gain"),
        (try_end),
      (try_end),
    (try_end),

    #Add morale
    (assign, ":morale_gain", ":total_gain"),
    (val_div, ":morale_gain", ":num_player_party_shares"),#if there are lots of soldiers in my party there will be less morale increase.

    (try_begin),
      (eq, "$cheat_mode", 1),
      (assign, reg0, ":num_player_party_shares"),
      (assign, reg1, ":total_gain"),
      (display_message, "@{!}DEBUGS3 : num_player_party_shares:{reg0}, total_gain:{reg1}"),
    (try_end),

    (call_script, "script_change_player_party_morale", ":morale_gain"),

    (store_mul, ":killed_enemies_by_our_soldiers", ":died_enemy_population", "$g_strength_contribution_of_player"),
    (store_div, ":faction_morale_change", ":killed_enemies_by_our_soldiers", 8), #each 8 killed agent with any faction decreases morale of troops belong to that faction in our party by 1.
    (try_begin),
      (gt, ":faction_morale_change", 2000),
      (assign, ":faction_morale_change", 2000),
    (try_end),

    (try_begin), #here we give positive morale to our troops of with same faction of ally party with 2/3x multipication.
      (ge, "$g_ally_party", 0),

      (store_div, ":ally_faction_morale_change", ":faction_morale_change", 3), #2/3x multipication (less than normal)
      (val_mul, ":ally_faction_morale_change", 2),
      (store_faction_of_party, ":ally_faction", "$g_ally_party"),
      (call_script, "script_change_faction_troop_morale", ":ally_faction", ":faction_morale_change", 0),
      # (faction_get_slot, ":faction_morale", ":ally_faction",  slot_faction_morale_of_player_troops),
      # (val_add, ":faction_morale", ":ally_faction_morale_change"),
      # (faction_set_slot, ":ally_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),

    (try_begin), #here we give positive morale to our troops of owner of rescued village's faction after saving village from bandits by x3 bonus.
      (neg|party_is_active, "$g_enemy_party"),
      (ge, "$current_town", 0),

      (val_mul, ":faction_morale_change", 2), #2x bonus (more than normal)
      (store_faction_of_party, ":ally_faction", "$current_town"),
      #SB : script call
      (call_script, "script_change_faction_troop_morale", ":ally_faction", ":faction_morale_change", 1),  #SB : script call
      # (faction_get_slot, ":faction_morale", ":ally_faction",  slot_faction_morale_of_player_troops),
      # (val_add, ":faction_morale", ":faction_morale_change"),
      # (faction_set_slot, ":ally_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (else_try),
      (party_is_active, "$g_enemy_party"),
      (assign, ":currently_in_rebellion", 0),
      (try_begin),
        (eq, "$players_kingdom", "fac_player_supporters_faction"),
        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        (assign, ":currently_in_rebellion", 1),
      (try_end),
      (eq, ":currently_in_rebellion", 0),

      (store_div, ":faction_morale_change", ":faction_morale_change", 3), #2/3x multipication (less than normal)
      (val_mul, ":faction_morale_change", 2),
      (store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
      (call_script, "script_change_faction_troop_morale", ":enemy_faction", ":faction_morale_change", 0), #SB : script call
      # (faction_get_slot, ":faction_morale", ":enemy_faction",  slot_faction_morale_of_player_troops),
      # (val_sub, ":faction_morale", ":faction_morale_change"),
      # (faction_set_slot, ":enemy_faction",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),

  ]),

  #script_print_casualties_to_s0:

  # script_apply_effect_of_other_people_on_courage_scores
  # Input: none
  # Output: none
  ("apply_effect_of_other_people_on_courage_scores",
    [
      (get_player_agent_no, ":player_agent"),

      (try_for_agents, ":centered_agent_no"),
        (agent_is_human, ":centered_agent_no"),
        (agent_is_alive, ":centered_agent_no"),
        (neq, ":centered_agent_no", ":player_agent"),
        ###(((courage_scores NEW FIX
        (agent_slot_eq, ":centered_agent_no", slot_agent_is_running_away, 1), 
        ###)))
        (agent_get_position, pos0, ":centered_agent_no"),
        (try_begin),
          (agent_is_ally, ":centered_agent_no"),
          (assign, ":is_centered_agent_ally", 1),
        (else_try),
          (assign, ":is_centered_agent_ally", 0),
        (try_end),

        (try_for_agents, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),
          (neq, ":centered_agent_no", ":agent_no"),

          (try_begin),
            (agent_is_ally, ":agent_no"),
            (assign, ":is_agent_ally", 1),
          (else_try),
            (assign, ":is_agent_ally", 0),
          (try_end),

          (eq, ":is_centered_agent_ally", ":is_agent_ally"), #if centered agent and other agent is at same team then continue.
          (agent_get_slot, ":agent_is_running_away_or_not", ":agent_no", slot_agent_is_running_away),

          (try_begin),
            (eq, ":agent_no", ":player_agent"),
            (assign, ":agent_delta_courage_score", 6),
          (else_try),
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (troop_is_hero, ":troop_id"),

            #Hero Agent : if near agent (hero, agent_no) is not running away his positive effect on centered agent (centered_agent_no) fighting at his side is effected by his hit points.
            (try_begin),
              (neq, ":agent_is_running_away_or_not", 1), #if agent is not running away
              (store_agent_hit_points, ":agent_hit_points", ":agent_no"),
              (try_begin),
                (eq, ":agent_hit_points", 100),
                (assign, ":agent_delta_courage_score", 6),
              (else_try),
                (ge, ":agent_hit_points", 75),
                (assign, ":agent_delta_courage_score", 5),
              (else_try),
                (ge, ":agent_hit_points", 60),
                (assign, ":agent_delta_courage_score", 4),
              (else_try),
                (ge, ":agent_hit_points", 45),
                (assign, ":agent_delta_courage_score", 3),
              (else_try),
                (ge, ":agent_hit_points", 30),
                (assign, ":agent_delta_courage_score", 2),
              (else_try),
                (ge, ":agent_hit_points", 15),
                (assign, ":agent_delta_courage_score", 1),
              (end_try),
            (else_try),
              (assign, ":agent_delta_courage_score", 4),
            (end_try),
          (else_try),
            #Normal Agent : if near agent (agent_no) is not running away his positive effect on centered agent (centered_agent_no) fighting at his side is effected by his hit points.
            (try_begin),
              (neq, ":agent_is_running_away_or_not", 1), # if agent is not running away
              (store_agent_hit_points, ":agent_hit_points", ":agent_no"),
              (try_begin),
                (eq, ":agent_hit_points", 100),
                (assign, ":agent_delta_courage_score", 4),
              (else_try),
                (ge, ":agent_hit_points", 75),
                (assign, ":agent_delta_courage_score", 3),
              (else_try),
                (ge, ":agent_hit_points", 50),
                (assign, ":agent_delta_courage_score", 2),
              (else_try),
                (ge, ":agent_hit_points", 25),
                (assign, ":agent_delta_courage_score", 1),
              (try_end),
              (try_begin), # to make our warrior run away easier we decrease one, because they have player_agent (+6) advantage.
                (agent_is_ally, ":agent_no"),
                (val_sub, ":agent_delta_courage_score", 1),
              (try_end),
            (else_try),
              (assign, ":agent_delta_courage_score", 2),
            (end_try),
          (try_end),

          ###(((courage_scores NEW FIX
          (try_begin),
            (agent_get_troop_id, ":centered_troop_id", ":centered_agent_no"),
            (troop_is_hero, ":centered_troop_id"),
            (assign, ":agent_delta_courage_score_2", 4),
          (else_try),
            (assign, ":agent_delta_courage_score_2", 2),
          (try_end),

          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),

          (assign, ":pos_effect", 0),
          (try_begin),
            (lt, ":dist", 2000), #0-20 meter
            (assign, ":pos_effect", 50),
          (else_try),
            (lt, ":dist", 4000), #21-40 meter
            (assign, ":pos_effect", 40),
          (else_try),
            (lt, ":dist", 7000), #41-70 meter
            (assign, ":pos_effect", 30),
          (else_try),
            (lt, ":dist", 11000), #71-110 meter
            (assign, ":pos_effect", 20),
          (else_try),      
            (lt, ":dist", 16000), # 111-160 meter, assumed that eye can see agents friendly at most 160 meters far while fighting. 
                                  # this is more than below limit (108 meters) because we hear that allies come from further.
            (assign, ":pos_effect", 10),
          (try_end),

          (assign, ":neg_effect", 0),                             # negative effect of running agent on other ally agents are lower then positive effects above, to avoid starting  
          (try_begin),                                            # run away of all agents at a moment. I want to see agents running away one by one during battle, not all together.
            (lt, ":dist", 200), #1-2 meter,                       # this would create better game play.
            (assign, ":neg_effect", 15),
          (else_try),
            (lt, ":dist", 400), #3-4 meter, 
            (assign, ":neg_effect", 13),
          (else_try),
            (lt, ":dist", 600), #5-6 meter
            (assign, ":neg_effect", 11),
          (else_try),
            (lt, ":dist", 800), #7-8 meter
            (assign, ":neg_effect", 9),
          (else_try),
            (lt, ":dist", 1200), #9-12 meters
            (assign, ":neg_effect", 7),
          (else_try),
            (lt, ":dist", 2400), #13-24 meters
            (assign, ":neg_effect", 5),
          (else_try),
            (lt, ":dist", 4800), #25-48 meters
            (assign, ":neg_effect", 3),
          (else_try),
            (lt, ":dist", 9600), #49-98 meters, assumed that eye can see agents running away at most 98 meters far while fighting.
            (assign, ":neg_effect", 1),
          (try_end),   

          (try_begin),
            (neq, ":agent_is_running_away_or_not", 1),
            (val_mul, ":agent_delta_courage_score", 1),
            (val_mul, ":agent_delta_courage_score", ":pos_effect"),

            (val_mul, ":agent_delta_courage_score_2", -2),
            (val_mul, ":agent_delta_courage_score_2", ":neg_effect"),
            (neq, ":agent_delta_courage_score_2", 0),
            (agent_get_slot, ":agent_courage_score_2", ":agent_no", slot_agent_courage_score),
            (val_add, ":agent_courage_score_2", ":agent_delta_courage_score_2"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score_2"),

          (else_try),
            (val_mul, ":agent_delta_courage_score", -1),
            (val_mul, ":agent_delta_courage_score", ":neg_effect"),
          (try_end),
          (neq, ":agent_delta_courage_score", 0),
          (agent_get_slot, ":agent_courage_score", ":centered_agent_no", slot_agent_courage_score),
          (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
          (agent_set_slot, ":centered_agent_no", slot_agent_courage_score, ":agent_courage_score"),
          ###)))
        (try_end),
      (try_end),
  ]), #ozan


#jacobhinds Morale Code BEGIN

  # script_apply_death_effect_on_courage_scores
  # Input: dead agent id, killer agent id
  # Output: none
  ("apply_death_effect_on_courage_scores",
    [
      (store_script_param, ":dead_agent_no", 1),
      (store_script_param, ":killer_agent_no", 2),



      (try_begin),
        (agent_is_human, ":dead_agent_no"),

        (try_begin),
          (agent_is_ally, ":dead_agent_no"),
          (assign, ":is_dead_agent_ally", 1),
        (else_try),
          (assign, ":is_dead_agent_ally", 0),
        (try_end),

        #(agent_get_position, pos0, ":dead_agent_no"),
        #(assign, ":number_of_near_allies_to_dead_agent", 0),

        # (try_for_agents, ":agent_no"),
          # (agent_is_human, ":agent_no"),
          # (agent_is_alive, ":agent_no"),

          # (agent_get_position, pos1, ":agent_no"),
          # (get_distance_between_positions, ":dist", pos0, pos1),

          # (le, ":dist", 1300), # to count number of allies within 13 meters to dead agent.

          # (try_begin),
            # (agent_is_ally, ":agent_no"),
            # (assign, ":is_agent_ally", 1),
          # (else_try),
            # (assign, ":is_agent_ally", 0),
          # (try_end),

          # (try_begin),
            # (eq, ":is_dead_agent_ally", ":is_agent_ally"),
            # (val_add, ":number_of_near_allies_to_dead_agent", 1), #was 1
																	# # (number_of_near_allies_to_dead_agent) is counted because if there are
          # (try_end),                                              # many allies of dead agent around him, negative courage effect become less.

			# # jacobhinds edit: wait a second, this doesn't really make sense.
			# # If a soldier in a blob of soldiers gets slaughtered, nobody routs,
			# # but if they're outside, they cause more routing. Halve this effect:
			# # distance should play the biggest role.
          # (val_div, ":number_of_near_allies_to_dead_agent", 2),

        # (try_end),

        (try_for_agents, ":agent_no"),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),

          (try_begin),
            (agent_is_ally, ":agent_no"),
            (assign, ":is_agent_ally", 1),
          (else_try),
            (assign, ":is_agent_ally", 0),
          (try_end),

          (try_begin), # each agent is effected by a killed agent positively if he is rival or negatively if he is ally.
            (neq, ":is_dead_agent_ally", ":is_agent_ally"),
            (assign, ":agent_delta_courage_score", 3),  # if killed agent is agent of rival side, add points to fear score #was 10 #after that, was 1
          (else_try),
            (assign, ":agent_delta_courage_score", -5), # if killed agent is agent of our side, decrease points from fear score #jacobhinds was -15, was -4 before battle_ratio overhaul, FEAR SCORE
            #(val_add, ":agent_delta_courage_score", ":number_of_near_allies_to_dead_agent"), # ":number_of_near_allies_to_dead_agent" is added because if there are many # allies of dead agent around him, negative courage effect become less.
            # (try_begin),
              # (lt, ":agent_delta_courage_score", -4), #was -5 #was -2 before battle_ratio overhaul #was gt
              # (assign, ":agent_delta_courage_score", -4), #was -5
            # (try_end),

            (agent_get_slot, ":dead_agent_was_running_away_or_not", ":dead_agent_no",  slot_agent_is_running_away), #look dead agent was running away or not.
            (try_begin),
              (eq, ":dead_agent_was_running_away_or_not", 1),
              (val_div, ":agent_delta_courage_score", 3), #was 3 # if killed agent was running away his negative effect on ally courage scores become very less. This added because
            (try_end),                                     # running away agents are easily killed and courage scores become very in a running away group after a time, and
          (try_end),                                       # they do not stop running away although they pass near a new powerful ally party.
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),

          (try_begin), #if agent is the killer, give him x20 more courage than usual
            (eq, ":killer_agent_no", ":agent_no"),
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 20),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (try_end),

			#jacobhinds edit: prevent morale from getting too high
          (try_begin),
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
			(ge, ":agent_courage_score", max_morale),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, max_morale),
          (try_end),

          (try_begin),
            (lt, ":dist", 100), #0-1 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 120), #was 150
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 200), #2 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 110), #was 120
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 300), #3 meter
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 100),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 400), #4 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 90),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 600), #5-6 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 80),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 800), #7-8 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 70),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 1000), #9-10 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 60),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 1500), #11-15 meter
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 50),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 2500), #16-25 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 40),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 4000), #26-40 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 30),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 6500), #41-65 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 20),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (else_try),
            (lt, ":dist", 10000), #61-100 meters
            (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            (val_mul, ":agent_delta_courage_score", 10),
            (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          (try_end),
        (try_end),
      (try_end),

			#housekeeping
			# (store_random_in_range, ":rand", 0, 10),
			# (try_begin),
				# (eq, ":rand", 1),
				# (assign, reg4, ":agent_delta_courage_score"),
				# (display_message, "@{reg4}"),
			# (try_end),
			#housekeeping

      ]), #ozan

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
]
