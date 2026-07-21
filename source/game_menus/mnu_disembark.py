# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

disembark_menu = [
(
    "disembark",0,
    "Do you wish to disembark?",
    "none",
    [],
    [
      ("disembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_get_position, pos1, "p_main_party"),
        (party_set_position, "p_main_party", pos0),
        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (le, "$g_main_ship_party", 0),
          (set_spawn_radius, 0),
          (spawn_around_party, "p_main_party", "pt_none"),
          (assign, "$g_main_ship_party", reg0),
          (party_set_flags, "$g_main_ship_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_is_ship, 1),
          (str_store_troop_name, s1, "trp_player"),
          (party_set_slot, "$g_main_ship_party", slot_party_ship_type, ":ship_type"),
          (party_set_name, "$g_main_ship_party", "@{s1}'s Ship"),
          (party_set_icon, "$g_main_ship_party", "icon_ship"),
          (party_set_slot, "$g_main_ship_party", slot_party_type, spt_ship),

          (try_begin),
            (eq, ":ship_type", 1),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Longship"),
          (else_try),
            (eq, ":ship_type", 2),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Galley"),
          (else_try),
            (eq, ":ship_type", 3),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Cog"),
          (else_try),
            (eq, ":ship_type", 4),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Dhow"),
          (try_end),


        (try_end),
        (enable_party, "$g_main_ship_party"),
        (party_set_position, "$g_main_ship_party", pos0),
        (party_set_icon, "$g_main_ship_party", "icon_ship_on_land"),
        (assign, "$g_main_ship_party", -1),
        (party_set_slot, "p_main_party", slot_party_ship_type, 0),
        (change_screen_return),
        ]),
      ("disembark_no", [
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 3),
        (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
        (lt, ":dist", 3),
      ], "No.",
       [
        #(map_get_water_position_around_position, pos1, pos0, 6),
        #(party_set_position, "p_main_party", pos2),
        (rest_for_hours_interactive, 1, 20, 1),
        (change_screen_return),
        ]),
    ]
  )
]
