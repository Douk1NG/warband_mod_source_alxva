# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_domestic_policy_menu = [
(
    "dplmc_domestic_policy",0,
    "You can now shape the domestic policy of your kingdom. Do you want to change your policy now?",
    "none",
    [
      (try_begin),
          (eq, "$g_players_policy_set", 1),
          (change_screen_return),
      (try_end),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
    ],
    [
      ("dplmc_yes",[],"Yes, I want to change the domestic policy.",
       [
         (start_presentation, "prsnt_dplmc_policy_management"),
        ]),
      ("dplmc_no",[],"No, I don't want to change the domestic policy.",
       [
         (change_screen_return),
        ]),
     ]
  )
]
