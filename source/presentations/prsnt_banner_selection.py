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

banner_selection = ("banner_selection",0,mesh_load_window,[
      (ti_on_presentation_load,
       [(set_fixed_point_multiplier, 1000),
        (str_store_string, s1, "str_banner_selection_text"),
        (create_text_overlay, reg1, s1, tf_center_justify),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 670),
        (overlay_set_position, reg1, pos1),
        (overlay_set_text, reg1, s1),
        # (create_button_overlay, "$g_presentation_obj_banner_selection_1", "@Next Page", tf_center_justify),
        # (position_set_x, pos1, 500),
        # (position_set_y, pos1, 50),
        # (overlay_set_position, "$g_presentation_obj_banner_selection_1", pos1),

        (str_clear, s0),
        (create_text_overlay, reg1, s0, tf_scrollable),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 50),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 850),
        (position_set_y, pos1, 585),
        (overlay_set_area_size, reg1, pos1),
        (set_container_overlay, reg1),

        (assign, ":try_end", banner_meshes_end_minus_one),
        (store_sub, ":num_npc_kingdoms", npc_kingdoms_end, npc_kingdoms_begin), ## CC
        (val_sub, ":try_end", ":num_npc_kingdoms"), #do not allow kingdom banners to be selected
        # (store_mul, ":begin_mesh", 16, "$g_presentation_page_no"),
        # (val_add, ":begin_mesh", banner_meshes_begin),
        # (store_add, ":try_end_2", ":begin_mesh", 16),
        # (val_min, ":try_end", ":try_end_2"),
        # (store_add, "$g_presentation_banner_start", "$g_presentation_obj_banner_selection_1", 1),
        (store_sub, ":num_banners", ":try_end", banner_meshes_begin),
        (store_div, ":num_rows", ":num_banners", 12),
        (store_mod, ":extra_row", ":num_banners", 12),
        (val_min, ":extra_row", 1),
        (val_add, ":num_rows", ":extra_row"),
        (store_mul, ":y_pos", ":num_rows", 150),
        (val_sub, ":y_pos", 15),
        (assign, ":x_pos", 40),

        (assign, "$g_presentation_obj_banner_selection_1", 0),
        (try_for_range, ":cur_banner_mesh", banner_meshes_begin, ":try_end"),
          (create_image_button_overlay, reg1, ":cur_banner_mesh", ":cur_banner_mesh"),
          (position_set_x, pos1, ":x_pos"),
          (position_set_y, pos1, ":y_pos"),
          (overlay_set_position, reg1, pos1),
          (position_set_x, pos1, 60),
          (position_set_y, pos1, 60),
          (overlay_set_size, reg1, pos1),
          (troop_set_slot, "trp_temp_array_a", "$g_presentation_obj_banner_selection_1", reg1),
          (troop_set_slot, "trp_temp_array_b", "$g_presentation_obj_banner_selection_1", ":cur_banner_mesh"),
          (val_add, "$g_presentation_obj_banner_selection_1", 1),
          ## position
          (val_add, ":x_pos", 70),
          (ge, ":x_pos", 70*12+40),
          (assign, ":x_pos", 40),
          (val_sub, ":y_pos", 150),
        (try_end),

        (set_container_overlay, -1),
        (presentation_set_duration, 999999),

        # ####### mouse fix pos system #######
        # (call_script, "script_mouse_fix_pos_ready"),
        # ####### mouse fix pos system #######
        ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        # (try_begin),
          # (eq, ":object", "$g_presentation_obj_banner_selection_1"),
          # (val_add, "$g_presentation_page_no", 1),
          # (val_mod, "$g_presentation_page_no", 9), ## CC
          # (start_presentation, "prsnt_banner_selection"),
        # (else_try),
          ## CC give back the lord's banner ($g_troop_take_back_banner)
          # (try_begin),
            # (gt, "$lord_selected", 0),
            # (troop_get_slot, ":player_cur_banner_spr", "trp_player", slot_troop_banner_scene_prop),
            # (troop_set_slot, "$lord_selected", slot_troop_banner_scene_prop, ":player_cur_banner_spr"),
            # (store_sub, ":cur_banner", ":player_cur_banner_spr", banner_scene_props_begin),
            # (val_add, ":cur_banner", banner_map_icons_begin),
            # (try_begin),
              # (troop_get_slot, ":cur_party", "$lord_selected", slot_troop_leaded_party),
              # (gt, ":cur_party", 0),
              # (party_set_banner_icon, ":cur_party", ":cur_banner"),
            # (try_end),
            # (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
              # (party_slot_eq, ":cur_center", slot_town_lord, "$lord_selected"),
              # (party_set_banner_icon, ":cur_center", ":cur_banner"),
            # (try_end),
          # (try_end),
          # ## CC
          (try_for_range, ":trp_slot_index", 0, "$g_presentation_obj_banner_selection_1"),
            (troop_slot_eq, "trp_temp_array_a", ":trp_slot_index", ":object"),
            (troop_get_slot, ":cur_banner_mesh", "trp_temp_array_b", ":trp_slot_index"),
            (store_sub, ":selected_banner", ":cur_banner_mesh", banner_meshes_begin),
            (store_add, ":selected_banner_map_icon", ":selected_banner", banner_map_icons_begin),
            (try_begin),
              (eq, "$g_edit_banner_troop", "trp_player"),
              (party_set_banner_icon, "p_main_party", ":selected_banner_map_icon"),
            (else_try),
              (troop_get_slot, ":leaded_party", "$g_edit_banner_troop", slot_troop_leaded_party),
              (gt, ":leaded_party", 0),
              (party_is_active, ":leaded_party"),
              (party_set_banner_icon, ":leaded_party", ":selected_banner_map_icon"),
            (try_end),
            (store_add, ":selected_banner_spr", ":selected_banner", banner_scene_props_begin),
            (troop_set_slot, "$g_edit_banner_troop", slot_troop_banner_scene_prop, ":selected_banner_spr"),

            #Correcting banners according to the player banner
            #(assign, ":end_cond", active_npcs_end),
            #(try_for_range, ":cur_troop", original_kingdom_heroes_begin, ":end_cond"),
            #  (troop_slot_eq, ":cur_troop", slot_troop_banner_scene_prop, ":selected_banner_spr"),
            #  (str_store_troop_name, s7, ":cur_troop"),
            #  (display_message, "@DEBUGS : {s7}'s banner is changed"),
            #  (troop_set_slot, ":cur_troop", slot_troop_banner_scene_prop, banner_scene_props_end_minus_one),
            #  (assign, ":end_cond", 0),
            #(try_end),

            (try_begin),
              (gt, "$g_presentation_next_presentation", 0),
              (start_presentation, "$g_presentation_next_presentation"),
            (else_try),
              (presentation_set_duration, 0),
            (try_end),
            # (assign, ":troop_to_change", 0),
            # (assign, ":end_cond", active_npcs_end),
            # (try_for_range, ":cur_troop", active_npcs_begin, ":end_cond"),
              # (troop_slot_eq, ":cur_troop", slot_troop_banner_scene_prop, ":selected_banner_spr"),
              # (assign, ":troop_to_change", ":cur_troop"),
              # (assign, ":end_cond", 0),
              # (troop_set_slot, ":cur_troop", slot_troop_banner_scene_prop, banner_scene_props_end_minus_one),
              # (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
              # (gt, ":cur_party", 0),
              # (party_set_banner_icon, ":cur_party", banner_map_icons_end_minus_one),
            # (try_end),

            (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
              # (try_begin),
                (party_slot_eq, ":cur_center", slot_town_lord, "$g_edit_banner_troop"),
                (party_set_banner_icon, ":cur_center", ":selected_banner_map_icon"),
              # (else_try),
                # (party_slot_eq, ":cur_center", slot_town_lord, ":troop_to_change"),
                # (party_set_banner_icon, ":cur_center", banner_map_icons_end_minus_one),
              # (try_end),
            (try_end),
          (try_end),
        # (try_end),
        ]),
      (ti_on_presentation_run,
       [(try_begin),
          (this_or_next|key_clicked, key_space),
          (this_or_next|key_clicked, key_enter),
          (this_or_next|key_clicked, key_escape),
          (this_or_next|key_clicked, key_back_space),
          (this_or_next|key_clicked, key_xbox_ltrigger),
          (key_clicked, key_xbox_rtrigger),
          (try_begin),
            (gt, "$g_presentation_next_presentation", 0),
            (start_presentation, "$g_presentation_next_presentation"),
          (else_try),
            (presentation_set_duration, 0),
          (try_end),
        (try_end),
        # ####### mouse fix pos system #######
        # (call_script, "script_mouse_fix_pos_run"),
        # ####### mouse fix pos system #######
        ]),
      ])
