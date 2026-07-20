# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

give_center_to_player_2_menu = [
(
    "give_center_to_player_2",0,
    "With a brief ceremony, you are officially confirmed as the new lord of {s2}{reg3? and its bound village {s4}:}.\
 {reg3?They:It} will make a fine part of your fiefdom.\
 You can now claim the rents and revenues from your personal estates there, draft soldiers from the populace,\
 and manage the lands as you see fit.\
 However, you are also expected to defend your fief and your people from harm,\
 as well as maintaining the rule of law and order.",
    "none",
    [
      (str_store_party_name, s2, "$g_center_to_give_to_player"),
      (assign, reg3, 0),
      (try_begin),
        (party_slot_eq, "$g_center_to_give_to_player", slot_party_type, spt_castle),
        (try_for_range, ":cur_village", villages_begin, villages_end),
          (party_slot_eq, ":cur_village", slot_village_bound_center, "$g_center_to_give_to_player"),
          (str_store_party_name, s4, ":cur_village"),
          (assign, reg3, 1),
        (try_end),
      (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
    ],
  )
]
