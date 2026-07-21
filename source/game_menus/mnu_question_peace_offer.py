# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

question_peace_offer_menu = [
(
    "question_peace_offer",0,
    "You Receive a Peace Offer^^The {s1} offers you a peace agreement. What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),

      ##diplomacy begin
      (store_relation,  ":relation", "fac_player_supporters_faction", "$g_notification_menu_var1"),
      (try_begin),
        (ge, ":relation", 0),
        (change_screen_return),
      (try_end),
      ##diplomacy end
      ],
    [
      ("peace_offer_accept",[],"Accept",
       [
         (call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (change_screen_return),
        ]),
        ##diplomacy begin
      ("dplmc_peace_offer_terms",[],"Dictate the peace terms",
       [
        (start_presentation, "prsnt_dplmc_peace_terms"),
        ]),
        ##diplomacy end
      ("peace_offer_reject",[],"Reject",
       [
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
         (change_screen_return),
        ]),
     ]
  )
]
