# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

bandit_lair_menu = [
(
    "bandit_lair",0,
    "{s3}",
    "none",
    [
      (try_begin),
        (eq, "$loot_screen_shown", 1),

        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),

           #dckplmc
           (store_current_hours, ":cur_hours"),
           (val_add, ":cur_hours", bandit_lair_respawn_hours), #spawn again after configured delay
           (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),

        (try_end),

        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),

        (assign, "$g_leave_encounter", 0),
        (change_screen_return),

      (else_try),
        (party_stack_get_troop_id, ":bandit_type", "$g_encountered_party", 0),
        (str_store_troop_name_plural, s4, ":bandit_type"),
        (str_store_string, s5, "str_bandit_approach_defile"),

        #SB : set pictures
        (try_begin),
          (eq, ":bandit_type", "trp_desert_bandit"),
          (str_store_string, s5, "str_bandit_approach_defile"),
        (else_try),
          (eq, ":bandit_type", "trp_mountain_bandit"),
          (str_store_string, s5, "str_bandit_approach_cliffs"),
          (set_background_mesh, "mesh_pic_mountain_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_forest_bandit"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
          (set_background_mesh, "mesh_pic_forest_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_taiga_bandit"),
          (str_store_string, s5, "str_bandit_approach_swamp"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_steppe_bandit"),
          (str_store_string, s5, "str_bandit_approach_thickets"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, ":bandit_type", "trp_sea_raider"),
          (str_store_string, s5, "str_bandit_approach_cove"),
          (set_background_mesh, "mesh_pic_sea_raiders"),
        (try_end),


        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_preattack"),
        (else_try),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (eq, ":template", "pt_looter_lair"),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_lost_startup_hideout_attack"),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_failure"),
          (set_background_mesh, "mesh_pic_wounded"),
          (try_begin),
            (eq, "$character_gender", tf_female),
            (set_background_mesh, "mesh_pic_wounded_fem"),
          (try_end),
        (else_try),
          (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2), #used in place of global variable
          (str_store_string, s3, "str_bandit_hideout_success"),
          (set_background_mesh, "mesh_pic_victory"),
        (try_end),
      (try_end),
    ],
    [
      ("continue_1",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0), #used in place of global variable
      ],
      "Attack the hideout...",

      [
        (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 1),
        (party_get_template_id, ":template", "$g_encountered_party"),
        (assign, "$g_enemy_party", "$g_encountered_party"),

        (try_begin),
          (eq, ":template", "pt_sea_raider_lair"),
          (assign, ":bandit_troop", "trp_sea_raider"),
          (assign, ":scene_to_use", "scn_lair_sea_raiders"),
        (else_try),
          (eq, ":template", "pt_forest_bandit_lair"),
          (assign, ":bandit_troop", "trp_forest_bandit"),
          (assign, ":scene_to_use", "scn_lair_forest_bandits"),
        (else_try),
          (eq, ":template", "pt_desert_bandit_lair"),
          (assign, ":bandit_troop", "trp_desert_bandit"),
          (assign, ":scene_to_use", "scn_lair_desert_bandits"),
        (else_try),
          (eq, ":template", "pt_mountain_bandit_lair"),
          (assign, ":bandit_troop", "trp_mountain_bandit"),
          (assign, ":scene_to_use", "scn_lair_mountain_bandits"),
        (else_try),
          (eq, ":template", "pt_taiga_bandit_lair"),
          (assign, ":bandit_troop", "trp_taiga_bandit"),
          (assign, ":scene_to_use", "scn_lair_taiga_bandits"),
        (else_try),
          (eq, ":template", "pt_steppe_bandit_lair"),
          (assign, ":bandit_troop", "trp_steppe_bandit"),
          (assign, ":scene_to_use", "scn_lair_steppe_bandits"),
        (else_try),
          (eq, ":template", "pt_looter_lair"),
          (assign, ":bandit_troop", "trp_looter"),

          (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),

          (try_begin),
            (eq, ":starting_town_faction", "fac_kingdom_1"), #player selected swadian city as starting town.
            (assign, ":scene_to_use", "scn_lair_forest_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_2"), #player selected Vaegir city as starting town.
            (assign, ":scene_to_use", "scn_lair_taiga_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_3"), #player selected Khergit city as starting town.
            (assign, ":scene_to_use", "scn_lair_steppe_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_4"), #player selected Nord city as starting town.
            (assign, ":scene_to_use", "scn_lair_sea_raiders"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_5"), #player selected Rhodok city as starting town.
            (assign, ":scene_to_use", "scn_lair_mountain_bandits"),
          (else_try),
            (eq, ":starting_town_faction", "fac_kingdom_6"), #player selected Sarranid city as starting town.
            (assign, ":scene_to_use", "scn_lair_desert_bandits"),
          (try_end),
        (try_end),

        (modify_visitors_at_site,":scene_to_use"),
        (reset_visitors),

        (store_character_level, ":player_level", "trp_player"),
        (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
        (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),

        (try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),
          (store_random_in_range, ":random_entry_point", 2, 11),
          (set_visitor, ":random_entry_point", ":bandit_troop", 1),
        (try_end),

        (party_clear, "p_temp_casualties"),

        (set_party_battle_mode),
        (set_battle_advantage, 0),
        (assign, "$g_battle_result", 0),
        (set_jump_mission,"mt_bandit_lair"),

        (jump_to_scene, ":scene_to_use"),
        (change_screen_mission),
      ]),

      ("leave_no_attack",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 0),
      ],
      "Leave...",
      [
        (change_screen_return),
      ]),

      ("leave_victory",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 2),
      ],
      "Continue...",
      [
        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end), #SB : template range
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
          #dckplmc : keep this bandit type suppressed for the configured delay
          (store_current_hours, ":cur_hours"),
          (val_add, ":cur_hours", bandit_lair_respawn_hours),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),
        (try_end),

        (party_get_template_id, ":template", "$g_encountered_party"),
        (try_begin),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_succeed_quest", "qst_destroy_bandit_lair"),
        (try_end),

        # Show loot screen before leaving
        (try_begin),
          (eq, "$loot_screen_shown", 0),
          (assign, "$loot_screen_shown", 1),
          (troop_clear_inventory, "trp_temp_troop"),

          (party_get_num_companion_stacks, ":num_stacks", "p_temp_casualties"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
            (try_begin),
              (party_stack_get_size, ":stack_size", "p_temp_casualties", ":stack_no"),
              (party_stack_get_troop_id, ":stack_troop", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_size", 0),
              (party_add_members, "p_total_enemy_casualties", ":stack_troop", ":stack_size"), #addition_to_p_total_enemy_casualties
              (party_stack_get_num_wounded, ":stack_wounded_size", "p_temp_casualties", ":stack_no"),
              (gt, ":stack_wounded_size", 0),
              (party_wound_members, "p_total_enemy_casualties", ":stack_troop", ":stack_wounded_size"),
            (try_end),
          (try_end),

          (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"), #p_encountered_party_backup changed to total_enemy_casualties
          (gt, reg0, 0),
          (troop_sort_inventory, "trp_temp_troop"),
          ##diplomacy start+
          (try_begin),
            (call_script, "script_party_calculate_loot", "p_total_enemy_casualties"),
            (assign, "$dplmc_return_menu", "mnu_bandit_lair"),
            #SB : variable resets
            (assign, "$lord_selected", "trp_player"),
            (str_clear, dplmc_loot_string),
            (jump_to_menu, "mnu_dplmc_manage_loot_pool"),
          (else_try),
             #Fall back to old behavior
            (change_screen_loot, "trp_temp_troop"),
          (try_end),
          ##diplomacy end+
        (try_end),

        # Remove the lair party (all types including non-looter)
        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (remove_party, "$g_encountered_party"),
        (try_end),

        (assign, "$g_leave_encounter", 0),
        (change_screen_return),
      ]),

      ("leave_defeat",
      [
        (party_slot_eq, "$g_encountered_party", slot_party_ai_substate, 1),
      ],
      "Continue...",
      [
        # Player lost — bandits pack up and move (lair is destroyed, spawns elsewhere in 24h)
        (try_for_range, ":bandit_template", bandit_party_templates_begin, bandit_party_templates_end),
          (party_template_slot_eq, ":bandit_template", slot_party_template_lair_party, "$g_encountered_party"),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_party, 0),
          (store_current_hours, ":cur_hours"),
          (val_add, ":cur_hours", 24),
          (party_template_set_slot, ":bandit_template", slot_party_template_lair_next_spawn, ":cur_hours"),
        (try_end),

        (try_begin),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (check_quest_active, "qst_destroy_bandit_lair"),
          (quest_slot_eq, "qst_destroy_bandit_lair", slot_quest_target_party, "$g_encountered_party"),
          (call_script, "script_fail_quest", "qst_destroy_bandit_lair"),
        (try_end),

        (try_begin),
          (ge, "$g_encountered_party", 0),
          (party_is_active, "$g_encountered_party"),
          (party_get_template_id, ":template", "$g_encountered_party"),
          (neq, ":template", "pt_looter_lair"),
          (remove_party, "$g_encountered_party"),
        (try_end),

        (assign, "$g_leave_encounter", 0),

        (try_begin),
            (party_is_active, "$g_encountered_party"),
            (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 0),
        (try_end),

        (change_screen_return),
        ]),

     ]
  )
]
