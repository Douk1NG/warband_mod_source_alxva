# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_player_stats_menu = [
("camp_cheat_player_stats",0,
   "Player stats:",
   "none",
   [
     (try_begin),
       (neq, "$g_player_icon_state", pis_ship),
     (assign, "$g_player_icon_state", pis_normal),
        (party_get_slot, ":player_party", "$marshalship"),
        (ge, ":player_party", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
        (try_end),
    ],
    [
      ("camp_cheat_0",[],"{!}Increase player RTR.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_player_right_to_rule", 25),
          (else_try),
            (call_script, "script_change_player_right_to_rule", 3),
          (try_end),
        ]
       ),

      ("camp_cheat_1",[],"{!}Increase player renown.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_troop_renown", "trp_player", 500),
          (else_try),
            (call_script, "script_change_troop_renown", "trp_player", 100),
          (try_end),
        ]
       ),

      ("camp_cheat_2",[],"{!}Increase player honor.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_player_honor", 50),
          (else_try),
            (call_script, "script_change_player_honor", 5),
          (try_end),
        ]
       ),

      ("gender_change", [], "Change player gender.",
       [(store_sub, "$character_gender", 1, "$character_gender"),
        (troop_set_type, "trp_player", "$character_gender"),
        (display_message, "@Your gender has been changed!"),
        ]
       ),

      ("back_to_cheat_menu",[],"Back to cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),]
       ),
      ]
  )
]
