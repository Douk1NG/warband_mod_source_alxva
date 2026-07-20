# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

castle_attack_walls_with_allies_simulate_menu = [
(
    "castle_attack_walls_with_allies_simulate",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
        (try_begin),
          (set_background_mesh, "mesh_pic_siege_attack"),
        (try_end),
        ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+
        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),
        (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
        (assign, ":friend_party_strength", reg0),
        (val_div, ":friend_party_strength", 10),

        (val_max, ":friend_party_strength", 1),

        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

##        (assign, reg0, ":player_party_strength"),
##        (assign, reg1, ":friend_party_strength"),
##        (assign, reg2, ":enemy_party_strength"),
##        (assign, reg3, "$g_enemy_party"),
##        (assign, reg4, "$g_ally_party"),
##        (display_message, "@{!}player_str={reg0} friend_str={reg1} enemy_str={reg2}"),
##        (display_message, "@{!}enemy_party={reg3} ally_party={reg4}"),

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
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),

        (call_script, "script_collect_friendly_parties"),

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_us)
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (le, reg0, 0), #(TODO : compare with num_routed_enemies)
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
		###diplomacy start+
		##Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		###diplomacy end+
     ],
    [
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_besiegers_camp_with_allies")]),
    ]
  )
]
