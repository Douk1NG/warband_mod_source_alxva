# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

tournament_participants_menu = [
(
    "tournament_participants",0,
    "You ask one of the criers for the names of the tournament participants. They are:^{s11}",
    "none",
    [
        (str_clear, s11),
        (call_script, "script_sort_tournament_participant_troops"),
        (call_script, "script_get_num_tournament_participants"),
        (assign, ":num_participants", reg0),
        (try_for_range, ":cur_slot", 0, ":num_participants"),
          (troop_get_slot, ":troop_no", "trp_tournament_participants", ":cur_slot"),
          (str_store_troop_name, s12, ":troop_no"),
          (str_store_string, s11, "@{!}{s11}^{s12}"),
        (try_end),
        ],
    [
      ("go_back_dot", [], "Go back.",
       [(jump_to_menu, "mnu_town_tournament"),
        ]),
    ]
  )
]
