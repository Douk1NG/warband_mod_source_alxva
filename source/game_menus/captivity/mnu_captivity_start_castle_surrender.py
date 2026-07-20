# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_start_castle_surrender_menu = [
(
    "captivity_start_castle_surrender",0,
    "Stub",
    "none",
    [
        (assign, "$g_player_is_captive", 1),
        (assign,"$auto_menu",-1),
        (assign, "$capturer_party", "$g_encountered_party"),
        # (try_begin),
          # (store_random_in_range, ":random_no", -100, 100),
          # (ge, ":random_no", "$g_player_luck"),
          # (assign, "$g_next_menu", "mnu_captivity_castle_taken_prisoner"),
          # (jump_to_menu, "mnu_permanent_damage"),
        # (else_try),
          (jump_to_menu, "mnu_captivity_castle_taken_prisoner"),
        # (try_end),
      ],
    []
  )
]
