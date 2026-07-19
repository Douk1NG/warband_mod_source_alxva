# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_casus_belli_expired_menu = [
(
    "notification_casus_belli_expired",0,
    "Kingdom Fails to Respond^^The {s1} has not responded to the {s2}'s provocations, and {s3} suffers a loss of face among {reg4?her:his} more bellicose subjects...^",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
	  (faction_get_slot, ":faction_leader", "$g_notification_menu_var1", slot_faction_leader),
      (str_store_troop_name, s3, ":faction_leader"),
	  ##diplomacy start+ use a script for gender
	  #(troop_get_type, reg4, ":faction_leader"),#<- OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
     ##diplomacy end+

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue",
       [
	   (call_script, "script_faction_follows_controversial_policy", "$g_notification_menu_var1", logent_policy_ruler_ignores_provocation),
	   (change_screen_return),
        ]),
     ]
  )
]
