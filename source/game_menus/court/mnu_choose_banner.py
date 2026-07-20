# ======================================================================
# SHARED DEPENDENCY
# Entity: choose_banner (menu)
# Called by menus in 2 domains: camp, character_creation
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

choose_banner_menu = [
(
    "choose_banner",0,
    "Members of the nobility are each granted the right to carry their own banner. {s1} can either choose between the preset banners or design a custom banner.",
    "none",
    [
        (try_begin),
            (neq, "$g_edit_banner_troop", "trp_player"),
            (str_store_troop_name, s1, "$g_edit_banner_troop"),
        (else_try),
            (str_store_string, s1, "@You"),
        (try_end),
     ],
    [
      ("select_preset_banner",[],"Choose from preset banners.",
       [
           (jump_to_menu, "mnu_auto_return"),
           (start_presentation, "prsnt_banner_selection"),
        ]
       ),
      ("select_custom_banner",[],"Create a custom banner.",
       [
           (jump_to_menu, "mnu_auto_return"),
           (start_presentation, "prsnt_custom_banner"),
        ]
       ),
      ]
  )
]
