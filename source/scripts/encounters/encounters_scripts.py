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

("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
	  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":checked_troop_no"),
	  (lt, reg0, -10),
 ]),

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

("neutral_behavior_in_fight",
	[
      (get_player_agent_no, ":player_agent"),
      (agent_get_position, pos3, ":player_agent"),
      (agent_get_team, ":player_team", ":player_agent"),

      (try_begin),
        (gt, "$g_main_attacker_agent", 0),
        (agent_get_team, ":attacker_team_no", "$g_main_attacker_agent"),
        (agent_get_position, pos5, "$g_main_attacker_agent"),
      (else_try),
        (eq, ":attacker_team_no", -1),
        (agent_get_position, pos5, ":player_agent"),
      (try_end),

      (set_fixed_point_multiplier, 100),

      (try_for_agents, ":agent"),
        (agent_get_team, ":other_team", ":agent"),
        (neq, ":other_team", ":attacker_team_no"),
        (neq, ":other_team", ":player_team"),

        (agent_get_troop_id, ":troop_id", ":agent"),
        #SB : better range checks
        (this_or_next|eq, ":troop_id", "trp_farmer"), #farmers are "neutral"
        (neg|is_between, ":troop_id", soldiers_begin, soldiers_end), #but lie within this range
        (troop_slot_eq, ":troop_id", slot_troop_mission_participation, mp_unaware), #neutral prisoners?

        (agent_get_position, pos4, ":agent"),

        (assign, ":best_position_score", 0),
        (assign, ":best_position", -1),

        (try_begin),
          (neg|agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is running away
          (agent_get_slot, ":target_entry_point_plus_one",  ":agent", slot_agent_is_running_away),
          (store_sub, ":target_entry_point", ":target_entry_point_plus_one", 1),
          (entry_point_get_position, pos6, ":target_entry_point"),
          (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
          (lt, ":agent_distance_to_target", 100),
          (agent_set_slot, ":agent", slot_agent_is_running_away, 0),
        (try_end),

        (agent_slot_eq, ":agent", slot_agent_is_running_away, 0), #if agent is not already running away

        (try_begin), #stand in place
          (get_distance_between_positions, ":distance", pos4, pos5),
          (get_distance_between_positions, ":distance_to_player", pos4, pos3),

          (val_min, ":distance", ":distance_to_player"),

          (this_or_next|gt, ":distance", 700), #7 meters away from main belligerents
          (main_hero_fallen),

          (agent_set_scripted_destination, ":agent", pos4),
        (else_try), #get out of the way
          (try_for_range, ":target_entry_point", 0, 64),
            (neg|entry_point_is_auto_generated, ":target_entry_point"),
            (entry_point_get_position, pos6, ":target_entry_point"),
            (get_distance_between_positions, ":agent_distance_to_target", pos6, pos4),
            (get_distance_between_positions, ":player_distance_to_target", pos6, pos3),
            (store_sub, ":position_score", ":player_distance_to_target", ":agent_distance_to_target"),
            (ge, ":position_score", 0),
            (try_begin),
              (ge, ":agent_distance_to_target", 2000),
              (store_sub, ":extra_distance", ":agent_distance_to_target", 2000),
              (val_min, ":extra_distance", 1000),
              (val_min, ":agent_distance_to_target", 2000), #if more than 10 meters assume it is 10 meters far while calculating best run away target
              (val_sub, ":agent_distance_to_target", ":extra_distance"),
            (try_end),
            (val_mul, ":position_score", ":agent_distance_to_target"),
            (try_begin),
              (ge, ":position_score", ":best_position_score"),
              (assign, ":best_position_score", ":position_score"),
              (assign, ":best_position", ":target_entry_point"),
            (try_end),
          (try_end),

          (try_begin),
            (ge, ":best_position", 0),
            (entry_point_get_position, pos6, ":best_position"),
            (agent_set_speed_limit, ":agent", 10),
            (agent_set_scripted_destination, ":agent", pos6),
            (store_add, ":best_position_plus_one", ":best_position", 1),
            (agent_set_slot, ":agent", slot_agent_is_running_away, ":best_position_plus_one"),
          (try_end),
        (try_end),
	  (try_end),
	]),

("set_up_duel_with_troop", #now the setup is handled through the menu
	[
	  (store_script_param, "$g_duel_troop", 1),
      #SB : change by parameter instead of always one
	  (store_script_param, "$g_start_arena_fight_at_nearest_town", 2),
	  (store_faction_of_troop, ":troop_faction", "$g_duel_troop"),
	  (try_begin),
	    (eq, "$g_start_arena_fight_at_nearest_town", 1),
        # (assign, ":closest_town", -1),
        (assign, ":minimum_dist", 500),
        (try_for_range, ":cur_town", walled_centers_begin, walled_centers_end),
          (store_distance_to_party_from_party, ":dist", ":cur_town", "$g_encountered_party"),
          (lt, ":dist", ":minimum_dist"),
          #make sure it's at least neutral, so we don't fight in an enemy town's arena
          (store_faction_of_party, ":center_faction", ":cur_town"),
          (store_relation, ":relation", ":troop_faction", ":center_faction"),
          (ge, ":relation", 0),
          (assign, ":minimum_dist", ":dist"),
          (assign, "$g_start_arena_fight_at_nearest_town", ":cur_town"),
        (try_end),
	  (try_end),
	  (unlock_achievement, ACHIEVEMENT_PUGNACIOUS_D),
      (jump_to_menu, "mnu_arena_duel_fight"),
	  (finish_mission),

	]),

("setup_camera_keys", [

      # (assign, "$g_dplmc_cam_default", camera_keyboard),
      # (assign, "$g_camera_up", key_w),
      # (assign, "$g_camera_down", key_s),
      # (assign, "$g_camera_left", key_a),
      # (assign, "$g_camera_right", key_d),

      #default custom commander y/z offsets
      (call_script, "script_setup_camera_offset"),
      #these will be retained after being changed inside missions

      #deathcam
      (assign, "$g_cam_tilt_left", key_numpad_1),
      (assign, "$g_cam_tilt_right", key_numpad_3),

      (assign, "$g_camera_adjust_add", key_numpad_plus),
      (assign, "$g_camera_adjust_sub", key_numpad_minus),

      #normally numpad swaps equipment, but we're dead so w/e
      (assign, "$g_camera_rot_up", key_numpad_8),
      (assign, "$g_camera_rot_down", key_numpad_2),
      (assign, "$g_camera_rot_left", key_numpad_4),
      (assign, "$g_camera_rot_right", key_numpad_6),
    ]),

("setup_camera_offset",
      [
      (assign, "$g_camera_z", 200),
      (assign, "$g_camera_y", -175),
      (assign, "$g_camera_rotate_x", 0),
      (assign, "$g_camera_rotate_y", 0),
      (assign, "$g_camera_rotate_z", 0),

      ]),

("init_death_cam",
      [
        (assign, "$deathcam_mouse_last_x", 5000),
        (assign, "$deathcam_mouse_last_y", 3750),
        (assign, "$deathcam_mouse_last_notmoved_x", 5000),
        (assign, "$deathcam_mouse_last_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_x", 5000), #Center screen (10k fixed pos)
        (assign, "$deathcam_mouse_notmoved_y", 3750),
        (assign, "$deathcam_mouse_notmoved_counter", 0),

        (assign, "$deathcam_total_rotx", 0),

        (assign, "$deathcam_sensitivity_x", 200), #4:3 ratio may be best
        (assign, "$deathcam_sensitivity_y", 150), #If modified, change values in common_move_deathcam

        (assign, "$deathcam_prsnt_was_active", 0),

        (assign, "$deathcam_keyboard_rotation_x", 0),
        (assign, "$deathcam_keyboard_rotation_y", 0),

        (assign, "$g_dplmc_cam_activated", 0),
        (assign, "$dmod_current_agent", -1),
        # check if keys are not set/invalid
        (try_begin),
          (neg|is_between, "$g_dplmc_cam_default", camera_keyboard, camera_follow + 1),
          (call_script, "script_setup_camera_keys"),
          (assign, "$g_dplmc_cam_default", camera_keyboard),
        (try_end),

        (get_player_agent_no, "$g_player_agent"),
        (agent_get_team, "$g_player_team", "$g_player_agent"),
      ]),

("cf_cancel_camera_keys", [
      (this_or_next|game_key_is_down, gk_view_char),
      (this_or_next|game_key_is_down, gk_zoom),
      (game_key_is_down, gk_cam_toggle),
      (mission_cam_set_mode, 0),
    ]),

("dmod_closest_agent", [
          (assign, ":cur_agent", -1),
          (assign, ":distance", 999999),
          (mission_cam_get_position, pos11),
          (position_set_z_to_ground_level, pos11),
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            #position on the ground
            (agent_get_position, pos13, ":agent_no"),
            # (position_get_screen_projection, pos14, pos13),
            # (get_distance_between_positions, ":cur_distance", pos12, pos14),
            (get_distance_between_positions, ":cur_distance", pos11, pos13),
            (lt, ":cur_distance", ":distance"),
            (assign, ":distance", ":cur_distance"),
            (assign, ":cur_agent", ":agent_no"),
          (try_end),
          (try_begin),
            (neq, ":cur_agent", 1),
            (assign, "$dmod_current_agent", ":cur_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
          (try_end),

      ]
    ),

("dmod_cycle_forwards",[

         (assign, ":agent_moved", 0),
         (assign, ":first_agent", -1),
         # (get_player_agent_no, ":player_agent"),
         # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_moved", 1),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
            # (agent_get_team, ":cur_team", ":agent_no"),
            # (this_or_next|eq, ":cur_team", 5), #bodyguards
            # (eq, ":cur_team", ":player_team"),
            (try_begin),
              (lt, ":first_agent", 0),
              (assign, ":first_agent", ":agent_no"),
            (try_end),
            (gt, ":agent_no", "$dmod_current_agent"),
            (assign, "$dmod_current_agent", ":agent_no"),
            (assign, ":agent_moved", 1),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 0),
            (neq, ":first_agent", -1),
            (assign, "$dmod_current_agent", ":first_agent"),
            (assign, ":agent_moved", 1),
        (else_try),
            (eq, ":agent_moved", 0),
            (eq, ":first_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (eq, ":agent_moved", 1),
            (str_store_agent_name, s1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      #(assign, "$dmod_move_camera", 1),
      ]),

("dmod_cycle_backwards",[

        (assign, ":new_agent", -1),
        (assign, ":last_agent", -1),
        # (get_player_agent_no, ":player_agent"),
        # (agent_get_team, ":player_team", ":player_agent"),

        (try_for_agents, ":agent_no"),
            (neq, ":agent_no", "$g_player_agent"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_ally, ":agent_no"),
        # (agent_get_team, ":cur_team", ":agent_no"),
        # (this_or_next|eq, ":cur_team", 5), #bodyguards
        # (eq, ":cur_team", ":player_team"),
            (assign, ":last_agent", ":agent_no"),
            (lt, ":agent_no", "$dmod_current_agent"),
            (assign, ":new_agent", ":agent_no"),
        (try_end),

        (try_begin),
            (eq, ":new_agent", -1),
            (neq, ":last_agent", -1),
            (assign, ":new_agent", ":last_agent"),
        (else_try),
            (eq, ":new_agent", -1),
            (eq, ":last_agent", -1),
            (display_message, "@No Troops Left."),
        (try_end),

        (try_begin),
            (neq, ":new_agent", -1),
            (assign, "$dmod_current_agent", ":new_agent"),
            (str_store_agent_name, 1, "$dmod_current_agent"),
            (display_message, "@Selected Troop: {s1}"),
        (try_end),
      ]),

("game_missile_dives_into_water", [
	# (store_script_param, ":launcher_item_modifier", 4),
	# (store_script_param, ":shooter_agent_no", 5),
	# (store_script_param, ":missile_no", 6),

    (play_sound_at_position, "snd_jump_end_water", pos1),
    (particle_system_burst, "psys_game_water_splash_2", pos1, 40),

]),

("all_enemies_routed", [
  (assign, ":enemies_remaining", 0),
  (try_for_agents, ":agent"),
    (neg|agent_is_ally, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_slot, ":routing", ":agent", slot_agent_is_running_away),
    (eq, ":routing", 0),
    (val_add, ":enemies_remaining", 1),
  (try_end),
  (assign, reg10, ":enemies_remaining"),
]),

("cf_calculate_battle_ratio",
		[
			#bugfix; prevents earlier scripts from enforcing
			#fixed_point_* operations
			#(set_fixed_point_multiplier, 1),

			(assign, "$battle_ratio", 0),

			(assign, "$j_num_us_ready", 0),
			(assign, "$j_num_us_wounded", 0),
			(assign, "$j_num_us_routed", 0),
			(assign, "$j_num_us_dead", 0),

			(assign, "$j_num_allies_ready", 0),
			(assign, "$j_num_allies_wounded", 0),
			(assign, "$j_num_allies_routed", 0),
			(assign, "$j_num_allies_dead", 0),

			(assign, "$j_num_enemies_ready", 0),
			(assign, "$j_num_enemies_wounded", 0),
			(assign, "$j_num_enemies_routed", 0),
			(assign, "$j_num_enemies_dead", 0),

			#count and categorize agents (me, ally, enemy/wounded, dead, routed, alive)
			(try_for_agents, ":cur_agent"),
			  (agent_is_human, ":cur_agent"),
			  (agent_get_party_id, ":agent_party", ":cur_agent"),
			  (try_begin),
				(eq, ":agent_party", "p_main_party"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_us_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_us_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_us_routed", 1),
				(else_try),
				  (val_add, "$j_num_us_dead", 1),
				(try_end),
			  (else_try),
				(agent_is_ally, ":cur_agent"),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_allies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_allies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_allies_routed", 1),
				(else_try),
				  (val_add, "$j_num_allies_dead", 1),
				(try_end),
			  (else_try),
				(try_begin),
				  (agent_is_alive, ":cur_agent"),
				  (val_add, "$j_num_enemies_ready", 1),
				(else_try),
				  (agent_is_wounded, ":cur_agent"),
				  (val_add, "$j_num_enemies_wounded", 1),
				(else_try),
				  (agent_is_routed, ":cur_agent"),
				  (val_add, "$j_num_enemies_routed", 1),
				(else_try),
				  (val_add, "$j_num_enemies_dead", 1),
				(try_end),
			  (try_end),
			(try_end),

			#don't think I need these
			# (assign, ":ratio", 0),
			# (assign, ":ratio_3", 0),
			# (assign, ":difference", 0),
			# (assign, ":enemy_sqrt", 0),
			# (assign, ":ally_sqrt", 0),

			# ALLY STRENGTH
			(assign, ":ally_strength", 1),
			(val_add, ":ally_strength", "$j_num_enemies_routed"),
			(val_add, ":ally_strength", "$j_num_enemies_dead"),
			(val_add, ":ally_strength", "$j_num_enemies_wounded"),
			#ready is counted three times
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_us_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),
			(val_add, ":ally_strength", "$j_num_allies_ready"),

			# ENEMY STRENGTH
			(assign, ":enemy_strength", 1),
			(val_add, ":enemy_strength", "$j_num_us_dead"),
			(val_add, ":enemy_strength", "$j_num_us_wounded"),
			(val_add, ":enemy_strength", "$j_num_us_routed"),
			(val_add, ":enemy_strength", "$j_num_allies_dead"),
			(val_add, ":enemy_strength", "$j_num_allies_wounded"),
			(val_add, ":enemy_strength", "$j_num_allies_routed"),
			#ready is counted three times
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),
			(val_add, ":enemy_strength", "$j_num_enemies_ready"),

			#(A*10/E)
			#10/1 ratio = 10,000 morale penalty
			(store_mul, ":enemy_value", ":enemy_strength", battle_ratio_multiple),
			(val_div, ":enemy_value", ":ally_strength"),

			#(E*10/A)
			(store_mul, ":ally_value", ":ally_strength", battle_ratio_multiple),
			(val_div, ":ally_value", ":enemy_strength"),

			#if enemy value is greater, use negative of that.
			(try_begin),
				(gt, ":enemy_value", ":ally_value"),
				(val_sub, ":enemy_value", battle_ratio_multiple),
				(store_sub, ":enemy_value", 0, ":enemy_value"),
				(assign, "$battle_ratio", ":enemy_value"),
			(else_try),
				(val_sub, ":ally_value", battle_ratio_multiple),
				(assign, "$battle_ratio", ":ally_value"),
			(try_end),

			#(val_clamp, "$battle_ratio", -max_ratio, max_ratio),

			# (assign, reg2, ":enemy_value"),
			# (assign, reg1, ":ally_value"),

			#(assign, reg0, "$battle_ratio"),
			#(display_message, "@Battle Ratio:{reg0}"),


			#(sqrt A - sqrt E)^3 + (A-E) (unused)

				#(sqrt A - sqrt E)^3
				# (store_sqrt, ":enemy_sqrt", ":enemy_strength"),
				# (store_sqrt, ":ally_sqrt", ":ally_strength"),
				# (store_sub, ":ratio", ":ally_sqrt", ":enemy_sqrt"),
				# #I get the feeling store_pow doesn't work or is deprecated in some way; keep getting weird results
				# #perhaps use cumbersome approach instead:
				# (store_pow, ":ratio_3", ":ratio", 3),
				# # (store_mul, ":ratio_3", ":ratio", ":ratio"), #squared
				# # (val_mul, ":ratio_3", ":ratio"), #cubed

				# #(A-E)
				# (store_sub, ":difference", ":ally_strength", ":enemy_strength"),

			# (store_add, "$battle_ratio", ":difference", ":ratio_3"),
			# (val_mul, "$battle_ratio", 10),
			# (val_mul, "$battle_ratio", 10),

		#housekeeping BEGIN
			# (assign, reg2, "$battle_ratio"),
			# (assign, reg3, ":ally_strength"),
			# (assign, reg4, ":enemy_strength"),
			# (display_message, "@{reg3}/{reg4}={reg2}"),

			#find average morale for each side
			# (assign, ":enemy_morale", 1),
			# (assign, ":ally_morale", 1),
			# (assign, ":ally_amount", 1),

			#store morale for all troops
			# (try_for_agents,":cur_agent"),
				# (agent_is_human, ":cur_agent"),
				# (agent_is_alive, ":cur_agent"),
				# (agent_get_slot, ":agent_courage_score", ":cur_agent", slot_agent_courage_score),
				# (try_begin),
					# (agent_is_ally, ":cur_agent"),
					# (val_add, ":ally_morale", ":agent_courage_score"),
				# (else_try),
					# (val_add, ":enemy_morale", ":agent_courage_score"),
				# (try_end),
			# (try_end),

			# (store_add, ":ally_amount", "$j_num_us_ready", "$j_num_allies_ready"),

			# (store_div, reg6, ":ally_morale", ":ally_amount"),
			# (store_div, reg7, ":enemy_morale", "$j_num_enemies_ready"),
			# (display_message, "@Morale: {reg6}/{reg7}"),

			#check that fixed_point_whatever or something else isn't screwing me over
			#answer: it is, and tends to fluctuate
			# (store_sqrt, ":four", 16),
			# (assign, reg5, ":four"),
			# (display_message, "@the square root of sixteen is {reg5}"),
		#housekeeping END

			#100-10	= ~400
			#100-30	= ~150
			#100-50	= ~75

			#50-10	= ~100
			#50-30	= ~25
			#50-40	= ~10
		]
	),

("cf_agent_can_rout", [
	(store_script_param, ":agent", 1),

	(try_begin),
		(agent_is_ally, ":agent"),
		#count ready allies
		(assign, ":ready", "$j_num_us_ready"),
		(val_add, ":ready", "$j_num_allies_ready"),

		#count deady allies
		(store_add, ":deady", "$j_num_us_wounded", "$j_num_us_routed"),
		(val_add, ":deady", "$j_num_us_dead"),
		(val_add, ":deady", "$j_num_allies_wounded"),
		(val_add, ":deady", "$j_num_allies_routed"),
		(val_add, ":deady", "$j_num_allies_dead"),
		(val_mul, ":deady", 10),
	(else_try),
		#count ready enemies
		(assign, ":ready", "$j_num_enemies_ready"),

		#count deady enemies
		(store_add, ":deady", "$j_num_enemies_wounded", "$j_num_enemies_routed"),
		(val_add, ":deady", "$j_num_enemies_dead"),
		(val_mul, ":deady", 10),
	(try_end),
	# (display_message, "@agents cannot rout"),
	(gt, ":deady", ":ready"),
	# (display_message, "@agents can rout"),
]),

("setup_camp_scene",
    [
      (party_get_current_terrain, ":terrain_type", "p_main_party"),
      (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (try_begin),
        (this_or_next|eq, ":terrain_type", rt_steppe),
        (eq, ":terrain_type", rt_steppe_forest),
        (assign, ":scene_to_use", "scn_camp_scene_steppe"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_plain),
        (eq, ":terrain_type", rt_forest),
        (assign, ":scene_to_use", "scn_camp_scene_plain"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_snow),
        (eq, ":terrain_type", rt_snow_forest),
        (assign, ":scene_to_use", "scn_camp_scene_snow"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_desert),
        (eq, ":terrain_type", rt_desert_forest),
        (assign, ":scene_to_use", "scn_camp_scene_desert"),
      (else_try),
        (this_or_next|eq, ":terrain_type", rt_river),
        (eq, ":terrain_type", rt_water), #figure this out later
        (assign, ":scene_to_use", "scn_sea_1"),

        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (eq, ":ship_type", 1),
          (assign, ":scene_to_use", "scn_sea_1"),
        (else_try),
          (eq, ":ship_type", 2),
          (assign, ":scene_to_use", "scn_sea_2"),
        (else_try),
          (eq, ":ship_type", 3),
          (assign, ":scene_to_use", "scn_sea_3"),
        (else_try),
          (eq, ":ship_type", 4),
          (assign, ":scene_to_use", "scn_sea_4"),
        (try_end),

       (try_for_range, ":entry_no", 33, 40),
         (mission_tpl_entry_set_override_flags, "mt_camp", ":entry_no", af_override_horse),
       (try_end),

      (else_try),
        (eq, ":terrain_type", rt_bridge),
		(try_for_parties, ":party_no"),
			(is_between, ":party_no", "p_bridge_1", "p_looter_spawn_point"),
			(store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
			(lt, ":distance", 2),
			(party_get_icon, ":icon", ":party_no"),
			(try_begin),
				(eq, ":icon", "icon_bridge_snow_a"),
				(assign, ":scene_to_use", "scn_camp_scene_snow"),
			(else_try),
				(assign, ":scene_to_use", "scn_camp_scene_plain"),
			(try_end),
		(try_end),
      (try_end),
	  (modify_visitors_at_site, ":scene_to_use"),
	  (reset_visitors),
	# (set_visitor,1,"trp_follower_woman"),

	(assign, ":cur_entry", 2),

    (assign, ":entry_1_assigned", 0),

    (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),

   (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":num_stacks"), #1st pass: grab all heroes
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
         (eq, ":cur_troop_id", ":spouse"),
		 (set_visitor, 1, ":cur_troop_id"), #is spouse
         (assign, ":entry_1_assigned", 1),
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (val_add, ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (try_for_range, ":troop_iterator", 0, ":num_stacks"),
	 (party_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 40),
		(assign, ":num_stacks", -1), #break the loop
	 (else_try),
		 (party_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (party_stack_get_num_wounded, ":num_wounded","p_main_party",":troop_iterator"),
		 (val_sub, ":stack_size", ":num_wounded"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 40),
				(assign, ":stack_size", -1), #break the loop
             (else_try),
                 (neq, ":entry_1_assigned", 1),
                 (this_or_next|eq, ":cur_troop_id", "trp_prostitute"),
                 (eq, ":cur_troop_id", "trp_courtesan"),
                 (set_visitor, 1, ":cur_troop_id"),
                 (assign, ":entry_1_assigned", 1),
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	#prisoners
	(assign, ":cur_entry", 40),
	(party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
    (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"), #1st pass: grab all heroes
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (troop_is_hero, ":cur_troop_id"),
	 (neq, ":cur_troop_id", "trp_player"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":prisoner_stacks"), #break the loop
	 (else_try),
		 (set_visitor, ":cur_entry", ":cur_troop_id"),
		 (store_add, ":cur_entry", ":cur_entry", 1),
	 (try_end),
   (try_end),

   #2nd pass: get anyone else
   (party_get_num_prisoner_stacks, ":prisoner_stacks","p_main_party"),
   (try_for_range, ":troop_iterator", 0, ":prisoner_stacks"),
	 (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":troop_iterator"),
	 (neg|troop_is_hero, ":cur_troop_id"),
	 (try_begin),
		(ge, ":cur_entry", 48),
		(assign, ":troop_iterator", ":num_stacks"), #break the loop
	 (else_try),
		 (party_prisoner_stack_get_size, ":stack_size","p_main_party",":troop_iterator"),
		 (gt, ":stack_size", 0),
		 (try_for_range, ":stack_iterator", 0, ":stack_size"), #nested loop ayy lmao
			 (try_begin),
				(ge, ":cur_entry", 48),
				(assign, ":stack_size", -1), #break the loop
			 (else_try),
				 (store_random_in_range,":troop_dna",0,1000),
				 (set_visitor, ":cur_entry", ":cur_troop_id", ":troop_dna"),
                 (troop_set_slot, "trp_temp_array_c", ":cur_entry", ":troop_dna"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
		 (try_end),
	  (try_end),
   (try_end),

	(mission_tpl_entry_clear_override_items,"mt_camp",1),
	(store_random_in_range,":r",0,2),
	(try_begin),
		(eq,":r",0),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lute"),
	(else_try),
		(mission_tpl_entry_add_override_item,"mt_camp",1,"itm_lyre"),
	(try_end),

	  (assign, "$talk_context", tc_camp_talk),
      (jump_to_scene,":scene_to_use"),
  ]),

("cf_count_casualties", [
      (assign, ":num_casualties", 0),
      (try_for_agents,":cur_agent"),
        (try_begin),
          (this_or_next | agent_is_wounded, ":cur_agent"),
          (this_or_next | agent_slot_eq, ":cur_agent", slot_agent_is_running_away, 1),
          (neg | agent_is_alive, ":cur_agent"),
          (val_add, ":num_casualties", 1),
        (try_end),
      (try_end),
      (assign, reg0, ":num_casualties"),
      (gt, ":num_casualties", 0)]),

("cf_any_fighting", [
      (assign, ":any_fighting", 0),
      (try_for_range, ":team", 0, 4),
        (team_slot_ge, ":team", slot_team_size, 1),
        (eq, ":any_fighting", 0),
        (assign, ":num_divs", 9),
        (try_for_range, ":division", 0, ":num_divs"),
          (store_add, ":slot", slot_team_d0_is_fighting, ":division"),
          (team_slot_ge, ":team", ":slot", 1),
          (assign, ":any_fighting", 1),
          (assign, ":num_divs", 0),
        (try_end),
      (try_end),

      #lag this check to be sure
      (store_mission_timer_c, ":time_stamp"),
      (try_begin),	#time lag
        (gt, ":any_fighting", 0),
        (assign, "$teams_last_fighting", ":time_stamp"),
      (try_end),
      (assign, ":fighting_finished", formation_reform_interval),
      (val_max, ":fighting_finished", 5),
      (val_add, ":fighting_finished", "$teams_last_fighting"),
      (gt, ":fighting_finished", ":time_stamp"),]),
]
