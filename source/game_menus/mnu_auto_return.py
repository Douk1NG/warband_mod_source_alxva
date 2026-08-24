# ======================================================================
# SHARED DEPENDENCY
# Entity: auto_return (menu)
# Called by menus in 2 domains: character_creation, court
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

auto_return_menu = [
(
    "auto_return",0,
    "{!}This menu automatically returns to caller.",
    "none",
    [
      (try_begin),
        (eq, "$cstm_open_troop_tree_view", 1),
        (assign, "$cstm_open_troop_tree_view", 0),
        (assign, "$cstm_selected_troop", -1),
        (start_presentation, "prsnt_cstm_choose_troop_tree"),
      (else_try),
        (change_screen_return, 0),
      (try_end),
    ],
    [
    ]
  )
]
