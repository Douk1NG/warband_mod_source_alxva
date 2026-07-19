# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

siege_menus = [
  (
    "cut_siege_without_fight",0,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
  ),
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
  ),
  (
    "siege_attack_meets_sally",mnf_scale_picture,
    "The defenders sally out to meet your assault.",
    "none",
    [
        (set_background_mesh, "mesh_pic_sally_out"),
    ],
    [
      ("continue",[],
       "Continue...",
       [
             (jump_to_menu, "mnu_battle_debrief"),
             (change_screen_mission),
       ]),
    ]
  ),

   (
    "castle_besiege_inner_battle",mnf_scale_picture,
    "{s1}",
    "none",
    [
		  # ##diplomacy start+ test gender with script
        # #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        # (try_begin),
          # #(eq, ":is_female", 1),#<- replaced
		  # (eq, "$character_gender", tf_female),#<- added
          # (set_background_mesh, "mesh_pic_siege_sighted_fem"),
        # (else_try),
          # (set_background_mesh, "mesh_pic_siege_sighted"),
        # (try_end),
		  # ##diplomacy end+
        #SB : sally picture more appropriate
        (set_background_mesh, "mesh_pic_sally_out"),
        (assign, ":result", "$g_battle_result"),#will be reset at script_encounter_calculate_fit
        (call_script, "script_encounter_calculate_fit"),

# TODO: To use for the future:
        (try_begin),
          (this_or_next|neq, ":result", 1),
          (this_or_next|le, "$g_friend_fit_for_battle", 0),
          (le, "$g_enemy_fit_for_battle", 0),
          (jump_to_menu, "$g_siege_final_menu"),
        (else_try),
          (call_script, "script_encounter_calculate_fit"),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (try_begin), #SB : siege strings
              (eq, "$g_ally_party", "$g_encountered_party"),
              (str_store_string, s1, "@You've been driven away from the walls.\
 Now the attackers are pouring into the streets. If you can defeat them, you can perhaps turn the tide and save the day."),
            (else_try),
              (str_store_string, s1, "@You've breached the town walls,\
 but the stubborn defenders continue to resist you in the streets!\
 You'll have to deal with them before you can attack the keep at the heart of the town."),
            (try_end),
          (else_try),
            (eq, "$g_siege_battle_state", 2),
            (eq, ":result", 1),
            (try_begin), #SB : siege strings
              (eq, "$g_ally_party", "$g_encountered_party"),
              (str_store_string, s1, "@As a last defensive effort, you retreat to the main hall of the keep.\
 You and your remaining soldiers will put up a desperate fight here. If you are defeated, there's no other place to fall back to."),
            (else_try),
              (str_store_string, s1, "@The town centre is yours,\
 but the remaining defenders have retreated to the castle.\
 It must fall before you can complete your victory."),
            (try_end),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (else_try),
          (try_begin),
            (eq, "$g_siege_battle_state", 0),
            (eq, ":result", 1),
            (assign, "$g_battle_result", 0),
            (jump_to_menu, "$g_siege_final_menu"),
          (else_try),
            (eq, "$g_siege_battle_state", 1),
            (eq, ":result", 1),
            (str_store_string, s1, "@The remaining defenders have retreated to the castle as a last defense. You must go in and crush any remaining resistance."),
          (else_try),
            (jump_to_menu, "$g_siege_final_menu"),
          (try_end),
        (try_end),
    ],
    [
      ("continue",[],
       "Continue...",
       [
           (try_begin),
             (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
             (try_begin),
               (eq, "$g_siege_battle_state", 1),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_center),
               (set_jump_mission, "mt_besiege_inner_battle_town_center"),
             (else_try),
               (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
               (set_jump_mission, "mt_besiege_inner_battle_castle"),
             (try_end),
           (else_try),
             (party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle),
             (set_jump_mission, "mt_besiege_inner_battle_castle"),
           (try_end),
##           (call_script, "script_calculate_battle_advantage"),
##           (set_battle_advantage, reg0),
           (set_party_battle_mode),
           (jump_to_scene, ":battle_scene"),
           (val_add, "$g_siege_battle_state", 1),
           (assign, "$g_next_menu", "mnu_castle_besiege_inner_battle"),
           (jump_to_menu, "mnu_battle_debrief"),
           (change_screen_mission),
       ]),
    ]
  ),
  (
    "construct_ladders",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that it will take\
 {reg4} hours to build enough scaling ladders for the assault.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 14, ":max_skill"),
     (val_mul, reg4, 2),
     (val_div, reg4, 3),

     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),

    #SB : add tableau
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
    ],
    [
      ("build_ladders_cont",[],
       "Do it.", [
           (assign, "$g_siege_method", 1),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           (store_sub, ":hours_takes", 14, reg0),
           (val_mul, ":hours_takes", 2),
           (val_div, ":hours_takes", 3),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (rest_for_hours_interactive, 96, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  ),
  (
    "construct_siege_tower",0,
    "As the party member with the highest Engineer skill ({reg2}), {reg3?you estimate:{s3} estimates} that building a siege tower will take\
 {reg4} hours.",
    "none",
    [(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
     (assign, ":max_skill", reg0),
     (assign, ":max_skill_owner", reg1),
     (assign, reg2, ":max_skill"),

     (store_sub, reg4, 15, ":max_skill"),
     (val_mul, reg4, 6),

     (try_begin),
       (eq, ":max_skill_owner", "trp_player"),
       (assign, reg3, 1),
     (else_try),
       (assign, reg3, 0),
       (str_store_troop_name, s3, ":max_skill_owner"),
     (try_end),

    #SB : add tableau
    (set_fixed_point_multiplier, 100),
    (position_set_x, pos0, 70),
    (position_set_y, pos0, 5),
    (position_set_z, pos0, 75),
    (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":max_skill_owner", pos0),
    ],
    [
      ("build_siege_tower_cont",[],
       "Start building.", [
           (assign, "$g_siege_method", 2),
           (store_current_hours, ":cur_hours"),
           (call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
           (store_sub, ":hours_takes", 15, reg0),
           (val_mul, ":hours_takes", 6),
           (store_add, "$g_siege_method_finish_hours",":cur_hours", ":hours_takes"),
           (assign,"$auto_besiege_town","$current_town"),
           (rest_for_hours_interactive, 240, 5, 1), #rest while attackable. A trigger will divert control when attack is ready.
           (change_screen_return),
           ]),
      ("go_back",[],
       "Go back.", [(jump_to_menu,"mnu_castle_besiege")]),
        ],
  ),

   (
    "castle_attack_walls_simulate",mnf_scale_picture|mnf_disable_all_keys,
    "{s4}^^Your casualties:{s8}^^Enemy casualties were: {s9}",
    "none",
    [
        (try_begin),
          (set_background_mesh, "mesh_pic_siege_attack"),
        (try_end),
        ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+
        (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
        (assign, ":player_party_strength", reg0),
        (val_div, ":player_party_strength", 10),

        (call_script, "script_party_calculate_strength", "$g_encountered_party", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 4),

        (inflict_casualties_to_party_group, "p_main_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s8, s0),

        (inflict_casualties_to_party_group, "$g_encountered_party", ":player_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),

        (assign, "$no_soldiers_left", 0),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_us)
          (assign, "$no_soldiers_left", 1),
          (str_store_string, s4, "str_attack_walls_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","$g_encountered_party"),
          (le, reg0, 0), #(TODO : compare with num_routed_enemies)
          (assign, "$no_soldiers_left", 1),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_attack_walls_success"),
        (else_try),
          (str_store_string, s4, "str_attack_walls_continue"),
        (try_end),
		##diplomacy start+
		#Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		##diplomacy end+
     ],
    [
##      ("lead_next_wave",[(eq, "$no_soldiers_left", 0)],"Lead the next wave of attack personally.", [
##           (party_get_slot, ":battle_scene", "$g_encountered_party", slot_castle_exterior),
##           (set_party_battle_mode),
##           (set_jump_mission,"mt_castle_attack_walls"),
##           (jump_to_scene,":battle_scene"),
##           (jump_to_menu,"mnu_castle_outside"),
##           (change_screen_mission),
##       ]),
##      ("continue_attacking",[(eq, "$no_soldiers_left", 0)],"Order your soldiers to keep attacking...", [
##                                    (jump_to_menu,"mnu_castle_attack_walls_3"),
##                                    ]),
##      ("call_soldiers_back",[(eq, "$no_soldiers_left", 0)],"Call your soldiers back.",[(jump_to_menu,"mnu_castle_outside")]),
      ("continue",[],"Continue...",[(jump_to_menu,"mnu_castle_besiege")]),
    ]
  ),

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
  ),
  (
    "siege_join_defense",mnf_disable_all_keys,
    "{s4}^^Your casualties: {s8}^^Allies' casualties: {s9}^^Enemy casualties: {s10}",
    "none",
    [
	    ###diplomacy start+
		##If terrain advantage is on, use siege settings
        #(assign, ":save_dplmc_terrain_advantage", "$g_dplmc_terrain_advantage"),
		##(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		#(try_begin),
		#   (eq, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_ENABLE),
		#   (assign, "$g_dplmc_terrain_advantage", TERRAIN_ADVANTAGE_FORCE_SIEGE),
		#(try_end),
		###diplomacy end+
        (try_begin),
          (eq, "$g_siege_join", 1),
          (call_script, "script_party_calculate_strength", "p_main_party", 1), #skip player
          (assign, ":player_party_strength", reg0),
          (val_div, ":player_party_strength", 5),
        (else_try),
          (assign, ":player_party_strength", 0),
        (try_end),

        (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
        (assign, ":ally_party_strength", reg0),
        (val_div, ":ally_party_strength", 5),
        (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
        (assign, ":enemy_party_strength", reg0),
        (val_div, ":enemy_party_strength", 10),

        (store_add, ":friend_party_strength", ":player_party_strength", ":ally_party_strength"),
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

        (inflict_casualties_to_party_group, "$g_ally_party", ":enemy_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s9, s0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_collective_ally"),

        (inflict_casualties_to_party_group, "$g_enemy_party", ":friend_party_strength", "p_temp_casualties"),
        (call_script, "script_print_casualties_to_s0", "p_temp_casualties", 0),
        (str_store_string_reg, s10, s0),
        (party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy"),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health","p_main_party"),
          (le, reg0, 0),
          (str_store_string, s4, "str_siege_defender_order_attack_failure"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health","p_collective_enemy"),
          (le, reg0, 0),
          (assign, "$g_battle_result", 1),
          (str_store_string, s4, "str_siege_defender_order_attack_success"),
        (else_try),
          (str_store_string, s4, "str_siege_defender_order_attack_continue"),
        (try_end),
		###diplomacy start+
		##Revert terrain advantage settings
		#(assign, "$g_dplmc_terrain_advantage", ":save_dplmc_terrain_advantage"),
		###diplomacy end+
    ],
    [
      ("continue",[],"Continue...",[
          (jump_to_menu,"mnu_siege_started_defender"),
          ]),
    ]
  ),
  (
    "enter_your_own_castle",0,
    "{s10}",
    "none",
    [
      (try_begin),
	  ##diplomacy start+ Add support for the player as co-ruler of an NPC faction
	    (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(neg|is_between, "$supported_pretender", pretenders_begin, pretenders_end), #SB : exception for honorific
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(try_begin),
			(eq, "$character_gender", tf_female),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING_FEMALE, s10),
		(else_try),
			(call_script, "script_dplmc_print_cultural_word_to_sreg", "trp_player", DPLMC_CULTURAL_TERM_KING, s10),
		(try_end),
		(str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {s10}."),
	  (else_try),
	  ##diplomacy end+
        (neg|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {king/queen}."),
      (else_try),
        (str_store_string, s10, "@As you approach, you are spotted by the castle guards, who welcome you and open the gates for their {lord/lady}."),
      (try_end),

      (str_store_party_name, s2, "$current_town"),
    ],
    [
      ("continue",[],"Continue...",
       [ (jump_to_menu,"mnu_town"),
        ]),
    ],
  ),
]
