# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

order_attack_2_menu = [
(
    "order_attack_2",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Enemy casualties: {s9}",
    "none",
    [
      (set_background_mesh, "mesh_pic_charge"),

      (call_script, "script_party_calculate_strength", "p_main_party", 1), #exclude player
      (assign, ":player_party_strength", reg0),

      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, ":enemy_party_strength", reg0),

      (party_collect_attachments_to_party, "p_main_party", "p_collective_ally"),
      (call_script, "script_party_calculate_strength", "p_collective_ally", 1), #exclude player
      (assign, ":total_player_and_followers_strength", reg0),

      (try_begin),
        (le, ":total_player_and_followers_strength", ":enemy_party_strength"),
        (assign, ":minimum_power", ":total_player_and_followers_strength"),
      (else_try),
        (assign, ":minimum_power", ":enemy_party_strength"),
      (try_end),

      (try_begin),
        (le, ":minimum_power", 25),
        (assign, ":division_constant", 1),
      (else_try),
        (le, ":minimum_power", 50),
        (assign, ":division_constant", 2),
      (else_try),
        (le, ":minimum_power", 75),
        (assign, ":division_constant", 3),
      (else_try),
        (le, ":minimum_power", 125),
        (assign, ":division_constant", 4),
      (else_try),
        (le, ":minimum_power", 200),
        (assign, ":division_constant", 5),
      (else_try),
        (le, ":minimum_power", 400),
        (assign, ":division_constant", 6),
      (else_try),
        (le, ":minimum_power", 800),
        (assign, ":division_constant", 7),
      (else_try),
        (le, ":minimum_power", 1600),
        (assign, ":division_constant", 8),
      (else_try),
        (le, ":minimum_power", 3200),
        (assign, ":division_constant", 9),
      (else_try),
        (le, ":minimum_power", 6400),
        (assign, ":division_constant", 10),
      (else_try),
        (le, ":minimum_power", 12800),
        (assign, ":division_constant", 11),
      (else_try),
        (le, ":minimum_power", 25600),
        (assign, ":division_constant", 12),
      (else_try),
        (le, ":minimum_power", 51200),
        (assign, ":division_constant", 13),
      (else_try),
        (le, ":minimum_power", 102400),
        (assign, ":division_constant", 14),
      (else_try),
        (assign, ":division_constant", 15),
      (try_end),

      (val_div, ":player_party_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":player_party_strength", 1), #1.126
      (val_div, ":enemy_party_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":enemy_party_strength", 1), #1.126
      (val_div, ":total_player_and_followers_strength", ":division_constant"), #1.126, ":division_constant" was 5 before
      (val_max, ":total_player_and_followers_strength", 1), #1.126

      (store_mul, "$g_strength_contribution_of_player", ":player_party_strength", 100),
      (val_div, "$g_strength_contribution_of_player", ":total_player_and_followers_strength"),

      (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
      (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
      (str_store_string_reg, s8, s0),

      (try_begin),
        (ge, "$g_ally_party", 0),
        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (str_store_string_reg, s8, s0),
      (try_end),

      (inflict_casualties_to_party_group, "$g_encountered_party", ":total_player_and_followers_strength", "p_temp_casualties"),

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
      (str_store_string_reg, s9, s0),

      (party_collect_attachments_to_party, "$g_encountered_party", "p_collective_enemy"),
      (assign, "$no_soldiers_left", 0),
      (try_begin),
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),
        (assign, ":num_our_regulars_remaining", reg0),
        (store_add, ":num_routed_us_plus_one", "$num_routed_us", 1),
        (le, ":num_our_regulars_remaining", ":num_routed_us_plus_one"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_order_attack_failure"),
      (else_try),
        (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
        (assign, ":num_enemy_regulars_remaining", reg0),
        (this_or_next|le, ":num_enemy_regulars_remaining", 0),
        (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.
        (assign, ":continue", 0),
        (party_get_num_companion_stacks, ":party_num_stacks", "p_collective_enemy"),
        (try_begin),
          (eq, ":party_num_stacks", 0),
          (assign, ":continue", 1),
        (else_try),
          (party_stack_get_troop_id, ":party_leader", "p_collective_enemy", 0),
          (try_begin),
            (neg|troop_is_hero, ":party_leader"),
            (assign, ":continue", 1),
          (else_try),
            (troop_is_wounded, ":party_leader"),
            (assign, ":continue", 1),
          (try_end),
        (try_end),
        (eq, ":continue", 1),
        (assign, "$g_battle_result", 1),
        (assign, "$no_soldiers_left", 1),
        (str_store_string, s4, "str_order_attack_success"),
      (else_try),
      (str_store_string, s4, "str_order_attack_continue"),
    (try_end),
    ],
    [
      ("order_attack_continue",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to continue the attack.",[
          (jump_to_menu,"mnu_order_attack_2"),
          ]),
      ("order_retreat",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
      ("continue",[(eq, "$no_soldiers_left", 1)],"Continue...",[
          (jump_to_menu,"mnu_simple_encounter"),
          ]),
    ]
  )
]
