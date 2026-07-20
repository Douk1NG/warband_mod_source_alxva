# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

simple_encounter_menu = [
(
    "simple_encounter",mnf_enable_hot_keys|mnf_scale_picture,
    "{s2} You have {reg10} troops fit for battle against their {reg11}.",
    "none",
    [
        (assign, "$g_enemy_party", "$g_encountered_party"),
        (assign, "$g_ally_party", -1),
        (call_script, "script_encounter_calculate_fit"),
        (try_begin),
          (eq, "$new_encounter", 1),
          (assign, "$new_encounter", 0),
          (assign, "$g_encounter_is_in_village", 0),
          (assign, "$g_encounter_type", 0),
          (try_begin),
            (party_slot_eq, "$g_enemy_party", slot_party_ai_state, spai_raiding_around_center),
            (party_get_slot, ":village_no", "$g_enemy_party", slot_party_ai_object),

            (store_distance_to_party_from_party, ":dist", ":village_no", "$g_enemy_party"),

            (try_begin),
              (lt, ":dist", raid_distance),
              (assign, "$g_encounter_is_in_village", ":village_no"),
              (assign, "$g_encounter_type", enctype_fighting_against_village_raid),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_player_raiding_village", 0),
            (assign, "$g_encounter_is_in_village", "$g_player_raiding_village"),
            (assign, "$g_encounter_type", enctype_catched_during_village_raid),
            (party_quick_attach_to_current_battle, "$g_encounter_is_in_village", 1), #attach as enemy
            (str_store_string, s1, "@Villagers"),
            (display_message, "str_s1_joined_battle_enemy", message_negative), #SB : colorize
          (else_try),
            (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
            (party_quick_attach_to_current_battle, "$g_encounter_is_in_village", 0), #attach as friend
            (str_store_string, s1, "@Villagers"),
            (display_message, "str_s1_joined_battle_friend", message_positive), #SB : colorize
            # Let village party join battle at your side
          (try_end),

          (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
          (call_script, "script_encounter_init_variables"),
          (assign, "$encountered_party_hostile", 0),
          (assign, "$encountered_party_friendly", 0),
          (try_begin),
            (gt, "$g_encountered_party_relation", 0),
            (try_begin), #SB : apply provocation override
              (check_quest_active, "qst_cause_provocation"),
              (neg|check_quest_concluded, "qst_cause_provocation"),
              (quest_slot_eq, "qst_cause_provocation", slot_quest_target_faction, "$g_encountered_party_faction"),
              (party_slot_eq, "$g_encountered_party", slot_party_type, spt_kingdom_caravan),
              (assign, "$encountered_party_friendly", 0),
            (else_try),
              (assign, "$encountered_party_friendly", 1),
            (try_end),
          (try_end),

          (try_begin),
            (lt, "$g_encountered_party_relation", 0),
            (assign, "$encountered_party_hostile", 1),
            (try_begin),
              (encountered_party_is_attacker),
              (assign, "$cant_leave_encounter", 1),
            (try_end),
          (try_end),
          (assign, "$talk_context", tc_party_encounter),
          (call_script, "script_setup_party_meeting", "$g_encountered_party"),
        (else_try), #second or more turn
#          (try_begin),
#            (call_script, "script_encounter_calculate_morale_change"),
#          (try_end),
          (try_begin),
            # We can leave battle only after some troops have been killed.
            (eq, "$cant_leave_encounter", 1),
            (call_script, "script_party_count_members_with_full_health", "p_main_party_backup"),
            (assign, ":org_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_encountered_party_backup"),
            (val_add, ":org_total_party_counts", reg0),

            (call_script, "script_party_count_members_with_full_health", "p_main_party"),
            (assign, ":cur_total_party_counts", reg0),
            (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
            (val_add, ":cur_total_party_counts", reg0),

            (store_sub, ":leave_encounter_limit", ":org_total_party_counts", 10),
            (lt, ":cur_total_party_counts", ":leave_encounter_limit"),
            (assign, "$cant_leave_encounter", 0),
          (try_end),
          (eq, "$g_leave_encounter",1),
          (change_screen_return),
        (try_end),

        #setup s2
        (try_begin),
          (party_is_active, "$g_encountered_party"),
          (str_store_party_name, s1,"$g_encountered_party"),
          (try_begin),
            (eq, "$g_encounter_type", 0),
            (str_store_string, s2,"@You have encountered {s1}."),
          (else_try),
            (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
            (str_store_party_name, s3, "$g_encounter_is_in_village"),
            (str_store_string, s2,"@You have engaged {s1} while they were raiding {s3}."),
          (else_try),
            (eq, "$g_encounter_type", enctype_catched_during_village_raid),
            (str_store_party_name, s3, "$g_encounter_is_in_village"),
            (str_store_string, s2,"@You were caught by {s1} while your forces were raiding {s3}."),
          (try_end),
        (try_end),
        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg0),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1), #battle won

            (this_or_next|le, ":num_enemy_regulars_remaining", 0), #battle won
            (le, ":num_enemy_regulars_remaining",  "$num_routed_enemies"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign, ":enemy_finished",1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),

            (this_or_next|le, ":num_enemy_regulars_remaining", 0),
            (le, "$g_enemy_fit_for_battle", "$num_routed_enemies"),  #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (ge, "$g_friend_fit_for_battle",1),
            (assign, ":enemy_finished",1),
          (try_end),

          (this_or_next|eq, ":enemy_finished",1),
          # (this_or_next|eq, ":num_enemy_regulars_remaining",0),
          (eq,"$g_enemy_surrenders",1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"),
          (assign, ":num_our_regulars_remaining", reg0),
          (assign, ":friends_finished",0),
          (try_begin),
            (eq, "$g_battle_result", -1),

            #(eq, ":num_our_regulars_remaining", 0), #battle lost
            (le, ":num_our_regulars_remaining",  "$num_routed_us"), #replaced for above line because we do not want routed agents to spawn again in next turn of battle.

            (assign,  ":friends_finished", 1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (ge, "$g_enemy_fit_for_battle",1),
            (le, "$g_friend_fit_for_battle",0),
            (assign, ":friends_finished",1),
          (try_end),

          (this_or_next|eq, ":friends_finished",1),
          (eq,"$g_player_surrenders",1),
          (assign, "$g_next_menu", "mnu_captivity_start_wilderness"),
          (jump_to_menu, "mnu_total_defeat"),
        (try_end),


        (try_begin),
          (eq, "$g_encountered_party_template", "pt_looters"),
          (set_background_mesh, "mesh_pic_bandits"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_mountain_bandits"),
          (set_background_mesh, "mesh_pic_mountain_bandits"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_steppe_bandits"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_taiga_bandits"),
          (set_background_mesh, "mesh_pic_steppe_bandits"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_sea_raiders"),
          (set_background_mesh, "mesh_pic_sea_raiders"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_forest_bandits"),
          (set_background_mesh, "mesh_pic_forest_bandits"),
        (else_try),
          (this_or_next|eq, "$g_encountered_party_template", "pt_deserters"),
          (eq, "$g_encountered_party_template", "pt_routed_warriors"),
          (set_background_mesh, "mesh_pic_deserters"),
        #SB : dplmc party templates
        (else_try),
          (eq, "$g_encountered_party_template", "pt_center_reinforcements"),
          (set_background_mesh, "mesh_pic_recruits"),
        (else_try),
          (eq, "$g_encountered_party_template", "pt_kingdom_hero_party"),
		  (party_stack_get_troop_id, ":leader_troop", "$g_encountered_party", 0),
		  (ge, ":leader_troop", 1),
		  (troop_get_slot, ":leader_troop_faction", ":leader_troop", slot_troop_original_faction),
		  (try_begin),
			(eq, ":leader_troop_faction", fac_kingdom_1),
            (set_background_mesh, "mesh_pic_swad"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_2),
            (set_background_mesh, "mesh_pic_vaegir"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_3),
            (set_background_mesh, "mesh_pic_khergit"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_4),
            (set_background_mesh, "mesh_pic_nord"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_5),
            (set_background_mesh, "mesh_pic_rhodock"),
		  (else_try),
			(eq, ":leader_troop_faction", fac_kingdom_6),
            (set_background_mesh, "mesh_pic_sarranid_encounter"),
		  (try_end),
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

      ("encounter_attack",
      [
        (eq, "$encountered_party_friendly", 0),
        (neg|troop_is_wounded, "trp_player"),
      ],
      "Charge the enemy.",
      [
        (assign, "$g_battle_result", 0),
        (assign, "$g_engaged_enemy", 1),

        #(assign, "$player_deploy_troops", 1),

        (party_get_template_id, ":encountered_party_template", "$g_encountered_party"),
        (try_begin),
		  (eq, ":encountered_party_template", "pt_village_farmers"),
		  (unlock_achievement, ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED),
		(try_end),

        (call_script, "script_calculate_renown_value"),
		##diplomacy start+
		(try_begin),
			#Call this to properly set cached values for strength
			(eq, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(assign, ":terrain_code", dplmc_terrain_code_none),#defined in header_terrain_types.py
			(try_begin),
				(this_or_next|eq, "$g_encounter_type", enctype_fighting_against_village_raid),
					(eq, "$g_encounter_type", enctype_catched_during_village_raid),
				(assign, ":terrain_code", dplmc_terrain_code_village),#defined in header_terrain_types.py
			(else_try),
				(encountered_party_is_attacker),
				(call_script, "script_dplmc_get_terrain_code_for_battle", "$g_encountered_party", "p_main_party"),
				(assign, ":terrain_code", reg0),
			(else_try),
				(call_script, "script_dplmc_get_terrain_code_for_battle", "p_main_party", "$g_encountered_party"),
				(assign, ":terrain_code", reg0),
			(try_end),
			(neq, ":terrain_code", dplmc_terrain_code_none),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_main_party", ":terrain_code", 0, 1),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "$g_encountered_party", ":terrain_code", 0, 1),
		(try_end),
		##diplomacy end+
        (call_script, "script_calculate_battle_advantage"),
        (set_battle_advantage, reg0),
        (set_party_battle_mode),

        (try_begin),
          (eq, "$g_encounter_type", enctype_fighting_against_village_raid),
          (assign, "$g_village_raid_evil", 0),
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$g_encounter_is_in_village", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
        (else_try),
          (eq, "$g_encounter_type", enctype_catched_during_village_raid),
          (assign, "$g_village_raid_evil", 1), #SB : probably true
          (set_jump_mission,"mt_village_raid"),
          (party_get_slot, ":scene_to_use", "$g_encounter_is_in_village", slot_castle_exterior),
          (jump_to_scene, ":scene_to_use"),
        (else_try), #ships
          (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
          (party_get_slot, ":enemy_ship_type", "$g_encountered_party", slot_party_ship_type),
          (gt, ":ship_type", 0),
          (gt, ":enemy_ship_type", 0),
          #(set_jump_mission,"mt_ship_battle"),
          (call_script, "script_setup_random_scene"),
        (else_try),
          (set_jump_mission,"mt_lead_charge"),
          (call_script, "script_setup_random_scene"),
        (try_end),
        (assign, "$g_next_menu", "mnu_simple_encounter"),
        (jump_to_menu, "mnu_battle_debrief"),
        (change_screen_mission),
      ]),

      ("encounter_order_attack",
      [
        (eq, "$encountered_party_friendly", 0),
        (call_script, "script_party_count_members_with_full_health", "p_main_party"),(ge, reg0, 4),
      ],
      "Order your troops to attack without you.",
      [
        (jump_to_menu, "mnu_order_attack_begin"),
        #(simulate_battle,3),
      ]),

      ("encounter_leave",[
          (eq,"$cant_leave_encounter", 0),
          ],"Leave.",[

###NPC companion changes begin
              (try_begin),
                  (eq, "$encountered_party_friendly", 0),
                  (encountered_party_is_attacker),
                  (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
              (try_end),
###NPC companion changes end
#Troop commentary changes begin
              (try_begin),
                  (eq, "$encountered_party_friendly", 0),
#                  (encountered_party_is_attacker),
                  (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
                  (try_for_range, ":stack_no", 0, ":num_stacks"),
                    (party_stack_get_troop_id,   ":stack_troop","p_encountered_party_backup",":stack_no"),
                    (is_between, ":stack_troop", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
                    (store_troop_faction, ":victorious_faction", ":stack_troop"),
#					(store_relation, ":relation_with_stack_troop", ":victorious_faction", "fac_player_faction"),
#					(lt, ":relation_with_stack_troop", 0),
                    (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player",  -1, ":stack_troop", ":victorious_faction"),
                  (try_end),
              (try_end),
#Troop commentary changes end
          	(leave_encounter),(change_screen_return)]),
      ("encounter_retreat",[
         (eq,"$cant_leave_encounter", 1),
         (call_script, "script_get_max_skill_of_player_party", "skl_tactics"),
         (assign, ":max_skill", reg0),
         (val_add, ":max_skill", 4),

         (call_script, "script_party_count_members_with_full_health", "p_collective_enemy", 0),
         (assign, ":enemy_party_strength", reg0),
         (val_div, ":enemy_party_strength", 2),

         (val_div, ":enemy_party_strength", ":max_skill"),
         (val_max, ":enemy_party_strength", 1),

         (call_script, "script_party_count_fit_regulars", "p_main_party"),
         (assign, ":player_count", reg0),
         (ge, ":player_count", ":enemy_party_strength"),
         ],"Pull back, leaving some soldiers behind to cover your retreat.",[(jump_to_menu, "mnu_encounter_retreat_confirm"),]),

      ("encounter_surrender",[
         (eq,"$cant_leave_encounter", 1),
          ],"Surrender.",[(assign,"$g_player_surrenders",1)]),
    ]
  )
]
