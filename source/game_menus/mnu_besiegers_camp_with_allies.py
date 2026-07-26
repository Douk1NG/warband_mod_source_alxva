# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

besiegers_camp_with_allies_menu = [
( #SB : pic hotkeys
    "besiegers_camp_with_allies",mnf_enable_hot_keys,
    "{s1} remains under siege. The banners of {s2} fly above the camp of the besiegers,\
 where you and your men are welcomed.",
    "none",
    [
        (str_store_party_name, s1, "$g_encountered_party"),
        (str_store_party_name, s2, "$g_encountered_party_2"),
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", "$g_encountered_party_2"),
        (select_enemy, 0),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
		  ###diplomacy start+
		  ##If terrain advantage is on, use siege settings
          #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		  ##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  #(try_begin),
		  #   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		  #   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		  #(try_end),
		  ###diplomacy end+
          (call_script, "script_encounter_init_variables"),
		  ###diplomacy start+
		  ##Revert terrain advantage setting
		  #(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		  ###diplomacy end+
        (try_end),

        (try_begin),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (else_try),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (assign, ":enemy_finished", 1),
          (else_try),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
##          (assign, "$g_next_menu", -1),#"mnu_castle_taken_by_friends"),
##          (jump_to_menu, "mnu_total_victory"),

          #SB : TODO : add prisoner train of unclaimed prisoners and such, succeed quests by proxy
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "$g_enemy_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            # (eq, ":break", 0),
            (party_prisoner_stack_get_troop_id, ":stack_troop", "p_collective_enemy", ":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (try_begin),
              (check_quest_active, "qst_rescue_prisoner"),
              (quest_slot_eq, "qst_rescue_prisoner", slot_quest_target_troop, ":stack_troop"),
              (call_script, "script_succeed_quest", "qst_rescue_prisoner"),
            (else_try),
              (check_quest_active, "qst_deliver_message_to_prisoner_lord"),
              (quest_slot_eq, "qst_deliver_message_to_prisoner_lord", slot_quest_target_troop, ":stack_troop"),
              (call_script, "script_end_quest", "qst_deliver_message_to_prisoner_lord"),
            (try_end),
          (try_end),
          (try_begin), #check if player gets a share of party prisoners, freed prisoners doesn't count
            (store_faction_of_party, ":faction_no", "$g_ally_party"),
            (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", ":faction_no"),
            (ge, reg0, DPLMC_FACTION_STANDING_MEMBER),
            #check relation with siege leader as well
            (party_stack_get_troop_id, ":leader","$g_encountered_party_2",0),
            (call_script, "script_troop_get_player_relation", ":leader"),
            (this_or_next|troop_slot_eq, ":leader", slot_lord_reputation_type, lrep_martial),
            (ge, reg0, -10),
            (eq, "$capture_screen_shown", 0),
            (assign, "$capture_screen_shown", 1),

            (party_clear, "p_temp_party"),
            (assign, "$g_move_heroes", 0),
            (change_screen_exchange_with_party, "p_temp_party"),
          (else_try), #check if player has seen the loot
            (eq, "$loot_screen_shown", 0),
            (assign, "$loot_screen_shown", 1),
            (troop_clear_inventory, "trp_temp_troop"),
            (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
            (gt, reg0, 0),
            (troop_sort_inventory, "trp_temp_troop"),
            (try_begin),
              (call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
              (assign, "$dplmc_return_menu", "$g_siege_final_menu"),
              (assign, "$lord_selected", "trp_player"),
              (jump_to_menu, "mnu_dplmc_manage_loot_pool"),
            (else_try),
              #Old behavior:
              (change_screen_loot, "trp_temp_troop"),
            (try_end),
          (else_try), #SB : increment globals, add exp
            (call_script, "script_party_give_xp_and_gold", "p_total_enemy_casualties"),
            (call_script, "script_auto_upgrade_troops"),
            (val_add, "$g_total_victories", 1),
            (call_script, "script_party_wound_all_members", "$g_enemy_party"),
            (leave_encounter),
            (change_screen_return),
          (try_end),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":ally_num_soldiers", reg0),
          (eq, "$g_battle_result", -1),
          (eq, ":ally_num_soldiers", 0), #battle lost (TODO : also compare this with routed allies too like in other parts)
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

      ("talk_to_siege_commander",[]," Request a meeting with the commander.",[
                                (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
                                (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
                                (set_visitor,0,"trp_player"),
                                (party_stack_get_troop_id, ":siege_leader_id","$g_encountered_party_2",0),
                                (party_stack_get_troop_dna,":siege_leader_dna","$g_encountered_party_2",0),
                                (set_visitor,17,":siege_leader_id",":siege_leader_dna"),
                                (set_jump_mission,"mt_conversation_encounter"),
                                (jump_to_scene,":meeting_scene"),
                                (assign, "$talk_context", tc_siege_commander),
                                (change_screen_map_conversation, ":siege_leader_id")]),
      ("join_siege_with_allies",[(neg|troop_is_wounded, "trp_player")], "Join the next assault.",
       [
           (assign, "$g_joined_battle_to_help", 1),
           (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
           (try_begin),
             (check_quest_active, "qst_join_siege_with_army"),
             (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
             (add_xp_as_reward, 250),
             (call_script, "script_end_quest", "qst_join_siege_with_army"),
             #Reactivating follow army quest
             (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
             (str_store_troop_name_link, s9, ":faction_marshall"),
             (setup_quest_text, "qst_follow_army"),
             ##diplomacy start+ fix pronoun
             (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
             (str_store_string, s2, "@{s9} wants you to follow {reg0?her:his} army until further notice."),
             ##diplomacy end+
             (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
             (assign, "$g_player_follow_army_warnings", 0),
           (try_end),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_walls),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
           (try_end),
           (call_script, "script_calculate_battle_advantage"),
           (val_mul, reg0, 2),
           (val_div, reg0, 3), #scale down the advantage a bit in sieges.
           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_center_siege_with_belfry, 1),
             (set_jump_mission,"mt_castle_attack_walls_belfry"),
           (else_try),
             (set_jump_mission,"mt_castle_attack_walls_ladder"),
           (try_end),
           (jump_to_scene,":battle_scene"),
           (assign, "$g_siege_final_menu", "mnu_besiegers_camp_with_allies"),
           (assign, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
          ]),
      ("join_siege_stay_back", [(call_script, "script_party_count_members_with_full_health", "p_main_party"),
                                (ge, reg0, 3),
                                ],
       "Order your soldiers to join the next assault without you.",
       [
         (assign, "$g_joined_battle_to_help", 1),
         (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
         (try_begin),
           (check_quest_active, "qst_join_siege_with_army"),
           (quest_slot_eq, "qst_join_siege_with_army", slot_quest_target_center, "$g_encountered_party"),
           (add_xp_as_reward, 100),
           (call_script, "script_end_quest", "qst_join_siege_with_army"),
           #Reactivating follow army quest
           (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
           (str_store_troop_name_link, s9, ":faction_marshall"),
           (setup_quest_text, "qst_follow_army"),
           ##diplomacy start+ fix pronoun
           (call_script, "script_dplmc_store_troop_is_female", ":faction_marshall"),
           (str_store_string, s2, "@{s9} wants you to follow {reg0?her:his} army until further notice."),
           ##diplomacy end+
           (call_script, "script_start_quest", "qst_follow_army", ":faction_marshall"),
           (assign, "$g_player_follow_army_warnings", 0),
         (try_end),
         (jump_to_menu,"mnu_castle_attack_walls_with_allies_simulate")]),
      ("leave",[],"Leave.",[(leave_encounter),(change_screen_return)]),
    ]
  )
]
