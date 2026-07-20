# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

draw_d6_side_scripts = [
# "script_draw_d6_side"
# Description: for prsnt_dices_game
# Input:
# Output: none
("draw_d6_side",
   [(store_script_param, ":line", 1),
    (store_script_param, ":column", 2),
    (store_script_param, ":side", 3),#1-6
    #(store_script_param, ":present_obj", 4),
    (assign,":dice_x",220),
    (try_begin),
	    (store_mul,":offset_x",":column",55),
	    (val_add,":dice_x",":offset_x"),
        (assign,":dice_y",380),
        (assign,":offset_y",70),
    (try_end),
    (try_begin),
        (gt,":side",6),
        (val_sub,":side",6),
    (try_end),
	(try_begin),
        (eq, ":line", 1),
            (try_begin),
                (gt,"$g_presentation_obj_1", 0),
			    (overlay_set_display, "$g_presentation_obj_1", 0),
			(try_end),
    (else_try),
        (eq, ":line", 2),
            (try_begin),
                (gt,"$g_presentation_obj_2", 0),
			    (overlay_set_display, "$g_presentation_obj_2", 0),
			(try_end),
		(val_add,":dice_x",25),
        (val_sub, ":dice_y", ":offset_y"),
    (else_try),
        (eq, ":line", 3),
            (try_begin),
                (gt,"$g_presentation_obj_3", 0),
			    (overlay_set_display, "$g_presentation_obj_3", 0),
			(try_end),
		(val_sub,":dice_x",25),
		(val_mul,":offset_y",2),
        (val_sub, ":dice_y", ":offset_y"),
 	(try_end),
	(try_begin),
        (call_script, "script_d6_roll",":side"),
			(try_begin),
                (eq, ":line", 1),
                (create_mesh_overlay, "$g_presentation_obj_1", reg0),
				(assign, ":present_obj", "$g_presentation_obj_1"),
			(else_try),
                (eq, ":line", 2),
				(create_mesh_overlay, "$g_presentation_obj_2", reg0),
				(assign, ":present_obj", "$g_presentation_obj_2"),
			(else_try),
                (eq, ":line", 3),
				(create_mesh_overlay, "$g_presentation_obj_3", reg0),
				(assign, ":present_obj", "$g_presentation_obj_3"),
			(try_end),
        (position_set_x, pos1, ":dice_x"),
        (position_set_y, pos1, ":dice_y"),#380
		(overlay_set_position, ":present_obj", pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 633),
        (overlay_set_size, ":present_obj", pos1),
    (try_end),
 ])
]
