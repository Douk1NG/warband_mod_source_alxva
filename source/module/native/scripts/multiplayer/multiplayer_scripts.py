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
# MULTIPLAYER SCRIPTS
# 
# This file contains all the scripts used exclusively in multiplayer game modes. 
# It handles server options, agent spawning, team balance, scoring, item purchasing/availability, 
# network message syncing, and multiplayer-specific mechanics like duels and bot management.
####################################################################################################################

multiplayer_scripts = [
  # This script is called from the game engine when a multiplayer map is ended in clients (not in server).
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_set_multiplayer_mission_end",
    [
      (assign, "$g_multiplayer_mission_end_screen", 1),
  ]),
  #script_game_enable_cheat_menu
  # INPUT: arg1 = agent_no
  # OUTPUT: none
  ("multiplayer_server_on_agent_spawn_common",
   [
     (store_script_param, ":agent_no", 1),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, -1),
     (try_begin),
       (agent_is_non_player, ":agent_no"),
       (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
     (try_end),
     ]),

  #script_multiplayer_server_player_joined_common
  # INPUT: arg1 = player_no
  # OUTPUT: none
  ("multiplayer_server_player_joined_common",
   [
     (store_script_param, ":player_no", 1),
     (try_begin),
       (this_or_next|player_is_active, ":player_no"),
       (eq, ":player_no", 0),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (store_mission_timer_a, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_join_time, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1),
       #fight and destroy only
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_1, 0),
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_2, 0),
       #fight and destroy only end
       (try_begin),
         (multiplayer_is_server),
         (assign, ":initial_gold", multi_initial_gold_value),
         (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
         (val_div, ":initial_gold", 100),
         (player_set_gold, ":player_no", ":initial_gold"),
         (call_script, "script_multiplayer_send_initial_information", ":player_no"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_server_before_mission_start_common
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_server_before_mission_start_common",
   [
     (try_begin),
       (scene_allows_mounted_units),
       (assign, "$g_horses_are_avaliable", 1),
     (else_try),
       (assign, "$g_horses_are_avaliable", 0),
     (try_end),
     (scene_set_day_time, 15),
     (assign, "$g_multiplayer_mission_end_screen", 0),

     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (assign, ":initial_gold", multi_initial_gold_value),
       (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
       (val_div, ":initial_gold", 100),
       (player_set_gold, ":player_no", ":initial_gold"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1), #not required in siege, bt, fd
     (try_end),
     ]),

  #script_multiplayer_server_on_agent_killed_or_wounded_common
  # INPUT: arg1 = dead_agent_no, arg2 = killer_agent_no
  # OUTPUT: none
  ("multiplayer_server_on_agent_killed_or_wounded_common",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),

     (call_script, "script_multiplayer_event_agent_killed_or_wounded", ":dead_agent_no", ":killer_agent_no"),
     #adding 1 score points to agent which kills enemy agent at server
     (try_begin),
       (multiplayer_is_server),
       (try_begin), #killing myself because of some reason (friend hit, fall, team change)
         (lt, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (neg|agent_is_non_player, ":dead_agent_no"),
         (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
         (player_is_active, ":dead_agent_player_id"),
         (player_get_score, ":dead_agent_player_score", ":dead_agent_player_id"),
         (val_add, ":dead_agent_player_score", -1),
         (player_set_score, ":dead_agent_player_id", ":dead_agent_player_score"),
       (else_try), #killing teammate
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_get_team, ":killer_team_no", ":killer_agent_no"),
         (agent_get_team, ":dead_team_no", ":dead_agent_no"),
         (eq, ":killer_team_no", ":dead_team_no"),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (val_add, ":killer_agent_player_score", -1),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
         #(player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player_id"),
         #(val_add, ":killer_agent_player_kill_count", -2),
         #(player_set_kill_count, ":killer_agent_player_id", ":killer_agent_player_kill_count"),
       (else_try), #killing enemy
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_human, ":killer_agent_no"),
         (try_begin),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (try_begin),
             (eq, "$g_battle_death_mode_started", 1),
             (neq, ":dead_agent_no", ":killer_agent_no"),
             (call_script, "script_calculate_new_death_waiting_time_at_death_mod"),
           (try_end),
         (try_end),
         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
           (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
           (try_begin),
             (ge, ":dead_player_no", 0),
             (player_is_active, ":dead_player_no"),
             (neg|agent_is_non_player, ":dead_agent_no"),
             (try_for_agents, ":cur_agent"),
               (agent_is_non_player, ":cur_agent"),
               (agent_is_human, ":cur_agent"),
               (agent_is_alive, ":cur_agent"),
               (agent_get_group, ":agent_group", ":cur_agent"),
               (try_begin),
                 (eq, ":dead_player_no", ":agent_group"),
                 (agent_set_group, ":cur_agent", -1),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
         (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
         (try_begin),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (val_add, ":killer_agent_player_score", 1),
         (else_try),
           (val_add, ":killer_agent_player_score", -1),
         (try_end),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
       (try_end),
     (try_end),

     (call_script, "script_add_kill_death_counts", ":killer_agent_no", ":dead_agent_no"),
     #money management
     (call_script, "script_money_management_after_agent_death", ":killer_agent_no", ":dead_agent_no"),
     ]),

  #script_multiplayer_close_gate_if_it_is_open
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_close_gate_if_it_is_open",
   [
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_winch_b"),
     (try_for_range, ":cur_prop_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":prop_instance_id", "spr_winch_b", ":cur_prop_instance"),
       (scene_prop_slot_eq, ":prop_instance_id", scene_prop_open_or_close_slot, 1),
       (scene_prop_get_instance, ":effected_object_instance_id", "spr_portcullis", ":cur_prop_instance"),
       (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
       (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
     (try_end),
   ]),

  #script_multiplayer_move_moveable_objects_initial_positions
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_move_moveable_objects_initial_positions",
   [
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_6m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_8m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_10m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_12m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_14m"),
   ]),

  #script_move_belfries_to_their_first_entry_point
  # INPUT: arg1 = multiplayer_message_type
  # OUTPUT: none
  ("show_multiplayer_message",
   [
    (store_script_param, ":multiplayer_message_type", 1),
    (store_script_param, ":value", 2),

    (assign, "$g_multiplayer_message_type", ":multiplayer_message_type"),

    (try_begin),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),

      (try_begin), #end of round in clients
        (neg|multiplayer_is_server),
        (assign, "$g_battle_death_mode_started", 0),
      (try_end),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_done),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_2"),
      (assign, "$g_team_balance_next_round", 0),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
      (assign, "$g_team_balance_next_round", 1),
      (call_script, "script_warn_player_about_auto_team_balance"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_no_need),
      (assign, "$g_team_balance_next_round", 0),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_score),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_returned_home),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_stole),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_poll_result),
      (assign, "$g_multiplayer_message_value_3", ":value"),
      (start_presentation, "prsnt_multiplayer_message_3"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_neutralized),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_captured),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_is_pulling),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_target_destroyed),

      (try_begin), #destroy score (condition : a target destroyed)
        (eq, "$g_defender_team", 0),
        (assign, ":attacker_team_no", 1),
      (else_try),
        (assign, ":attacker_team_no", 0),
      (try_end),

      (team_get_score, ":team_score", ":attacker_team_no"),
      (val_add, ":team_score", 1),
      (call_script, "script_team_set_score", ":attacker_team_no", ":team_score"), #destroy score end

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_defenders_saved_n_targets),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_attackers_won_the_round),
      (try_begin),
        (eq, "$g_defender_team", 0),
        (assign, "$g_multiplayer_message_value_1", 1),
      (else_try),
        (assign, "$g_multiplayer_message_value_1", 0),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    ]),

  #script_get_headquarters_scores
  # Input: none
  # Output: none (can fail)
  ("cf_multiplayer_evaluate_poll",
   [
     (assign, ":result", 0),
     (assign, "$g_multiplayer_poll_ended", 1),
     (store_add, ":total_votes", "$g_multiplayer_poll_yes_count", "$g_multiplayer_poll_no_count"),
     (store_sub, ":abstain_votes", "$g_multiplayer_poll_num_sent", ":total_votes"),
     (store_mul, ":nos_from_abstains", 3, ":abstain_votes"),
     (val_div, ":nos_from_abstains", 10), #30% of abstains are counted as no
     (val_add, ":total_votes", ":nos_from_abstains"),
     (val_max, ":total_votes", 1), #if someone votes and only 1-3 abstain occurs?
     (store_mul, ":vote_ratio", 100, "$g_multiplayer_poll_yes_count"),
     (val_div, ":vote_ratio", ":total_votes"),
     (try_begin),
       (ge, ":vote_ratio", "$g_multiplayer_valid_vote_ratio"),
       (assign, ":result", 1),
       (try_begin),
         (eq, "$g_multiplayer_poll_to_show", 1), #kick player
         (try_begin),
           (player_is_active, "$g_multiplayer_poll_value_to_show"),
           (kick_player, "$g_multiplayer_poll_value_to_show"),
         (try_end),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 2), #ban player
         (ban_player_using_saved_ban_info), #already loaded at the beginning of the poll
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
         (team_set_faction, 0, "$g_multiplayer_poll_value_2_to_show"),
         (team_set_faction, 1, "$g_multiplayer_poll_value_3_to_show"),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 4), #change number of bots
         (assign, "$g_multiplayer_num_bots_team_1", "$g_multiplayer_poll_value_to_show"),
         (assign, "$g_multiplayer_num_bots_team_2", "$g_multiplayer_poll_value_2_to_show"),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
         (try_end),
       (try_end),
     (else_try),
       (assign, "$g_multiplayer_poll_running", 0), #end immediately if poll fails. but end after some time if poll succeeds (apply the results first)
     (try_end),
     (get_max_players, ":num_players"),
     #for only server itself-----------------------------------------------------------------------------------------------
     (call_script, "script_show_multiplayer_message", multiplayer_message_type_poll_result, ":result"), #0 is useless here
     #for only server itself-----------------------------------------------------------------------------------------------
     (try_for_range, ":cur_player", 1, ":num_players"),
       (player_is_active, ":cur_player"),
       (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_show_multiplayer_message, multiplayer_message_type_poll_result, ":result"),
     (try_end),
     (eq, ":result", 1),
     ]),

  # script_multiplayer_accept_duel
  # Input: arg1 = agent_no, arg2 = agent_no_offerer
  # Output: none
  ("multiplayer_accept_duel",
   [
     (store_script_param, ":agent_no", 1),
     (store_script_param, ":agent_no_offerer", 2),
     (try_begin),
       (agent_slot_ge, ":agent_no", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (agent_get_player_id, ":player_no", ":ex_duelist"),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (try_begin),
       (agent_slot_ge, ":agent_no_offerer", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no_offerer", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no_offerer"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, ":agent_no_offerer"),
     (agent_set_slot, ":agent_no_offerer", slot_agent_in_duel_with, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no_offerer"),
##     (agent_add_relation_with_agent, ":agent_no", ":agent_no_offerer", -1),
##     (agent_add_relation_with_agent, ":agent_no_offerer", ":agent_no", -1),
     (agent_get_player_id, ":player_no", ":agent_no"),
     (store_mission_timer_a, ":mission_timer"),
     (try_begin),
       (player_is_active, ":player_no"), #might be AI
       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_start_duel, ":agent_no_offerer"),
     (else_try),
       (agent_force_rethink, ":agent_no"),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_duel_start_time, ":mission_timer"),
     (agent_get_player_id, ":agent_no_offerer_player", ":agent_no_offerer"),
     (try_begin),
       (player_is_active, ":agent_no_offerer_player"), #might be AI
       (multiplayer_send_int_to_player, ":agent_no_offerer_player", multiplayer_event_start_duel, ":agent_no"),
     (else_try),
       (agent_force_rethink, ":agent_no_offerer"),
     (try_end),
     (agent_set_slot, ":agent_no_offerer", slot_agent_duel_start_time, ":mission_timer"),
     ]),

  # script_game_get_multiplayer_server_option_for_mission_template
  # Input: arg1 = mission_template_id, arg2 = option_index
  # Output: trigger_result = 1 for option available, 0 for not available
  # reg0 = option_value
  ("game_get_multiplayer_server_option_for_mission_template",
   [
     (store_script_param, ":mission_template_id", 1),
     (store_script_param, ":option_index", 2),
     (try_begin),
       (eq, ":option_index", 0),
       (assign, reg0, "$g_multiplayer_team_1_faction"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 1),
       (assign, reg0, "$g_multiplayer_team_2_faction"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 2),
       (assign, reg0, "$g_multiplayer_num_bots_team_1"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 3),
       (assign, reg0, "$g_multiplayer_num_bots_team_2"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 4),
       (server_get_friendly_fire, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 5),
       (server_get_melee_friendly_fire, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 6),
       (server_get_friendly_fire_damage_self_ratio, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 7),
       (server_get_friendly_fire_damage_friend_ratio, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 8),
       (server_get_ghost_mode, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 9),
       (server_get_control_block_dir, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 10),
       (server_get_combat_speed, reg0),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (eq, ":mission_template_id", "mt_multiplayer_hq"),
         (val_add, ":option_index", 1), #max game time
       (try_end),
       (eq, ":option_index", 11),
       (assign, reg0, "$g_multiplayer_game_max_minutes"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1), #max round time
       (try_end),
       (eq, ":option_index", 12),
       (assign, reg0, "$g_multiplayer_round_max_seconds"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (val_add, ":option_index", 1), #respawn as bot
       (try_end),
       (eq, ":option_index", 13),
       (assign, reg0, "$g_multiplayer_player_respawn_as_bot"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1), #respawn limit
       (try_end),
       (eq, ":option_index", 14),
       (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 15),
       (assign, reg0, "$g_multiplayer_game_max_points"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_hq"),
         (val_add, ":option_index", 1), #point gained from flags
       (try_end),
       (eq, ":option_index", 16),
       (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_cf"),
         (val_add, ":option_index", 1), #point gained from capturing flag
       (try_end),
       (eq, ":option_index", 17),
       (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 18),
       (assign, reg0, "$g_multiplayer_respawn_period"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 19),
       (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 20),
       (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
       (set_trigger_result, 1),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1),
       (try_end),
       (eq, ":option_index", 21),
       (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
       (set_trigger_result, 1),
     (try_end),
     ]),

  # script_game_multiplayer_server_option_for_mission_template_to_string
  # Input: arg1 = mission_template_id, arg2 = option_index, arg3 = option_value
  # Output: s0 = option_text
  ("game_multiplayer_server_option_for_mission_template_to_string",
   [
     (store_script_param, ":mission_template_id", 1),
     (store_script_param, ":option_index", 2),
     (store_script_param, ":option_value", 3),
     (str_clear, s0),
     (try_begin),
       (eq, ":option_index", 0),
       (assign, reg1, 1),
       (str_store_string, s0, "str_team_reg1_faction"),
       (str_store_faction_name, s1, ":option_value"),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 1),
       (assign, reg1, 2),
       (str_store_string, s0, "str_team_reg1_faction"),
       (str_store_faction_name, s1, ":option_value"),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 2),
       (assign, reg1, 1),
       (str_store_string, s0, "str_number_of_bots_in_team_reg1"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 3),
       (assign, reg1, 2),
       (str_store_string, s0, "str_number_of_bots_in_team_reg1"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 4),
       (str_store_string, s0, "str_allow_friendly_fire"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 5),
       (str_store_string, s0, "str_allow_melee_friendly_fire"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 6),
       (str_store_string, s0, "str_friendly_fire_damage_self_ratio"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 7),
       (str_store_string, s0, "str_friendly_fire_damage_friend_ratio"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 8),
       (str_store_string, s0, "str_spectator_camera"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_free"),
       (else_try),
         (eq, ":option_value", 1),
         (str_store_string, s1, "str_stick_to_any_player"),
       (else_try),
         (eq, ":option_value", 2),
         (str_store_string, s1, "str_stick_to_team_members"),
       (else_try),
         (str_store_string, s1, "str_stick_to_team_members_view"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 9),
       (str_store_string, s0, "str_control_block_direction"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_automatic"),
       (else_try),
         (str_store_string, s1, "str_by_mouse_movement"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 10),
       (str_store_string, s0, "str_combat_speed"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_combat_speed_0"),
       (else_try),
         (eq, ":option_value", 1),
         (str_store_string, s1, "str_combat_speed_1"),
       (else_try),
         (eq, ":option_value", 2),
         (str_store_string, s1, "str_combat_speed_2"),
       (else_try),
         (eq, ":option_value", 3),
         (str_store_string, s1, "str_combat_speed_3"),
       (else_try),
         (str_store_string, s1, "str_combat_speed_4"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (try_begin),
         (eq, ":mission_template_id", "mt_multiplayer_hq"),
         (val_add, ":option_index", 1), #max game time
       (try_end),
       (eq, ":option_index", 11),
       (str_store_string, s0, "str_map_time_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1), #max round time
       (try_end),
       (eq, ":option_index", 12),
       (str_store_string, s0, "str_round_time_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (val_add, ":option_index", 1), #respawn as bot
       (try_end),
       (eq, ":option_index", 13),
       (str_store_string, s0, "str_players_take_control_of_a_bot_after_death"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1), #respawn limit
       (try_end),
       (eq, ":option_index", 14),
       (str_store_string, s0, "str_defender_spawn_count_limit"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_unlimited"),
       (else_try),
         (assign, reg1, ":option_value"),
         (str_store_string, s1, "str_reg1"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 15),
       (str_store_string, s0, "str_team_points_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_hq"),
         (val_add, ":option_index", 1), #point gained from flags
       (try_end),
       (eq, ":option_index", 16),
       (str_store_string, s0, "str_point_gained_from_flags"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_cf"),
         (val_add, ":option_index", 1), #point gained from capturing flag
       (try_end),
       (eq, ":option_index", 17),
       (str_store_string, s0, "str_point_gained_from_capturing_flag"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 18),
       (str_store_string, s0, "str_respawn_period"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 19),
       (str_store_string, s0, "str_initial_gold_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 20),
       (str_store_string, s0, "str_battle_earnings_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (try_begin),
         (neq, ":mission_template_id", "mt_multiplayer_bt"),
         (neq, ":mission_template_id", "mt_multiplayer_fd"),
         (neq, ":mission_template_id", "mt_multiplayer_sg"),
         (val_add, ":option_index", 1),
       (try_end),
       (eq, ":option_index", 21),
       (str_store_string, s0, "str_round_earnings_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (try_end),
     ]),

  # script_cf_multiplayer_team_is_available
  # Input: arg1 = player_no, arg2 = team_no
  # Output: none, true or false
  ("cf_multiplayer_team_is_available",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":team_no", 2),
     (assign, ":continue_change_team", 1),
     (try_begin),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (is_between, ":team_no", 0, multi_team_spectator),
       (neg|teams_are_enemies, ":team_no", ":team_no"), #checking if it is a deathmatch or not
       (assign, ":continue_change_team", 0),
       #counting number of players for team balance checks
       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
         (neq, ":cur_player", ":player_no"),
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

       (try_begin),
         (ge, ":difference_of_number_of_players", 0),
         (val_add, ":difference_of_number_of_players", 1),
       (else_try),
         (val_add, ":difference_of_number_of_players", -1),
       (try_end),

       (try_begin),
         (eq, ":team_no", 0),
         (lt, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
         (assign, ":continue_change_team", 1),
       (else_try),
         (eq, ":team_no", 1),
         (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
         (gt, ":difference_of_number_of_players", ":checked_value"),
         (assign, ":continue_change_team", 1),
       (try_end),
     (try_end),
     (eq, ":continue_change_team", 1),
     ]),

  # script_find_number_of_agents_constant
  # Input: arg1 = agent_no
  # Output: none
  ("game_multiplayer_event_duel_offered",
   [
     (store_script_param, ":agent_no", 1),
     (get_player_agent_no, ":player_agent_no"),
     (try_begin),
       (agent_is_active, ":player_agent_no"),
       (this_or_next|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, -1),
       (agent_check_offer_from_agent, ":player_agent_no", ":agent_no"),
       (neg|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, ":agent_no"), #don't allow spamming duel offers during countdown
       (multiplayer_send_int_to_server, multiplayer_event_offer_duel, ":agent_no"),
       (agent_get_player_id, ":player_no", ":agent_no"),
       (try_begin),
         (player_is_active, ":player_no"),
         (str_store_player_username, s0, ":player_no"),
       (else_try),
         (str_store_agent_name, s0, ":agent_no"),
       (try_end),
       (display_message, "str_a_duel_request_is_sent_to_s0"),
     (try_end),
     ]),

  # script_game_get_multiplayer_game_type_enum
  # Input: none
  # Output: reg0:first type, reg1:type count
  ("game_get_multiplayer_game_type_enum",
   [
     (assign, reg0, multiplayer_game_type_deathmatch),
	 (assign, reg1, multiplayer_num_game_types),
	 ]),

  # script_game_multiplayer_get_game_type_mission_template
  # Input: arg1 = game_type
  # Output: mission_template
  ("game_multiplayer_get_game_type_mission_template",
   [
     (assign, ":selected_mt", -1),
     (store_script_param, ":game_type", 1),
     (try_begin),
       (eq, ":game_type", multiplayer_game_type_deathmatch),
       (assign, ":selected_mt", "mt_multiplayer_dm"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_team_deathmatch),
       (assign, ":selected_mt", "mt_multiplayer_tdm"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_battle),
       (assign, ":selected_mt", "mt_multiplayer_bt"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_destroy),
       (assign, ":selected_mt", "mt_multiplayer_fd"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_capture_the_flag),
       (assign, ":selected_mt", "mt_multiplayer_cf"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_headquarters),
       (assign, ":selected_mt", "mt_multiplayer_hq"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_siege),
       (assign, ":selected_mt", "mt_multiplayer_sg"),
     (else_try),
       (eq, ":game_type", multiplayer_game_type_duel),
       (assign, ":selected_mt", "mt_multiplayer_duel"),
     (try_end),
     (assign, reg0, ":selected_mt"),
     ]),

  # script_multiplayer_get_mission_template_game_type
  # Input: arg1 = mission_template_no
  # Output: game_type
  ("multiplayer_get_mission_template_game_type",
   [
     (store_script_param, ":mission_template_no", 1),
     (assign, ":game_type", -1),
     (try_begin),
       (eq, ":mission_template_no", "mt_multiplayer_dm"),
       (assign, ":game_type", multiplayer_game_type_deathmatch),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_tdm"),
       (assign, ":game_type", multiplayer_game_type_team_deathmatch),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_bt"),
       (assign, ":game_type", multiplayer_game_type_battle),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_fd"),
       (assign, ":game_type", multiplayer_game_type_destroy),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_cf"),
       (assign, ":game_type", multiplayer_game_type_capture_the_flag),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_hq"),
       (assign, ":game_type", multiplayer_game_type_headquarters),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_sg"),
       (assign, ":game_type", multiplayer_game_type_siege),
     (else_try),
       (eq, ":mission_template_no", "mt_multiplayer_duel"),
       (assign, ":game_type", multiplayer_game_type_duel),
     (try_end),
     (assign, reg0, ":game_type"),
     ]),


  # script_multiplayer_fill_available_factions_combo_button
  # Input: arg1 = overlay_id, arg2 = selected_faction_no, arg3 = opposite_team_selected_faction_no
  # Output: none
  ("multiplayer_fill_available_factions_combo_button",
   [
     (store_script_param, ":overlay_id", 1),
     (store_script_param, ":selected_faction_no", 2),
##     (store_script_param, ":opposite_team_selected_faction_no", 3),
##     (try_for_range, ":cur_faction", "fac_kingdom_1", "fac_kingdoms_end"),
##       (try_begin),
##         (eq, ":opposite_team_selected_faction_no", ":cur_faction"),
##         (try_begin),
##           (gt, ":selected_faction_no", ":opposite_team_selected_faction_no"),
##           (val_sub, ":selected_faction_no", 1),
##         (try_end),
##       (else_try),
##         (str_store_faction_name, s0, ":cur_faction"),
##         (overlay_add_item, ":overlay_id", s0),
##       (try_end),
##     (try_end),
##     (val_sub, ":selected_faction_no", "fac_kingdom_1"),
##     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
       (str_store_faction_name, s0, ":cur_faction"),
       (overlay_add_item, ":overlay_id", s0),
     (try_end),
     (val_sub, ":selected_faction_no", "fac_kingdom_1"),
     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     ]),


  # script_multiplayer_get_troop_class
  # Input: arg1 = troop_no
  # Output: reg0: troop_class
  ("multiplayer_get_troop_class",
   [
     (store_script_param_1, ":troop_no"),
     (assign, ":troop_class", multi_troop_class_other),
     (try_begin),
       (this_or_next|eq, ":troop_no", "trp_vaegir_archer_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_nord_archer_multiplayer"),
       (eq, ":troop_no", "trp_sarranid_archer_multiplayer"),
       (assign, ":troop_class", multi_troop_class_archer),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_man_at_arms_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_nord_scout_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_rhodok_horseman_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_sarranid_mamluke_multiplayer"),
       (eq, ":troop_no", "trp_vaegir_horseman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_cavalry),
     (else_try),
       (eq, ":troop_no", "trp_khergit_veteran_horse_archer_multiplayer"),
       (assign, ":troop_class", multi_troop_class_mounted_archer),
#     (else_try),
#       (eq, ":troop_no", "trp_swadian_mounted_crossbowman_multiplayer"),
#       (assign, ":troop_class", multi_troop_class_mounted_crossbowman),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_crossbowman_multiplayer"),
       (eq, ":troop_no", "trp_rhodok_veteran_crossbowman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_crossbowman),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_swadian_infantry_multiplayer"),
       (this_or_next|eq, ":troop_no", "trp_sarranid_footman_multiplayer"),
       (eq, ":troop_no", "trp_nord_veteran_multiplayer"),
       (assign, ":troop_class", multi_troop_class_infantry),
     (else_try),
       (eq, ":troop_no", "trp_vaegir_spearman_multiplayer"),
       (assign, ":troop_class", multi_troop_class_spearman),
     (try_end),
     (assign, reg0, ":troop_class"),
     ]),

  #script_multiplayer_clear_player_selected_items
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_clear_player_selected_items",
   [
     (store_script_param, ":player_no", 1),
     (try_for_range, ":slot_no", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_set_slot, ":player_no", ":slot_no", -1),
     (try_end),
     ]),


  #script_multiplayer_init_player_slots
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_init_player_slots",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_multiplayer_clear_player_selected_items", ":player_no"),
     (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (player_set_slot, ":player_no", slot_player_poll_disabled_until_time, 0),

     (player_set_slot, ":player_no", slot_player_bot_type_1_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_2_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_3_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_4_wanted, 0),
     ]),

  #script_multiplayer_initialize_belfry_wheel_rotations
  # Input: none
  # Output: none
  ("multiplayer_initialize_belfry_wheel_rotations",
   [
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_mul, ":wheel_no", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),
##    (try_end),
##
##    (scene_prop_get_num_instances, ":num_belfries_a", "spr_belfry_a"),
##
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_add, ":wheel_no_plus_num_belfries_a", ":wheel_no", ":num_belfries_a"),
##      (store_mul, ":wheel_no_plus_num_belfries_a", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),
##    (try_end),

      (scene_prop_get_num_instances, ":num_wheel", "spr_belfry_wheel"),
      (try_for_range, ":wheel_no", 0, ":num_wheel"),
        (scene_prop_get_instance, ":wheel_id", "spr_belfry_wheel", ":wheel_no"),
        (prop_instance_initialize_rotation_angles, ":wheel_id"),
      (try_end),

      (scene_prop_get_num_instances, ":num_winch", "spr_winch"),
      (try_for_range, ":winch_no", 0, ":num_winch"),
        (scene_prop_get_instance, ":winch_id", "spr_winch", ":winch_no"),
        (prop_instance_initialize_rotation_angles, ":winch_id"),
      (try_end),

      (scene_prop_get_num_instances, ":num_winch_b", "spr_winch_b"),
      (try_for_range, ":winch_b_no", 0, ":num_winch_b"),
        (scene_prop_get_instance, ":winch_b_id", "spr_winch_b", ":winch_b_no"),
        (prop_instance_initialize_rotation_angles, ":winch_b_id"),
      (try_end),
     ]),

  #script_send_open_close_information_of_object
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_send_initial_information",
   [
     (store_script_param, ":player_no", 1),

     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_auto_team_balance_limit, "$g_multiplayer_auto_team_balance_limit"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_num_bots_voteable, "$g_multiplayer_num_bots_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_factions_voteable, "$g_multiplayer_factions_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_maps_voteable, "$g_multiplayer_maps_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_kick_voteable, "$g_multiplayer_kick_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ban_voteable, "$g_multiplayer_ban_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_allow_player_banners, "$g_multiplayer_allow_player_banners"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_force_default_armor, "$g_multiplayer_force_default_armor"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_disallow_ranged_weapons, "$g_multiplayer_disallow_ranged_weapons"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_type, "$g_multiplayer_game_type"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),

     (store_mission_timer_a, ":mission_timer"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_server_mission_timer_while_player_joined, ":mission_timer"),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_count, "$g_multiplayer_number_of_respawn_count"),
     (try_end),

     (try_for_agents, ":cur_agent"), #send if any agent is carrying any scene object
       (agent_is_human, ":cur_agent"),
       (agent_get_attached_scene_prop, ":attached_scene_prop", ":cur_agent"),
       (ge, ":attached_scene_prop", 0),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":cur_agent", ":attached_scene_prop"),
     (try_end),

     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_6m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_8m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_10m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_12m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_14m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_winch_b"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_e_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_left"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_right"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_door_destructible"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_b"),

     (try_begin),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

       (store_mission_timer_a, ":current_time"),
       (val_sub, ":current_time", "$g_round_start_time"),
       (val_mul, ":current_time", -1),

       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, ":current_time"),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       #if game type is capture the flag send current flag situations to each player.
       (team_get_slot, ":flag_situation_team_1", 0, slot_team_flag_situation),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, 0, ":flag_situation_team_1"),
       (team_get_slot, ":flag_situation_team_2", 1, slot_team_flag_situation),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, 1, ":flag_situation_team_2"),
     (else_try),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       #if game type is headquarters send number of agents placed around each pole's around to player.
       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (assign, ":number_of_agents_around_flag_team_1", 0),
         (assign, ":number_of_agents_around_flag_team_2", 0),

         (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
         (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.

         (try_for_agents, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (agent_is_alive, ":cur_agent"),
           (neg|agent_is_non_player, ":cur_agent"),
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
           (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
           (get_sq_distance_between_position_heights, ":squared_height_dist", pos0, pos1),
           (val_add, ":squared_dist", ":squared_height_dist"),
           (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
           (try_begin),
             (eq, ":cur_agent_team", 0),
             (val_add, ":number_of_agents_around_flag_team_1", 1),
           (else_try),
             (eq, ":cur_agent_team", 1),
             (val_add, ":number_of_agents_around_flag_team_2", 1),
           (try_end),
         (try_end),

         (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
         (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),
         (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
       (try_end),

       #if game type is headquarters send owners of each pole to player.
       (assign, "$g_placing_initial_flags", 1),
       (try_for_range, ":cur_flag", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":cur_flag"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_slot"),
         (store_mul, ":cur_flag_owner_code", ":cur_flag_owner", 100),
         (val_add, ":cur_flag_owner_code", ":cur_flag_owner"),
         (val_add, ":cur_flag_owner_code", 1),
         (val_mul, ":cur_flag_owner_code", -1),
         (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":cur_flag", ":cur_flag_owner_code"),
       (try_end),
       (assign, "$g_placing_initial_flags", 0),
     (try_end),

     #(multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_day_time, "$g_round_day_time"),
    ]),

  #script_multiplayer_remove_headquarters_flags
  # Input: none
  # Output: none
  ("multiplayer_remove_headquarters_flags",
   [
     (store_add, ":end_cond", "spr_headquarters_flag_gray", 1),
     (try_for_range, ":headquarters_flag_no", "spr_headquarters_flag_red", ":end_cond"),
       (replace_scene_props, ":headquarters_flag_no", "spr_empty"),
     (try_end),
     ]),

  #script_multiplayer_remove_destroy_mod_targets
  # Input: none
  # Output: none
  ("multiplayer_remove_destroy_mod_targets",
   [
       (replace_scene_props, "spr_catapult_destructible", "spr_empty"),
       (replace_scene_props, "spr_trebuchet_destructible", "spr_empty"),
     ]),

  #script_multiplayer_init_mission_variables
  ("multiplayer_init_mission_variables",
   [
     (assign, "$g_multiplayer_team_1_first_spawn", 1),
     (assign, "$g_multiplayer_team_2_first_spawn", 1),
     (assign, "$g_multiplayer_poll_running", 0),
##     (assign, "$g_multiplayer_show_poll_when_suitable", 0),
     (assign, "$g_waiting_for_confirmation_to_terminate", 0),
     (assign, "$g_confirmation_result", 0),
     (assign, "$g_team_balance_next_round", 0),
     (team_get_faction, "$g_multiplayer_team_1_faction", 0),
     (team_get_faction, "$g_multiplayer_team_2_faction", 1),
     (assign, "$g_multiplayer_next_team_1_faction", "$g_multiplayer_team_1_faction"),
     (assign, "$g_multiplayer_next_team_2_faction", "$g_multiplayer_team_2_faction"),

     (assign, "$g_multiplayer_bot_type_1_wanted", 0),
     (assign, "$g_multiplayer_bot_type_2_wanted", 0),
     (assign, "$g_multiplayer_bot_type_3_wanted", 0),
     (assign, "$g_multiplayer_bot_type_4_wanted", 0),

     (call_script, "script_music_set_situation_with_culture", mtf_sit_multiplayer_fight),
     ]),

  #script_multiplayer_event_mission_end
  # Input: none
  # Output: none
  ("multiplayer_event_mission_end",
   [
     #EVERY_BREATH_YOU_TAKE achievement
     (try_begin),
       (multiplayer_get_my_player, ":my_player_no"),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_kill_count, ":kill_count", ":my_player_no"),
       (player_get_death_count, ":death_count", ":my_player_no"),
       (gt, ":kill_count", ":death_count"),
       (unlock_achievement, ACHIEVEMENT_EVERY_BREATH_YOU_TAKE),
     (try_end),
     #EVERY_BREATH_YOU_TAKE achievement end
     ]),


  #script_multiplayer_event_agent_killed_or_wounded
  # Input: arg1 = dead_agent_no, arg2 = killer_agent_no
  # Output: none
  ("multiplayer_event_agent_killed_or_wounded",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),

     (multiplayer_get_my_player, ":my_player_no"),
     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":my_player_agent", ":my_player_no"),
       (ge, ":my_player_agent", 0),
       (try_begin),
         (eq, ":my_player_agent", ":dead_agent_no"),
         (store_mission_timer_a, "$g_multiplayer_respawn_start_time"),
       (try_end),
       (try_begin),
         (eq, ":my_player_agent", ":killer_agent_no"),
         (neq, ":my_player_agent", ":dead_agent_no"),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_alive, ":my_player_agent"),
         (neg|agent_is_ally, ":dead_agent_no"),
         (agent_get_horse, ":my_horse_agent", ":my_player_agent"),
         (agent_get_wielded_item, ":my_wielded_item", ":my_player_agent", 0),
         (assign, ":my_item_class", -1),
         (try_begin),
           (ge, ":my_wielded_item", 0),
           (item_get_slot, ":my_item_class", ":my_wielded_item", slot_item_multiplayer_item_class),
         (try_end),
         #SPOIL_THE_CHARGE achievement
         (try_begin),
           (lt, ":my_horse_agent", 0),
           (agent_get_horse, ":dead_agent_horse_agent", ":dead_agent_no"),
           (ge, ":dead_agent_horse_agent", 0),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SPOIL_THE_CHARGE, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SPOIL_THE_CHARGE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_SPOIL_THE_CHARGE),
         (try_end),
         #SPOIL_THE_CHARGE achievement end
         #HARASSING_HORSEMAN achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_bow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_crossbow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_HARASSING_HORSEMAN, 0),
           (lt, ":achievement_stat", 100),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_HARASSING_HORSEMAN, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 100),
           (unlock_achievement, ACHIEVEMENT_HARASSING_HORSEMAN),
         (try_end),
         #HARASSING_HORSEMAN achievement end
         #THROWING_STAR achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THROWING_STAR, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THROWING_STAR, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_THROWING_STAR),
         (try_end),
         #THROWING_STAR achievement end
         #SHISH_KEBAB achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (eq, ":my_item_class", multi_item_class_type_lance),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SHISH_KEBAB, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SHISH_KEBAB, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_SHISH_KEBAB),
         (try_end),
         #SHISH_KEBAB achievement end
         #CHOPPY_CHOP_CHOP achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_axe),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_cleavers),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_axe),
           (this_or_next|eq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (eq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_CHOPPY_CHOP_CHOP),
         (try_end),
         #CHOPPY_CHOP_CHOP achievement end
         #MACE_IN_YER_FACE achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_blunt),
           (eq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_MACE_IN_YER_FACE, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_MACE_IN_YER_FACE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_MACE_IN_YER_FACE),
         (try_end),
         #MACE_IN_YER_FACE achievement end
         #THE_HUSCARL achievement
         (try_begin),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THE_HUSCARL, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THE_HUSCARL, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_THE_HUSCARL),
         (try_end),
         #THE_HUSCARL achievement end
       (try_end),
     (try_end),

     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":player_agent", ":my_player_no"),
       (eq, ":dead_agent_no", ":player_agent"),

       (assign, ":show_respawn_counter", 0),
       (try_begin),
         #TODO: add other game types with no respawns here
         (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
         (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
         (assign, ":show_respawn_counter", 1),
       (else_try),
         (eq, "$g_multiplayer_player_respawn_as_bot", 1),
         (player_get_team_no, ":my_player_team", ":my_player_no"),
         (assign, ":is_found", 0),
         (try_for_agents, ":cur_agent"),
           (eq, ":is_found", 0),
           (agent_is_alive, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_get_team ,":cur_team", ":cur_agent"),
           (eq, ":cur_team", ":my_player_team"),
           (assign, ":is_found", 1),
         (try_end),
         (eq, ":is_found", 1),
         (assign, ":show_respawn_counter", 1),
       (try_end),

       (try_begin),
         #(player_get_slot, ":spawn_count", ":player_no", slot_player_spawn_count),
         (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
         (gt, "$g_multiplayer_number_of_respawn_count", 0),

         (ge, "$g_my_spawn_count", "$g_multiplayer_number_of_respawn_count"),

         (multiplayer_get_my_player, ":my_player_no"),
         (player_get_team_no, ":my_player_team", ":my_player_no"),

         (this_or_next|eq, ":my_player_team", 0),
         (ge, "$g_my_spawn_count", 999),

         (assign, "$g_show_no_more_respawns_remained", 1),
       (else_try),
         (assign, "$g_show_no_more_respawns_remained", 0),
       (try_end),

       (eq, ":show_respawn_counter", 1),

       (start_presentation, "prsnt_multiplayer_respawn_time_counter"),
     (try_end),
     ]),

  #script_multiplayer_get_item_value_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: item_value
  ("multiplayer_get_item_value_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (try_begin),
       (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":item_no", ":troop_no"),
       (assign, ":item_value", 0),
     (else_try),
       (store_item_value, ":item_value", ":item_no"),
       (store_troop_faction, ":faction_no", ":troop_no"),
       (store_sub, ":faction_slot", ":faction_no", npc_kingdoms_begin),
       (val_add, ":faction_slot", slot_item_multiplayer_faction_price_multipliers_begin),
       (item_get_slot, ":price_multiplier", ":item_no", ":faction_slot"),
       (val_mul, ":item_value", ":price_multiplier"),
       (val_div, ":item_value", 100),
     (try_end),
     (assign, reg0, ":item_value"),
     ]),

  #script_multiplayer_get_previous_item_for_item_and_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: previous_item_no (-1 if it is the root item, 0 if the item is invalid)
  ("multiplayer_get_previous_item_for_item_and_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
     (call_script, "script_multiplayer_get_item_value_for_troop", ":item_no", ":troop_no"),
     (assign, ":item_value", reg0),
     (store_sub, ":troop_index", ":troop_no", multiplayer_troops_begin),
     (val_add, ":troop_index", slot_item_multiplayer_availability_linked_list_begin),
     (assign, ":max_item_no", -1),
     (assign, ":max_item_value", -1),
     (try_for_range, ":i_item", all_items_begin, all_items_end),
       (item_slot_eq, ":i_item", slot_item_multiplayer_item_class, ":item_class"),
       (item_slot_ge, ":i_item", ":troop_index", 1),
       (call_script, "script_multiplayer_get_item_value_for_troop", ":i_item", ":troop_no"),
       (assign, ":i_item_value", reg0),
       (try_begin),
         (eq, ":i_item_value", 0),
         (eq, ":max_item_value", 0),
         #choose between 2 default items
         (store_item_value, ":i_item_real_value", ":i_item"),
         (store_item_value, ":max_item_real_value", ":max_item_no"),
         (try_begin),
           (gt, ":i_item_real_value", ":max_item_real_value"),
           (assign, ":max_item_value", ":i_item_value"),
           (assign, ":max_item_no", ":i_item"),
         (try_end),
       (else_try),
         (gt, ":i_item_value", ":max_item_value"),
         (lt, ":i_item_value", ":item_value"),
         (assign, ":max_item_value", ":i_item_value"),
         (assign, ":max_item_no", ":i_item"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":max_item_no", -1),
       (assign, ":item_upper_class", -1),
       (try_begin),
         (is_between, ":item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
         (assign, ":item_upper_class", 0),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_shields_begin, multi_item_class_type_shields_end),
         (assign, ":item_upper_class", 1),
       (else_try),
         (eq, ":item_class", multi_item_class_type_bow),
         (assign, ":item_upper_class", 2),
       (else_try),
         (eq, ":item_class", multi_item_class_type_crossbow),
         (assign, ":item_upper_class", 3),
       (else_try),
         (eq, ":item_class", multi_item_class_type_arrow),
         (assign, ":item_upper_class", 4),
       (else_try),
         (eq, ":item_class", multi_item_class_type_bolt),
         (assign, ":item_upper_class", 5),
       (else_try),
         (eq, ":item_class", multi_item_class_type_throwing),
         (assign, ":item_upper_class", 6),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
         (assign, ":item_upper_class", 7),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
         (assign, ":item_upper_class", 8),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
         (assign, ":item_upper_class", 9),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
         (assign, ":item_upper_class", 10),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
         (assign, ":item_upper_class", 11),
       (try_end),
       (neq, ":item_upper_class", 0),
       #search for the default item for non-weapon classes (only 1 slot is easy to fill)
       (assign, ":end_cond", all_items_end),
       (try_for_range, ":i_item", all_items_begin, ":end_cond"),
         (item_slot_ge, ":i_item", ":troop_index", 1),
         (item_get_slot, ":i_item_class", ":i_item", slot_item_multiplayer_item_class),
         (try_begin),
           (is_between, ":i_item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
           (assign, ":i_item_upper_class", 0),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_shields_begin, multi_item_class_type_shields_end),
           (assign, ":i_item_upper_class", 1),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_bow),
           (assign, ":i_item_upper_class", 2),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_crossbow),
           (assign, ":i_item_upper_class", 3),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_arrow),
           (assign, ":i_item_upper_class", 4),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_bolt),
           (assign, ":i_item_upper_class", 5),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_throwing),
           (assign, ":i_item_upper_class", 6),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
           (assign, ":i_item_upper_class", 7),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
           (assign, ":i_item_upper_class", 8),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
           (assign, ":i_item_upper_class", 9),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
           (assign, ":i_item_upper_class", 10),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
           (assign, ":i_item_upper_class", 11),
         (try_end),
         (eq, ":i_item_upper_class", ":item_upper_class"),
         (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_item", ":troop_no"),
         (assign, ":max_item_no", ":i_item"),
         (assign, ":end_cond", 0), #break
       (try_end),
     (try_end),
     (assign, reg0, ":max_item_no"),
     ]),

  #script_cf_multiplayer_is_item_default_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: total_cost
  ("cf_multiplayer_is_item_default_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (assign, ":default_item", 0),
     (try_begin),
       (neg|is_between, ":item_no", horses_begin, horses_end),
       (neq, ":item_no", "itm_warhorse_sarranid"),
       (neq, ":item_no", "itm_warhorse_steppe"),

       (troop_get_inventory_capacity, ":end_cond", ":troop_no"), #troop no can come -1 here error occured at friday
       (try_for_range, ":i_slot", 0, ":end_cond"),
         (troop_get_inventory_slot, ":default_item_id", ":troop_no", ":i_slot"),
         (eq, ":item_no", ":default_item_id"),
         (assign, ":default_item", 1),
         (assign, ":end_cond", 0), #break
       (try_end),
     (try_end),
     (eq, ":default_item", 1),
     ]),

  #script_multiplayer_calculate_cur_selected_items_cost
  # Input: arg1 = player_no
  # Output: reg0: total_cost
  ("multiplayer_calculate_cur_selected_items_cost",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":calculation_type", 2), #0 for normal calculation
     (assign, ":total_cost", 0),
     (player_get_troop_id, ":troop_no", ":player_no"),

     (try_begin),
       (eq, ":calculation_type", 0),
       (assign, ":begin_cond", slot_player_cur_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_cur_selected_item_indices_end),
     (else_try),
       (assign, ":begin_cond", slot_player_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_selected_item_indices_end),
     (try_end),

     (try_for_range, ":i_item", ":begin_cond", ":end_cond"),
       (player_get_slot, ":item_id", ":player_no", ":i_item"),
       (ge, ":item_id", 0), #might be -1 for horses etc.
       (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_no"),
       (val_add, ":total_cost", reg0),
     (try_end),
     (assign, reg0, ":total_cost"),
     ]),

  #script_multiplayer_set_item_available_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: none
  ("multiplayer_set_item_available_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),
     (item_set_slot, ":item_no", ":item_troop_slot", 1),
     ]),

  #script_multiplayer_send_item_selections
  # Input: none
  # Output: none
  ("multiplayer_send_item_selections",
   [
     (multiplayer_get_my_player, ":my_player_no"),
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":item_id", ":my_player_no", ":i_item"),
       (multiplayer_send_2_int_to_server, multiplayer_event_set_item_selection, ":i_item", ":item_id"),
     (try_end),
     ]),

  #script_multiplayer_set_default_item_selections_for_troop
  # Input: arg1 = troop_no
  # Output: none
  ("multiplayer_set_default_item_selections_for_troop",
   [
     (store_script_param, ":troop_no", 1),
     (multiplayer_get_my_player, ":my_player_no"),
     (call_script, "script_multiplayer_clear_player_selected_items", ":my_player_no"),
     (assign, ":cur_weapon_slot", 0),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":item_id", ":troop_no", ":i_slot"),
       (ge, ":item_id", 0),
       (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
       (try_begin),
         (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
         (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
         (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, ":cur_weapon_slot"),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
         (val_add, ":cur_weapon_slot", 1),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 4),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 5),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 6),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 7),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
         (eq, "$g_horses_are_avaliable", 1),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 8),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_display_available_items_for_troop_and_item_classes
  # Input: arg1 = troop_no, arg2 = item_classes_begin, arg3 = item_classes_end, arg4 = pos_x_begin, arg5 = pos_y_begin
  # Output: none
  ("multiplayer_display_available_items_for_troop_and_item_classes",
   [
     (store_script_param, ":troop_no", 1),
     (store_script_param, ":item_classes_begin", 2),
     (store_script_param, ":item_classes_end", 3),
     (store_script_param, ":pos_x_begin", 4),
     (store_script_param, ":pos_y_begin", 5),

     (assign, ":x_adder", 100),
     (try_begin),
       (gt, ":pos_x_begin", 500),
       (assign, ":x_adder", -100),
     (try_end),

     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),

     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, multi_data_item_button_indices_end),
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot", -1),
     (try_end),

     (assign, ":num_available_items", 0),

     (try_for_range, ":item_no", all_items_begin, all_items_end),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (is_between, ":item_class", ":item_classes_begin", ":item_classes_end"),
       (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
       (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
       (item_slot_ge, ":item_no", ":item_troop_slot", 1),
       (store_add, ":cur_slot_index", ":num_available_items", multi_data_item_button_indices_begin),
       #using the result array for item_ids
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot_index", ":item_no"),
       (val_add, ":num_available_items", 1),
     (try_end),

     #sorting
     (store_add, ":item_slots_end", ":num_available_items", multi_data_item_button_indices_begin),
     (store_sub, ":item_slots_end_minus_one", ":item_slots_end", 1),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end_minus_one"),
       (store_add, ":cur_slot_2_begin", ":cur_slot", 1),
       (try_for_range, ":cur_slot_2", ":cur_slot_2_begin", ":item_slots_end"),
         (troop_get_slot, ":item_1", "trp_multiplayer_data", ":cur_slot"),
         (troop_get_slot, ":item_2", "trp_multiplayer_data", ":cur_slot_2"),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_1", ":troop_no"),
         (assign, ":item_1_point", reg0),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_2", ":troop_no"),
         (assign, ":item_2_point", reg0),
         (item_get_slot, ":item_1_class", ":item_1", slot_item_multiplayer_item_class),
         (item_get_slot, ":item_2_class", ":item_2", slot_item_multiplayer_item_class),
         (val_mul, ":item_1_class", 1000000), #assuming maximum item price is 1000000
         (val_mul, ":item_2_class", 1000000), #assuming maximum item price is 1000000
         (val_add, ":item_1_point", ":item_1_class"),
         (val_add, ":item_2_point", ":item_2_class"),
         (lt, ":item_2_point", ":item_1_point"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot", ":item_2"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot_2", ":item_1"),
       (try_end),
     (try_end),

     (troop_get_slot, ":last_item_no", "trp_multiplayer_data", multi_data_item_button_indices_begin),
     (assign, ":num_item_classes", 0),
     (try_begin),
       (ge, ":last_item_no", 0),
       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),

       (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
         (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
         (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
         (neq, ":item_class", ":last_item_class"),
         (val_add, ":num_item_classes", 1),
         (assign, ":last_item_class", ":item_class"),
       (try_end),

       (try_begin),
         (store_mul, ":required_y", ":num_item_classes", 100),
         (gt, ":required_y", ":pos_y_begin"),
         (store_sub, ":dif", ":required_y", ":pos_y_begin"),
         (val_div, ":dif", 100),
         (val_add, ":dif", 1),
         (val_mul, ":dif", 100),
         (val_add, ":pos_y_begin", ":dif"),
       (try_end),

       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),
     (try_end),
     (assign, ":cur_x", ":pos_x_begin"),
     (assign, ":cur_y", ":pos_y_begin"),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
       (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (try_begin),
         (neq, ":item_class", ":last_item_class"),
         (val_sub, ":cur_y", 100),
         (assign, ":cur_x", ":pos_x_begin"),
         (assign, ":last_item_class", ":item_class"),
       (try_end),
       (create_image_button_overlay, ":cur_obj", "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
       (position_set_x, pos1, 800),
       (position_set_y, pos1, 800),
       (overlay_set_size, ":cur_obj", pos1),
       (position_set_x, pos1, ":cur_x"),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, ":cur_obj", pos1),
       (create_mesh_overlay_with_item_id, reg0, ":item_no"),
       (store_add, ":item_x", ":cur_x", 50),
       (store_add, ":item_y", ":cur_y", 50),
       (position_set_x, pos1, ":item_x"),
       (position_set_y, pos1, ":item_y"),
       (overlay_set_position, reg0, pos1),
       (val_add, ":cur_x", ":x_adder"),
     (try_end),
     ]),

  # script_multiplayer_fill_map_game_types
  # Input: game_type
  # Output: num_maps
  ("multiplayer_fill_map_game_types",
    [
      (store_script_param, ":game_type", 1),
      (try_for_range, ":i_multi", multi_data_maps_for_game_type_begin, multi_data_maps_for_game_type_end),
        (troop_set_slot, "trp_multiplayer_data", ":i_multi", -1),
      (try_end),
      (assign, ":num_maps", 0),
      (try_begin),
        (this_or_next|eq, ":game_type", multiplayer_game_type_deathmatch),
        (this_or_next|eq, ":game_type", multiplayer_game_type_duel),
        (eq, ":game_type", multiplayer_game_type_team_deathmatch),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_1"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_2"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_4"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_7"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_9"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_11"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 6, "scn_multi_scene_12"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 7, "scn_multi_scene_14"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 8, "scn_multi_scene_17"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 9, "scn_multi_scene_18"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 10, "scn_multi_scene_19"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 11, "scn_multi_scene_20"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 12, "scn_random_multi_plain_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 13, "scn_random_multi_plain_large"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 14, "scn_random_multi_steppe_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 15, "scn_random_multi_steppe_large"),
        (assign, ":num_maps", 16),
      (else_try),
        (eq, ":game_type", multiplayer_game_type_battle),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_1"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_2"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_4"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_7"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_9"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_11"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 6, "scn_multi_scene_12"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 7, "scn_multi_scene_14"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 8, "scn_multi_scene_17"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 9, "scn_multi_scene_18"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 10, "scn_multi_scene_19"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 11, "scn_multi_scene_20"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 12, "scn_random_multi_plain_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 13, "scn_random_multi_plain_large"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 14, "scn_random_multi_steppe_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 15, "scn_random_multi_steppe_large"),
        (assign, ":num_maps", 16),
      (else_try),
        (eq, ":game_type", multiplayer_game_type_destroy),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_1"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_2"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_4"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_7"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_9"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_12"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 6, "scn_multi_scene_14"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 7, "scn_multi_scene_19"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 8, "scn_multi_scene_20"),
        (assign, ":num_maps", 9),
      (else_try),
        (eq, ":game_type", multiplayer_game_type_capture_the_flag),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_1"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_2"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_4"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_7"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_9"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_11"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 6, "scn_multi_scene_12"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 7, "scn_multi_scene_14"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 8, "scn_multi_scene_17"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 9, "scn_multi_scene_18"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 10, "scn_multi_scene_19"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 11, "scn_multi_scene_20"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 12, "scn_random_multi_plain_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 13, "scn_random_multi_plain_large"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 14, "scn_random_multi_steppe_medium"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 15, "scn_random_multi_steppe_large"),
        (assign, ":num_maps", 16),
      (else_try),
        (eq, ":game_type", multiplayer_game_type_headquarters),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_1"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_2"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_4"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_7"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_9"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_11"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 6, "scn_multi_scene_12"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 7, "scn_multi_scene_14"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 8, "scn_multi_scene_17"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 9, "scn_multi_scene_18"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 10, "scn_multi_scene_19"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 11, "scn_multi_scene_20"),
        (assign, ":num_maps", 12),
      (else_try),
        (eq, ":game_type", multiplayer_game_type_siege),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin, "scn_multi_scene_3"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 1, "scn_multi_scene_8"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 2, "scn_multi_scene_10"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 3, "scn_multi_scene_13"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 4, "scn_multi_scene_15"),
        (troop_set_slot, "trp_multiplayer_data", multi_data_maps_for_game_type_begin + 5, "scn_multi_scene_16"),
        (assign, ":num_maps", 6),
      (try_end),
      (assign, reg0, ":num_maps"),
      ]),


  # script_multiplayer_count_players_bots
  # Input: none
  # Output: none
  ("multiplayer_count_players_bots",
    [
      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (player_is_active, ":cur_player"),
        (player_set_slot, ":cur_player", slot_player_last_bot_count, 0),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_get_player_id, ":agent_player", ":cur_agent"),
        (lt, ":agent_player", 0), #not a player
        (agent_get_group, ":agent_group", ":cur_agent"),
        (player_is_active, ":agent_group"),
        (player_get_slot, ":bot_count", ":agent_group", slot_player_last_bot_count),
        (val_add, ":bot_count", 1),
        (player_set_slot, ":agent_group", slot_player_last_bot_count, ":bot_count"),
      (try_end),
      ]),

  # script_multiplayer_find_player_leader_for_bot
  # Input: arg1 = team_no
  # Output: reg0 = player_no
  ("multiplayer_find_player_leader_for_bot",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (team_get_faction, ":team_faction", ":team_no"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (call_script, "script_multiplayer_count_players_bots"),

      (assign, ":team_player_count", 0),

      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (assign, ":continue", 0),
        (player_is_active, ":cur_player"),
        (try_begin),
          (eq, ":look_only_actives", 0),
          (assign, ":continue", 1),
        (else_try),
          (neq, ":look_only_actives", 0),
          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),
          (assign, ":continue", 1),
        (try_end),

        (eq, ":continue", 1),

        (player_get_team_no, ":player_team", ":cur_player"),
        (eq, ":team_no", ":player_team"),
        (val_add, ":team_player_count", 1),
      (try_end),
      (assign, ":result_leader", -1),
      (try_begin),
        (gt, ":team_player_count", 0),
        (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_1"),
        (try_begin),
          (eq, ":team_no", 1),
          (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_2"),
        (try_end),
        (store_div, ":num_bots_for_each_player", ":total_bot_count", ":team_player_count"),
        (store_mul, ":check_remainder", ":num_bots_for_each_player", ":team_player_count"),
        (try_begin),
          (lt, ":check_remainder", ":total_bot_count"),
          (val_add, ":num_bots_for_each_player", 1),
        (try_end),

        (assign, ":total_bot_req", 0),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),

          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_add, ":total_bot_req", ":num_bots_for_each_player"),
          (val_sub, ":total_bot_req", ":player_bot_count"),
        (try_end),
        (gt, ":total_bot_req", 0),

        (store_random_in_range, ":random_bot", 0, ":total_bot_req"),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),

          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_sub, ":random_bot", ":num_bots_for_each_player"),
          (val_add, ":random_bot", ":player_bot_count"),
          (lt, ":random_bot", 0),
          (assign, ":result_leader", ":cur_player"),
          (assign, ":num_players", 0), #break
        (try_end),
      (try_end),
      (assign, reg0, ":result_leader"),
      ]),

  # script_multiplayer_find_bot_troop_and_group_for_spawn
  # Input: arg1 = team_no
  # Output: reg0 = troop_id, reg1 = group_id
  ("multiplayer_find_bot_troop_and_group_for_spawn",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", ":look_only_actives"),
      (assign, ":leader_player", reg0),

      (assign, ":available_troops_in_faction", 0),
      (assign, ":available_troops_to_spawn", 0),
      (team_get_faction, ":team_faction_no", ":team_no"),

      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (try_begin),
          (this_or_next|lt, ":leader_player", 0),
          (player_slot_ge, ":leader_player", ":wanted_slot", 1),
          (val_add, ":available_troops_to_spawn", 1),
        (try_end),
      (try_end),

      (assign, ":available_troops_in_faction", 0),

      (store_random_in_range, ":random_troop_index", 0, ":available_troops_to_spawn"),
      (assign, ":end_cond", multiplayer_ai_troops_end),
      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (this_or_next|lt, ":leader_player", 0),
        (player_slot_ge, ":leader_player", ":wanted_slot", 1),
        (val_sub, ":random_troop_index", 1),
        (lt, ":random_troop_index", 0),
        (assign, ":end_cond", 0),
        (assign, ":selected_troop", ":troop_no"),
      (try_end),
      (assign, reg0, ":selected_troop"),
      (assign, reg1, ":leader_player"),
      ]),

  # script_multiplayer_change_leader_of_bot
  # Input: arg1 = agent_no
  # Output: none
  ("multiplayer_change_leader_of_bot",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_team, ":team_no", ":agent_no"),
      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", 1),
      (assign, ":leader_player", reg0),
      (agent_set_group, ":agent_no", ":leader_player"),
      ]),

  ("multiplayer_find_spawn_point",
  [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care

     (set_fixed_point_multiplier, 100),

     (assign, ":flags", 0),

     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (val_or, ":flags", spf_examine_all_spawn_points),
     (try_end),

     (try_begin),
       (eq, ":is_horseman", 1),
       (val_or, ":flags", spf_is_horseman),
     (try_end),

     (try_begin),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (val_or, ":flags", spf_all_teams_are_enemy),
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (val_or, ":flags", spf_team_1_spawn_far_from_entry_66), #team 1 agents will not spawn 70 meters around of entry 0
       (val_or, ":flags", spf_team_0_walkers_spawn_at_high_points),
       (val_or, ":flags", spf_team_0_spawn_near_entry_66),
       (val_or, ":flags", spf_care_agent_to_agent_distances_less),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (val_or, ":flags", spf_team_1_spawn_far_from_entry_0), #team 1 agents will not spawn 70 meters around of entry 0
       (val_or, ":flags", spf_team_0_spawn_far_from_entry_32), #team 0 agents will not spawn 70 meters around of entry 32
       (val_or, ":flags", spf_try_to_spawn_close_to_at_least_one_enemy),
     (else_try),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (assign, ":assigned_flag_count", 0),

       (store_sub, ":maximum_moved_flag_distance", multi_headquarters_pole_height, 50), #900 - 50 = 850
       (store_mul, ":maximum_moved_flag_distance_sq", ":maximum_moved_flag_distance", ":maximum_moved_flag_distance"),
       (val_div, ":maximum_moved_flag_distance_sq", 100), #dividing 100, because fixed point multiplier is 100 and it is included twice, look above line.

       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

         (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
         (prop_instance_get_position, pos0, ":pole_id"),

         (try_begin),
           (eq, ":cur_flag_owner", 1),
           (scene_prop_get_instance, ":flag_of_team_1", "$team_1_flag_scene_prop", ":flag_no"),

           (prop_instance_get_position, pos1, ":flag_of_team_1"),
           (get_sq_distance_between_positions, ":flag_height_sq", pos0, pos1),
           (ge, ":flag_height_sq", ":maximum_moved_flag_distance_sq"),

           (set_spawn_effector_scene_prop_id, ":assigned_flag_count", ":flag_of_team_1"),
           (val_add, ":assigned_flag_count", 1),
         (else_try),
           (eq, ":cur_flag_owner", 2),
           (scene_prop_get_instance, ":flag_of_team_2", "$team_2_flag_scene_prop", ":flag_no"),

           (prop_instance_get_position, pos1, ":flag_of_team_2"),
           (get_sq_distance_between_positions, ":flag_height_sq", pos0, pos1),
           (ge, ":flag_height_sq", ":maximum_moved_flag_distance_sq"),

           (set_spawn_effector_scene_prop_id, ":assigned_flag_count", ":flag_of_team_2"),
           (val_add, ":assigned_flag_count", 1),
         (try_end),
       (try_end),
       (set_spawn_effector_scene_prop_id, ":assigned_flag_count", -1),
     (try_end),

     (multiplayer_find_spawn_point, reg0, ":team_no", ":flags"),
  ]),

  # script_multiplayer_find_spawn_point_2
  # Input: arg1 = team_no, arg2 = examine_all_spawn_points, arg3 = is_horseman
  # Output: reg0 = entry_point_no
  ("multiplayer_find_spawn_point_2",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care

     (assign, ":best_entry_point_score", -10000000),
     (assign, ":best_entry_point", 0),

     (assign, ":num_operations", 0),

     (assign, ":num_human_agents_div_3_plus_one", 0),
     (try_begin), #counting number of agents
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
       (try_for_agents, ":i_agent"),
         (agent_is_alive, ":i_agent"),
         (agent_is_human, ":i_agent"),
         (val_add, ":num_human_agents_div_3_plus_one", 1),
       (try_end),
     (try_end),

     (assign, ":num_human_agents_plus_one", ":num_human_agents_div_3_plus_one"),

     (try_begin),
       (le, ":num_human_agents_plus_one", 4),
       (assign, ":random_number_upper_limit", 2), #this is not typo-mistake this should be 2 too, not 1.
     (else_try),
       (le, ":num_human_agents_plus_one", 8),
       (assign, ":random_number_upper_limit", 2),
     (else_try),
       (le, ":num_human_agents_plus_one", 16),
       (assign, ":random_number_upper_limit", 3),
     (else_try),
       (le, ":num_human_agents_plus_one", 24),
       (assign, ":random_number_upper_limit", 4),
     (else_try),
       (le, ":num_human_agents_plus_one", 32),
       (assign, ":random_number_upper_limit", 5),
     (else_try),
       (le, ":num_human_agents_plus_one", 40),
       (assign, ":random_number_upper_limit", 6),
     (else_try),
       (assign, ":random_number_upper_limit", 7),
     (try_end),

     (val_div, ":num_human_agents_div_3_plus_one", 3),
     (val_add, ":num_human_agents_div_3_plus_one", 1),
     (store_mul, ":negative_num_human_agents_div_3_plus_one", ":num_human_agents_div_3_plus_one", -1),

     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (assign, ":random_number_upper_limit", 1),
     (try_end),

     (try_begin), #counting number of our flags and enemy flags
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (assign, ":our_flag_count", 0),
       (assign, ":enemy_flag_count", 0),
       (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
         (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
         (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
         (neq, ":cur_flag_owner", 0),
         (val_sub, ":cur_flag_owner", 1),
         (try_begin),
           (eq, ":cur_flag_owner", ":team_no"),
           (val_add, ":our_flag_count", 1),
         (else_try),
           (val_add, ":enemy_flag_count", 1),
         (try_end),
       (try_end),
     (try_end),

     (assign, ":first_agent", 0),
     (try_begin), #first spawned agents will be spawned at their base points in tdm, cf and hq mods.
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
       (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
       (try_begin),
         (eq, ":team_no", 0),
         (eq, "$g_multiplayer_team_1_first_spawn", 1),
         (assign, ":first_agent", 1),
         (assign, "$g_multiplayer_team_1_first_spawn", 0),
       (else_try),
         (eq, ":team_no", 1),
         (eq, "$g_multiplayer_team_2_first_spawn", 1),
         (assign, ":first_agent", 1),
         (assign, "$g_multiplayer_team_2_first_spawn", 0),
       (try_end),
     (try_end),

     (try_begin),
       (eq, ":first_agent", 1),
       (store_mul, ":best_entry_point", ":team_no", multi_num_valid_entry_points_div_2),
     (else_try),
       (try_for_range, ":i_entry_point", 0, multi_num_valid_entry_points),
         (assign, ":minimum_enemy_distance", 3000),
         (assign, ":second_minimum_enemy_distance", 3000),

         (assign, ":entry_point_score", 0),
         (store_random_in_range, ":random_value", 0, ":random_number_upper_limit"), #in average it is 5
         (eq, ":random_value", 0),
         (entry_point_get_position, pos0, ":i_entry_point"), #pos0 holds current entry point position
         (try_for_agents, ":i_agent"),
           (agent_is_alive, ":i_agent"),
           (agent_is_human, ":i_agent"),
           (agent_get_team, ":agent_team", ":i_agent"),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (try_begin),
               (teams_are_enemies, ":team_no", ":agent_team"),
               (assign, ":multiplier", -2),
             (else_try),
               (assign, ":multiplier", 1),
             (try_end),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
             (assign, ":multiplier", -1),
           (try_end),
           (agent_get_position, pos1, ":i_agent"),
           (get_distance_between_positions_in_meters, ":distance", pos0, pos1),
           (val_add, ":num_operations", 1),
           (try_begin),
             (try_begin), #find closest enemy soldiers
               (lt, ":multiplier", 0),
               (try_begin),
                 (lt, ":distance", ":minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":minimum_enemy_distance"),
                 (assign, ":minimum_enemy_distance", ":distance"),
               (else_try),
                 (lt, ":distance", ":second_minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":distance"),
               (try_end),
             (try_end),

             (lt, ":distance", 100),
             (try_begin), #do not spawn over or too near to another agent (limit is 2 meters, squared 4 meters)
               (lt, ":distance", 3),
               (try_begin),
                 (this_or_next|eq, ":examine_all_spawn_points", 0),
                 (this_or_next|lt, ":multiplier", 0), #new added 20.08.08
                 (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
                 (try_begin),
                   (lt, ":distance", 1),
                   (assign, ":dist_point", -1000000), #never place
                 (else_try),
                   (lt, ":distance", 2),
                   (try_begin),
                     (lt, ":multiplier", 0),
                     (assign, ":dist_point", -20000),
                   (else_try),
                     (assign, ":dist_point", -2000), #can place, friend and distance is between 1-2 meters
                   (try_end),
                 (else_try),
                   (try_begin),
                     (lt, ":multiplier", 0),
                     (assign, ":dist_point", -10000),
                   (else_try),
                     (assign, ":dist_point", -1000), #can place, friend and distance is between 2-3 meters
                   (try_end),
                 (try_end),
               (else_try),
                 #if examinining all spawn points and mod is siege only. This happens in new round start placings.
                 (try_begin),
                   (lt, ":distance", 1),
                   (assign, ":dist_point", -20000), #very hard to place distance is < 1 meter
                 (else_try),
                   (lt, ":distance", 2),
                   (assign, ":dist_point", -2000),
                 (else_try),
                   (assign, ":dist_point", -1000), #can place, distance is between 2-3 meters
                 (try_end),
               (try_end),

               (val_mul, ":dist_point", ":num_human_agents_div_3_plus_one"),
             (else_try),
               (assign, ":dist_point", 0),
               (this_or_next|neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
               (this_or_next|lt, ":multiplier", 0),
               (eq, ":team_no", 1), #only attackers are effected by positive enemy & friend distance at siege mod, defenders only get negative score effect a bit

               (try_begin), #in siege give no positive or negative score to > 40m distance. (6400 = 10000 - 3600(60 * 60))
                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #new added after moving below part to above
                 (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #new added after moving below part to above
                 (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #new added after moving below part to above

                 (store_sub, ":dist_point", multiplayer_spawn_min_enemy_dist_limit, ":distance"), #up to 40 meters give (positive(if friend) or negative(if enemy)) points
                 (val_max, ":dist_point", 0),
                 (val_mul, ":dist_point", ":dist_point"),
               (else_try),
                 (store_mul, ":one_and_half_limit", multiplayer_spawn_min_enemy_dist_limit, 3),
                 (val_div, ":one_and_half_limit", 2),
                 (store_sub, ":dist_point", ":one_and_half_limit", ":distance"), #up to 60 meters give (positive(if friend) or negative(if enemy)) points
                 (val_mul, ":dist_point", ":dist_point"),
               (try_end),

               (val_mul, ":dist_point", ":multiplier"),
             (try_end),
             (val_add, ":entry_point_score", ":dist_point"),
           (try_end),
         (try_end),

         (try_begin),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
           (store_mul, ":max_enabled_agent_distance_score", 1000, ":num_human_agents_div_3_plus_one"),
           (ge, ":entry_point_score", ":max_enabled_agent_distance_score"),
           (assign, ":entry_point_score", ":max_enabled_agent_distance_score"),
         (try_end),

         (try_begin),
           (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

           #(assign, ":minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, ":second_minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, reg2, ":minimum_enemy_distance"), #close also these with displays
           #(assign, reg3, ":second_minimum_enemy_distance"), #close also these with displays

           (try_begin), #if minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":minimum_enemy_distance", 3000),
             (try_begin),
               (gt, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":minimum_enemy_dist_score", ":minimum_enemy_distance", -50),
               (val_mul, ":minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":minimum_enemy_dist_score"),
             (try_end),
           (try_end),

           (try_begin), #if second minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":second_minimum_enemy_distance", 3000), #3000 x 3000
             (try_begin),
               (gt, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":second_minimum_enemy_dist_score", ":second_minimum_enemy_distance", -50),
               (val_mul, ":second_minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":second_minimum_enemy_dist_score"),
             (try_end),
           (try_end),

           #(assign, reg0, ":minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(assign, reg1, ":second_minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(display_message, "@{!}minimum enemy distance : {reg2}, score : {reg0}"), #close also above assignment lines with these displays
           #(display_message, "@{!}second minimum enemy distance : {reg3}, score : {reg1}"), #close also above assignment lines with these displays
         (try_end),

         (try_begin), #giving positive points for "distance of entry point position to ground" while searching for entry point for defender team
           (neq, ":is_horseman", -1), #if being horseman or rider is not (not important)

           #additional score to entry points which has distance to ground value of > 0 meters
           (position_get_distance_to_terrain, ":height_to_terrain", pos0),
           (val_max, ":height_to_terrain", 0),
           (val_min, ":height_to_terrain", 300),
           (ge, ":height_to_terrain", 40),

           (store_mul, ":height_to_terrain_score", ":height_to_terrain", ":num_human_agents_div_3_plus_one"), #it was 8

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
             (val_mul, ":height_to_terrain_score", 16),
           (else_try),
             (val_mul, ":height_to_terrain_score", 4),
           (try_end),

           (try_begin),
             (eq, ":is_horseman", 0),
             (try_begin),
               (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #but only in siege mod, defender infantries will get positive points for spawning in high places.
               (eq, ":team_no", 0),
               (val_add, ":entry_point_score", ":height_to_terrain_score"),
             (try_end),
           (else_try),
             (val_mul, ":height_to_terrain_score", 5),
             (val_sub, ":entry_point_score", ":height_to_terrain_score"),
           (try_end),
         (try_end),

         (try_begin), #additional random entry point score at deathmatch, teamdethmatch, capture the flag and siege
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
           (try_begin),
             (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (store_random_in_range, ":random_value", 0, 400),

             (try_begin),
               (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
               (val_mul, ":random_value", 5),
             (try_end),
           (else_try),
             (eq, ":team_no", 1),
             (store_random_in_range, ":random_value", 0, 600), #siege-attacker
           (else_try),
             (store_random_in_range, ":random_value", 0, 200), #siege-defender
           (try_end),
           (val_mul, ":random_value", ":num_human_agents_div_3_plus_one"),
           (val_add, ":entry_point_score", ":random_value"),
         (try_end),

         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
             (try_begin),
               (eq, ":team_no", 0),
               (entry_point_get_position, pos1, multi_base_point_team_1), #our base is at pos1
               (entry_point_get_position, pos2, multi_base_point_team_2), #enemy base is at pos2
             (else_try),
               (entry_point_get_position, pos1, multi_base_point_team_2), #our base is at pos2
               (entry_point_get_position, pos2, multi_base_point_team_1), #enemy base is at pos1
             (try_end),
           (else_try),
             (try_begin), #siege
               (eq, ":team_no", 0),
               (entry_point_get_position, pos1, multi_siege_flag_point), #our base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
               (entry_point_get_position, pos2, multi_initial_spawn_point_team_2), #enemy base is at pos2
             (else_try),
               (entry_point_get_position, pos1, multi_initial_spawn_point_team_2), #our base is at pos2
               (entry_point_get_position, pos2, multi_siege_flag_point), #enemy base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
             (try_end),
           (try_end),

           (try_begin),
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (position_get_z, ":pos0_z", pos0),
             (position_set_z, pos1, ":pos0_z"), #make z of our base same with entry point position z
             (position_set_z, pos2, ":pos0_z"), #make z of enemy base same with entry point position z
           (try_end),

           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_our_base", pos0, pos1),
           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_enemy_base", pos0, pos2),
           (get_distance_between_positions_in_meters, ":dist_to_enemy_base", pos0, pos2),

           #give positive points if this entry point is near to our base.
           (assign, ":dist_to_our_base_point", 0),
           (try_begin), #capture the flag (points for being near to base)
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),

             (get_distance_between_positions_in_meters, ":dist_to_our_base", pos0, pos1),
             (lt, ":dist_to_our_base", 100),
             (store_sub, ":dist_to_our_base_point", 100, ":dist_to_our_base"),

             (try_begin), #assign all 75-100's to 75
               (gt, ":dist_to_our_base_point", 75),
               (assign, ":dist_to_our_base_point", 75),
             (try_end),

             (val_mul, ":dist_to_our_base_point", 50), #0..5000 (increase is linear)

             (val_mul, ":dist_to_our_base_point", ":num_human_agents_div_3_plus_one"),
           (else_try), #siege (points for being near to base)
             (lt, ":sq_dist_to_our_base", 10000), #in siege give entry points score until 100m distance is reached
             (try_begin),
               (eq, ":team_no", 0),
               (try_begin),
                 (lt, ":sq_dist_to_our_base", 2500), #if distance is < 50m in siege give all highest point possible
                 (assign, ":sq_dist_to_our_base", 0),
               (else_try),
                 (val_sub, ":sq_dist_to_our_base", 2500),
                 (val_mul, ":sq_dist_to_our_base", 2),
               (try_end),
             (try_end),

             (store_sub, ":dist_to_our_base_point", 10000, ":sq_dist_to_our_base"),

             #can be (10000 - (10000 - 2500) * 2) = -5000 (for only defenders) so we are adding this loss.
             (val_add, ":dist_to_our_base_point", 5000), #so score getting from being near to base changes between 0 to 15000

             (try_begin),
               (eq, ":team_no", 0),
             (else_try), #in siege mod for attackers being near to base entry point has 45 times less importance
               (val_div, ":dist_to_our_base_point", 45),
             (try_end),
             (val_mul, ":dist_to_our_base_point", ":num_human_agents_div_3_plus_one"),
           (try_end),

           (val_add, ":entry_point_score", ":dist_to_our_base_point"),


           #give negative points if this entry point is near to enemy base.
           (assign, ":dist_to_enemy_base_point", 0),
           (try_begin), #capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),

             (lt, ":dist_to_enemy_base", 150),
             (store_sub, ":dist_to_enemy_base_point", 150, ":dist_to_enemy_base"),

             (try_begin), #assign 150 to 150 + (150 - 50) * 2 = 350, assign 100 to 100 + (100 - 50) * 2 = 200
               (gt, ":dist_to_enemy_base_point", 50),
               (store_sub, ":dist_to_enemy_base_point_minus_50", ":dist_to_enemy_base_point", 50),
               (val_mul, ":dist_to_enemy_base_point_minus_50", 2),
               (val_add, ":dist_to_enemy_base_point", ":dist_to_enemy_base_point_minus_50"),
             (try_end),

             (val_mul, ":dist_to_enemy_base_point", -50), #-7500(with extras 350 * 50 = -17500)..0 (increase is linear)

             (val_mul, ":dist_to_enemy_base_point", ":num_human_agents_div_3_plus_one"),
           (else_try),
             (this_or_next|neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
             (eq, ":team_no", 1),

             (assign, ":dist_to_enemy_base_point", 0),

             (try_begin),
               (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

               (try_begin),
                 (lt, ":sq_dist_to_enemy_base", 10000),
                 (store_sub, ":dist_to_enemy_base_point", 10000, ":sq_dist_to_enemy_base"),
                 (val_div, ":dist_to_enemy_base_point", 4),
                 (val_mul, ":dist_to_enemy_base_point", ":negative_num_human_agents_div_3_plus_one"),
               (try_end),
             (else_try),
               (val_max, ":dist_to_enemy_base", 60), #<60 meters has all most negative score

               (try_begin),
                 (eq, ":is_horseman", 1),
                 (assign, ":optimal_distance", 120),
               (else_try),
                 (assign, ":optimal_distance", 80),
               (try_end),

               (try_begin),
                 (le, ":dist_to_enemy_base", ":optimal_distance"),
                 (store_sub, ":dist_to_enemy_base_point", ":optimal_distance", ":dist_to_enemy_base"),
                 (val_mul, ":dist_to_enemy_base_point", 180), #-3600 max
               (else_try),
                 (store_sub, ":dist_to_enemy_base_point", ":dist_to_enemy_base", ":optimal_distance"),
                 (val_mul, ":dist_to_enemy_base_point", 30), #-unlimited max but lower slope
               (try_end),

               (val_sub, ":dist_to_enemy_base_point", 600),
               (val_max, ":dist_to_enemy_base_point", 0),

               (val_mul, ":dist_to_enemy_base_point", ":negative_num_human_agents_div_3_plus_one"),
             (try_end),
           (try_end),

           (val_add, ":entry_point_score", ":dist_to_enemy_base_point"),
         (else_try),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),

           (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
             (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
             (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
             (neq, ":cur_flag_owner", 0),
             (val_sub, ":cur_flag_owner", 1),

             (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
             (prop_instance_get_position, pos1, ":pole_id"), #pos1 holds pole position.

             (get_sq_distance_between_positions_in_meters, ":sq_dist_to_cur_pole", pos0, pos1),
             (lt, ":sq_dist_to_cur_pole", 6400),

             (try_begin),
               (eq, ":cur_flag_owner", ":team_no"),
               (store_sub, ":dist_to_flag_point", 6400, ":sq_dist_to_cur_pole"), #up to 80 meters give positive points if entry point is near our base
               (val_mul, ":dist_to_flag_point", 2),
               (val_div, ":dist_to_flag_point", ":our_flag_count"),
               (val_mul, ":dist_to_flag_point", ":num_human_agents_div_3_plus_one"),
             (else_try),
               (store_sub, ":dist_to_flag_point", 6400, ":sq_dist_to_cur_pole"), #up to 80 meters give negative points if entry point is near enemy base
               (val_mul, ":dist_to_flag_point", 2),
               (val_div, ":dist_to_flag_point", ":enemy_flag_count"),
               (val_mul, ":dist_to_flag_point", ":negative_num_human_agents_div_3_plus_one"),
             (try_end),
             (val_add, ":entry_point_score", ":dist_to_flag_point"),
           (try_end),
         (try_end),

         #(assign, reg1, ":i_entry_point"),
         #(assign, reg2, ":entry_point_score"),
         #(display_message, "@{!}entry_no : {reg1} , entry_score : {reg2}"),

         (gt, ":entry_point_score", ":best_entry_point_score"),
         (assign, ":best_entry_point_score", ":entry_point_score"),
         (assign, ":best_entry_point", ":i_entry_point"),
       (try_end),

       #(assign, reg0, ":best_entry_point"),
       #(assign, reg1, ":best_entry_point_score"),
       #(assign, reg2, ":num_operations"),
       #(assign, reg7, ":is_horseman"),
       #(display_message, "@{!},is horse:{reg7}, best entry:{reg0}, best entry score:{reg1}, num_operations:{reg2}"),
     (try_end),
     (assign, reg0, ":best_entry_point"),
     ]),

  #script_multiplayer_buy_agent_equipment
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_buy_agent_equipment",
   [
     (store_script_param, ":player_no", 1),
     (player_get_troop_id, ":player_troop", ":player_no"),
     (player_get_gold, ":player_gold", ":player_no"),
     (player_get_slot, ":added_gold", ":player_no", slot_player_last_rounds_used_item_earnings),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (val_add, ":player_gold", ":added_gold"),
     (assign, ":armor_bought", 0),

     #moving original values to temp slots
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":selected_item_index", ":player_no", ":i_item"),
       (store_sub, ":i_cur_selected_item", ":i_item", slot_player_selected_item_indices_begin),
       (try_begin),
         (player_item_slot_is_picked_up, ":player_no", ":i_cur_selected_item"),
         (assign, ":selected_item_index", -1),
       (try_end),
       (val_add, ":i_cur_selected_item", slot_player_cur_selected_item_indices_begin),
       (player_set_slot, ":player_no", ":i_cur_selected_item", ":selected_item_index"),
     (try_end),
     (assign, ":end_cond", 1000),
     (try_for_range, ":unused", 0, ":end_cond"),
       (call_script, "script_multiplayer_calculate_cur_selected_items_cost", ":player_no", 0),
       (assign, ":total_cost", reg0),
       (try_begin),
         (gt, ":total_cost", ":player_gold"),
         #downgrade one of the selected items
         #first normalize the prices
         #then prioritize some of the weapon classes for specific troop classes
         (call_script, "script_multiplayer_get_troop_class", ":player_troop"),
         (assign, ":player_troop_class", reg0),

         (assign, ":max_cost_value", 0),
         (assign, ":max_cost_value_index", -1),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           (ge, ":item_id", 0), #might be -1 for horses etc.
           (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":player_troop"),
           (assign, ":item_value", reg0),
           (store_sub, ":item_type", ":i_item", slot_player_cur_selected_item_indices_begin),
           (try_begin), #items
             (this_or_next|eq, ":item_type", 0),
             (this_or_next|eq, ":item_type", 1),
             (this_or_next|eq, ":item_type", 2),
             (eq, ":item_type", 3),
             (val_mul, ":item_value", 5),
           (else_try), #head
             (eq, ":item_type", 4),
             (val_mul, ":item_value", 4),
           (else_try), #body
             (eq, ":item_type", 5),
             (val_mul, ":item_value", 2),
           (else_try), #foot
             (eq, ":item_type", 6),
             (val_mul, ":item_value", 8),
           (else_try), #gloves
             (eq, ":item_type", 7),
             (val_mul, ":item_value", 8),
           (else_try), #horse
             #base value (most expensive)
           (try_end),
           (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
           (try_begin),
             (eq, ":player_troop_class", multi_troop_class_infantry),
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_axe),
             (this_or_next|eq, ":item_class", multi_item_class_type_blunt),
             (this_or_next|eq, ":item_class", multi_item_class_type_war_picks),
             (this_or_next|eq, ":item_class", multi_item_class_type_two_handed_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_small_shield),
             (eq, ":item_class", multi_item_class_type_two_handed_axe),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_spearman),
             (this_or_next|eq, ":item_class", multi_item_class_type_spear),
             (eq, ":item_class", multi_item_class_type_large_shield),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_cavalry),
             (this_or_next|eq, ":item_class", multi_item_class_type_lance),
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_archer),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (eq, ":item_class", multi_item_class_type_arrow),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_crossbowman),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (eq, ":item_class", multi_item_class_type_bolt),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_mounted_archer),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (this_or_next|eq, ":item_class", multi_item_class_type_arrow),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_mounted_crossbowman),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (this_or_next|eq, ":item_class", multi_item_class_type_bolt),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (try_end),

           (try_begin),
             (gt, ":item_value", ":max_cost_value"),
             (assign, ":max_cost_value", ":item_value"),
             (assign, ":max_cost_value_index", ":i_item"),
           (try_end),
         (try_end),

         #max_cost_value and max_cost_value_index will definitely be valid
         #unless no items are left (therefore some items must cost 0 gold)
         (player_get_slot, ":item_id", ":player_no", ":max_cost_value_index"),
         (call_script, "script_multiplayer_get_previous_item_for_item_and_troop", ":item_id", ":player_troop"),
         (assign, ":item_id", reg0),
         (player_set_slot, ":player_no", ":max_cost_value_index", ":item_id"),
       (else_try),
         (assign, ":end_cond", 0),
         (val_sub, ":player_gold", ":total_cost"),
         (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           #checking if different class default item replace is needed for weapons
           (try_begin),
             (ge, ":item_id", 0),
             #then do nothing
           (else_try),
             (store_sub, ":base_index_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (store_add, ":selected_item_index_slot", ":base_index_slot", slot_player_selected_item_indices_begin),
             (player_get_slot, ":selected_item_index", ":player_no", ":selected_item_index_slot"),
             (this_or_next|eq, ":selected_item_index", -1),
             (player_item_slot_is_picked_up, ":player_no", ":base_index_slot"),
             #then do nothing
           (else_try),
             #an item class without a default value is -1, then find a default weapon
             (item_get_slot, ":item_class", ":selected_item_index", slot_item_multiplayer_item_class),
             (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
             (assign, ":dc_replaced_item", -1),
             (try_for_range, ":i_dc_item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
               (lt, ":dc_replaced_item", 0),
               (assign, ":dc_item_class_used", 0),
               (try_for_range, ":i_dc_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
                 (player_get_slot, ":dc_cur_item", ":player_no", ":i_dc_item"),
                 (ge, ":dc_cur_item", 0),
                 (item_get_slot, ":dc_item_class", ":dc_cur_item", slot_item_multiplayer_item_class),
                 (eq, ":dc_item_class", ":i_dc_item_class"),
                 (assign, ":dc_item_class_used", 1),
               (try_end),
               (eq, ":dc_item_class_used", 0),
               (assign, ":dc_end_cond", all_items_end),
               (try_for_range, ":i_dc_new_item", all_items_begin, ":dc_end_cond"),
                 (item_slot_eq, ":i_dc_new_item", slot_item_multiplayer_item_class, ":i_dc_item_class"),
                 (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_dc_new_item", ":player_troop"),
                 (assign, ":dc_end_cond", 0), #break
                 (assign, ":dc_replaced_item", ":i_dc_new_item"),
               (try_end),
             (try_end),
             (ge, ":dc_replaced_item", 0),
             (player_set_slot, ":player_no", ":i_item", ":dc_replaced_item"),
             (assign, ":item_id", ":dc_replaced_item"),
           (try_end),

           #finally, add the item to agent
           (try_begin),
             (ge, ":item_id", 0), #might be -1 for horses etc.
             (store_sub, ":item_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (player_add_spawn_item, ":player_no", ":item_slot", ":item_id"),
             (try_begin),
               (eq, ":item_slot", ek_body), #ek_body is the slot for armor
               (assign, ":armor_bought", 1),
             (try_end),
           (try_end),
         (try_end),

         (player_set_slot, ":player_no", slot_player_total_equipment_value, ":total_cost"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":armor_bought", 0),
       (eq, "$g_multiplayer_force_default_armor", 1),
       (assign, ":end_cond", all_items_end),
       (try_for_range, ":i_new_item", all_items_begin, ":end_cond"),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_medium_armor),
         (item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_heavy_armor),
         (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_new_item", ":player_troop"),
         (assign, ":end_cond", 0), #break
         (player_add_spawn_item, ":player_no", ek_body, ":i_new_item"), #ek_body is the slot for armor
       (try_end),
     (try_end),
     ]),

  # script_party_get_ideal_size @used for NPC parties.
("done_skin_multiplayer",
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(agent_is_active, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_item_slot, ":body_armor", ":agent_no", ek_body),
			(eq, ":body_armor", -1),
			(agent_equip_item, ":agent_no", "itm_loincloth"), # man also equip - troop_type always 0 - "is_female" not working
		(try_end),
	]
  ),

  ]
