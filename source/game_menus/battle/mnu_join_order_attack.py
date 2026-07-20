# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

join_order_attack_menu = [
(
    "join_order_attack",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
      (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
      (assign, ":player_party_strength", reg0),
      (val_div, ":player_party_strength", 5),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, ":friend_party_strength", reg0),
      (val_div, ":friend_party_strength", 5),

      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),
      (val_div, ":enemy_party_strength", 5),

      (try_begin),
        (eq, ":friend_party_strength", 0),
        (store_div, ":enemy_party_strength_for_p", ":enemy_party_strength", 2),
      (else_try),
        (assign, ":enemy_party_strength_for_p", ":enemy_party_strength"),
        (val_mul, ":enemy_party_strength_for_p", ":player_party_strength"),
        (val_div, ":enemy_party_strength_for_p", ":friend_party_strength"),
      (try_end),

      (val_sub, ":enemy_party_strength", ":enemy_party_strength_for_p"),
      (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength_for_p", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),

      (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),

      #ozan begin
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
        (try_begin),
          (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
          (gt, ":stack_size", 0),
          (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
          (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),
          (gt, ":stack_wounded_size", 0),
          (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
        (try_end),
      (try_end),
      #ozan end

      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s10, s0),

      (call_script, "script_collect_friendly_parties"),
      #(party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

      (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s9, s0),
      (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

       #(assign, "$cant_leave_encounter", 0),
       (assign, "$no_soldiers_left", 0),
       (try_begin),
         (call_script, "script_party_count_members_with_full_health","p_main_party"),
         (assign, ":num_our_regulars_remaining", reg0),

         #(le, ":num_our_regulars_remaining", 0),
         (le, ":num_our_regulars_remaining", "$num_routed_us"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

         (assign, "$no_soldiers_left", 1),
         (str_store_string, s4, "str_join_order_attack_failure"),
       (else_try),
         (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
         (assign, ":num_enemy_regulars_remaining", reg0),

         (this_or_next|le, ":num_enemy_regulars_remaining", 0),
         (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

         (assign, "$g_battle_result", 1),
         (assign, "$no_soldiers_left", 1),
         (str_store_string, s4, "str_join_order_attack_success"),
       (else_try),
         (str_store_string, s4, "str_join_order_attack_continue"),
       (try_end),
    ],
    [
      ("continue",[],"Continue...",
      [
        (jump_to_menu,"mnu_join_battle"),
      ]),
    ]
  )
]
