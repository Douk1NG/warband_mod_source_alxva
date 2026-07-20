# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_question_nonaggression_offer_menu = [
(
    "dplmc_question_nonaggression_offer",0,
    "You Receive a Pact Offer^^The {s1} offers you a non-aggression treaty. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("dplmc_nonaggression_offer_accept",[],"Accept",
       [
         (call_script, "script_dplmc_start_nonaggression_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
      ("dplmc_nonaggression_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -2),
         (change_screen_return),
        ]),
     ]
  )
]
