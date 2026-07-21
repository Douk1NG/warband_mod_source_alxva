# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_end_exchanged_with_prisoner_menu = [
(
    "captivity_end_exchanged_with_prisoner",0,
    "After days of imprisonment, you are finally set free {s0}",
    "none",
    [
      (play_cue_track, "track_escape"),

      (try_begin),
		  (party_is_active, "$capturer_party"),
		  (store_faction_of_party, ":capturer_faction", "$capturer_party"),
		  (is_between, ":capturer_faction", kingdoms_begin, kingdoms_end),
		  (store_relation, ":relation_w_player_faction", ":capturer_faction", "fac_player_faction"),
		  (ge, ":relation_w_player_faction", 0),
          (str_store_party_name, s13, "$capturer_party"),
          (str_store_string, s0, "@as {s13} is no longer held by your enemies."),
      (else_try),
          (str_store_string, s0, "@when your captors exchange you with another prisoner."),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:12, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
           (assign, "$g_player_icon_state", pis_normal),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
		   (call_script, "script_simple_remove_disguise"),
           (change_screen_return),
        ]),
    ]
  )
]
