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

world_map = ("world_map", 0, mesh_load_window, [
        (ti_on_presentation_load,
          [
            (presentation_set_duration, 999999),
            (set_fixed_point_multiplier, 1000),

          ## initialization part begin
            # presentation obj: begin from top left corner
            (assign, ":init_pos_x", 20), # init x
            (assign, ":init_pos_y", 720), # init y

            # world map, X: -180 t0 180  Y: -145 t0 145
            (assign, ":min_map_x", -180*1000),
            (assign, ":max_map_x", 180*1000),
            (assign, ":min_map_y", -145*1000),
            (assign, ":max_map_y", 145*1000),
            # also begin from top left corner
            (assign, ":init_map_x", ":min_map_x"), # init map_x
            (assign, ":init_map_y", ":max_map_y"), # init map_y

            # move length of p_temp_party, total_cols and total_rows
            (assign, ":party_move_length", 2*1000),
            (store_sub, ":total_cols", ":max_map_x", ":min_map_x"),
            (store_sub, ":total_rows", ":max_map_y", ":min_map_y"),
            (val_div, ":total_cols", ":party_move_length"),
            (val_div, ":total_rows", ":party_move_length"),

            # color_block_length
            (assign, ":color_block_length", 4),
            (store_mul, ":color_block_size", ":color_block_length", 50),
            (position_set_x, pos2, ":color_block_size"),
            (position_set_y, pos2, ":color_block_size"),
          ## initialization part end

            (assign, ":pos_x", ":init_pos_x"), # assign to cur pos_x
            (assign, ":pos_y", ":init_pos_y"), # assign to cur pos_y
            (assign, ":map_x", ":init_map_x"), # assign to cur map_x
            (assign, ":map_y", ":init_map_y"), # assign to cur map_y
            ## draw whole map
            (try_for_range, ":unused_rows", 0, ":total_rows"),
              (try_for_range, ":unused_cols", 0, ":total_cols"),
                (assign, ":dest_color", 0xFFFFFF), # default
                (position_set_x, pos3, ":map_x"),
                (position_set_y, pos3, ":map_y"),
                (party_set_position, "p_temp_party", pos3),
                (party_get_current_terrain, ":current_terrain", "p_temp_party"),
                (try_begin),
                  (eq, ":current_terrain", rt_water),
                  (assign, ":dest_color", 0xFFFFFF), # default
                (else_try),
                  (call_script, "script_get_closest_center", "p_temp_party"),
                  (assign, ":nearest_center", reg0),
                  (try_begin),
                    (gt, ":nearest_center", -1),
                    (store_faction_of_party, ":center_faction", ":nearest_center"),
                    (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
                    (faction_get_color, ":dest_color", ":center_faction"),
                  (try_end),
                (try_end),
                (create_mesh_overlay, reg0, "mesh_white_plane"),
                (overlay_set_color, reg0, ":dest_color"),
                (position_set_x, pos1, ":pos_x"),
                (position_set_y, pos1, ":pos_y"),
                (overlay_set_position, reg0, pos1),
                (overlay_set_size, reg0, pos2), # color block size

                ## draw borderlines begin [optional]
                # borderlines length and whidth
                #(store_add, ":line_length", ":color_block_size", 1*50),
                #(assign, ":line_whidth", 1*50),
                # find bound_center
                #(try_begin),
                #  (this_or_next|party_slot_eq, ":nearest_center", slot_party_type, spt_town),
                #  (party_slot_eq, ":nearest_center", slot_party_type, spt_castle),
                #  (assign, ":bound_center", ":nearest_center"), # itself
                #(else_try),
                #  (party_slot_eq, ":nearest_center", slot_party_type, spt_village),
                #  (party_get_slot, ":bound_center", ":nearest_center", slot_village_bound_center),
                #(try_end),
                # compare with the left side color block
                #(try_begin),
                #  (store_sub, ":map_x_2", ":map_x", ":party_move_length"),
                #  (assign, ":map_y_2", ":map_y"),
                #  (position_set_x, pos4, ":map_x_2"),
                #  (position_set_y, pos4, ":map_y_2"),
                #  (party_set_position, "p_temp_party", pos4),
                #  (party_get_current_terrain, ":current_terrain_2", "p_temp_party"),
                #  (try_begin),
                #    (assign, ":continue", 0),
                #    (try_begin),
                #      (neq, ":current_terrain", rt_water),
                #      (neq, ":current_terrain_2", rt_water),
                #      (call_script, "script_get_closest_center", "p_temp_party"),
                #      (assign, ":nearest_center_2", reg0),
                #      (try_begin),
                #        (gt, ":nearest_center_2", -1),
                #        (try_begin),
                #          (this_or_next|party_slot_eq, ":nearest_center_2", slot_party_type, spt_town),
                #          (party_slot_eq, ":nearest_center_2", slot_party_type, spt_castle),
                #         (assign, ":bound_center_2", ":nearest_center_2"), # itself
                #        (else_try),
                #          (party_slot_eq, ":nearest_center_2", slot_party_type, spt_village),
                #          (party_get_slot, ":bound_center_2", ":nearest_center_2", slot_village_bound_center),
                #        (try_end),
                #        (neq, ":bound_center_2", ":bound_center"),
                #        (assign, ":continue", 1),
                #      (try_end),
                #    (else_try),
                #      (neq, ":current_terrain", ":current_terrain_2"),
                #      (this_or_next|eq, ":current_terrain", rt_water),
                #      (eq, ":current_terrain_2", rt_water),
                #      (assign, ":continue", 1),
                #    (try_end),
                #    (eq, ":continue", 1),
                #    (create_mesh_overlay, reg0, "mesh_white_plane"),
                #    (overlay_set_color, reg0, 0),
                #    (position_set_x, pos1, ":pos_x"),
                #    (position_set_y, pos1, ":pos_y"),
                #    (overlay_set_position, reg0, pos1),
                #    (position_set_x, pos1, ":line_whidth"),
                #    (position_set_y, pos1, ":line_length"),
                #    (overlay_set_size, reg0, pos1),
                #  (try_end),
                #(try_end),
                # compare with the under color block
                #(try_begin),
                #  (assign, ":map_x_2", ":map_x"),
                #  (store_sub, ":map_y_2", ":map_y", ":party_move_length"),
                #  (position_set_x, pos4, ":map_x_2"),
                #  (position_set_y, pos4, ":map_y_2"),
                #  (party_set_position, "p_temp_party", pos4),
                #  (party_get_current_terrain, ":current_terrain_2", "p_temp_party"),
                #  (try_begin),
                #    (assign, ":continue", 0),
                #    (try_begin),
                #      (neq, ":current_terrain", rt_water),
                #      (neq, ":current_terrain_2", rt_water),
                #      (call_script, "script_get_closest_center", "p_temp_party"),
                #      (assign, ":nearest_center_2", reg0),
                #      (try_begin),
                #        (gt, ":nearest_center_2", -1),
                #        (try_begin),
                #          (this_or_next|party_slot_eq, ":nearest_center_2", slot_party_type, spt_town),
                #          (party_slot_eq, ":nearest_center_2", slot_party_type, spt_castle),
                #          (assign, ":bound_center_2", ":nearest_center_2"),
                #        (else_try),
                #          (party_slot_eq, ":nearest_center_2", slot_party_type, spt_village),
                #          (party_get_slot, ":bound_center_2", ":nearest_center_2", slot_village_bound_center),
                #        (try_end),
                #        (neq, ":bound_center_2", ":bound_center"),
                #        (assign, ":continue", 1),
                #      (try_end),
                #    (else_try),
                #      (neq, ":current_terrain", ":current_terrain_2"),
                #      (this_or_next|eq, ":current_terrain", rt_water),
                #      (eq, ":current_terrain_2", rt_water),
                #      (assign, ":continue", 1),
                #    (try_end),
                #    (eq, ":continue", 1),
                #    (create_mesh_overlay, reg0, "mesh_white_plane"),
                #    (overlay_set_color, reg0, 0),
                #    (position_set_x, pos1, ":pos_x"),
                #    (position_set_y, pos1, ":pos_y"),
                #    (overlay_set_position, reg0, pos1),
                #    (position_set_x, pos1, ":line_length"),
                #    (position_set_y, pos1, ":line_whidth"),
                #    (overlay_set_size, reg0, pos1),
                #  (try_end),
                #(try_end),
                ## draw borderlines end [optional]

                # offset
                (val_add, ":pos_x", ":color_block_length"),
                (val_add, ":map_x", ":party_move_length"),
              (try_end),
              # offset
              (assign, ":pos_x", ":init_pos_x"),
              (val_sub, ":pos_y", ":color_block_length"),
              (assign, ":map_x", ":init_map_x"),
              (val_sub, ":map_y", ":party_move_length"),
            (try_end),

            ## blocks of centers
            (assign, ":slot_no", 0),
            (try_for_range, ":center_no", centers_begin, centers_end),
              (party_is_active, ":center_no"),
              (party_get_position, pos4, ":center_no"),
              (position_get_x, ":center_x", pos4),
              (position_get_y, ":center_y", pos4),
              (val_sub, ":center_x", ":init_map_x"),
              (val_sub, ":center_y", ":init_map_y"),
              (val_mul, ":center_x", ":color_block_length"),
              (val_mul, ":center_y", ":color_block_length"),
              (val_div, ":center_x", ":party_move_length"),
              (val_div, ":center_y", ":party_move_length"),
              (val_add, ":center_x", ":init_pos_x"),
              (val_add, ":center_y", ":init_pos_y"),
              # offset and size
              (try_begin),
                (party_slot_eq, ":center_no", slot_party_type, spt_town),
                (assign, ":block_size", 8),
                (assign, ":center_type", spt_town),
              (else_try),
                (party_slot_eq, ":center_no", slot_party_type, spt_castle),
                (assign, ":block_size", 4),
                (assign, ":center_type", spt_castle),
              (else_try),
                (party_slot_eq, ":center_no", slot_party_type, spt_village),
                (assign, ":block_size", 2),
                (assign, ":center_type", spt_village),
              (try_end),
              (store_div, ":half_block_size", ":block_size", 2),
              (val_sub, ":center_x", ":half_block_size"),
              (val_sub, ":center_y", ":half_block_size"),
              (val_mul, ":block_size", 50),
              # block
              (create_mesh_overlay, reg0, "mesh_white_plane"),
              (overlay_set_color, reg0, 0),
              (position_set_x, pos1, ":center_x"),
              (position_set_y, pos1, ":center_y"),
              (overlay_set_position, reg0, pos1),
              (position_set_x, pos1, ":block_size"),
              (position_set_y, pos1, ":block_size"),
              (overlay_set_size, reg0, pos1),
              # name
              (str_store_party_name, s1, ":center_no"),
              (create_text_overlay, reg1, s1, tf_center_justify),
              (store_add, ":text_x", ":center_x", 0),
              (store_add, ":text_y", ":center_y", 10),
              (position_set_x, pos1, ":text_x"),
              (position_set_y, pos1, ":text_y"),
              (overlay_set_position, reg1, pos1),
              (overlay_set_display, reg1, 0),
              # slots
              (troop_set_slot, "trp_temp_array_a", ":slot_no", reg0), # overlay id
              (troop_set_slot, "trp_temp_array_b", ":slot_no", ":center_type"), # center type
              (troop_set_slot, "trp_temp_array_c", ":slot_no", reg1), # center name
              (val_add, ":slot_no", 1),
            (try_end),
            (assign, "$temp", ":slot_no"), # record num of slots

            ## blocks of kingdoms
            (create_text_overlay, reg0, "@Factions", tf_vertical_align_center),
            (position_set_x, pos1, 790),
            (position_set_y, pos1, 700),
            (overlay_set_position, reg0, pos1),

            (assign, ":pos_x", 750),
            (assign, ":pos_y", 650),
            (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
              (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
              # color block
              (create_mesh_overlay, reg0, "mesh_white_plane"),
              (faction_get_color, ":dest_color", ":cur_kingdom"),
              (overlay_set_color, reg0, ":dest_color"),
              (position_set_x, pos1, ":pos_x"),
              (position_set_y, pos1, ":pos_y"),
              (overlay_set_position, reg0, pos1),
              # size: 35*25
              (position_set_x, pos1, 35*50),
              (position_set_y, pos1, 25*50),
              (overlay_set_size, reg0, pos1),
              # kingdom name
              (store_add, ":text_x", ":pos_x", 40),
              (store_add, ":text_y", ":pos_y", 12),
              (str_store_faction_name, s1, ":cur_kingdom"),
              (create_text_overlay, reg0, s1, tf_vertical_align_center),
              (position_set_x, pos1, ":text_x"),
              (position_set_y, pos1, ":text_y"),
              (overlay_set_position, reg0, pos1),
              (position_set_x, pos1, 900),
              (position_set_y, pos1, 900),
              (overlay_set_size, reg0, pos1),
              (val_sub, ":pos_y", 40),
            (try_end),

            ## show centers or not
            # towns
            (create_check_box_overlay, "$g_presentation_obj_1", "mesh_checkbox_off", "mesh_checkbox_on"),
            (position_set_x, pos1, 50),
            (position_set_y, pos1, 110),
            (overlay_set_position, "$g_presentation_obj_1", pos1),
            (overlay_set_val, "$g_presentation_obj_1", 1),
            (create_text_overlay, reg0, "@Show towns", tf_vertical_align_center),
            (position_set_x, pos1, 80),
            (position_set_y, pos1, 120),
            (overlay_set_position, reg0, pos1),
            # castles
            (create_check_box_overlay, "$g_presentation_obj_2", "mesh_checkbox_off", "mesh_checkbox_on"),
            (position_set_x, pos1, 250),
            (position_set_y, pos1, 110),
            (overlay_set_position, "$g_presentation_obj_2", pos1),
            (overlay_set_val, "$g_presentation_obj_2", 1),
            (create_text_overlay, reg0, "@Show castles", tf_vertical_align_center),
            (position_set_x, pos1, 280),
            (position_set_y, pos1, 120),
            (overlay_set_position, reg0, pos1),
            # villages
            (create_check_box_overlay, "$g_presentation_obj_3", "mesh_checkbox_off", "mesh_checkbox_on"),
            (position_set_x, pos1, 450),
            (position_set_y, pos1, 110),
            (overlay_set_position, "$g_presentation_obj_3", pos1),
            (overlay_set_val, "$g_presentation_obj_3", 1),
            (create_text_overlay, reg0, "@Show villages", tf_vertical_align_center),
            (position_set_x, pos1, 480),
            (position_set_y, pos1, 120),
            (overlay_set_position, reg0, pos1),

            (create_text_overlay, reg0, "@Tip: move the mouse onto the black blocks to show their names.", tf_vertical_align_center),
            (position_set_x, pos1, 50),
            (position_set_y, pos1, 95),
            (overlay_set_position, reg0, pos1),
            (position_set_x, pos1, 750),
            (position_set_y, pos1, 750),
            (overlay_set_size, reg0, pos1),

            (create_text_overlay, reg0, "@The World Map", tf_double_space|tf_center_justify),
            (position_set_x, pos1, 380),
            (position_set_y, pos1, 30),
            (overlay_set_position, reg0, pos1),
            (position_set_x, pos1, 2000),
            (position_set_y, pos1, 2000),
            (overlay_set_size, reg0, pos1),

            # Done
            (create_game_button_overlay, "$g_presentation_obj_5", "@Done"),
            (position_set_x, pos1, 900),
            (position_set_y, pos1, 25),
            (overlay_set_position, "$g_presentation_obj_5", pos1),
          ]),

        (ti_on_presentation_mouse_enter_leave,
          [
            (store_trigger_param_1, ":object"),
            (store_trigger_param_2, ":enter_leave"),

            # show center name when mouse on it
            (try_for_range, ":slot_no", 0, "$temp"),
              (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
              (store_sub, ":display_overlay", 1, ":enter_leave"),
              (troop_get_slot, ":cur_overlay", "trp_temp_array_c", ":slot_no"),
              (overlay_set_display, ":cur_overlay", ":display_overlay"),
            (try_end),
          ]),

        (ti_on_presentation_event_state_change,
          [
            (store_trigger_param_1, ":object"),
            (store_trigger_param_2, ":value"),

            (try_begin),
              (eq, ":object", "$g_presentation_obj_1"), # show towns
              (try_for_range, ":slot_no", 0, "$temp"),
                (troop_slot_eq, "trp_temp_array_b", ":slot_no", spt_town),
                (troop_get_slot, ":cur_overlay", "trp_temp_array_a", ":slot_no"),
                (overlay_set_display, ":cur_overlay", ":value"),
              (try_end),
            (else_try),
              (eq, ":object", "$g_presentation_obj_2"), # show castles
              (try_for_range, ":slot_no", 0, "$temp"),
                (troop_slot_eq, "trp_temp_array_b", ":slot_no", spt_castle),
                (troop_get_slot, ":cur_overlay", "trp_temp_array_a", ":slot_no"),
                (overlay_set_display, ":cur_overlay", ":value"),
              (try_end),
            (else_try),
              (eq, ":object", "$g_presentation_obj_3"), # show villages
              (try_for_range, ":slot_no", 0, "$temp"),
                (troop_slot_eq, "trp_temp_array_b", ":slot_no", spt_village),
                (troop_get_slot, ":cur_overlay", "trp_temp_array_a", ":slot_no"),
                (overlay_set_display, ":cur_overlay", ":value"),
              (try_end),
            (else_try),
              (eq, ":object", "$g_presentation_obj_5"),
              (presentation_set_duration, 0),
            (try_end),
          ]),
      ])
