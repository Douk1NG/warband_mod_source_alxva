# ======================================================================
# SHARED DEPENDENCY
# Entity: camp_cheat (menu)
# Called by menus in 2 domains: camp, cheats
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_menu = [
("camp_cheat",0,
   "Select a cheat:",
   "none",
   [ # Character preview
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
      ("camp_cheat_find_item",[], "Find an item...",
       [(jump_to_menu, "mnu_cheat_find_item"),]
       ),

      ("camp_cheat_player_stats",[],"Player stats...",
       [(jump_to_menu, "mnu_camp_cheat_player_stats"),]
       ),

      ("camp_cheat_party",[],"Party cheats...",
       [(jump_to_menu, "mnu_camp_cheat_party"),]
       ),

      ("camp_cheat_world",[],"World cheats...",
       [(jump_to_menu, "mnu_camp_cheat_world"),]
       ),

      ("camp_cheat_player",[],"Player & Kingdom cheats...",
       [(jump_to_menu, "mnu_camp_cheat_player_kingdom"),]
       ),

      ("camp_cheat_debug",[],"Debug tools...",
       [(jump_to_menu, "mnu_camp_cheat_debug"),]
       ),

      ("camp_fuck_1",[(ge, "$cheat_mode", 1),(ge, "$g_sexual_content", 1)],"Fuck Test",
       [(jump_to_menu, "mnu_fuck"),
        ]
       ),

      ("back_to_camp_menu",[],"Back to camp menu.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
