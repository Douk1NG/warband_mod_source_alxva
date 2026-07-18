# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

companion_overview = ("companion_overview", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        # (position_set_x, pos1, 500),
        # (position_set_y, pos1, 700),
        # (str_store_string, s1, "@Please select a hero."),

        # (create_text_overlay, "$g_presentation_obj_1", s1, tf_center_justify|tf_vertical_align_center|tf_with_outline),
        # (overlay_set_position, "$g_presentation_obj_1", pos1),
        # (overlay_set_color, "$g_presentation_obj_1", 0xFFFFFF),

        #Set up the bottom row: [banner] -> export -> done
        (create_in_game_button_overlay, "$g_presentation_obj_2", "str_done"),
        (position_set_x, pos1, 870),
        (position_set_y, pos1, 15),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (overlay_set_color, "$g_presentation_obj_2", 0xFFFFFF),

        (try_begin),
          (neq, "$g_player_troop", "trp_player"),
          (create_in_game_button_overlay, "$g_presentation_obj_3", "@Export/Import"),
          (position_set_x, pos1, 650),
          (position_set_y, pos1, 15),
          (overlay_set_position, "$g_presentation_obj_3", pos1),
          (overlay_set_color, "$g_presentation_obj_3", 0xFFFFFF),
        (else_try),
          (assign, "$g_presentation_obj_3", 0),
        (try_end),

        (try_begin),
          (this_or_next|ge, "$cheat_mode", 1),
          (troop_slot_ge, "$g_player_troop", slot_troop_banner_scene_prop, banner_scene_props_begin),
          (create_in_game_button_overlay, "$g_presentation_obj_4", "@Reselect Banner"),
          (position_set_x, pos1, 440),
          (position_set_y, pos1, 15),
          (overlay_set_position, "$g_presentation_obj_4", pos1),
          (overlay_set_color, "$g_presentation_obj_4", 0xFFFFFF),
        (else_try),
          (assign, "$g_presentation_obj_4", 0),
        (try_end),


        (assign, ":pos_x", 900),
        (assign, ":pos_y", 600),
        # (assign, ":num_of_heros", 0),
        # (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
        (try_for_range, ":stack_troop", active_npcs_including_player_begin, companions_end),
          # (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
          # (troop_is_hero, ":stack_troop"),
          # (neg|troop_is_wounded, ":stack_troop"),
          (this_or_next|eq, ":stack_troop", active_npcs_including_player_begin), #player placeholder
          (this_or_next|troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
          (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_player_companion),
          (try_begin),
            (eq, ":stack_troop", active_npcs_including_player_begin),
            (assign, ":stack_troop", "trp_player"),
          (try_end),
          (str_store_troop_name, s1, ":stack_troop"),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (val_sub, ":pos_y", 30),

          #add some emphasis, lords are recognizable by title already
          (try_begin),
            (eq, ":stack_troop", "$g_player_troop"),
            # (create_text_overlay, reg0, s1, tf_center_justify|tf_vertical_align_center),
            # (overlay_set_position, reg0, pos1),
            # (try_begin),
              # (troop_get_slot, ":home", "$g_talk_troop", slot_troop_home),
              # (is_between, ":home", centers_begin, centers_end),
              # (party_get_slot, ":faction", ":home", slot_center_original_faction),
              # (faction_get_color, ":color", ":faction"),
              # (overlay_set_color, reg0, ":color"),
            # (try_end),
            (create_button_overlay, reg0, s1, tf_center_justify|tf_vertical_align_center),
            (overlay_set_alpha, reg0, 0xCC),
          (else_try),
            (create_button_overlay, reg0, s1, tf_center_justify|tf_vertical_align_center),
            (overlay_set_alpha, reg0, 0x99),
          (try_end),
          (assign, ":obj", reg0),
          (overlay_set_position, ":obj", pos1),
          (try_begin),
            (troop_is_wounded, ":stack_troop"),
            (overlay_set_color, ":obj", 0xFF0000),
          (try_end),

          (troop_set_slot, ":stack_troop", dplmc_slot_troop_temp_slot, ":obj"),
          # (troop_set_slot, "trp_temp_array_a", ":num_of_heros", reg0),
          # (troop_set_slot, "trp_temp_array_b", ":num_of_heros", ":stack_troop"),
          # (val_add, ":num_of_heros", 1),
        (try_end),

        ################
        # (create_mesh_overlay_with_tableau_material, reg0, -1, "tableau_troop_note_mesh", "$g_player_troop"),
        # (position_set_x, pos1, 500),
        # (position_set_y, pos1, 500),
        # (overlay_set_size, reg0, pos1),
        # (position_set_x, pos1, 150),
        # (position_set_y, pos1, 560),
        # (overlay_set_position, reg0, pos1),

        (store_mul, ":cur_troop", "$g_player_troop", 2), #with weapons
        (create_image_button_overlay_with_tableau_material, "$g_presentation_obj_1", -1, "tableau_game_party_window", ":cur_troop"),
        (position_set_x, pos1, 675),
        (position_set_y, pos1, 900),
        (overlay_set_size, "$g_presentation_obj_1", pos1),
        (position_set_x, pos1, -25),
        (position_set_y, pos1, 50),
        (overlay_set_position, "$g_presentation_obj_1", pos1),


        (try_begin), #vital statistics like killcount/renown/honor/rtr
          (eq, "$g_player_troop", "trp_player"),
          (troop_get_slot, reg1, "trp_player", slot_troop_renown),
          (assign, reg2, "$player_honor"),
          (assign, reg3, "$player_right_to_rule"),
          #renown_reg2_honour_rating_reg3s12_friends_s8_enemies_s6_s9
          (str_store_string, s0, "@ Renown: {reg1}^ Honor: {reg2}^ Right to rule: {reg3}"),
        (else_try),#companion mission strings
          (troop_slot_eq, "$g_player_troop", slot_troop_occupation, slto_player_companion),
          (call_script, "script_dplmc_npc_morale", "$g_player_troop", 0), #overwrites s6,7,8, 63, so we should do this first
          (assign, reg1, reg0),
          (str_store_string, s2, "str_morale_reg1"),
          (call_script, "script_companion_get_mission_string", "$g_player_troop"),
          (str_store_string, s0, "@{s2}^{s8}^({s5})"), #discard s4 as name
        (else_try),
          (troop_slot_eq, "$g_player_troop", slot_troop_occupation, slto_kingdom_hero),
          (call_script, "script_troop_get_player_relation", "$g_player_troop"),
          (assign, reg1, reg0),
          (str_store_string, s2, "str_relation_reg1"),
          (str_clear, s0),
          (try_begin), #too lazy to get custom vassal titles, use the nicely formatted presets
            (call_script, "script_cf_dplmc_troop_is_female", "$g_player_troop"),
            (str_store_string, s1, "str_faction_title_female_player"),
          (else_try),
            (str_store_string, s1, "str_faction_title_male_player"),
          (try_end),
          (call_script, "script_print_troop_owned_centers_in_numbers_to_s0", "$g_player_troop"),
          (troop_get_slot, reg2, "$g_player_troop", slot_troop_renown),
          (str_store_string, s0, "@ Renown: {reg2}^{s2}^{s1}of {s0}"),
        (else_try),
          (str_clear, s0),
        (try_end),
        (str_store_troop_name, s4, "$g_player_troop"),
        (store_character_level, reg3, "$g_player_troop"),
        (store_troop_health, reg2, "$g_player_troop", 1),
        (call_script, "script_dplmc_get_troop_max_hp", "$g_player_troop"),
        (str_store_string, s1, "@Name: {s4}^Level: {reg3}^HP: {reg2}/{reg0}^^{s0}"),

        #if names are too long might need to warp
        (create_text_overlay, reg0, s1, tf_double_space),
        (position_set_x, pos1, 130),
        (position_set_y, pos1, 90),
        (overlay_set_position, reg0, pos1),

        #borrow cur_hero equipments from latest CC
        (create_mesh_overlay, reg1, "mesh_inventory_equipment_panel"),
        (position_set_x, pos1, 960),
        (position_set_y, pos1, 960),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 10),
        (position_set_y, pos1, 15),
        (overlay_set_position, reg1, pos1),

        (assign, ":init_pos_x", 219),
        (assign, ":init_pos_y", 683),
        (assign, ":cur_troop", "$g_player_troop"),

        # (create_combo_label_overlay, "$g_presentation_obj_admin_panel_1"),
        (store_add, ":pos_x", ":init_pos_x", 140),
        (store_add, ":pos_y", ":init_pos_y", 2),
        (position_set_x, pos1, 259),
        (position_set_y, pos1, ":init_pos_y"),
        (create_text_overlay, reg1, "@Arms", tf_center_justify),
        (overlay_set_position, reg1, pos1),
        # (position_set_x, pos1, 400),
        # (position_set_y, pos1, 750),
        # (overlay_set_size, "$g_presentation_obj_admin_panel_1", pos1),
        # (overlay_add_item, "$g_presentation_obj_admin_panel_1", "@Arms 1"),
        # (overlay_add_item, "$g_presentation_obj_admin_panel_1", "@Arms 2"),
        # (overlay_set_val, "$g_presentation_obj_admin_panel_1", "$g_weapons_set_no"),

        (create_text_overlay, reg1, "@Outfit", tf_center_justify),
        (store_add, ":pos_x", ":init_pos_x", -98),
        (store_add, ":pos_y", ":init_pos_y", 2),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),
        (create_text_overlay, reg1, "@Horse", tf_center_justify),
        (store_add, ":pos_x", ":init_pos_x", -140),
        (store_add, ":pos_y", ":init_pos_y", -278),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (overlay_set_position, reg1, pos1),

        (assign, "$g_current_opened_item_details", -1),

        (assign, ":pos_x", ":init_pos_x"),
        (assign, ":pos_y", ":init_pos_y"),
        (try_for_range, ":slot_no", ek_item_0, ek_food),
          (try_begin),
            (eq, ":slot_no", ek_head),
            (val_sub, ":pos_x", 96),
            (assign, ":pos_y", ":init_pos_y"),
          (else_try),
            (eq, ":slot_no", ek_gloves),
            (val_sub, ":pos_x", 84),
            (store_sub, ":pos_y", ":init_pos_y", 85),
          (else_try),
            (eq, ":slot_no", ek_horse),
            (val_sub, ":pos_y", 108),
          (try_end),
          (val_sub, ":pos_y", 85),

          (troop_get_inventory_slot, ":cur_item", ":cur_troop", ":slot_no"),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          # (overlay_set_position, reg1, pos1),
          # (overlay_set_color, reg1, 0x000000),
          # (try_begin), # alpha
            # (lt, ":cur_item", 0),
            # (overlay_set_alpha, reg1, 0x00),
          # (else_try),
            # (overlay_set_alpha, reg1, 0xFF),
          # (try_end),

          (try_begin), # item mesh
            (lt, ":cur_item", 0),
            (assign, ":cur_item", 0),
            (troop_set_slot, "trp_temp_array_c", ":slot_no", -1),
          (else_try),
            (create_mesh_overlay_with_item_id, reg1, ":cur_item"), #this has the problem of not respecting alternative imod meshes
            (position_set_x, pos1, 850),
            (position_set_y, pos1, 850),
            (overlay_set_size, reg1, pos1),
            (store_add, ":item_x", ":pos_x", 42),
            (store_add, ":item_y", ":pos_y", 42),
            (position_set_x, pos1, ":item_x"),
            (position_set_y, pos1, ":item_y"),
            (overlay_set_position, reg1, pos1),
            (troop_set_slot, "trp_temp_array_c", ":slot_no", reg1),
            # (troop_set_slot, "trp_temp_array_c", ":slot_no", 1), # can use

            # # action layer
            # (create_mesh_overlay, reg1, "mesh_white_plane"),
            # (position_set_x, pos1, 4150),
            # (position_set_y, pos1, 4150),
            # (overlay_set_size, reg1, pos1),
            # (position_set_x, pos1, ":pos_x"),
            # (position_set_y, pos1, ":pos_y"),
            # (overlay_set_position, reg1, pos1),
            # (overlay_set_alpha, reg1, 0x00),
            # (troop_set_slot, "trp_temp_array_b", ":slot_no", reg1),
          (try_end),
        (try_end),

        #so there's a bunch of whitespace between middle portion and top of screen, add some pictures I guess or strings
        #add backing mesh either mp_ui_welcome_panel or mp_ui_host_main
        #str_npcx_home_recap, npcx_signup_2, npcx_backstory_b etc
        (try_begin),
          (eq, "$g_player_troop", "trp_player"),
          (call_script, "script_build_background_answer_story", 0),
          (create_text_overlay, ":obj", s0, tf_scrollable_style_2),
        (else_try),
          (str_clear, s19), #so it doesn't say "here"
          (troop_get_slot, ":first_met", "$g_player_troop", slot_troop_first_encountered),
          (str_store_party_name, s20, ":first_met"),
          (troop_get_slot, ":home", "$g_player_troop", slot_troop_home),
          (str_store_party_name, s21, ":home"),
          (troop_get_slot, ":recap", "$g_player_troop", slot_troop_home_recap),
          (str_store_string, s5, ":recap"),
          (troop_get_slot, ":backstory", "$g_player_troop", slot_troop_backstory_b),
          (str_store_string, s6, ":backstory"),
          (troop_get_slot, ":signup", "$g_player_troop", slot_troop_signup_2),
          (str_store_string, s7, ":signup"),
          (create_text_overlay, ":obj", "@{s5}^^{s6}^^{s7}", tf_scrollable_style_2),
        (try_end),
        (position_set_x, pos1, 330),
        (position_set_y, pos1, 530),
        (overlay_set_position, ":obj", pos1),
        (position_set_x, pos1, 420),
        (position_set_y, pos1, 190),
        (overlay_set_area_size, ":obj", pos1),
        (position_set_x, pos1, 850),
        (position_set_y, pos1, 850),
        (overlay_set_size, ":obj", pos1),

        #first column : fixed length attribute + proficiencies
        (str_store_string, s3, "@Attributes:"),
        (store_attribute_level, reg1, "$g_player_troop", ca_strength),
        (store_attribute_level, reg2, "$g_player_troop", ca_agility),
        (store_attribute_level, reg3, "$g_player_troop", ca_intelligence),
        (store_attribute_level, reg4, "$g_player_troop", ca_charisma),
        (str_store_string, s3, "@{s3}^STR: {reg1}^AGI: {reg2}^INT: {reg3}^CHA: {reg4}"),
        (store_proficiency_level, reg1, "$g_player_troop", wpt_one_handed_weapon),
        (store_proficiency_level, reg2, "$g_player_troop", wpt_two_handed_weapon),
        (store_proficiency_level, reg3, "$g_player_troop", wpt_polearm),
        (store_proficiency_level, reg4, "$g_player_troop", wpt_archery),
        (store_proficiency_level, reg5, "$g_player_troop", wpt_crossbow),
        (store_proficiency_level, reg6, "$g_player_troop", wpt_throwing),
        #some of these strings are too long unfortunately
        # (str_store_string, s11, "str_dplmc_hero_wpn_slot_one_handed"),
        # (str_store_string, s12, "str_dplmc_hero_wpn_slot_two_handed"),
        (str_store_string, s13, "str_dplmc_hero_wpn_slot_polearm_all"),
        (str_store_string, s14, "str_dplmc_hero_wpn_slot_bow"),
        (str_store_string, s15, "str_dplmc_hero_wpn_slot_crossbow"),
        # (str_store_string, s16, "str_dplmc_hero_wpn_slot_throwing"),
        (str_store_string, s3, "@{s3}^^Proficiencies:^1H Weapons: {reg1}^2H Weapons: {reg2}^{s13}: {reg3}^{s14}: {reg4}^{s15}: {reg5}^Throwing: {reg6}"),

        (create_text_overlay, reg0, s3, tf_double_space),
        (position_set_x, pos1, 330),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),

        #second column: skills (include all of them greater than 0)
        (str_store_string, s4, "@Skills:"),
        (try_for_range_backwards, ":skill", skl_trade, skl_ironflesh + 1),
          (store_skill_level, reg1, ":skill", "$g_player_troop"),
          (gt, reg1, 0),
          (store_add, ":string", "str_skl_trade", ":skill"),
          (str_store_string, s1, ":string"),
          (str_store_string, s4, "@{s4}^{s1} : {reg1}"),
        (try_end),
        #if this list gets too long, exclude personal skills

        (create_text_overlay, reg0, s4, tf_double_space|tf_right_align),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),
        ################
      ]),

    ##show details
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),


      (try_for_range, ":item_slot", ek_item_0, ek_food),
        (troop_slot_eq, "trp_temp_array_c", ":item_slot", ":object"),
        (try_begin), #entering, show details
          (eq, ":enter_leave", 0),
          #find item
          (troop_get_inventory_slot, ":item_no", "$g_player_troop", ":item_slot"),
          (gt, ":item_no", -1),
          (troop_get_inventory_slot_modifier, ":imod_no", "$g_player_troop", ":item_slot"),
          (overlay_get_position, pos1, ":object"),
          (show_item_details_with_modifier, ":item_no", ":imod_no", pos1, 100),
        (else_try), #close it
          (eq, ":enter_leave", 1),
          (close_item_details),
        (try_end),
      (try_end),
      ]
    ),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),

        (try_begin), #tableau clicked
          (eq, ":object", "$g_presentation_obj_1"),
          (change_screen_notes, 1, "$g_player_troop"),
          # (presentation_set_duration, 0),
        (else_try), #done
          (eq, ":object", "$g_presentation_obj_2"),
          (presentation_set_duration, 0),
        (else_try), #export/import
          (eq, ":object", "$g_presentation_obj_3"),
          (assign, "$g_next_menu", "mnu_companion_report"),
          # (assign, "$auto_menu", "mnu_companion_report"),
          # (jump_to_menu, "mnu_auto_return_to_map"),
          (jump_to_menu, "mnu_export_import"),
          # (assign, "$talk_context", tc_town_talk),
          # (start_map_conversation, "$g_player_troop"),
          (set_player_troop, "$g_player_troop"),
          (presentation_set_duration, 0),
          # (change_screen_return),
        (else_try), #banner
          (eq, ":object", "$g_presentation_obj_4"),
          (assign, "$g_presentation_next_presentation", "prsnt_companion_overview"),
          (start_presentation, "prsnt_banner_selection"),
        (try_end),

        # (assign, ":num_of_heros", 0),
        # (try_begin),
          # (party_is_active, "$g_ally_party"),
          # (assign, ":party", "p_collective_friends"),
        # (else_try),
          # (assign, ":party", "p_main_party"),
        # (try_end),
        (try_for_range, ":stack_troop", active_npcs_including_player_begin, companions_end),
          (this_or_next|eq, ":stack_troop", active_npcs_including_player_begin), #player placeholder
          (this_or_next|troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
          (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_player_companion),

          (try_begin),
            (eq, ":stack_troop", active_npcs_including_player_begin),
            (assign, ":stack_troop", "trp_player"),
          (try_end),
          (troop_slot_eq, ":stack_troop", dplmc_slot_troop_temp_slot, ":object"),

          (assign, "$g_player_troop", ":stack_troop"),
          (start_presentation, "prsnt_companion_overview"),
        (try_end),
        # (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
        # (try_for_range, ":i_stack", 0, ":num_stacks"),
          # (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
          # (troop_is_hero, ":stack_troop"),
          # (neg|troop_is_wounded, ":stack_troop"),
          # (assign, ":trp_slot_prsnt_no", ":num_of_heros"),
          # (val_add, ":num_of_heros", 1),
          # (troop_slot_eq, "trp_temp_array_a", ":trp_slot_prsnt_no", ":object"),
          # (troop_get_slot, ":cur_troop", "trp_temp_array_b", ":trp_slot_prsnt_no"),
          # (assign, "$g_player_troop", ":cur_troop"),
          # (start_presentation, "prsnt_companion_overview"),
        # (try_end),
      ]),
    ])
