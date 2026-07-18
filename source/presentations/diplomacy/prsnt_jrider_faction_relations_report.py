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

jrider_faction_relations_report = ("jrider_faction_relations_report", 0,
   mesh_message_window,
   [
     (ti_on_presentation_load,
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        # Embed picture upper right
        (create_mesh_overlay, reg1, "mesh_pic_castledes"),
        (position_set_x, pos1, 180),
        (position_set_y, pos1, 180),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 795),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

        # Embed picture upper left
        (create_mesh_overlay, reg1, "mesh_pic_looted_village"),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 170),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, -15),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

    # Presentation title, centered at the top
        (create_text_overlay, reg1, "@_Faction Relations Report_", tf_center_justify),
    (position_set_x, pos1, 500), # Higher, means more toward the right
        (position_set_y, pos1, 670), # Higher, means more toward the top
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1500),
        (position_set_y, pos1, 1500),
    (overlay_set_size, reg1, pos1),

    # Back to menu - graphical button
    (create_game_button_overlay, reg1, "@_Return to menu_"),
    (position_set_x, pos1, 500),
        (position_set_y, pos1, 23),
        (overlay_set_position, reg1, pos1),
        (assign, "$g_jrider_faction_report_return_to_menu", reg1),

    # Set Headlines
#set column title
          (assign, ":x_poshl", 250),
          (assign, ":y_pos", 620),
          (position_set_y, pos1, ":y_pos"),
    (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction", slot_faction_state, sfs_active), # continue if active
            (try_begin),
              (is_between, ":faction", npc_kingdoms_begin, npc_kingdoms_end),
              (store_sub, ":offset", ":faction", "fac_kingdom_1"),
              (val_add, ":offset", "str_swadians"),
              (str_store_string, s1, ":offset"),
            (else_try),
              (str_store_string, s1, "@Your kingdom"),
            (try_end),

            (str_store_string, s11, ":offset"),
            (create_text_overlay, reg10, s1, tf_left_align|tf_with_outline),
            (faction_get_color, ":faction_color", ":faction"),
            (overlay_set_color, reg10, ":faction_color"),

            (position_set_x, pos3, 650),
            (position_set_y, pos3, 800),
            (overlay_set_size, reg10, pos3),

            (position_set_x, pos1, ":x_poshl"),
            (overlay_set_position, reg10, pos1),
            (val_add, ":x_poshl", 90),
    (try_end),


    (assign, ":x_poshl", 215),
     (assign, ":y_pos", 597),
     (assign, ":headline_size", 0),
    (position_set_x, ":headline_size", 720),
        (position_set_y, ":headline_size", 775),

        (assign, ":hl_columnsep_size", 50),
        (position_set_x, ":hl_columnsep_size", 60),
        (position_set_y, ":hl_columnsep_size", 28000),

        (create_text_overlay, reg2, "@Player^Relation", tf_center_justify),
        (overlay_set_size, reg2, ":headline_size"),
        (position_set_x, pos1, ":x_poshl"),
        (position_set_y, pos1, ":y_pos"),
        (overlay_set_position, reg2, pos1),

        (val_add, ":x_poshl", 45),
        (try_for_range, ":count", 0, 7),
          # create a separator column
          (create_mesh_overlay, reg1, "mesh_white_plane"),
          (overlay_set_color, reg1, 0x000000),
          (overlay_set_size, reg1, ":hl_columnsep_size"),
          (store_sub, ":line_x", ":x_poshl", 15), # set it 21 pix left of current column start
          (store_sub, ":y_pos2", ":y_pos", 500), # set it 21 pix left of current column start
          (position_set_x, pos2, ":line_x"),
          (position_set_y, pos2, ":y_pos2"),
          (overlay_set_position, reg1, pos2),
          (val_add, ":x_poshl", 90),

          (try_begin),
            (eq, "$cheat_mode", 1),
            (assign, reg20, ":count"),
            (display_message, "@{!}DEBUG - Drawing line {reg20}"),
          (try_end),
        (try_end),

        # clear the string globals that we'll use
         (str_clear, s9),
    (str_clear, s8),
    (str_clear, s3),
    (str_clear, s60),
    (str_clear, s61),
    (str_clear, s0),

        # Scrollable area (all the next overlay will be contained in this, s0 sets the scrollbar)
        (create_text_overlay, reg1, s0, tf_scrollable_style_2),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 70),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 860),
        (position_set_y, pos1, 527),
        (overlay_set_area_size, reg1, pos1),
        (set_container_overlay, reg1),

        # set base position and size for lines
        (assign, ":line_size", 0),
        (assign, ":y_pos", 0),

        # set base color for line
    (assign, ":line_color", 0x000000),

        # Line faction loop begins here - fetching corresponding informations and printing the line title
        (try_for_range_backwards, ":faction_line", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction_line", slot_faction_state, sfs_active), # continue if active

            # Base position for subheaders
            (assign, ":x_posfhl", 220),

            # Loop other factions (columns)
            (try_for_range, ":faction_column", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":faction_column", slot_faction_state, sfs_active), # continue if active

                (try_begin), # not same faction
                  (neq, ":faction_column", ":faction_line"),

                  (str_store_faction_name, s8, ":faction_column"),

                  # sub-faction excluding current faction line
                  (try_begin),
                      # different from faction line, display status and relation with faction line
                      (neq, ":faction_column", ":faction_line"),
                      (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_line", ":faction_column"),
                      (assign, ":global_diplomatic_status", reg0),
                      (assign, ":extended_diplomatic_status", reg1),

                      (try_begin), # War
                          (eq, ":global_diplomatic_status", -2),
                          (str_store_string, s60, "@War"),
                          (assign, reg60, 0xDD0000),
                          (assign, reg59, 0),
                      (else_try), # Border incident
                          (eq, ":global_diplomatic_status", -1),
                          (str_store_string, s60, "@Casus Belli"),
                          (assign, reg60, 0xDD8000),
                          (assign, reg59, ":extended_diplomatic_status"),
                      (else_try), # Peace
                          (eq, ":global_diplomatic_status", 0),
                          (str_store_string, s60, "@Peace"),
                          (assign, reg60, 0xFFFFFF),
                          (assign, reg59, 0),
                      (else_try), # Truce (non aggression)
                          (eq, ":global_diplomatic_status", 1),
                          (str_store_string, s60, "@Truce"),
                          (assign, reg60, 0xDDDDDD),
                          (assign, reg59, ":extended_diplomatic_status"),

                          # for Diplomacy, comment if not using
                          (try_begin),
                              (ge, ":extended_diplomatic_status", 61),
                              (str_store_string, s60, "@Alliance"),
                              (assign, reg60, 0x00FF00),
                              (store_sub, reg59, ":extended_diplomatic_status", 60),
                          (else_try),
                              (ge, ":extended_diplomatic_status", 41),
                              (str_store_string, s60, "@Defense"),
                              (assign, reg60, 0x00FFAA),
                              (store_sub, reg59, ":extended_diplomatic_status", 40),
                          (else_try),
                              (ge, ":extended_diplomatic_status", 21),
                              (str_store_string, s60, "@Trade"),
                              (assign, reg60, 0x00FFCC),
                              (store_sub, reg59, ":extended_diplomatic_status", 20),
                          (try_end),
                      (try_end),

                      (val_add, ":x_poshl", 50),

                      # diplomatic status and duration block (set at current line)
                      (create_text_overlay, reg10, s60, tf_left_align|tf_with_outline),
                      (overlay_set_size, reg10, ":line_size"),
                      (overlay_set_color, reg10, reg60),
                      (store_sub, ":line_x", ":x_posfhl", 20),
                      (store_add, ":line_y", ":y_pos", 54),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),

                      (create_text_overlay, reg10, "@{reg59?{reg59} days:}", tf_center_justify),
                      (overlay_set_size, reg10, ":line_size"),
                      (store_add, ":line_y", ":y_pos", 36),
                      (store_add, ":line_x", ":x_posfhl", 10),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),


                      # add diplomatic status
                      (store_relation, ":kingdom_relation", ":faction_line", ":faction_column"),

                      # kingdom relation (same line as faction name)
                      (assign, reg61, ":kingdom_relation"),
                      (create_text_overlay, reg10, "@{reg61}", tf_center_justify),
                      (overlay_set_size, reg10, ":line_size"),

                      (store_add, ":line_y", ":y_pos", 18),
                      (store_add, ":line_x", ":x_posfhl", 10),
                      (position_set_x, pos3, ":line_x"),
                      (position_set_y, pos3, ":line_y"),
                      (overlay_set_position, reg10, pos3),
                  (try_end), # end select alternate display
                (try_end),

                # increase column x position
                (val_add, ":x_posfhl", 90), # valid values 220, 385, 550, 715
            (try_end), # end of column faction loop

            # Faction line information, this is a 4 line block
            # reset x postion for next beginning column and decrease y position according to line count
            (assign, ":x_poshl", 165),

            (val_add, ":y_pos", 54), # linebreak

            # create a separator for faction line
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_color, reg1, 0x000000),
            (position_set_x, pos1, 42000),
            (position_set_y, pos1, 60),
            (overlay_set_size, reg1, pos1),
            (position_set_x, pos1, 17),
            (store_add, ":line_y", ":y_pos", 20), # set it 20 pix above current line
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg1, pos1),

            # Set line title
            (str_store_faction_name, s9, ":faction_line"),
            (str_store_string, s1, "@{s9}"),
            (create_text_overlay, reg10, s1, tf_left_align|tf_with_outline),
            (faction_get_color, ":faction_color", ":faction_line"),
            (overlay_set_color, reg10, ":faction_color"),

            (position_set_x, pos3, 750),
            (position_set_y, pos3, 850),
            (overlay_set_size, reg10, pos3),

            (position_set_x, pos3, 10),
            (position_set_y, pos3, ":y_pos"),
            (overlay_set_position, reg10, pos3),

            # set position for columns
            (assign, ":x_poshl", 165),
            (assign, ":line_size", 0),
            (position_set_x, ":line_size", 700),
            (position_set_y, ":line_size", 800),

            ## Player relation (first column)
            (store_relation, reg1, "fac_player_supporters_faction", ":faction_line"),

            # no clean strings existing, doing it the same way it's done in game_menu
            (try_begin),
                (ge, reg1, 90),
                (str_store_string, s3, "@Loyal"),
            (else_try),
                (ge, reg1, 80),
                (str_store_string, s3, "@Devoted"),
            (else_try),
                (ge, reg1, 70),
                (str_store_string, s3, "@Fond"),
            (else_try),
                (ge, reg1, 60),
                (str_store_string, s3, "@Gracious"),
            (else_try),
                (ge, reg1, 50),
                (str_store_string, s3, "@Friendly"),
            (else_try),
                (ge, reg1, 40),
                (str_store_string, s3, "@Supportive"),
            (else_try),
                (ge, reg1, 30),
                (str_store_string, s3, "@Favorable"),
            (else_try),
                (ge, reg1, 20),
                (str_store_string, s3, "@Cooperative"),
            (else_try),
                (ge, reg1, 10),
                (str_store_string, s3, "@Accepting"),
            (else_try),
                (ge, reg1, 0),
                (str_store_string, s3, "@Indifferent"),
            (else_try),
                (ge, reg1, -10),
                (str_store_string, s3, "@Suspicious"),
            (else_try),
                (ge, reg1, -20),
                (str_store_string, s3, "@Grumbling"),
            (else_try),
                (ge, reg1, -30),
                (str_store_string, s3, "@Hostile"),
            (else_try),
                (ge, reg1, -40),
                (str_store_string, s3, "@Resentful"),
            (else_try),
                (ge, reg1, -50),
                (str_store_string, s3, "@Angry"),
            (else_try),
                (ge, reg1, -60),
                (str_store_string, s3, "@Hateful"),
            (else_try),
                (ge, reg1, -70),
                (str_store_string, s3, "@Revengeful"),
            (else_try),
                (str_store_string, s3, "@Vengeful"),
            (try_end),

            # Set relation to player numerical value (same line)
            (create_text_overlay, reg10, "@{reg1}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (store_add, ":line_x", ":x_poshl", 20),
            (position_set_x, pos1, ":line_x"),
            (position_set_y, pos1, ":y_pos"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, ":line_color"),

            # Set relation to player string value (second line)
            (create_text_overlay, reg10, "@{s3}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, ":line_x"),
            (store_sub, ":line_y", ":y_pos", 20),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, ":line_color"),

            # Set Faction Coat of Arm for standard faction (left of relation string)
            (try_begin),
                (neq, ":faction_line", "fac_player_supporters_faction"),
                (store_sub, ":mesh_index", ":faction_line", kingdoms_begin),
                (val_add, ":mesh_index", "mesh_pic_recruits"),
                (create_mesh_overlay, reg10, ":mesh_index"),
                (position_set_x, pos1, 75),
                (position_set_y, pos1, 75),
                (overlay_set_size, reg10, pos1),
                (position_set_x, pos1, 165),
                (store_sub, ":line_y", ":y_pos", 37),
                (position_set_y, pos1, ":line_y"),
                (overlay_set_position, reg10, pos1),
            (try_end),

            # for current line_faction count lords and centers
            (assign, ":num_lords", 0),
            (assign, ":num_caravans", 0),
            (assign, ":num_centers", 0),
            (assign, ":unassigned_centers", 0),
            (try_for_parties, ":cur_party"),
                (store_faction_of_party, ":cur_faction", ":cur_party"),
                (eq, ":cur_faction", ":faction_line"),

                (try_begin),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
                    (val_add, ":num_lords", 1),
                (else_try),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_caravan),
                    (val_add, ":num_caravans", 1),
                (else_try),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_town),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_castle),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_village),
                    (val_add, ":num_centers", 1),

                    (try_begin),
                        (party_slot_eq, ":cur_party", slot_town_lord, stl_unassigned),
                        (val_add, ":unassigned_centers", 1),
                    (try_end),
                (try_end),
            (try_end), # end of parties loop

            # Count prisoners
            (assign, ":prisoners", 0),
            (try_for_range, ":lord_id", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":lord_id", slot_troop_occupation, slto_kingdom_hero),
                (troop_slot_ge, ":lord_id", slot_troop_prisoner_of_party, 0),
                (store_troop_faction, ":lord_faction", ":lord_id"),
                (eq, ":lord_faction", ":faction_line"),
                (val_add, ":prisoners", 1),
            (try_end),

            # add count to last line for faction line report (second, third and fourth line)
            (assign, reg61, ":num_centers"),
            (assign, reg58, ":unassigned_centers"),
            (create_text_overlay, reg10, "@{reg61} {reg58?({reg58} U) :}Centers", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (store_sub, ":line_y", ":y_pos", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            (assign, reg62, ":num_caravans"),
            (create_text_overlay, reg10, "@{reg62} Caravans", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            (assign, reg60, ":num_lords"),
            (assign, reg59, ":prisoners"),
            (create_text_overlay, reg10, "@{reg60} {reg59?({reg59} P) :}Lords", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, 0x000000),

            # increase line for next faction block
            (val_add, ":y_pos", 18),#linebreak

        (try_end), # end of faction loop
        (set_container_overlay, -1),
   ]),
   ## END on load trigger

   ## Check for buttonpress
   (ti_on_presentation_event_state_change,
    [
    (store_trigger_param_1, ":button_pressed_id"),
    (try_begin),
         (eq, ":button_pressed_id", "$g_jrider_faction_report_return_to_menu"), # pressed  (Return to menu)
        (presentation_set_duration, 0),
    (try_end),
    ]),
   ## END presentation event state change trigger

   ## Event to process when running the presentation
   (ti_on_presentation_run,
    [
        (try_begin),
          (this_or_next|key_clicked, key_escape),
          (key_clicked, key_right_mouse_button),
          (presentation_set_duration, 0),
          (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
   ])
