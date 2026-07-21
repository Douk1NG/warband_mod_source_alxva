# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

ship_reembark_menu = [
(
    "ship_reembark",0,
    "Do you wish to embark?",
    "none",
    [],
    [
      ("reembark_yes", [
        (party_get_position, pos1, "$g_encountered_party"),
        (map_get_water_position_around_position, pos2, pos1, 3),
        (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
        (lt, ":dist", 3),
        #(neq, "$g_player_icon_state", pis_ship),
        ], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        #(party_get_position, pos1, "p_main_party"),
        #(map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),

        (party_get_slot, ":ship_type", "$g_encountered_party", slot_party_ship_type),
        (party_set_slot, "p_main_party", slot_party_ship_type, ":ship_type"),

        (assign, "$g_main_ship_party", "$g_encountered_party"),
        (disable_party, "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("reembark_no", [], "No.",
       [(change_screen_return),
        ]),
    ]
  )
]
