# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

cut_siege_without_fight_menu = [
(
    "cut_siege_without_fight",0,
    "The besiegers let you approach the gates without challenge.",
    "none",
    [],
    [
      ("continue",[],"Continue...",[(try_begin),
                                   (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                                   (eq, "$g_encountered_party_faction", "$players_kingdom"),
                                   (jump_to_menu, "mnu_town"),
                                 (else_try),
                                   (jump_to_menu, "mnu_castle_outside"),
                                 (try_end)]),
      ]
  )
]
