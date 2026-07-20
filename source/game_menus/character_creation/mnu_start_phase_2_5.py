# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

start_phase_2_5_menu = [
("start_phase_2_5",mnf_disable_all_keys,
    "{!}{s16}",
    "none",
    [
      (str_store_party_name, s1, "$g_starting_town"),
      (str_store_string, s16, "$g_journey_string"),
      (call_script, "script_player_arrived"),
    ],
    [
      ("continue",[], "Go find an inn...",
       [
        (jump_to_menu, "mnu_start_phase_3"),
       ]),

    #SB : skip quest
      ("skip_quest",[], "Take a nice long walk outside {s1}...",
       [
        (assign, "$g_starting_town", -1), #this disables the startup merchant from taverns
        #let triggers load first
        (rest_for_hours, 3, 5, 0),
        (assign, "$auto_enter_town", "$current_town"),
        # (start_encounter, "$current_town"),
        (change_screen_return),
       ]),
    ]
  )
]
