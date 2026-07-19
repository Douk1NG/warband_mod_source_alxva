# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

join_battle_menu = [
(#SB : pic hotkeys
    "join_battle",mnf_enable_hot_keys,
    "You are helping the {s2} against the {s1}. You have {reg10} troops fit for battle against the enemy's {reg11}.",
    "none",
    [
        (str_store_party_name, 1,"$g_enemy_party"),
        (str_store_party_name, 2,"$g_ally_party"),

        (call_script, "script_encounter_calculate_fit"),

        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (call_script, "script_encounter_init_variables"),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished",0),
          (try_begin),
            (eq, "$g_battle_result", 1),

            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
            (le, ":num_enemy_regulars_remaining", "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle",0),
            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),

          (this_or_next|eq, ":enemy_finished",1),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":num_ally_regulars_remaining", reg0),
          (assign, ":battle_lost", 0),
          (try_begin),
            (eq, "$g_battle_result", -1),

            #(eq, ":num_ally_regulars_remaining", 0), #battle lost
            (le, ":num_ally_regulars_remaining",  "$num_routed_allies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign, ":battle_lost",1),
          (try_end),

          (this_or_next|eq, ":battle_lost",1),
          (eq,"$g_player_surrenders",1),
          (leave_encounter),
          (change_screen_return),
        (try_end),
      ],
    [
      ("toggle_weapons",
        [
          (call_script, "script_get_num_heroes_of_party", "p_main_party", 0),
          (assign, ":num_of_heroes", reg0),
          (gt, ":num_of_heroes", 1),
          (try_begin),
            (eq, "$g_weapons_set_no", 0),
            (assign, reg1, 2),
          (else_try),
            (assign, reg1, 1),
          (try_end),
        ],
        "Toggle weapons to set {reg1} for heroes.",
        [
          (val_add, "$g_weapons_set_no", 1),
          (val_mod, "$g_weapons_set_no", 2),
          (call_script, "script_all_toggle_weapons_set", 0),
        ]),

      ("join_attack",
      [
        (neg|troop_is_wounded, "trp_player"),
      ],
      "Charge the enemy.",
      [
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (assign, "$g_battle_result", 0),

        #(assign, "$player_deploy_troops", 1),

        (call_script, "script_calculate_renown_value"),
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),

        (try_begin), #ships
          (party_get_slot, ":ship_type", "$g_ally_party", slot_party_ship_type),
          (party_get_slot, ":enemy_ship_type", "$g_enemy_party", slot_party_ship_type),
          (gt, ":ship_type", 0),
          (gt, ":enemy_ship_type", 0),
          #(set_jump_mission,"mt_ship_battle"),
          (call_script, "script_setup_random_scene"),
        (else_try),
        (set_jump_mission,"mt_lead_charge"),
        (call_script, "script_setup_random_scene"),
        (try_end),
        (assign, "$g_next_menu", "mnu_join_battle"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),

      ("join_order_attack",
      [
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),
        (ge, reg0, 3),
      ],
      "Order your troops to attack with your allies while you stay back.",
      [
        (assign, "$g_joined_battle_to_help", 1),
        (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
        (jump_to_menu,"mnu_join_order_attack"),
      ]),

      ("join_leave",[],"Leave.",
      [
        (try_begin),
           (neg|troop_is_wounded, "trp_player"),
           (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
           (party_stack_get_troop_id, ":enemy_leader","$g_enemy_party",0),
		   (is_between, ":enemy_leader", active_npcs_begin, active_npcs_end),
           (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":enemy_leader", -1),
        (try_end),

        (leave_encounter),(change_screen_return)]),
      ])
]
