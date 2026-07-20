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

add_troop_to_custom_armor_tableau_scripts = [
#VIKING CONQUEST END
#COMBAT OSP END
#custom armor
#script_add_troop_to_custom_armor_tableau
# INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
# OUTPUT: none
("add_troop_to_custom_armor_tableau",	# NOT USED YET - Pure Somebody code
    [
       (store_script_param, ":troop_no",1),
       (store_mul, ":side", "$g_custom_armor_angle", 60), #add some more sides

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),

	   (cur_tableau_set_override_flags, af_override_weapons),

       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (val_clamp, "$g_custom_armor_angle", 0, anim_walk_forward_crouch - anim_walk_backward),
       (store_add, ":animation", "$g_custom_armor_angle", "anim_walk_backward"),

       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

	   (try_begin), #shouldn't be necessary, it's already on the troop (player character) - good for hand items
         (gt, "$g_current_opened_item_details", -1),
         (cur_tableau_add_override_item, "$g_current_opened_item_details"),
       (try_end),

		(call_script, "script_show_body_on_tableau", ":troop_no"), # force show body item for tattoos, and loins if cenzored
		#custom armor

       (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 155,155,155),
     ])
]
