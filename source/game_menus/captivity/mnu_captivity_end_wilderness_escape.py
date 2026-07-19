# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

captivity_end_wilderness_escape_menu = [
(
    "captivity_end_wilderness_escape", mnf_scale_picture,
    "After painful days of being dragged about as a prisoner, you find a chance and escape from your captors!",
    "none",
    [
        (play_cue_track, "track_escape"),
          ##diplomacy start+ test gender with script
        #(troop_get_type, ":is_female", "trp_player"),#<- replaced
        (try_begin),
          #(eq, ":is_female", 1),#<- replaced
          (eq, "$character_gender", tf_female),#<- added
          (set_background_mesh, "mesh_pic_escape_1_fem"),
        (else_try),
          (set_background_mesh, "mesh_pic_escape_1"),
        (try_end),
          ##diplomacy end+
    ],
    [
      ("continue",[],"Continue...",
       [
           (assign, "$g_player_is_captive", 0),
           (try_begin),
             (party_is_active, "$capturer_party"),
             (party_relocate_near_party, "p_main_party", "$capturer_party", 2),
           (try_end),
           (call_script, "script_set_parties_around_player_ignore_player", 8, 12), #it was radius:2 and hours:4, but players make lots of complains about consequent battle losses after releases from captivity then I changed this.
           (try_begin),
             (neq, "$g_player_icon_state", pis_ship),
           (assign, "$g_player_icon_state", pis_normal),
           (try_end),
           (set_camera_follow_party, "p_main_party"),
           (rest_for_hours, 0, 0, 0), #stop resting
           ##diplomacy begin
           #(assign, "$g_move_fast", 1),
           ##diplomacy end
           (change_screen_return),
        ]),
    ]
  )
]
