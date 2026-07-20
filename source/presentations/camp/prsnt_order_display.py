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

order_display = ("order_display", prsntf_read_only,0,[
    (ti_on_presentation_load, [
        (set_fixed_point_multiplier, 1000),

        (try_for_range, ":slot", 0, 9),
          (troop_set_slot, "trp_multiplayer_profile_troop_male", ":slot", -1),  #recycle for order array
        (try_end),

        (assign, ":num_orders", 0),
        (assign, ":y_position", 564),
        (try_begin), #Figure out which orders to display, set strings
			(eq, "$gk_order", 0),
			(str_store_string, s1, "@F5 - Additional formation types"),
			(assign, ":num_orders", 1),
			(assign, ":y_position", 444),	#564 - 4 * 30
        (else_try),
          (eq, "$gk_order", gk_order_2),
          (str_store_string, s1, "@F8 - Memorize div. placement"),
          (str_store_string, s2, "@F9 - Default division placement"),
          (assign, ":num_orders", 2),
          (assign, ":y_position", 354),	#564 - 7 * 30
        (else_try),
			(eq, "$gk_order", gk_order_5),
			(str_store_string, s1, "@F5 - Ranks"),
			(str_store_string, s2, "@F6 - Shieldwall"),
			(str_store_string, s3, "@F7 - Wedge"),
			(str_store_string, s4, "@F8 - Square"),
			(str_store_string, s5, "@F9 - No Formation"),
			(assign, ":num_orders", 5),
        (try_end),
        (assign, "$menu_by_gk_order", "$gk_order"),

        (try_for_range, ":i", 0, ":num_orders"),
          (try_begin),
            (eq, ":i", 0),
            (str_store_string_reg, s0, s1),
          (else_try),
            (eq, ":i", 1),
            (str_store_string_reg, s0, s2),
          (else_try),
            (eq, ":i", 2),
            (str_store_string_reg, s0, s3),
          (else_try),
            (eq, ":i", 3),
            (str_store_string_reg, s0, s4),
          (else_try),
            (eq, ":i", 4),
            (str_store_string_reg, s0, s5),
          (try_end),
          (create_text_overlay, ":overlay", s0),
          (overlay_set_color, ":overlay", 0xFFFFFF),
          (position_set_x, pos1, 1000),
          (position_set_y, pos1, 1000),
          (overlay_set_size, ":overlay", pos1),
          (position_set_x, pos1, 1),
          (position_set_y, pos1, ":y_position"),
          (overlay_set_position, ":overlay", pos1),

          (troop_set_slot, "trp_multiplayer_profile_troop_male", ":i", ":overlay"),
          (val_sub, ":y_position", 30),
        (try_end),
        (store_mul, ":add_back", 30, ":num_orders"),
        (val_add, ":y_position", ":add_back"),
        (val_sub, ":y_position", 4),
        (try_for_range, ":i", 0, ":num_orders"),
          (create_mesh_overlay, ":overlay", "mesh_order_frame"),
          (position_set_x, pos1, 700),
          (position_set_y, pos1, 700),
          (overlay_set_size, ":overlay", pos1),

          (position_set_x, pos1, 0),
          (position_set_y, pos1, ":y_position"),
          (overlay_set_position, ":overlay", pos1),

          (val_sub, ":y_position", 30),
        (try_end),

		(try_begin),
			(neq, "$gk_order", 0),
			(neq, "$gk_order", gk_order_2),
			(create_mesh_overlay, ":overlay", "mesh_white_plane"),
			(overlay_set_color, ":overlay", 0),
			(overlay_set_alpha, ":overlay", 0x10),
			(position_set_x, pos1, 14000),
			(position_set_y, pos1, 6000),
			(overlay_set_size, ":overlay", pos1),

			(position_set_x, pos1, 0),
			(position_set_y, pos1, 468),
			(overlay_set_position, ":overlay", pos1),
		(try_end),

        (presentation_set_duration, 999999),
    ]),

    (ti_on_presentation_run, [
        (store_trigger_param_1, ":cur_time"),
        (gt, ":cur_time", 250), #0.25 Second after Pres. Start
        (try_begin),
		  (this_or_next|game_key_clicked, gk_order_1),
		  (this_or_next|game_key_clicked, gk_order_2),
		  (this_or_next|game_key_clicked, gk_order_3),
		  (this_or_next|game_key_clicked, gk_order_4), #Order Keys not used by Expanded Orders
          (this_or_next|game_key_clicked, gk_view_orders),
          (this_or_next|game_key_clicked, gk_group0_hear),
          (this_or_next|game_key_clicked, gk_group1_hear),
          (this_or_next|game_key_clicked, gk_group2_hear),
          (this_or_next|game_key_clicked, gk_group3_hear),
          (this_or_next|game_key_clicked, gk_group4_hear),
          (this_or_next|game_key_clicked, gk_group5_hear),
          (this_or_next|game_key_clicked, gk_group6_hear),
          (this_or_next|game_key_clicked, gk_group7_hear),
          (this_or_next|game_key_clicked, gk_group8_hear),
          (this_or_next|game_key_clicked, gk_everyone_hear),
          (this_or_next|game_key_clicked, gk_reverse_order_group),
          (game_key_clicked, gk_everyone_around_hear),
          (presentation_set_duration, 0),
        (try_end),
        (try_begin),
          (assign, ":key", -1),
			(try_begin),
				(game_key_clicked, gk_order_5),
				(assign, ":key", 5),
			(else_try),
				(game_key_clicked, gk_order_6),
				(assign, ":key", 6),
			(else_try),
				(game_key_clicked, gk_order_7),
				(assign, ":key", 7),
			(else_try),
				(game_key_clicked, gk_order_8),
				(assign, ":key", 8),
			(else_try),
				(key_clicked, key_f9),
				(assign, ":key", 9),
			(try_end),
          (neq, ":key", -1),
          (try_begin),
            (eq, "$menu_by_gk_order", 0),
            (presentation_set_duration, 0),
          (else_try),
            (eq, "$menu_by_gk_order", gk_order_5),
            (assign, ":min_key", 5),
            (assign, ":max_key", 9),

            (store_sub, ":num_orders", ":max_key", ":min_key"),
            (val_add, ":num_orders", 1),
            (store_sub, ":key_pressed", ":key", ":min_key"),
            (is_between, ":key_pressed", 0, ":num_orders"),
            (try_for_range, ":i", 0, ":num_orders"),
              (troop_get_slot, ":overlay", "trp_multiplayer_profile_troop_male", ":i"),
              (try_begin),
                (neq, ":i", ":key_pressed"),
                (overlay_animate_to_alpha, ":overlay", 400, 0x00),
                (val_add, ":overlay", ":num_orders"),
                (overlay_animate_to_alpha, ":overlay", 400, 0x00),
              (else_try),
                (overlay_animate_to_alpha, ":overlay", 1100, 0x00),
                (val_add, ":overlay", ":num_orders"),
                (overlay_animate_to_alpha, ":overlay", 1100, 0x00),
              (try_end),
            (try_end),
            (presentation_set_duration, 200),
            (close_order_menu),
            (assign, "$native_opening_menu", 0),
          (try_end),
        (try_end),
    ]),
])
