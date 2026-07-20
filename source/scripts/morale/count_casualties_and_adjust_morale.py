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

count_casualties_and_adjust_morale_scripts = [
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

  ])
]
