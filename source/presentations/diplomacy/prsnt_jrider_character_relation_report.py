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

jrider_character_relation_report = ("jrider_character_relation_report", 0,
   mesh_message_window,
   [
     ## Load Presentation
     (ti_on_presentation_load,
      # generic_ti_on_load +
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (str_clear, s0),
        (str_clear, s1),

        # Character presentation type variations
        (try_begin),
            ###############################
            ## Courtship Relations presentation
            (eq, "$g_character_presentation_type", 0),

            # Set presentation title string
            (str_store_string, s0, "@_Courtships in progress_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 160),
            (assign, ":base_scroll_size_y", 480),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 430

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 1000),

            # presentation specific extra overlays
            (call_script, "script_generate_known_poems_string"),

            # Extra text area for knowns poems (filling once so we use a register), filled from s1 generated in script call
            (create_text_overlay, reg1, s1, tf_left_align),
            (position_set_x, pos1, 590), # position
            (position_set_y, pos1, 55),
            (overlay_set_position, reg1, pos1),
            (position_set_x, pos1, 750), # size
            (position_set_y, pos1, 850),
            (overlay_set_size, reg1, pos1),
            (overlay_set_color, reg1, 0xFF66CC), # color
        (else_try),
            ###############################
            ## Lord Relations presentation
            (eq, "$g_character_presentation_type", 1),

            # Set presentation title string
            (str_store_string, s0, "@_Known Lords by Relation_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550),
            (assign, ":base_candidates_y", 0), # scrollable area size minus 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 2000),
        (else_try),
            ###############################
            ## Player and Companions presentation
            (eq, "$g_character_presentation_type", 2),

            # Set presentation title string
            (str_store_string, s0, "@_Character & Companions_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 3000),

            # Extra area for equipment display
            (assign, ":inv_bar_size", 0),
            (position_set_x, ":inv_bar_size", 400),
            (position_set_y, ":inv_bar_size", 400),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_left"),
            (position_set_x, pos1, 67),
            (position_set_y, pos1, 300),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_right"),
            (position_set_x, pos1, 450),
            (position_set_y, pos1, 330),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),
        (try_end),
        # END of presentation type specific init and static overlay

        ###############################
        # Create common overlays
        # set foreground mesh overlay (has some transparency in it, so can't use it directly)
        (create_mesh_overlay, reg1, "mesh_face_gen_window"),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1000),
        (position_set_y, pos1, 1000),
    (overlay_set_size, reg1, pos1),

    # Presentation title overlay, centered at the top of right pane (from s0, presentation type specific)
        (create_text_overlay, reg1, s0, tf_center_justify),
        (overlay_set_color, reg1, 0xDDDDDD),
    (position_set_x, pos1, 740), # Higher, means more toward the right
        (position_set_y, pos1, 680), # Higher, means more toward the top
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
        (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),

    # Done button
        (create_game_button_overlay, "$g_jrider_faction_report_return_to_menu", "@_Done_"),
        (position_set_x, pos1, 290),
        (position_set_y, pos1, 10),
        (overlay_set_position, "$g_jrider_faction_report_return_to_menu", pos1),

        # Character Information text to fill when an entry is clicked in the list
        (create_text_overlay, "$g_jrider_character_information_text", "str_space", tf_left_align),
        (overlay_set_color, "$g_jrider_character_information_text", 0xFFFFFF),
        (position_set_x, pos1, 55), # Higher, means more toward the right
        (position_set_y, pos1, 60), # Higher, means more toward the top
        (overlay_set_position, "$g_jrider_character_information_text", pos1),
        (position_set_x, pos1, 700), # smaller means smaller font
        (position_set_y, pos1, 800),
        (overlay_set_size, "$g_jrider_character_information_text", pos1),

        # Character selection listbox overlay
        # use scrollable text area with global reference so objects can be put inside using overlay_set_container
        (create_text_overlay, "$g_jrider_character_relation_listbox", "str_empty_string", tf_scrollable_style_2),
        (position_set_x, pos1, 590),
        (position_set_y, pos1, ":base_scroll_y"),
        (overlay_set_position, "$g_jrider_character_relation_listbox", pos1),
        (position_set_x, pos1, 335),
        (position_set_y, pos1, ":base_scroll_size_y"),
        (overlay_set_area_size, "$g_jrider_character_relation_listbox", pos1),

        # Faction filter
        (create_combo_button_overlay, "$g_jrider_character_faction_filter", "str_empty_string",0),
        (position_set_x, pos1, 507),
        (position_set_y, pos1, 709),
        (overlay_set_position, "$g_jrider_character_faction_filter", pos1),
        (position_set_x, pos1, 550),
        (position_set_y, pos1, 650),
        (overlay_set_size, "$g_jrider_character_faction_filter", pos1),

        # add elements to filter button
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Your supporters"),
        (try_for_range, ":faction_no", npc_kingdoms_begin, kingdoms_end), #SB : add loop
          (call_script, "script_faction_get_adjective_to_s10", ":faction_no"),
          (overlay_add_item, "$g_jrider_character_faction_filter", "@{s10}s"),
        (try_end),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Swadians"),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Vaegirs"),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Khergits"),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Nords"),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Rhodoks"),
        # (overlay_add_item, "$g_jrider_character_faction_filter", "@Sarranids"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@All Factions"),

        # Set initial value for selection box
        (try_begin),
            (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
            (eq, "$g_jrider_faction_filter", -1),

            (assign, "$g_jrider_faction_filter", -1),
            (overlay_set_val, "$g_jrider_character_faction_filter", 7),
        (else_try),
            (overlay_set_val, "$g_jrider_character_faction_filter", "$g_jrider_faction_filter"),
        (try_end),

        ###############################
        # Populate lists
        # Init presentation common global variables
        (assign, "$num_charinfo_candidates", 0),

        # Fill listbox (overlay_add_item and extra storage)
        (call_script, "script_fill_relation_canditate_list_for_presentation", "$g_character_presentation_type", ":base_candidates_y"),
        (assign, "$g_jrider_reset_selected_on_faction", 0),
        # stop if there's no candidate
        (gt, "$num_charinfo_candidates", 0),

        # get extra information from storage
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$g_latest_character_relation_entry"),
        (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":current_storage_index"),

        # Fill text information for current entry and update text information overlay
        (call_script, "script_generate_extended_troop_relation_information_string", "$character_info_id"),
        (overlay_set_text, "$g_jrider_character_information_text", s1),

        # color selected entry
        (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
        (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

        # Begin common dynamic overlay
        # mesh Overlay for character portrait (global not needed)
        (create_image_button_overlay_with_tableau_material, "$g_jrider_character_portrait", -1, "tableau_troop_note_mesh", "$character_info_id"),
        (position_set_x, pos2, 100),
        (position_set_y, pos2, 280),
        (overlay_set_position, "$g_jrider_character_portrait", pos2),
        (position_set_x, pos2, 1100), #1150
        (position_set_y, pos2, 1100), #1150
        (overlay_set_size, "$g_jrider_character_portrait", pos2),

        # mesh Overlay for faction coat of arms
        (try_begin),
            (store_troop_faction, ":troop_faction", "$character_info_id"),
            (neq, ":troop_faction", "fac_player_supporters_faction"),
            (is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
            (store_sub, ":faction_mesh_index", ":troop_faction", kingdoms_begin),
            (val_add, ":faction_mesh_index", "mesh_pic_recruits"),

            (create_mesh_overlay, "$g_jrider_faction_coat_of_arms", ":faction_mesh_index"),
            (position_set_x, pos3, 150),
            (position_set_y, pos3, 600),
            (overlay_set_position, "$g_jrider_faction_coat_of_arms", pos3),
            (position_set_x, pos3, 250),
            (position_set_y, pos3, 250),
            (overlay_set_size, "$g_jrider_faction_coat_of_arms", pos3),
        (try_end),

        # Begin presentation type specific dynamic overlay
        # equipement meshes for character/companions
        (try_begin),
            (eq, "$g_character_presentation_type", 2),

            (assign, ":base_inv_slot_x", 452),
            (assign, ":base_inv_slot_y", 536),

            (try_for_range, ":item_eq", 0, 9),
            # loop equipment slots
                (troop_get_inventory_slot, reg1, "$character_info_id", ":item_eq"),

                (try_begin),
                    (eq, ":item_eq", 4),
                    (assign, ":base_inv_slot_x", 68),
                    (assign, ":base_inv_slot_y", 557),
                (try_end),
                (try_begin),
                    (lt, reg1, 1),
                    # empty... assign default mesh
                   (try_begin),
                       (lt, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_equip"),
                   (else_try),
                       (eq, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_helmet"),
                   (else_try),
                       (eq, ":item_eq", 5),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_armor"),
                   (else_try),
                       (eq, ":item_eq", 6),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_boot"),
                   (else_try),
                       (eq, ":item_eq", 7),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_glove"),
                   (else_try),
                       (eq, ":item_eq", 8),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_horse"),
                   (try_end),

                   (create_mesh_overlay, reg11, ":mesh_id"),
                   (overlay_set_size, reg11, ":inv_bar_size"),

                   (position_set_x, pos1, ":base_inv_slot_x"),
                   (position_set_y, pos1, ":base_inv_slot_y"),
                   (overlay_set_position, reg11, pos1),

                   (troop_set_slot, "trp_temp_array_a", ":item_eq", -1),
                   (store_add, ":item_eq_id", ":item_eq", 10),
                   (troop_set_slot, "trp_temp_array_a", ":item_eq_id", -1),
                # end missing item
                (else_try),
                    (create_mesh_overlay_with_item_id, reg10, reg1),
                    (position_set_x, pos1, 450),
                    (position_set_y, pos1, 450),
                    (overlay_set_size, reg10, pos1),

                    (store_add, ":item_inv_slot_x", ":base_inv_slot_x", 25),
                    (store_add, ":item_inv_slot_y", ":base_inv_slot_y", 25),

                    (position_set_x, pos1, ":item_inv_slot_x"),
                    (position_set_y, pos1, ":item_inv_slot_y"),
                    (overlay_set_position, reg10, pos1),

                    # save id for reuse
                    (troop_set_slot, "trp_temp_array_a", ":item_eq", reg10),
                    (store_add, ":item_eq_id", ":item_eq", 10),
                    (troop_set_slot, "trp_temp_array_a", ":item_eq_id", reg1),
                # real items
                (try_end),
                (val_sub, ":base_inv_slot_y", 51),
            (try_end),
            # end loop equipments slots
        (try_end),

        # do an update if called from menu and reset init variable
        (try_begin),
            (eq, "$g_jrider_pres_called_from_menu", 1),
            (assign, "$g_jrider_pres_called_from_menu", 0),
        (try_end),
    ]),
    # end presentation load

    ## Mouse-over
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
          (eq, "$g_character_presentation_type", 2),
          (try_begin),
              (eq, ":enter_leave", 0),
              (try_for_range, ":slot_no", 0, 9),
                  (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                  (store_add, ":slot_no_eq", ":slot_no", 10),
                  (troop_get_slot, ":item_no", "trp_temp_array_a", ":slot_no_eq"),

                  (set_fixed_point_multiplier, 1000),

                  (position_set_x,pos0,740),
                  (position_set_y,pos0,235),
          (show_item_details_with_modifier, ":item_no", "$g_all_items_imod", pos0, 100),
              (try_end),
          (else_try),
              (try_for_range, ":slot_no", 0, 9),
                (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                (close_item_details),
              (try_end),
          (try_end),
      (try_end),
    ]),
    # end mouseover

    ## Check for buttonpress
    (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"), # object
        (store_trigger_param_2, ":value"),  # value

        (try_begin),
            # pressed  (Return to menu)
            (eq, ":object", "$g_jrider_faction_report_return_to_menu"),

            (try_begin),
                (neq, "$num_charinfo_candidates", 0),
                (overlay_set_text, "$g_jrider_character_information_text", "str_empty_string"),
                (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (try_end),
            (presentation_set_duration, 0),

        (else_try),
            # Faction filter
            (eq, ":object", "$g_jrider_character_faction_filter"),
            (try_begin),
                (eq, ":value", 7),
                (assign, "$g_jrider_faction_filter", -1),
            (else_try),
                (assign, "$g_jrider_faction_filter", ":value"),
            (try_end),

            # reset selected to first
            (assign, "$g_jrider_reset_selected_on_faction", 1000),

            # restart presentation to take filters into account
            (start_presentation, "prsnt_jrider_character_relation_report"),

        (else_try),
            (neq, ":object", "$g_jrider_character_information_text"),
            (neq, ":object", "$g_jrider_character_portrait"),
            (neq, ":object", "$g_jrider_character_relation_listbox"),
            #(neq, ":object", "$g_jrider_faction_coat_of_arms"),
            # clicked on list entry
            # get storage index + base storage index
            (store_add, ":storage_button_id", ":object", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, ":character_number", "trp_temp_array_b", ":storage_button_id"),

            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xDDDDDD),

            # update last entry and check variables
            (assign, "$g_latest_character_relation_entry", ":character_number"),
            (assign, "$g_jrider_last_checked_indicator", ":object"),

            # color selected entry
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

            # get troop information from storage to update text
            (val_add, ":character_number", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":character_number"),

            # restart presentation to update picture and text
            (start_presentation, "prsnt_jrider_character_relation_report"),
    (try_end),
     ] # + generic_ti_on_presentation_event_state_change
     ),
     # end event state change

    ## Event to process when running the presentation
    (ti_on_presentation_run,
     # generic_ti_on_presentation_run +
     [
        (try_begin),
          (this_or_next|key_clicked, key_escape),
          (key_clicked, key_right_mouse_button),
          (presentation_set_duration, 0),
          (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
     # end presentation run
     ])
