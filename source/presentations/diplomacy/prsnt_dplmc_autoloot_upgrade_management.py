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

dplmc_autoloot_upgrade_management = ("dplmc_autoloot_upgrade_management", 0, mesh_load_window, [
    (ti_on_presentation_load,
     [
      (set_fixed_point_multiplier, 1000),
      (presentation_set_duration, 999999),

      # done
      (create_game_button_overlay, "$g_presentation_obj_10", "str_done"),
      (position_set_x, pos1, 850),
      (position_set_y, pos1, 25),
      (overlay_set_position, "$g_presentation_obj_10", pos1),

      ## current hero
      # character picture
      (create_mesh_overlay_with_tableau_material, reg0, -1, "tableau_troop_note_mesh", "$temp"),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 500),
      (overlay_set_size, reg0, pos1),
      (position_set_x, pos1, 200),
      (position_set_y, pos1, 560),
      (overlay_set_position, reg0, pos1),

      (str_store_troop_name, s1, "$temp"),
      (store_character_level, reg2, "$temp"),
      (store_troop_health, reg1, "$temp", 1),
      (call_script, "script_dplmc_get_troop_max_hp", "$temp"),
      (str_store_string, s1, "@Name: {s1}^Level: {reg2}^HP: {reg1}/{reg0}"),


      (create_text_overlay, reg1, "@{s1}", tf_double_space),
      (position_set_x, pos1, 380),
      (position_set_y, pos1, 560),
      (overlay_set_position, reg1, pos1),

      # title
      (create_text_overlay, reg1, "@Weapon upgrade settings:", tf_center_justify|tf_vertical_align_center),
      (position_set_x, pos1, 445),
      (position_set_y, pos1, 530),
      (overlay_set_position, reg1, pos1),

      # init trp_temp_array_c
      (assign, ":sub_overlay_id", 0),
      (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        (eq, ":item_type", 0),
        (troop_set_slot, "trp_temp_array_c", ":sub_overlay_id", ":item_type"),
        (val_add, ":sub_overlay_id", 1),
      (try_end),


      # settings 1
      # set 1: wpn slot button
      (call_script, "script_create_wpn_slot_overlay", 0, 450),
      (assign, "$g_presentation_obj_1", reg1),

      (call_script, "script_create_wpn_slot_overlay", 1, 420),
      (assign, "$g_presentation_obj_2", reg1),

      (call_script, "script_create_wpn_slot_overlay", 2, 390),
      (assign, "$g_presentation_obj_3", reg1),

      (call_script, "script_create_wpn_slot_overlay", 3, 360),
      (assign, "$g_presentation_obj_4", reg1),

      # SB : damage types + meta type combo labels
      (create_combo_label_overlay, "$g_presentation_obj_sliders_1"),
      (overlay_add_item, "$g_presentation_obj_sliders_1", "str_dplmc_none"),

      (position_set_x, pos1, 465),
      (position_set_y, pos1, 450),
      (create_text_overlay, reg1, "@Damage preference", tf_single_line),
      (overlay_set_position, reg1, pos1),
      # (position_set_x, pos1, 600),
      (position_set_x, pos1, 600),
      (position_set_y, pos1, 420),
      (overlay_set_position, "$g_presentation_obj_sliders_1", pos1),
      (position_set_x, pos1, 800),
      (position_set_y, pos1, 750),
      (overlay_set_size, "$g_presentation_obj_sliders_1", pos1),
      (overlay_set_val, "$g_presentation_obj_sliders_1", 0), #by default
      # (overlay_set_alpha, "$g_presentation_obj_sliders_1", 0), #so apparently this only works for the text

      (position_set_x, pos1, 465),
      (position_set_y, pos1, 390),
      (create_text_overlay, reg1, "@Item meta-type", tf_single_line),
      (overlay_set_position, reg1, pos1),

      (position_set_x, pos1, 600),
      (position_set_y, pos1, 360),
      (create_combo_label_overlay, "$g_presentation_obj_sliders_2"),
      (overlay_set_position, "$g_presentation_obj_sliders_2", pos1),
      # (position_set_x, pos1, 600),
      (position_set_x, pos1, 800),
      (position_set_y, pos1, 750),
      (overlay_set_size, "$g_presentation_obj_sliders_2", pos1),
      (overlay_add_item, "$g_presentation_obj_sliders_2", "str_dplmc_hero_wpn_slot_no_metatype"),
      (overlay_set_val, "$g_presentation_obj_sliders_2", 0), #by default

      (assign, ":slot_value", -1),
      (assign, ":meta_value", -1),
      (assign, ":icon", -1),
      (try_begin), #set values here
        (neq, "$temp_2", -1),
        (troop_get_slot, ":slot_value", "$temp", "$temp_2"),
        (store_div, ":dmg_type", ":slot_value", meta_dmg_mask),
        (store_mod, ":meta_value", ":slot_value", meta_dmg_mask),
        (val_mod, ":slot_value", meta_itp_mask),

        (try_begin), #populate damage type slider
          (call_script, "script_cf_item_type_has_advanced_autoloot", ":slot_value"),
          (overlay_add_item, "$g_presentation_obj_sliders_1", "@cut"),
          (overlay_add_item, "$g_presentation_obj_sliders_1", "@pierce"),
          (overlay_add_item, "$g_presentation_obj_sliders_1", "@blunt"),
        (try_end),
        (overlay_set_val, "$g_presentation_obj_sliders_1", ":dmg_type"),
        # (overlay_set_alpha, "$g_presentation_obj_sliders_1", 0xff),
      (try_end),
      #populate slider with values, tooltip unnecessary since icons are directly below label
      (try_begin),
        (eq, ":slot_value", itp_type_polearm),
        (overlay_add_item, "$g_presentation_obj_sliders_2", "str_dplmc_hero_wpn_slot_lance"),
        (overlay_add_item, "$g_presentation_obj_sliders_2", "str_dplmc_hero_wpn_slot_pikes"),
        (overlay_add_item, "$g_presentation_obj_sliders_2", "str_dplmc_hero_wpn_slot_halberd"),
        (try_begin),
          (eq, ":meta_value", dplmc_itp_lance),
          (overlay_set_val, "$g_presentation_obj_sliders_2", 1),
          (assign, ":icon", "mesh_icon_lance"),
        (else_try),
          (eq, ":meta_value", dplmc_itp_pike),
          (overlay_set_val, "$g_presentation_obj_sliders_2", 2),
          (assign, ":icon", "mesh_icon_spear"),
        (else_try),
          (eq, ":meta_value", dplmc_itp_halberd),
          (overlay_set_val, "$g_presentation_obj_sliders_2", 3),
          (assign, ":icon", "mesh_icon_bardiche"),
        (try_end),
      (else_try),
        (eq, ":slot_value", itp_type_two_handed_wpn),
        (overlay_add_item, "$g_presentation_obj_sliders_2", "str_dplmc_hero_wpn_slot_morningstar"),
        (try_begin),
          (eq, ":meta_value", dplmc_itp_morningstar),
          (assign, ":icon", "mesh_icon_morningstar"),
          (overlay_set_val, "$g_presentation_obj_sliders_2", 1),
        (try_end),
      (try_end),

      #add icons
      (try_begin),
        (neq, ":icon", -1),
        (create_mesh_overlay, "$g_presentation_obj_sliders_2_val", ":icon"),
        (position_set_x, pos1, 560),
        (position_set_y, pos1, 325),
        (overlay_set_position, "$g_presentation_obj_sliders_2_val", pos1),
      (else_try), #create it anyway, but keep it blank
        (create_mesh_overlay, "$g_presentation_obj_sliders_2_val", "mesh_white_plane"),
        (overlay_set_alpha, "$g_presentation_obj_sliders_2_val", 0),
      (try_end),

      #do inventory polling, draw backing grid
      (init_position, pos2),
      (init_position, pos3),

      (assign, ":cur_x", 75),
      (position_set_y, pos1, 200),
      #downscale base meshes by 75%, bounding box by 60%
      (position_set_x, pos2, 600),
      (position_set_y, pos2, 600),
      (position_set_x, pos3, 750),
      (position_set_y, pos3, 750),
      # (store_sub, ":cur_slot", "$temp_2", dplmc_slot_upgrade_wpn_0),

      #exclude weapons, there's already objects for them
      (try_for_range, ":item_slot", ek_head, ek_food),
        (assign, ":inventory_mesh", "mesh_mp_inventory_choose"), #default bordered square
        (try_begin),
          # (is_between, ":item_slot", ek_item_0, ek_head),
          # (try_begin),
            # (eq, ":cur_slot", ":item_slot"),
            # (assign, ":inventory_mesh", "mesh_mp_inventory_choose"),
          # (else_try),
            # (assign, ":inventory_mesh", "mesh_mp_inventory_slot_equip"),
          # (try_end),
        # (else_try), #would be easier if they were in order
          (eq, ":item_slot", ek_horse),
          (troop_slot_ge, "$temp", dplmc_slot_upgrade_horse, 1),
          (assign, ":inventory_mesh", "mesh_mp_inventory_slot_horse"),
        (else_try),
          # (is_between, ":item_slot", ek_head, ek_horse),
          (troop_slot_ge, "$temp", dplmc_slot_upgrade_armor, 1),
          (try_begin),
            (eq, ":item_slot", ek_head),
            (assign, ":inventory_mesh", "mesh_mp_inventory_slot_helmet"),
          (else_try),
            (eq, ":item_slot", ek_body),
            (assign, ":inventory_mesh", "mesh_mp_inventory_slot_armor"),
          (else_try),
            (eq, ":item_slot", ek_foot),
            (assign, ":inventory_mesh", "mesh_mp_inventory_slot_boot"),
          (else_try),
            (eq, ":item_slot", ek_gloves),
            (assign, ":inventory_mesh", "mesh_mp_inventory_slot_glove"),
          (try_end),
        (try_end),
        (create_mesh_overlay, reg1, ":inventory_mesh"),
        (position_set_x, pos1, ":cur_x"),
        (position_set_y, pos1, 200),
        (overlay_set_position, reg1, pos1),
        (overlay_set_size, reg1, pos2),
        (overlay_set_alpha, reg1, 0x99), #reduce visibility to 60%
        (try_begin), #fetch actual item
          (troop_get_inventory_slot, ":item", "$temp", ":item_slot"),
          (gt, ":item", 0),
          (create_mesh_overlay_with_item_id, reg1, ":item"),
          # (store_add, ":item_x", ":cur_x", 50),
          (store_add, ":item_x", ":cur_x", 37),
          (position_set_x, pos1, ":item_x"),
          (position_set_y, pos1, 200 + 37),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos3),
          #store item object for mouseover effect
          (troop_set_slot, "trp_stack_selection_ids", ":item_slot", reg1),
        (try_end),
        (val_add, ":cur_x", 75),
      (try_end),

      # (position_set_y, pos1, 360),
      # (create_combo_button_overlay, "$g_presentation_obj_4"),
      # (overlay_set_position, "$g_presentation_obj_4", pos1),
      # (assign, ":sub_overlay_id", 0),
      # (call_script, "script_dplmc_get_current_item_for_autoloot", 3),
      # (try_for_range_backwards, ":item_type", 0, itp_type_animal),
        # (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
        # (this_or_next|is_between, ":item_type", itp_type_pistol, itp_type_animal),
        # (eq, ":item_type", 0),
        # (store_add, ":out_string", "str_dplmc_hero_wpn_slot_none", ":item_type"),
        # (str_store_string, s0, ":out_string"),
        # (overlay_add_item, "$g_presentation_obj_4", s0),
        # (try_begin),
          # (troop_slot_eq, "$temp", dplmc_slot_upgrade_wpn_3, ":item_type"),
          # (overlay_set_val, "$g_presentation_obj_4", ":sub_overlay_id"),
        # (try_end),
        # (val_add, ":sub_overlay_id", 1),
      # (try_end),

      (position_set_x, pos1, 1000),
      (position_set_y, pos1, 800),
      (overlay_set_size, "$g_presentation_obj_1", pos1),
      (overlay_set_size, "$g_presentation_obj_2", pos1),
      (overlay_set_size, "$g_presentation_obj_3", pos1),
      (overlay_set_size, "$g_presentation_obj_4", pos1),
      # set 1: apply to all
      (position_set_x, pos1, 128),
      (position_set_y, pos1, 310),
      (create_image_button_overlay, "$g_presentation_obj_11", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_11", pos1),
      (position_set_x, pos1, 270),
      (position_set_y, pos1, 325),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),

      # upgrade armor and horse
      # text
      (position_set_x, pos1, 300),
      (position_set_y, pos1, 155),
      (create_text_overlay, reg1, "@Upgrade armor", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      (position_set_y, pos1, 105),
      (create_text_overlay, reg1, "@Upgrade horse", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      # checkbox
      (position_set_x, pos1, 180),
      (position_set_y, pos1, 148),
      (create_check_box_overlay, "$g_presentation_obj_13", "mesh_checkbox_off", "mesh_checkbox_on"),
      (overlay_set_position, "$g_presentation_obj_13", pos1),
      (troop_get_slot,":upg_armor", "$temp",dplmc_slot_upgrade_armor),
      (overlay_set_val, "$g_presentation_obj_13", ":upg_armor"),
      (position_set_y, pos1, 98),
      (create_check_box_overlay, "$g_presentation_obj_14", "mesh_checkbox_off", "mesh_checkbox_on"),
      (overlay_set_position, "$g_presentation_obj_14", pos1),
      (troop_get_slot,":upg_horse", "$temp",dplmc_slot_upgrade_horse),
      (overlay_set_val, "$g_presentation_obj_14", ":upg_horse"),
      # long button
      (position_set_x, pos1, 418),
      (position_set_y, pos1, 140),
      (create_image_button_overlay, "$g_presentation_obj_15", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_15", pos1),
      (position_set_y, pos1, 90),
      (create_image_button_overlay, "$g_presentation_obj_16", "mesh_longer_button", "mesh_longer_button_down"),
      (overlay_set_position, "$g_presentation_obj_16", pos1),
      (position_set_x, pos1, 560),
      (position_set_y, pos1, 155),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),
      (position_set_y, pos1, 105),
      (create_text_overlay, reg1, "@Apply to everyone", tf_center_justify|tf_vertical_align_center),
      (overlay_set_position, reg1, pos1),

      # hero list
      #TODO: Add pagination in case the player has a lot of companions. Possible if they recruit all tavern companions and have polygamy
      #Might also want to move this column a bit, as long spouse names crash with the border
      (assign, ":pos_x", 850),
      (assign, ":pos_y", 600),
      (assign, ":num_of_heros", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
        (assign, ":is_spouse", 0),
        (try_begin),
          (is_between, ":stack_troop", heroes_begin, heroes_end),
          (troop_slot_eq, ":stack_troop", slot_troop_spouse, "trp_player"),
          (assign, ":is_spouse", 1),
        (try_end),
        (this_or_next|eq, ":is_spouse", 1),
        (this_or_next|is_between, ":stack_troop", pretenders_begin, pretenders_end),
        (is_between, ":stack_troop", companions_begin, companions_end),
        (str_store_troop_name, s1, ":stack_troop"),
        (position_set_x, pos1, ":pos_x"),
        (position_set_y, pos1, ":pos_y"),
        (val_sub, ":pos_y", 30),
        (create_button_overlay, reg0, s1, tf_center_justify|tf_vertical_align_center),
        (overlay_set_position, reg0, pos1),

        (assign, ":trp_slot_prsnt_no", ":num_of_heros"),
        (troop_set_slot, "trp_temp_array_a", ":trp_slot_prsnt_no", reg0),
        (troop_set_slot, "trp_temp_array_b", ":trp_slot_prsnt_no", ":stack_troop"),
        (val_add, ":num_of_heros", 1),
      (try_end),
#      ####### mouse fix pos system #######
#      (call_script, "script_mouse_fix_pos_ready"),
#      ####### mouse fix pos system #######
     ]),

#    (ti_on_presentation_run,
#      [
#      ####### mouse fix pos system #######
#      (call_script, "script_mouse_fix_pos_run"),
#      ####### mouse fix pos system #######
#    ]),


    ## Mouse-over, iterate through objects in trp_stack_selection_ids
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),


      (try_for_range, ":item_slot", ek_item_0, ek_food),
        (troop_slot_eq, "trp_stack_selection_ids", ":item_slot", ":object"),
        (try_begin), #entering, show details
          (eq, ":enter_leave", 0),
          #find item
          (troop_get_inventory_slot, ":item_no", "$temp", ":item_slot"),
          (gt, ":item_no", -1),
          (troop_get_inventory_slot_modifier, ":imod_no", "$temp", ":item_slot"),
          (set_fixed_point_multiplier, 1000),
          (position_set_x, pos1, 560),
          (position_set_y, pos1, 310),
          (show_item_details_with_modifier, ":item_no", ":imod_no", pos1, 100),
        (else_try), #close it
          (eq, ":enter_leave", 1),
          (close_item_details),
        (try_end),
      (try_end),
      ]
    ),
    # # meta-type selector based on which combobox was last touched
    # (ti_on_presentation_mouse_press,
      # [ (store_trigger_param_1, ":object"),
        # (store_trigger_param_2, ":mouse_state"),

        # (try_begin),
          # #technically they should be sequential, but w/e
          # (eq, ":mouse_state", 0),
          # (try_begin),
            # (eq, ":object", "$g_presentation_obj_1"),
            # (assign, "$temp_2", dplmc_slot_upgrade_wpn_0),
          # (else_try),
            # (eq, ":object", "$g_presentation_obj_2"),
            # (assign, "$temp_2", dplmc_slot_upgrade_wpn_1),
          # (else_try),
            # (eq, ":object", "$g_presentation_obj_3"),
            # (assign, "$temp_2", dplmc_slot_upgrade_wpn_2),
          # (else_try),
            # (eq, ":object", "$g_presentation_obj_4"),
            # (assign, "$temp_2", dplmc_slot_upgrade_wpn_3),
          # (try_end),
        # (try_end),

      # ]
    # ),

    (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (call_script, "script_update_wpn_slot_itp", dplmc_slot_upgrade_wpn_0, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (call_script, "script_update_wpn_slot_itp", dplmc_slot_upgrade_wpn_1, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (call_script, "script_update_wpn_slot_itp", dplmc_slot_upgrade_wpn_2, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_4"),
          (call_script, "script_update_wpn_slot_itp", dplmc_slot_upgrade_wpn_3, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),
          (presentation_set_duration, 0),
        (else_try),
          (eq, ":object", "$g_presentation_obj_11"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_wpn_setting_1),
        (else_try),
          (eq, ":object", "$g_presentation_obj_13"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_armor, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_14"),
          (troop_set_slot, "$temp", dplmc_slot_upgrade_horse, ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_15"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_armor_setting),
        (else_try),
          (eq, ":object", "$g_presentation_obj_16"),
          (call_script, "script_dplmc_copy_upgrade_to_all_heroes", "$temp", dplmc_horse_setting),
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_1"), #damage type
          (is_between, "$temp_2", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1), #valid range
          (store_mul, ":slot_value", ":value", meta_dmg_mask),
          (troop_get_slot, ":cur_value", "$temp", "$temp_2"),
          (val_mod, ":cur_value", meta_dmg_mask), #unmask
          (val_add, ":slot_value", ":cur_value"),
          (troop_set_slot, "$temp", "$temp_2", ":slot_value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_2"), #meta-type combo label
          (is_between, "$temp_2", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1), #valid range
          (store_mul, ":slot_value", ":value", meta_itp_mask),
          (troop_get_slot, ":cur_value", "$temp", "$temp_2"),

          #get lower bits
          (store_mod, ":item_type", ":cur_value", meta_itp_mask),
          (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
          (val_add, ":slot_value", ":item_type"), #base type
          #get icon at this point
          (overlay_set_alpha, "$g_presentation_obj_sliders_2_val", 0),
          (try_begin),
            (eq, ":slot_value", dplmc_itp_morningstar),
            (assign, ":icon", "mesh_icon_morningstar"),
          (else_try),
            (this_or_next|eq, ":slot_value", dplmc_itp_lance),
            (this_or_next|eq, ":slot_value", dplmc_itp_pike),
            (eq, ":slot_value", dplmc_itp_halberd),
            (store_add, ":icon", "mesh_icon_morningstar", ":value"), #1 to 3
          (else_try),
            (assign, ":icon", -1),
          (try_end),
          #get higher bits
          (val_div, ":cur_value", meta_dmg_mask),
          (val_mul, ":cur_value", meta_dmg_mask),
          (val_add, ":slot_value", ":cur_value"),

          (troop_set_slot, "$temp", "$temp_2", ":slot_value"),

          (try_begin), #replacing old icon
            (gt, ":icon", 0),
            (set_fixed_point_multiplier, 1000),
            (create_mesh_overlay, reg1, ":icon"),
            (position_set_x, pos1, 560),
            (position_set_y, pos1, 325),
            (overlay_set_position, reg1, pos1),
            (assign, "$g_presentation_obj_sliders_2_val", reg1),
          (try_end),
        (try_end),

        (assign, ":num_of_heros", 0),
        (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id,":stack_troop","p_main_party",":i_stack"),
          (assign, ":is_spouse", 0),
          (try_begin),
            (is_between, ":stack_troop", heroes_begin, heroes_end),
            (troop_slot_eq, ":stack_troop", slot_troop_spouse, "trp_player"),
            (assign, ":is_spouse", 1),
          (try_end),
          (this_or_next|eq, ":is_spouse", 1),
          (this_or_next|is_between, ":stack_troop", pretenders_begin, pretenders_end),
          (is_between, ":stack_troop", companions_begin, companions_end),
          (assign, ":trp_slot_prsnt_no", ":num_of_heros"),
          (val_add, ":num_of_heros", 1),
          (troop_slot_eq, "trp_temp_array_a", ":trp_slot_prsnt_no", ":object"),
          (troop_get_slot, ":cur_troop", "trp_temp_array_b", ":trp_slot_prsnt_no"),
          (assign, "$lord_selected", ":cur_troop"),
          (assign, "$temp", ":cur_troop"),
          (set_player_troop, ":cur_troop"), # SB : set troop here, restore on exit
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        (try_end),
    ]),
  ])
