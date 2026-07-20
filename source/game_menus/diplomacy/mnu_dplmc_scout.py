# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_scout_menu = [
(
    "dplmc_scout",0,
    "Your spy returned from {s10}^^{s11}{s12}",
    "none",
    [
    (set_background_mesh, "mesh_pic_messenger"),
    (str_store_party_name, s10, "$g_notification_menu_var1"),

    (call_script, "script_game_get_center_note", "$g_notification_menu_var1", 0),
    (str_store_string, s11, "@{!}{s0}"),
    (try_begin),
      (this_or_next|is_between, "$g_notification_menu_var1", towns_begin, towns_end),
      (is_between, "$g_notification_menu_var1", castles_begin, castles_end),
      (party_get_slot, ":center_food_store", "$g_notification_menu_var1", slot_party_food_store),
      (call_script, "script_center_get_food_consumption", "$g_notification_menu_var1"),
      (assign, ":food_consumption", reg0),
      (store_div, reg6, ":center_food_store", ":food_consumption"),
      (store_party_size, reg5, "$g_notification_menu_var1"),
      (str_store_string, s11, "@{s11}^^ The current garrison consists of {reg5} men.^The food stock lasts for {reg6} days."),
    (try_end),

    (str_clear, s12),
    (party_get_num_attached_parties, ":num_attached_parties", "$g_notification_menu_var1"),
    (try_begin),#<- dplmc+ unclosed try_begin!
      (gt, ":num_attached_parties", 0),
      (str_store_string, s12, "@^^Additional the following parties are currently inside:^"),
    (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
      (party_get_attached_party_with_rank, ":attached_party", "$g_notification_menu_var1", ":attached_party_rank"),
      (str_store_party_name, s3, ":attached_party"),
      (store_party_size, reg1, ":attached_party"),
      (str_store_string, s12, "@{s12} {s3} with {reg1} troops.^"),
    (try_end),
	##diplomacy start+
	#Add missing try-end for (gt, ":num_attached_parties", 0),
	(try_end),
	##diplomacy end+

    (call_script, "script_update_center_recon_notes", "$g_notification_menu_var1"),
    ],
    [
      ("dplmc_continue",[],"Continue...",
       [
         (change_screen_return),
        ]),
     ]
  )
]
