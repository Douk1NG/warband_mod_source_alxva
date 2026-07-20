# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

siege_started_defender_menu = [
( #SB : pic hotkeys
    "siege_started_defender",mnf_enable_hot_keys,
    "{s1} is launching an assault against the walls of {s2}. You have {reg10} troops fit for battle against the enemy's {reg11}. You decide to...",
    "none",
    [
        (select_enemy,1),
        (assign, "$g_enemy_party", "$g_encountered_party_2"),
        (assign, "$g_ally_party", "$g_encountered_party"),
        (str_store_party_name, s1, "$g_enemy_party"),
        (str_store_party_name, s2, "$g_ally_party"),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$g_siege_first_encounter", 1),
          (call_script, "script_let_nearby_parties_join_current_battle", 0, 1),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage settings
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplmacy end+
        (try_end),

        (try_begin),
          (eq, "$g_siege_first_encounter", 0),
          (try_begin),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (assign, ":num_enemy_regulars_remaining", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
            (assign, ":num_ally_regulars_remaining", reg0),
            (assign, ":enemy_finished", 0),
            (try_begin),
              (eq, "$g_battle_result", 1),
              (eq, ":num_enemy_regulars_remaining", 0), #battle won (TODO : compare with num_routed_us)
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
            (assign, ":battle_lost", 0),
            (try_begin),
              (this_or_next|eq, "$g_battle_result", -1),
              (troop_is_wounded,  "trp_player"),
              (eq, ":num_ally_regulars_remaining", 0), #(TODO : compare with num_routed_allies)
              (assign, ":battle_lost",1),
            (try_end),
            (this_or_next|eq, ":battle_lost",1),
            (eq,"$g_player_surrenders",1),
            (assign, "$g_next_menu", "mnu_captivity_start_under_siege_defeat"),
            (jump_to_menu, "mnu_total_defeat"),
          (else_try),
            # Ordinary victory/defeat.
            (assign, ":attackers_retreat", 0),
            (try_begin),
            #check whether enemy retreats
              (eq, "$g_battle_result", 1),
  ##            (store_mul, ":min_enemy_str", "$g_enemy_fit_for_battle", 2),
  ##            (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try), #fix this
              (eq, "$g_battle_result", 0),
              (store_div, ":min_enemy_str", "$g_enemy_fit_for_battle", 3),
              (lt, ":min_enemy_str", "$g_friend_fit_for_battle"),
              (assign, ":attackers_retreat", 1),
            (else_try),
              (store_random_in_range, ":random_no", 0, 100),
              (store_mul, ":num_ally_regulars_remaining_multiplied", ":num_ally_regulars_remaining", 13),
              (val_div, ":num_ally_regulars_remaining_multiplied", 10),
              (ge, ":num_ally_regulars_remaining_multiplied", ":num_enemy_regulars_remaining"),
              (lt, ":random_no", 10),
              (neq, "$new_encounter", 1),
              (assign, ":attackers_retreat", 1),
            (try_end),
            (try_begin),
              (eq, ":attackers_retreat", 1),
              (party_get_slot, ":siege_hardness", "$g_encountered_party", slot_center_siege_hardness),
              (val_add, ":siege_hardness", 100),
              (party_set_slot, "$g_encountered_party", slot_center_siege_hardness, ":siege_hardness"),
              (party_set_slot, "$g_enemy_party", slot_party_retreat_flag, 1),

              (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
                #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
                (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
                (gt, ":party_no", 0),
                (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
                (party_slot_eq, ":party_no", slot_party_ai_object, "$g_encountered_party"),
                (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
                (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, "$g_encountered_party"),
              (try_end),
              (display_message, "@The enemy has been forced to retreat. The assault is over, but the siege continues."),
              (assign, "$g_battle_simulation_cancel_for_party", "$g_encountered_party"),
              (leave_encounter),
              (change_screen_return),
              (assign, "$g_battle_simulation_auto_enter_town_after_battle", "$g_encountered_party"),
            (try_end),
          (try_end),
        (try_end),
        # (assign, "$g_siege_first_encounter", 0), #dckplmc - moved this down
        # (assign, "$new_encounter", 0),
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

      ("siege_defender_castle",
      [

        #SB : some gender string tweaks
        (try_begin),
          (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
          (lt, ":town_lord", 0),
          (assign, reg4, 0), #default to lord
        (else_try),
          (call_script, "script_dplmc_store_troop_is_female_reg", ":town_lord", 4),
        (try_end),
        #possibly replace "the" with "your"
        ],"Go to the {reg4?Lady:Lord}'s hall.",
       [
             (call_script, "script_enter_court", "$current_town"),
        ], "Door to the castle."),

      #SB : add garrison management, maybe penalties if player disbands prisoners
      ("siege_defender_manage_troops",[
        (assign, ":player_can_draw_from_garrison", 0),
        (str_clear, s10),
        (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),

        (store_party_size_wo_prisoners, ":party_size", "$g_encountered_party"),
        (gt, ":party_size", 0),
        (try_begin), #option 1 - player is town lord
          (eq, ":town_lord", "trp_player"),
          (assign, ":player_can_draw_from_garrison", 1),
        (else_try), #option 2 - town is unassigned and part of the player faction
          (store_faction_of_party, ":faction", "$g_encountered_party"),
          (eq, ":faction", "fac_player_supporters_faction"),
          (neg|party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin), #ie, zero or -1

          (assign, ":player_can_draw_from_garrison", 1),
        (else_try), #option 3 - town was captured by player
          (lt, ":town_lord", 0), #ie, unassigned
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (eq, "$players_kingdom", ":castle_faction"),

          (eq, "$g_encountered_party", "$g_castle_requested_by_player"),

          (str_store_string, s10, "str_retrieve_garrison_warning"),
          (assign, ":player_can_draw_from_garrison", 1),
        # (else_try),
          # (lt, ":town_lord", 0), #ie, unassigned
          # (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          # (eq, "$players_kingdom", ":castle_faction"),

          # (store_party_size_wo_prisoners, ":party_size", "$g_encountered_party"),
          # (eq, ":party_size", 0),

          # (str_store_string, s10, "str_retrieve_garrison_warning"),
          # (assign, ":player_can_draw_from_garrison", 1),
        (else_try),
          (party_slot_ge, "$g_encountered_party", slot_town_lord, active_npcs_begin),
          (store_faction_of_party, ":castle_faction", "$g_encountered_party"),
          (eq, "$players_kingdom", ":castle_faction"),
          ##diplomacy start+ can arise if using this to represent polygamy
          (this_or_next|troop_slot_eq, ":town_lord", slot_troop_spouse, "trp_player"),
             (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),
          (this_or_next|is_between, ":town_lord", heroes_begin, heroes_end),
          ##diplomacy end+
          (troop_slot_eq, "trp_player", slot_troop_spouse, ":town_lord"),

          (assign, ":player_can_draw_from_garrison", 1),
        (try_end),

        (eq, ":player_can_draw_from_garrison", 1),
      ],
          "Manage the garrison {s10}",[
              (troop_set_slot, "trp_temp_array_d", slot_adv_transfer_mode, 12),
              (change_screen_exchange_members,1),]),

     ##diplomacy begin
      ("dplmc_negotiate_with_besieger",
      [
        (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
        (party_slot_ge, "$current_town", slot_center_is_besieged_by, 1),
      ]
       ,"Negotiate with the besieger.",
       [
        (jump_to_menu, "mnu_dplmc_negotiate_besieger"),
        ]),
     ##diplomacy end
      ("siege_defender_join_battle",
       [
         (neg|troop_is_wounded, "trp_player"),
         ],
          "Join the battle.",[

              (try_begin),
                  (troop_is_wounded, "trp_player"),
                  (display_message,"@Your wounds are too severe to fight.",message_locked),
              (else_try),
                  (assign, "$g_siege_first_encounter", 0), #dckplmc - moved from main menu conditions
                  (assign, "$new_encounter", 0),

                  (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                  (assign, "$g_battle_result", 0),
                  (try_begin),
                    (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                    (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
                  (else_try),
                    (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
                  (try_end),
                  (call_script, "script_calculate_battle_advantage"),
                  (val_mul, reg0, 2),
                  (val_div, reg0, 3), #scale down the advantage a bit.
                  (set_battle_advantage, reg0),
                  (set_party_battle_mode),
                  (try_begin),
                    (party_slot_eq, "$current_town", slot_center_siege_with_belfry, 1),
                    (set_jump_mission,"mt_castle_attack_walls_belfry"),
                  (else_try),
                    (set_jump_mission,"mt_castle_attack_walls_ladder"),
                  (try_end),
                  (jump_to_scene,":battle_scene"),
                  (assign, "$g_next_menu", "mnu_siege_started_defender"),
                  (jump_to_menu, "mnu_battle_debrief"),
                  (change_screen_mission),
              (try_end),
              ], "Join the defense."),

      ("siege_defender_join_battle",
       [
         (neg|troop_is_wounded, "trp_player"),
         ],
          "Sally out.",[
                  (assign, "$g_siege_first_encounter", 0), #dckplmc - moved from main menu conditions
                  (assign, "$new_encounter", 0),

                  (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
                  (assign, "$g_battle_result", 0),
                  (try_begin),
                    (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
                    (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
                  (else_try),
                    (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
                  (try_end),
                  (call_script, "script_calculate_battle_advantage"),
                  (val_mul, reg0, 2),
                  (val_div, reg0, 3), #scale down the advantage a bit.
                  (set_battle_advantage, reg0),
                  (set_party_battle_mode),
                  (set_jump_mission,"mt_castle_attack_walls_defenders_sally"),
                  (jump_to_scene,":battle_scene"),
                  (assign, "$g_next_menu", "mnu_siege_started_defender"),
                  (jump_to_menu, "mnu_battle_debrief"),
                  (change_screen_mission),
              ]),

      ("siege_defender_troops_join_battle",[(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                            (this_or_next|troop_is_wounded,  "trp_player"),
                                            (ge, reg0, 3)],
          "Order your men to join the battle without you.",[
              (assign, "$g_siege_first_encounter", 0), #dckplmc - moved from main menu conditions
              (assign, "$new_encounter", 0),

              (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
              (select_enemy,1),
              (assign,"$g_enemy_party","$g_encountered_party_2"),
              (assign,"$g_ally_party","$g_encountered_party"),
              (assign,"$g_siege_join", 1),
              (jump_to_menu,"mnu_siege_join_defense")]),


    ]
  )
]
