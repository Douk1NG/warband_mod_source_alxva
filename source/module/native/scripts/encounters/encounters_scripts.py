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
# ENCOUNTERS & BATTLE SETUP SCRIPTS
# 
# This file handles the logic for map encounters, joining battles, battle advantages,
# auto-calc battle simulations, and tactical battle formations (tactics skill effects).
####################################################################################################################

encounters_scripts = [
  # This script is called from the game engine whenever player party encounters another party or a battle on the world map
  # INPUT:
  # param1: encountered_party
  # param2: second encountered_party (if this was a battle
  ("game_event_party_encounter",
   [
       (store_script_param_1, "$g_encountered_party"),
       (store_script_param_2, "$g_encountered_party_2"),# encountered_party2 is set when we come across a battle or siege, otherwise it's a negative value
#       (store_encountered_party, "$g_encountered_party"),
#       (store_encountered_party2,"$g_encountered_party_2"), # encountered_party2 is set when we come across a battle or siege, otherwise it's a minus value
       (store_faction_of_party, "$g_encountered_party_faction","$g_encountered_party"),
       (store_relation, "$g_encountered_party_relation", "$g_encountered_party_faction", "fac_player_faction"),

       (party_get_slot, "$g_encountered_party_type", "$g_encountered_party", slot_party_type),
       (party_get_template_id,"$g_encountered_party_template","$g_encountered_party"),
#       (try_begin),
#         (gt, "$g_encountered_party_2", 0),
#         (store_faction_of_party, "$g_encountered_party_2_faction","$g_encountered_party_2"),
#         (store_relation, "$g_encountered_party_2_relation", "$g_encountered_party_2_faction", "fac_player_faction"),
#         (party_get_template_id,"$g_encountered_party_2_template","$g_encountered_party_2"),
#       (else_try),
#         (assign, "$g_encountered_party_2_faction",-1),
#         (assign, "$g_encountered_party_2_relation", 0),
#         (assign,"$g_encountered_party_2_template", -1),
#       (try_end),


#NPC companion changes begin
       (call_script, "script_party_count_fit_regulars", "p_main_party"),
       (assign, "$playerparty_prebattle_regulars", reg0),

#        (try_begin),
#            (assign, "$player_party__regulars", 0),
#            (call_script, "script_party_count_fit_regulars", "p_main_party"),
#            (gt, reg0, 0),
#            (assign, "$player_party_contains_regulars", 1),
#        (try_end),
#NPC companion changes end


        (assign, "$g_last_rest_center", -1),
        (assign, "$talk_context", 0),
        (assign, "$g_player_surrenders",0),
        (assign, "$g_enemy_surrenders",0),
        (assign, "$g_leave_encounter",0),
        (assign, "$g_engaged_enemy", 0),
#       (assign,"$waiting_for_arena_fight_result", 0),
#       (assign,"$arena_bet_amount",0),
#       (assign,"$g_player_raiding_village",0),
        (try_begin),
          (neg|is_between, "$g_encountered_party", centers_begin, centers_end),
          (rest_for_hours, 0), #stop waiting
          (assign, "$g_infinite_camping", 0),
        (try_end),
        #       (assign, "$g_permitted_to_center",0),
        #SB : do cheat here before other menus are accessed
      (try_begin),
        (eq, "$new_encounter", 2),
        (jump_to_menu, "mnu_party_cheat"),
      (else_try),
        (assign, "$new_encounter", 1), #check this in the menu.
        (try_begin),
         (lt, "$g_encountered_party_2",0), #Normal encounter. Not battle or siege.
         (try_begin),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
           (jump_to_menu, "mnu_castle_outside"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
           (jump_to_menu, "mnu_ship_reembark"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
           (jump_to_menu, "mnu_village"),
         (else_try),
           (party_slot_eq, "$g_encountered_party", slot_party_type, spt_cattle_herd),
           (jump_to_menu, "mnu_cattle_herd"),
         (else_try),
           (is_between, "$g_encountered_party", training_grounds_begin, training_grounds_end),
           (jump_to_menu, "mnu_training_ground"),
         (else_try),
           (party_get_template_id, ":template", "$g_encountered_party"), #SB : is_between range
           (is_between, ":template", "pt_steppe_bandit_lair", "pt_bandit_lair_templates_end"),
           (assign, "$loot_screen_shown", 0),
           (jump_to_menu, "mnu_bandit_lair"),
         (else_try),
           (is_between, "$g_encountered_party", "p_port_1", "p_ports_end"),
           (party_get_slot, ":port_town", "$g_encountered_party", slot_port_town),
           (party_get_position, pos0, ":port_town"),
           (assign, "$g_player_icon_state", pis_normal),
           (party_set_flags, "p_main_party", pf_is_ship, 0),
           (assign, "$g_main_ship_party", -1),
           (party_set_slot, "p_main_party", slot_party_ship_type, 0),
           (party_set_position, "p_main_party", pos0),
           (jump_to_menu, "mnu_auto_return"),
         (else_try),
           (eq, "$g_encountered_party", "p_zendar"),
           (jump_to_menu, "mnu_zendar"),
         (else_try),
           (eq, "$g_encountered_party", "p_salt_mine"),
           (jump_to_menu, "mnu_salt_mine"),
         (else_try),
           (eq, "$g_encountered_party", "p_four_ways_inn"),
           (jump_to_menu, "mnu_four_ways_inn"),
         (else_try),
           (eq, "$g_encountered_party", "p_test_scene"),
           (jump_to_menu, "mnu_test_scene"),
         (else_try),
           (eq, "$g_encountered_party", "p_battlefields"),
           (jump_to_menu, "mnu_battlefields"),
         (else_try),
           (eq, "$g_encountered_party", "p_training_ground"),
           (jump_to_menu, "mnu_tutorial"),
         (else_try),
           (eq, "$g_encountered_party", "p_camp_bandits"),
           (jump_to_menu, "mnu_camp"),
         (else_try),
           (jump_to_menu, "mnu_simple_encounter"),
         (try_end),
        (else_try), #Battle or siege
          (try_begin),
            (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),
            (try_begin),
              (eq, "$auto_enter_town", "$g_encountered_party"),
              (jump_to_menu, "mnu_town"),
            (else_try),
              (eq, "$auto_besiege_town", "$g_encountered_party"),
              (jump_to_menu, "mnu_besiegers_camp_with_allies"),
            (else_try),
              (jump_to_menu, "mnu_join_siege_outside"),
            (try_end),
          (else_try),
            (jump_to_menu, "mnu_pre_join"),
          (try_end),
        (try_end),
      (try_end),
       (assign,"$auto_enter_town",0),
       (assign,"$auto_besiege_town",0),
      ]),

  #script_game_event_simulate_battle:
  # This script is called whenever the game simulates the battle between two parties on the map.
  # INPUT:
  # param1: Defender Party
  # param2: Attacker Party
  ("game_event_simulate_battle",
    [
      (store_script_param_1, ":root_defender_party"),
      (store_script_param_2, ":root_attacker_party"),

      (assign, "$marshall_defeated_in_battle", -1),

      (store_current_hours, ":hours"),

      ##diplomacy start+ Get campaign AI, used below
      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      ##diplomacy end+

      (try_for_parties, ":party"),
        (party_get_battle_opponent, ":opponent", ":party"),
        (gt, ":opponent", 0),
        (party_set_slot, ":party", slot_party_last_in_combat, ":hours"),
      (try_end),

      (assign, ":trigger_result", 1),
      (try_begin),
        (ge, ":root_defender_party", 0),
        (ge, ":root_attacker_party", 0),
        (party_is_active, ":root_defender_party"),
        (party_is_active, ":root_attacker_party"),
        (store_faction_of_party, ":defender_faction", ":root_defender_party"),
        (store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
        #(neq, ":defender_faction", "fac_player_faction"),
        #(neq, ":attacker_faction", "fac_player_faction"),
        (store_relation, ":reln", ":defender_faction", ":attacker_faction"),
        (lt, ":reln", 0),
        (assign, ":trigger_result", 0),

        (try_begin),
          (this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
          (eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
          (assign, "$g_battle_simulation_cancel_for_party", -1),
          (assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),
          (assign, ":trigger_result", 1),
        (else_try),
          (try_begin),
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
            (party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
            (assign, ":trigger_result", 1), #End battle!
          (try_end),
          (party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),

          #(assign, ":cancel_attack", 0),

          (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),

	      ##diplomacy start+
 		  (assign, ":terrain_code", dplmc_terrain_code_none),#defined in header_terrain.py
          (try_begin),
              (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			  (call_script, "script_dplmc_get_terrain_code_for_battle", ":root_attacker_party", ":root_defender_party"),
			  (assign, ":terrain_code", reg0),
			  #
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_ally", ":terrain_code", 0, 1),
              (assign, ":defender_strength", reg0),
              (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code", 0, 1),
              (assign, ":attacker_strength", reg0),
          (else_try),
              (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
              (assign, ":defender_strength", reg0),
          #(call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
              (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
              (assign, ":attacker_strength", reg0),
          (try_end),
          ##diplomacy end+

          (store_div, ":defender_strength", ":defender_strength", 20),
          (val_min, ":defender_strength", 50),
          (val_max, ":defender_strength", 1),
          (store_div, ":attacker_strength", ":attacker_strength", 20),
          (val_min, ":attacker_strength", 50),
          (val_add, ":attacker_strength", 1),
          (try_begin),
            #For sieges increase attacker casualties and reduce defender casualties.
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
            (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
            (val_mul, ":defender_strength", 123), #it was 1.5 in old version, now it is only 1.23
            (val_div, ":defender_strength", 100),

            (val_mul, ":attacker_strength", 100), #it was 0.5 in old version, now it is only 1 / 1.23
            (val_div, ":attacker_strength", 123),
          (try_end),

          ##diplomacy begin
          (assign, ":defender_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":defender_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":defender_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":defender_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":defender_percent", ":quality"),
          (try_end),
          (val_mul, ":defender_strength", ":defender_percent"),
          (val_div, ":defender_strength", 100),

          (assign, ":attacker_percent", 100),
          (try_begin),
            (faction_get_slot, ":serfdom", ":attacker_faction", dplmc_slot_faction_serfdom),
            (neq, ":serfdom", 0),
            (val_mul, ":serfdom", -2),
            (val_add, ":attacker_percent", ":serfdom"),
          (try_end),
          (try_begin),
            (faction_get_slot, ":quality", ":attacker_faction", dplmc_slot_faction_quality),
            (neq, ":quality", 0),
            (val_mul, ":quality", 4),
            (val_add, ":attacker_percent", ":quality"),
          (try_end),
          (val_mul, ":attacker_strength", ":attacker_percent"),
          (val_div, ":attacker_strength", 100),
          ##diplomacy end

          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":old_defender_strength", reg0),

          (try_begin),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
          (assign, ":new_attacker_strength", reg0),

          (try_begin),
            (gt, ":new_attacker_strength", 0),
            (neg|is_currently_night), #Don't fight at night
            (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
            (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (try_end),
          (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
          (assign, ":new_defender_strength", reg0),

          (try_begin),
            (this_or_next|eq, ":new_attacker_strength", 0),
            (eq, ":new_defender_strength", 0),
            # Battle concluded! determine winner

            (assign, ":do_not_end_battle", 0),
            (try_begin),
              (neg|troop_is_wounded, "trp_player"),
              (eq, ":new_defender_strength", 0),
              (eq, "$auto_enter_town", "$g_encountered_party"),
              (eq, ":old_defender_strength", ":new_defender_strength"),
              (assign, ":do_not_end_battle", 1),
            (try_end),
            (eq, ":do_not_end_battle", 0),

            (try_begin),
              (eq, ":new_attacker_strength", 0),
              (eq, ":new_defender_strength", 0),
              (assign, ":root_winner_party", -1),
              (assign, ":root_defeated_party", -1),
              (assign, ":collective_casualties", -1),
            (else_try),
              (eq, ":new_attacker_strength", 0),
              (assign, ":root_winner_party", ":root_defender_party"),
              (assign, ":root_defeated_party", ":root_attacker_party"),
              (assign, ":collective_casualties", "p_collective_enemy"),
            (else_try),
              (assign, ":root_winner_party", ":root_attacker_party"),
              (assign, ":root_defeated_party", ":root_defender_party"),
              (assign, ":collective_casualties", "p_collective_ally"),
            (try_end),
##diplomacy begin
        (try_begin),
          (gt, ":root_defeated_party", -1),
# Recruiter kit begin
 # This little fella just shows a message when a recruiter is defeated.

         (assign, ":minimum_distance", 1000000),
         (try_for_range, ":center", centers_begin, centers_end),
           (store_distance_to_party_from_party, ":dist", ":root_defeated_party", ":center"),
           (try_begin),
             (lt, ":dist", ":minimum_distance"),
             (assign, ":minimum_distance", ":dist"),
             (assign, ":nearest_center", ":center"),
           (try_end),
         (try_end),

        (str_clear, s10),
        (try_begin),
          (gt, ":nearest_center", 0),
          (str_store_party_name, s10, ":nearest_center"),
          (str_store_string, s10, "@ near {s10}"),
        (try_end),

        #SB : reformat loop
        (party_get_slot, ":type", ":root_defeated_party", slot_party_type),
        (try_begin),
          (eq, ":type", dplmc_spt_recruiter),
          (party_get_slot, reg10, ":root_defeated_party", dplmc_slot_party_recruiter_needed_recruits),
          (party_get_slot, ":party_origin", ":root_defeated_party", dplmc_slot_party_recruiter_origin),
          (str_store_party_name_link, s13, ":party_origin"),
          (display_log_message, "@Your recruiter who was commissioned to recruit {reg10} recruits to {s13} has been defeated{s10}!", message_defeated),
        (else_try),
          (eq,":type", dplmc_spt_gift_caravan),
          (party_get_slot, ":target_troop", ":root_defeated_party", slot_party_orders_object),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (try_begin),
            (gt, ":target_troop", 0),
            (str_store_troop_name, s13, ":target_troop"),
          (else_try),
            (str_store_party_name, s13, ":target_party"),
          (end_try),
          (party_get_slot, ":gift", ":root_defeated_party", dplmc_slot_party_mission_diplomacy),
          (str_store_item_name, s12, ":gift"),
          #SB : defeated -> looted
          (display_log_message, "@Your caravan sending {s12} to {s13} has been looted{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_messenger),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),
          #SB : defeated -> intercepted
          (display_log_message, "@Your messenger on the way to {s13} has been ambushed{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_patrol),
          (party_slot_eq, ":root_defeated_party", dplmc_slot_party_mission_diplomacy, "trp_player"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_ai_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@Your soldiers patrolling {s13} have been defeated{s10}!", message_defeated),
        (else_try),
          (eq, ":type", spt_scout),
          (store_faction_of_party, ":party_faction", ":root_defeated_party"),
          (eq, ":party_faction", "$players_kingdom"),
          (party_get_slot, ":target_party", ":root_defeated_party", slot_party_orders_object),
          (str_store_party_name, s13, ":target_party"),
          (display_log_message, "@A scout trying to gather information about {s13} has been slain{s10}!", message_defeated),
        (else_try), #SB : reinforcements
          (eq, ":type", spt_reinforcement),
          (store_faction_of_party, ":party_faction", ":root_defeated_party"),
          (eq, ":party_faction", "$players_kingdom"), #show only if relevant
          (party_get_slot, ":home_village", ":root_defeated_party", slot_party_home_center),
          (party_get_slot, ":target_party", ":home_village", slot_village_bound_center),
          (str_store_party_name_link, s12, ":home_village"),
          (str_store_party_name_link, s13, ":target_party"),
          (display_log_message, "@Reinforcements from {s12} intended for {s13} have been intercepted{s10}!", message_defeated),
        (try_end),
      (try_end),
##diplomacy end

            (try_begin),
              (ge, ":root_winner_party", 0),
              (call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
              (assign, ":nonempty_winner_party", reg0),
              (store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
              (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
            (else_try),
              (assign, ":nonempty_winner_party", -1),
            (try_end),

            (try_begin),
              (ge, ":collective_casualties", 0),
              (party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
            (else_try),
              (assign, ":num_stacks", 0),
            (try_end),

            #SB : set up primary color here
            (faction_get_color, ":faction_color", ":faction_receiving_prisoners"),
            #depending on war status we can enforce either message_positive or message_negative
            (try_for_range, ":troop_iterator", 0, ":num_stacks"),
              (party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
              (troop_is_hero, ":cur_troop_id"),

              (try_begin),
                #abort quest if troop loses a battle during rest time
                (check_quest_active, "qst_lend_surgeon"),
                (quest_slot_eq, "qst_lend_surgeon", slot_quest_giver_troop, ":cur_troop_id"),
                (call_script, "script_abort_quest", "qst_lend_surgeon", 0),
              (try_end),

              (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),

              (troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),

              (store_random_in_range, ":rand", 0, 100),
              (str_store_troop_name_link, s1, ":cur_troop_id"),
              (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
              (store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
              (str_store_faction_name_link, s3, ":defeated_troop_faction"),
              #SB : colorize
              (faction_get_color, ":color", ":defeated_troop_faction"),
              (try_begin),
                (this_or_next|eq, ":nonempty_winner_party", "p_main_party"),
                (ge, ":rand", hero_escape_after_defeat_chance),

                #dckplmc
                (party_get_template_id, ":party_template", ":root_defeated_party"),
                (try_begin),
                    (eq, ":party_template", "pt_hero_party"),
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                    # (assign, ":continue", 1),
                    # (assign, ":minimum_distance", 99999),
                    # (assign, ":prison_center", -1),
                     # (try_for_range, ":center", walled_centers_begin, walled_centers_end),
                        # (store_distance_to_party_from_party, ":dist", ":center", ":root_defeated_party"),
                        # (lt, ":dist", ":minimum_distance"),
                        # (assign, ":minimum_distance", ":dist"),
                        # (assign, ":prison_center", ":center"),
                     # (try_end),
                      # (assign, reg1, ":prison_center"),
                      # #(display_message, "@{!}DEBUG : prison center is {reg1}"),
                      # (try_begin),
                        # (ge, ":prison_center", 0),
                        # (party_add_prisoners, ":prison_center", ":cur_troop_id", 1),
                        # (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":prison_center"),
                      # (else_try),
                        # (store_random_in_range, ":town_no", towns_begin, towns_end),
                        # (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                      # (try_end),
                (try_end),
                #(neq, ":party_template", "pt_hero_party"), #end




                (party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
                ##diplomacy start+ kingdom ladies might lead kingdom parties
                (this_or_next|is_between,":leader_troop_id", kingdom_ladies_begin, kingdom_ladies_end),
                   (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end),

                (this_or_next|troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
                ##diplomacy end+
                (is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end), #disable non-kingdom parties capturing enemy lords
                (party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1),
                (gt, reg0, 0),
                #(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
                (troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),

                (display_log_message, "str_hero_taken_prisoner", ":color"),

                (try_begin),
                  (call_script, "script_cf_prisoner_offered_parole", ":cur_troop_id"),

                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner granted parole"),
                  (try_end),

                  (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", 3),
				  (val_add, "$total_battle_enemy_changes", 3),
                (else_try),
                  (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Prisoner not offered parole"),
		          (try_end),

		          (call_script, "script_troop_change_relation_with_troop", ":leader_troop_id", ":cur_troop_id", -5),
				  (val_add, "$total_battle_enemy_changes", -5),
		        (try_end),

				(store_faction_of_party, ":capturer_faction", ":nonempty_winner_party"),
                (call_script, "script_update_troop_location_notes_prisoned", ":cur_troop_id", ":capturer_faction"),
              (else_try),

                #dckplmc
                (try_begin),
                    (party_get_template_id, ":party_template", ":root_defeated_party"),
                    (eq, ":party_template", "pt_hero_party"),
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (store_random_in_range, ":town_no", towns_begin, towns_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                (try_end),

                (display_message,"@{s1} of {s3} was defeated in battle but managed to escape.", ":color"),
              (try_end),

              (try_begin),
                (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
                (is_between, ":cur_troop_faction", kingdoms_begin, kingdoms_end),
                (assign, "$marshall_defeated_in_battle", ":cur_troop_id"),
                #Marshall is defeated, refresh ai.
                (assign, "$g_recalculate_ais", 1),
              (try_end),

              ##diplomacy begin
              (try_begin),
                (call_script, "script_dplmc_is_affiliated_family_member", ":cur_troop_id"),
                (eq, reg0, 1),
                ##diplomacy start+ skip relationship decay for defeat when the player himself is imprisoned or wounded
					 (eq, "$g_player_is_captive", 0),
                (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
                (neg|troop_is_wounded, "trp_player"),
                ##diplomacy end+
					 (assign, ":mitigating_factors", 0),
					 (try_begin),
					    #Being at war with the troop's faction is a mitigating factor, unless the player leads his faction.
						 (store_relation, reg0, "$players_kingdom", ":cur_troop_faction"),
						 (lt, reg0, 0),
						 (neq, "$players_kingdom", "fac_player_supporters_faction"),
						 (neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
						 (assign, ":mitigating_factors", 1),
					 (try_end),

                (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
					   ##diplomacy start+
						#The dead, exiled, and retired don't participate in this
						(neg|troop_slot_ge, ":family_member", slot_troop_occupation, slto_retirement),
						#Members of factions at war with the defeated affiliate's faction don't have
						#any relation loss either: it would be nonsensical for them to be willing to
						#battle him themselves, but become enraged at his defeat.
						(store_troop_faction, ":family_member_faction", ":family_member"),
						(store_relation, reg0, ":family_member_faction", ":cur_troop_faction"),
						(this_or_next|eq, ":family_member_faction", ":cur_troop_faction"),
							(ge, reg0, 0),
                  ##(call_script, "script_troop_get_family_relation_to_troop", ":family_member", "$g_player_affiliated_troop"),
                  (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
                  (gt, reg0, 0),
                  (assign, reg0, -2),
                  (try_begin),
                    (eq, ":reduce_campaign_ai", 0),#hard: -1
                    (assign, reg0, -1),
                  (else_try),
                    (eq, ":reduce_campaign_ai", 1),#medium: -1 or 0
                    (store_random_in_range, reg0, -1, 1),
                  (else_try),
                    (eq, ":reduce_campaign_ai", 2),#easy: 0
                    (assign, reg0, 0),
                  (try_end),
                  (val_add, reg0, ":mitigating_factors"),
                  (lt, reg0, 0),
                  (call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
                  ##diplomacy end+
                (try_end),
              (try_end),
              ##diplomacy end
            (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
             (else_try),
               (assign, ":num_stacks", 0),
             (try_end),
             (try_for_range, ":troop_iterator", 0, ":num_stacks"),
               (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
               (troop_is_hero, ":cur_troop_id"),
               (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
               (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
               (str_store_troop_name_link, s1, ":cur_troop_id"),
               (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
               (str_store_faction_name_link, s3, ":cur_troop_faction"),
               #SB : colorize, use previously set up primary color
               (display_log_message, "str_hero_freed", ":faction_color"),

                (try_begin), #dckplmc
                    (is_between, ":cur_troop_id", companions_begin, companions_end),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
                    (neg|troop_slot_eq, ":cur_troop_id", slot_troop_occupation, slto_kingdom_hero),
                    (store_random_in_range, ":town_no", towns_begin, towns_end),
                    (troop_set_slot, ":cur_troop_id", slot_troop_cur_center, ":town_no"),
                    (troop_set_slot, ":cur_troop_id", slot_troop_playerparty_history, pp_history_scattered),
                    (troop_set_slot, ":cur_troop_id", slot_troop_turned_down_twice, 0),
                    (troop_set_slot, ":cur_troop_id", slot_troop_occupation, 0),
                (try_end),
             (try_end),

             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_clear, "p_temp_party"),
               (assign, "$g_move_heroes", 0), #heroes are already processed above. Skip them here.
               (call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
               (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
               (distribute_party_among_party_group, "p_temp_party", ":root_winner_party"),

               (call_script, "script_battle_political_consequences", ":root_defeated_party", ":root_winner_party"),

               (call_script, "script_clear_party_group", ":root_defeated_party"),
             (try_end),
             (assign, ":trigger_result", 1), #End battle!

             #Center captured
             (try_begin),
               (ge, ":collective_casualties", 0),
               (party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
               (this_or_next|eq, ":cur_party_type", spt_town),
               (eq, ":cur_party_type", spt_castle),

               #free all captive ladies
               (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                   (troop_get_slot, ":center", ":lady", slot_troop_prisoner_of_party),
                   (neg|troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_hero),
                   (eq, ":root_defeated_party", ":center"),
                   (call_script, "script_remove_troop_from_prison", ":lady"),
                   (store_faction_of_troop, ":lady_faction", ":lady"),
                   (store_faction_of_party, ":rescue_faction", ":root_winner_party"),
                   (faction_get_color, ":lady_faction_color", ":lady_faction"),
                   (str_store_troop_name_link, s1, ":lady"),
                   (str_store_faction_name_link, s2, ":rescue_faction"),
                   (str_store_faction_name_link, s3, ":lady_faction"),
                   (display_log_message, "str_hero_freed", ":lady_faction_color"),
               (try_end),

               (assign, "$g_recalculate_ais", 1),

               (store_faction_of_party, ":winner_faction", ":root_winner_party"),
               (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),

               (str_store_party_name, s1, ":root_defeated_party"),
               (str_store_faction_name, s2, ":winner_faction"),
               (str_store_faction_name, s3, ":defeated_faction"),
               ## CC
               (faction_get_color, ":faction_color", ":winner_faction"),
               (display_log_message, "str_center_captured", ":faction_color"),
               ## CC

			   (store_current_hours, ":hours"),
			   (faction_set_slot, ":winner_faction", slot_faction_ai_last_decisive_event, ":hours"),

               (try_begin),
                 (eq, "$g_encountered_party", ":root_defeated_party"),
                 (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
                 (call_script, "script_change_player_relation_with_lords_after_battle"),
               (try_end),

               (try_begin),
                 (party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
                 (gt, ":num_stacks", 0),
                 (party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
		##diplomacy start+ support for promoted kingdom ladies
                 (is_between, ":leader_troop_no", heroes_begin, heroes_end),#<- dplmc+ added
                 (this_or_next|troop_slot_eq, ":leader_troop_no", slot_troop_occupation, slto_kingdom_hero),#<- dplmc+ addded
                     (is_between, ":leader_troop_no", active_npcs_begin, active_npcs_end),
		##diplomacy end+
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
               (else_try),
                 (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
               (try_end),

               (call_script, "script_lift_siege", ":root_defeated_party", 0),
               (call_script, "script_spawn_looters", ":root_defeated_party", 5), #SB : spawn some looters
               (store_faction_of_party, ":fortress_faction", ":root_defeated_party"),
			   (try_begin),
			     (is_between, ":root_defeated_party", towns_begin, towns_end),
			     (assign, ":damage", 40),
			   (else_try),
			     (assign, ":damage", 20),
			   (try_end),
			   (call_script, "script_faction_inflict_war_damage_on_faction", ":winner_faction", ":fortress_faction", ":damage"),

               (call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"),
               (try_begin),
			     ##diplomacy start+ Handle player is co-ruler of faction
			     (assign, ":is_defeated_faction_coruler", 0),
            	 (try_begin),
            		##zerilius changes begin
            		(eq, ":defeated_faction", "$players_kingdom"),
            		# (eq, ":is_defeated_faction_coruler", "$players_kingdom"),
            		##zerilius changes end
            		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
            		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            		(assign, ":is_defeated_faction_coruler", 1),
            	 (try_end),
				 (this_or_next|eq, ":is_defeated_faction_coruler", 1),
	  		     ##diplomacy end+
                 (eq, ":defeated_faction", "fac_player_supporters_faction"),
                 (call_script, "script_add_notification_menu", "mnu_notification_center_lost", ":root_defeated_party", ":winner_faction"),
               (try_end),

               (party_get_num_attached_parties, ":num_attached_parties",  ":root_attacker_party"),
                 (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
                 (party_get_attached_party_with_rank, ":attached_party", ":root_attacker_party", ":attached_party_rank"),

                 (party_get_num_companion_stacks, ":num_stacks", ":attached_party"),
                 (assign, ":total_size", 0),
                 (try_for_range, ":i_stack", 0, ":num_stacks"),
                   (party_stack_get_size, ":stack_size", ":attached_party", ":i_stack"),
                   (val_add, ":total_size", ":stack_size"),
                 (try_end),

                 (try_begin),
                   (ge, ":total_size", 10),

                   (assign, ":stacks_added", 0),
                   (assign, ":last_random_stack", -1),

                   (assign, ":end_condition", 10),
                   (try_for_range, ":unused", 0, ":end_condition"),
                     (store_random_in_range, ":random_stack", 1, ":num_stacks"),
                     (party_stack_get_troop_id, ":random_stack_troop", ":attached_party", ":random_stack"),
                     (party_stack_get_size, ":stack_size", ":attached_party", ":random_stack"),
                     (ge, ":stack_size", 4),
                     (neq, ":random_stack", ":last_random_stack"),

                     (store_mul, ":total_size_mul_2", ":total_size", 2),
                     (assign, ":percentage", ":total_size_mul_2"),
                     (val_min, ":percentage", 100),

                     (val_mul, ":stack_size", ":percentage"),
                     (val_div, ":stack_size", 100),

                     (party_stack_get_troop_id, ":party_leader", ":attached_party", 0),

                     (try_begin),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_conventional),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_otherworldly),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_adventurous),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_goodnatured),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_upstanding),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_martial),
                       (assign, reg2, 0),
                       (store_random_in_range, ":random_percentage", 40, 50), #average 45%
                     (else_try),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_ambitious),
                       ##diplmoacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_quarrelsome),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_cunning),
                       (assign, reg2, 1),
                       (store_random_in_range, ":random_percentage", 30, 40), #average 35%
                     (else_try),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_selfrighteous),
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_roguish),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_debauched),
                       (assign, reg2, 2),
                       (store_random_in_range, ":random_percentage", 20, 30), #average 25%
                     (else_try),
                       ##diplomacy start+ add lady personality
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_moralist),
                       ##diplomacy end+
                       (this_or_next|troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_benefactor),
                       (troop_slot_eq, ":party_leader", slot_lord_reputation_type, lrep_custodian),
                       (assign, reg2, 3),
                       (store_random_in_range, ":random_percentage", 50, 60), #average 55%
                     (try_end),

                     (val_min, ":random_percentage", 100),
                     (val_mul, ":stack_size", ":random_percentage"),
                     (val_div, ":stack_size", 100),

                     (party_add_members, ":root_defender_party", ":random_stack_troop", ":stack_size"),
                     (party_remove_members, ":attached_party", ":random_stack_troop", ":stack_size"),

                     (val_add, ":stacks_added", 1),
                     (assign, ":last_random_stack", ":random_stack"),

                     (try_begin),
                       #if troops from three different stack is already added then break
                       (eq, ":stacks_added", 3),
                       (assign, ":end_condition", 0),
                     (try_end),
                   (try_end),
                 (try_end),
               (try_end),

               #Reduce prosperity of the center by 5
			   (try_begin),
			     (neg|is_between, ":root_defeated_party", castles_begin, castles_end),
			     (call_script, "script_change_center_prosperity", ":root_defeated_party", -5),
			     (val_add, "$newglob_total_prosperity_from_townloot", -5),
			   (try_end),
               (call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
               (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
             (try_end),
           (try_end),

           #ADD XP
           (try_begin),
             (party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),

             (assign, ":xp_gained_attacker", 200),
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (store_faction_of_party, ":root_attacker_party_faction", ":root_attacker_party"),
             (try_begin),
               (this_or_next|eq, ":root_attacker_party", "p_main_party"),
               (this_or_next|eq, ":root_attacker_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_attacker_party_faction", "$players_kingdom"),
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_attacker", 3),
               (val_div, ":xp_gained_attacker", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_attacker", 2),
             (try_end),

             (gt, ":new_attacker_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_attacker_party", ":xp_gained_attacker"),
           (try_end),
           (try_begin),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),

             (assign, ":xp_gained_defender", 200),
             (store_faction_of_party, ":root_defender_party_faction", ":root_defender_party"),
             (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             (try_begin),
               (this_or_next|eq, ":root_defender_party", "p_main_party"),
               (this_or_next|eq, ":root_defender_party_faction", "fac_player_supporters_faction"),
               (eq, ":root_defender_party_faction", "$players_kingdom"),
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
               (val_mul, ":xp_gained_defender", 3),
               (val_div, ":xp_gained_defender", 2),
             (else_try),
               (eq, ":reduce_campaign_ai", 1), #moderate (1.0x)
               #same
             (else_try),
               (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
               (val_div, ":xp_gained_defender", 2),
             (try_end),

             (gt, ":new_defender_strength", 0),
             (call_script, "script_upgrade_hero_party", ":root_defender_party", ":xp_gained_defender"),
           (try_end),

           (try_begin),
             #ozan - do not randomly end battles aganist towns or castles.
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle), #added by ozan
             (neg|party_slot_eq, ":root_defender_party", slot_party_type, spt_town),   #added by ozan
             #end ozan

             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_attacker_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_attacker_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_defender_followers", ":root_defender_party", slot_party_follower_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_defender_followers"),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),

             (try_begin),
               (lt, ":random_num", 10),
               (assign, ":trigger_result", 1), #End battle!
             (try_end),
           (else_try),
             (party_get_slot, ":attacker_root_strength", ":root_attacker_party", slot_party_cached_strength),
             (party_get_slot, ":attacker_nearby_friend_strength", ":root_attacker_party", slot_party_nearby_friend_strength),
             (party_get_slot, ":strength_of_followers", ":root_attacker_party", slot_party_follower_strength),
             (store_add, ":total_attacker_strength", ":attacker_root_strength", ":attacker_nearby_friend_strength"),
             (val_add, ":total_attacker_strength", ":strength_of_followers"),

             (party_get_slot, ":defender_root_strength", ":root_defender_party", slot_party_cached_strength),
             (party_get_slot, ":defender_nearby_friend_strength", ":root_defender_party", slot_party_nearby_friend_strength),
             (store_add, ":total_defender_strength", ":defender_root_strength", ":defender_nearby_friend_strength"),

             (val_mul, ":total_defender_strength", 13), #multiply defender strength with 1.3
             (val_div, ":total_defender_strength", 10),

             (gt, ":total_defender_strength", ":total_attacker_strength"),
             (gt, ":total_defender_strength", 3),

             #Players can make save loads and change history because these random values are not determined from random_slots of troops
             (store_random_in_range, ":random_num", 0, 100),

             (try_begin),
               (lt, ":random_num", 15), #15% is a bit higher than 10% (which is open area escape probability)
               (assign, ":trigger_result", 1), #End battle!

               (assign, "$g_recalculate_ais", 1), #added new

               (try_begin),
                 (eq, "$cheat_mode", 1),
                 (display_message, "@{!}DEBUG : Siege attackers are running away"),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
       (try_end),
       (set_trigger_result, ":trigger_result"),
  ]),

  #script_game_event_battle_end:
  # Output: reg0 = battle advantage
  ("calculate_battle_advantage",
    [
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, ":friend_count", reg(0)),

      (party_get_skill_level, ":player_party_tactics",  "p_main_party", skl_tactics),
      (party_get_skill_level, ":ally_party_tactics",  "p_collective_friends", skl_tactics),
      (val_max, ":player_party_tactics", ":ally_party_tactics"),

      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, ":enemy_count", reg(0)),

      (party_get_skill_level, ":enemy_party_tactics",  "p_collective_enemy", skl_tactics),

      (val_add, ":friend_count", 1),
      (val_add, ":enemy_count", 1),

      (try_begin),
        (ge, ":friend_count", ":enemy_count"),
        (val_mul, ":friend_count", 100),
        (store_div, ":ratio", ":friend_count", ":enemy_count"),
        (store_sub, ":raw_advantage", ":ratio", 100),
      (else_try),
        (val_mul, ":enemy_count", 100),
        (store_div, ":ratio", ":enemy_count", ":friend_count"),
        (store_sub, ":raw_advantage", 100, ":ratio"),
      (try_end),
      (val_mul, ":raw_advantage", 2),

      (val_mul, ":player_party_tactics", 30),
      (val_mul, ":enemy_party_tactics", 30),
      (val_add, ":raw_advantage", ":player_party_tactics"),
      (val_sub, ":raw_advantage", ":enemy_party_tactics"),
      (val_div, ":raw_advantage", 100),


      (assign, reg0, ":raw_advantage"),
      (display_message, "@Battle Advantage = {reg0}.", 0xFFFFFFFF),
  ]),


  # script_cf_check_enemies_nearby
  # Input: none
  # Output: none
  ("select_battle_tactic",
    [
      (assign, "$ai_team_1_battle_tactic", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (num_active_teams_le, 2),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (assign, "$ai_team_2", -1),
      (else_try),
        (try_begin),
          (eq, ":player_team", 0),
          (assign, "$ai_team_1", 1),
        (else_try),
          (assign, "$ai_team_1", 0),
        (try_end),
        (store_add, "$ai_team_2", ":player_team", 2),
      (try_end),
      (call_script, "script_select_battle_tactic_aux", "$ai_team_1", 0),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (assign, ":defense_not_an_option", 0),
        (try_begin),
          (eq, "$ai_team_1_battle_tactic", btactic_hold),
          (assign, ":defense_not_an_option", 1), #don't let two AI defend at the same time
        (try_end),
        (call_script, "script_select_battle_tactic_aux", "$ai_team_2", ":defense_not_an_option"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ]),

  # script_select_battle_tactic_aux
  # Input: team_no
  # Output: battle_tactic
  ("select_battle_tactic_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":defense_not_an_option", 2),
      (assign, ":battle_tactic", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_begin),
        (eq, "$cant_leave_encounter", 1),
        (teams_are_enemies, ":team_no", ":player_team"),
        (assign, ":defense_not_an_option", 1),
      (try_end),
      (call_script, "script_team_get_class_percentages", ":team_no", 0),
      #      (assign, ":ai_perc_infantry", reg0),
      (assign, ":ai_perc_archers",  reg1),
      (assign, ":ai_perc_cavalry",  reg2),
      (call_script, "script_team_get_class_percentages", ":team_no", 1),#enemies of the ai_team
      #      (assign, ":enemy_perc_infantry", reg0),
      #      (assign, ":enemy_perc_archers",  reg1),
      #      (assign, ":enemy_perc_cavalry",  reg2),

      (store_random_in_range, ":rand", 0, 100),
      (try_begin),
        (assign, ":continue", 0),
        (try_begin),
          (teams_are_enemies, ":team_no", ":player_team"),
          (party_slot_eq, "$g_enemy_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (else_try),
          (neg|teams_are_enemies, ":team_no", ":player_team"),
          (gt, "$g_ally_party", 0),
          (party_slot_eq, "$g_ally_party", slot_party_type, spt_kingdom_hero_party),
          (assign, ":continue", 1),
        (try_end),
        #(this_or_next|lt, ":rand", 20),
        (eq, ":continue", 1),
		(store_faction_of_party, ":enemy_faction_no", "$g_enemy_party"),
		(neq, ":enemy_faction_no", "fac_kingdom_3"), #don't let khergits use battle tactics
        (try_begin),
          (eq, ":defense_not_an_option", 0),
          (gt, ":ai_perc_archers", 50),
          (lt, ":ai_perc_cavalry", 35),
          (assign, ":battle_tactic", btactic_hold),
        (else_try),
          (lt, ":rand", 80),
          (assign, ":battle_tactic", btactic_follow_leader),
        (try_end),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),

  # script_battle_calculate_initial_powers
  # Input: none
  # Output: none
  #("battle_calculate_initial_powers",
  #  [
  #    (try_for_agents, ":agent_no"),
  #      (agent_is_human, ":agent_no"),
  #
  #      (call_script, "script_calculate_team_powers", ":agent_no"),
  #      (assign, ":ally_power", reg0),
  #      (assign, ":enemy_power", reg1),
  #
  #      (agent_set_slot, ":agent_no", slot_agent_initial_ally_power, ":ally_power"),
  #      (agent_set_slot, ":agent_no", slot_agent_initial_enemy_power, ":enemy_power"),
  #    (try_end),
  #]),

  # script_battle_tactic_init
  # Input: none
  # Output: none
  ("battle_tactic_init",
    [
      (call_script, "script_battle_tactic_init_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_init_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0), #initially nobody is running away.
      (try_end),
  ]),

  # script_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("orig_battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (team_get_leader, ":ai_leader", ":team_no"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_get_position, pos1, ":ai_leader"),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30),
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos52),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (ge, ":ai_leader", 0),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
  ]),

  # script_calculate_team_powers


#jacobhinds Morale Code END
#(Native version)

  # script_apply_death_effect_on_courage_scores
  # Input: dead agent id, killer agent id
  # Output: none
  # ("apply_death_effect_on_courage_scores",
    # [
      # (store_script_param, ":dead_agent_no", 1),
      # (store_script_param, ":killer_agent_no", 2),

      # (try_begin),
        # (agent_is_human, ":dead_agent_no"),

        # (try_begin),
          # (agent_is_ally, ":dead_agent_no"),
          # (assign, ":is_dead_agent_ally", 1),
        # (else_try),
          # (assign, ":is_dead_agent_ally", 0),
        # (try_end),

        # (agent_get_position, pos0, ":dead_agent_no"),
        # (assign, ":number_of_near_allies_to_dead_agent", 0),

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
            # (val_add, ":number_of_near_allies_to_dead_agent", 1), # (number_of_near_allies_to_dead_agent) is counted because if there are
          # (try_end),                                              # many allies of dead agent around him, negative courage effect become less.
        # (try_end),

        # (try_for_agents, ":agent_no"),
          # (agent_is_human, ":agent_no"),
          # (agent_is_alive, ":agent_no"),

          # (try_begin),
            # (agent_is_ally, ":agent_no"),
            # (assign, ":is_agent_ally", 1),
          # (else_try),
            # (assign, ":is_agent_ally", 0),
          # (try_end),

          # (try_begin), # each agent is effected by a killed agent positively if he is rival or negatively if he is ally.
            # (neq, ":is_dead_agent_ally", ":is_agent_ally"),
            # (assign, ":agent_delta_courage_score", 10),  # if killed agent is agent of rival side, add points to fear score
          # (else_try),
            # (assign, ":agent_delta_courage_score", -15), # if killed agent is agent of our side, decrease points from fear score
            # (val_add, ":agent_delta_courage_score", ":number_of_near_allies_to_dead_agent"), # ":number_of_near_allies_to_dead_agent" is added because if there are many
            # (try_begin),                                                                     # allies of dead agent around him, negative courage effect become less.
              # (gt, ":agent_delta_courage_score", -5),
              # (assign, ":agent_delta_courage_score", -5),
            # (try_end),

            # (agent_get_slot, ":dead_agent_was_running_away_or_not", ":dead_agent_no",  slot_agent_is_running_away), #look dead agent was running away or not.
            # (try_begin),
              # (eq, ":dead_agent_was_running_away_or_not", 1),
              # (val_div, ":agent_delta_courage_score", 3),  # if killed agent was running away his negative effect on ally courage scores become very less. This added because
            # (try_end),                                     # running away agents are easily killed and courage scores become very in a running away group after a time, and
          # (try_end),                                       # they do not stop running away althought they pass near a new powerfull ally party.
          # (agent_get_position, pos1, ":agent_no"),
          # (get_distance_between_positions, ":dist", pos0, pos1),

          # (try_begin),
            # (eq, ":killer_agent_no", ":agent_no"),
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 20),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (try_end),

          # (try_begin),
            # (lt, ":dist", 100), #0-1 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 150),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 200), #2 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 120),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 300), #3 meter
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 100),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 400), #4 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 90),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 600), #5-6 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 80),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 800), #7-8 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 70),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 1000), #9-10 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 60),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 1500), #11-15 meter
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 50),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 2500), #16-25 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 40),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 4000), #26-40 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 30),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 6500), #41-65 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 20),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (else_try),
            # (lt, ":dist", 10000), #61-100 meters
            # (agent_get_slot, ":agent_courage_score", ":agent_no", slot_agent_courage_score),
            # (val_mul, ":agent_delta_courage_score", 10),
            # (val_add, ":agent_courage_score", ":agent_delta_courage_score"),
            # (agent_set_slot, ":agent_no", slot_agent_courage_score, ":agent_courage_score"),
          # (try_end),
        # (try_end),
      # (try_end),
      # ]), #ozan

  # # script_decide_run_away_or_not
  # # Input: none
  # # Output: none
  # ("decide_run_away_or_not",
    # [
      # (store_script_param, ":cur_agent", 1),
      # (store_script_param, ":mission_time", 2),

      # (assign, ":force_retreat", 0),
      # (agent_get_team, ":agent_team", ":cur_agent"),
      # (agent_get_division, ":agent_division", ":cur_agent"),
      # (try_begin),
        # (lt, ":agent_division", 9), #static classes
        # (team_get_movement_order, ":agent_movement_order", ":agent_team", ":agent_division"),
        # (eq, ":agent_movement_order", mordr_retreat),
        # (assign, ":force_retreat", 1),
      # (try_end),

      # (agent_get_slot, ":is_cur_agent_running_away", ":cur_agent", slot_agent_is_running_away),
      # (try_begin),
        # (eq, ":is_cur_agent_running_away", 0),
        # (try_begin),
          # (eq, ":force_retreat", 1),
          # (agent_start_running_away, ":cur_agent"),
          # (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
        # (else_try),
          # (ge, ":mission_time", 4), #first 45 seconds anyone does not run away whatever happens.
          # (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
          # (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
          # (val_mul, ":agent_hit_points", 4),
          # (try_begin),
            # (agent_is_ally, ":cur_agent"),
            # (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
          # (try_end),
          # (val_mul, ":agent_hit_points", 10),
          # (store_sub, ":start_running_away_courage_score_limit", 3500, ":agent_hit_points"),
          # (lt, ":agent_courage_score", ":start_running_away_courage_score_limit"), #if (courage score < 3500 - (agent hit points * 40)) and (agent is not running away) then start running away, average hit points : 50, average running away limit = 1500

          # (agent_get_troop_id, ":troop_id", ":cur_agent"), #for now do not let heroes to run away from battle
          # (neg|troop_is_hero, ":troop_id"),

          # (agent_start_running_away, ":cur_agent"),
          # (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 1),
        # (try_end),
      # (else_try),
        # (neq, ":force_retreat", 1),
        # (agent_get_slot, ":agent_courage_score", ":cur_agent",  slot_agent_courage_score),
        # (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        # (val_mul, ":agent_hit_points", 4),
        # (try_begin),
          # (agent_is_ally, ":cur_agent"),
          # (val_sub, ":agent_hit_points", 100), #ally agents will be more tend to run away, to make game more funnier/harder
        # (try_end),
        # (val_mul, ":agent_hit_points", 10),
        # (store_sub, ":stop_running_away_courage_score_limit", 3700, ":agent_hit_points"),
        # (ge, ":agent_courage_score", ":stop_running_away_courage_score_limit"), #if (courage score > 3700 - agent hit points) and (agent is running away) then stop running away, average hit points : 50, average running away limit = 1700
        # (agent_stop_running_away, ":cur_agent"),
        # (agent_set_slot, ":cur_agent",  slot_agent_is_running_away, 0),
      # (try_end),
  # ]), #ozan

  # script_battle_tactic_apply
  # Input: none
  # Output: none
  ("battle_tactic_apply",
    [
      (call_script, "script_battle_tactic_apply_aux", "$ai_team_1", "$ai_team_1_battle_tactic"),
      (assign, "$ai_team_1_battle_tactic", reg0),
      (try_begin),
        (ge, "$ai_team_2", 0),
        (call_script, "script_battle_tactic_apply_aux", "$ai_team_2", "$ai_team_2_battle_tactic"),
        (assign, "$ai_team_2_battle_tactic", reg0),
      (try_end),
  ]),

  # script_battle_tactic_apply_aux
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("orig_battle_tactic_apply_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (store_mission_timer_a, ":mission_time"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (copy_position, pos1, pos52),
        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no", 1),
        (assign, ":avg_dist", reg0),
        (assign, ":min_dist", reg1),
        (try_begin),
          (this_or_next|lt, ":min_dist", 1000),
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (try_begin),
          (ge, ":ai_leader", 0),
          (agent_is_alive, ":ai_leader"),
          (agent_set_speed_limit, ":ai_leader", 9),
          (call_script, "script_team_get_average_position_of_enemies", ":team_no"),
          (copy_position, pos60, pos0),
          (agent_get_position, pos61, ":ai_leader"),
          (position_transform_position_to_local, pos62, pos61, pos60), #pos62 = vector to enemy w.r.t leader
          (position_normalize_origin, ":distance_to_enemy", pos62),
          (convert_from_fixed_point, ":distance_to_enemy"),
          (assign, reg17, ":distance_to_enemy"),
          (position_get_x, ":dir_x", pos62),
          (position_get_y, ":dir_y", pos62),
          (val_mul, ":dir_x", 23),
          (val_mul, ":dir_y", 23), #move 23 meters
          (position_set_x, pos62, ":dir_x"),
          (position_set_y, pos62, ":dir_y"),

          (position_transform_position_to_parent, pos63, pos61, pos62), #pos63 is 23m away from leader in the direction of the enemy.
          (position_set_z_to_ground_level, pos63),

          (team_give_order, ":team_no", grc_everyone, mordr_hold),
          (team_set_order_position, ":team_no", grc_everyone, pos63),
          (agent_get_position, pos1, ":ai_leader"),
          (try_begin),
            (lt, ":distance_to_enemy", 50),
            (ge, ":mission_time", 30),
            (assign, ":battle_tactic", 0),
            (team_give_order, ":team_no", grc_everyone, mordr_charge),
            (agent_set_speed_limit, ":ai_leader", 60),
          (try_end),
        (else_try),
          (assign, ":battle_tactic", 0),
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (try_end),

      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),


##  # script_siege_defender_tactic_apply
  # Input: arg1 = players_side_damage, arg2 = enemy_side_damage, arg3 = continue_battle s5 = title_string
  # Output: none
  ("simulate_retreat",
    [
      (call_script, "script_music_set_situation_with_culture", mtf_sit_killed),
      (set_show_messages, 0),
      (store_script_param, ":players_side_damage", 1),
      (store_script_param, ":enemy_side_damage", 2),
      (store_script_param, ":continue_battle", 3),

      (assign, ":players_side_strength", 0),
      (assign, ":enemy_side_strength", 0),

      (assign, ":do_calculate", 1),
      (try_begin),
        (try_for_agents, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (agent_set_slot, ":cur_agent", slot_agent_is_alive_before_retreat, 1),#needed for simulation

          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
          (store_character_level, ":cur_level", ":cur_troop"),
          (val_add, ":cur_level", 5),
          (try_begin),
            (troop_is_hero, ":cur_troop"),
            (val_add, ":cur_level", 5),
          (try_end),
          (try_begin),
            (agent_is_ally, ":cur_agent"),
            (val_add, ":players_side_strength", ":cur_level"),
          (else_try),
            (val_add, ":enemy_side_strength", ":cur_level"),
          (try_end),
        (try_end),
        (eq, "$pin_player_fallen", 0),
        (lt, ":enemy_side_strength", ":players_side_strength"),
        (eq, ":continue_battle", 1),
        (assign, ":do_calculate", 0),
      (try_end),

      (try_begin),
        (eq, ":do_calculate", 1),

        (assign, "$g_last_mission_player_damage", 0),
        (party_clear, "p_temp_party"),
        (party_clear, "p_temp_party_2"),
        (call_script, "script_simulate_battle_with_agents_aux", 0, ":players_side_damage"),
        (call_script, "script_simulate_battle_with_agents_aux", 1, ":enemy_side_damage"),

        (assign, ":display_casualties", 0),

        (try_begin),
          (gt, "$g_last_mission_player_damage", 0),
          (assign, ":display_casualties", 1),
          (assign, reg1, "$g_last_mission_player_damage"),
          (str_store_string, s12, "str_casualty_display_hp"),
        (else_try),
          (str_clear, s12),
        (try_end),

        (call_script, "script_print_casualties_to_s0", "p_temp_party", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s10, s0),

        (call_script, "script_print_casualties_to_s0", "p_temp_party_2", 1),
        (try_begin),
          (party_get_num_companion_stacks, ":num_stacks", "p_temp_party_2"),
          (gt, ":num_stacks", 0),
          (assign, ":display_casualties", 1),
        (try_end),
        (str_store_string_reg, s11, s0),
        (try_begin),
          (eq, ":display_casualties", 1),
          (dialog_box,"str_casualty_display", s5),
        (try_end),
      (try_end),
      (set_show_messages, 1),

      #Calculating morale penalty (can be between 0-30)
      (assign, ":ally_casualties", 0),
      (assign, ":enemy_casualties", 0),
      (assign, ":total_allies", 0),

      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (val_add, ":total_allies", 1),
          (try_begin),
            (neg|agent_is_alive, ":cur_agent"),
            (val_add, ":ally_casualties", 1),
          (try_end),
        (else_try),
          (neg|agent_is_alive, ":cur_agent"),
          (val_add, ":enemy_casualties", 1),
        (try_end),
      (try_end),
      (store_add, ":total_casualties", ":ally_casualties", ":enemy_casualties"),
      (try_begin),
        (gt, ":total_casualties", 0),
        (store_mul, ":morale_adder", ":ally_casualties", 100),
        (val_div, ":morale_adder", ":total_casualties"),
        (val_mul, ":morale_adder", ":ally_casualties"),
        (val_div, ":morale_adder", ":total_allies"),
        (val_mul, ":morale_adder", -30),
        (val_div, ":morale_adder", 100),
        (call_script, "script_change_player_party_morale", ":morale_adder"),
      (try_end),
  ]),



  # script_simulate_battle_with_agents_aux
  # For internal use only
  # Input: arg1 = attacker_side (0 = ally, 1 = enemy), arg2 = damage amount
  # Output: none
  ("simulate_battle_with_agents_aux",
    [
      (store_script_param_1, ":attacker_side"),
      (store_script_param_2, ":damage"),

      (get_player_agent_no, ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (neq, ":player_agent", ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        #do not check agent_is_alive, check slot_agent_is_alive_before_retreat instead, so that dead agents can still hit enemies
        (agent_slot_eq, ":cur_agent", slot_agent_is_alive_before_retreat, 1),
        (try_begin),
          (agent_is_ally, ":cur_agent"),
          (assign, ":cur_agents_side", 0),
        (else_try),
          (assign, ":cur_agents_side", 1),
        (try_end),
        (eq, ":cur_agents_side", ":attacker_side"),
        (agent_get_position, pos2, ":cur_agent"),
        (assign, ":closest_agent", -1),
        (assign, ":min_distance", 100000),
        (try_for_agents, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (try_begin),
            (agent_is_ally, ":cur_agent_2"),
            (assign, ":cur_agents_side_2", 0),
          (else_try),
            (assign, ":cur_agents_side_2", 1),
          (try_end),
          (this_or_next|neq, ":cur_agent_2", ":player_agent"),
          (eq, "$pin_player_fallen", 0),
          (neq, ":attacker_side", ":cur_agents_side_2"),
          (agent_get_position, pos3, ":cur_agent_2"),
          (get_distance_between_positions, ":cur_distance", pos2, pos3),
          (lt, ":cur_distance", ":min_distance"),
          (assign, ":min_distance", ":cur_distance"),
          (assign, ":closest_agent", ":cur_agent_2"),
        (try_end),
        (ge, ":closest_agent", 0),
        #Fight
        (agent_get_class, ":agent_class", ":cur_agent"),
        (assign, ":agents_speed", 1),
        (assign, ":agents_additional_hit", 0),
        (try_begin),
          (eq, ":agent_class", grc_archers),
          (assign, ":agents_additional_hit", 2),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed", 2),
        (try_end),
        (agent_get_class, ":agent_class", ":closest_agent"),
        (assign, ":agents_speed_2", 1),
        (try_begin),
          (eq, ":agent_class", grc_cavalry),
          (assign, ":agents_speed_2", 2),
        (try_end),
        (assign, ":agents_hit", 18000),
        (val_add, ":min_distance", 3000),
        (val_div, ":agents_hit", ":min_distance"),
        (val_mul, ":agents_hit", 2),# max 10, min 2 hits within 150 meters

        (val_mul, ":agents_hit", ":agents_speed"),
        (val_div, ":agents_hit", ":agents_speed_2"),
        (val_add, ":agents_hit", ":agents_additional_hit"),

        (assign, ":cur_damage", ":damage"),
        (agent_get_troop_id, ":closest_troop", ":closest_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (store_character_level, ":closest_level", ":closest_troop"),
        (store_character_level, ":cur_level", ":cur_troop"),
        (store_sub, ":level_dif", ":cur_level", ":closest_level"),
        (val_div, ":level_dif", 5),
        (val_add, ":cur_damage", ":level_dif"),

        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (val_div, ":cur_damage", 2),
          (store_agent_hit_points, ":init_player_hit_points", ":player_agent", 1),
        (try_end),

        (try_for_range, ":unused", 0, ":agents_hit"),
          (store_random_in_range, ":random_damage", 0, 100),
          (lt, ":random_damage", ":cur_damage"),
          (agent_deliver_damage_to_agent, ":cur_agent", ":closest_agent"),
        (try_end),

        (try_begin),
          (eq, ":closest_agent", ":player_agent"),
          (store_agent_hit_points, ":final_player_hit_points", ":player_agent", 1),
          (store_sub, ":hit_points_difference", ":init_player_hit_points", ":final_player_hit_points"),
          (val_add, "$g_last_mission_player_damage", ":hit_points_difference"),
        (try_end),

        (neg|agent_is_alive, ":closest_agent"),
        (try_begin),
          (eq, ":attacker_side", 1),
          (party_add_members, "p_temp_party", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party", ":closest_troop", 1),
          (try_end),
        (else_try),
          (party_add_members, "p_temp_party_2", ":closest_troop", 1),
          (try_begin),
            (agent_is_wounded, ":closest_agent"),
            (party_wound_members, "p_temp_party_2", ":closest_troop", 1),
          (try_end),
        (try_end),
      (try_end),
  ]),


  # script_map_get_random_position_around_position_within_range
  # Input: arg1 = troop_no
  # Output: none
  ("encounter_calculate_fit",
    [
      #(assign, "$g_enemy_fit_for_battle_old",  "$g_enemy_fit_for_battle"),
      #(assign, "$g_friend_fit_for_battle_old", "$g_friend_fit_for_battle"),
      #(assign, "$g_main_party_fit_for_battle_old", "$g_main_party_fit_for_battle"),
      (call_script, "script_party_count_fit_for_battle", "p_main_party"),
      #(assign, "$g_main_party_fit_for_battle", reg(0)),
      (call_script, "script_collect_friendly_parties"),
      (call_script, "script_party_count_fit_for_battle", "p_collective_friends"),
      (assign, "$g_friend_fit_for_battle", reg(0)),

      (party_clear, "p_collective_ally"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_is_active, "$g_ally_party"),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),
        #(call_script, "script_party_count_fit_for_battle", "p_collective_ally"),
        #(val_add, "$g_friend_fit_for_battle", reg(0)),
        #SB : pre-process command structure here
        (party_get_num_attached_parties, ":attached", "$g_ally_party"),
        (troop_get_slot, ":limit", "$g_player_troop", slot_troop_renown),
        (val_sub, ":limit", dplmc_command_renown_limit),
        (game_get_reduce_campaign_ai, ":bonus"),
        (val_mul, ":bonus", "$player_right_to_rule"),
        (val_add, ":limit", ":bonus"),

        (assign, reg0, ":attached"),
        (val_add, ":attached", 1),
        (try_for_range, ":rank", 0, ":attached"),
          (party_get_attached_party_with_rank, ":party_no", "$g_ally_party", ":rank"),
          (try_begin),
            (eq, ":party_no", -1),
            (assign, ":party_no", "$g_ally_party"),
          (try_end),
          (assign, ":continue", -1),

          (store_faction_of_party, ":party_faction", ":party_no"),
          (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),

          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (assign, ":continue", 0),
          (else_try),
            (assign, ":continue", -1), #by default, not under command
          (try_end),

          (try_begin), #under command if marshal
            (eq, ":party_faction", "$players_kingdom"),
            (troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),

            (try_begin), #as marshal
               # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
               # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
               # (assign, ":continue", 0),
            # (else_try), #as ruler/pretender marshal
               # (faction_slot_eq, ":party_faction", slot_faction_state, sfs_active),
               (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":party_faction"),
               (ge, reg0, DPLMC_FACTION_STANDING_MARSHALL),
               # (this_or_next|faction_slot_eq, ":party_faction", slot_faction_marshall, "trp_player"),
               # (faction_slot_eq, ":party_faction", slot_faction_leader, "$g_player_troop"),
               (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", -1), #If still not satisfied, check other conditions
          (else_try), #or high enough renown
            (troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
            (troop_get_slot, ":renown", ":leader_troop_id", slot_troop_renown),
            (call_script, "script_troop_get_relation_with_troop", ":leader_troop_id", "$g_player_troop"),
            (val_sub, ":renown", reg0), #higher relation means less renown needed.
            (le, ":renown", ":limit"),
            (assign, ":continue", 0),
          (else_try), #straggler parties - patrols, caravans, etc.
            (neg|troop_slot_eq, ":leader_troop_id", slot_troop_occupation, slto_kingdom_hero),
            (assign, ":continue", 0),
          (try_end),
          (party_set_slot, ":party_no", slot_party_temp_slot_1, ":continue"),
          (try_begin),
            (ge, "$cheat_mode", 1),
            (assign, reg0, ":continue"),
            # (str_store_party_name, s0, ":party_no"),
            (str_store_party_name, s0, ":party_no"),
            (faction_get_color, ":color", ":party_faction"),
            (display_message, "@{s0} will {reg0?not :} be under your command", ":color"),
          (try_end),
        (try_end),
      (try_end),

      (party_clear, "p_collective_enemy"),
      (try_begin),
        (party_is_active, "$g_enemy_party"),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),
      (try_end),
      (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
      (assign, "$g_enemy_fit_for_battle", reg(0)),
      (assign, reg11, "$g_enemy_fit_for_battle"),
      (assign, reg10, "$g_friend_fit_for_battle"),
  ]),

  # script_encounter_init_variables
  # Input: arg1 = troop_no
  # Output: none
  ("encounter_init_variables",
    [
      (assign, "$capture_screen_shown", 0),
      (assign, "$loot_screen_shown", 0),
      (assign, "$thanked_by_ally_leader", 0),
      (assign, "$g_battle_result", 0),
      (assign, "$cant_leave_encounter", 0),
      (assign, "$cant_talk_to_enemy", 0),
      (assign, "$last_defeated_hero", 0),
      (assign, "$last_freed_hero", 0),

      (call_script, "script_encounter_calculate_fit"),
      (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
	  ##diplomacy start+
	  #If terrain advantage is enabled, use it to initialize the variables.
	  (assign, ":terrain_code", -1),
	  (try_begin),
	     (eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
		 (lt, "$g_encounter_is_in_village", 1),#Do not apply to village encounters
	     (try_begin),
	        (encountered_party_is_attacker),
		    (call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
	     (else_try),
	        (call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
		 (try_end),
		 (assign, ":terrain_code", reg0),
		 #calculate party strength with terrain
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_main_party", reg0),
		 (try_begin),
			#Print debug Message
		    (ge, "$cheat_mode", 1),
		    (assign, reg2, ":terrain_code"),
			(display_message, "@{!}DEBUG - Main party raw strength {reg1}, terrain code {reg2}, modified strength {reg0}"),
		 (try_end),
		 #calculate enemy strength with terrain
		 (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_enemy_party", reg0),
		 (assign, "$g_strength_contribution_of_player", 100),
		 (try_begin),
		    (ge, "$cheat_mode", 1),#debug
		    (assign, reg2, ":terrain_code"),
			(display_message, "@{!} DEBUG - Enemy party raw strength {reg1}, terrain code {reg2}, modified strength {reg0}"),
		 (try_end),
		 #calculate friends strength with terrain
		 (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
		 (call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_friends", ":terrain_code", 0, 1),
		 (assign, "$g_starting_strength_friends", reg0),
	  (else_try),
	     ##Calculate all party strengths without terrain:
	     #calculate main party strength
         (call_script, "script_party_calculate_strength", "p_main_party", 0),
         (assign, "$g_starting_strength_main_party", reg0),
		 #calculate enemy strength
         (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
         (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
         (assign, "$g_starting_strength_enemy_party", reg0),
         (assign, "$g_strength_contribution_of_player", 100),
		 #calculate friends strength
         (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
         (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
         (assign, "$g_starting_strength_friends", reg0),
	  (try_end),
	  ##diplomacy end+

      (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.

	  (try_begin),
		(gt, "$g_starting_strength_friends", 0), #this new to prevent occasional div by zero error
		(val_div, "$g_strength_contribution_of_player","$g_starting_strength_friends"),
	  (else_try),
		(assign, "$g_strength_contribution_of_player", 100), #Or zero, maybe
	  (try_end),

      (party_clear, "p_routed_enemies"), #new
      (assign, "$num_routed_us", 0),#newtoday
      (assign, "$num_routed_allies", 0),#newtoday
      (assign, "$num_routed_enemies", 0),#newtoday
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_main_party", ":i_stack"),
        (try_begin),
          (troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (party_get_num_companion_stacks, ":num_stacks", "p_collective_friends"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_collective_friends", ":i_stack"),
        (try_begin),
          #(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          (troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop_id", "p_collective_enemy", ":i_stack"),
        (try_begin),
          #(troop_set_slot, ":stack_troop_id", slot_troop_player_routed_agents, 0),
          (troop_set_slot, ":stack_troop_id", slot_troop_enemy_routed_agents, 0),
          #(troop_set_slot, ":stack_troop_id", slot_troop_ally_routed_agents, 0),
        (try_end),
      (try_end),

      (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_set_slot, ":cur_faction", slot_faction_num_routed_agents, 0),
      (try_end),

      (assign, "$routed_party_added", 0), #new
      (party_clear, "p_total_enemy_casualties"), #new

      ###(((add wounded troops of enemy to p_total_enemy_casualties
      (party_get_num_companion_stacks, ":num_stacks", "p_collective_enemy"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_wounded_size", "p_collective_enemy", ":stack_no"),
        (gt, ":stack_wounded_size", 0),
        (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
        (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
      (try_end),
      ###)))

#      (try_begin),
#        (gt, "$g_ally_party", 0),
#        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
#        (call_script, "script_party_calculate_strength", "p_collective_ally"),
#        (assign, "$g_starting_strength_ally_party", reg0),
#        (store_add, ":starting_strength_factor_combined","$g_starting_strength_ally_party","$g_starting_strength_main_party"),
#         (store_mul, "$g_strength_contribution_of_player","$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
#        (val_div, "$g_strength_contribution_of_player",":starting_strength_factor_combined"),
#      (try_end),
  ]),

  # script_calculate_renown_value
  # Input: none
  # Output: none
  ("custom_battle_end",
    [
      (assign, "$g_custom_battle_team1_death_count", 0),
      (assign, "$g_custom_battle_team2_death_count", 0),
      (get_player_agent_no, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),
      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (neg|agent_is_alive, ":cur_agent"),
        (agent_get_team, ":cur_team", ":cur_agent"),
        (try_begin),
          (eq, ":cur_team", ":player_team"),
          (val_add, "$g_custom_battle_team1_death_count", 1),
        (else_try),
          (val_add, "$g_custom_battle_team2_death_count", 1),
        (try_end),
      (try_end),
      ]),

  # script_remove_troop_from_prison
    #input: none, based on $g_talk_agent
    #output: none, agent wields first available weapon to show aggression
    ("encounter_agent_draw_weapon",
    [
        (store_conversation_agent, "$g_talk_agent"),
        (try_begin),
          (agent_get_item_slot, ":item_no", "$g_talk_agent", ek_item_0),
          (gt, ":item_no", 0),
          (agent_set_wielded_item, "$g_talk_agent", ":item_no"),
        (try_end),

    ]),

    #script_troop_debug_range
  # script_formation_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("formation_battle_tactic_init_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (team_get_leader, ":ai_leader", ":team_no"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (agent_get_position, pos1, ":ai_leader"),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30),
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (copy_position, pos1, pos52),
        (call_script, "script_find_high_ground_around_pos1", ":team_no", 30), # call again just in case we are not at peak point.
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos52),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
        (team_give_order, ":team_no", grc_archers, mordr_advance),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (ge, ":ai_leader", 0),
        (agent_set_speed_limit, ":ai_leader", 8),
        (agent_get_position, pos60, ":ai_leader"),
        (team_give_order, ":team_no", grc_everyone, mordr_hold),
        (team_set_order_position, ":team_no", grc_everyone, pos60),
      (try_end),
# formations additions
	  (call_script, "script_division_reset_places"),
	  (call_script, "script_get_default_formation", ":team_no"),
	  (assign, ":fformation", reg0),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_infantry, ":fformation"),
		(store_add, ":slot", slot_team_d0_formation, grc_infantry),
		(team_set_slot, ":team_no", ":slot", ":fformation"),
		(store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_infantry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_infantry),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_archers, formation_default),
		(store_add, ":slot", slot_team_d0_formation, grc_archers),
		(team_set_slot, ":team_no", ":slot", formation_default),
		(store_add, ":slot", slot_team_d0_formation_space, grc_archers),
		(team_set_slot, ":team_no", ":slot", 2),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_archers),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_archers),

	  (try_begin),
		(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_cavalry, formation_wedge),
		(store_add, ":slot", slot_team_d0_formation, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", formation_wedge),
		(store_add, ":slot", slot_team_d0_formation_space, grc_cavalry),
		(team_set_slot, ":team_no", ":slot", 0),
	  (else_try),
		(call_script, "script_formation_end", ":team_no", grc_cavalry),
	  (try_end),
	  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_cavalry),

	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
	  (team_give_order, ":team_no", grc_archers, mordr_spread_out),
# end formations additions
  ]),

  # script_formation_battle_tactic_apply_aux #CABA - OK; Need expansion when new AI divisions to work with
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("formation_battle_tactic_apply_aux",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":battle_tactic", 2),
      (store_mission_timer_a, ":mission_time"),
      (try_begin),
        (eq, ":battle_tactic", btactic_hold),
        (copy_position, pos1, pos52),
        (call_script, "script_get_closest3_distance_of_enemies_at_pos1", ":team_no", 1),
        (assign, ":avg_dist", reg0),
        (assign, ":min_dist", reg1),
        (try_begin),
          (this_or_next|lt, ":min_dist", 1000),
          (lt, ":avg_dist", 4000),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_infantry),	#formations
		  (call_script, "script_formation_end", ":team_no", grc_archers),	#formations
		  (call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (else_try),
        (eq, ":battle_tactic", btactic_follow_leader),
        (team_get_leader, ":ai_leader", ":team_no"),
        (try_begin),
          (agent_is_alive, ":ai_leader"),
          (agent_set_speed_limit, ":ai_leader", 9),
          (call_script, "script_team_get_average_position_of_enemies", ":team_no"),
          (copy_position, pos60, pos0),
          (ge, ":ai_leader", 0),
          (agent_get_position, pos61, ":ai_leader"),
          (position_transform_position_to_local, pos62, pos61, pos60), #pos62 = vector to enemy w.r.t leader
          (position_normalize_origin, ":distance_to_enemy", pos62),
          (convert_from_fixed_point, ":distance_to_enemy"),
          (assign, reg17, ":distance_to_enemy"),
          (position_get_x, ":dir_x", pos62),
          (position_get_y, ":dir_y", pos62),
          (val_mul, ":dir_x", 23),
          (val_mul, ":dir_y", 23), #move 23 meters
          (position_set_x, pos62, ":dir_x"),
          (position_set_y, pos62, ":dir_y"),

          (position_transform_position_to_parent, pos63, pos61, pos62), #pos63 is 23m away from leader in the direction of the enemy.
          (position_set_z_to_ground_level, pos63),

          (team_give_order, ":team_no", grc_everyone, mordr_hold),
          (team_set_order_position, ":team_no", grc_everyone, pos63),
#formations code
		  (call_script, "script_point_y_toward_position", pos63, pos60),
		  (agent_get_position, pos49, ":ai_leader"),
		  (agent_set_position, ":ai_leader", pos63),	#fake out script_battlegroup_place_around_leader
		  (call_script, "script_division_reset_places"),
		  (call_script, "script_get_default_formation", ":team_no"),
		  (assign, ":fformation", reg0),

		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_infantry, ":fformation"),
			(store_add, ":slot", slot_team_d0_formation, grc_infantry),
			(team_set_slot, ":team_no", ":slot", ":fformation"),
			(store_add, ":slot", slot_team_d0_formation_space, grc_infantry),
			(team_set_slot, ":team_no", ":slot", 0),
		  (else_try),
			(call_script, "script_formation_end", ":team_no", grc_infantry),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_infantry),

		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_archers, formation_default),
			(store_add, ":slot", slot_team_d0_formation, grc_archers),
			(team_set_slot, ":team_no", ":slot", formation_default),
			(store_add, ":slot", slot_team_d0_formation_space, grc_archers),
			(team_set_slot, ":team_no", ":slot", 2),
		  (else_try),
			(call_script, "script_formation_end", ":team_no", grc_archers),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_archers),

		  (try_begin),
			(call_script, "script_cf_battlegroup_valid_formation", ":team_no", grc_cavalry, formation_wedge),
			(store_add, ":slot", slot_team_d0_formation, grc_cavalry),
			(team_set_slot, ":team_no", ":slot", formation_wedge),
			(store_add, ":slot", slot_team_d0_formation_space, grc_cavalry),
			(team_set_slot, ":team_no", ":slot", 0),
		  (else_try),
			(call_script, "script_formation_end", ":team_no", grc_cavalry),
		  (try_end),
		  (call_script, "script_battlegroup_place_around_leader", ":team_no", grc_cavalry),

		  (agent_set_position, ":ai_leader", pos49),
#end formations code
          (agent_get_position, pos1, ":ai_leader"),
          (try_begin),
            (lt, ":distance_to_enemy", 50),
            (ge, ":mission_time", 30),
            (assign, ":battle_tactic", 0),
			(call_script, "script_formation_end", ":team_no", grc_infantry),	#formations
			(call_script, "script_formation_end", ":team_no", grc_archers),	#formations
			(call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations
            (team_give_order, ":team_no", grc_everyone, mordr_charge),
            (agent_set_speed_limit, ":ai_leader", 60),
          (try_end),
        (else_try),
          (assign, ":battle_tactic", 0),
		  (call_script, "script_formation_end", ":team_no", grc_infantry),	#formations
		  (call_script, "script_formation_end", ":team_no", grc_archers),	#formations
		  (call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations
          (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (try_end),
      (try_end),

      (try_begin), # charge everyone after a while
        (neq, ":battle_tactic", 0),
        (ge, ":mission_time", 300),
        (assign, ":battle_tactic", 0),
		(call_script, "script_formation_end", ":team_no", grc_infantry),	#formations
		(call_script, "script_formation_end", ":team_no", grc_archers),	#formations
		(call_script, "script_formation_end", ":team_no", grc_cavalry),	#formations
        (team_give_order, ":team_no", grc_everyone, mordr_charge),
        (team_get_leader, ":ai_leader", ":team_no"),
        (agent_set_speed_limit, ":ai_leader", 60),
      (try_end),
      (assign, reg0, ":battle_tactic"),
  ]),

  # Replacement script for battle_tactic_init_aux to switch between using
  # M&B Standard AI with changes for formations and original based on
  # NOTE: original script "battle_tactic_init_aux" should be renamed to "orig_battle_tactic_init_aux"
  # constant formation_native_ai_use_formation ( 0: original, 1: use formation )
  # script_battle_tactic_init_aux
  # Input: team_no, battle_tactic
  # Output: none
  ("battle_tactic_init_aux",
	[
	  (store_script_param, ":team_no", 1),
	  (store_script_param, ":battle_tactic", 2),
	  (try_begin),
		(eq, formation_native_ai_use_formation, 1),
		(call_script, "script_formation_battle_tactic_init_aux", ":team_no", ":battle_tactic"),
	  (else_try),
		(call_script, "script_orig_battle_tactic_init_aux", ":team_no", ":battle_tactic"),
	  (try_end),
	]),

  # Replacement script for battle_tactic_init_aux to switch between using
  # M&B Standard AI with changes for formations and original based on
  # NOTE: original script "battle_tactic_apply_aux" should be renamed to "orig_battle_tactic_apply_aux"
  # constant formation_native_ai_use_formation ( 0: original, 1: use formation )
  # script_battle_tactic_apply_aux
  # Input: team_no, battle_tactic
  # Output: battle_tactic
  ("battle_tactic_apply_aux",
	[
	  (store_script_param, ":team_no", 1),
	  (store_script_param, ":battle_tactic", 2),
	  (try_begin),
		(eq, formation_native_ai_use_formation, 1),
		(call_script, "script_formation_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
	  (else_try),
		(call_script, "script_orig_battle_tactic_apply_aux", ":team_no", ":battle_tactic"),
	  (try_end),
  ]),

  # # AI with Formations Scripts
]
